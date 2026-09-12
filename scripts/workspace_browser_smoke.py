#!/usr/bin/env python3
"""Deep browser gate for the canonical URBION HORIZON workspace.

This gate verifies the existing product surface; it does not add or invent
parallel UI/function layers. GIS upstream tile failures are recorded
separately because the authoritative services are external to URBION.
"""
from __future__ import annotations
import json, os, sys
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

BASE = os.environ.get("URBION_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
ARTIFACT = Path(os.environ.get("URBION_ARTIFACT_DIR", "artifacts/workspace-browser"))
ARTIFACT.mkdir(parents=True, exist_ok=True)

def check(condition, message):
    if not condition:
        raise AssertionError(message)
    print(f"[ OK ] {message}")

def nearest_sec(page, control_id):
    return page.locator(f"#{control_id}").evaluate("""el=>{let p=el;while(p && !(p.classList&&p.classList.contains('sec')))p=p.parentElement;return p}""")

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
        page.on("requestfailed",on_failed); page.on("response",on_response)
        analysis_requests=[]; copilot_requests=[]; whatif_requests=[]
        page.on("request",lambda r: analysis_requests.append(r.url) if r.url.endswith("/workstation/analysis") else copilot_requests.append(r.url) if r.url.endswith("/copilot/explain") else whatif_requests.append(r.url) if r.url.endswith("/what-if") else None)
        try:
            page.goto(f"{BASE}/workspace", wait_until="domcontentloaded")
            page.wait_for_selector("#map"); page.wait_for_timeout(1800)
            page.wait_for_function("window.__URBION_CANONICAL_UI_V1__===true", timeout=15000)
            check("Planning Workspace" in page.title(),"workspace route/title")
            check(page.locator("#map").is_visible(),"GIS map container visible")
            check(page.evaluate("typeof map!=='undefined' && !!map && typeof map.getCenter==='function'"),"Leaflet map instance initialized")
            check(page.locator("#map .leaflet-tile").count()>=1,"Leaflet tile imagery rendered")
            check(page.locator("#run").is_visible(),"Run Site Analysis visible")

            resources=page.evaluate("performance.getEntriesByType('resource').map(e=>e.name)")
            check(not any(u.endswith('/urbion_workspace_final.js') for u in resources),"legacy workspace bundle not requested")
            for ident in ["landuse1","landuse2","landuse3"]:
                check(page.locator(f"#{ident}").count()==1,f"{ident.upper()} control unique")
            dup_ids=page.evaluate("""()=>{const a=[...document.querySelectorAll('[id]')].map(e=>e.id);const c={};a.forEach(x=>c[x]=(c[x]||0)+1);return Object.entries(c).filter(([,n])=>n>1)}""")
            check(not dup_ids,"no duplicate DOM ids")
            scripts=page.evaluate("""()=>[...document.scripts].map(s=>s.src).filter(Boolean)""")
            expected=["urbion_workspace_bridge.js","urbion_workspace_runtime.js","urbion_layer_runtime_fix.js","urbion_workspace_canonical_ui.js","urbion_workspace_modal_owner.js"]
            check(all(any(x.endswith('/'+e) for x in scripts) for e in expected),"canonical script owners all loaded")
            check(page.evaluate("window.__URBION_CANONICAL_UI_V1__===true"),"canonical UI owner guard active")
            check(page.evaluate("window.__URBION_LAYER_MANAGER__===true"),"single live layer manager guard active")
            check(page.evaluate("window.__URBION_MODAL_OWNER_V1__===true"),"single modal owner guard active")

            gt1=page.locator("#landuse1 option").all_text_contents()
            check(len(gt1)>=10,"GT1 taxonomy populated")
            check(not any(x.strip().lower()=="perdagangan" for x in gt1),"legacy Perdagangan absent")
            for ident in ["landuse1","landuse2","landuse3"]:
                page.locator(f"#{ident}").evaluate("""el=>{let p=el;while(p&&!(p.classList&&p.classList.contains('sec')))p=p.parentElement;if(p?.classList.contains('collapsed'))p.querySelector('.sechead button')?.click();}""")
            check(page.locator("#landuse1").is_visible(),"land-use controls visible")
            page.locator("#landuse1").select_option(label="Komersial")
            check(len(page.locator("#landuse2 option").all_text_contents())>=2,"GT2 cascades")
            page.locator("#landuse2").select_option(index=1)
            check(len(page.locator("#landuse3 option").all_text_contents())>=2,"GT3 cascades")
            sec_before=page.locator("#landuse1").evaluate("""el=>{let p=el;while(p&&!(p.classList&&p.classList.contains('sec')))p=p.parentElement;return p?.classList.contains('collapsed')}""")
            page.locator("#landuse1").evaluate("""el=>{let p=el;while(p&&!(p.classList&&p.classList.contains('sec')))p=p.parentElement;p?.querySelector('.sechead button')?.click();}""")
            page.wait_for_timeout(100)
            sec_after=page.locator("#landuse1").evaluate("""el=>{let p=el;while(p&&!(p.classList&&p.classList.contains('sec')))p=p.parentElement;return p?.classList.contains('collapsed')}""")
            check(sec_after!=sec_before,"section header toggles state once")
            page.locator("#landuse1").evaluate("""el=>{let p=el;while(p&&!(p.classList&&p.classList.contains('sec')))p=p.parentElement;p?.querySelector('.sechead button')?.click();}""")

            for kind in ["street","sat","hybrid"]:
                page.locator(f"[data-base='{kind}']").click(); page.wait_for_timeout(150)
                check(page.locator(f"[data-base='{kind}']").evaluate("e=>e.classList.contains('active')"),f"{kind} base active")
                check(page.evaluate("k=>typeof baseLayers!=='undefined' && map.hasLayer(baseLayers[k])",kind),f"{kind} layer mounted")
            check(page.evaluate("typeof baseLayers!=='undefined' && map.hasLayer(baseLayers.hybrid) && !map.hasLayer(baseLayers.sat) && !map.hasLayer(baseLayers.street)"),"basemap switching removes prior base")

            page.locator("#layerBtn").click(); page.wait_for_timeout(300)
            check(page.locator("#layers").evaluate("e=>e.classList.contains('open')"),"layers opens")
            rows=page.locator("#layerList [data-urbion-layer]"); count=rows.count()
            check(count>=20,f"authoritative live layer catalogue populated ({count})")
            layer_results=[]
            for i in range(count):
                row=rows.nth(i); layer_id=row.get_attribute("data-urbion-layer") or f"layer-{i}"
                row.evaluate("""el=>{const g=el.closest('.layer-group');if(g?.classList.contains('closed'))g.querySelector('.layer-group-head')?.click();}""")
                row.scroll_into_view_if_needed(); row.check(force=True); page.wait_for_timeout(250)
                try:
                    page.wait_for_function("id=>!!window.__URBION_LIVE_LAYERS__?.[id]",arg=layer_id,timeout=6000)
                    page.wait_for_function("""id=>{const l=window.__URBION_LIVE_LAYERS__?.[id];if(!l)return false;const t=Object.keys(l._tiles||{}).length;const d=l._container?.querySelectorAll('img,canvas').length||0;return t>0||d>0}""",arg=layer_id,timeout=6000)
                    state=page.locator(f"[data-layer-state='{layer_id}']").inner_text().strip().upper()
                    check(not state.startswith("ERROR"),f"layer {layer_id} state non-error")
                    check(page.evaluate("id=>{const l=window.__URBION_LIVE_LAYERS__?.[id];return !!l&&map.hasLayer(l)}",layer_id),f"layer {layer_id} mounted on map")
                    check(page.evaluate("id=>{const l=window.__URBION_LIVE_LAYERS__?.[id];if(!l)return false;return Object.keys(l._tiles||{}).length>0||(l._container?.querySelectorAll('img,canvas').length||0)>0}",layer_id),f"layer {layer_id} rendered imagery")
                    layer_results.append({"id":layer_id,"ok":True,"state":state})
                except (AssertionError,PlaywrightTimeoutError) as exc:
                    layer_results.append({"id":layer_id,"ok":False,"error":str(exc)}); raise
                finally:
                    row=page.locator("#layerList [data-urbion-layer]").nth(i)
                    if row.is_checked(): row.uncheck(force=True)
            page.locator("#layerBtn").click(); page.wait_for_timeout(120)
            check(not page.locator("#layers").evaluate("e=>e.classList.contains('open')"),"layers closes")
            check(all(x["ok"] for x in layer_results),f"all {len(layer_results)} live GIS layers render end-to-end")

            page.locator("#map").click(position={"x":420,"y":260}); page.wait_for_timeout(150)
            coords=page.locator("#coords").inner_text().strip()
            check("," in coords and coords!="2.285000, 102.196000","map click updates coordinates")

            analysis_requests.clear(); copilot_requests.clear(); page.locator("#run").click()
            page.wait_for_function("document.querySelector('#run')&&document.querySelector('#run').textContent.includes('RUN SITE ANALYSIS')",timeout=45000)
            check(len(analysis_requests)==1,"one analysis request per Run click")
            check("ANALYSIS COMPLETE" in page.locator("#mapStatus").inner_text(),"site analysis completes")
            check(page.locator("#readyLabel").inner_text().strip()!="PRE-RUN","readiness updates")
            page.wait_for_timeout(800); check(len(copilot_requests)<=1,"zero or one copilot request per analysis")
            if page.locator("#aiSynthesisCard").count():
                check(page.locator("#aiSynthesisCard").is_visible(),"AI synthesis surfaced when available")
                check("SOURCE OF TRUTH" in page.locator("#aiSynthesisCard").inner_text().upper(),"AI source-of-truth boundary surfaced")
            check("AI / COPILOT" in page.locator("#evidenceHealth").inner_text() or len(copilot_requests)==0,"AI evidence state or deterministic fallback surfaced")

            for sel,title in [("#evidenceBtn","EVIDENCE CHAIN"),("#whatifBtn","WHAT-IF SCENARIO"),("#decisionBtn","DECISION SUPPORT"),("#outputBtn","PLANNER-READY OUTPUT")]:
                page.locator(sel).click(); page.wait_for_selector("#modal.show",timeout=6000); check(title in page.locator("#modalTitle").inner_text(),f"{sel} opens expected content"); page.locator("#closeModal").click()

            page.locator("#whatifBtn").click(); page.wait_for_selector("#runWi",timeout=5000)
            page.locator("#wi_ratio").fill("5.0"); page.locator("#wi_height").fill("10")
            n0=len(whatif_requests); page.locator("#runWi").click()
            page.wait_for_function("document.querySelector('#modalTitle')&&document.querySelector('#modalTitle').textContent.includes('WHAT-IF RESULT')",timeout=30000)
            check(len(whatif_requests)>=n0+1,"What-If request reaches backend")
            check("WHAT-IF RESULT" in page.locator("#modalTitle").inner_text(),"What-If result rendered")
            page.locator("#closeModal").click()

            page.wait_for_selector("#runtimeHelp",timeout=10000)
            for sel in ["#runtimeAbout","#runtimeHelp","#runtimeSources","#runtimeStatus","#runtimeFullscreen","#runtimeReset"]:
                check(page.locator(sel).count()==1,f"{sel} injected once")
            for sel in ["#runtimeHelp","#runtimeSources","#runtimeStatus"]:
                page.locator(sel).click(); page.wait_for_selector("#modal.show",timeout=8000); check(page.locator("#modal.show").count()==1,f"{sel} works"); page.locator("#closeModal").click()
            page.locator("#themeBtn").click(); check(page.locator("body").evaluate("e=>e.classList.contains('light')"),"dark/light toggle"); page.locator("#themeBtn").click(); check(not page.locator("body").evaluate("e=>e.classList.contains('light')"),"dark mode restores")
            page.locator("#langBtn").click(); check(page.locator("#langBtn").inner_text().strip()=="BM","BM language toggle"); page.locator("#langBtn").click(); check(page.locator("#langBtn").inner_text().strip()=="EN","EN language toggle")

            for w,h in [(1440,900),(1366,768),(1920,1080)]:
                page.set_viewport_size({"width":w,"height":h}); page.wait_for_timeout(250)
                ov=page.evaluate("({x:document.documentElement.scrollWidth-innerWidth,y:document.documentElement.scrollHeight-innerHeight})")
                check(ov["x"]<=2 and ov["y"]<=2,f"no page overflow at {w}x{h}")
                page.screenshot(path=str(ARTIFACT/f"workspace-{w}x{h}.png"),full_page=True)

            urls=page.evaluate("performance.getEntriesByType('resource').map(e=>e.name)")
            legacy=[u for u in urls if any(x in u.lower() for x in ("premium_v","p20506","championship_frontend","language_bootstrap"))]
            check(not legacy,"no legacy frontend assets requested")
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
        if checks or errors:
            raise AssertionError("; ".join(checks+errors[:5]))
        critical=[x for x in failed if "/workspace" in x or "/urbion_workspace_" in x]
        if critical:
            raise AssertionError("critical browser request failures: "+" | ".join(critical[:10]))
        print("WORKSPACE DEEP BROWSER GATE: PASS")
    return 0

if __name__=="__main__":
    try: raise SystemExit(main())
    except (AssertionError,PlaywrightTimeoutError) as exc:
        print(f"[FAIL] {exc}",file=sys.stderr); raise SystemExit(1)
