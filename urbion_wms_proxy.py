"""Same-origin proxies for authoritative i-Plan/JMG GIS imagery."""
from __future__ import annotations

import asyncio
import json
import math
from urllib.parse import quote, urlsplit

import httpx
from fastapi import APIRouter, Request
from fastapi.responses import Response, StreamingResponse

router = APIRouter()
WMS_UPSTREAM = "https://iplan.planmalaysia.gov.my/geoserver/gwc/service/wms"
WMTS_UPSTREAMS = (
    "https://iplan.planmalaysia.gov.my/geoserver/gwc/service/wmts",
    "https://iplan.planmalaysia.gov.my/geoserver/service/wmts",
)
WMTS_UPSTREAM = WMTS_UPSTREAMS[0]
ROOT_WMS_UPSTREAMS = (
    "https://iplan.planmalaysia.gov.my/geoserver/service/wms",
    "https://iplan.planmalaysia.gov.my/geoserver/wms",
    "https://iplan.planmalaysia.gov.my/geoserver/ows",
)
DIRECT_WMS_UPSTREAM = "https://iplan.planmalaysia.gov.my/geoserver/iplan/wms"
TMS_UPSTREAMS = (
    "https://iplan.planmalaysia.gov.my/geoserver/gwc/service/tms/1.0.0",
    "https://iplan.planmalaysia.gov.my/geoserver/service/tms/1.0.0",
)
TMS_FALLBACK_LAYERS = {
    "iplan:gunatanah_komited_04", "iplan:rsn", "iplan:warisan",
    "iplan:rumah_mampu_milik", "iplan:topo",
}
WMTS_FALLBACK_LAYERS = set(TMS_FALLBACK_LAYERS)
ARCGIS_ALLOWLIST = (
    ("scharms.planmalaysia.gov.my", "/arcgis/rest/services/"),
    ("mygems.jmg.gov.my", "/server/rest/services/"),
)
WMS_ARCGIS_FALLBACKS = {
    "iplan:gunatanah_semasa_04": ("https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN/GTsemasa_04/MapServer", 0),
    "iplan:gunatanah_zoning_04": ("https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN/GTzoning_04/MapServer", 0),
    "iplan:rfn": ("https://scharms.planmalaysia.gov.my/arcgis/rest/services/DPFDN/AlamSekitar/MapServer", 5),
    "iplan:ksas": ("https://scharms.planmalaysia.gov.my/arcgis/rest/services/DPFDN/AlamSekitar/MapServer", 2),
    "iplan:hakisan_pantai": ("https://scharms.planmalaysia.gov.my/arcgis/rest/services/DPFDN/Bencana/MapServer", 5),
    "iplan:banjir": ("https://scharms.planmalaysia.gov.my/arcgis/rest/services/DPFDN/Bencana/MapServer", 2),
}
DIRECT_WMS_FALLBACKS = {
    "iplan:gunatanah_komited_04", "iplan:rsn", "iplan:banjir", "iplan:warisan",
    "iplan:rumah_mampu_milik", "iplan:topo",
}
ROOT_WMS_FALLBACKS = {
    "iplan:gunatanah_komited_04", "iplan:rsn", "iplan:warisan",
    "iplan:rumah_mampu_milik", "iplan:topo",
}
JMG_DEFAULT_LAYERS = {
    "/server/rest/services/GeologiAsas/Major_Fault/MapServer": "show:5",
    "/server/rest/services/LombongKuari/Lombong_Kuari_Awam/MapServer": "show:0",
    "/server/rest/services/Air_Bawah_Tanah/Air_Bawah_Tanah_Awam/MapServer": "show:0",
    "/server/rest/services/Demarcation/Litology_by_Negeri/MapServer": "show:22",
}
JMG_FEATURE_FALLBACKS = {
    "/server/rest/services/GeologiAsas/Major_Fault/MapServer": ("/server/rest/services/GeologiAsas/Major_Fault/FeatureServer", 5),
    "/server/rest/services/LombongKuari/Lombong_Kuari_Awam/MapServer": ("/server/rest/services/LombongKuari/Lombong_Kuari_Awam/FeatureServer", 0),
}
ALLOWED_WMS_PARAMS = {
    "service", "request", "layers", "styles", "format", "transparent", "version", "tiled",
    "tilesorigin", "width", "height", "srs", "bbox", "crs", "bgcolor", "exceptions", "time", "elevation",
}
ARCGIS_PARAM_NAMES = {
    "bbox": "bbox", "bboxsr": "bboxSR", "imagesr": "imageSR", "size": "size", "imagedisplay": "imageDisplay",
    "dpi": "dpi", "format": "format", "transparent": "transparent", "f": "f", "layers": "layers",
    "layerdefs": "layerDefs", "dynamiclayers": "dynamicLayers",
}
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/151 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Referer": "https://www.planmalaysia.gov.my/",
    "Connection": "close",
}
_LIMITS = httpx.Limits(max_connections=8, max_keepalive_connections=4)
_JMG_LIMITS = httpx.Limits(max_connections=4, max_keepalive_connections=0)
_TIMEOUT = httpx.Timeout(connect=6.0, read=12.0, write=6.0, pool=6.0)
_JMG_TIMEOUT = httpx.Timeout(connect=4.0, read=15.0, write=4.0, pool=4.0)
_CLIENT = httpx.AsyncClient(follow_redirects=True, timeout=_TIMEOUT, headers=HEADERS, limits=_LIMITS)
_JMG_CLIENT = httpx.AsyncClient(follow_redirects=True, timeout=_JMG_TIMEOUT, headers=HEADERS, limits=_JMG_LIMITS)
_UPSTREAM_SEMAPHORE = asyncio.Semaphore(6)


async def _client_get(url: str, params: dict[str, str]) -> httpx.Response:
    async with _UPSTREAM_SEMAPHORE:
        client = _JMG_CLIENT if urlsplit(url).hostname == "mygems.jmg.gov.my" else _CLIENT
        return await client.get(url, params=params)


def _cache_headers() -> dict[str, str]:
    return {"Cache-Control": "public, max-age=60, stale-while-revalidate=30"}


def _proxy_failure(prefix: str, detail: str) -> StreamingResponse:
    body = f"{prefix}: {detail}".encode("utf-8")
    return StreamingResponse(iter([body]), status_code=502, media_type="text/plain")


def _arcgis_fallback_params(params: dict[str, str], layer_id: int) -> dict[str, str]:
    spatial_ref = str(params.get("srs") or params.get("crs") or params.get("bboxSR") or "EPSG:3857").upper()
    wkid = "4326" if spatial_ref.endswith(":4326") else "3857"
    width = str(params.get("width", "256")); height = str(params.get("height", "256"))
    return {
        "bbox": str(params.get("bbox", "")), "bboxSR": wkid, "imageSR": wkid,
        "size": f"{width},{height}", "dpi": "96", "format": "png32",
        "transparent": str(params.get("transparent", "true")), "f": "image", "layers": f"show:{layer_id}",
    }


async def _arcgis_wms_fallback(layer: str, params: dict[str, str]) -> Response | None:
    target = WMS_ARCGIS_FALLBACKS.get(layer)
    if not target: return None
    service_url, layer_id = target
    try: upstream = await _client_get(service_url + "/export", _arcgis_fallback_params(params, layer_id))
    except (httpx.HTTPError, asyncio.TimeoutError): return None
    if upstream.status_code != 200: return None
    content_type = upstream.headers.get("content-type", "image/png")
    if not content_type.lower().startswith("image/"): return None
    return Response(upstream.content, status_code=200, media_type=content_type.split(";", 1)[0].strip() or "image/png", headers={**_cache_headers(), "X-URBION-GIS-Fallback": "PLANMalaysia-ArcGIS"})


def _untiled_wms_params(params: dict[str, str]) -> dict[str, str]:
    untiled = dict(params); untiled.pop("tiled", None); untiled.pop("tilesorigin", None)
    untiled.setdefault("format", "image/png"); untiled.setdefault("version", "1.1.1"); untiled.setdefault("request", "GetMap"); untiled.setdefault("service", "WMS")
    return untiled


async def _untiled_wms_fallback(layer: str, params: dict[str, str]) -> Response | None:
    try: upstream = await _client_get(WMS_UPSTREAM, _untiled_wms_params(params))
    except (httpx.HTTPError, asyncio.TimeoutError): return None
    if upstream.status_code != 200: return None
    content_type = upstream.headers.get("content-type", "")
    if not content_type.lower().startswith("image/"): return None
    return Response(upstream.content, status_code=200, media_type=content_type.split(";", 1)[0].strip() or "image/png", headers={**_cache_headers(), "X-URBION-GIS-Fallback": "PLANMalaysia-WMS-UNTILED"})


def _direct_wms_params(params: dict[str, str]) -> dict[str, str]:
    direct = dict(params); direct.pop("tiled", None); direct.pop("tilesorigin", None)
    direct.setdefault("format", "image/png"); direct.setdefault("version", "1.1.1"); direct.setdefault("request", "GetMap"); direct.setdefault("service", "WMS")
    return direct


async def _direct_wms_fallback(layer: str, params: dict[str, str]) -> Response | None:
    if layer not in DIRECT_WMS_FALLBACKS: return None
    try: upstream = await _client_get(DIRECT_WMS_UPSTREAM, _direct_wms_params(params))
    except (httpx.HTTPError, asyncio.TimeoutError): return None
    if upstream.status_code != 200: return None
    content_type = upstream.headers.get("content-type", "image/png")
    if not content_type.lower().startswith("image/"): return None
    return Response(upstream.content, status_code=200, media_type=content_type.split(";", 1)[0].strip() or "image/png", headers={**_cache_headers(), "X-URBION-GIS-Fallback": "PLANMalaysia-WMS"})


async def _root_wms_fallback(layer: str, params: dict[str, str]) -> Response | None:
    if layer not in ROOT_WMS_FALLBACKS: return None
    root_params = _direct_wms_params(params)
    for upstream_url in ROOT_WMS_UPSTREAMS:
        try: upstream = await _client_get(upstream_url, root_params)
        except (httpx.HTTPError, asyncio.TimeoutError): continue
        if upstream.status_code != 200: continue
        content_type = upstream.headers.get("content-type", "")
        if not content_type.lower().startswith("image/"): continue
        return Response(upstream.content, status_code=200, media_type=content_type.split(";", 1)[0].strip() or "image/png", headers={**_cache_headers(), "X-URBION-GIS-Fallback": "PLANMalaysia-WMS-ROOT"})
    return None


def _wmts_xyz(params: dict[str, str]) -> tuple[int, int, int] | None:
    bbox_raw = str(params.get("bbox", ""))
    try:
        xmin, ymin, xmax, ymax = (float(v) for v in bbox_raw.split(",")); width = int(params.get("width", "256")); height = int(params.get("height", "256"))
    except (TypeError, ValueError): return None
    if width != 256 or height != 256 or xmax <= xmin or ymax <= ymin: return None
    world = 20037508.342789244; resolution = (xmax - xmin) / 256.0
    if resolution <= 0: return None
    z_float = math.log2((world * 2.0) / (256.0 * resolution)); z = int(round(z_float))
    if z < 0 or z > 20 or abs(z_float - z) > 0.02: return None
    tile_span = (world * 2.0) / (2 ** z)
    x = int(math.floor((xmin + world) / tile_span + 1e-9)); y = int(math.floor((world - ymax) / tile_span + 1e-9))
    return z, x, y


async def _tms_tile_fallback(layer: str, params: dict[str, str]) -> Response | None:
    """Use GWC's authoritative TMS tile endpoint for layers whose WMS path is broken."""
    if layer not in TMS_FALLBACK_LAYERS:
        return None
    xyz = _wmts_xyz(params)
    if xyz is None:
        return None
    z, x, y_xyz = xyz
    y_tms = (2 ** z - 1) - y_xyz
    encoded_layer = quote(layer, safe=":")
    for base in TMS_UPSTREAMS:
        for gridset in ("EPSG:900913", "EPSG:4326"):
            for ext in ("png", "jpeg"):
                url = f"{base}/{encoded_layer}@{gridset}@{ext}/{z}/{x}/{y_tms}.{ext}"
                try:
                    upstream = await _client_get(url, {})
                except (httpx.HTTPError, asyncio.TimeoutError):
                    continue
                if upstream.status_code != 200:
                    continue
                content_type = upstream.headers.get("content-type", "")
                if not content_type.lower().startswith("image/"):
                    continue
                return Response(upstream.content, status_code=200, media_type=content_type.split(";", 1)[0].strip() or f"image/{ext}", headers={**_cache_headers(), "X-URBION-GIS-Fallback": "PLANMalaysia-GWC-TMS"})
    return None


async def _wmts_get(params: dict[str, str]) -> httpx.Response | None:
    """Try each official WMTS route, accepting only actual image tiles."""
    for url in WMTS_UPSTREAMS:
        try:
            upstream = await _client_get(url, params)
        except (httpx.HTTPError, asyncio.TimeoutError):
            continue
        content_type = upstream.headers.get("content-type", "")
        if upstream.status_code == 200 and content_type.lower().startswith("image/") and len(upstream.content) > 100:
            return upstream
    return None


async def _wmts_kvp_fallback(layer: str, params: dict[str, str]) -> Response | None:
    if layer not in WMTS_FALLBACK_LAYERS:
        return None
    xyz = _wmts_xyz(params)
    if xyz is None:
        return None
    z, x, y = xyz
    variants = (f"EPSG:900913:{z}", str(z))
    for matrix in variants:
        for style in ("", "default"):
            query = {
                "SERVICE": "WMTS", "REQUEST": "GetTile", "VERSION": "1.0.0", "LAYER": layer,
                "STYLE": style, "FORMAT": "image/png", "TILEMATRIXSET": "EPSG:900913",
                "TILEMATRIX": matrix, "TILEROW": str(y), "TILECOL": str(x),
            }
            try:
                upstream = await _wmts_get(query)
            except (httpx.HTTPError, asyncio.TimeoutError):
                continue
            if upstream is None or upstream.status_code != 200:
                continue
            content_type = upstream.headers.get("content-type", "")
            if not content_type.lower().startswith("image/"): continue
            return Response(upstream.content, status_code=200, media_type=content_type.split(";", 1)[0].strip() or "image/png", headers={**_cache_headers(), "X-URBION-GIS-Fallback": "PLANMalaysia-GWC-WMTS"})
    return None


def _svg_from_arcgis_features(payload: dict, bbox: tuple[float, float, float, float], width: int = 256, height: int = 256) -> str | None:
    xmin, ymin, xmax, ymax = bbox; dx = xmax - xmin; dy = ymax - ymin
    if dx <= 0 or dy <= 0: return None
    features = payload.get("features") or []; parts = []
    def xy(x, y): return (float(x) - xmin) / dx * width, height - (float(y) - ymin) / dy * height
    for feature in features[:500]:
        geom = feature.get("geometry") if isinstance(feature, dict) else None
        if not isinstance(geom, dict): continue
        if isinstance(geom.get("paths"), list):
            for path in geom["paths"]:
                coords = [xy(*pt[:2]) for pt in path if isinstance(pt, (list, tuple)) and len(pt) >= 2]
                if len(coords) >= 2:
                    d = "M " + " L ".join(f"{px:.2f},{py:.2f}" for px, py in coords)
                    parts.append(f'<path d="{d}" fill="none" stroke="#1de0ff" stroke-width="2.2" vector-effect="non-scaling-stroke"/>')
        elif isinstance(geom.get("rings"), list):
            for ring in geom["rings"]:
                coords = [xy(*pt[:2]) for pt in ring if isinstance(pt, (list, tuple)) and len(pt) >= 2]
                if len(coords) >= 3:
                    d = "M " + " L ".join(f"{px:.2f},{py:.2f}" for px, py in coords) + " Z"
                    parts.append(f'<path d="{d}" fill="rgba(29,224,255,0.16)" stroke="#1de0ff" stroke-width="1.2" vector-effect="non-scaling-stroke"/>')
        elif geom.get("x") is not None and geom.get("y") is not None:
            px, py = xy(geom["x"], geom["y"]); parts.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="3" fill="#1de0ff" stroke="#06212b" stroke-width="1"/>')
    if not parts: return None
    return '<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">' + "".join(parts) + '</svg>'


async def _jmg_feature_image_fallback(parsed_path: str, params: dict[str, str]) -> Response | None:
    target = JMG_FEATURE_FALLBACKS.get(parsed_path)
    if not target:
        return None
    feature_path, layer_id = target
    bbox_raw = str(params.get("bbox", ""))
    try:
        bbox = tuple(float(x) for x in bbox_raw.split(","))
        if len(bbox) != 4:
            return None
    except (TypeError, ValueError):
        return None

    base_query = {
        "where": "1=1", "outFields": "OBJECTID,Line_code,Type,Name",
        "returnGeometry": "true", "outSR": "3857", "resultRecordCount": "500", "f": "json",
    }
    queries = [
        (
            f"https://mygems.jmg.gov.my{feature_path}/{layer_id}/query",
            {
                **base_query,
                "geometry": bbox_raw,
                "geometryType": "esriGeometryEnvelope",
                "inSR": "3857",
                "spatialRel": "esriSpatialRelIntersects",
                "resultType": "tile",
                "returnExceededLimitFeatures": "true",
            },
        ),
        (
            f"https://mygems.jmg.gov.my{parsed_path}/{layer_id}/query",
            base_query,
        ),
    ]
    for query_url, query in queries:
        try:
            upstream = await _client_get(query_url, query)
        except (httpx.HTTPError, asyncio.TimeoutError):
            continue
        if upstream.status_code != 200:
            continue
        content_type = upstream.headers.get("content-type", "")
        if "json" not in content_type.lower():
            continue
        try:
            payload = upstream.json()
        except ValueError:
            continue
        if isinstance(payload, dict) and payload.get("error"):
            continue
        svg = _svg_from_arcgis_features(payload, bbox)
        if not svg:
            svg = '<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"></svg>'
        return Response(
            svg.encode("utf-8"), status_code=200, media_type="image/svg+xml",
            headers={**_cache_headers(), "X-URBION-GIS-Fallback": "JMG-FeatureServer"},
        )
    return None


@router.get("/map/wms", include_in_schema=False)
async def map_wms_proxy(request: Request) -> Response:
    params = {key.lower(): value for key, value in request.query_params.multi_items() if key.lower() in ALLOWED_WMS_PARAMS}
    layers = str(params.get("layers", ""))
    if not layers.startswith("iplan:"):
        return Response("WMS layer is not in the allow-listed i-Plan workspace namespace.", status_code=400, media_type="text/plain")
    if str(params.get("request", "GetMap")).upper() != "GETMAP":
        return Response("Only WMS GetMap requests are exposed by this proxy.", status_code=400, media_type="text/plain")
    params.setdefault("service", "WMS"); params.setdefault("request", "GetMap"); params.setdefault("format", "image/png"); params.setdefault("transparent", "true"); params.setdefault("version", "1.1.1")
    try: upstream = await _client_get(WMS_UPSTREAM, params)
    except (httpx.HTTPError, asyncio.TimeoutError): upstream = None
    if upstream is not None:
        content_type = upstream.headers.get("content-type", "")
        if upstream.status_code == 200 and content_type.lower().startswith("image/"):
            return Response(upstream.content, status_code=200, media_type=content_type.split(";", 1)[0].strip() or "image/png", headers=_cache_headers())
    fallback = await _tms_tile_fallback(layers, params)
    if fallback is not None: return fallback
    fallback = await _wmts_kvp_fallback(layers, params)
    if fallback is not None: return fallback
    fallback = await _arcgis_wms_fallback(layers, params)
    if fallback is not None: return fallback
    fallback = await _root_wms_fallback(layers, params)
    if fallback is not None: return fallback
    fallback = await _untiled_wms_fallback(layers, params)
    if fallback is not None: return fallback
    fallback = await _direct_wms_fallback(layers, params)
    if fallback is not None: return fallback
    detail = f"GWC={upstream.status_code if upstream is not None else 'UNAVAILABLE'}"
    if upstream is not None and upstream.headers.get("content-type"): detail += f" CT={upstream.headers.get('content-type')}"
    return _proxy_failure("i-Plan WMS authoritative fallbacks unavailable", detail)


@router.get("/map/arcgis", include_in_schema=False)
async def map_arcgis_proxy(request: Request) -> Response:
    raw_service = str(request.query_params.get("service", "")).strip(); parsed = urlsplit(raw_service)
    if parsed.scheme.lower() != "https" or not parsed.hostname: return Response("ArcGIS service URL must be HTTPS.", status_code=400, media_type="text/plain")
    match = next(((host, prefix) for host, prefix in ARCGIS_ALLOWLIST if parsed.hostname.lower() == host and parsed.path.startswith(prefix)), None)
    if not match or not parsed.path.endswith("/MapServer"): return Response("ArcGIS service is outside the allow-listed authoritative GIS namespace.", status_code=400, media_type="text/plain")
    params: dict[str, str] = {}
    for key, value in request.query_params.multi_items():
        canonical = ARCGIS_PARAM_NAMES.get(key.lower())
        if canonical and key.lower() != "service": params[canonical] = value
    params.setdefault("f", "image"); params.setdefault("format", "png32"); params.setdefault("transparent", "true")
    parsed_path = parsed.path.rstrip("/"); is_jmg = parsed.hostname.lower() == "mygems.jmg.gov.my"
    if is_jmg: params.setdefault("layers", JMG_DEFAULT_LAYERS.get(parsed_path, ""))
    if is_jmg and parsed_path.endswith("/GeologiAsas/Major_Fault/MapServer"): params["layers"] = "show:5"
    export_url = f"https://{match[0]}{parsed_path}/export"; last_detail = "no response"
    try:
        upstream = await _client_get(export_url, dict(params))
    except (httpx.HTTPError, asyncio.TimeoutError) as exc:
        upstream = None; last_detail = str(exc)
    if upstream is not None:
        content_type = upstream.headers.get("content-type", "")
        if upstream.status_code == 200 and content_type.lower().startswith("image/"):
            return Response(upstream.content, status_code=200, media_type=content_type.split(";", 1)[0].strip() or "image/png", headers=_cache_headers())
        body = upstream.text[:240].replace("\n", " ").replace("\r", " "); last_detail = f"HTTP={upstream.status_code} CT={content_type or '-'} BODY={body}"
    if is_jmg and parsed_path in JMG_FEATURE_FALLBACKS:
        fallback = await _jmg_feature_image_fallback(parsed_path, params)
        if fallback is not None:
            return fallback
    return _proxy_failure("Authoritative ArcGIS upstream render failed", last_detail)