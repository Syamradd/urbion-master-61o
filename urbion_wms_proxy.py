"""Same-origin proxy for the authoritative i-Plan GeoServer WMS tiles.

The public workspace renders these images inside the browser. Keeping the WMS
request same-origin avoids browser cross-origin response blocking while the
upstream domain remains tightly allow-listed.
"""
from __future__ import annotations

import httpx
from fastapi import APIRouter, Request
from fastapi.responses import Response

router = APIRouter()
UPSTREAM = "https://iplan.planmalaysia.gov.my/geoserver/iplan/wms"
ALLOWED_PARAMS = {
    "service", "request", "layers", "styles", "format", "transparent",
    "version", "tiled", "width", "height", "srs", "bbox", "crs",
    "bgcolor", "exceptions", "time", "elevation",
}


@router.get("/map/wms", include_in_schema=False)
def map_wms_proxy(request: Request) -> Response:
    params = {
        key: value
        for key, value in request.query_params.multi_items()
        if key.lower() in ALLOWED_PARAMS
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
        with httpx.Client(follow_redirects=True, timeout=20.0) as client:
            upstream = client.get(UPSTREAM, params=params)
    except httpx.HTTPError as exc:
        return Response(f"i-Plan WMS upstream unavailable: {exc}", status_code=502, media_type="text/plain")

    if upstream.status_code != 200:
        return Response(
            f"i-Plan WMS upstream returned HTTP {upstream.status_code}.",
            status_code=502,
            media_type="text/plain",
        )

    content_type = upstream.headers.get("content-type", "image/png")
    if not content_type.lower().startswith("image/"):
        return Response("i-Plan WMS upstream did not return an image tile.", status_code=502, media_type="text/plain")

    return Response(
        upstream.content,
        status_code=200,
        media_type=content_type.split(";", 1)[0].strip() or "image/png",
        headers={"Cache-Control": "no-store, max-age=0"},
    )
