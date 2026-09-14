#!/usr/bin/env python3
"""Functional smoke for the canonical URBION HORIZON About surface."""
from __future__ import annotations

import os
from playwright.sync_api import sync_playwright

BASE = os.environ.get("URBION_BASE_URL", "http://127.0.0.1:8765").rstrip("/")


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[ OK ] {message}")


def main() -> None:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        page.goto(f"{BASE}/about", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_selector(".master", timeout=15000)
        check(page.title() == "URBION HORIZON — About Us", "About route/title is canonical")
        check(page.locator(".master").is_visible(), "About master visual is visible")
        check(page.locator("[data-modal]").count() >= 10, "About information/team hotspots are present")
        check(page.locator("[data-href='/workspace']").count() == 1, "About exposes Open Workspace action")

        page.locator("[data-modal='mission']").click()
        page.wait_for_selector("#modal.open", timeout=5000)
        check(page.locator("#modalTitle").inner_text().strip() != "", "Mission modal opens")
        page.locator("#close").click()
        check(not page.locator("#modal").evaluate("e => e.classList.contains('open')"), "Mission modal closes")

        page.locator("[data-modal='syamir']").click()
        page.wait_for_selector("#modal.open", timeout=5000)
        body = page.locator("#modalBody").inner_text()
        check("Muhammad Syamir Aidid" in body, "Syamir team profile is restored and readable")
        page.keyboard.press("Escape")
        check(not page.locator("#modal").evaluate("e => e.classList.contains('open')"), "About modal closes with Escape")

        page.locator("[data-href='/workspace']").click()
        page.wait_for_timeout(400)
        check(page.url.rstrip("/").endswith("/workspace"), "About Open Workspace navigation works")
        check("Planning Workspace" in page.title(), "Open Workspace reaches canonical workspace")
        browser.close()

    print("About functional smoke: PASS")


if __name__ == "__main__":
    main()
