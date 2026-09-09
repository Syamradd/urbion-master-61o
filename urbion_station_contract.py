"""Explicit source capability contract for station intelligence.

This module is intentionally data-only plus small selectors. It does not fetch
or invent readings. Portal-only sources remain PORTAL_REFERENCE until a
verified machine-query adapter is registered.
"""
from __future__ import annotations

from typing import Any

STATION_SOURCE_CONTRACT: dict[str, dict[str, Any]] = {
    "air_quality": {
        "provider": "JAS MyEQMS / EQMP",
        "mode": "PUBLIC_DATA_PORTAL",
        "machine_query": "AVAILABLE_AS_FEATURE_QUERY",
        "geometry": "FEATURE_QUERY",
        "reading_fields": ["IPU", "PM2.5", "PM10", "SO2", "NO2", "O3", "CO"],
        "evidence_state": "SOURCE_CONTEXT",
        "adapter": "urbion_myeqms_adapter.fetch_myeqms_stations",
    },
    "rainfall": {
        "provider": "JPS Public Infobanjir",
        "mode": "PUBLIC_REAL_TIME_PORTAL",
        "machine_query": "NOT_ESTABLISHED",
        "geometry": "NOT_CLAIMED",
        "reading_fields": ["rainfall", "timestamp", "warning_status"],
        "evidence_state": "SOURCE_CONTEXT",
    },
    "water_level": {
        "provider": "JPS Public Infobanjir",
        "mode": "PUBLIC_REAL_TIME_PORTAL",
        "machine_query": "NOT_ESTABLISHED",
        "geometry": "NOT_CLAIMED",
        "reading_fields": ["water_level", "timestamp", "warning_status"],
        "evidence_state": "SOURCE_CONTEXT",
    },
    "stream_flow": {
        "provider": "JPS Public Infobanjir",
        "mode": "PUBLIC_REAL_TIME_PORTAL",
        "machine_query": "NOT_ESTABLISHED",
        "geometry": "NOT_CLAIMED",
        "reading_fields": ["stream_flow", "timestamp"],
        "evidence_state": "SOURCE_CONTEXT",
    },
    "water_quality": {
        "provider": "Official environmental monitoring sources",
        "mode": "PORTAL_REFERENCE",
        "machine_query": "NOT_ESTABLISHED",
        "geometry": "NOT_CLAIMED",
        "reading_fields": ["water_quality_indicator", "timestamp"],
        "evidence_state": "SOURCE_CONTEXT",
    },
    "geohazard": {
        "provider": "JMG MyGEMS",
        "mode": "LIVE_MAP_SERVICES",
        "machine_query": "AVAILABLE_AS_SPATIAL_CONTEXT",
        "geometry": "FEATURE_QUERY",
        "reading_fields": [],
        "evidence_state": "SOURCE_CONTEXT",
    },
}


def station_source_contract(domain: str) -> dict[str, Any] | None:
    """Return a defensive copy of the contract for one station domain."""
    record = STATION_SOURCE_CONTRACT.get(str(domain).strip())
    return dict(record) if record else None


def live_query_domains() -> list[str]:
    """Return domains whose current contract permits machine-query evidence."""
    return [name for name, record in STATION_SOURCE_CONTRACT.items()
            if record.get("machine_query") not in {"NOT_ESTABLISHED", "NOT_CONFIGURED"}]


def portal_reference_domains() -> list[str]:
    """Return domains that must remain explicitly portal/reference-only."""
    return [name for name, record in STATION_SOURCE_CONTRACT.items()
            if record.get("machine_query") == "NOT_ESTABLISHED"]
