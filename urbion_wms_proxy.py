"""Same-origin proxies for authoritative i-Plan/JMG GIS imagery.

Browser-facing imagery stays same-origin while upstream GIS hosts and service
prefixes remain tightly allow-listed. Query parameters are normalized to the
upstream APIs' canonical names before forwarding.
"""
from __future__ import annotations

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


def _headers() -> dict[str, str]:
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/151 Safari/537.36",
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "Referer": "https://www.planmalaysia.gov.my/",
    }


def _client_get(url: str, params: dict[str, str]) -> httpx.Response:
    with httpx.Client(follow_redirects=True, timeout=30.0, headers=_headers()) as client:
        return client.get(url, params=params)


@router.get("/map/wms", include_in_schema=False)
def map_wms_proxy(request: Request) -> Response:
    params = {key: value for key, value in request.query_params.multi_items() if key.lower() in ALLOWED_WMS_PARAMS}
    layers = str(params.get("layers", ""))
    if not layers.startswith("iplan:"):
        return Response("WMS layer is not in the allow-listed i-Plan workspace namespace.", status_code=400, media_type="text/plain")
    if str(params.get("request", "GetMap")).upper() != "GETMAP":
        return Response("Only WMS GetMap requests are exposed by this proxy.", status_code=400, media_type="text/plain")
    params.setdefault("service", "WMS")
    params.setdefault("request", "GetMap")
    params.setdefault("format", "image/png")
    params.setdefault("transparent", "true")
    try:
        upstream = _client_get(WMS_UPSTREAM, params)
    except httpx.HTTPError as exc:
        return Response(f"i-Plan WMS upstream unavailable: {exc}", status_code=502, media_type="text/plain")
    if upstream.status_code != 200:
        return Response(f"i-Plan WMS upstream returned HTTP {upstream.status_code}.", status_code=502, media_type="text/plain")
    content_type = upstream.headers.get("content-type", "image/png")
    if not content_type.lower().startswith("image/"):
        return Response("i-Plan WMS upstream did not return an image tile.", status_code=502, media_type="text/plain")
    return Response(upstream.content, status_code=200, media_type=content_type.split(";", 1)[0].strip() or "image/png", headers={"Cache-Control": "no-store, max-age=0"})


@router.get("/map/arcgis", include_in_schema=False)
def map_arcgis_proxy(request: Request) -> Response:
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
    export_url = f"https://{match[0]}{parsed.path.rstrip('/')}/export"

    try:
        upstream = _client_get(export_url, params)
    except httpx.HTTPError as exc:
        return Response(f"Authoritative ArcGIS upstream unavailable: {exc}", status_code=502, media_type="text/plain")
    if upstream.status_code != 200:
        return Response(f"Authoritative ArcGIS upstream returned HTTP {upstream.status_code}.", status_code=502, media_type="text/plain")
    content_type = upstream.headers.get("content-type", "image/png")
    if not content_type.lower().startswith("image/"):
        return Response("Authoritative ArcGIS upstream did not return an image tile.", status_code=502, media_type="text/plain")
    return Response(upstream.content, status_code=200, media_type=content_type.split(";", 1)[0].strip() or "image/png", headers={"Cache-Control": "no-store, max-age=0"})
