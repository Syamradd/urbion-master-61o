"""Deterministic contract for turning queried map features into usable evidence.

This module is intentionally dependency-light and side-effect free. It does not
fetch data or decide statutory compliance. It normalises a live GIS feature into
an identify payload that the map UI can safely render and optionally hand to the
evidence/assessment layer.
"""
from __future__ import annotations

from typing import Any

IDENTIFY_EVIDENCE_STATES = {"SOURCE_CONTEXT", "EVIDENCE_GAP", "REVIEW"}
IDENTIFY_QUERY_STATES = {"LIVE_QUERY", "NO_FEATURE", "QUERY_ERROR", "NOT_CONFIGURED"}


def feature_identity(feature: dict[str, Any], *, layer_id: str, source: str) -> dict[str, Any]:
    """Return a stable, compact identity record for one GeoJSON-like feature."""
    properties = feature.get("properties") or feature.get("attributes") or {}
    geometry = feature.get("geometry") or {}
    raw_id = feature.get("id") or properties.get("id") or properties.get("OBJECTID")
    if raw_id is None:
        raw_id = properties.get("objectid") or properties.get("fid")
    return {
        "layer_id": str(layer_id),
        "feature_id": str(raw_id) if raw_id is not None else None,
        "source": str(source),
        "geometry_type": geometry.get("type"),
    }


def identify_payload(
    *,
    layer: dict[str, Any],
    feature: dict[str, Any],
    query_status: str = "LIVE_QUERY",
    evidence_state: str = "SOURCE_CONTEXT",
) -> dict[str, Any]:
    """Build the canonical map-identify payload without asserting compliance."""
    query_status = str(query_status).upper()
    evidence_state = str(evidence_state).upper()
    if query_status not in IDENTIFY_QUERY_STATES:
        raise ValueError(f"unsupported query status: {query_status}")
    if evidence_state not in IDENTIFY_EVIDENCE_STATES:
        raise ValueError(f"unsupported evidence state: {evidence_state}")

    identity = feature_identity(
        feature,
        layer_id=str(layer.get("id", "unknown")),
        source=str(layer.get("source", "unknown")),
    )
    properties = feature.get("properties") or feature.get("attributes") or {}
    selected = {
        str(key): value
        for key, value in properties.items()
        if value not in (None, "") and isinstance(value, (str, int, float, bool))
    }

    return {
        **identity,
        "layer_name": layer.get("name") or layer.get("name_ms") or identity["layer_id"],
        "group": layer.get("group", "UNKNOWN"),
        "query_status": query_status,
        "evidence_state": evidence_state,
        "decision_safe": False,
        "properties": selected,
        "use_as_evidence": {
            "available": query_status == "LIVE_QUERY" and evidence_state == "SOURCE_CONTEXT",
            "requires_rule_binding": True,
        },
    }


def evidence_handoff(payload: dict[str, Any]) -> dict[str, Any]:
    """Create a conservative handoff from map identify to evidence binding."""
    return {
        "layer_id": payload.get("layer_id"),
        "feature_id": payload.get("feature_id"),
        "source": payload.get("source"),
        "evidence_state": payload.get("evidence_state"),
        "decision_safe": False,
        "rule_binding_required": True,
        "statutory_approval_claim": False,
    }
