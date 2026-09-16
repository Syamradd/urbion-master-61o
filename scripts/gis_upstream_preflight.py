#!/usr/bin/env python3
"""Preflight authoritative i-Plan GIS directly and through the canonical proxy."""
from __future__ import annotations
import math
import os
import time
from urllib.parse import quote

import httpx

BASE_URL = os.getenv("URBION_BASE_URL", "http://127.0.0.1:8765").rstrip("/")
UPSTREAM = "https://iplan.planmalaysia.gov.my/geoserver/gwc/service/wms"
WMTS_UPSTREAMS = (
    "https://iplan.planmalaysia.gov.my/geoserver/gwc/service/wmts",
    "https://iplan.planmalaysia.gov.my/geoserver/service/wmts",
)
TMS_UPSTREAMS = (
    "https://iplan.planmalaysia.gov.my/geoserver/gwc/service/tms/1.0.0",
    "https://iplan.planmalaysia.gov.my/geoserver/service/tms/1.0.0",
)
ROOT_WMS_UPSTREAMS = (
    "https://iplan.planmalaysia.gov.my/geoserver/service/wms",
    "https://iplan.planmalaysia.gov.my/geoserver/wms",
    "https://iplan.planmalaysia.gov.my/geoserver/ows",
)
DIRECT_WMS = "https://iplan.planmalaysia.gov.my/geoserver/iplan/wms"
GWC_GRIDSET_ORIGIN = "-20037508.342789244,-20037508.342789244"
LAYERS = [
    "iplan:gunatanah_semasa_04", "iplan:gunatanah_zoning_04", "iplan:gunatanah_komited_04",
    "iplan:rfn", "iplan:rsn", "iplan:banjir", "iplan:ksas", "iplan:cfs",
    "iplan:rangkaian_ekologi", "iplan:warisan", "iplan:rumah_mampu_milik", "iplan:topo",
    "iplan:hakisan_pantai", "iplan:rmm01",
]
ARCGIS_FALLBACKS = {
    "iplan:gunatanah_semasa_04": ("https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN/GTsemasa_04/MapServer", 0),
    "iplan:gunatanah_zoning_04": ("https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN/GTzoning_04/MapServer", 0),
    "iplan:rfn": ("https://scharms.planmalaysia.gov.my/arcgis/rest/services/DPFDN/AlamSekitar/MapServer", 5),
    "iplan:ksas": ("https://scharms.planmalaysia.gov.my/arcgis/rest/services/DPFDN/AlamSekitar/MapServer", 2),
    "iplan:hakisan_pantai": ("https://scharms.planmalaysia.gov.my/arcgis/rest/services/DPFDN/Bencana/MapServer", 5),
    "iplan:banjir": ("https://scharms.planmalaysia.gov.my/arcgis/rest/services/DPFDN/Bencana/MapServer", 2),
    "iplan:gunatanah_komited_04": ("https://gisdev.planmalaysia.gov.my/server/rest/services/Hosted/MERGE_KOMITED/MapServer", 0),
    "iplan:warisan": ("https://gisdev.planmalaysia.gov.my/server/rest/services/RFN4/04_PERANCANGAN_SOSIAL/MapServer", 1),
    "iplan:topo": ("https://gisdev.planmalaysia.gov.my/server/rest/services/RFN4/04_PERANCANGAN_ALAM_SEKITAR/MapServer", 19),
}
DIRECT_WMS_FALLBACKS = {
    "iplan:gunatanah_komited_04", "iplan:rsn", "iplan:banjir", "iplan:warisan",
    "iplan:rumah_mampu_milik", "iplan:topo",
}
TMS_FALLBACK_LAYERS = {
    "iplan:gunatanah_komited_04", "iplan:rsn", "iplan:warisan",
    "iplan:rumah_mampu_milik", "iplan:topo",
}
WORLD = 20037508.342789244


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
        detail = str(r.url.path)
        if r.status_code >= 400 or not ct.lower().startswith("image/"):
            body = r.text[:500].replace("\n", " ").replace("\r", " ")
            detail += f" :: {body}"
        return r.status_code, ct, len(r.content), elapsed, detail
    except Exception as exc:
        return 0, "", 0, time.perf_counter() - started, f"ERROR: {type(exc).__name__}: {exc}"


def arcgis_params(base: dict[str, str], layer_id: int) -> dict[str, str]:
    return {
        "bbox": base["bbox"], "bboxSR": "3857", "imageSR": "3857",
        "size": f"{base['width']},{base['height']}", "dpi": "96", "format": "png32",
        "transparent": base["transparent"], "f": "image", "layers": f"show:{layer_id}",
    }


def untiled_wms_params(base: dict[str, str], layer: str) -> dict[str, str]:
    return {
        "service": "WMS", "request": "GetMap", "layers": layer, "styles": "",
        "format": "image/png", "transparent": "true", "version": "1.1.1",
        "width": base["width"], "height": base["height"], "srs": "EPSG:900913", "bbox": base["bbox"],
    }


def direct_wms_params(base: dict[str, str], layer: str) -> dict[str, str]:
    return untiled_wms_params(base, layer)


def gridset_wms_params(base: dict[str, str], layer: str) -> dict[str, str]:
    return {
        **untiled_wms_params(base, layer),
        "tiled": "true",
        "tilesorigin": GWC_GRIDSET_ORIGIN,
    }


def wmts_params(layer: str, zoom: int, x: int, y: int, matrix: str) -> dict[str, str]:
    return {
        "SERVICE": "WMTS", "REQUEST": "GetTile", "VERSION": "1.0.0",
        "LAYER": layer, "STYLE": "", "FORMAT": "image/png",
        "TILEMATRIXSET": "EPSG:900913", "TILEMATRIX": matrix,
        "TILEROW": str(y), "TILECOL": str(x),
    }


def tms_urls(layer: str, zoom: int, x: int, y_xyz: int):
    y_tms = (2**zoom - 1) - y_xyz
    encoded_layer = quote(layer, safe=":")
    return tuple(f"{base}/{encoded_layer}@EPSG:900913@png/{zoom}/{x}/{y_tms}.png" for base in TMS_UPSTREAMS)


def wmts_rest_urls(layer: str, zoom: int, x: int, y: int):
    encoded_layer = quote(layer, safe=":")
    for base in (
        "https://iplan.planmalaysia.gov.my/geoserver/gwc/service/wmts/rest",
        "https://iplan.planmalaysia.gov.my/geoserver/service/wmts/rest",
    ):
        for matrix in (f"EPSG:900913:{zoom}", str(zoom)):
            yield f"{base}/{encoded_layer}//EPSG:900913/{matrix}/{y}/{x}?format=image/png"


def _target_layers(selected: str | None) -> list[str]:
    if selected:
        if selected not in LAYERS:
            raise SystemExit(f"Unknown URBION_PREFLIGHT_LAYER: {selected}")
        return [selected]
    return list(LAYERS)


def main() -> None:
    selected = os.getenv("URBION_PREFLIGHT_LAYER")
    target_layers = _target_layers(selected)

    if not selected:
        import concurrent.futures
        import subprocess
        import sys
        failures = []
        max_workers = min(4, len(target_layers))
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {
                pool.submit(
                    subprocess.run,
                    [sys.executable, __file__],
                    env={**os.environ, "URBION_PREFLIGHT_LAYER": layer},
                    capture_output=True,
                    text=True,
                ): layer
                for layer in target_layers
            }
            ordered = {}
            for future, layer in [(future, futures[future]) for future in futures]:
                result = future.result()
                ordered[layer] = result
                if result.returncode != 0:
                    failures.append(layer)
            for layer in target_layers:
                result = ordered[layer]
                print(f"\n===== PREFLIGHT LAYER {layer} =====")
                if result.stdout:
                    print(result.stdout, end="")
                if result.stderr:
                    print(result.stderr, end="", file=sys.stderr)
        if failures:
            raise SystemExit("Parallel GIS preflight failures: " + ", ".join(failures))
        print(f"Parallel GIS authoritative + proxy preflight: PASS · {len(target_layers)}/{len(target_layers)} layers")
        return

    bbox, tile_x, tile_y = tile_bbox(102.196, 2.285, 13)
    base = {
        "service": "WMS", "request": "GetMap", "styles": "", "format": "image/png",
        "transparent": "true", "version": "1.1.1", "tiled": "true", "width": "256", "height": "256",
        "srs": "EPSG:900913", "bbox": bbox,
    }
    failures: list[str] = []
    with httpx.Client(timeout=httpx.Timeout(25.0, connect=10.0), follow_redirects=True, headers={
        "User-Agent": "URBION-HORIZON-GIS-Preflight/2.1",
        "Referer": "https://iplan.planmalaysia.gov.my/geoserver/demo",
        "Accept": "image/png,image/*,*/*;q=0.8", "Accept-Encoding": "identity", "Connection": "close",
    }) as client:
        print(f"GIS UPSTREAM PREFLIGHT · {len(target_layers)} representative i-Plan layers · tile z13/{tile_x}/{tile_y} · EPSG:900913")
        for layer in target_layers:
            status, ct, size, elapsed, detail = probe(client, UPSTREAM, dict(base, layers=layer))
            ok = status == 200 and ct.lower().startswith("image/") and size > 100
            print(f"GWC {'PASS' if ok else 'FAIL'} · {layer} · HTTP={status} · CT={ct or '-'} · bytes={size} · {elapsed:.2f}s · {detail}")
            if not ok:
                if layer in TMS_FALLBACK_LAYERS:
                    wmts_rest_ok = False
                    for wmts_rest_url in wmts_rest_urls(layer, 13, tile_x, tile_y):
                        r_status, r_ct, r_size, r_elapsed, r_detail = probe(client, wmts_rest_url, {})
                        r_ok = r_status == 200 and r_ct.lower().startswith("image/") and r_size > 100
                        print(f"GWC WMTS REST FALLBACK {'PASS' if r_ok else 'FAIL'} · {layer} · HTTP={r_status} · CT={r_ct or '-'} · bytes={r_size} · {r_elapsed:.2f}s · {r_detail}")
                        if r_ok:
                            wmts_rest_ok = True
                            break
                    if wmts_rest_ok:
                        continue
                if layer in TMS_FALLBACK_LAYERS:
                    wmts_ok = False
                    for wmts_url in WMTS_UPSTREAMS:
                        for matrix in ("EPSG:900913:13", "13"):
                            w_status, w_ct, w_size, w_elapsed, w_detail = probe(client, wmts_url, wmts_params(layer, 13, tile_x, tile_y, matrix))
                            w_ok = w_status == 200 and w_ct.lower().startswith("image/") and w_size > 100
                            print(f"GWC WMTS FALLBACK {'PASS' if w_ok else 'FAIL'} · {layer} · upstream={wmts_url} · matrix={matrix} · HTTP={w_status} · CT={w_ct or '-'} · bytes={w_size} · {w_elapsed:.2f}s · {w_detail}")
                            if w_ok:
                                wmts_ok = True
                                break
                        if wmts_ok:
                            break
                    if wmts_ok:
                        continue
                if layer in TMS_FALLBACK_LAYERS:
                    t_ok = False
                    for t_url in tms_urls(layer, 13, tile_x, tile_y):
                        t_status, t_ct, t_size, t_elapsed, t_detail = probe(client, t_url, {})
                        one_ok = t_status == 200 and t_ct.lower().startswith("image/") and t_size > 100
                        print(f"GWC TMS FALLBACK {'PASS' if one_ok else 'FAIL'} · {layer} · upstream={t_url} · HTTP={t_status} · CT={t_ct or '-'} · bytes={t_size} · {t_elapsed:.2f}s · {t_detail}")
                        if one_ok:
                            t_ok = True
                            break
                    if t_ok:
                        continue
                if layer in TMS_FALLBACK_LAYERS:
                    o_status, o_ct, o_size, o_elapsed, o_detail = probe(client, UPSTREAM, gridset_wms_params(base, layer))
                    o_ok = o_status == 200 and o_ct.lower().startswith("image/") and o_size > 100
                    print(f"GWC GRIDSET-ORIGIN FALLBACK {'PASS' if o_ok else 'FAIL'} · {layer} · HTTP={o_status} · CT={o_ct or '-'} · bytes={o_size} · {o_elapsed:.2f}s · {o_detail}")
                    if o_ok:
                        continue
                fallback = ARCGIS_FALLBACKS.get(layer)
                if fallback:
                    fallback_url, layer_id = fallback
                    f_status, f_ct, f_size, f_elapsed, f_detail = probe(client, fallback_url + "/export", arcgis_params(base, layer_id))
                    f_ok = f_status == 200 and f_ct.lower().startswith("image/") and f_size > 100
                    print(f"ARCGIS FALLBACK {'PASS' if f_ok else 'FAIL'} · {layer} · HTTP={f_status} · CT={f_ct or '-'} · bytes={f_size} · {f_elapsed:.2f}s · {f_detail}")
                    if f_ok:
                        continue
                root_ok = False
                for root_url in ROOT_WMS_UPSTREAMS:
                    r_status, r_ct, r_size, r_elapsed, r_detail = probe(client, root_url, untiled_wms_params(base, layer))
                    one_ok = r_status == 200 and r_ct.lower().startswith("image/") and r_size > 100
                    print(f"ROOT WMS FALLBACK {'PASS' if one_ok else 'FAIL'} · {layer} · upstream={root_url} · HTTP={r_status} · CT={r_ct or '-'} · bytes={r_size} · {r_elapsed:.2f}s · {r_detail}")
                    if one_ok:
                        root_ok = True
                        break
                if root_ok:
                    continue
                u_status, u_ct, u_size, u_elapsed, u_detail = probe(client, UPSTREAM, untiled_wms_params(base, layer))
                u_ok = u_status == 200 and u_ct.lower().startswith("image/") and u_size > 100
                print(f"UNTILED WMS FALLBACK {'PASS' if u_ok else 'FAIL'} · {layer} · HTTP={u_status} · CT={u_ct or '-'} · bytes={u_size} · {u_elapsed:.2f}s · {u_detail}")
                if u_ok:
                    continue
                if layer in DIRECT_WMS_FALLBACKS:
                    d_status, d_ct, d_size, d_elapsed, d_detail = probe(client, DIRECT_WMS, direct_wms_params(base, layer))
                    d_ok = d_status == 200 and d_ct.lower().startswith("image/") and d_size > 100
                    print(f"DIRECT WMS FALLBACK {'PASS' if d_ok else 'FAIL'} · {layer} · HTTP={d_status} · CT={d_ct or '-'} · bytes={d_size} · {d_elapsed:.2f}s · {d_detail}")
                    if d_ok:
                        continue
                failures.append(f"UPSTREAM {layer}: GWC HTTP={status} CT={ct or '-'} bytes={size} detail={detail}")
        print(f"GIS PROXY PREFLIGHT · {BASE_URL}/map/wms")
        for layer in target_layers:
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
