#!/usr/bin/env python3
"""Preflight authoritative i-Plan WMS directly and through the canonical proxy.

This intentionally probes a small, representative set before the browser's
25-layer loop. It distinguishes upstream availability from frontend/runtime
failures and records timing/content-type evidence without changing product data.
"""
from __future__ import annotations

import os
import time
from urllib.parse import urlencode

import httpx

BASE_URL = os.getenv("URBION_BASE_URL", "http://127.0.0.1:8765").rstrip("/")
UPSTREAM = "https://iplan.planmalaysia.gov.my/geoserver/iplan/wms"
LAYERS = [
    "iplan:gunatanah_semasa_04",
    "iplan:gunatanah_zoning_04",
    "iplan:gunatanah_komited_04",
    "iplan:rfn",
    "iplan:rsn",
    "iplan:banjir",
    "iplan:ksas",
    "iplan:cfs",
    "iplan:rangkaian_ekologi",
    "iplan:warisan",
    "iplan:rumah_mampu_milik",
    "iplan:topo",
    "iplan:hakisan_pantai",
    "iplan:rmm01",
]


def mercator(lon: float, lat: float) -> tuple[float, float]:
    x = lon * 20037508.34 / 180.0
    y = 20037508.34 / 180.0
    y *= __import__("math").log(__import__("math").tan((90 + lat) * __import__("math").pi / 360.0))
    return x, y


def probe(client: httpx.Client, url: str, params: dict[str, str]) -> tuple[int, str, int, float, str]:
    started = time.perf_counter()
    try:
        r = client.get(url, params=params)
        elapsed = time.perf_counter() - started
        ct = r.headers.get("content-type", "")
        return r.status_code, ct, len(r.content), elapsed, r.url.path if hasattr(r.url, "path") else str(r.url)
    except Exception as exc:
        elapsed = time.perf_counter() - started
        return 0, "", 0, elapsed, f"ERROR: {type(exc).__name__}: {exc}"


def main() -> None:
    west, south = mercator(102.17, 2.24)
    east, north = mercator(102.23, 2.33)
    bbox = f"{west},{south},{east},{north}"
    params_base = {
        "service": "WMS",
        "request": "GetMap",
        "styles": "",
        "format": "image/png",
        "transparent": "true",
        "version": "1.1.1",
        "tiled": "true",
        "width": "256",
        "height": "256",
        "srs": "EPSG:3857",
        "bbox": bbox,
    }
    failures: list[str] = []
    with httpx.Client(timeout=httpx.Timeout(25.0, connect=10.0), follow_redirects=True, headers={
        "User-Agent": "URBION-HORIZON-GIS-Preflight/1.0",
        "Referer": "https://www.planmalaysia.gov.my/",
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    }) as client:
        print(f"GIS UPSTREAM PREFLIGHT · {len(LAYERS)} representative i-Plan layers")
        for layer in LAYERS:
            params = dict(params_base, layers=layer)
            status, ct, size, elapsed, detail = probe(client, UPSTREAM, params)
            ok = status == 200 and ct.lower().startswith("image/") and size > 100
            print(f"DIRECT {'PASS' if ok else 'FAIL'} · {layer} · HTTP={status} · CT={ct or '-'} · bytes={size} · {elapsed:.2f}s · {detail}")
            if not ok:
                failures.append(f"DIRECT {layer}: HTTP={status} CT={ct or '-'} bytes={size} detail={detail}")

        print(f"GIS PROXY PREFLIGHT · {BASE_URL}/map/wms")
        for layer in LAYERS:
            params = dict(params_base, layers=layer)
            status, ct, size, elapsed, detail = probe(client, f"{BASE_URL}/map/wms", params)
            ok = status == 200 and ct.lower().startswith("image/") and size > 100
            print(f"PROXY {'PASS' if ok else 'FAIL'} · {layer} · HTTP={status} · CT={ct or '-'} · bytes={size} · {elapsed:.2f}s · {detail}")
            if not ok:
                failures.append(f"PROXY {layer}: HTTP={status} CT={ct or '-'} bytes={size} detail={detail}")

    if failures:
        raise SystemExit("\n".join(["GIS PREFLIGHT FAILURES:", *failures]))
    print("GIS authoritative upstream + canonical proxy preflight: PASS")


if __name__ == "__main__":
    main()
