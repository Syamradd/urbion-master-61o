#!/usr/bin/env python3
"""Deep browser gate for the canonical URBION HORIZON workspace."""
from __future__ import annotations
import json, os, sys
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
BASE=os.environ.get("URBION_BASE_URL","http://127.0.0.1:8000").rstrip("/")
ARTIFACT=Path(os.environ.get("URBION_ARTIFACT_DIR","artifacts/workspace-browser")); ARTIFACT.mkdir(parents=True,exist_ok=True)
def check(c,m):
    if not c: raise AssertionError(m)
    print(f"[ OK ] {m}")
def main():
    errors=[]; failed=[]; http=[]; gis_optional=[]; checks=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True)
        page=browser.new_page(viewport={"width":1440,"height":900},device_scale_factor=1)
        page.on("console",lambda m: errors.append(f"console {m.type}: {m.text}") if m.type=="error" and "Failed to load resource: the server responded with a status of 502 (Bad Gateway)" not in m.text else None)
        page.on("pageerror",lambda e: errors.append(f"pageerror: {e}"))
        def on_failed(r):
            item=f"{r.method} {r.url} :: {r.failure}"
            (gis_optional if "/map/wms" in r.url or "/map/arcgis" in r.url else failed).append(item)
        def on_response(r):
            if r.status<400:return
            item=f"{r.status} {r.request.method} {r.url}"
            (gis_optional if "/map/wms" in r.url or "/map/arcgis" in r.url else http).append(item)
        page.on("requestfailed",on_failed)
        page.on("response",on_response)
        analysis_requests=[]; copilot_requests=[]; whatif_requests=[]
        page.on("request",lambda r: analysis_requests.append(r.url) if r.url.endswith("/workstation/analysis") else copilot_requests.append(r.url) if r.url.endswith("/copilot/explain") else whatif_requests.append(r.url) if r.url.endswith("/what-if") else None)
        try:
            page.goto(f"{BASE}/workspace",wait_until="domcontentloaded"); page.wait_for_selector("#map"); page.wait_for_timeout(1800)
            page.wait_for_function("window.__URBION_CANONICAL_UI_V1__===true",timeout=15000)
            check("Planning Workspace" in page.title(),"workspace route/title")
            check(page.locator("#map").is_visible(),"GIS map container visible")
            check(page.evaluate("typeof map!=='undefined' && !!map && typeof map.getCenter==='function'"),"Leaflet map instance initialized")
            check(page.locator("#map .leaflet-tile").count()>=1,"Leaflet tile imagery rendered")
            check(page.locator("#run").is_visible(),"Run Site Analysis visible")
            resources=page.evaluate("performance.getEntriesByType('resource').map(e=>e.name)")
            check(not any(u.endswith('/urbion_workspace_final.js') for u in resources),"duplicate workspace function bundle not requested")
            for id_ in ["landuse1","landuse2","landuse3"]: check(page.locator(f"#{id_}").count()==1,f"{id_.upper()} control unique")
            gt1=page.locator("#landuse1 option").all_text_contents(); check(len(gt1)>=10,"GT1 taxonomy populated"); check(not any(x.strip().lower()=="perdagangan" for x in gt1),"legacy Perdagangan absent")
            for id_ in ["landuse1","landuse2","landuse3"]:
                page.locator(f"#{id_}").evaluate("""el=>{let p=el;while(p&&!(p.classList&&p.classList.contains('sec')))p=p.parentElement;if(p?.classList.contains('collapsed'))p.querySelector('.sechead button')?.click();}""")
            check(page.locator("#landuse1").is_visible(),"land-use controls visible before selection")
            page.locator("#landuse1").select_option(label="Komersial"); check(len(page.locator("#landuse2 option").all_text_contents())>=2,"GT2 cascades")
            page.locator("#landuse2").select_option(index=1); check(len(page.locator("#landuse3 option").all_text_contents())>=2,"GT3 cascades")
            sec_info=page.locator("#landuse1").evaluate("""el=>{let p=el;while(p&&!(p.classList&&p.classList.contains('sec')))p=p.parentElement;return p?{exists:true,collapsed:p.classList.contains('collapsed')}:{exists:false}}""")
            if sec_info["exists"]:
                before=sec_info["collapsed"]; page.locator("#landuse1").evaluate("""el=>{let p=el;while(p&&!(p.classList&&p.classList.contains('sec')))p=p.parentElement;p?.querySelector('.sechead button')?.click();}"""); page.wait_for_timeout(100); after=page.locator("#landuse1").evaluate("""el=>{let p=el;while(p&&!(p.classList&&p.classList.contains('sec')))p=p.parentElement;return p?.classList.contains('collapsed')||false;}"""); check(after!=before,"section header toggles state once"); page.locator("#landuse1").evaluate("""el=>{let p=el;while(p&&!(p.classList&&p.classList.contains('sec')))p=p.parentElement;p?.querySelector('.sechead button')?.click();}""")
            page.locator("[data-base='street']").click(); page.wait_for_timeout(150); check(page.locator("[data-base='street']").evaluate("e=>e.classList.contains('active')"),"street base active"); check(page.evaluate("typeof baseLayers!=='undefined' && map.hasLayer(baseLayers.street)"),"street layer mounted")
            page.locator("[data-base='sat']").click(); page.wait_for_timeout(150); check(page.locator("[data-base='sat']").evaluate("e=>e.classList.contains('active')"),"satellite base active"); check(page.evaluate("typeof baseLayers!=='undefined' && !map.hasLayer(baseLayers.street) && map.hasLayer(baseLayers.sat)"),"basemap switch removes prior layer")
            page.locator("[data-base='hybrid']").click(); page.wait_for_timeout(150); check(page.locator("[data-base='hybrid']").evaluate("e=>e.classList.contains('active')"),"hybrid base active"); check(page.evaluate("typeof baseLayers!=='undefined' && !map.hasLayer(baseLayers.sat) && map.hasLayer(baseLayers.hybrid)"),"hybrid replaces satellite layer")
            page.locator("#layerBtn").click(); page.wait_for_timeout(300); check(page.locator("#layers").evaluate("e=>e.classList.contains('open')"),"layers opens"); layer_rows=page.locator("#layerList [data-urbion-layer]"); layer_count=layer_rows.count(); check(layer_count>=1,"authoritative live layer rows rendered")
            layer_results=[]
            for i in range(layer_count):
                cb=page.locator("#layerList [data-urbion-layer]").nth(i); layer_id=cb.get_attribute("data-urbion-layer") or f"layer-{i}"
                cb.evaluate("""el=>{const g=el.closest('.layer-group');if(g?.classList.contains('closed'))g.querySelector('.layer-group-head')?.click();}""")
                cb.scroll_into_view_if_needed(); cb.check(force=True); page.wait_for_timeout(250)
                try:
                    page.wait_for_function("id=>!!(window.__URBION_LIVE_LAYERS__&&window.__URBION_LIVE_LAYERS__[id])",arg=layer_id,timeout=6000)
                    page.wait_for_function("""id=>{const l=window.__URBION_LIVE_LAYERS__?.[id]; if(!l)return false; const tiles=Number(l._tiles?Object.keys(l._tiles).length:0); const dom=Number(l._container?.querySelectorAll('img,canvas').length||0); return tiles>0||dom>0;}""",arg=layer_id,timeout=6000)
                    state=page.locator(f"[data-layer-state='{layer_id}']").inner_text().strip().upper(); check(not state.startswith("ERROR"),f"layer {layer_id} has no render error"); check(page.evaluate("id=>{const l=window.__URBION_LIVE_LAYERS__?.[id]; return !!l && typeof map!=='undefined' && map.hasLayer(l)}",layer_id),f"layer {layer_id} mounted on map"); check(page.evaluate("id=>{const l=window.__URBION_LIVE_LAYERS__?.[id]; if(!l)return false; const tiles=Number(l._tiles?Object.keys(l._tiles).length:0); const dom=Number(l._container?.querySelectorAll('img,canvas').length||0); return tiles>0||dom>0}",layer_id),f"layer {layer_id} rendered map tiles"); layer_results.append({"id":layer_id,"ok":True,"state":state})
                except (AssertionError,PlaywrightTimeoutError) as exc:
                    layer_results.append({"id":layer_id,"ok":False,"error":str(exc)}); raise
                finally:
                    cb=page.locator("#layerList [data-urbion-layer]").nth(i)
                    if cb.is_checked(): cb.uncheck(force=True); page.wait_for_timeout(100)
            page.locator("#layerBtn").click(); page.wait_for_timeout(120); check(not page.locator("#layers").evaluate("e=>e.classList.contains('open')"),"layers closes"); check(all(x["ok"] for x in layer_results),f"all {len(layer_results)} live GIS layers render end-to-end")
            page.locator("#map").click(position={"x":420,"y":260}); page.wait_for_timeout(160); coords=page.locator("#coords").inner_text().strip(); check("," in coords and coords!="2.285000, 102.196000","map click updates selected coordinates")
            analysis_requests.clear(); copilot_requests.clear(); page.locator("#run").click(); page.wait_for_function("document.querySelector('#run')&&document.querySelector('#run').textContent.includes('RUN SITE ANALYSIS')",timeout=45000); check(len(analysis_requests)==1,"one analysis request per Run click"); check("ANALYSIS COMPLETE" in page.locator("#mapStatus").inner_text(),"site analysis completes"); check(page.locator("#readyLabel").inner_text().strip()!="PRE-RUN","readiness updates"); page.wait_for_timeout(800); check(len(copilot_requests)<=1,"zero or one copilot request per analysis")
            if page.locator("#aiSynthesisCard").count(): check(page.locator("#aiSynthesisCard").is_visible(),"AI synthesis surfaced when available"); check("SOURCE OF TRUTH" in page.locator("#aiSynthesisCard").inner_text().upper(),"AI boundary text surfaced")
            check("AI / COPILOT" in page.locator("#evidenceHealth").inner_text() or len(copilot_requests)==0,"AI evidence status surfaced or deterministic fallback retained")
            for sel,title in [("#evidenceBtn","EVIDENCE CHAIN"),("#whatifBtn","WHAT-IF SCENARIO"),("#decisionBtn","DECISION SUPPORT"),("#outputBtn","PLANNER-READY OUTPUT")]:
                page.locator(sel).click(); page.wait_for_selector("#modal.show",timeout=6000); check(title in page.locator("#modalTitle").inner_text(),f"{sel} opens expected content"); page.locator("#closeModal").click(); page.wait_for_timeout(100)
            page.locator("#whatifBtn").click(); page.wait_for_selector("#wfRun",timeout=4000); page.locator("#wfRatio").fill("5.0"); page.locator("#wfHeight").fill("10"); n0=len(whatif_requests); page.locator("#wfRun").click(); page.wait_for_function("document.querySelector('#modalTitle')&&document.querySelector('#modalTitle').textContent.includes('WHAT-IF RESULT')",timeout=30000); check(len(whatif_requests)>=n0+1,"What-If request completes"); page.locator("#closeModal").click()
            page.wait_for_selector("#runtimeHelp",timeout=10000)
            for sel in ["#runtimeAbout","#runtimeHelp","#runtimeSources","#runtimeStatus","#runtimeFullscreen","#runtimeReset"]: check(page.locator(sel).count()==1,f"{sel} injected once")
            for sel in ["#runtimeHelp","#runtimeSources","#runtimeStatus"]:
                page.locator(sel).click(); page.wait_for_selector("#modal.show",timeout=8000); check(page.locator("#modal.show").count()==1,f"{sel} works"); page.locator("#closeModal").click(); page.wait_for_timeout(100)
            page.locator("#themeBtn").click(); check(page.locator("body").evaluate("e=>e.classList.contains('light')"),"dark/light toggle"); page.locator("#themeBtn").click(); check(not page.locator("body").evaluate("e=>e.classList.contains('light')"),"dark mode restores")
            page.locator("#langBtn").click(); check(page.locator("#langBtn").inner_text().strip()=="BM","BM language toggle"); page.locator("#langBtn").click(); check(page.locator("#langBtn").inner_text().strip()=="EN","EN language toggle")
            for w,h in [(1440,900),(1366,768),(1920,1080)]:
                page.set_viewport_size({"width":w,"height":h}); page.wait_for_timeout(250); ov=page.evaluate("({x:document.documentElement.scrollWidth-innerWidth,y:document.documentElement.scrollHeight-innerHeight})"); check(ov["x"]<=2 and ov["y"]<=2,f"no page overflow at {w}x{h}"); page.screenshot(path=str(ARTIFACT/f"workspace-{w}x{h}.png"),full_page=True)
            urls=page.evaluate("performance.getEntriesByType('resource').map(e=>e.name)"); legacy=[u for u in urls if any(x in u.lower() for x in ("premium_v","p20506","championship_frontend","language_bootstrap"))]; check(not legacy,"no legacy frontend assets requested")
            (ARTIFACT/"layer-results.json").write_text(json.dumps(layer_results,ensure_ascii=False,indent=2),encoding="utf-8")
        except (AssertionError,PlaywrightTimeoutError) as exc:
            checks.append(str(exc)); page.screenshot(path=str(ARTIFACT/"failure-final.png"),full_page=True)
        finally:
            (ARTIFACT/"diagnostics.json").write_text(json.dumps({"http_failures":http,"request_failures":failed,"gis_optional_failures":gis_optional,"console_errors":errors,"check_failures":checks},ensure_ascii=False,indent=2),encoding="utf-8")
            if http: print("HTTP FAILURES:\n"+"\n".join(http[:100]))
            if failed: print("REQUEST FAILURES:\n"+"\n".join(failed[:100]))
            if gis_optional: print("GIS OPTIONAL/UPSTREAM EVENTS:\n"+"\n".join(gis_optional[:100]))
            if errors: print("CONSOLE/JS ERRORS:\n"+"\n".join(errors[:100]))
            if checks: print("CHECK FAILURES:\n"+"\n".join(checks[:100]))
            browser.close()
        if checks or errors: raise AssertionError("; ".join(checks+errors[:5]))
        critical=[x for x in failed if "/workspace" in x or "/urbion_workspace_" in x]
        if critical: raise AssertionError("critical browser request failures: "+" | ".join(critical[:10]))
        print("WORKSPACE DEEP BROWSER GATE: PASS")
    return 0
if __name__=="__main__":
    try: raise SystemExit(main())
    except (AssertionError,PlaywrightTimeoutError) as exc: print(f"[FAIL] {exc}",file=sys.stderr); raise SystemExit(1)
