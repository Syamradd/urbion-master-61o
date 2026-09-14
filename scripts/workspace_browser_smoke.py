#!/usr/bin/env python3
"""Deep browser gate for the canonical URBION HORIZON workspace."""
from __future__ import annotations
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = os.environ.get("URBION_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
ARTIFACT = Path(os.environ.get("URBION_ARTIFACT_DIR", "artifacts/workspace-browser"))
ARTIFACT.mkdir(parents=True, exist_ok=True)


def check(condition, message):
    if not condition:
        raise AssertionError(message)
    print(f"[ OK ] {message}")


def row_control(page, label_text):
    rows = page.locator(".sec .row").filter(has_text=label_text)
    for i in range(rows.count()):
        row = rows.nth(i)
        visible = row.locator("input:visible,select:visible,textarea:visible").first
        if visible.count():
            return visible
    return rows.first.locator("input,select,textarea").first


def usable_options(control):
    return [x for x in control.locator("option").all_text_contents() if x.strip() and not x.strip().lower().startswith("select")]


def fill_first_option(control):
    options = usable_options(control)
    if not options:
        raise AssertionError(f"no usable options for control {control}")
    control.select_option(label=options[0])
    return options[0]


def prepare_ready_case(page):
    row_control(page, "PROJECT / SITE NAME").fill("Browser Gate Planning Case")

    state = row_control(page, "STATE")
    if state.evaluate("el=>el.tagName") == "SELECT":
        state.select_option(label="Melaka")
    else:
        state.fill("Melaka")
    page.wait_for_timeout(300)

    district = row_control(page, "DISTRICT")
    if district.evaluate("el=>el.tagName") == "SELECT":
        opts = usable_options(district)
        if opts:
            district.select_option(label=opts[0])
    else:
        district.fill("Melaka Tengah")
    page.wait_for_timeout(300)

    pbt = row_control(page, "LOCAL AUTHORITY")
    if pbt.evaluate("el=>el.tagName") == "SELECT":
        opts = usable_options(pbt)
        if opts:
            pbt.select_option(label=opts[0])
    else:
        pbt.fill("Majlis Bandaraya Melaka Bersejarah")

    page.locator("#site_lat").fill("2.285000")
    page.locator("#site_lon").fill("102.196000")

    for label in ["DEVELOPMENT TYPE", "DEVELOPMENT CLASS"]:
        control = row_control(page, label)
        if control.evaluate("el=>el.tagName") == "SELECT":
            fill_first_option(control)
        else:
            control.fill("General")
        page.wait_for_timeout(150)

    page.locator("#landuse1").select_option(label="Komersial")
    page.wait_for_timeout(200)
    fill_first_option(page.locator("#landuse2"))
    page.wait_for_timeout(200)
    fill_first_option(page.locator("#landuse3"))
    page.wait_for_timeout(250)

    ready = page.evaluate("""()=>{
      const pick=label=>[...document.querySelectorAll('.sec .row')]
        .find(r=>r.querySelector('.lab')?.textContent.toLowerCase().includes(label.toLowerCase()))
        ?.querySelector('input:visible,select:visible,textarea:visible');
      const controls=[
        pick('project / site name'),pick('state'),pick('district'),pick('local authority'),
        document.querySelector('#site_lat'),document.querySelector('#site_lon'),
        pick('development type'),pick('development class'),
        document.querySelector('#landuse1'),document.querySelector('#landuse2'),document.querySelector('#landuse3')
      ].filter(Boolean);
      return {filled:controls.filter(c=>String(c.value||'').trim()!=='').length,total:controls.length};
    }""")
    check(ready["total"] >= 11 and ready["filled"] == ready["total"], f"planning case fixture is complete ({ready['filled']}/{ready['total']})")
    page.wait_for_function("document.querySelector('#run') && !document.querySelector('#run').disabled", timeout=10000)
    check(not page.locator("#run").is_disabled(), "Run Site Analysis unlocked by canonical readiness")


def main():
    console_errors = []
    failed = []
    http = []
    gis_optional = []
    checks = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        page.on("console", lambda m: console_errors.append(f"console {m.type}: {m.text}") if m.type == "error" and "Failed to load resource: the server responded with a status of 502 (Bad Gateway)" not in m.text else None)
        page.on("pageerror", lambda e: console_errors.append(f"pageerror: {e}"))

        def on_failed(request):
            item = f"{request.method} {request.url} :: {request.failure}"
            (gis_optional if "/map/wms" in request.url or "/map/arcgis" in request.url else failed).append(item)

        def on_response(response):
            if response.status < 400:
                return
            item = f"{response.status} {response.request.method} {response.url}"
            (gis_optional if "/map/wms" in response.url or "/map/arcgis" in response.url else http).append(item)

        page.on("requestfailed", on_failed)
        page.on("response", on_response)
        analysis_requests = []
        copilot_requests = []
        whatif_requests = []

        def on_request(request):
            if request.url.endswith("/workstation/analysis"):
                analysis_requests.append(request.url)
            elif request.url.endswith("/copilot/explain"):
                copilot_requests.append(request.url)
            elif request.url.endswith("/what-if"):
                whatif_requests.append(request.url)

        page.on("request", on_request)

        try:
            page.goto(f"{BASE}/workspace", wait_until="domcontentloaded")
            page.wait_for_selector("#map")
            page.wait_for_timeout(1800)
            page.wait_for_function("window.__URBION_CANONICAL_UI_V1__===true", timeout=15000)

            check("Planning Workspace" in page.title(), "workspace route/title")
            check(page.locator("#map").is_visible(), "GIS map container visible")
            check(page.evaluate("typeof map!=='undefined' && !!map && typeof map.getCenter==='function'"), "Leaflet map instance initialized")
            check(page.locator("#map .leaflet-tile").count() >= 1, "Leaflet tile imagery rendered")
            check(page.locator("#run").is_visible(), "Run Site Analysis visible")
            resources = page.evaluate("performance.getEntriesByType('resource').map(e=>e.name)")
            check(not any(u.endswith("/urbion_workspace_final.js") for u in resources), "legacy workspace bundle not requested")

            for ident in ["landuse1", "landuse2", "landuse3"]:
                check(page.locator(f"#{ident}").count() == 1, f"{ident.upper()} control unique")
            dup_ids = page.evaluate("""()=>{const a=[...document.querySelectorAll('[id]')].map(e=>e.id);const c={};a.forEach(x=>c[x]=(c[x]||0)+1);return Object.entries(c).filter(([,n])=>n>1)}""")
            check(not dup_ids, "no duplicate DOM ids")

            scripts = page.evaluate("[...document.scripts].map(s=>s.src).filter(Boolean)")
            expected = [
                "urbion_workspace_bridge.js",
                "urbion_workspace_runtime.js",
                "urbion_layer_runtime_fix.js",
                "urbion_workspace_canonical_ui.js",
                "urbion_workspace_modal_owner.js",
                "urbion_workspace_pbt_catalog.js",
            ]
            check(all(any(x.endswith("/" + e) for x in scripts) for e in expected), "canonical script owners all loaded")
            check(page.evaluate("window.__URBION_CANONICAL_UI_V1__===true"), "canonical UI owner guard active")
            check(page.evaluate("window.__URBION_LAYER_MANAGER__===true"), "single live layer manager guard active")
            check(page.evaluate("window.__URBION_MODAL_OWNER_V1__===true"), "single modal owner guard active")

            state = row_control(page, "STATE")
            district = row_control(page, "DISTRICT")
            mukim = row_control(page, "MUKIM")
            pbt = row_control(page, "LOCAL AUTHORITY")
            check(state.evaluate("el=>el.tagName") == "SELECT", "State control is canonical select")
            check(district.evaluate("el=>el.tagName") == "SELECT", "District control is canonical select")
            check(mukim.evaluate("el=>el.tagName") == "SELECT", "Mukim control is canonical select")
            check(pbt.evaluate("el=>el.tagName") == "SELECT", "Local Authority control is canonical select")
            check(page.evaluate("!!document.querySelector('[data-pbt-catalog-owner=\"urbion_workspace_pbt_catalog.js\"]')"), "single frontend PBT catalogue owner active")
            check(page.evaluate("Object.keys(window.__URBION_PBT_CATALOG__||{}).length" ) >= 16, "full state/territory PBT catalogue exposed")

            state.select_option(label="Selangor")
            page.wait_for_timeout(350)
            sel_districts = usable_options(district)
            sel_pbts = usable_options(pbt)
            check(len(sel_districts) >= 5, "State change populates District hierarchy")
            check(len(sel_pbts) >= 10, "State change populates authoritative PBT catalogue")
            district.select_option(label=sel_districts[0])
            page.wait_for_timeout(350)
            sel_mukims = usable_options(mukim)
            check(len(sel_mukims) >= 1, "District change populates Mukim hierarchy")
            state.select_option(label="Melaka")
            page.wait_for_timeout(350)
            check(len(usable_options(district)) >= 3, "State reset refreshes District options")
            check(len(usable_options(pbt)) == 4, "State reset refreshes Melaka PBT catalogue")

            gt1 = page.locator("#landuse1 option").all_text_contents()
            check(len(gt1) >= 10, "GT1 taxonomy populated")
            check(not any(x.strip().lower() == "perdagangan" for x in gt1), "legacy Perdagangan absent")
            for ident in ["landuse1", "landuse2", "landuse3"]:
                page.locator(f"#{ident}").evaluate("""el=>{let p=el;while(p&&!(p.classList&&p.classList.contains('sec')))p=p.parentElement;if(p?.classList.contains('collapsed'))p.querySelector('.sechead button')?.click();}""")
            check(page.locator("#landuse1").is_visible(), "land-use controls visible")
            page.locator("#landuse1").select_option(label="Komersial")
            check(len(page.locator("#landuse2 option").all_text_contents()) >= 2, "GT2 cascades")
            page.locator("#landuse2").select_option(index=1)
            check(len(page.locator("#landuse3 option").all_text_contents()) >= 2, "GT3 cascades")

            sec_before = page.locator("#landuse1").evaluate("""el=>{let p=el;while(p&&!(p.classList&&p.classList.contains('sec')))p=p.parentElement;return p?.classList.contains('collapsed')}""")
            page.locator("#landuse1").evaluate("""el=>{let p=el;while(p&&!(p.classList&&p.classList.contains('sec')))p=p.parentElement;p?.querySelector('.sechead button')?.click();}""")
            page.wait_for_timeout(100)
            sec_after = page.locator("#landuse1").evaluate("""el=>{let p=el;while(p&&!(p.classList&&p.classList.contains('sec')))p=p.parentElement;return p?.classList.contains('collapsed')}""")
            check(sec_after != sec_before, "section header toggles state once")

            for kind in ["street", "sat", "hybrid"]:
                page.locator(f"[data-base='{kind}']").click()
                page.wait_for_timeout(150)
                check(page.locator(f"[data-base='{kind}']").evaluate("e=>e.classList.contains('active')"), f"{kind} base active")
                check(page.evaluate("k=>typeof baseLayers!=='undefined' && map.hasLayer(baseLayers[k])", kind), f"{kind} layer mounted")
            check(page.evaluate("typeof baseLayers!=='undefined' && map.hasLayer(baseLayers.hybrid) && !map.hasLayer(baseLayers.sat) && !map.hasLayer(baseLayers.street)"), "basemap switching removes prior base")

            page.locator("#layerBtn").click()
            page.wait_for_timeout(300)
            check(page.locator("#layers").evaluate("e=>e.classList.contains('open')"), "layers opens")
            rows = page.locator("#layerList [data-urbion-layer]")
            count = rows.count()
            check(count >= 20, f"authoritative live layer catalogue populated ({count})")
            layer_results = []
            for i in range(count):
                row = rows.nth(i)
                layer_id = row.get_attribute("data-urbion-layer") or f"layer-{i}"
                row.evaluate("""el=>{const g=el.closest('.layer-group');if(g?.classList.contains('closed'))g.querySelector('.layer-group-head')?.click();}""")
                row.scroll_into_view_if_needed()
                row.check(force=True)
                page.wait_for_timeout(250)
                try:
                    page.wait_for_function("id=>!!window.__URBION_LIVE_LAYERS__?.[id]", arg=layer_id, timeout=6000)
                    page.wait_for_function("""id=>{const l=window.__URBION_LIVE_LAYERS__?.[id];if(!l)return false;return Object.keys(l._tiles||{}).length>0||(l._container?.querySelectorAll('img,canvas').length||0)>0}""", arg=layer_id, timeout=6000)
                    state_text = page.locator(f"[data-layer-state='{layer_id}']").inner_text().strip().upper()
                    check(not state_text.startswith("ERROR"), f"layer {layer_id} state non-error")
                    check(page.evaluate("id=>{const l=window.__URBION_LIVE_LAYERS__?.[id];return !!l&&map.hasLayer(l)}", layer_id), f"layer {layer_id} mounted on map")
                    check(page.evaluate("id=>{const l=window.__URBION_LIVE_LAYERS__?.[id];if(!l)return false;return Object.keys(l._tiles||{}).length>0||(l._container?.querySelectorAll('img,canvas').length||0)>0}", layer_id), f"layer {layer_id} rendered imagery")
                    layer_results.append({"id": layer_id, "ok": True, "state": state_text})
                except Exception as exc:
                    layer_results.append({"id": layer_id, "ok": False, "error": str(exc)})
                    failed.append(f"layer {layer_id}: {exc}")
            page.locator("#layerBtn").click()
            page.wait_for_timeout(150)
            check(not page.locator("#layers").evaluate("e=>e.classList.contains('open')"), "layers closes")
            check(all(item["ok"] for item in layer_results), f"all {count} live GIS layers render end-to-end")

            page.locator("#map").click(position={"x": 300, "y": 200})
            page.wait_for_timeout(150)
            coords = page.locator("#coords").inner_text().strip()
            check("," in coords and len(coords) > 7, "map click updates coordinates")

            prepare_ready_case(page)
            analysis_requests.clear()
            copilot_requests.clear()
            page.locator("#run").click()
            page.wait_for_timeout(350)
            check(len(analysis_requests) == 1, "RUN sends exactly one analysis request")
            page.wait_for_function("document.body.innerText.includes('ANALYSIS COMPLETE')", timeout=20000)
            check(bool(page.evaluate("window.URBION_LAST")), "analysis packet stored")
            check(page.locator("#caseReadinessNote").inner_text().strip().upper().startswith("READY"), "case remains ready after analysis")
            if copilot_requests:
                check(bool(page.evaluate("window.URBION_AI_LAST")), "AI/Copilot narrative stored")

            for kind, selector in [("evidence", "#evidenceBtn"), ("whatif", "#whatifBtn"), ("decision", "#decisionBtn"), ("output", "#outputBtn")]:
                page.locator(selector).click()
                page.wait_for_timeout(150)
                check(page.locator("#modal").is_visible(), f"{kind} modal opens")
                page.locator("#closeModal").click()
                page.wait_for_timeout(100)
                check(not page.locator("#modal").is_visible(), f"{kind} modal closes")

            page.locator("#whatifBtn").click()
            page.wait_for_timeout(150)
            check(page.locator("#modal").is_visible(), "what-if studio opens")
            whatif_requests.clear()
            wf_button = page.locator("#whatIfRun")
            if wf_button.count():
                wf_button.click()
                page.wait_for_timeout(300)
                check(len(whatif_requests) == 1, "what-if sends exactly one request")
            page.locator("#closeModal").click()
            page.wait_for_timeout(100)

            utilities = [("#runtimeAbout", "ABOUT"), ("#runtimeHelp", "HELP"), ("#runtimeSources", "SOURCES"), ("#runtimeStatus", "STATUS")]
            for selector, label in utilities:
                page.locator(selector).click()
                page.wait_for_timeout(100)
                check(page.locator("#modal").is_visible(), f"{label} utility opens")
                page.locator("#closeModal").click()
            if page.locator("#runtimeFullscreen").count():
                page.locator("#runtimeFullscreen").click()
                page.wait_for_timeout(100)
                check(True, "FULLSCREEN utility action")
            if page.locator("#runtimeReset").count():
                page.locator("#runtimeReset").click()
                page.wait_for_timeout(100)
                check(True, "RESET utility action")
            if page.locator("#themeBtn").count():
                page.locator("#themeBtn").click()
                page.wait_for_timeout(80)
                check(True, "theme toggle action")
            if page.locator("#langBtn").count():
                page.locator("#langBtn").click()
                page.wait_for_timeout(80)
                check(True, "language toggle action")

            for width, height in [(1440, 900), (1366, 768), (1920, 1080)]:
                page.set_viewport_size({"width": width, "height": height})
                page.wait_for_timeout(120)
                overflow = page.evaluate("document.documentElement.scrollWidth>window.innerWidth+4 || document.body.scrollWidth>window.innerWidth+4")
                check(not overflow, f"responsive no horizontal overflow at {width}x{height}")
            page.set_viewport_size({"width": 1440, "height": 900})

            resources = page.evaluate("performance.getEntriesByType('resource').map(e=>e.name)")
            legacy_hits = [u for u in resources if "urbion_workspace_final" in u or "workspace_final" in u]
            check(not legacy_hits, "legacy workspace assets absent")
            check(not failed, "no non-GIS browser request failures")
            check(not http, "no non-GIS HTTP errors")
            checks.append("all canonical browser-gate controls passed")
        except Exception as exc:
            failed.append(str(exc))
            print("CHECK FAILURES:")
            print(exc)
        finally:
            page.screenshot(path=str(ARTIFACT / "workspace-final.png"), full_page=True)
            (ARTIFACT / "workspace-browser.json").write_text(
                json.dumps({"base": BASE, "failed": failed, "http": http, "gis_optional": gis_optional, "console_errors": console_errors, "checks": checks}, indent=2),
                encoding="utf-8",
            )
            browser.close()
    return 1 if failed or http else 0


if __name__ == "__main__":
    raise SystemExit(main())
