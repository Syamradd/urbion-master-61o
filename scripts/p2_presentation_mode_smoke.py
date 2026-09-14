#!/usr/bin/env python3
"""P2 presentation-mode contract for the canonical V5 workspace."""
from __future__ import annotations
import os
from playwright.sync_api import sync_playwright

BASE=os.getenv("URBION_BASE_URL","http://127.0.0.1:8000")


def main() -> None:
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page(viewport={"width":1440,"height":900})
        page.goto(BASE+"/workspace",wait_until="domcontentloaded",timeout=30000)
        page.wait_for_selector("#urbionJudgeCard",timeout=15000)
        page.locator("#urbionPresentBtn").click()
        page.wait_for_function("document.body.classList.contains('urbion-present-mode')",timeout=3000)
        assert page.locator(".left").is_hidden()
        assert page.locator(".right").is_hidden()
        assert page.locator("#map").is_visible()
        page.keyboard.press("Escape")
        page.wait_for_function("!document.body.classList.contains('urbion-present-mode')",timeout=3000)
        assert page.locator(".left").is_visible()
        assert page.locator(".right").is_visible()
        assert page.locator("#map").is_visible()
        browser.close()
    print("P2 PRESENTATION MODE PASS")


if __name__=="__main__":
    main()
