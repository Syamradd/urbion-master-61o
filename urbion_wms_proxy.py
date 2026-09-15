"""Same-origin proxies for authoritative i-Plan/JMG GIS imagery.

Browser-facing imagery stays same-origin while upstream GIS hosts and service
prefixes remain tightly allow-listed. Query parameters are normalized to the
upstream APIs' canonical names before forwarding. Upstream requests are async
and concurrency-bounded so aborted map tiles cannot starve the planning APIs.
"""
from __future__ import annotations

import asyncio
from urllib.parse import urlsplit

import httpx
from fastapi import APIRouter, Request
from fastapi.responses import Response

router = APIRouter()
WMS_UPSTREAM = "https://iplan.planmalaysia.gov.my/geoserver/gwc/service/wms"
DIRECT_WMS_UPSTREAM = "https://iplan.planmalaysia.gov.my/geoserver/iplan/wms"
ARCGIS_ALLOWLIST = (
    ("scharms.planmalaysia.gov.my", "/arcgis/rest/services/"),
    ("mygems.jmg.gov.my", "/server/rest/services/"),
)
WMS_ARCGIS_FALLBACKS = {
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
# These layers exist in the authoritative i-Plan GeoServer namespace but do
# not currently have a verified public ArcGIS equivalent. Try the official
# non-GWC WMS before reporting the layer unavailable; never substitute data.
DIRECT_WMS_FALLBACKS = {
    "iplan:gunatanah_komited_04",
    "iplan:rsn",
    "iplan:banjir",
    "iplan:warisan",
    "iplan:rumah_mampu_milik",
    "iplan:topo",
}
# JMG MapServer services expose multiple child layers. Rendering the exact
# canonical layer instead of relying on service defaults materially reduces
# export work and prevents unrelated child layers from blocking a tile.
JMG_DEFAULT_LAYERS = {
    "/server/rest/services/GeologiAsas/Major_Fault/MapServer": "show:5",
    "/server/rest/services/LombongKuari/Lombong_Kuari_Awam/MapServer": "show:0",
    "/server/rest/services/Air_Bawah_Tanah/Air_Bawah_Tanah_Awam/MapServer": "show:0",
    "/server/rest/services/Demarcation/Litology_by_Negeri/MapServer": "show:22",
}
ALLOWED_WMS_PARAMS = {
    "service", "request", "layers", "styles", "format", "transparent",
    "version", "tiled", "tilesorigin", "width", "height", "srs", "bbox", "crs",
    "bgcolor", "exceptions", "time", "elevation",
}
ARCGIS_PARAM_NAMES = {
    "bbox": "bbox", "bboxsr": "bboxSR", "imagesr": "imageSR", "size": "size",
    "imagedisplay": "imageDisplay", "dpi": "dpi", "format": "format",
    "transparent": "transparent", "f": "f", "layers": "layers",
    "layerdefs": "layerDefs", "dynamiclayers": "dynamicLayers",
}
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/151 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Referer": "https://www.planmalaysia.gov.my/",
}
_LIMITS = httpx.Limits(max_connections=8, max_keepalive_connections=4)
_JMG_LIMITS = httpx.Limits(max_connections=4, max_keepalive_connections=0)
_TIMEOUT = httpx.Timeout(connect=10.0, read=25.0, write=10.0, pool=10.0)
_CLIENT = httpx.AsyncClient(follow_redirects=True, timeout=_TIMEOUT, headers=HEADERS, limits=_LIMITS)
_JMG_CLIENT = httpx.AsyncClient(
    follow_redirects=True,
    timeout=_TIMEOUT,
    headers={**HEADERS, "Connection": "close"},
    limits=_JMG_LIMITS,
)
_UPSTREAM_SEMAPHORE = asyncio.Semaphore(6)


async def _client_get(url: str, params: dict[str, str]) -> httpx.Response:
    async with _UPSTREAM_SEMAPHORE:
        client = _JMG_CLIENT if urlsplit(url).hostname == "mygems.jmg.gov.my" else _CLIENT
        return await client.get(url, params=params)


def _cache_headers() -> dict[str, str]:
    return {"Cache-Control": "public, max-age=60, stale-while-revalidate=30"}


def _proxy_failure(prefix: str, detail: str) -> Response:
    return Response(f"{prefix}: {detail}", status_code=502, media_type="text/plain")


def _arcgis_fallback_params(params: dict[str, str], layer_id: int) -> dict[str, str]:
    spatial_ref = str(params.get("srs") or params.get("crs") or "EPSG:3857").upper()
    wkid = "4326" if spatial_ref.endswith(":4326") else "3857"
    width = str(params.get("width", "256"))
    height = str(params.get("height", "256"))
    return {
        "bbox": str(params.get("bbox", "")), "bboxSR": wkid, "imageSR": wkid,
        "size": f"{width},{height}", "dpi": "96", "format": "png32",
        "transparent": str(params.get("transparent", "true")), "f": "image",
        "layers": f"show:{layer_id}",
    }


async def _arcgis_wms_fallback(layer: str, params: dict[str, str]) -> Response | None:
    target = WMS_ARCGIS_FALLBACKS.get(layer)
    if not target:
        return None
    service_url, layer_id = target
    try:
        upstream = await _client_get(service_url + "/export", _arcgis_fallback_params(params, layer_id))
    except (httpx.HTTPError, asyncio.TimeoutError):
        return None
    if upstream.status_code != 200:
        return None
    content_type = upstream.headers.get("content-type", "image/png")
    if not content_type.lower().startswith("image/"):
        return None
    return Response(
        upstream.content, status_code=200,
        media_type=content_type.split(";", 1)[0].strip() or "image/png",
        headers={**_cache_headers(), "X-URBION-GIS-Fallback": "PLANMalaysia-ArcGIS"},
    )


def _direct_wms_params(params: dict[str, str]) -> dict[str, str]:
    direct = dict(params)
    direct.pop("tiled", None)
    direct.pop("tilesorigin", None)
    direct.setdefault("format", "image/png")
    direct.setdefault("version", "1.1.1")
    direct.setdefault("request", "GetMap")
    direct.setdefault("service", "WMS")
    return direct


async def _direct_wms_fallback(layer: str, params: dict[str, str]) -> Response | None:
    if layer not in DIRECT_WMS_FALLBACKS:
        return None
    try:
        upstream = await _client_get(DIRECT_WMS_UPSTREAM, _direct_wms_params(params))
    except (httpx.HTTPError, asyncio.TimeoutError):
        return None
    if upstream.status_code != 200:
        return None
    content_type = upstream.headers.get("content-type", "image/png")
    if not content_type.lower().startswith("image/"):
        return None
    return Response(
        upstream.content, status_code=200,
        media_type=content_type.split(";", 1)[0].strip() or "image/png",
        headers={**_cache_headers(), "X-URBION-GIS-Fallback": "PLANMalaysia-WMS"},
    )


@router.get("/map/wms", include_in_schema=False)
async def map_wms_proxy(request: Request) -> Response:
    params: dict[str, str] = {}
    for key, value in request.query_params.multi_items():
        canonical = key.lower()
        if canonical in ALLOWED_WMS_PARAMS:
            params[canonical] = value
    layers = str(params.get("layers", ""))
    if not layers.startswith("iplan:"):
        return Response("WMS layer is not in the allow-listed i-Plan workspace namespace.", status_code=400, media_type="text/plain")
    if str(params.get("request", "GetMap")).upper() != "GETMAP":
        return Response("Only WMS GetMap requests are exposed by this proxy.", status_code=400, media_type="text/plain")
    params.setdefault("service", "WMS")
    params.setdefault("request", "GetMap")
    params.setdefault("format", "image/png")
    params.setdefault("transparent", "true")
    params.setdefault("version", "1.1.1")
    try:
        upstream = await _client_get(WMS_UPSTREAM, params)
    except (httpx.HTTPError, asyncio.TimeoutError):
        upstream = None
    if upstream is None or upstream.status_code != 200 or not upstream.headers.get("content-type", "").lower().startswith("image/"):
        fallback = await _arcgis_wms_fallback(layers, params)
        if fallback is not None:
            return fallback
        fallback = await _direct_wms_fallback(layers, params)
        if fallback is not None:
            return fallback
        detail = f"GWC={upstream.status_code if upstream is not None else 'UNAVAILABLE'}"
        if upstream is not None and upstream.headers.get("content-type"):
            detail += f" CT={upstream.headers.get('content-type')}"
        return _proxy_failure("i-Plan WMS authoritative fallbacks unavailable", detail)
    content_type = upstream.headers.get("content-type", "image/png")
    return Response(upstream.content, status_code=200, media_type=content_type.split(";", 1)[0].strip() or "image/png", headers=_cache_headers())


@router.get("/map/arcgis", include_in_schema=False)
async def map_arcgis_proxy(request: Request) -> Response:
    raw_service = str(request.query_params.get("service", "")).strip()
    parsed = urlsplit(raw_service)
    if parsed.scheme.lower() != "https" or not parsed.hostname:
        return Response("ArcGIS service URL must be HTTPS.", status_code=400, media_type="text/plain")
    match = next(((host, prefix) for host, prefix in ARCGIS_ALLOWLIST if parsed.hostname.lower() == host and parsed.path.startswith(prefix)), None)
    if not match or not parsed.path.endswith("/MapServer"):
        return Response("ArcGIS service is outside the allow-listed authoritative GIS namespace.", status_code=400, media_type="text/plain")
    params: dict[str, str] = {}
    for key, value in request.query_params.multi_items():
        canonical = ARCGIS_PARAM_NAMES.get(key.lower())
        if canonical and key.lower() != "service":
            params[canonical] = value
    params.setdefault("f", "image")
    params.setdefault("format", "png32")
    params.setdefault("transparent", "true")
    parsed_path = parsed.path.rstrip("/")
    if parsed.hostname.lower() == "mygems.jmg.gov.my":
        params.setdefault("layers", JMG_DEFAULT_LAYERS.get(parsed_path, ""))
    is_jmg_fault = parsed.hostname.lower() == "mygems.jmg.gov.my" and parsed_path.endswith("/GeologiAsas/Major_Fault/MapServer")
    if is_jmg_fault:
        params["layers"] = "show:5"
    export_url = f"https://{match[0]}{parsed_path}/export"
    attempts = [dict(params)]
    if is_jmg_fault:
        # Major Fault is a single authoritative child layer. Keep one exact
        # export request plus a minimal fallback without explicit layers.
        attempts.append({k: v for k, v in params.items() if k != "layers"})
        attempts.append({k: v for k, v in attempts[-1].items() if k not in {"format", "transparent"}} | {"format": "png", "transparent": "true"})
    last_detail = "no response"
    for attempt in attempts:
        try:
            upstream = await _client_get(export_url, attempt)
        except (httpx.HTTPError, asyncio.TimeoutError) as exc:
            last_detail = str(exc)
            continue
        content_type = upstream.headers.get("content-type", "")
        if upstream.status_code == 200 and content_type.lower().startswith("image/"):
            return Response(upstream.content, status_code=200, media_type=content_type.split(";", 1)[0].strip() or "image/png", headers=_cache_headers())
        body = upstream.text[:240].replace("\n", " ").replace("\r", " ")
        last_detail = f"HTTP={upstream.status_code} CT={content_type or '-'} BODY={body}"
    return _proxy_failure("Authoritative ArcGIS upstream render failed", last_detail)
