"""Phase 1 browser contract for plot-ratio presentation."""
from __future__ import annotations
import os
from playwright.sync_api import sync_playwright

BASE = os.getenv("URBION_BASE_URL", "http://127.0.0.1:8000")


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(BASE + "/workspace", wait_until="domcontentloaded")
        page.wait_for_timeout(1200)
        ratio = page.locator("#plot_ratio")
        assert ratio.count() == 1, "plot ratio control missing"
        assert ratio.get_attribute("data-ratio-owner") == "1", "plot ratio presentation owner did not bind"
        assert ratio.get_attribute("type") == "number", "engine input must remain numeric"
        assert ratio.input_value() == "4.5"
        assert page.get_by_text("PLOT RATIO · 1 : X", exact=True).count() == 1
        assert page.get_by_text("1 :", exact=True).count() >= 1
        assert page.get_by_text("4.5 → 1 : 4.5", exact=False).count() == 1
        browser.close()
    print("PLOT RATIO UI CONTRACT PASS")
    print("presentation: 1 : X")
    print("engine_value: 4.5")


if __name__ == "__main__":
    main()
