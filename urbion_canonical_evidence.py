"""Canonical evidence packet contract for URBION Phase 1.

This module is intentionally pure and additive. It does not call external
services, change deterministic planning calculations, or promote source
context to statutory verification. It provides one stable envelope for the
existing intelligence modules to converge into before the UI is wired to it.
"""
from __future__ import annotations
from typing import Any
from urbion_cadastral_identity import build_cadastral_identity

EVIDENCE_STATES = ("USER_PROVIDED", "CALCULATED", "SOURCE_CONTEXT", "VERIFIED", "UNVERIFIED")
PACKET_VERSION = "PHASE1.2"


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


def _rule_review_gaps(assessment: dict[str, Any]) -> list[str]:
    """Translate untraceable rule provenance into explicit review gaps."""
    gaps: list[str] = []
    for rule in assessment.get("retrieved_rules", []) or []:
        if not isinstance(rule, dict):
            continue
        provenance = rule.get("provenance") or {}
        verification = str(rule.get("verification_status") or provenance.get("verification_status") or "").upper()
        source_status = str(rule.get("source_status") or provenance.get("source_status") or "").upper()
        missing_locator = not any(provenance.get(key) for key in ("page", "clause", "table", "citation_locator"))
        if verification == "REQUIRES_REVIEW" or source_status == "PRIMARY_REFERENCE_PARTIAL" or missing_locator:
            rule_id = rule.get("rule_id") or "UNSPECIFIED_RULE"
            document = provenance.get("document") or rule.get("source_document") or "planning source"
            gaps.append(f"{rule_id}: exact page/clause/table locator and current applicability require review ({document}).")
    return gaps


def build_canonical_evidence_packet(
    *,
    assessment: dict[str, Any] | None = None,
    spatial: dict[str, Any] | None = None,
    environment: dict[str, Any] | None = None,
    stations: dict[str, Any] | None = None,
    development_impact: dict[str, Any] | None = None,
    policy_graph: dict[str, Any] | None = None,
    lcp: dict[str, Any] | None = None,
    cadastral: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create the single evidence envelope used by downstream decision surfaces."""
    assessment = assessment or {}
    site = dict(assessment.get("site") or {})
    evidence_state = dict(assessment.get("evidence_state") or {})
    source_registry = list(assessment.get("source_registry") or [])

    if not isinstance(cadastral, dict):
        cadastral = build_cadastral_identity(
            state=site.get("state"),
            district=site.get("district"),
            mukim=site.get("mukim"),
            lot_no=site.get("lot_no") if site.get("lot_no") not in (None, "Not specified") else None,
            iplan_result=assessment.get("cadastral_query"),
            jupem_verification=assessment.get("jupem_verification"),
        )

    environment_packet = environment or assessment.get("live_environment_evidence") or assessment.get("evidence_intelligence") or {}
    gaps = _gaps(assessment, spatial, environment_packet, stations, development_impact, policy_graph, lcp)
    gaps.extend(_rule_review_gaps(assessment))
    if cadastral.get("project_reference", {}).get("status") == "NOT_PROVIDED":
        gaps.append("Project-reference lot number is not provided; cadastral identity requires explicit project input or authoritative parcel evidence.")
    gaps = list(dict.fromkeys(gaps))

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
        "cadastral_identity": cadastral,
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
            "environment": environment_packet,
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
