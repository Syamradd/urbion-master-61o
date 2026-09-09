"""Isolated JAS MyEQMS/APIMS source adapter for URBION station intelligence.

This module intentionally does not alter the canonical station endpoint yet.
It normalizes the authoritative public ArcGIS response into the existing
station-engine contract so integration can be reviewed separately.

Evidence rules:
- Geometry and values are used only when supplied by the upstream response.
- No pollutant value is inferred when a field is absent.
- A response with station identity + coordinates + timestamp is VERIFIED;
  otherwise the record remains SOURCE_CONTEXT/EVIDENCE_GAP.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable

import httpx

MYEQMS_QUERY_URL = (
    "https://eqms.doe.gov.my/api3/publicmapproxy/"
    "PUBLIC_DISPLAY/CAQM_MCAQM_Current_Reading/MapServer/0/query"
)
TIMEOUT_S = 8.0


def _as_float(value: Any) -> float | None:
    try:
        return float(value) if value not in (None, "") else None
    except (TypeError, ValueError):
        return None


def _timestamp(value: Any) -> str | None:
    try:
        number = float(value)
        if number > 10_000_000_000:
            dt = datetime.fromtimestamp(number / 1000.0, tz=timezone.utc)
        else:
            dt = datetime.fromtimestamp(number, tz=timezone.utc)
        return dt.isoformat()
    except (TypeError, ValueError, OSError, OverflowError):
        return None


def _first(attrs: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = attrs.get(key)
        if value not in (None, ""):
            return value
    return None


def normalize_feature(feature: dict[str, Any]) -> dict[str, Any] | None:
    """Normalize one official MyEQMS ArcGIS feature to the station contract."""
    attrs = feature.get("attributes") or {}
    geometry = feature.get("geometry") or {}
    lon = _as_float(_first(attrs, "LONGITUDE", "longitude"))
    lat = _as_float(_first(attrs, "LATITUDE", "latitude"))
    if lon is None:
        lon = _as_float(geometry.get("x"))
    if lat is None:
        lat = _as_float(geometry.get("y"))
    station_id = _first(attrs, "STATION_ID", "station_id")
    name = _first(attrs, "PLACE", "STATION_LOCATION", "station_name")
    if not station_id or lat is None or lon is None:
        return None

    last_updated = _timestamp(_first(attrs, "DATETIME", "datetime"))
    record: dict[str, Any] = {
        "name": name or station_id,
        "station_id": station_id,
        "lat": lat,
        "lon": lon,
        "reading": _first(attrs, "API", "api"),
        "last_updated": last_updated,
        "source": "JAS MyEQMS / APIMS",
        "source_url": MYEQMS_QUERY_URL,
        "evidence_state": "VERIFIED" if last_updated else "SOURCE_CONTEXT",
        "status": _first(attrs, "CLASS", "class"),
        "state": _first(attrs, "STATE_NAME", "state_name"),
        "region": _first(attrs, "REGION_NAME", "region_name"),
        "station_location": _first(attrs, "STATION_LOCATION"),
        "place": _first(attrs, "PLACE"),
        "api": _first(attrs, "API", "api"),
        "api_pm10": _first(attrs, "API_PM10", "api_pm10"),
        "primary_pollutant": _first(attrs, "PARAM_SELECTED", "param_selected"),
    }

    aliases = {
        "pm25": ("PM25", "PM2_5", "PM2.5", "PM25_VALUE", "PM2_5_VALUE"),
        "pm10": ("PM10", "PM10_VALUE"),
        "so2": ("SO2", "SO2_VALUE"),
        "no2": ("NO2", "NO2_VALUE"),
        "o3": ("O3", "O3_VALUE"),
        "co": ("CO", "CO_VALUE"),
    }
    for output_key, keys in aliases.items():
        value = _first(attrs, *keys)
        if value not in (None, ""):
            record[output_key] = value
    return record


def fetch_myeqms_stations(
    *,
    state: str | None = None,
    http_get: Callable[..., dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Fetch and normalize the current public MyEQMS station layer."""
    params = {
        "f": "json",
        "where": "1=1",
        "outFields": "*",
        "returnGeometry": "true",
        "outSR": "4326",
        "resultRecordCount": 200,
    }
    if http_get is None:
        with httpx.Client(timeout=TIMEOUT_S, follow_redirects=True) as client:
            response = client.get(MYEQMS_QUERY_URL, params=params)
            response.raise_for_status()
            payload = response.json()
    else:
        payload = http_get(MYEQMS_QUERY_URL, params=params)

    if not isinstance(payload, dict):
        raise ValueError("MYEQMS_INVALID_RESPONSE")
    if payload.get("error"):
        raise ValueError("MYEQMS_QUERY_ERROR")

    records = []
    for feature in payload.get("features") or []:
        record = normalize_feature(feature)
        if record is None:
            continue
        if state and str(record.get("state") or "").strip().casefold() != str(state).strip().casefold():
            continue
        records.append(record)
    return records
