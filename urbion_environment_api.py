"""Canonical live-environment API surface for URBION HORIZON."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
import math

from urbion_environment_live import build_live_environment_evidence

router = APIRouter(prefix="/environment", tags=["environment"])


@router.get("/live")
def live_environment(
    site_lat: float,
    site_lon: float,
    state: str = "Melaka",
    radius_m: float = 1000,
):
    if not math.isfinite(float(site_lat)) or not math.isfinite(float(site_lon)):
        raise HTTPException(status_code=422, detail={"code": "INVALID_SPATIAL_INPUT", "message": "Coordinates must be finite numeric values."})
    if (float(site_lat), float(site_lon)) == (-90.0, -180.0):
        raise HTTPException(status_code=422, detail={"code": "INVALID_SPATIAL_INPUT", "message": "Placeholder coordinates cannot be used for live environmental screening."})
    if not math.isfinite(float(radius_m)) or radius_m <= 0 or radius_m > 10000:
        raise HTTPException(status_code=422, detail={"code": "INVALID_RADIUS", "message": "radius_m must be greater than 0 and no more than 10000 metres."})
    return build_live_environment_evidence(
        latitude=float(site_lat),
        longitude=float(site_lon),
        state=state,
        radius_m=float(radius_m),
    )


__all__ = ["router"]
