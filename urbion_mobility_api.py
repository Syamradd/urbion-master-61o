"""Canonical mobility/station evidence API.

This adapter exposes existing live-station intelligence without turning
observations into statutory planning conclusions.
"""
from __future__ import annotations
from math import isfinite
from fastapi import APIRouter, Query
from urbion_live_stations import build_live_station_snapshot

router = APIRouter(prefix="/mobility", tags=["URBION Mobility"])

@router.get("/stations")
def live_stations(
    site_lat: float = Query(...),
    site_lon: float = Query(...),
    state: str = Query("Melaka"),
    limit: int = Query(5, ge=1, le=10),
):
    if not (isfinite(site_lat) and isfinite(site_lon)):
        return {"status": "INVALID_SPATIAL_INPUT", "statutory_verification": "NOT_CLAIMED"}
    if site_lat == -90.0 and site_lon == -180.0:
        return {"status": "INVALID_SPATIAL_INPUT", "statutory_verification": "NOT_CLAIMED"}
    return build_live_station_snapshot(site_lat, site_lon, state, limit)

__all__ = ["router"]
