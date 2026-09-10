"""Responsive visual acceptance for the public landing and canonical workstation."""
from __future__ import annotations

import os
from pathlib import Path
from playwright.sync_api import expect, sync_playwright

BASE = os.getenv("BASE_URL", "http://127.0.0.1:8765")
ARTIFACT_DIR = Path(os.getenv("URBION_BROWSER_ARTIFACT_DIR", "/tmp/urbion-browser-qa"))
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

LANDING_VIEWPORTS = (375, 390, 430, 768, 820, 1280, 1440, 1600, 1920)
WORKSPACE_VIEWPORTS = (375, 768, 1280, 1600)


def assert_no_horizontal_overflow(page) -> None:
    overflow = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
    assert overflow <= 2, f"horizontal overflow: {overflow}px at {page.viewport_size['width']}px viewport"


def main() -> None:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for width in LANDING_VIEWPORTS:
            page = browser.new_page(viewport={"width": width, "height": 900}, device_scale_factor=1)
            page.goto(BASE + "/", wait_until="networkidle", timeout=30_000)
            expect(page).to_have_title("URBION HORIZON — Smarter Places. Stronger Futures.")
            expect(page.locator(".page")).to_have_count(1)
            expect(page.locator(".hero h1")).to_contain_text("Smarter Places.")
            expect(page.locator("#enter-platform")).to_be_visible()
            expect(page.locator("#about-us")).to_have_count(1)
            expect(page.locator(".team-photo")).to_be_visible()
            assert_no_horizontal_overflow(page)
            page.screenshot(path=ARTIFACT_DIR / f"landing-responsive-{width}.png", full_page=True)
            page.close()

        for width in WORKSPACE_VIEWPORTS:
            page = browser.new_page(viewport={"width": width, "height": 900}, device_scale_factor=1)
            page.goto(BASE + "/championship.html", wait_until="networkidle", timeout=30_000)
            expect(page).to_have_title("URBION HORIZON — Planning Command Centre")
            expect(page.locator("#urbion-championship-shell")).to_have_count(1)
            expect(page.locator("#cs-map")).to_have_count(1)
            expect(page.locator("#cs-project_name")).to_have_count(1)
            expect(page.locator(".nav")).to_be_visible()
            assert_no_horizontal_overflow(page)
            page.screenshot(path=ARTIFACT_DIR / f"workspace-responsive-{width}.png", full_page=True)
            page.close()

        browser.close()


if __name__ == "__main__":
    main()
