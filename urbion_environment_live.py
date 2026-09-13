"""Live environmental evidence adapter for the canonical URBION packet.

This adapter composes the existing PLANMalaysia DPFDN connector and the
existing evidence-aware environment intelligence without changing planning
rules or treating source context as statutory verification.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from urbion_environment_intelligence import build_environment_intelligence
from urbion_iplan import query_environment_context


def build_live_environment_evidence(
    *,
    latitude: float,
    longitude: float,
    state: str = "Melaka",
    radius_m: float = 1000,
) -> dict[str, Any]:
    queried_at = datetime.now(timezone.utc).isoformat()
    raw = query_environment_context(latitude, longitude, radius_m, state)
    intelligence = build_environment_intelligence(raw)

    layers = raw.get("layers") or {}
    query_errors = [
        key for key, item in layers.items()
        if str((item or {}).get("status") or "").upper() in {"QUERY_UNAVAILABLE", "QUERY_ERROR"}
    ]
    no_feature = [
        key for key, item in layers.items()
        if str((item or {}).get("status") or "").upper() == "NO_FEATURE"
    ]

    intelligence["live_query"] = {
        "provider": raw.get("provider"),
        "state": raw.get("state"),
        "scope": raw.get("scope"),
        "queried_at_utc": queried_at,
        "radius_m": radius_m,
        "layer_count": len(layers),
        "query_error_count": len(query_errors),
        "query_error_layers": query_errors,
        "no_feature_count": len(no_feature),
        "no_feature_layers": no_feature,
        "evidence": "SOURCE_CONTEXT",
        "statutory_verification": "NOT_CLAIMED",
    }
    if query_errors and not (intelligence.get("summary") or {}).get("flagged_count"):
        intelligence["status"] = "QUERY_ERROR"
    return intelligence


__all__ = ["build_live_environment_evidence"]
