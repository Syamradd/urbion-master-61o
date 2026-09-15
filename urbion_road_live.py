from __future__ import annotations

"""Live OpenStreetMap/Overpass context for URBION road intelligence.

This adapter is deliberately source-context only. It discovers nearby OSM roads
and significant place nodes for planner orientation, but it does not claim an
official Malaysian road classification, statutory accessibility threshold, or
authority decision. Existing explicit source-backed inputs remain preferred.
"""

import json
import math
import os
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from typing import Any

OVERPASS_URL = os.getenv("URBION_OVERPASS_URL", "https://overpass-api.de/api/interpreter").strip()
OVERPASS_FALLBACKS = tuple(x.strip() for x in os.getenv("URBION_OVERPASS_FALLBACKS", "https://overpass.kumi.systems/api/interpreter,https://overpass.private.coffee/api/interpreter").split(",") if x.strip())
ROAD_RADIUS_M = 5000
CENTRE_RADIUS_M = 50000
ROAD_CLASSES = (
    ("motorway", "Motorway / Lebuhraya", 0),
    ("trunk", "Trunk / Laluan Utama", 1),
    ("primary", "Primary / Jalan Utama", 2),
    ("secondary", "Secondary / Jalan Sekunder", 3),
    ("tertiary", "Tertiary / Jalan Pengumpul", 4),
    ("unclassified", "Unclassified / Jalan Lain", 5),
    ("residential", "Residential / Jalan Tempatan", 6),
    ("service", "Service / Akses", 7),
)
ROAD_RANK = {key: rank for key, _, rank in ROAD_CLASSES}
ROAD_LABEL = {key: label for key, label, _ in ROAD_CLASSES}


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def _clean(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _overpass_urls() -> list[str]:
    urls: list[str] = []
    for url in (OVERPASS_URL, *OVERPASS_FALLBACKS):
        if url and url not in urls:
            urls.append(url)
    return urls


def _request_one(url: str, query: str, timeout: float) -> dict[str, Any]:
    body = urllib.parse.urlencode({"data": query}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "User-Agent": "URBION-HORIZON/1.0"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8", errors="replace"))
    if not isinstance(payload, dict):
        raise RuntimeError("Overpass returned a non-object payload")
    return payload


def _request(query: str, timeout: float = 8.0) -> dict[str, Any]:
    """Race configured Overpass endpoints so one slow mirror cannot block the UI."""
    urls = _overpass_urls()
    if not urls:
        raise RuntimeError("No Overpass endpoint is configured")
    last: Exception | None = None
    with ThreadPoolExecutor(max_workers=min(3, len(urls))) as pool:
        futures = {pool.submit(_request_one, url, query, timeout): url for url in urls[:3]}
        for future in as_completed(futures):
            try:
                return future.result()
            except Exception as exc:
                last = exc
        for future in futures:
            future.cancel()
    raise RuntimeError(f"All Overpass endpoints unavailable: {last}")


def _valid_point(lat: Any, lon: Any) -> bool:
    try:
        lat_n, lon_n = float(lat), float(lon)
        return math.isfinite(lat_n) and math.isfinite(lon_n) and -90 <= lat_n <= 90 and -180 <= lon_n <= 180
    except (TypeError, ValueError):
        return False


def _road_query(lat: float, lon: float) -> str:
    classes = "|".join(key for key, _, _ in ROAD_CLASSES)
    return f'''[out:json][timeout:8];way(around:{ROAD_RADIUS_M},{lat},{lon})["highway"~"^({classes})$"];out tags center;'''


def _centre_query(lat: float, lon: float) -> str:
    return f'''[out:json][timeout:8];node(around:{CENTRE_RADIUS_M},{lat},{lon})["place"~"^(city|town|municipality)$"];out tags;'''


def discover_live_road_context(site_lat: float, site_lon: float) -> dict[str, Any]:
    """Discover source-backed OSM road hierarchy tags and nearby urban centres."""
    if not _valid_point(site_lat, site_lon):
        raise ValueError("Site coordinates must be finite numeric values")
    site_lat, site_lon = float(site_lat), float(site_lon)
    queried_at = datetime.now(timezone.utc).isoformat()

    road_error: str | None = None
    try:
        road_data = _request(_road_query(site_lat, site_lon), timeout=8.0)
    except Exception as exc:
        road_data = {"elements": []}
        road_error = str(exc)

    roads = []
    for element in road_data.get("elements") or []:
        tags = element.get("tags") or {}
        highway = str(tags.get("highway") or "").strip().lower()
        if highway not in ROAD_RANK:
            continue
        center = element.get("center") or {}
        if not _valid_point(center.get("lat"), center.get("lon")):
            continue
        center_lat, center_lon = float(center["lat"]), float(center["lon"])
        distance = haversine_km(site_lat, site_lon, center_lat, center_lon) * 1000.0
        roads.append({
            "name": tags.get("name") or tags.get("ref") or f"{ROAD_LABEL[highway]} (unnamed)",
            "ref": tags.get("ref"),
            "highway": highway,
            "hierarchy": ROAD_LABEL[highway],
            "distance_m": round(distance, 1),
            "distance_km": round(distance / 1000.0, 3),
            "lat": center_lat,
            "lon": center_lon,
            "source": "OpenStreetMap via Overpass API",
            "evidence_status": "SOURCE_CONTEXT",
        })

    roads.sort(key=lambda x: (x["distance_m"], ROAD_RANK.get(x["highway"], 99)))
    unique_roads: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for row in roads:
        key = (str(row.get("name") or ""), str(row.get("highway") or ""))
        if key in seen:
            continue
        seen.add(key)
        unique_roads.append(row)
        if len(unique_roads) >= 25:
            break

    centres: list[dict[str, Any]] = []
    centre_error: str | None = None
    if unique_roads:
        try:
            centre_data = _request(_centre_query(site_lat, site_lon), timeout=8.0)
        except Exception as exc:
            centre_data = {"elements": []}
            centre_error = str(exc)
    else:
        centre_data = {"elements": []}
        if road_error:
            centre_error = "Centre query skipped because no live road endpoint responded."

    seen_centres: set[tuple[str, str]] = set()
    for element in centre_data.get("elements") or []:
        tags = element.get("tags") or {}
        name = tags.get("name") or tags.get("name:en") or tags.get("name:ms")
        place = str(tags.get("place") or "").lower()
        if not name or place not in {"city", "town", "municipality"}:
            continue
        lat, lon = element.get("lat"), element.get("lon")
        if not _valid_point(lat, lon):
            continue
        key = (str(name).casefold(), place)
        if key in seen_centres:
            continue
        seen_centres.add(key)
        distance = haversine_km(site_lat, site_lon, float(lat), float(lon))
        centres.append({
            "name": name,
            "type": place,
            "distance_km": round(distance, 3),
            "source": "OpenStreetMap via Overpass API",
            "evidence_status": "SOURCE_CONTEXT",
            "importance": "MAJOR" if place in {"city", "municipality"} else "URBAN_CENTRE",
        })
    centres.sort(key=lambda x: (x["distance_km"], 0 if x.get("importance") == "MAJOR" else 1))
    centres = centres[:20]

    nearest = unique_roads[0] if unique_roads else None
    hierarchy_levels = []
    for key, label, _ in ROAD_CLASSES:
        candidates = [x for x in unique_roads if x.get("highway") == key]
        if not candidates:
            continue
        nearest_for_class = min(candidates, key=lambda x: x["distance_m"])
        hierarchy_levels.append({
            "highway": key,
            "hierarchy": label,
            "nearest_name": nearest_for_class.get("name"),
            "distance_m": nearest_for_class.get("distance_m"),
            "distance_km": nearest_for_class.get("distance_km"),
            "lat": nearest_for_class.get("lat"),
            "lon": nearest_for_class.get("lon"),
            "source": "OpenStreetMap via Overpass API",
            "evidence_status": "SOURCE_CONTEXT",
        })

    status = "LIVE" if unique_roads or centres else "NO_FEATURE"
    errors = [x for x in (road_error, centre_error) if x]
    return {
        "status": status,
        "source": "OpenStreetMap via Overpass API",
        "queried_at_utc": queried_at,
        "site": {"latitude": site_lat, "longitude": site_lon},
        "road_radius_m": ROAD_RADIUS_M,
        "centre_radius_m": CENTRE_RADIUS_M,
        "nearest_road": nearest,
        "roads": unique_roads,
        "hierarchy_levels": hierarchy_levels,
        "centre_proximity": centres,
        "statutory_verification": "NOT_CLAIMED",
        "evidence_boundary": "OSM road tags and place proximity are source context; Malaysian statutory road hierarchy and accessibility thresholds require authoritative verification.",
        "error_type": "OVERPASS_UNAVAILABLE" if errors and not unique_roads else None,
        "error": "; ".join(errors) if errors else None,
    }
