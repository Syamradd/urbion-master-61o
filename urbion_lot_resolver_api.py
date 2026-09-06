from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException
from server import app
from urbion_lot_resolver import resolve_lot

router = APIRouter(tags=["lot-resolution"])


@router.post("/spatial/lot-resolve")
def spatial_lot_resolve(payload: dict = Body(default_factory=dict)):
    try:
        return resolve_lot(
            lat=payload.get("site_lat"),
            lon=payload.get("site_lon"),
            state=payload.get("state") or "Melaka",
            lot_no=payload.get("lot_no"),
            upi=payload.get("upi"),
            project_reference=payload.get("project_reference"),
        )
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail={"code":"INVALID_LOT_RESOLUTION_INPUT","message":str(exc)}) from exc


@router.get("/spatial/lot-resolve")
def spatial_lot_resolve_get(site_lat: float | None = None, site_lon: float | None = None, state: str = "Melaka", lot_no: str | None = None, upi: str | None = None):
    try:
        return resolve_lot(site_lat, site_lon, state, lot_no, upi)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail={"code":"INVALID_LOT_RESOLUTION_INPUT","message":str(exc)}) from exc


app.include_router(router)
