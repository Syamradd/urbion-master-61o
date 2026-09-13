"""Canonical evidence packet contract for URBION Phase 1.

This module is intentionally pure and additive. It does not call external
services, change deterministic planning calculations, or promote source
context to statutory verification. It provides one stable envelope for the
existing intelligence modules to converge into before the UI is wired to it.
"""
from __future__ import annotations
from typing import Any

EVIDENCE_STATES = ("USER_PROVIDED", "CALCULATED", "SOURCE_CONTEXT", "VERIFIED", "UNVERIFIED")
PACKET_VERSION = "PHASE1.1"


def _state(value: Any) -> str:
    text = str(value or "UNVERIFIED").upper()
    return text if text in EVIDENCE_STATES else "UNVERIFIED"


def _gaps(*sections: dict[str, Any] | None) -> list[str]:
    values: list[str] = []
    for section in sections:
        if not isinstance(section, dict):
            continue
        raw = section.get("review_gaps") or []
        if isinstance(raw, list):
            values.extend(str(x) for x in raw if x)
    return list(dict.fromkeys(values))


def build_canonical_evidence_packet(
    *,
    assessment: dict[str, Any] | None = None,
    spatial: dict[str, Any] | None = None,
    environment: dict[str, Any] | None = None,
    stations: dict[str, Any] | None = None,
    development_impact: dict[str, Any] | None = None,
    policy_graph: dict[str, Any] | None = None,
    lcp: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create the single evidence envelope used by downstream decision surfaces."""
    assessment = assessment or {}
    site = dict(assessment.get("site") or {})
    evidence_state = dict(assessment.get("evidence_state") or {})
    source_registry = list(assessment.get("source_registry") or [])

    gaps = _gaps(assessment, spatial, environment, stations, development_impact, policy_graph, lcp)

    return {
        "version": PACKET_VERSION,
        "project": assessment.get("project", "URBION"),
        "site": site,
        "identity": {
            "state": site.get("state"),
            "district": site.get("district"),
            "pbt": site.get("pbt"),
            "lot_no": site.get("lot_no"),
            "identity_evidence": _state(evidence_state.get("site_coordinates", "USER_PROVIDED")),
            "statutory_verification": "NOT_CLAIMED",
        },
        "assessment": {
            "final_status": assessment.get("final_status"),
            "classification": assessment.get("classification"),
            "decision_confidence": assessment.get("decision_confidence"),
            "recommendation": assessment.get("recommendation"),
            "policy_coverage": assessment.get("policy_coverage"),
            "retrieved_rules": assessment.get("retrieved_rules", []),
            "applicability_results": assessment.get("applicability_results", []),
            "compliance_results": assessment.get("compliance_results", []),
        },
        "evidence": {
            "spatial": spatial or {},
            "environment": environment or {},
            "stations": stations or {},
            "development_impact": development_impact or {},
            "policy_graph": policy_graph or {},
            "lcp": lcp or {},
            "source_registry": source_registry,
        },
        "evidence_states": evidence_state,
        "review_gaps": gaps,
        "trace": assessment.get("decision_trace") or "SITE → SPATIAL → POLICY → EVIDENCE → DECISION",
        "decision_boundary": "INTEGRATED_PLANNING_DECISION_SUPPORT",
        "statutory_verification": "NOT_CLAIMED",
    }


__all__ = ["EVIDENCE_STATES", "PACKET_VERSION", "build_canonical_evidence_packet"]
