"""Evidence-aware multi-source spatial intelligence helpers for URBION.

These helpers summarize source availability without inventing measurements. A
source can be live, portal-only, unavailable, or not queried; only explicit
numeric inputs are converted into calculated screening metrics.
"""
from __future__ import annotations


def _state(value: str | None) -> str:
    if value in {"LIVE_QUERY", "LIVE_WMS"}:
        return "SOURCE_CONTEXT"
    if value in {"PUBLIC_PORTAL", "PUBLIC_REAL_TIME_PORTAL", "PORTAL_REFERENCE"}:
        return "SOURCE_CONTEXT"
    if value in {"VERIFIED"}:
        return "VERIFIED"
    return "UNVERIFIED"


def build_spatial_intelligence(*, source_context: dict | None = None,
                               road_distance_m: float | None = None,
                               elevation_m: float | None = None,
                               flood_exposure: bool | None = None) -> dict:
    """Build a conservative spatial screening summary from explicit evidence."""
    ctx = source_context or {}
    metrics: list[dict] = []
    if road_distance_m is not None:
        metrics.append({"id": "road_access", "value_m": float(road_distance_m), "evidence": "CALCULATED", "status": "CALCULATED"})
    else:
        metrics.append({"id": "road_access", "value_m": None, "evidence": "UNVERIFIED", "status": "REVIEW_REQUIRED"})
    if elevation_m is not None:
        metrics.append({"id": "elevation", "value_m": float(elevation_m), "evidence": "CALCULATED", "status": "CALCULATED"})
    else:
        metrics.append({"id": "elevation", "value_m": None, "evidence": "UNVERIFIED", "status": "REVIEW_REQUIRED"})
    if flood_exposure is not None:
        metrics.append({"id": "flood_exposure", "value": bool(flood_exposure), "evidence": "CALCULATED", "status": "FLAGGED" if flood_exposure else "NO_FLAG"})
    else:
        metrics.append({"id": "flood_exposure", "value": None, "evidence": "UNVERIFIED", "status": "REVIEW_REQUIRED"})

    sources = []
    for source_id, payload in ctx.items():
        if isinstance(payload, dict):
            sources.append({"id": source_id, "status": payload.get("status", "UNKNOWN"), "evidence": _state(payload.get("status"))})
        else:
            sources.append({"id": source_id, "status": "UNKNOWN", "evidence": "UNVERIFIED"})

    review_gaps = [m["id"] for m in metrics if m["status"] == "REVIEW_REQUIRED"]
    return {
        "version": "MASTER-183",
        "metrics": metrics,
        "sources": sources,
        "review_gaps": review_gaps,
        "decision_boundary": "SCREENING_ONLY",
        "statutory_verification": "NOT_CLAIMED",
    }
