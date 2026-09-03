"""Live station intelligence helpers for LCP-ready spatial evidence.

Network adapters are deliberately injectable so CI remains deterministic. The
module never invents a reading: unavailable portal data is surfaced as a
review gap with SOURCE_CONTEXT provenance.
"""
from __future__ import annotations

from datetime import datetime, timezone
from math import asin, cos, isfinite, radians, sin, sqrt
from typing import Any, Callable, Iterable

STATE_CODES = {"Melaka": "MLK", "Selangor": "SGR", "Johor": "JHR", "Perak": "PRK", "Pahang": "PHG", "Kedah": "KDH", "Perlis": "PLS", "Penang": "PNG", "Negeri Sembilan": "NSN", "Kelantan": "KTN", "Terengganu": "TRG", "Sabah": "SBH", "Sarawak": "SRW", "WP Kuala Lumpur": "WPKL", "Putrajaya": "PJY", "Labuan": "LBN"}
DOE_APIMS_URL = "https://eqms.doe.gov.my/api3/publicmapproxy/PUBLIC_DISPLAY/CAQM_MCAQM_Current_Reading/MapServer/0/query"
JPS_RAINFALL_URL = "https://publicinfobanjir.water.gov.my/hujan/data-hujan/"
JPS_WATER_LEVEL_URL = "https://publicinfobanjir.water.gov.my/aras-air/data-paras-air/"


def _valid_coord(lat: Any, lon: Any) -> bool:
    try:
        return isfinite(float(lat)) and isfinite(float(lon)) and -90 <= float(lat) <= 90 and -180 <= float(lon) <= 180
    except (TypeError, ValueError):
        return False


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    if not all(_valid_coord(a, b) for a, b in ((lat1, lon1), (lat2, lon2))):
        raise ValueError("INVALID_SPATIAL_INPUT")
    r = 6371008.8
    p1, p2 = radians(lat1), radians(lat2)
    dp, dl = radians(lat2-lat1), radians(lon2-lon1)
    a = sin(dp/2)**2 + cos(p1)*cos(p2)*sin(dl/2)**2
    return 2*r*asin(sqrt(a))


def nearest_station(site_lat: float, site_lon: float, stations: Iterable[dict[str, Any]]) -> dict[str, Any] | None:
    candidates = []
    for station in stations:
        lat, lon = station.get("lat"), station.get("lon")
        if not _valid_coord(lat, lon):
            continue
        item = dict(station)
        item["distance_m"] = round(haversine_m(site_lat, site_lon, float(lat), float(lon)), 1)
        candidates.append(item)
    return min(candidates, key=lambda x: x["distance_m"]) if candidates else None


def freshness_minutes(last_updated: Any, now: datetime | None = None) -> float | None:
    if not last_updated:
        return None
    try:
        text = str(last_updated).replace("Z", "+00:00")
        dt = datetime.fromisoformat(text)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        ref = now or datetime.now(timezone.utc)
        return round(max(0.0, (ref - dt.astimezone(timezone.utc)).total_seconds()/60), 1)
    except (TypeError, ValueError):
        return None


def classify_api(value: Any) -> str | None:
    try:
        n = float(value)
    except (TypeError, ValueError):
        return None
    if n <= 50: return "Good"
    if n <= 100: return "Moderate"
    if n <= 200: return "Unhealthy"
    if n <= 300: return "Very Unhealthy"
    return "Hazardous"


def build_lcp_snapshot(records: dict[str, dict[str, Any] | None]) -> list[dict[str, Any]]:
    snapshot = []
    for domain, rec in records.items():
        if not rec:
            continue
        snapshot.append({"domain": domain, "station": rec.get("name"), "station_id": rec.get("station_id"), "distance_m": rec.get("distance_m"), "reading": rec.get("reading"), "last_updated": rec.get("last_updated"), "status": rec.get("status"), "source": rec.get("source"), "evidence_state": rec.get("evidence_state", "SOURCE_CONTEXT")})
    return snapshot


def build_station_intelligence(site_lat: float, site_lon: float, state: str = "Melaka", fetchers: dict[str, Callable[..., list[dict[str, Any]]]] | None = None) -> dict[str, Any]:
    if not _valid_coord(site_lat, site_lon) or (float(site_lat), float(site_lon)) == (-90.0, -180.0):
        raise ValueError("INVALID_SPATIAL_INPUT")
    fetchers = fetchers or {}
    state_code = STATE_CODES.get(state, state)
    records: dict[str, dict[str, Any] | None] = {}
    gaps: list[str] = []
    for domain in ("air_quality", "rainfall", "water_level", "stream_flow", "water_quality", "geohazard"):
        fn = fetchers.get(domain)
        if not fn:
            gaps.append(f"{domain}:LIVE_QUERY_NOT_CONFIGURED")
            records[domain] = None
            continue
        try:
            stations = fn(state=state, state_code=state_code)
            records[domain] = nearest_station(float(site_lat), float(site_lon), stations)
            if records[domain] is None:
                gaps.append(f"{domain}:NO_VALID_STATION_GEOMETRY")
        except Exception as exc:
            records[domain] = None
            gaps.append(f"{domain}:LIVE_QUERY_FAILED:{type(exc).__name__}")
    for rec in records.values():
        if rec:
            rec["freshness_minutes"] = freshness_minutes(rec.get("last_updated"))
            if rec.get("api") is not None:
                rec.setdefault("reading", rec.get("api"))
                rec.setdefault("status", classify_api(rec.get("api")))
            rec.setdefault("evidence_state", "SOURCE_CONTEXT")
    return {"status": "LIVE_STATION_INTELLIGENCE", "as_of": datetime.now(timezone.utc).isoformat(), "site": {"lat": float(site_lat), "lon": float(site_lon)}, "state": state, "nearest": records, "lcp_snapshot": build_lcp_snapshot(records), "review_gaps": gaps, "statutory_verification": "NOT_CLAIMED"}
