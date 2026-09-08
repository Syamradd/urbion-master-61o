"""FastAPI adapter for URBION station intelligence.

The underlying station intelligence builder is deterministic by default and
never fabricates live readings. Portal adapters can be added later through the
builder's injected fetchers without changing this endpoint contract.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from server import app
from urbion_station_intelligence import build_station_intelligence

router = APIRouter(tags=["station-intelligence"])


@router.get("/station-intelligence")
def station_intelligence(
    site_lat: float,
    site_lon: float,
    state: str = "Melaka",
):
    try:
        return build_station_intelligence(site_lat, site_lon, state=state)
    except ValueError as exc:
        if str(exc) == "INVALID_SPATIAL_INPUT":
            raise HTTPException(
                status_code=422,
                detail={
                    "code": "INVALID_SPATIAL_INPUT",
                    "message": "Site coordinates must be valid and cannot use placeholder coordinates (-90, -180).",
                },
            ) from exc
        raise HTTPException(status_code=422, detail={"code": "STATION_INPUT_ERROR", "message": str(exc)}) from exc


app.include_router(router)

# Imported last so championship_server has already completed `from server import app`
# and all original API routes exist before the optional-TOD UI compatibility routes
# register. The compatibility module reuses the same deterministic planning engines.
import urbion_championship_optional_assessment_api  # noqa: E402,F401
