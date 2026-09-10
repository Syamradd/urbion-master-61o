"""Cross-browser smoke for the canonical URBION HORIZON presentation layer.

The test intentionally avoids changing application state beyond theme/language and
uses the same stable planning flow already covered by Chromium acceptance.
"""
from __future__ import annotations

import os
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8765")
BROWSER_NAME = os.getenv("URBION_BROWSER", "chromium")
ARTIFACT_DIR = Path(os.getenv("URBION_BROWSER_ARTIFACT_DIR", "/tmp/urbion-cross-browser"))
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    with sync_playwright() as pw:
        browser_type = getattr(pw, BROWSER_NAME)
        browser = browser_type.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)

        # The public root is the welcome/landing page. The planning workspace is
        # reached through the same user-facing CTA that judges will use.
        page.goto(BASE_URL + "/", wait_until="networkidle", timeout=30_000)
        expect(page).to_have_title("URBION HORIZON — Smarter Places. Stronger Futures.")
        expect(page.locator("#enter-platform")).to_be_visible()
        expect(page.locator(".hero h1")).to_have_text("Smarter Places.Stronger Futures.")
        page.locator("#enter-platform").click()
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url(BASE_URL + "/championship.html")

        expect(page).to_have_title("URBION HORIZON — Planning Command Centre")
        expect(page.locator("#urbion-championship-shell")).to_have_count(1)
        expect(page.locator("#cs-map")).to_have_count(1)
        expect(page.locator(".case-panel")).to_have_count(1)
        expect(page.locator(".map-panel-canonical")).to_have_count(1)
        expect(page.locator(".intel-panel")).to_have_count(1)
        status = page.get_by_role("status")
        expect(status).to_have_count(1)
        expect(status).to_be_visible()
        expect(page.locator(".horizon-metrics")).to_be_visible()

        settings = page.locator("#urbion-settings-btn")
        expect(settings).to_be_visible()
        settings.click()
        panel = page.locator("#urbion-settings-backdrop")
        expect(panel).to_have_class("urbion-settings-backdrop open")
        page.locator('[data-setting-theme="light"]').click()
        expect(page.locator("html")).to_have_class(lambda value: "cs-light" in value.split())
        page.locator('[data-setting-theme="dark"]').click()
        expect(page.locator("html")).not_to_have_class(lambda value: "cs-light" in value.split())
        page.locator(".urbion-settings-close").click()
        expect(panel).not_to_have_class("open")

        # Language cycle is a presentation contract; the main Chromium suite already
        # covers the complete copy audit. Here we ensure the toggle works in each engine.
        lang = page.locator("#cs-lang")
        expect(lang).to_have_count(1)
        before = page.locator("html").get_attribute("lang")
        lang.click()
        page.wait_for_timeout(700)
        after = page.locator("html").get_attribute("lang")
        assert before != after, (before, after)
        lang.click()
        page.wait_for_timeout(700)
        assert page.locator("html").get_attribute("lang") == before

        nav = page.get_by_role("navigation")
        expect(nav).to_have_count(1)
        expect(nav).to_be_visible()
        for tab in ("site", "ai", "whatif", "decision", "lcp", "output"):
            button = page.locator(f'.workbench-nav button[data-tab="{tab}"]')
            expect(button).to_have_count(1)
            button.click()
            expect(page.locator("#cs-content")).not_to_have_text("Planning case not defined")

        # Visual density: the canonical right-hand intelligence stack must stay populated.
        intel_text = page.locator(".intel-panel").inner_text()
        assert len(intel_text) >= 120, len(intel_text)
        assert "Evidence" in intel_text or "EVIDENCE" in intel_text

        # Decision/policy surface exists independently from the final score value.
        page.locator('.workbench-nav button[data-tab="decision"]').click()
        decision_text = page.locator("#cs-content").inner_text()
        assert "RECOMMENDED OPTION" in decision_text
        assert "POLICY" in decision_text
        assert "PLANNER" in decision_text

        page.screenshot(path=ARTIFACT_DIR / f"{BROWSER_NAME}-visual-smoke.png", full_page=True)
        browser.close()


if __name__ == "__main__":
    main()
