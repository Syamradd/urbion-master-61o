#!/usr/bin/env python3
"""Preflight authoritative i-Plan GIS directly and through the canonical proxy.

The primary surface is i-Plan GeoWebCache. A small, explicit set of layers also
has an official PLANMalaysia ArcGIS REST rendering path when GWC currently
returns a GeoServer 400. CI validates that fallback rather than requiring a
known-broken cache path to remain green.
"""
from __future__ import annotations

import math
import os
import time

import httpx

BASE_URL = os.getenv("URBION_BASE_URL", "http://127.0.0.1:8765").rstrip("/")
UPSTREAM = "https://iplan.planmalaysia.gov.my/geoserver/gwc/service/wms"
LAYERS = [
    "iplan:gunatanah_semasa_04", "iplan:gunatanah_zoning_04", "iplan:gunatanah_komited_04",
    "iplan:rfn", "iplan:rsn", "iplan:banjir", "iplan:ksas", "iplan:cfs",
    "iplan:rangkaian_ekologi", "iplan:warisan", "iplan:rumah_mampu_milik", "iplan:topo",
    "iplan:hakisan_pantai", "iplan:rmm01",
]
ARCGIS_FALLBACKS = {
    "iplan:gunatanah_semasa_04": (
        "https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN/GTsemasa_04/MapServer", 0,
    ),
    "iplan:gunatanah_zoning_04": (
        "https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN/GTzoning_04/MapServer", 0,
    ),
    "iplan:rfn": (
        "https://scharms.planmalaysia.gov.my/arcgis/rest/services/DPFDN/AlamSekitar/MapServer", 5,
    ),
    "iplan:ksas": (
        "https://scharms.planmalaysia.gov.my/arcgis/rest/services/DPFDN/AlamSekitar/MapServer", 2,
    ),
    "iplan:hakisan_pantai": (
        "https://scharms.planmalaysia.gov.my/arcgis/rest/services/DPFDN/Bencana/MapServer", 5,
    ),
}
WORLD = 20037508.342789244
# EPSG:900913 gridset is anchored at the top-left corner of WebMercator.
GRID_ORIGIN = f"{-WORLD},{WORLD}"


def tile_bbox(lon: float, lat: float, zoom: int) -> tuple[str, int, int]:
    lat = max(-85.05112878, min(85.05112878, lat))
    n = 2**zoom
    x = int((lon + 180.0) / 360.0 * n)
    y = int((1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n)
    res = 2.0 * WORLD / (256.0 * n)
    min_x = -WORLD + x * 256.0 * res
    max_x = -WORLD + (x + 1) * 256.0 * res
    max_y = WORLD - y * 256.0 * res
    min_y = WORLD - (y + 1) * 256.0 * res
    return f"{min_x},{min_y},{max_x},{max_y}", x, y


def probe(client: httpx.Client, url: str, params: dict[str, str]) -> tuple[int, str, int, float, str]:
    started = time.perf_counter()
    try:
        r = client.get(url, params=params)
        elapsed = time.perf_counter() - started
        ct = r.headers.get("content-type", "")
        headers = ""
        for key in ("geowebcache-cache-result", "geowebcache-miss-reason", "geowebcache-gridset", "geowebcache-crs"):
            value = r.headers.get(key)
            if value:
                headers += f" {key}={value}"
        detail = f"{r.url.path}{headers}"
        if r.status_code >= 400:
            body = r.text[:700].replace("\n", " ").replace("\r", " ")
            detail += f" :: {body}"
        return r.status_code, ct, len(r.content), elapsed, detail
    except Exception as exc:
        return 0, "", 0, time.perf_counter() - started, f"ERROR: {type(exc).__name__}: {exc}"


def arcgis_params(base: dict[str, str], layer_id: int) -> dict[str, str]:
    return {
        "bbox": base["bbox"],
        "bboxSR": "3857",
        "imageSR": "3857",
        "size": f"{base['width']},{base['height']}",
        "dpi": "96",
        "format": "png32",
        "transparent": base["transparent"],
        "f": "image",
        "layers": f"show:{layer_id}",
    }


def main() -> None:
    bbox, tile_x, tile_y = tile_bbox(102.196, 2.285, 13)
    base = {
        "service": "WMS", "request": "GetMap", "styles": "", "format": "image/png",
        "transparent": "true", "version": "1.1.1", "tiled": "true",
        "width": "256", "height": "256", "srs": "EPSG:900913", "bbox": bbox,
        "tilesorigin": GRID_ORIGIN,
    }
    failures: list[str] = []
    with httpx.Client(timeout=httpx.Timeout(25.0, connect=10.0), follow_redirects=True, headers={
        "User-Agent": "URBION-HORIZON-GIS-Preflight/1.4",
        "Referer": "https://iplan.planmalaysia.gov.my/geoserver/demo",
        "Accept": "image/png,image/*,*/*;q=0.8",
        "Accept-Encoding": "identity",
    }) as client:
        print(f"GIS UPSTREAM PREFLIGHT · {len(LAYERS)} representative i-Plan layers · tile z13/{tile_x}/{tile_y} · EPSG:900913 · TILESORIGIN={GRID_ORIGIN}")
        for layer in LAYERS:
            status, ct, size, elapsed, detail = probe(client, UPSTREAM, dict(base, layers=layer))
            ok = status == 200 and ct.lower().startswith("image/") and size > 100
            print(f"GWC {'PASS' if ok else 'FAIL'} · {layer} · HTTP={status} · CT={ct or '-'} · bytes={size} · {elapsed:.2f}s · {detail}")
            if not ok:
                fallback = ARCGIS_FALLBACKS.get(layer)
                if fallback:
                    fallback_url, layer_id = fallback
                    f_status, f_ct, f_size, f_elapsed, f_detail = probe(
                        client, fallback_url + "/export", arcgis_params(base, layer_id)
                    )
                    f_ok = f_status == 200 and f_ct.lower().startswith("image/") and f_size > 100
                    print(f"ARCGIS FALLBACK {'PASS' if f_ok else 'FAIL'} · {layer} · HTTP={f_status} · CT={f_ct or '-'} · bytes={f_size} · {f_elapsed:.2f}s · {f_detail}")
                    if f_ok:
                        continue
                failures.append(f"UPSTREAM {layer}: GWC HTTP={status} CT={ct or '-'} bytes={size} detail={detail}")
        print(f"GIS PROXY PREFLIGHT · {BASE_URL}/map/wms")
        for layer in LAYERS:
            status, ct, size, elapsed, detail = probe(client, f"{BASE_URL}/map/wms", dict(base, layers=layer))
            ok = status == 200 and ct.lower().startswith("image/") and size > 100
            print(f"PROXY {'PASS' if ok else 'FAIL'} · {layer} · HTTP={status} · CT={ct or '-'} · bytes={size} · {elapsed:.2f}s · {detail}")
            if not ok:
                failures.append(f"PROXY {layer}: HTTP={status} CT={ct or '-'} bytes={size} detail={detail}")
    if failures:
        raise SystemExit("\n".join(["GIS PREFLIGHT FAILURES:", *failures]))
    print("GIS authoritative upstream + canonical proxy preflight: PASS")


if __name__ == "__main__":
    main()
