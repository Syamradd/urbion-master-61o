"""Transit-oriented spatial analytics for URBION."""
from __future__ import annotations
from math import asin, cos, radians, sin, sqrt
from typing import Any


def haversine_m(*, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    p1, p2 = radians(lat1), radians(lat2)
    dlat, dlon = radians(lat2-lat1), radians(lon2-lon1)
    a = sin(dlat/2)**2 + cos(p1)*cos(p2)*sin(dlon/2)**2
    return 6371000 * 2 * asin(sqrt(a))


def tod_catchment(*, site_lat: float, site_lon: float, tod_lat: float, tod_lon: float) -> dict[str, Any]:
    distance = round(haversine_m(lat1=site_lat, lon1=site_lon, lat2=tod_lat, lon2=tod_lon), 2)
    if distance <= 400:
        band = "TOD 400m"
    elif distance <= 800:
        band = "TOD 800m"
    else:
        band = "OUTSIDE 800m"
    return {"distance_m": distance, "band": band, "within_400m": distance <= 400, "within_800m": distance <= 800, "evidence_type": "SPATIAL_DISTANCE", "decision_safe": False, "note": "Spatial proximity is an analytical signal; applicable planning rules and authoritative evidence remain controlling."}
