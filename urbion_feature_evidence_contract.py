"""Conservative map-feature -> evidence handoff contract for URBION HORIZON."""
from __future__ import annotations

from typing import Any


ALLOWED_EVIDENCE_STATES = {"SOURCE_CONTEXT", "EVIDENCE_GAP", "REVIEW"}


def feature_evidence(feature: dict[str, Any]) -> dict[str, Any]:
    """Normalize an identified feature without upgrading it to decision-safe evidence."""
    evidence_state = str(feature.get("evidence_state") or "REVIEW").upper()
    if evidence_state not in ALLOWED_EVIDENCE_STATES:
        raise ValueError(f"unsupported evidence state: {evidence_state}")
    source = feature.get("source")
    query_status = str(feature.get("query_status") or "UNKNOWN").upper()
    eligible = bool(source) and query_status == "LIVE_QUERY" and evidence_state == "SOURCE_CONTEXT"
    return {
        "layer_id": feature.get("layer_id"),
        "feature_id": feature.get("feature_id"),
        "layer_name": feature.get("layer_name"),
        "source": source,
        "query_status": query_status,
        "evidence_state": evidence_state,
        "eligible_for_rule_binding": eligible,
        "decision_safe": False,
        "rule_binding_required": True,
        "statutory_approval_claim": False,
    }
