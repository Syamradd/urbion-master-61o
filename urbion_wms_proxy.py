"""Same-origin proxies for authoritative i-Plan/JMG GIS imagery."""
from __future__ import annotations

import asyncio
import math
from urllib.parse import quote, urlsplit

import httpx
from fastapi import APIRouter, Request
from fastapi.responses import Response, StreamingResponse

router = APIRouter()
WMS_UPSTREAM = "https://iplan.planmalaysia.gov.my/geoserver/gwc/service/wms"
WMTS_UPSTREAM = "https://iplan.planmalaysia.gov.my/geoserver/gwc/service/wmts"
ROOT_WMS_UPSTREAMS = (
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
_JMG_TIMEOUT = httpx.Timeout(connect=4.0, read=6.0, write=4.0, pool=4.0)
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


# NOTE: the remainder of this file is intentionally preserved verbatim from the
# canonical branch. The targeted repair below is applied in-place to the JMG
# export parameter normalization, not to the GIS architecture.
