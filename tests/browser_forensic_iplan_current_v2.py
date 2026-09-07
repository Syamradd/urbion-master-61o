from __future__ import annotations

import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8765")
HEAD_SHA = "19b630a1ef845e8b0293bb236d1997672c3f27a9"
ARTIFACT_DIR = Path(os.getenv("URBION_FORENSIC_ARTIFACT_DIR", "/tmp/urbion-iplan-forensic"))
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
TRACE_FILE = ARTIFACT_DIR / "trace.jsonl"
TOKENS = ("GTsemasa", "GTsemasa_04", "MapServer", "/export", "scharms.planmalaysia.gov.my")


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def emit(kind: str, **data) -> None:
    row = {"ts": now(), "kind": kind, **data}
    text = json.dumps(row, ensure_ascii=False, default=str)
    print(f"FORENSIC::{kind}::{text}", flush=True)
    with TRACE_FILE.open("a", encoding="utf-8") as fh:
        fh.write(text + "\n")


def inject(source: str, pattern: str, replacement: str, name: str) -> tuple[str, bool]:
    updated, count = re.subn(pattern, replacement, source, count=1)
    if count == 0:
        emit("INSTRUMENT_MARKER_MISSING", name=name)
        return source, False
    emit("INSTRUMENT_MARKER_OK", name=name)
    return updated, True


def instrument_bundle(source: str) -> str:
    out = source
    markers = 0

    replacements = [
        (r"if\(window\.__URBION_PREMIUM_V7_INTEGRATION__\)return;",
         "console.log('FORENSIC::V7_GUARD::CHECK',!!window.__URBION_PREMIUM_V7_INTEGRATION__);if(window.__URBION_PREMIUM_V7_INTEGRATION__){console.log('FORENSIC::V7_GUARD::EARLY_RETURN');return;}", "v7_guard"),
        (r"window\.__URBION_PREMIUM_V7_INTEGRATION__=true;",
         "window.__URBION_PREMIUM_V7_INTEGRATION__=true;console.log('FORENSIC::V7_BOOT::EXECUTED');", "v7_boot_flag"),
        (r"function reconcileSourceLayerCatalogue\(r\)\{",
         "function reconcileSourceLayerCatalogue(r){console.log('FORENSIC::reconcileSourceLayerCatalogue::BEGIN');", "reconcile_begin"),
        (r"reconcileTransportGroup\(d\);syncSourceLayerCount\(d\)\}",
         "reconcileTransportGroup(d);syncSourceLayerCount(d);console.log('FORENSIC::reconcileSourceLayerCatalogue::END')}", "reconcile_end"),
        (r"function wireOfficialLayers\(r\)\{",
         "function wireOfficialLayers(r){console.log('FORENSIC::wireOfficialLayers::BEGIN',!!window.__URBION_FCC_MAP__,!!window.L);", "wire_begin"),
        (r"input\.addEventListener\('change',\(\)=>setOfficialActive\(r,input\.dataset\.layer,input\.checked\),false\);",
         "input.addEventListener('change',()=>{console.log('FORENSIC::V7_HANDLER::FIRED',input.dataset.layer,!!input.checked);return setOfficialActive(r,input.dataset.layer,input.checked)},false);", "wire_listener"),
        (r"function officialLayer\(id,state,map\)\{",
         "function officialLayer(id,state,map){console.log('FORENSIC::officialLayer::BEGIN',id,state,!!map,!!window.L);", "official_begin"),
        (r"const url='https://scharms\.planmalaysia\.gov\.my/arcgis/rest/services/iPLAN/'\+cfg\.prefix\+'_'+code+'/MapServer';",
         "const url='https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN/'+cfg.prefix+'_'+code+'/MapServer';console.log('FORENSIC::officialLayer::URL',url);", "official_url"),
        (r"function setOfficialActive\(r,id,active\)\{",
         "function setOfficialActive(r,id,active){console.log('FORENSIC::setOfficialActive::BEGIN',id,!!active);", "set_active_begin"),
        (r"const layer=officialLayer\(id,state,map\);",
         "const layer=officialLayer(id,state,map);console.log('FORENSIC::setOfficialActive::LAYER_RESULT',!!layer,layer?.constructor?.name||null);", "set_active_layer"),
        (r"layer\.addTo\(map\);",
         "console.log('FORENSIC::layer.addTo::BEFORE',layer?.constructor?.name||null,!!map?.hasLayer?.(layer),!!layer?._map);layer.addTo(map);console.log('FORENSIC::layer.addTo::AFTER',!!map?.hasLayer?.(layer),!!layer?._map);", "layer_add"),
        (r"function arcgisTileLayer\(map,service,opacity\)\{",
         "function arcgisTileLayer(map,service,opacity){console.log('FORENSIC::arcgisTileLayer::BEGIN',service,opacity);", "arcgis_begin"),
        (r"function createTile\(coords,done\)\{",
         "function createTile(coords,done){console.log('FORENSIC::createTile::BEGIN',coords);", "tile_begin"),
        (r"tile\.src=service\+'/export\?bbox='\+encodeURIComponent\(bbox\)\+([^;]+);",
         "const __urbionTileUrl=service+'/export?bbox='+encodeURIComponent(bbox)+\\1;console.log('FORENSIC::createTile::URL',__urbionTileUrl);tile.src=__urbionTileUrl;", "tile_src"),
        (r"tile\.onload=\(\)=>done\(null,tile\);",
         "tile.onload=()=>{console.log('FORENSIC::tileload::EVENT',tile.src);done(null,tile)};", "tile_load"),
        (r"tile\.onerror=e=>done\(e,tile\);",
         "tile.onerror=e=>{console.error('FORENSIC::tileerror::EVENT',e,tile.src);done(e,tile)};", "tile_error"),
    ]
    for pattern, repl, name in replacements:
        out, ok = inject(out, pattern, repl, name)
        markers += int(ok)
    emit("INSTRUMENTATION_SUMMARY", markers=markers, expected=len(replacements))
    return out


INIT_JS = r"""
(() => {
  const ids = new WeakMap();
  const listenerCounts = new WeakMap();
  let seq = 0;
  const nodeId = node => { if (!node) return null; if (!ids.has(node)) ids.set(node, `NODE-${++seq}`); return ids.get(node); };
  const nodeInfo = node => {
    if (!node) return null;
    const row = node.closest?.('.fcc-layer-row');
    return {nodeId: nodeId(node), checked: !!node.checked, disabled: !!node.disabled,
      dataLayer: node.dataset?.layer || null, listenerCount: listenerCounts.get(node)?.change || 0,
      rowText: row?.innerText || null, smallText: row?.querySelector?.('small')?.textContent || null,
      rowOuter: row?.outerHTML || null};
  };
  const snapshot = label => ({label,
    count: document.querySelectorAll('#cs-layer-drawer input[data-layer="iplan-current"]').length,
    input: nodeInfo(document.querySelector('#cs-layer-drawer input[data-layer="iplan-current"]')),
    state: document.querySelector('#cs-state')?.value || null});
  const layerInfo = layer => layer ? {constructorName: layer.constructor?.name || null,
    __urbionOfficial: !!layer.__urbionOfficial, __urbionLayerId: layer.__urbionLayerId || null,
    __urbionSource: layer.__urbionSource || null, mapHasLayer: !!window.__URBION_FCC_MAP__?.hasLayer?.(layer),
    layerMap: !!layer._map, tiles: layer._tiles ? Object.keys(layer._tiles).length : null,
    tilePane: !!document.querySelector('.leaflet-tile-pane'), zoom: window.__URBION_FCC_MAP__?.getZoom?.() ?? null,
    size: window.__URBION_FCC_MAP__?.getSize?.() ? {x:window.__URBION_FCC_MAP__.getSize().x,y:window.__URBION_FCC_MAP__.getSize().y}:null}:null;
  window.__URBION_FORENSIC__ = {nodeInfo, snapshot, layerInfo};
  const originalAdd = EventTarget.prototype.addEventListener;
  EventTarget.prototype.addEventListener = function(type, listener, options) {
    if (this instanceof HTMLInputElement && this.matches?.('#cs-layer-drawer input[data-layer="iplan-current"]')) {
      const c = listenerCounts.get(this) || {}; c[type] = (c[type] || 0) + 1; listenerCounts.set(this, c);
      console.log('FORENSIC::ADD_EVENT_LISTENER', type, nodeInfo(this));
    }
    return originalAdd.call(this, type, listener, options);
  };
  const installObserver = () => {
    if (!document.documentElement) return;
    const mo = new MutationObserver(records => records.forEach(record => {
      if (!record.addedNodes.length && !record.removedNodes.length) return;
      const inputs = document.querySelectorAll('#cs-layer-drawer input[data-layer="iplan-current"]');
      if (inputs.length) console.log('FORENSIC::DOM_MUTATION', {count:inputs.length, input:nodeInfo(inputs[0]), added:record.addedNodes.length, removed:record.removedNodes.length});
    }));
    mo.observe(document.documentElement, {subtree:true, childList:true});
    console.log('FORENSIC::DOM_OBSERVER::INSTALLED');
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', installObserver, {once:true}); else installObserver();
})();
"""


def main() -> None:
    TRACE_FILE.unlink(missing_ok=True)
    emit("HEAD", sha=HEAD_SHA)
    console_errors: list[str] = []
    page_errors: list[str] = []
    started: dict[str, float] = {}

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context(viewport={"width":1440,"height":900}, device_scale_factor=1)
        page = context.new_page()
        page.add_init_script(INIT_JS)
        page.on("console", lambda msg: (print(msg.text, flush=True), console_errors.append(msg.text)) if "FORENSIC::" in msg.text or msg.type == "error" else None)
        page.on("pageerror", lambda exc: (emit("PAGE_ERROR", error=str(exc)), page_errors.append(str(exc))))
        def request_cb(req):
            if any(t in req.url for t in TOKENS):
                started[req.url]=time.monotonic(); emit("REQUEST", url=req.url, method=req.method)
        def failed_cb(req):
            if any(t in req.url for t in TOKENS):
                emit("REQUEST_FAILED", url=req.url, method=req.method, reason=str(req.failure), elapsed_ms=round((time.monotonic()-started.get(req.url,time.monotonic()))*1000,1))
        def response_cb(resp):
            if any(t in resp.url for t in TOKENS):
                emit("RESPONSE", url=resp.url, method=resp.request.method, status=resp.status, elapsed_ms=round((time.monotonic()-started.get(resp.url,time.monotonic()))*1000,1))
        page.on("request", request_cb); page.on("requestfailed", failed_cb); page.on("response", response_cb)

        def route_handler(route):
            response = route.fetch()
            body = response.body().decode("utf-8")
            body = instrument_bundle(body)
            headers = dict(response.headers)
            headers.pop("content-encoding", None)
            headers["content-length"] = str(len(body.encode("utf-8")))
            route.fulfill(status=response.status, headers=headers, body=body)
        page.route("**/urbion_championship_command_shell.js*", route_handler)

        page.goto(BASE_URL + "/", wait_until="domcontentloaded", timeout=30_000)
        page.wait_for_selector("#cs-map", timeout=15_000)
        page.wait_for_timeout(1000)
        emit("PRECHECK", checkbox_count=page.locator('#cs-layer-drawer input[data-layer="iplan-current"]').count(),
             checkbox=page.evaluate("window.__URBION_FORENSIC__.nodeInfo(document.querySelector('#cs-layer-drawer input[data-layer=\"iplan-current\"]'))"),
             state=page.locator('#cs-state').input_value(),
             map_exists=page.evaluate("!!window.__URBION_FCC_MAP__"),
             L_exists=page.evaluate("!!window.L"),
             syncLayerState_type=page.evaluate("typeof window.syncLayerState"),
             v7_flag=page.evaluate("window.__URBION_PREMIUM_V7_INTEGRATION__ ?? null"),
             official_layers=page.evaluate("window.__URBION_OFFICIAL_LAYERS__ ?? null"),
             integration=page.evaluate("window.__URBION_PREMIUM_V7_INTEGRATION__ ?? null"),
             qa_layer=page.evaluate("window.__URBION_QA__?.layers?.['iplan-current'] ?? null"))
        emit("IDENTITY_500MS", **page.evaluate("window.__URBION_FORENSIC__.snapshot('500ms')"))
        page.wait_for_timeout(900)
        emit("IDENTITY_1400MS", **page.evaluate("window.__URBION_FORENSIC__.snapshot('1400ms')"))

        # Exact case prerequisites used by the documented browser QA flow.
        for sel, val in [("#cs-project_name","Browser Forensic · Sg. Udang"),("#cs-lat","2.285"),("#cs-lon","102.196")]: page.locator(sel).fill(val)
        for sel, label in [("#cs-state","Melaka"),("#cs-pbt","Majlis Bandaraya Melaka Bersejarah"),("#cs-district","Melaka Tengah"),("#cs-landuse","Komersial"),("#cs-category","Pembangunan Penggunaan Bercampur"),("#cs-activity","TOD / Mixed Use"),("#cs-development","New Development")]: page.locator(sel).select_option(label=label)
        page.locator("#cs-ratio").fill("4.5")
        page.locator("#cs-map-layers").click()
        page.wait_for_selector('#cs-layer-drawer input[data-layer="iplan-current"]', timeout=10_000)
        page.wait_for_timeout(300)
        emit("ACTION_BEFORE", checkbox=page.evaluate("window.__URBION_FORENSIC__.nodeInfo(document.querySelector('#cs-layer-drawer input[data-layer=\"iplan-current\"]'))"),
             state=page.locator('#cs-state').input_value(), v7_flag=page.evaluate("window.__URBION_PREMIUM_V7_INTEGRATION__ ?? null"))

        target = page.locator('#cs-layer-drawer input[data-layer="iplan-current"]')
        target.check(timeout=10_000)
        emit("ACTION_AFTER_CHECK", checkbox=page.evaluate("window.__URBION_FORENSIC__.nodeInfo(document.querySelector('#cs-layer-drawer input[data-layer=\"iplan-current\"]'))"))
        page.wait_for_timeout(7000)
        emit("FINAL", checkbox=page.evaluate("window.__URBION_FORENSIC__.nodeInfo(document.querySelector('#cs-layer-drawer input[data-layer=\"iplan-current\"]'))"),
             official_layer=page.evaluate("window.__URBION_OFFICIAL_LAYERS__?.['iplan-current'] ? window.__URBION_FORENSIC__.layerInfo(window.__URBION_OFFICIAL_LAYERS__['iplan-current']) : null"),
             qa_layer=page.evaluate("window.__URBION_QA__?.layers?.['iplan-current'] ?? null"),
             console_errors=console_errors, page_errors=page_errors)
        page.screenshot(path=ARTIFACT_DIR / "final.png", full_page=True)
        browser.close()


if __name__ == "__main__":
    main()
