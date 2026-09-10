"""Browser acceptance for the current public URBION HORIZON landing entrypoint."""
from __future__ import annotations

import os
from pathlib import Path
from playwright.sync_api import expect, sync_playwright

BASE = os.getenv("BASE_URL", "http://127.0.0.1:8765")
ARTIFACT_DIR = Path(os.getenv("URBION_BROWSER_ARTIFACT_DIR", "/tmp/urbion-browser-qa"))
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

LANDING_TITLE = "URBION HORIZON — Spatial Decision Intelligence"
WORKSPACE_TITLE = "URBION HORIZON — Planning Command Centre"


def main() -> None:
    errors: list[str] = []
    page_errors: list[str] = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1600, "height": 900}, device_scale_factor=1)
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: page_errors.append(str(exc)))

        page.goto(BASE + "/", wait_until="networkidle", timeout=30_000)
        expect(page).to_have_title(LANDING_TITLE)
        expect(page.locator(".hero")).to_have_count(1)
        expect(page.locator(".hero .eyebrow")).to_contain_text("URBION HORIZON")
        expect(page.locator(".hero h1")).to_contain_text("From spatial evidence")
        expect(page.locator(".hero h1")).to_contain_text("to defensible decisions")
        expect(page.locator('a[href="/championship.html"]')).to_be_visible()
        expect(page.locator(".smartcity")).to_be_visible()
        expect(page.locator(".about")).to_have_count(1)
        expect(page.locator(".section .steps")).to_have_count(1)
        assert page.locator("#urbion-championship-shell").count() == 0
        assert page.locator("#cs-map").count() == 0
        assert page.locator("#cs-project_name").count() == 0
        assert page.evaluate("document.documentElement.scrollWidth - window.innerWidth") <= 2
        page.screenshot(path=ARTIFACT_DIR / "landing-1600x900.png", full_page=True)

        with page.expect_navigation(wait_until="networkidle"):
            page.locator('a[href="/championship.html"]').first.click()
        expect(page).to_have_url(BASE + "/championship.html")
        expect(page).to_have_title(WORKSPACE_TITLE)
        expect(page.locator("#urbion-championship-shell")).to_have_count(1)
        expect(page.locator("#cs-map")).to_have_count(1)
        expect(page.locator("#cs-project_name")).to_have_count(1)
        expect(page.locator(".case-panel")).to_have_count(1)
        expect(page.locator(".map-panel-canonical")).to_have_count(1)
        expect(page.locator(".intel-panel")).to_have_count(1)
        expect(page.locator(".persistent-case")).to_have_count(0)
        expect(page.locator(".persistent-layers")).to_have_count(0)
        page.screenshot(path=ARTIFACT_DIR / "landing-entered-workspace.png", full_page=True)

        assert not errors, errors
        assert not page_errors, page_errors
        browser.close()


if __name__ == "__main__":
    main()
