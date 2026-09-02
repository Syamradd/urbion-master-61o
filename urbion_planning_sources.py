"""Authoritative planning-source registry for URBION."""
from __future__ import annotations
from typing import Any

PLANNING_SOURCES: list[dict[str, Any]] = [
    {
        "id": "RT_MBMB",
        "name": "PLANMalaysia Melaka — Rancangan Tempatan",
        "layers": ["RT", "ZONING", "LAND_USE", "PLANNING_POLICY"],
        "status": "REFERENCE_REGISTERED",
        "authority": "PLANMalaysia Melaka",
        "reference": "https://www.jpbdmelaka.gov.my/rt-rancangan-tempatan",
    },
    {
        "id": "IPLAN",
        "name": "i-Plan PLANMalaysia",
        "layers": ["ZONING", "LAND_USE", "LOT", "RT"],
        "status": "PLANNED",
        "authority": "PLANMalaysia",
        "reference": "https://iplan.planmalaysia.gov.my/",
    },
    {
        "id": "MELGIS",
        "name": "MelGIS / PBT GIS",
        "layers": ["PARCEL", "LAND_USE", "ZONING", "BOUNDARY"],
        "status": "DISCOVERY_COMPLETE",
        "authority": "Melaka GIS / PBT",
        "reference": "https://melgis.melaka.gov.my",
    },
    {
        "id": "JUPEM",
        "name": "JUPEM",
        "layers": ["PARCEL", "CADASTRAL", "BOUNDARY"],
        "status": "PLANNED",
        "authority": "JUPEM",
        "reference": None,
    },
]


def planning_source_summary() -> dict[str, Any]:
    counts: dict[str, int] = {}
    for source in PLANNING_SOURCES:
        status = source["status"]
        counts[status] = counts.get(status, 0) + 1
    return {
        "sources": PLANNING_SOURCES,
        "status_counts": counts,
        "verified_query_sources": [s["id"] for s in PLANNING_SOURCES if s["status"] == "VERIFIED"],
        "evidence_gaps": [s["id"] for s in PLANNING_SOURCES if s["status"] in {"PLANNED", "DISCOVERY_COMPLETE"}],
        "version": "MASTER-109",
    }
