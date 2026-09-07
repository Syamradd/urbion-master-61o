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

TARGET = "iplan-current"
URL_TOKENS = ("GTsemasa", "GTsemasa_04", "MapServer", "/export", "scharms.planmalaysia.gov.my")


def ts() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def emit(kind: str, **data) -> None:
    row = {"ts": ts(), "kind": kind, **data}
    line = json.dumps(row, ensure_ascii=False, default=str)
    print(f"FORENSIC::{kind}::{line}", flush=True)
    with TRACE_FILE.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def instrument_bundle(source: str) -> str:
    def rep(old: str, new: str, name: str, count: int = 1) -> str:
        actual = source.count(old) if source is not None else 0
        if actual != count:
            raise AssertionError(f"Instrumentation marker {name} expected {count}, found {actual}")
        return new

    out = source
    markers = 0

    old = "if(window.__URBION_PREMIUM_V7_INTEGRATION__)return;"
    new = "console.log('FORENSIC::V7_BOOT::START::guard='+(!!window.__URBION_PREMIUM_V7_INTEGRATION__));if(window.__URBION_PREMIUM_V7_INTEGRATION__){console.log('FORENSIC::V7_GUARD::EARLY_RETURN');return;}"
    out = rep(out, new, "v7_guard")
    markers += 1

    old = "window.__URBION_PREMIUM_V7_INTEGRATION__=true;"
    new = "window.__URBION_PREMIUM_V7_INTEGRATION__=true;console.log('FORENSIC::V7_BOOT::EXECUTED::integration_flag=true');"
    out = rep(out, new, "v7_flag")
    markers += 1

    old = "function reconcileSourceLayerCatalogue(r){const d=r?.querySelector('#cs-layer-drawer');if(!d)return;"
    new = "function reconcileSourceLayerCatalogue(r){console.log('FORENSIC::reconcileSourceLayerCatalogue::BEGIN',window.__URBION_FORENSIC__?.snapshot?.('before-reconcile'));const d=r?.querySelector('#cs-layer-drawer');if(!d){console.log('FORENSIC::reconcileSourceLayerCatalogue::NO_DRAWER');return;}"
    out = rep(out, new, "reconcile_begin")
    markers += 1

    old = "reconcileTransportGroup(d);syncSourceLayerCount(d)}"
    new = "reconcileTransportGroup(d);syncSourceLayerCount(d);console.log('FORENSIC::reconcileSourceLayerCatalogue::END',window.__URBION_FORENSIC__?.snapshot?.('after-reconcile'));}"
    out = rep(out, new, "reconcile_end")
    markers += 1

    old = "function wireOfficialLayers(r){const d=r?.querySelector('#cs-layer-drawer');if(!d||!window.__URBION_FCC_MAP__||!window.L)return;"
    new = "function wireOfficialLayers(r){console.log('FORENSIC::wireOfficialLayers::BEGIN',window.__URBION_FORENSIC__?.snapshot?.('before-wire'));const d=r?.querySelector('#cs-layer-drawer');if(!d||!window.__URBION_FCC_MAP__||!window.L){console.log('FORENSIC::wireOfficialLayers::ABORT',!!d,!!window.__URBION_FCC_MAP__,!!window.L);return;}"
    out = rep(out, new, "wire_begin")
    markers += 1

    old = "inputs.forEach(input=>{if(input.dataset.officialInputWired==='1')return;input.dataset.officialInputWired='1';input.addEventListener('change',()=>setOfficialActive(r,input.dataset.layer,input.checked),false);"
    new = "inputs.forEach(input=>{if(input.dataset.officialInputWired==='1'){console.log('FORENSIC::wireOfficialLayers::ALREADY_WIRED',input.dataset.layer,window.__URBION_FORENSIC__?.nodeInfo?.(input));return;}input.dataset.officialInputWired='1';console.log('FORENSIC::wireOfficialLayers::WIRE_INPUT',input.dataset.layer,window.__URBION_FORENSIC__?.nodeInfo?.(input));input.addEventListener('change',()=>{console.log('FORENSIC::V7_HANDLER::FIRED',input.dataset.layer,!!input.checked,window.__URBION_FORENSIC__?.nodeInfo?.(input));try{return setOfficialActive(r,input.dataset.layer,input.checked)}catch(e){console.error('FORENSIC::setOfficialActive::THROW',e);throw e}},false);"
    out = rep(out, new, "wire_listener")
    markers += 1

    old = "function officialLayer(id,state,map){const cfg=OFFICIAL_SERVICES[id];const code=STATE_CODES[state];if(!cfg||!code||!map||!window.L)return null;"
    new = "function officialLayer(id,state,map){console.log('FORENSIC::officialLayer::BEGIN',id,state,!!map,!!window.L);const cfg=OFFICIAL_SERVICES[id];const code=STATE_CODES[state];if(!cfg||!code||!map||!window.L){console.log('FORENSIC::officialLayer::NULL',id,state,!!cfg,code,!!map,!!window.L);return null;}"
    out = rep(out, new, "official_begin")
    markers += 1

    old = "const url='https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN/'+cfg.prefix+'_'+code+'/MapServer';const layer=arcgisTileLayer(map,url,.62);layer.__urbionOfficial=true;"
    new = "const url='https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN/'+cfg.prefix+'_'+code+'/MapServer';console.log('FORENSIC::officialLayer::URL',url);let layer;try{layer=arcgisTileLayer(map,url,.62);console.log('FORENSIC::officialLayer::LAYER_CREATED',!!layer,layer?.constructor?.name)}catch(e){console.error('FORENSIC::arcgisTileLayer::THROW',e);throw e}layer.__urbionOfficial=true;"
    out = rep(out, new, "official_create")
    markers += 1

    old = "function setOfficialActive(r,id,active){const store=window.__URBION_OFFICIAL_LAYERS__||(window.__URBION_OFFICIAL_LAYERS__={});"
    new = "function setOfficialActive(r,id,active){console.log('FORENSIC::setOfficialActive::BEGIN',id,!!active,window.__URBION_FORENSIC__?.nodeInfo?.(r?.querySelector?.(`#cs-layer-drawer input[data-layer=\\\"${id}\\\"]`)));const store=window.__URBION_OFFICIAL_LAYERS__||(window.__URBION_OFFICIAL_LAYERS__={});"
    out = rep(out, new, "set_active_begin")
    markers += 1

    old = "const layer=officialLayer(id,state,map);if(!layer){input.checked=false;syncLayerState(r,id,false,'STATE REQUIRED');return}store[id]=layer;syncLayerState(r,id,true,'CHECKING SOURCE…');"
    new = "let layer;try{layer=officialLayer(id,state,map)}catch(e){console.error('FORENSIC::officialLayer::THROW_FROM_SET_ACTIVE',e);throw e}console.log('FORENSIC::setOfficialActive::OFFICIAL_RESULT',!!layer,layer?.constructor?.name);if(!layer){input.checked=false;try{syncLayerState(r,id,false,'STATE REQUIRED')}catch(e){console.error('FORENSIC::syncLayerState::THROW',e);throw e}return}store[id]=layer;try{syncLayerState(r,id,true,'CHECKING SOURCE…')}catch(e){console.error('FORENSIC::syncLayerState::THROW',e);throw e}"
    out = rep(out, new, "set_active_layer")
    markers += 1

    old = "layer.addTo(map);updateLegend(r)}"
    new = "try{console.log('FORENSIC::layer.addTo::BEFORE',window.__URBION_FORENSIC__?.layerInfo?.(layer));layer.addTo(map);console.log('FORENSIC::layer.addTo::AFTER',!!map.hasLayer(layer),!!layer._map)}catch(e){console.error('FORENSIC::layer.addTo::THROW',e);throw e}console.log('FORENSIC::setOfficialActive::END',window.__URBION_FORENSIC__?.layerInfo?.(layer));updateLegend(r)}"
    out = rep(out, new, "layer_add")
    markers += 1

    old = "function arcgisTileLayer(map,service,opacity){const Grid=L.GridLayer.extend({createTile(coords,done){const tile=document.createElement('img');"
    new = "function arcgisTileLayer(map,service,opacity){console.log('FORENSIC::arcgisTileLayer::BEGIN',service,opacity);const Grid=L.GridLayer.extend({createTile(coords,done){console.log('FORENSIC::createTile::BEGIN',coords,service);const tile=document.createElement('img');"
    out = rep(out, new, "arcgis_begin")
    markers += 1

    old = "tile.src=service+'/export?bbox='+encodeURIComponent(bbox)+'&bboxSR=4326&imageSR=4326&size='+size.x+','+size.y+'&dpi=96&format=png32&transparent=true&layers=show:0&f=image';tile.onload=()=>done(null,tile);tile.onerror=e=>done(e,tile);return tile}});"
    new = "const tileUrl=service+'/export?bbox='+encodeURIComponent(bbox)+'&bboxSR=4326&imageSR=4326&size='+size.x+','+size.y+'&dpi=96&format=png32&transparent=true&layers=show:0&f=image';console.log('FORENSIC::createTile::URL',tileUrl);try{tile.src=tileUrl}catch(e){console.error('FORENSIC::createTile::SRC_THROW',e);throw e}tile.onload=()=>{console.log('FORENSIC::tileload::EVENT',tileUrl);done(null,tile)};tile.onerror=e=>{console.error('FORENSIC::tileerror::EVENT',e,tileUrl);done(e,tile)};return tile}});"
    out = rep(out, new, "tile_src")
    markers += 1

    emit("instrumentation_installed", markers=markers)
    return out


INIT_JS = r"""
(() => {
  const targetIds = new WeakMap();
  const listenerCounts = new WeakMap();
  let seq = 0;
  const nodeId = node => {
    if (!node) return null;
    if (!targetIds.has(node)) targetIds.set(node, `NODE-${++seq}`);
    return targetIds.get(node);
  };
  const nodeInfo = node => {
    if (!node) return null;
    const row = node.closest?.('.fcc-layer-row');
    return {
      nodeId: nodeId(node),
      tag: node.tagName,
      checked: !!node.checked,
      disabled: !!node.disabled,
      dataLayer: node.dataset?.layer || null,
      rowExists: !!row,
      rowText: row?.innerText || null,
      smallText: row?.querySelector?.('small')?.textContent || null,
      rowOuter: row?.outerHTML || null,
      changeListeners: listenerCounts.get(node)?.change || 0,
    };
  };
  const snapshot = label => {
    const input = document.querySelector('#cs-layer-drawer input[data-layer="iplan-current"]');
    const rows = [...document.querySelectorAll('#cs-layer-drawer input[data-layer="iplan-current"]')];
    const info = {label, count: rows.length, input: nodeInfo(input), state: document.querySelector('#cs-state')?.value || null};
    console.log('FORENSIC::DOM_SNAPSHOT', info);
    return info;
  };
  const layerInfo = layer => layer ? {
    constructorName: layer.constructor?.name || null,
    __urbionOfficial: !!layer.__urbionOfficial,
    __urbionLayerId: layer.__urbionLayerId || null,
    __urbionSource: layer.__urbionSource || null,
    hasMap: !!layer._map,
    tileCount: layer._tiles ? Object.keys(layer._tiles).length : null,
    tilePaneExists: !!document.querySelector('.leaflet-tile-pane'),
    mapZoom: window.__URBION_FCC_MAP__?.getZoom?.() ?? null,
    mapSize: window.__URBION_FCC_MAP__?.getSize?.() ? {
      x: window.__URBION_FCC_MAP__.getSize().x,
      y: window.__URBION_FCC_MAP__.getSize().y,
    } : null,
  } : null;
  window.__URBION_FORENSIC__ = {nodeId, nodeInfo, snapshot, layerInfo, listenerCounts};

  const originalAdd = EventTarget.prototype.addEventListener;
  EventTarget.prototype.addEventListener = function(type, listener, options) {
    if (this instanceof HTMLInputElement && this.matches?.('#cs-layer-drawer input[data-layer="iplan-current"]')) {
      const counts = listenerCounts.get(this) || {};
      counts[type] = (counts[type] || 0) + 1;
      listenerCounts.set(this, counts);
      console.log('FORENSIC::ADD_EVENT_LISTENER', type, nodeInfo(this));
    }
    return originalAdd.call(this, type, listener, options);
  };

  const mo = new MutationObserver(records => {
    for (const record of records) {
      if (!record.addedNodes.length && !record.removedNodes.length) continue;
      const input = document.querySelector('#cs-layer-drawer input[data-layer="iplan-current"]');
      const count = document.querySelectorAll('#cs-layer-drawer input[data-layer="iplan-current"]').length;
      if (input || count) console.log('FORENSIC::DOM_MUTATION', {count, info: nodeInfo(input), removed: record.removedNodes.length, added: record.addedNodes.length});
    }
  });
  mo.observe(document.documentElement, {subtree:true, childList:true});
})();
"""


def main() -> None:
    emit("HEAD", sha=HEAD_SHA)
    console_errors = []
    page_errors = []
    request_failed = {}
    request_started = {}
    responses = {}

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        page = context.new_page()
        page.add_init_script(INIT_JS)

        page.on("console", lambda msg: (print(msg.text, flush=True), console_errors.append(msg.text)) if msg.type == "error" or "FORENSIC::" in msg.text else None)
        page.on("pageerror", lambda exc: (emit("PAGE_ERROR", error=str(exc)), page_errors.append(str(exc))))

        def req_cb(req):
            if any(token in req.url for token in URL_TOKENS):
                request_started[req] = time.monotonic()
                emit("REQUEST", url=req.url, method=req.method, timestamp=ts())
        page.on("request", req_cb)

        def fail_cb(req):
            if any(token in req.url for token in URL_TOKENS):
                reason = req.failure
                request_failed[req] = reason
                emit("REQUEST_FAILED", url=req.url, method=req.method, reason=str(reason), elapsed_ms=round((time.monotonic()-request_started.get(req,time.monotonic()))*1000,1))
        page.on("requestfailed", fail_cb)

        def response_cb(resp):
            if any(token in resp.url for token in URL_TOKENS):
                responses[resp.request] = resp.status
                emit("RESPONSE", url=resp.url, method=resp.request.method, status=resp.status, elapsed_ms=round((time.monotonic()-request_started.get(resp.request,time.monotonic()))*1000,1))
        page.on("response", response_cb)

        def route_handler(route):
            response = route.fetch()
            body = response.body().decode("utf-8")
            if "urbion_championship_command_shell.js" in route.request.url:
                body = instrument_bundle(body)
                headers = dict(response.headers)
                headers.pop("content-encoding", None)
                headers["content-length"] = str(len(body.encode("utf-8")))
                route.fulfill(status=response.status, headers=headers, body=body)
            else:
                route.fulfill(response=response)
        page.route("**/urbion_championship_command_shell.js*", route_handler)

        page.request.get(BASE_URL + "/health", timeout=10_000)
        page.goto(BASE_URL + "/", wait_until="networkidle", timeout=30_000)
        page.wait_for_selector("#cs-layer-drawer", state="attached", timeout=15_000)
        page.wait_for_timeout(100)

        emit("PRECHECK", head=HEAD_SHA,
             checkbox_count=page.locator('#cs-layer-drawer input[data-layer="iplan-current"]').count(),
             checkbox=page.evaluate("window.__URBION_FORENSIC__.nodeInfo(document.querySelector('#cs-layer-drawer input[data-layer=\\\"iplan-current\\\"]'))"),
             state=page.locator('#cs-state').input_value(),
             map_exists=page.evaluate("!!window.__URBION_FCC_MAP__"),
             L_exists=page.evaluate("!!window.L"),
             syncLayerState_type=page.evaluate("typeof window.syncLayerState"),
             v7_flag=page.evaluate("window.__URBION_PREMIUM_V7_INTEGRATION__ ?? null"),
             official_layers=page.evaluate("window.__URBION_OFFICIAL_LAYERS__ ?? null"),
             qa_layer=page.evaluate("window.__URBION_QA__?.layers?.['iplan-current'] ?? null"))

        page.wait_for_timeout(500)
        emit("IDENTITY_500MS", **page.evaluate("window.__URBION_FORENSIC__.snapshot('500ms')"))
        page.wait_for_timeout(900)
        emit("IDENTITY_1400MS", **page.evaluate("window.__URBION_FORENSIC__.snapshot('1400ms')"))

        # Configure the exact documented browser-QA case prerequisites without changing the test itself.
        page.locator("#cs-project_name").fill("Browser Forensic · Sg. Udang")
        page.locator("#cs-lat").fill("2.285")
        page.locator("#cs-lon").fill("102.196")
        page.locator("#cs-state").select_option(label="Melaka")
        page.locator("#cs-pbt").select_option(label="Majlis Bandaraya Melaka Bersejarah")
        page.locator("#cs-district").select_option(label="Melaka Tengah")
        page.locator("#cs-landuse").select_option(label="Komersial")
        page.locator("#cs-category").select_option(label="Pembangunan Penggunaan Bercampur")
        page.locator("#cs-activity").select_option(label="TOD / Mixed Use")
        page.locator("#cs-development").select_option(label="New Development")
        page.locator("#cs-ratio").fill("4.5")
        page.locator("#cs-map-layers").click()
        page.wait_for_selector("#cs-layer-drawer input[data-layer=\"iplan-current\"]", state="attached", timeout=10_000)
        page.wait_for_timeout(300)

        # Patch inherited Leaflet onAdd only in this browser context for diagnostic logging.
        page.evaluate("""
        (() => {
          const p = window.L?.GridLayer?.prototype;
          if (!p || p.__urbionForensicOnAddWrapped) return;
          const original = p.onAdd;
          p.onAdd = function(map) {
            console.log('FORENSIC::layer.onAdd::BEGIN', window.__URBION_FORENSIC__?.layerInfo?.(this));
            try {
              const out = original.apply(this, arguments);
              console.log('FORENSIC::layer.onAdd::AFTER', window.__URBION_FORENSIC__?.layerInfo?.(this));
              return out;
            } catch (e) {
              console.error('FORENSIC::layer.onAdd::THROW', e);
              throw e;
            }
          };
          p.__urbionForensicOnAddWrapped = true;
        })();
        """)

        emit("ACTION_BEFORE", checkbox=page.evaluate("window.__URBION_FORENSIC__.nodeInfo(document.querySelector('#cs-layer-drawer input[data-layer=\\\"iplan-current\\\"]'))"),
             state=page.locator('#cs-state').input_value(),
             v7_flag=page.evaluate("window.__URBION_PREMIUM_V7_INTEGRATION__ ?? null"),
             integration=page.evaluate("window.__URBION_PREMIUM_V7_INTEGRATION__ ?? null"))

        target = page.locator('#cs-layer-drawer input[data-layer="iplan-current"]')
        target.check(timeout=10_000)
        emit("ACTION_AFTER_CHECK", checkbox=page.evaluate("window.__URBION_FORENSIC__.nodeInfo(document.querySelector('#cs-layer-drawer input[data-layer=\\\"iplan-current\\\"]'))"))
        page.wait_for_timeout(6_000)

        emit("FINAL", checkbox=page.evaluate("window.__URBION_FORENSIC__.nodeInfo(document.querySelector('#cs-layer-drawer input[data-layer=\\\"iplan-current\\\"]'))"),
             official_layer=page.evaluate("window.__URBION_OFFICIAL_LAYERS__?.['iplan-current'] ? window.__URBION_FORENSIC__.layerInfo(window.__URBION_OFFICIAL_LAYERS__['iplan-current']) : null"),
             map_has_layer=page.evaluate("(()=>{const l=window.__URBION_OFFICIAL_LAYERS__?.['iplan-current'];return !!(l&&window.__URBION_FCC_MAP__?.hasLayer(l))})()"),
             layer_map=page.evaluate("window.__URBION_OFFICIAL_LAYERS__?.['iplan-current']?!!window.__URBION_OFFICIAL_LAYERS__['iplan-current']._map:null"),
             qa_layer=page.evaluate("window.__URBION_QA__?.layers?.['iplan-current'] ?? null"),
             console_errors=console_errors,
             page_errors=page_errors,
             request_count=len(request_started),
             response_count=len(responses),
             failed_count=len(request_failed))

        classification = page.evaluate("""
        (() => {
          const f = [...document.querySelectorAll('#cs-layer-drawer input[data-layer="iplan-current"]')][0];
          const l = window.__URBION_OFFICIAL_LAYERS__?.['iplan-current'];
          const traceText = document.body.innerText;
          if (!f) return '11';
          if (!window.__URBION_FORENSIC__) return '11';
          return null;
        })()
        """)
        # Classification is computed deterministically from emitted Python trace records below.
        records = [json.loads(line) for line in TRACE_FILE.read_text(encoding="utf-8").splitlines()]
        kinds = [r["kind"] for r in records]
        def has(prefix): return any(k == prefix for k in kinds)
        reqs = [r for r in records if r["kind"] == "REQUEST"]
        resps = [r for r in records if r["kind"] == "RESPONSE"]
        fails = [r for r in records if r["kind"] == "REQUEST_FAILED"]
        if not has("V7_HANDLER::FIRED") and not any("FORENSIC::V7_HANDLER::FIRED" in c for c in console_errors): cls = 1
        elif not has("setOfficialActive::BEGIN") and not any("V7_HANDLER::FIRED" in c for c in console_errors): cls = 2
        elif any("setOfficialActive::THROW_FROM" in c or "syncLayerState::THROW" in c for c in console_errors): cls = 3
        elif any("officialLayer::NULL" in c for c in console_errors): cls = 4
        elif not any("layer.addTo::BEFORE" in c for c in console_errors): cls = 5
        elif not any("createTile::BEGIN" in c for c in console_errors): cls = 6
        else:
            correct = [r for r in reqs if "GTsemasa_04/MapServer/export" in r["url"]]
            if not correct: cls = 7
            elif fails: cls = 8
            elif resps and not any("tileload::EVENT" in c for c in console_errors): cls = 9
            elif any("tileload::EVENT" in c for c in console_errors): cls = 10 if page.evaluate("window.__URBION_QA__?.layers?.['iplan-current']?.renderStatus") != 'RENDERED' else 11
            else: cls = 11
        emit("CLASSIFICATION", code=cls)
        capture = page.screenshot(path=ARTIFACT_DIR / "final.png", full_page=True)
        browser.close()

    raise SystemExit(0)


if __name__ == "__main__":
    main()
