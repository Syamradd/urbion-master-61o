#!/usr/bin/env python3
"""Diagnostic-only URBION map-reset forensic runner.

This file lives outside the repository/test suite and makes no source changes.
It targets an already-running URBION server via BASE_URL (default 127.0.0.1:8765),
replays the browser-QA TOD cycle, instruments Leaflet/ResizeObserver in-page only,
and writes screenshots + JSON metrics for A, TOD, B-immediate, B+1RAF, B+2RAF,
and B+100ms.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image
from playwright.sync_api import expect, sync_playwright

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8765")
OUT = Path(os.getenv("DIAG_OUT", "/tmp/diagnostic-map-reset"))
OUT.mkdir(parents=True, exist_ok=True)

CASE = {
    "project_name": "Browser QA · Sg. Udang",
    "lat": "2.285",
    "lon": "102.196",
    "state": "Melaka",
    "pbt": "Majlis Bandaraya Melaka Bersejarah",
    "district": "Melaka Tengah",
    "landuse": "Komersial",
    "category": "Pembangunan Penggunaan Bercampur",
    "activity": "TOD / Mixed Use",
    "development": "New Development",
    "ratio": "4.5",
}

INSTRUMENTATION = r"""
(() => {
  const d = window.__URBION_DIAG__ = {
    events: [], resizeObserverCallbacks: 0, invalidateSizeCalls: 0,
    setViewCalls: 0, rafScheduled: 0, rafExecuted: 0,
    windowResize: 0, fullscreenchange: 0, mapClicks: 0,
    todInput: 0, todChange: 0, layerAdds: [], layerRemoves: [],
    startedAt: performance.now()
  };
  const push = (type, data={}) => d.events.push({t: performance.now(), type, ...data});

  const NativeRO = window.ResizeObserver;
  if (NativeRO) {
    window.ResizeObserver = class DiagnosticResizeObserver {
      constructor(cb) {
        this._cb = cb;
        this._ro = new NativeRO((entries, observer) => {
          d.resizeObserverCallbacks++;
          push('resize-observer', {count: d.resizeObserverCallbacks,
            entries: entries.map(e => ({width:e.contentRect.width,height:e.contentRect.height}))});
          cb(entries, observer);
        });
      }
      observe(...args){ return this._ro.observe(...args); }
      unobserve(...args){ return this._ro.unobserve(...args); }
      disconnect(...args){ return this._ro.disconnect(...args); }
    };
  }

  const NativeRAF = window.requestAnimationFrame.bind(window);
  window.requestAnimationFrame = (cb) => {
    d.rafScheduled++;
    return NativeRAF((ts) => { d.rafExecuted++; push('raf', {ts}); cb(ts); });
  };
  window.cancelAnimationFrame = window.cancelAnimationFrame.bind(window);

  window.addEventListener('resize', () => { d.windowResize++; push('window-resize'); }, true);
  document.addEventListener('fullscreenchange', () => { d.fullscreenchange++; push('fullscreenchange'); }, true);
  document.addEventListener('click', e => {
    if (e.target?.closest?.('#cs-map')) { d.mapClicks++; push('map-click'); }
  }, true);
  document.addEventListener('input', e => {
    if (e.target?.matches?.('#cs-todlat,#cs-todlon')) { d.todInput++; push('tod-input',{id:e.target.id,value:e.target.value}); }
  }, true);
  document.addEventListener('change', e => {
    if (e.target?.matches?.('#cs-todlat,#cs-todlon')) { d.todChange++; push('tod-change',{id:e.target.id,value:e.target.value}); }
  }, true);

  const classify = (layer) => {
    const out = {type: layer?.constructor?.name || 'unknown'};
    try {
      const ll = layer?.getLatLng?.();
      if (ll) out.latlng = {lat:+ll.lat.toFixed(6), lng:+ll.lng.toFixed(6)};
    } catch {}
    try { out.hasElement = !!layer?._path || !!layer?._icon; } catch {}
    try { out._pathClass = layer?._path?.getAttribute?.('class') || null; } catch {}
    return out;
  };

  function patchLeaflet(){
    if (!window.L || window.L.__URBION_DIAG_PATCHED__) return false;
    window.L.__URBION_DIAG_PATCHED__ = true;
    const MapProto = window.L.Map.prototype;
    const oldInvalidate = MapProto.invalidateSize;
    MapProto.invalidateSize = function(...args){
      d.invalidateSizeCalls++;
      let size=null, center=null, zoom=null;
      try { const s=this.getSize(); size={x:s.x,y:s.y}; } catch {}
      try { const c=this.getCenter(); center={lat:c.lat,lng:c.lng}; } catch {}
      try { zoom=this.getZoom(); } catch {}
      push('invalidate-size',{n:d.invalidateSizeCalls,size,center,zoom,args});
      return oldInvalidate.apply(this,args);
    };
    const oldSetView = MapProto.setView;
    MapProto.setView = function(...args){
      d.setViewCalls++;
      push('set-view',{n:d.setViewCalls,args});
      return oldSetView.apply(this,args);
    };
    const oldAddLayer = MapProto.addLayer;
    MapProto.addLayer = function(layer){
      const rec=classify(layer); d.layerAdds.push(rec); push('layer-add',rec);
      return oldAddLayer.apply(this,arguments);
    };
    const oldRemoveLayer = MapProto.removeLayer;
    MapProto.removeLayer = function(layer){
      const rec=classify(layer); d.layerRemoves.push(rec); push('layer-remove',rec);
      return oldRemoveLayer.apply(this,arguments);
    };
    const m = window.__URBION_FCC_MAP__;
    if (m && !m.__URBION_DIAG_MAP_EVENTS__) {
      m.__URBION_DIAG_MAP_EVENTS__ = true;
      m.on('moveend',()=>push('map-moveend'));
      m.on('zoomend',()=>push('map-zoomend'));
      m.on('resize',()=>push('map-resize'));
      m.on('viewreset',()=>push('map-viewreset'));
      m.on('load',()=>push('map-load'));
    }
    return true;
  }

  const timer = setInterval(patchLeaflet, 10);
  d.stop = () => clearInterval(timer);
})();
"""


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def image_diff(a: Path, b: Path) -> dict[str, Any]:
    A = np.asarray(Image.open(a).convert("RGBA"))
    B = np.asarray(Image.open(b).convert("RGBA"))
    if A.shape != B.shape:
        return {"same_dimensions": False, "a_dimensions": [A.shape[1],A.shape[0]], "b_dimensions": [B.shape[1],B.shape[0]]}
    diff = np.any(A != B, axis=2)
    count = int(diff.sum())
    result = {
        "same_dimensions": True,
        "dimensions": [A.shape[1], A.shape[0]],
        "differing_pixels": count,
        "differing_pixel_percentage": float(count / diff.size * 100.0),
    }
    if count:
        ys, xs = np.where(diff)
        result["difference_bbox"] = [int(xs.min()), int(ys.min()), int(xs.max()+1), int(ys.max()+1)]
    else:
        result["difference_bbox"] = None
    return result


def metrics(page) -> dict[str, Any]:
    return page.evaluate(r"""
    function() {
      var map = window.__URBION_FCC_MAP__;
      var el = document.querySelector('#cs-map');
      var rect = el ? el.getBoundingClientRect() : null;
      var q = function(s) { return Array.prototype.slice.call(document.querySelectorAll(s)); };
      var loaded = q('.leaflet-tile-pane img').filter(function(i) { return i.complete && i.naturalWidth > 0; });
      var tiles = q('.leaflet-tile-pane img').map(function(i) {
        var r = i.getBoundingClientRect();
        return {src:i.currentSrc || i.src, complete:i.complete, naturalWidth:i.naturalWidth,
          rect:{x:r.x,y:r.y,width:r.width,height:r.height}, cls:i.className};
      });
      var canvases = q('#cs-map canvas').map(function(c) {
        var r=c.getBoundingClientRect();
        return {rect:{x:r.x,y:r.y,width:r.width,height:r.height}, width:c.width,height:c.height};
      });
      var svgs = q('#cs-map svg').map(function(s) {
        var r=s.getBoundingClientRect();
        return {rect:{x:r.x,y:r.y,width:r.width,height:r.height}};
      });
      var markers = q('#cs-map .leaflet-marker-pane img, #cs-map .leaflet-marker-pane .leaflet-marker-icon');
      var center=null, bounds=null, zoom=null, mapSize=null;
      if (map) {
        var c=map.getCenter(); center={lat:c.lat,lng:c.lng};
        var b=map.getBounds(); bounds={north:b.getNorth(),south:b.getSouth(),east:b.getEast(),west:b.getWest()};
        zoom=map.getZoom();
        var s=map.getSize(); mapSize={x:s.x,y:s.y};
      }
      var vectorLayers=[];
      try {
        map.eachLayer(function(l) {
          var latlng=null, points=null;
          try { var x=l.getLatLng && l.getLatLng(); if (x) latlng={lat:Number(x.lat.toFixed(6)),lng:Number(x.lng.toFixed(6))}; } catch (e) {}
          try { var pts=l.getLatLngs && l.getLatLngs(); if (pts) points=pts.map(function(x){return {lat:x.lat,lng:x.lng};}); } catch (e) {}
          vectorLayers.push({type:(l && l.constructor && l.constructor.name) || 'unknown',
            latlng:latlng, points:points, hasPath:!!(l && l._path), hasIcon:!!(l && l._icon),
            hasCanvas:!!(l && l._renderer && l._renderer._container)});
        });
      } catch (e) {}
      var stage=document.querySelector('.map-stage');
      var stageRect=null;
      if (stage) { var sr=stage.getBoundingClientRect(); stageRect={x:sr.x,y:sr.y,width:sr.width,height:sr.height}; }
      var todLat=document.querySelector('#cs-todlat');
      var todLon=document.querySelector('#cs-todlon');
      var sigTod=document.querySelector('#sig-tod');
      var statTod=document.querySelector('#stat-tod');
      return {
        time:performance.now(), center:center, zoom:zoom, bounds:bounds, mapSize:mapSize,
        mapRect:rect ? {x:rect.x,y:rect.y,width:rect.width,height:rect.height} : null,
        clientWidth:el ? el.clientWidth : null, clientHeight:el ? el.clientHeight : null,
        scrollWidth:el ? el.scrollWidth : null, scrollHeight:el ? el.scrollHeight : null,
        stageRect:stageRect, devicePixelRatio:window.devicePixelRatio, screenshotTargetSize:null,
        tileCount:tiles.length, loadedTileCount:loaded.length, tiles:tiles,
        canvasCount:canvases.length, canvases:canvases, svgCount:svgs.length, svgs:svgs,
        markerCount:markers.length, vectorLayers:vectorLayers,
        overlayCounts:{circles:q('#cs-map .leaflet-overlay-pane circle').length,
          paths:q('#cs-map .leaflet-overlay-pane path').length,
          polylines:q('#cs-map .leaflet-overlay-pane path').length},
        dom:{todLat:todLat ? todLat.value : '', todLon:todLon ? todLon.value : '',
          sigTod:sigTod ? sigTod.textContent : '', statTod:statTod ? statTod.textContent : ''}
      };
    }
    """)


def capture_map(page, label: str) -> dict[str, Any]:
    path = OUT / f"{label}.png"
    locator = page.locator("#cs-map")
    locator.screenshot(path=str(path))
    m = metrics(page)
    m["screenshot_dimensions"] = list(Image.open(path).size)
    m["screenshot_sha256"] = sha(path)
    return {"path": str(path), "metrics": m}


def wait_for_option(page, selector: str, label: str, timeout_ms: int = 10_000) -> None:
    page.locator(selector).wait_for(state="visible", timeout=timeout_ms)
    page.wait_for_function(
        """({selector, label}) => Array.from(document.querySelector(selector)?.options || [])
            .some(option => option.textContent.trim() === label)""",
        arg={"selector": selector, "label": label},
        timeout=timeout_ms,
    )


def set_field(page, key: str, value: str) -> None:
    locator = page.locator(f"#cs-{key}")
    tag = locator.evaluate("(el) => el.tagName")
    if tag == "SELECT":
        wait_for_option(page, f"#cs-{key}", value)
        locator.select_option(label=value)
    else:
        locator.fill(value)


def populate_case(page) -> None:
    select_keys = [
        "state", "pbt", "district", "landuse",
        "category", "activity", "development",
    ]
    for key in select_keys:
        set_field(page, key, CASE[key])
    for key, value in CASE.items():
        if key not in select_keys:
            set_field(page, key, value)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width":1440,"height":900,"device_scale_factor":1})
        page.add_init_script(INSTRUMENTATION)
        page.goto(BASE_URL, wait_until="domcontentloaded")
        page.wait_for_function("window.__URBION_FCC_MAP__ && document.querySelector('#cs-run')")

        populate_case(page)
        page.locator("#cs-todlat").locator("xpath=ancestor::details[1]").locator("summary").click()
        expect(page.locator("#cs-todlat")).to_be_visible()
        page.locator("#cs-run").click()
        expect(page.locator("#cs-status-pill")).to_have_text("ANALYSIS READY", timeout=30_000)
        expect(page.locator("#sig-tod")).to_have_text("NOT PROVIDED")
        A = capture_map(page,"A_blank")

        page.locator("#cs-todlat").fill("2.290")
        page.locator("#cs-todlon").fill("102.200")
        expect(page.locator("#cs-map .leaflet-marker-pane img")).to_have_count(1)
        TOD = capture_map(page,"TOD_valid")

        page.locator("#cs-todlat").fill("")
        page.locator("#cs-todlon").fill("")
        expect(page.locator("#sig-tod")).to_have_text("NOT PROVIDED")
        expect(page.locator("#stat-tod")).to_have_text("—")
        expect(page.locator("#cs-map .leaflet-marker-pane img")).to_have_count(0)
        B0 = capture_map(page,"B_immediate")

        page.evaluate("""() => new Promise(requestAnimationFrame)""")
        B1 = capture_map(page,"B_1raf")

        page.evaluate("""() => new Promise(requestAnimationFrame)""")
        B2 = capture_map(page,"B_2raf")

        page.evaluate("""() => new Promise(r => setTimeout(r, 100))""")
        B100 = capture_map(page,"B_100ms")

        states = {"A":A,"TOD":TOD,"B_immediate":B0,"B_1raf":B1,"B_2raf":B2,"B_100ms":B100}
        diffs={}
        for key in ("B_immediate","B_1raf","B_2raf","B_100ms"):
            diffs[f"A_vs_{key}"]=image_diff(Path(A["path"]),Path(states[key]["path"]))
        for a,b in (("B_immediate","B_1raf"),("B_1raf","B_2raf"),("B_2raf","B_100ms")):
            diffs[f"{a}_vs_{b}"]=image_diff(Path(states[a]["path"]),Path(states[b]["path"]))

        instrumentation = page.evaluate("window.__URBION_DIAG__")
        report={"base_url":BASE_URL,"states":states,"diffs":diffs,"instrumentation":instrumentation}
        (OUT/"report.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
        print(json.dumps(report,indent=2))
        browser.close()

if __name__ == "__main__":
    main()
