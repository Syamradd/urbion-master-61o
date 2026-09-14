from __future__ import annotations

"""Road/accessibility screening helpers for URBION.

The deterministic output remains transparent and source-state aware. When
explicit source-backed road/centre inputs are absent, a live OpenStreetMap /
Overpass context is requested and clearly labelled as SOURCE_CONTEXT.
No statutory Malaysian road classification or legal accessibility threshold is
inferred from OSM tags.
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


def _live_context(site_lat: float | None, site_lon: float | None) -> dict[str, Any] | None:
    if site_lat is None or site_lon is None:
        return None
    try:
        from urbion_road_live import discover_live_road_context
        return discover_live_road_context(float(site_lat), float(site_lon))
    except Exception as exc:
        return {
            "status": "UNAVAILABLE",
            "source": "OpenStreetMap via Overpass API",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "statutory_verification": "NOT_CLAIMED",
        }


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
    """Build a transparent road/accessibility profile.

    Explicit source-backed values win. Missing road or centre context may be
    enriched from the live OSM/Overpass adapter, while every discovered value
    stays SOURCE_CONTEXT and the statutory boundary remains NOT_CLAIMED.
    """
    explicit_centres = list(centres or [])
    live = None
    needs_live = not (nearest_road_name or nearest_road_distance_m is not None or road_hierarchy) or not explicit_centres
    if needs_live:
        live = _live_context(site_lat, site_lon)

    live_road = (live or {}).get("nearest_road") or {}
    final_name = _clean(nearest_road_name) or _clean(live_road.get("name"))
    final_distance = nearest_road_distance_m if nearest_road_distance_m is not None else live_road.get("distance_m")
    final_hierarchy = _clean(road_hierarchy) or _clean(live_road.get("hierarchy"))
    final_source = _clean(road_source) or _clean(live_road.get("source"))

    road = {
        "nearest_road": {
            "name": final_name,
            "distance_m": final_distance,
            "distance_km": round(float(final_distance) / 1000, 3) if final_distance is not None else None,
            "hierarchy": final_hierarchy,
            "source": final_source,
            "evidence_status": _status(final_source, final_name or final_distance or final_hierarchy),
        },
        "hierarchy_chain": [],
    }
    hierarchy = _clean(final_hierarchy)
    if hierarchy:
        road["hierarchy_chain"] = ["SITE", hierarchy.upper()]

    live_hierarchy = list((live or {}).get("hierarchy_levels") or [])
    road["hierarchy_levels"] = live_hierarchy
    if live_hierarchy and not hierarchy:
        road["hierarchy_chain"] = ["SITE"] + [str(x.get("hierarchy") or x.get("highway") or "").upper() for x in live_hierarchy]

    merged: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for item in explicit_centres + list((live or {}).get("centre_proximity") or []):
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
        key = (str(name or "").casefold(), str(row.get("type") or ""))
        if key in seen or not name:
            continue
        seen.add(key)
        row["name"] = name
        row["source"] = source
        row["distance_km"] = round(dist, 3) if dist is not None else None
        row["evidence_status"] = _status(source, name or dist)
        row.pop("lat", None)
        row.pop("lon", None)
        merged.append(row)

    merged.sort(key=lambda x: (x.get("distance_km") is None, x.get("distance_km") if x.get("distance_km") is not None else float("inf")))
    rings = []
    for ring in radius_km:
        inside = [x["name"] for x in merged if x.get("distance_km") is not None and x["distance_km"] <= ring and x.get("name")]
        rings.append({"radius_km": ring, "centres_inside": inside})

    nearest_city = next((x for x in merged if str(x.get("type") or "").lower() == "city"), None)
    nearest_town = next((x for x in merged if str(x.get("type") or "").lower() == "town"), None)
    return {
        "version": "ROAD-2.0",
        "road_access": road,
        "centre_proximity": merged,
        "nearest_city": nearest_city,
        "nearest_town": nearest_town,
        "radius_analysis": rings,
        "live_network": {
            "status": (live or {}).get("status", "NOT_QUERIED"),
            "source": (live or {}).get("source"),
            "road_count": len((live or {}).get("roads") or []),
            "centre_count": len((live or {}).get("centre_proximity") or []),
            "queried_at_utc": (live or {}).get("queried_at_utc"),
            "road_radius_m": (live or {}).get("road_radius_m"),
            "centre_radius_m": (live or {}).get("centre_radius_m"),
            "error_type": (live or {}).get("error_type"),
        },
        "evidence_boundary": "OSM road tags and centre proximity are source context; Malaysian statutory road hierarchy, road reserve standards, access spacing and authority requirements require authoritative verification.",
        "statutory_verification": "NOT_CLAIMED",
    }
