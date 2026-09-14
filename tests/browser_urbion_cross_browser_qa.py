"""Cross-browser smoke for the canonical URBION HORIZON V5 presentation layer."""
from __future__ import annotations

import os
import re
from pathlib import Path
from playwright.sync_api import expect, sync_playwright

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8765")
BROWSER_NAME = os.getenv("URBION_BROWSER", "chromium")
ARTIFACT_DIR = Path(os.getenv("URBION_BROWSER_ARTIFACT_DIR", "/tmp/urbion-cross-browser"))
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

LANDING_TITLE = "URBION HORIZON — AI-Assisted Urban Planning Intelligence"
WORKSPACE_TITLE = "URBION HORIZON — Planning Workspace"


def main() -> None:
    with sync_playwright() as pw:
        browser_type = getattr(pw, BROWSER_NAME)
        browser = browser_type.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)

        page.goto(BASE_URL + "/", wait_until="networkidle", timeout=30_000)
        expect(page).to_have_title(LANDING_TITLE)
        enter = page.locator('a[href="/workspace"]').first
        expect(enter).to_be_visible()
        heading_text = page.locator(".hero h1").inner_text()
        assert re.sub(r"\s+", " ", heading_text).strip().lower().startswith("from spatial evidence"), heading_text
        enter.click()
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url(BASE_URL + "/workspace")

        expect(page).to_have_title(WORKSPACE_TITLE)
        for selector in (".layout", ".left", ".center", ".right", ".mapwrap", "#map", "#run"):
            expect(page.locator(selector)).to_have_count(1)
        for selector in ("#evidenceBtn", "#whatifBtn", "#decisionBtn", "#outputBtn"):
            expect(page.locator(selector)).to_have_count(1)
            expect(page.locator(selector)).to_be_visible()
        for mode in ("plan", "evidence", "whatif", "decision", "output"):
            button = page.locator(f'.nav button[data-mode="{mode}"]')
            expect(button).to_have_count(1)
            expect(button).to_be_visible()

        page.locator('.nav button[data-mode="output"]').click()
        expect(page.locator("#modal")).to_have_count(1)
        page.locator("#closeModal").click()
        expect(page.locator("#modal")).not_to_have_class("show")
        page.locator('.nav button[data-mode="plan"]').click()
        expect(page.locator("#map")).to_be_visible()

        page.screenshot(path=ARTIFACT_DIR / f"{BROWSER_NAME}-visual-smoke.png", full_page=True)
        browser.close()


if __name__ == "__main__":
    main()
