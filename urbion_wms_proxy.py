"""Same-origin proxies for authoritative i-Plan GIS imagery.

The public workspace renders these images inside the browser. Keeping the
imagery same-origin avoids browser cross-origin response blocking while the
upstream domains and service paths remain tightly allow-listed.
"""
from __future__ import annotations

import httpx
from fastapi import APIRouter, Request
from fastapi.responses import Response

router = APIRouter()
WMS_UPSTREAM = "https://iplan.planmalaysia.gov.my/geoserver/iplan/wms"
ARCGIS_HOST = "scharms.planmalaysia.gov.my"
ARCGIS_PREFIX = "/arcgis/rest/services/iPLAN/"
ALLOWED_WMS_PARAMS = {
    "service", "request", "layers", "styles", "format", "transparent",
    "version", "tiled", "width", "height", "srs", "bbox", "crs",
    "bgcolor", "exceptions", "time", "elevation",
}
ALLOWED_ARCGIS_PARAMS = {
    "bbox", "bboxsr", "imagesr", "size", "imagedisplay", "dpi",
    "format", "transparent", "f", "layers", "layerdefs", "dynamiclayers",
}


def _client_get(url: str, params: dict[str, str]) -> httpx.Response:
    with httpx.Client(follow_redirects=True, timeout=20.0) as client:
        return client.get(url, params=params)


@router.get("/map/wms", include_in_schema=False)
def map_wms_proxy(request: Request) -> Response:
    params = {
        key: value
        for key, value in request.query_params.multi_items()
        if key.lower() in ALLOWED_WMS_PARAMS
    }
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
    service = str(request.query_params.get("service", ""))
    if not service.startswith(ARCGIS_PREFIX) or not service.endswith("/MapServer"):
        return Response("ArcGIS service is outside the allow-listed i-Plan workspace namespace.", status_code=400, media_type="text/plain")

    params = {
        key: value
        for key, value in request.query_params.multi_items()
        if key.lower() in ALLOWED_ARCGIS_PARAMS
    }
    params.setdefault("f", "image")
    params.setdefault("format", "png32")
    params.setdefault("transparent", "true")

    upstream_url = f"https://{ARCGIS_HOST}{ARCGIS_PREFIX}{service[len(ARCGIS_PREFIX):]}"
    if not upstream_url.endswith("/MapServer"):
        return Response("Invalid i-Plan ArcGIS service path.", status_code=400, media_type="text/plain")
    export_url = upstream_url + "/export"

    try:
        upstream = _client_get(export_url, params)
    except httpx.HTTPError as exc:
        return Response(f"i-Plan ArcGIS upstream unavailable: {exc}", status_code=502, media_type="text/plain")

    if upstream.status_code != 200:
        return Response(f"i-Plan ArcGIS upstream returned HTTP {upstream.status_code}.", status_code=502, media_type="text/plain")
    content_type = upstream.headers.get("content-type", "image/png")
    if not content_type.lower().startswith("image/"):
        return Response("i-Plan ArcGIS upstream did not return an image tile.", status_code=502, media_type="text/plain")
    return Response(upstream.content, status_code=200, media_type=content_type.split(";", 1)[0].strip() or "image/png", headers={"Cache-Control": "no-store, max-age=0"})
