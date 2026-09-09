"""Verified MyGEMS public ArcGIS adapter for URBION HORIZON.

The adapter is deliberately server-side and evidence-first:
- queries the official JMG MyGEMS FeatureServer;
- requests GeoJSON geometry in EPSG:4326;
- normalises source attributes without inventing values;
- returns explicit NO_FEATURE / QUERY_ERROR states;
- keeps the result SOURCE_CONTEXT, never statutory verification.
"""
from __future__ import annotations

from typing import Any

import httpx

MYGEMS_LITHOLOGY_SERVICE = (
    "https://mygems.jmg.gov.my/server/rest/services/"
    "Demarcation/Litology_by_Negeri/FeatureServer"
)

STATE_LAYER_IDS = {
    "Perlis": 0,
    "Kedah": 2,
    "Pulau Pinang": 4,
    "Perak": 6,
    "Kelantan": 8,
    "Terengganu": 10,
    "Pahang": 12,
    "Selangor": 14,
    "Putrajaya": 16,
    "Kuala Lumpur": 18,
    "Negeri Sembilan": 20,
    "Melaka": 22,
    "Johor": 24,
    "Sabah": 26,
    "Sarawak": 28,
}

DEFAULT_RADIUS_M = 800.0
MAX_RADIUS_M = 5000.0
MAX_FEATURES = 60
TIMEOUT_S = 8.0


def _valid_coord(lat: Any, lon: Any) -> bool:
    try:
        lat, lon = float(lat), float(lon)
    except (TypeError, ValueError):
        return False
    return -90 <= lat <= 90 and -180 <= lon <= 180


def layer_id_for_state(state: str) -> int | None:
    return STATE_LAYER_IDS.get(str(state or "").strip())


def query_mygems_lithology(
    site_lat: float,
    site_lon: float,
    *,
    state: str = "Melaka",
    radius_m: float = DEFAULT_RADIUS_M,
    http_get=None,
) -> dict[str, Any]:
    """Query nearby official MyGEMS lithology features.

    ``http_get`` is injectable so CI can remain deterministic. The production
    default is ``httpx.Client.get`` against the official JMG service.
    """
    if not _valid_coord(site_lat, site_lon):
        raise ValueError("INVALID_SPATIAL_INPUT")
    layer_id = layer_id_for_state(state)
    if layer_id is None:
        return {
            "layer_id": "mygems-lithology",
            "source": "JMG MyGEMS",
            "status": "NOT_CONFIGURED",
            "evidence_state": "EVIDENCE_GAP",
            "feature_count": 0,
            "features": [],
        }
    try:
        radius = min(MAX_RADIUS_M, max(1.0, float(radius_m)))
    except (TypeError, ValueError):
        raise ValueError("INVALID_RADIUS")

    url = f"{MYGEMS_LITHOLOGY_SERVICE}/{layer_id}/query"
    params = {
        "where": "1=1",
        "geometry": f"{float(site_lon)},{float(site_lat)}",
        "geometryType": "esriGeometryPoint",
        "inSR": "4326",
        "spatialRel": "esriSpatialRelIntersects",
        "distance": radius,
        "units": "esriSRUnit_Meter",
        "outFields": "OBJECTID,AGE,AGECODE,FCD,FNM,UGI,GLN,GAM,GAX,GLR,GLS,GEO,DAT,GFD,GLL,HOR,NAM,ARK",
        "returnGeometry": "true",
        "outSR": "4326",
        "resultRecordCount": MAX_FEATURES,
        "f": "geojson",
    }

    try:
        if http_get is None:
            with httpx.Client(timeout=TIMEOUT_S, follow_redirects=True, headers={"User-Agent": "URBION-HORIZON"}) as client:
                response = client.get(url, params=params)
        else:
            response = http_get(url, params=params)
        response.raise_for_status()
        payload = response.json()
        features = list(payload.get("features") or [])[:MAX_FEATURES]
        return {
            "layer_id": "mygems-lithology",
            "source": "JMG MyGEMS",
            "source_url": url,
            "source_service": MYGEMS_LITHOLOGY_SERVICE,
            "state": state,
            "status": "LIVE_QUERY" if features else "NO_FEATURE",
            "evidence_state": "SOURCE_CONTEXT",
            "feature_count": len(features),
            "features": features,
            "query": {"radius_m": radius, "geometry": {"lat": float(site_lat), "lon": float(site_lon)}},
            "statutory_verification": "NOT_CLAIMED",
        }
    except Exception as exc:
        return {
            "layer_id": "mygems-lithology",
            "source": "JMG MyGEMS",
            "source_url": url,
            "state": state,
            "status": "QUERY_ERROR",
            "evidence_state": "EVIDENCE_GAP",
            "feature_count": 0,
            "features": [],
            "error_type": type(exc).__name__,
            "statutory_verification": "NOT_CLAIMED",
        }


__all__ = ["MYGEMS_LITHOLOGY_SERVICE", "STATE_LAYER_IDS", "layer_id_for_state", "query_mygems_lithology"]
