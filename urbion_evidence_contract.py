"""Canonical evidence contract for URBION Phase E."""
from __future__ import annotations
from typing import Any

SAFE_STATES = {"AVAILABLE", "VERIFIED", "REFERENCE_REGISTERED"}
DISCLOSED_GAP_STATES = {"PLANNED", "QUERY_UNAVAILABLE", "DISCOVERY_COMPLETE", "NO_EVIDENCE"}

def build_evidence(*, source: str, layer: str, location: dict[str, Any] | None = None, value: Any = None, evidence_type: str = "UNKNOWN", confidence: str = "MEDIUM", timestamp: str | None = None, source_reference: str | None = None, status: str = "AVAILABLE") -> dict[str, Any]:
    state = str(status or "AVAILABLE").upper()
    if state not in SAFE_STATES | DISCLOSED_GAP_STATES:
        state = "NO_EVIDENCE"
    return {"source": source, "layer": layer, "location": location or {}, "value": value, "evidence_type": evidence_type, "confidence": confidence, "timestamp": timestamp, "source_reference": source_reference, "status": state, "decision_safe": state in SAFE_STATES}

def contract_summary(evidence: list[dict[str, Any]]) -> dict[str, Any]:
    items = list(evidence or [])
    counts = {state: 0 for state in sorted(SAFE_STATES | DISCLOSED_GAP_STATES)}
    for item in items:
        state = str(item.get("status", "NO_EVIDENCE")).upper()
        counts[state] = counts.get(state, 0) + 1
    safe = [item for item in items if item.get("decision_safe") is True]
    gaps = [item for item in items if item.get("decision_safe") is not True]
    return {"total": len(items), "decision_safe": len(safe), "disclosed_gaps": len(gaps), "status_counts": counts, "evidence": items, "safe_for_decision": bool(items) and len(gaps) == 0, "version": "PHASE-E.1"}
