"""Diagnostic-only Playwright tracing for the championship browser gate.

Loaded automatically because the browser QA script lives in this directory.
The tracer activates only around Locator.check() for the iplan-current
checkbox and only records runtime evidence; it does not alter production files.
"""
from __future__ import annotations

import hashlib
import json
import os
import time

try:
    from playwright.sync_api import Locator
except Exception:  # pragma: no cover - diagnostic hook only
    Locator = None  # type: ignore[assignment]


_ENABLED = os.getenv("URBION_DISABLE_FORENSIC_TRACE") != "1"
_ORIGINAL_CHECK = getattr(Locator, "check", None) if Locator is not None else None


def _emit(label: str, payload):
    print(f"FORENSIC::{label}::{json.dumps(payload, ensure_ascii=False, default=str)}", flush=True)


def _safe_eval(page, expression, arg=None):
    try:
        return page.evaluate(expression, arg)
    except Exception as exc:  # pragma: no cover - diagnostic path
        return {"error": f"{type(exc).__name__}: {exc}"}


def _served_bundle(page):
    try:
        base = os.getenv("BASE_URL", "http://127.0.0.1:8765")
        response = page.request.get(base + "/urbion_championship_command_shell.js", timeout=10_000)
        text = response.text()
        markers = {
            "status": response.status,
            "bytes": len(text.encode("utf-8")),
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "syncLayerState_count": text.count("function syncLayerState"),
            "syncLayerState_call_count": text.count("syncLayerState("),
            "v7_guard_count": text.count("__URBION_PREMIUM_V7_INTEGRATION__"),
            "officialLayer_count": text.count("function officialLayer"),
            "bundle_index_sync": text.find("function syncLayerState"),
            "bundle_index_v7_services": text.find("const OFFICIAL_SERVICES"),
            "bundle_index_v7_guard": text.find("__URBION_PREMIUM_V7_INTEGRATION__"),
            "bundle_index_qa": text.find("window.__URBION_QA__"),
            "contains_GTsemasa_service": "GTsemasa_" in text,
            "contains_export_constructor": "MapServer/export?bbox=" in text,
        }
        _emit("SERVED_BUNDLE", markers)
    except Exception as exc:  # pragma: no cover - diagnostic path
        _emit("SERVED_BUNDLE_ERROR", f"{type(exc).__name__}: {exc}")


def _dom_snapshot(page, phase: str):
    state = _safe_eval(
        page,
        r"""() => {
          const input = document.querySelector('#cs-layer-drawer input[data-layer="iplan-current"]');
          const row = input?.closest('.fcc-layer-row');
          const drawer = document.querySelector('#cs-layer-drawer');
          const map = window.__URBION_FCC_MAP__;
          const layer = window.__URBION_OFFICIAL_LAYERS__?.['iplan-current'];
          const tileKeys = layer?._tiles ? Object.keys(layer._tiles) : [];
          let mapSize = null, center = null, zoom = null;
          try { mapSize = map?.getSize?.(); center = map?.getCenter?.(); zoom = map?.getZoom?.(); } catch {}
          return {
            phase,
            typeofL: typeof window.L,
            typeofMap: typeof window.__URBION_FCC_MAP__,
            typeofV7: typeof window.__URBION_PREMIUM_V7_INTEGRATION__,
            typeofSyncLayerState: typeof window.syncLayerState,
            officialStoreExists: !!window.__URBION_OFFICIAL_LAYERS__,
            qaLayer: window.__URBION_QA__?.layers?.['iplan-current'] || null,
            drawerVisible: !!drawer && !!drawer.getClientRects().length,
            stateValue: document.querySelector('#cs-state')?.value || '',
            inputCount: document.querySelectorAll('#cs-layer-drawer input[data-layer="iplan-current"]').length,
            input: input ? {
              checked: input.checked,
              disabled: input.disabled,
              visible: !!input.getClientRects().length,
              connected: input.isConnected,
              officialInputWired: input.dataset.officialInputWired || null,
              diagnosticId: input.__urbionDiagnosticId || null,
            } : null,
            row: row ? { classList: Array.from(row.classList), small: row.querySelector('span small, small')?.textContent || '' } : null,
            expectedUrl: 'https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN/GTsemasa_04/MapServer',
            layer: layer ? {
              constructor: layer.constructor?.name || null,
              official: layer.__urbionOfficial,
              layerId: layer.__urbionLayerId,
              source: layer.__urbionSource,
              mapAttached: !!layer._map,
              tileCount: tileKeys.length,
              container: !!layer._container,
              tileZoom: layer._tileZoom ?? null,
            } : null,
            map: { zoom, center, size: mapSize ? {x: mapSize.x, y: mapSize.y} : null },
          };
        }""",
    )
    _emit("DOM", state)


def _install_runtime_hooks(page):
    expression = r"""() => {
      if (window.__URBION_FORENSIC_TRACE__) return 'already-installed';
      const trace = window.__URBION_FORENSIC_TRACE__ = {events: [], installedAt: performance.now()};
      const now = () => Number(performance.now().toFixed(3));
      const record = (type, data={}) => { trace.events.push({t: now(), type, ...data}); };
      trace.record = record;

      const input = document.querySelector('#cs-layer-drawer input[data-layer="iplan-current"]');
      if (input) {
        input.__urbionDiagnosticId = 'iplan-current-target-v1';
        input.addEventListener('change', () => record('CHECKBOX_CHANGE_CAPTURE', {
          checked: input.checked,
          connected: input.isConnected,
          wired: input.dataset.officialInputWired || null,
        }), true);
      }

      const drawer = document.querySelector('#cs-layer-drawer');
      if (drawer) {
        drawer.addEventListener('change', e => record('DRAWER_CHANGE_CAPTURE', {
          targetLayer: e.target?.dataset?.layer || null,
          targetContextLayer: e.target?.dataset?.contextLayer || null,
          checked: !!e.target?.checked,
        }), true);
      }

      const originalImgSrc = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, 'src');
      if (originalImgSrc?.get && originalImgSrc?.set && !window.__URBION_FORENSIC_IMG_SRC__) {
        window.__URBION_FORENSIC_IMG_SRC__ = originalImgSrc;
        Object.defineProperty(HTMLImageElement.prototype, 'src', {
          configurable: originalImgSrc.configurable,
          enumerable: originalImgSrc.enumerable,
          get: originalImgSrc.get,
          set(value) {
            const src = String(value);
            if (src.includes('GTsemasa') || src.includes('scharms.planmalaysia.gov.my')) record('IMG_SRC_SET', {src});
            return originalImgSrc.set.call(this, value);
          }
        });
      }

      if (window.L?.GridLayer?.prototype && !window.L.GridLayer.prototype.__urbionForensicWrapped) {
        const proto = window.L.GridLayer.prototype;
        const originalOnAdd = proto.onAdd;
        const originalUpdate = proto._update;
        proto.onAdd = function(map) {
          const result = originalOnAdd.apply(this, arguments);
          record('GRID_ONADD', {
            constructor: this.constructor?.name || null,
            official: !!this.__urbionOfficial,
            layerId: this.__urbionLayerId || null,
            source: this.__urbionSource || null,
            mapAttached: !!this._map,
          });
          return result;
        };
        proto._update = function() {
          const self = this;
          const originalCreate = self.createTile;
          self.createTile = function(coords, done) {
            record('CREATE_TILE', {layerId: self.__urbionLayerId || null, coords: {x: coords?.x, y: coords?.y, z: coords?.z}});
            const tile = originalCreate.apply(this, arguments);
            record('CREATE_TILE_RETURN', {
              layerId: self.__urbionLayerId || null,
              tileSrc: tile?.src || null,
              hasOnLoad: typeof tile?.onload === 'function',
              hasOnError: typeof tile?.onerror === 'function',
            });
            return tile;
          };
          try { return originalUpdate.apply(this, arguments); }
          finally { self.createTile = originalCreate; }
        };
        proto.__urbionForensicWrapped = true;
      }

      const map = window.__URBION_FCC_MAP__;
      if (map && !map.__urbionForensicLayerHook) {
        map.__urbionForensicLayerHook = true;
        map.on('layeradd', e => record('MAP_LAYER_ADD', {
          constructor: e.layer?.constructor?.name || null,
          official: !!e.layer?.__urbionOfficial,
          layerId: e.layer?.__urbionLayerId || null,
          source: e.layer?.__urbionSource || null,
          hasMap: !!e.layer?._map,
        }));
        map.on('layerremove', e => record('MAP_LAYER_REMOVE', {
          constructor: e.layer?.constructor?.name || null,
          official: !!e.layer?.__urbionOfficial,
          layerId: e.layer?.__urbionLayerId || null,
        }));
      }
      record('RUNTIME_HOOKS_INSTALLED');
      return 'installed';
    }"""
    _emit("HOOKS", _safe_eval(page, expression))


def _attach_events(page):
    def request(req):
        url = req.url
        if any(x in url for x in ("GTsemasa", "GTzoning", "MapServer", "/export", "scharms.planmalaysia.gov.my")):
            _emit("REQUEST", {"method": req.method, "url": url, "resourceType": req.resource_type})

    def response(resp):
        url = resp.url
        if any(x in url for x in ("GTsemasa", "GTzoning", "MapServer", "/export", "scharms.planmalaysia.gov.my")):
            _emit("RESPONSE", {"status": resp.status, "url": url})

    def failed(req):
        url = req.url
        if any(x in url for x in ("GTsemasa", "GTzoning", "MapServer", "/export", "scharms.planmalaysia.gov.my")):
            _emit("REQUEST_FAILED", {"url": url, "failure": req.failure})

    page.on("request", request)
    page.on("response", response)
    page.on("requestfailed", failed)


def _event_trace(page):
    trace = _safe_eval(page, "() => window.__URBION_FORENSIC_TRACE__?.events || []")
    _emit("EVENT_TRACE", trace)


def _listener_trace(page):
    try:
        cdp = page.context.new_cdp_session(page)
        out = {}
        for selector, label in [
            ('#cs-layer-drawer input[data-layer="iplan-current"]', 'input'),
            ('#cs-layer-drawer', 'drawer'),
        ]:
            result = cdp.send("Runtime.evaluate", {"expression": f"document.querySelector({json.dumps(selector)})", "objectGroup": "urbion-forensic"})
            object_id = result.get("result", {}).get("objectId")
            if not object_id:
                out[label] = {"error": "no objectId"}
                continue
            listeners = cdp.send("DOMDebugger.getEventListeners", {"objectId": object_id}).get("listeners", [])
            out[label] = [
                {
                    "type": item.get("type"),
                    "useCapture": item.get("useCapture"),
                    "passive": item.get("passive"),
                    "once": item.get("once"),
                    "scriptId": item.get("scriptId"),
                    "handler": item.get("handler", {}).get("description"),
                }
                for item in listeners
                if item.get("type") == "change"
            ]
        _emit("LISTENERS", out)
        cdp.detach()
    except Exception as exc:  # pragma: no cover - Chromium/CDP diagnostic path
        _emit("LISTENERS_ERROR", f"{type(exc).__name__}: {exc}")


def _diagnostic_check(self, *args, **kwargs):
    page = getattr(getattr(self, "_frame", None), "_page", None)
    if page is None:
        return _ORIGINAL_CHECK(self, *args, **kwargs)
    selector = getattr(self, "_selector", "")
    if "iplan-current" not in selector:
        return _ORIGINAL_CHECK(self, *args, **kwargs)

    _emit("HEAD", os.getenv("GITHUB_SHA") or "unknown")
    _served_bundle(page)
    _dom_snapshot(page, "BEFORE_CHECK")
    _listener_trace(page)
    _attach_events(page)
    _install_runtime_hooks(page)
    _dom_snapshot(page, "BEFORE_CHECK_HOOKED")

    started = time.perf_counter()
    result = None
    error = None
    try:
        result = _ORIGINAL_CHECK(self, *args, **kwargs)
        return result
    except Exception as exc:
        error = exc
        raise
    finally:
        elapsed_ms = round((time.perf_counter() - started) * 1000, 3)
        _emit("CHECK_RESULT", {"elapsed_ms": elapsed_ms, "exception": repr(error) if error else None, "returned": result is not None})
        _event_trace(page)
        _dom_snapshot(page, "AFTER_CHECK_OR_ERROR")
        _listener_trace(page)
        _emit("FINAL_QA", _safe_eval(page, "() => window.__URBION_QA__?.layers?.['iplan-current'] || null"))


if _ENABLED and _ORIGINAL_CHECK is not None:
    Locator.check = _diagnostic_check
