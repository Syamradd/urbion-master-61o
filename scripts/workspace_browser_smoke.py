#!/usr/bin/env python3
"""Browser smoke gate for the canonical URBION HORIZON workspace.

Runs against a locally started landing_server.py instance. This is deliberately
focused on the judge-facing journey: routing, taxonomy cascade, map controls,
modal navigation, utilities, console/network errors, and desktop overflow.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

BASE = os.environ.get("URBION_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
ARTIFACT = Path(os.environ.get("URBION_ARTIFACT_DIR", "artifacts/workspace-browser"))
ARTIFACT.mkdir(parents=True, exist_ok=True)


def check(page, condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[ OK ] {message}")


def main() -> int:
    errors: list[str] = []
    failed_requests: list[str] = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        page.on("console", lambda msg: errors.append(f"console {msg.type}: {msg.text}") if msg.type == "error" else None)
        page.on("pageerror", lambda exc: errors.append(f"pageerror: {exc}"))
        page.on("requestfailed", lambda req: failed_requests.append(f"{req.method} {req.url} :: {req.failure}"))

        page.goto(f"{BASE}/workspace", wait_until="domcontentloaded")
        page.wait_for_selector("#map")
        page.wait_for_timeout(900)
        check(page, "Planning Workspace" in page.title(), "workspace route/title")
        check(page.locator("#map").is_visible(), "GIS map container visible")
        check(page.locator("#run").is_visible(), "Run Site Analysis visible")
        check(page.locator("#landuse1").count() == 1, "GT1 control present")
        check(page.locator("#landuse2").count() == 1, "GT2 control present")
        check(page.locator("#landuse3").count() == 1, "GT3 control present")

        gt1 = page.locator("#landuse1 option").all_text_contents()
        check(len(gt1) >= 10, "current GT1 taxonomy populated")
        check(not any(x.strip().lower() == "perdagangan" for x in gt1), "legacy Perdagangan absent")
        page.locator("#landuse1").select_option(label="Komersial")
        gt2 = page.locator("#landuse2 option").all_text_contents()
        check(len(gt2) >= 2, "GT2 cascades from GT1")
        page.locator("#landuse2").select_option(index=1)
        gt3 = page.locator("#landuse3 option").all_text_contents()
        check(len(gt3) >= 2, "GT3 cascades from GT2")

        for selector in ["[data-base='street']", "[data-base='sat']", "[data-base='hybrid']"]:
            page.locator(selector).click()
            page.wait_for_timeout(150)
            check(page.locator(selector).evaluate("e => e.classList.contains('active')"), f"basemap {selector} active")

        for button, checkbox in [("#ring400", "#context400"), ("#ring800", "#context800"), ("#ring1000", "#context1000")]:
            before = page.locator(checkbox).is_checked()
            page.locator(button).click()
            page.wait_for_timeout(80)
            check(page.locator(checkbox).is_checked() != before, f"{button} toggles context ring")

        page.locator("#layerBtn").click()
        check(page.locator("#layers").evaluate("e => e.classList.contains('open')"), "layers drawer opens")
        page.locator("#layerBtn").click()
        check(not page.locator("#layers").evaluate("e => e.classList.contains('open')"), "layers drawer closes")

        for selector, title in [("#evidenceBtn", "EVIDENCE CHAIN"), ("#whatifBtn", ""), ("#decisionBtn", ""), ("#outputBtn", "")]:
            page.locator(selector).click()
            page.wait_for_timeout(120)
            check(page.locator("#modal.show").count() == 1, f"{selector} opens modal")
            if title:
                check(title in page.locator("#modalTitle").inner_text(), f"{selector} opens evidence chain")
            page.locator("#closeModal").click()

        # Runtime utility controls are generated after boot.
        for selector in ["#runtimeHelp", "#runtimeSources", "#runtimeStatus"]:
            page.locator(selector).click()
            check(page.locator("#modal.show").count() == 1, f"{selector} works")
            page.locator("#closeModal").click()

        page.locator("#themeBtn").click()
        check(page.locator("body").evaluate("e => e.classList.contains('light')"), "dark/light toggle")
        page.locator("#langBtn").click()
        check(page.locator("#langBtn").inner_text().strip() == "BM", "BM language toggle")
        page.locator("#langBtn").click()
        check(page.locator("#langBtn").inner_text().strip() == "EN", "EN language toggle")

        # Desktop visual overflow gate across the supported judge sizes.
        for width, height in [(1440, 900), (1366, 768), (1920, 1080)]:
            page.set_viewport_size({"width": width, "height": height})
            page.wait_for_timeout(200)
            overflow = page.evaluate("({x:document.documentElement.scrollWidth-innerWidth,y:document.documentElement.scrollHeight-innerHeight})")
            check(overflow["x"] <= 2 and overflow["y"] <= 2, f"no page overflow at {width}x{height}")
            page.screenshot(path=str(ARTIFACT / f"workspace-{width}x{height}.png"), full_page=True)

        # Legacy frontend pollution gate.
        resource_urls = page.evaluate("performance.getEntriesByType('resource').map(e => e.name)")
        legacy = [u for u in resource_urls if any(token in u.lower() for token in ("premium_v", "p20506", "championship_frontend", "language_bootstrap"))]
        check(not legacy, "no legacy frontend assets requested")

        if errors:
            raise AssertionError("browser console errors: " + " | ".join(errors[:10]))
        if failed_requests:
            critical = [x for x in failed_requests if "/workspace" in x or "/urbion_workspace_" in x]
            if critical:
                raise AssertionError("critical browser request failures: " + " | ".join(critical[:10]))
        print("WORKSPACE BROWSER SMOKE: PASS")
        browser.close()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, PlaywrightTimeoutError) as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1)
