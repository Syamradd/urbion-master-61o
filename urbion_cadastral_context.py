"""Official iPLAN cadastral parcel query bridge for URBION HORIZON."""
from __future__ import annotations

from typing import Any
import math

import httpx

STATE_CODES = {
    "Johor": "01", "Kedah": "02", "Kelantan": "03", "Melaka": "04",
    "Negeri Sembilan": "05", "Pahang": "06", "Pulau Pinang": "07",
    "Perak": "08", "Perlis": "09", "Selangor": "10", "Terengganu": "11",
    "Sabah": "12", "Sarawak": "13", "Wilayah Persekutuan": "14",
    "Labuan": "15", "Putrajaya": "16",
}

ARCGIS_ROOT = "https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN"
TIMEOUT_S = 8.0
MAX_FEATURES = 60


def _validate(lat: Any, lon: Any, radius_m: Any) -> tuple[float, float, float]:
    lat, lon, radius_m = float(lat), float(lon), float(radius_m)
    if not math.isfinite(lat) or not math.isfinite(lon) or not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        raise ValueError("coordinates are outside valid geographic ranges")
    if not math.isfinite(radius_m) or radius_m <= 0:
        raise ValueError("radius_m must be positive")
    return lat, lon, min(radius_m, 5000.0)


def cadastral_service_url(state: str) -> str:
    code = STATE_CODES.get(str(state).strip())
    if not code:
        raise ValueError(f"unsupported cadastral state: {state}")
    return f"{ARCGIS_ROOT}/LOT_{code}/MapServer/0"


def query_cadastral(lat: Any, lon: Any, radius_m: Any = 120, state: str = "Melaka") -> dict:
    lat, lon, radius_m = _validate(lat, lon, radius_m)
    layer_url = cadastral_service_url(state)
    params = {
        "where": "1=1",
        "geometry": f"{lon},{lat}",
        "geometryType": "esriGeometryPoint",
        "inSR": "4326",
        "spatialRel": "esriSpatialRelIntersects",
        "distance": radius_m,
        "units": "esriSRUnit_Meter",
        "outFields": "OBJECTID,NEGERI,DAERAH,MUKIM,SEKSYEN,LOT,UPI,KELUASAN",
        "returnGeometry": "true",
        "outSR": "4326",
        "resultRecordCount": MAX_FEATURES,
        "f": "geojson",
    }
    with httpx.Client(timeout=TIMEOUT_S, follow_redirects=True, headers={"User-Agent": "URBION-HORIZON/MASTER-331"}) as client:
        response = client.get(layer_url + "/query", params=params)
        response.raise_for_status()
        payload = response.json()
    if payload.get("error"):
        raise RuntimeError(str(payload["error"])[:240])
    features = list(payload.get("features") or [])[:MAX_FEATURES]
    return {
        "id": "iplan-cadastral",
        "name": "i-Plan · Cadastral Parcels",
        "name_ms": "i-Plan · Lot Kadaster",
        "group": "CADASTRAL",
        "status": "LIVE_QUERY" if features else "NO_FEATURE",
        "feature_count": len(features),
        "inside_count": len(features),
        "nearest_distance_m": 0 if features else None,
        "nearest_feature": None,
        "features": features,
        "source": layer_url,
        "evidence": "SOURCE_CONTEXT",
        "decision_safe": False,
        "query_kind": "ARCGIS",
        "service": "PLANMalaysia iPLAN LOT_* ArcGIS REST Feature Layer",
        "fields": ["LOT", "UPI", "KELUASAN", "NEGERI", "DAERAH", "MUKIM", "SEKSYEN"],
    }
