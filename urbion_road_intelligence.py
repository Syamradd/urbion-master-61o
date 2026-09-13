from __future__ import annotations

"""Deterministic road/centre proximity screening helpers for URBION.

This module does not invent road hierarchy or place data. Callers pass explicit
source-backed features; missing values stay UNVERIFIED/REQUIRES REVIEW.
"""

from math import asin, cos, radians, sin, sqrt
from typing import Any


DEFAULT_RADIUS_KM = (1, 5, 10, 25, 50)


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0088
    p1, p2 = radians(lat1), radians(lat2)
    dp = radians(lat2 - lat1)
    dl = radians(lon2 - lon1)
    a = sin(dp / 2) ** 2 + cos(p1) * cos(p2) * sin(dl / 2) ** 2
    return 2 * r * asin(sqrt(a))


def _clean(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _status(source: Any, value: Any) -> str:
    return "SOURCE_CONTEXT" if value is not None and _clean(source) else "UNVERIFIED"


def build_road_intelligence(
    *,
    site_lat: float | None,
    site_lon: float | None,
    nearest_road_name: str | None = None,
    nearest_road_distance_m: float | None = None,
    road_hierarchy: str | None = None,
    road_source: str | None = None,
    centres: list[dict[str, Any]] | None = None,
    radius_km: tuple[int, ...] = DEFAULT_RADIUS_KM,
) -> dict[str, Any]:
    """Build a transparent road/accessibility profile from explicit inputs.

    `centres` items may contain name, type, lat, lon, distance_km, source.
    Distance is calculated only when a centre has valid coordinates.
    """
    road = {
        "nearest_road": {
            "name": _clean(nearest_road_name),
            "distance_m": nearest_road_distance_m,
            "distance_km": round(nearest_road_distance_m / 1000, 3) if nearest_road_distance_m is not None else None,
            "hierarchy": _clean(road_hierarchy),
            "source": _clean(road_source),
            "evidence_status": _status(road_source, nearest_road_name or nearest_road_distance_m or road_hierarchy),
        },
        "hierarchy_chain": [],
    }
    hierarchy = _clean(road_hierarchy)
    if hierarchy:
        road["hierarchy_chain"] = ["SITE", hierarchy.upper()]

    proximity: list[dict[str, Any]] = []
    for item in centres or []:
        row = dict(item)
        name = _clean(row.get("name"))
        source = _clean(row.get("source"))
        lat = row.get("lat")
        lon = row.get("lon")
        dist = row.get("distance_km")
        try:
            if site_lat is not None and site_lon is not None and lat is not None and lon is not None:
                dist = haversine_km(float(site_lat), float(site_lon), float(lat), float(lon))
            elif dist is not None:
                dist = float(dist)
            else:
                dist = None
        except (TypeError, ValueError):
            dist = None
        row["name"] = name
        row["source"] = source
        row["distance_km"] = round(dist, 3) if dist is not None else None
        row["evidence_status"] = _status(source, name or dist)
        row.pop("lat", None)
        row.pop("lon", None)
        proximity.append(row)

    proximity.sort(key=lambda x: x.get("distance_km") is None)
    rings = []
    for ring in radius_km:
        inside = [x["name"] for x in proximity if x.get("distance_km") is not None and x["distance_km"] <= ring and x.get("name")]
        rings.append({"radius_km": ring, "centres_inside": inside})

    return {
        "version": "ROAD-1.0",
        "road_access": road,
        "centre_proximity": proximity,
        "radius_analysis": rings,
        "evidence_boundary": "Road hierarchy and centre identity remain source-context unless explicitly supplied from a geospatial source.",
    }
