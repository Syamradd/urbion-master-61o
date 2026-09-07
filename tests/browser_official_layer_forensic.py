"""Standalone forensic browser probe for the i-Plan current land-use layer.

This deliberately stops after the official-layer interaction and only emits
runtime evidence. It does not modify the production bundle or QA assertion.
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8765")


def select(page, selector: str, label: str) -> None:
    page.locator(selector).select_option(label=label)


def emit(kind: str, payload) -> None:
    print(f"FORENSIC_STANDALONE::{kind}::{json.dumps(payload, ensure_ascii=False, default=str)}", flush=True)


def snap(page, phase: str) -> None:
    data = page.evaluate(r"""(phase) => {
      const input = document.querySelector('#cs-layer-drawer input[data-layer="iplan-current"]');
      const row = input?.closest('.fcc-layer-row');
      const drawer = document.querySelector('#cs-layer-drawer');
      const map = window.__URBION_FCC_MAP__;
      const layer = window.__URBION_OFFICIAL_LAYERS__?.['iplan-current'];
      let center = null, size = null, zoom = null;
      try { center = map?.getCenter?.(); size = map?.getSize?.(); zoom = map?.getZoom?.(); } catch {}
      return {
        phase,
        typeofL: typeof window.L,
        typeofMap: typeof window.__URBION_FCC_MAP__,
        typeofV7: typeof window.__URBION_PREMIUM_V7_INTEGRATION__,
        typeofSyncLayerState: typeof window.syncLayerState,
        officialStoreExists: !!window.__URBION_OFFICIAL_LAYERS__,
        qa: window.__URBION_QA__?.layers?.['iplan-current'] || null,
        state: document.querySelector('#cs-state')?.value || '',
        drawer: {exists: !!drawer, visible: !!drawer?.getClientRects?.().length},
        inputs: Array.from(document.querySelectorAll('#cs-layer-drawer input[data-layer="iplan-current"]')).map((el, i) => ({
          i, checked: el.checked, disabled: el.disabled, visible: !!el.getClientRects().length,
          connected: el.isConnected, nodeId: el.__forensicNodeId || null,
        })),
        row: row ? {classList: Array.from(row.classList), small: row.querySelector('span small, small')?.textContent || ''} : null,
        expectedService: 'https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN/GTsemasa_04/MapServer',
        layer: layer ? {
          constructor: layer.constructor?.name || null,
          official: layer.__urbionOfficial,
          layerId: layer.__urbionLayerId,
          source: layer.__urbionSource,
          mapAttached: !!layer._map,
          tiles: layer._tiles ? Object.keys(layer._tiles).length : 0,
          container: !!layer._container,
          tileZoom: layer._tileZoom ?? null,
        } : null,
        map: {zoom, center, size: size ? {x: size.x, y: size.y} : null},
      };
    }""", phase)
    emit("SNAPSHOT", data)


def install_hooks(page) -> None:
    result = page.evaluate(r"""() => {
      const out = {events: []};
      const now = () => Number(performance.now().toFixed(3));
      const record = (type, data={}) => { out.events.push({t: now(), type, ...data}); };
      window.__URBION_FORENSIC_STANDALONE__ = out;

      const inputs = document.querySelectorAll('#cs-layer-drawer input[data-layer="iplan-current"]');
      inputs.forEach((el, i) => {
        el.__forensicNodeId = `iplan-current-${i}-${Math.random().toString(36).slice(2, 8)}`;
        el.addEventListener('change', () => record('CHECKBOX_CHANGE_BUBBLE', {node: el.__forensicNodeId, checked: el.checked}), false);
        el.addEventListener('change', () => record('CHECKBOX_CHANGE_CAPTURE', {node: el.__forensicNodeId, checked: el.checked}), true);
      });

      const drawer = document.querySelector('#cs-layer-drawer');
      drawer?.addEventListener('change', e => record('DRAWER_CHANGE', {target: e.target?.dataset?.layer || null, checked: !!e.target?.checked}), true);

      if (window.L?.GridLayer?.prototype && !window.L.GridLayer.prototype.__urbionForensicStandalone) {
        const proto = window.L.GridLayer.prototype;
        const originalOnAdd = proto.onAdd;
        const originalAddTo = proto.addTo;
        proto.onAdd = function(map) {
          record('GRID_ONADD', {constructor: this.constructor?.name || null, layerId: this.__urbionLayerId || null, source: this.__urbionSource || null, attached: !!map});
          return originalOnAdd.apply(this, arguments);
        };
        proto.addTo = function(map) {
          record('GRID_ADD_TO', {constructor: this.constructor?.name || null, layerId: this.__urbionLayerId || null, source: this.__urbionSource || null});
          return originalAddTo.apply(this, arguments);
        };
        proto.__urbionForensicStandalone = true;
      }

      const map = window.__URBION_FCC_MAP__;
      map?.on('layeradd', e => record('MAP_LAYER_ADD', {constructor: e.layer?.constructor?.name || null, official: !!e.layer?.__urbionOfficial, layerId: e.layer?.__urbionLayerId || null, mapAttached: !!e.layer?._map}));
      map?.on('layerremove', e => record('MAP_LAYER_REMOVE', {constructor: e.layer?.constructor?.name || null, layerId: e.layer?.__urbionLayerId || null}));

      const OriginalImage = window.Image;
      if (!window.__URBION_FORENSIC_IMAGE_WRAPPED__) {
        window.Image = function(...args) {
          const img = new OriginalImage(...args);
          const descriptor = Object.getOwnPropertyDescriptor(Object.getPrototypeOf(img), 'src');
          if (descriptor?.set && descriptor?.get) {
            Object.defineProperty(img, 'src', {
              configurable: true,
              get: descriptor.get.bind(img),
              set(value) { const src=String(value); if (src.includes('GTsemasa') || src.includes('scharms.planmalaysia.gov.my')) record('IMG_SRC_SET',{src}); return descriptor.set.call(img,value); }
            });
          }
          return img;
        };
        window.Image.prototype = OriginalImage.prototype;
        window.__URBION_FORENSIC_IMAGE_WRAPPED__ = true;
      }

      record('HOOKS_INSTALLED');
      return true;
    }""")
    emit("HOOKS", result)


def main() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        page = context.new_page()

        page.on("console", lambda msg: emit("CONSOLE", {"type": msg.type, "text": msg.text}) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: emit("PAGEERROR", str(exc)))
        page.on("request", lambda req: emit("REQUEST", {"method": req.method, "url": req.url, "resourceType": req.resource_type}) if any(x in req.url for x in ("GTsemasa", "GTzoning", "MapServer", "/export", "scharms.planmalaysia.gov.my")) else None)
        page.on("response", lambda resp: emit("RESPONSE", {"status": resp.status, "url": resp.url}) if any(x in resp.url for x in ("GTsemasa", "GTzoning", "MapServer", "/export", "scharms.planmalaysia.gov.my")) else None)
        page.on("requestfailed", lambda req: emit("REQUEST_FAILED", {"url": req.url, "failure": req.failure}) if any(x in req.url for x in ("GTsemasa", "GTzoning", "MapServer", "/export", "scharms.planmalaysia.gov.my")) else None)

        for _ in range(40):
            try:
                if page.request.get(BASE_URL + "/health", timeout=2_000).status == 200:
                    break
            except Exception:
                pass
            page.wait_for_timeout(250)
        else:
            raise RuntimeError("Server did not become ready")

        page.goto(BASE_URL + "/", wait_until="networkidle", timeout=30_000)
        expect(page).to_have_title("URBION HORIZON — Planning Command Centre")
        expect(page.locator("#cs-map")).to_be_visible()

        page.locator("#cs-project_name").fill("Browser QA · Sg. Udang")
        page.locator("#cs-lat").fill("2.285")
        page.locator("#cs-lon").fill("102.196")
        select(page, "#cs-state", "Melaka")
        select(page, "#cs-pbt", "Majlis Bandaraya Melaka Bersejarah")
        select(page, "#cs-district", "Melaka Tengah")
        select(page, "#cs-landuse", "Komersial")
        select(page, "#cs-category", "Pembangunan Penggunaan Bercampur")
        select(page, "#cs-activity", "TOD / Mixed Use")
        select(page, "#cs-development", "New Development")
        page.locator("#cs-ratio").fill("4.5")
        page.locator("#cs-run").click()
        expect(page.locator("#cs-status-pill")).to_have_text("ANALYSIS READY", timeout=30_000)
        page.locator("#cs-map-layers").click()
        expect(page.locator("#cs-layer-drawer")).to_be_visible()

        install_hooks(page)
        snap(page, "BEFORE_CHECK")

        current = page.locator('#cs-layer-drawer input[data-layer="iplan-current"]')
        emit("CHECK_TARGET", {
          "count": current.count(),
          "checked": current.is_checked(),
          "disabled": current.is_disabled(),
          "visible": current.is_visible(),
          "nodeId": page.evaluate(r"""() => document.querySelector('#cs-layer-drawer input[data-layer="iplan-current"]')?.__forensicNodeId || null"""),
        })

        try:
            current.check()
            emit("CHECK_RETURNED", True)
        except Exception as exc:
            emit("CHECK_EXCEPTION", f"{type(exc).__name__}: {exc}")

        page.wait_for_timeout(5_000)
        snap(page, "AFTER_CHECK")
        emit("EVENT_TRACE", page.evaluate("() => window.__URBION_FORENSIC_STANDALONE__?.events || []"))
        emit("FINAL_QA", page.evaluate("() => window.__URBION_QA__?.layers?.['iplan-current'] || null"))
        browser.close()


if __name__ == "__main__":
    main()
