"""FastAPI routes for live public GIS site-context screening."""
from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException

from server import app
from urbion_spatial_context import build_site_context, clear_spatial_context_cache

router = APIRouter(tags=["spatial-context"])

# Keep the initial analysis context bounded. The UI can still request the full
# layer catalogue explicitly, while the judge journey gets a deterministic
# first-pass context instead of waiting on every external GIS source.
INITIAL_ANALYSIS_LAYERS = (
    "iplan-current",
    "iplan-zoning",
    "iplan-committed",
    "iplan-rfn",
    "iplan-flood",
    "iplan-disaster-risk",
    "iplan-ksas",
    "iplan-heritage",
    "iplan-topography",
)


def _payload_site(payload: dict) -> tuple[float, float]:
    try:
        return float(payload["site_lat"]), float(payload["site_lon"])
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail={"code": "INVALID_SPATIAL_INPUT", "message": "site_lat and site_lon are required numeric coordinates."}) from exc


@router.post("/spatial/site-context")
def spatial_site_context(payload: dict = Body(default_factory=dict)):
    lat, lon = _payload_site(payload)
    try:
        requested_layers = payload.get("layer_ids")
        layer_ids = requested_layers if requested_layers else INITIAL_ANALYSIS_LAYERS
        return build_site_context(
            lat,
            lon,
            payload.get("radius_m", 800),
            payload.get("state") or "Melaka",
            layer_ids,
        )
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail={"code": "INVALID_SPATIAL_INPUT", "message": str(exc)}) from exc


@router.get("/spatial/site-context")
def spatial_site_context_get(site_lat: float, site_lon: float, radius_m: float = 800, state: str = "Melaka", layers: str = ""):
    layer_ids = tuple(x.strip() for x in layers.split(",") if x.strip()) or None
    try:
        return build_site_context(site_lat, site_lon, radius_m, state, layer_ids)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail={"code": "INVALID_SPATIAL_INPUT", "message": str(exc)}) from exc


@router.post("/spatial/site-context/clear-cache")
def spatial_site_context_clear_cache():
    clear_spatial_context_cache()
    return {"cleared": True, "evidence": "SYSTEM_OPERATION"}


app.include_router(router)
