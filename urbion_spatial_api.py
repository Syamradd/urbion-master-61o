"""Spatial intelligence API mounted by the production championship entrypoint."""
from fastapi import APIRouter, Body, HTTPException
from server import app
from urbion_spatial_intelligence import build_spatial_intelligence, nearest_feature, proximity_matrix, catchment_features
from urbion_network_intelligence import network_distance_m

router = APIRouter(tags=["spatial-intelligence"])

def _site(payload):
    try:
        return float(payload["site_lat"]), float(payload["site_lon"])
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail={"code":"INVALID_SPATIAL_INPUT","message":"site_lat and site_lon are required numeric coordinates."}) from exc

@router.post("/spatial/intelligence")
def spatial_intelligence(payload: dict = Body(default_factory=dict)):
    lat, lon = _site(payload)
    try:
        return {"project":"URBION HORIZON", "version":"PHASE-E.8", **build_spatial_intelligence(lat, lon, payload.get("tod_lat"), payload.get("tod_lon"), tuple(payload.get("radii") or (400,800)), payload.get("constraints")), "statutory_verification":"NOT_CLAIMED"}
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail={"code":"INVALID_SPATIAL_INPUT","message":str(exc)}) from exc

@router.post("/spatial/network-access")
def spatial_network_access(payload: dict = Body(default_factory=dict)):
    lat, lon = _site(payload)
    try:
        target_lat = float(payload["target_lat"])
        target_lon = float(payload["target_lon"])
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail={"code":"INVALID_NETWORK_TARGET","message":"target_lat and target_lon are required numeric coordinates."}) from exc
    if not all(-90 <= value <= 90 for value in (lat, target_lat)) or not all(-180 <= value <= 180 for value in (lon, target_lon)):
        raise HTTPException(status_code=422, detail={"code":"INVALID_SPATIAL_INPUT","message":"Coordinates are outside valid geographic ranges."})
    return {
        "site":{"latitude":lat,"longitude":lon},
        "target":{"latitude":target_lat,"longitude":target_lon},
        "network":network_distance_m(lat, lon, target_lat, target_lon),
        "decision_boundary":"NETWORK_MOBILITY_SCREENING",
        "statutory_verification":"NOT_CLAIMED",
    }

@router.get("/spatial/catchments")
def spatial_catchments(site_lat: float, site_lon: float, radii: str = "400,800"):
    try:
        parsed = tuple(int(x.strip()) for x in radii.split(",") if x.strip())
        return catchment_features(site_lat, site_lon, parsed)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail={"code":"INVALID_CATCHMENT_INPUT","message":str(exc)}) from exc

@router.post("/spatial/nearest")
def spatial_nearest(payload: dict = Body(default_factory=dict)):
    lat, lon = _site(payload)
    result = nearest_feature(lat, lon, payload.get("features") or [])
    return {"site":{"latitude":lat,"longitude":lon},"nearest":result,"decision_boundary":"CALCULATED_PROXIMITY","statutory_verification":"NOT_CLAIMED"}

@router.post("/spatial/matrix")
def spatial_matrix(payload: dict = Body(default_factory=dict)):
    try:
        result = proximity_matrix(payload.get("origins") or [], payload.get("destinations") or [])
        return {"matrix":result,"count":len(result),"evidence":"CALCULATED","statutory_verification":"NOT_CLAIMED"}
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail={"code":"INVALID_MATRIX_INPUT","message":str(exc)}) from exc

app.include_router(router)
