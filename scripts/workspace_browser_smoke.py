#!/usr/bin/env python3
"""Browser smoke gate for the canonical URBION HORIZON workspace.

Runs against a locally started landing_server.py instance. Focuses on the
judge-facing journey and records exact HTTP failures before failing.
"""
from __future__ import annotations
import os
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

BASE = os.environ.get("URBION_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
ARTIFACT = Path(os.environ.get("URBION_ARTIFACT_DIR", "artifacts/workspace-browser"))
ARTIFACT.mkdir(parents=True, exist_ok=True)

def check(condition: bool, message: str) -> None:
    if not condition: raise AssertionError(message)
    print(f"[ OK ] {message}")

def main() -> int:
    errors=[]; failed_requests=[]; http_failures=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True)
        page=browser.new_page(viewport={"width":1440,"height":900},device_scale_factor=1)
        page.on("console",lambda msg: errors.append(f"console {msg.type}: {msg.text}") if msg.type=="error" else None)
        page.on("pageerror",lambda exc: errors.append(f"pageerror: {exc}"))
        page.on("requestfailed",lambda req: failed_requests.append(f"{req.method} {req.url} :: {req.failure}"))
        page.on("response",lambda res: http_failures.append(f"{res.status} {res.request.method} {res.url}") if res.status>=400 else None)

        page.goto(f"{BASE}/workspace",wait_until="domcontentloaded"); page.wait_for_selector("#map"); page.wait_for_timeout(900)
        check("Planning Workspace" in page.title(),"workspace route/title")
        check(page.locator("#map").is_visible(),"GIS map container visible")
        check(page.locator("#run").is_visible(),"Run Site Analysis visible")
        for id_ in ["landuse1","landuse2","landuse3"]: check(page.locator(f"#{id_}").count()==1,f"{id_.upper()} control present")
        gt1=page.locator("#landuse1 option").all_text_contents(); check(len(gt1)>=10,"current GT1 taxonomy populated"); check(not any(x.strip().lower()=="perdagangan" for x in gt1),"legacy Perdagangan absent")
        page.locator("#landuse1").select_option(label="Komersial"); check(len(page.locator("#landuse2 option").all_text_contents())>=2,"GT2 cascades from GT1")
        page.locator("#landuse2").select_option(index=1); check(len(page.locator("#landuse3 option").all_text_contents())>=2,"GT3 cascades from GT2")
        for selector in ["[data-base='street']","[data-base='sat']","[data-base='hybrid']"]:
            page.locator(selector).click(); page.wait_for_timeout(150); check(page.locator(selector).evaluate("e=>e.classList.contains('active')"),f"basemap {selector} active")
        for button,checkbox in [("#ring400","#context400"),("#ring800","#context800"),("#ring1000","#context1000")]:
            before=page.locator(checkbox).is_checked(); page.locator(button).click(); page.wait_for_timeout(80); check(page.locator(checkbox).is_checked()!=before,f"{button} toggles context ring")
        page.locator("#layerBtn").click(); check(page.locator("#layers").evaluate("e=>e.classList.contains('open')"),"layers drawer opens"); page.locator("#layerBtn").click(); check(not page.locator("#layers").evaluate("e=>e.classList.contains('open')"),"layers drawer closes")
        page.locator("#run").click(); page.wait_for_function("document.querySelector('#run')&&document.querySelector('#run').textContent.includes('RUN SITE ANALYSIS')",timeout=30000)
        check("ANALYSIS COMPLETE" in page.locator("#mapStatus").inner_text(),"site analysis completes"); check(page.locator("#readyLabel").inner_text().strip()!="PRE-RUN","decision readiness updates after analysis")
        page.wait_for_selector("#aiSynthesisCard",timeout=20000); check(page.locator("#aiSynthesisCard").is_visible(),"bounded AI planning synthesis surfaced")
        ai_text=page.locator("#aiSynthesisCard").inner_text(); check("SOURCE OF TRUTH" in ai_text.upper(),"AI synthesis states deterministic source-of-truth boundary"); check("AI / COPILOT" in page.locator("#evidenceHealth").inner_text(),"AI/copilot status surfaced in evidence health")
        for selector,title in [("#evidenceBtn","EVIDENCE CHAIN"),("#whatifBtn","WHAT-IF STUDIO"),("#decisionBtn","DECISION SUPPORT"),("#outputBtn","URBION PLANNER-READY OUTPUT")]:
            page.locator(selector).click(); page.wait_for_timeout(120); check(page.locator("#modal.show").count()==1,f"{selector} opens modal"); check(title in page.locator("#modalTitle").inner_text(),f"{selector} opens expected content"); page.locator("#closeModal").click()
        page.wait_for_selector("#runtimeHelp",timeout=10000)
        for selector in ["#runtimeAbout","#runtimeHelp","#runtimeSources","#runtimeStatus","#runtimeFullscreen","#runtimeReset"]: check(page.locator(selector).count()==1,f"{selector} injected")
        for selector in ["#runtimeHelp","#runtimeSources","#runtimeStatus"]:
            page.locator(selector).click(); check(page.locator("#modal.show").count()==1,f"{selector} works"); page.locator("#closeModal").click()
        page.locator("#themeBtn").click(); check(page.locator("body").evaluate("e=>e.classList.contains('light')"),"dark/light toggle")
        page.locator("#langBtn").click(); check(page.locator("#langBtn").inner_text().strip()=="BM","BM language toggle"); page.locator("#langBtn").click(); check(page.locator("#langBtn").inner_text().strip()=="EN","EN language toggle")
        for width,height in [(1440,900),(1366,768),(1920,1080)]:
            page.set_viewport_size({"width":width,"height":height}); page.wait_for_timeout(200); overflow=page.evaluate("({x:document.documentElement.scrollWidth-innerWidth,y:document.documentElement.scrollHeight-innerHeight})"); check(overflow["x"]<=2 and overflow["y"]<=2,f"no page overflow at {width}x{height}"); page.screenshot(path=str(ARTIFACT/f"workspace-{width}x{height}.png"),full_page=True)
        resource_urls=page.evaluate("performance.getEntriesByType('resource').map(e=>e.name)"); legacy=[u for u in resource_urls if any(token in u.lower() for token in ("premium_v","p20506","championship_frontend","language_bootstrap"))]; check(not legacy,"no legacy frontend assets requested")
        if http_failures: print("HTTP FAILURES:\n"+"\n".join(http_failures[:50]))
        if errors: raise AssertionError("browser console errors: "+" | ".join(errors[:10]))
        if failed_requests:
            critical=[x for x in failed_requests if "/workspace" in x or "/urbion_workspace_" in x]
            if critical: raise AssertionError("critical browser request failures: "+" | ".join(critical[:10]))
        print("WORKSPACE BROWSER SMOKE: PASS"); browser.close()
    return 0

if __name__=="__main__":
    try: raise SystemExit(main())
    except (AssertionError,PlaywrightTimeoutError) as exc: print(f"[FAIL] {exc}",file=__import__('sys').stderr); raise SystemExit(1)
