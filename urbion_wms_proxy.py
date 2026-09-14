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
WMS_UPSTREAM = "https://iplan.planmalaysia.gov.my/geoserver/iplan/wms"
ARCGIS_ALLOWLIST = (
    ("scharms.planmalaysia.gov.my", "/arcgis/rest/services/iPLAN/"),
    ("mygems.jmg.gov.my", "/server/rest/services/"),
)
ALLOWED_WMS_PARAMS = {
    "service", "request", "layers", "styles", "format", "transparent",
    "version", "tiled", "width", "height", "srs", "bbox", "crs",
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
_TIMEOUT = httpx.Timeout(connect=5.0, read=8.0, write=5.0, pool=5.0)
_CLIENT = httpx.AsyncClient(follow_redirects=True, timeout=_TIMEOUT, headers=HEADERS, limits=_LIMITS)
_UPSTREAM_SEMAPHORE = asyncio.Semaphore(6)


async def _client_get(url: str, params: dict[str, str]) -> httpx.Response:
    async with _UPSTREAM_SEMAPHORE:
        return await _CLIENT.get(url, params=params)


def _cache_headers() -> dict[str, str]:
    return {"Cache-Control": "public, max-age=60, stale-while-revalidate=30"}


def _proxy_failure(prefix: str, detail: str) -> Response:
    return Response(f"{prefix}: {detail}", status_code=502, media_type="text/plain")


@router.get("/map/wms", include_in_schema=False)
async def map_wms_proxy(request: Request) -> Response:
    params = {
        key: value
        for key, value in request.query_params.multi_items()
        if key.lower() in ALLOWED_WMS_PARAMS
    }
    layers = str(params.get("layers", ""))
    if not layers.startswith("iplan:"):
        return Response(
            "WMS layer is not in the allow-listed i-Plan workspace namespace.",
            status_code=400,
            media_type="text/plain",
        )
    if str(params.get("request", "GetMap")).upper() != "GETMAP":
        return Response(
            "Only WMS GetMap requests are exposed by this proxy.",
            status_code=400,
            media_type="text/plain",
        )
    params.setdefault("service", "WMS")
    params.setdefault("request", "GetMap")
    params.setdefault("format", "image/png")
    params.setdefault("transparent", "true")
    try:
        upstream = await _client_get(WMS_UPSTREAM, params)
    except (httpx.HTTPError, asyncio.TimeoutError) as exc:
        return _proxy_failure("i-Plan WMS upstream unavailable", str(exc))
    if upstream.status_code != 200:
        return _proxy_failure("i-Plan WMS upstream returned HTTP", str(upstream.status_code))
    content_type = upstream.headers.get("content-type", "image/png")
    if not content_type.lower().startswith("image/"):
        return _proxy_failure("i-Plan WMS upstream did not return an image", content_type)
    return Response(
        upstream.content,
        status_code=200,
        media_type=content_type.split(";", 1)[0].strip() or "image/png",
        headers=_cache_headers(),
    )


@router.get("/map/arcgis", include_in_schema=False)
async def map_arcgis_proxy(request: Request) -> Response:
    raw_service = str(request.query_params.get("service", "")).strip()
    parsed = urlsplit(raw_service)
    if parsed.scheme.lower() != "https" or not parsed.hostname:
        return Response("ArcGIS service URL must be HTTPS.", status_code=400, media_type="text/plain")

    match = next(
        (
            (host, prefix)
            for host, prefix in ARCGIS_ALLOWLIST
            if parsed.hostname.lower() == host and parsed.path.startswith(prefix)
        ),
        None,
    )
    if not match or not parsed.path.endswith("/MapServer"):
        return Response(
            "ArcGIS service is outside the allow-listed authoritative GIS namespace.",
            status_code=400,
            media_type="text/plain",
        )

    params: dict[str, str] = {}
    for key, value in request.query_params.multi_items():
        canonical = ARCGIS_PARAM_NAMES.get(key.lower())
        if canonical and key.lower() != "service":
            params[canonical] = value
    params.setdefault("f", "image")
    params.setdefault("format", "png32")
    params.setdefault("transparent", "true")
    export_url = f"https://{match[0]}{parsed.path.rstrip('/')}/export"

    try:
        upstream = await _client_get(export_url, params)
    except (httpx.HTTPError, asyncio.TimeoutError) as exc:
        return _proxy_failure("Authoritative ArcGIS upstream unavailable", str(exc))
    if upstream.status_code != 200:
        return _proxy_failure("Authoritative ArcGIS upstream returned HTTP", str(upstream.status_code))
    content_type = upstream.headers.get("content-type", "image/png")
    if not content_type.lower().startswith("image/"):
        return _proxy_failure("Authoritative ArcGIS upstream did not return an image", content_type)
    return Response(
        upstream.content,
        status_code=200,
        media_type=content_type.split(";", 1)[0].strip() or "image/png",
        headers=_cache_headers(),
    )
