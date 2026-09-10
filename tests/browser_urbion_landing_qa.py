"""Browser acceptance for the public URBION HORIZON landing entrypoint."""
from __future__ import annotations

import os
from pathlib import Path
from playwright.sync_api import expect, sync_playwright

BASE = os.getenv("BASE_URL", "http://127.0.0.1:8765")
ARTIFACT_DIR = Path(os.getenv("URBION_BROWSER_ARTIFACT_DIR", "/tmp/urbion-browser-qa"))
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    errors: list[str] = []
    page_errors: list[str] = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1600, "height": 900}, device_scale_factor=1)
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: page_errors.append(str(exc)))
        page.goto(BASE + "/", wait_until="networkidle", timeout=30_000)
        expect(page).to_have_title("URBION HORIZON — Smarter Places. Stronger Futures.")
        expect(page.locator(".page")).to_have_count(1)
        expect(page.locator(".brand-name")).to_have_text("URBION HORIZON")
        expect(page.locator(".eyebrow")).to_have_text("SPATIAL INTELLIGENCE FOR BETTER URBAN DECISIONS")
        expect(page.locator(".hero h1")).to_contain_text("Smarter Places.")
        expect(page.locator(".hero h1")).to_contain_text("Stronger Futures.")
        expect(page.locator("#enter-platform")).to_be_visible()
        assert page.locator("#urbion-championship-shell").count() == 0
        assert page.locator("#cs-map").count() == 0
        assert page.locator("#cs-project_name").count() == 0
        assert page.evaluate("document.documentElement.scrollWidth - window.innerWidth") <= 2
        page.screenshot(path=ARTIFACT_DIR / "landing-1600x900.png", full_page=True)

        with page.expect_navigation(wait_until="networkidle"):
            page.locator("#enter-platform").click()
        expect(page).to_have_url(BASE + "/championship.html")
        expect(page).to_have_title("URBION HORIZON — Planning Command Centre")
        expect(page.locator("#urbion-championship-shell")).to_have_count(1)
        expect(page.locator("#cs-map")).to_have_count(1)
        expect(page.locator("#cs-project_name")).to_have_count(1)
        assert page.locator(".case-panel").count() == 1
        assert page.locator(".map-panel-canonical").count() == 1
        assert page.locator(".intel-panel").count() == 1
        assert page.locator(".persistent-case").count() == 0
        assert page.locator(".persistent-layers").count() == 0
        page.screenshot(path=ARTIFACT_DIR / "landing-entered-workspace.png", full_page=True)
        assert not errors, errors
        assert not page_errors, page_errors
        browser.close()


if __name__ == "__main__":
    main()
