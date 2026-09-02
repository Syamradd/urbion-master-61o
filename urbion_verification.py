"""Evidence-state semantics for URBION spatial and planning decisions.

The engine can calculate a result from user coordinates without claiming that
those coordinates or the resulting context have been independently verified.
This module keeps those states explicit and serialisable for the UI/API.
"""
from __future__ import annotations

EVIDENCE_STATES = {
    "USER_PROVIDED": "Input supplied by the user/project workflow; not independently verified.",
    "CALCULATED": "Derived deterministically by URBION from supplied spatial inputs.",
    "SOURCE_CONTEXT": "Returned by a public/official source endpoint or portal as decision-support context.",
    "SOURCE_CONFIRMED": "Matched against a named source record with sufficient provenance for the stated check.",
    "VERIFIED": "Independently verified against an authoritative current source for the specific decision use.",
    "REFERENCE": "Historical/project/reference material retained for reconciliation only.",
    "UNVERIFIED": "Relevant evidence is missing, stale, ambiguous, or not independently confirmed.",
}


def spatial_evidence(site_input: str = "USER_PROVIDED", calculation: str = "CALCULATED", source: str = "SOURCE_CONTEXT") -> dict:
    """Return a transparent evidence chain without upgrading any status implicitly."""
    return {
        "site_input": site_input,
        "spatial_calculation": calculation,
        "external_source_context": source,
        "verification_state": "VERIFIED" if source == "VERIFIED" else source,
        "decision_language": "VERIFIED" if source == "VERIFIED" else "SCREENED / CALCULATED",
        "upgrade_rule": "Only explicit authoritative-source confirmation may promote SOURCE_CONTEXT or CALCULATED to VERIFIED.",
    }


def rule_evidence(status: str, source_id: str | None = None, source_status: str | None = None) -> dict:
    """Describe rule evidence independently from the compliance outcome."""
    if status == "VERIFIED":
        state = "VERIFIED"
    elif source_status in {"LIVE_ARCGIS_REST", "LIVE_ARCGIS_REST + LIVE_WMS", "SOURCE_CONTEXT"}:
        state = "SOURCE_CONTEXT"
    else:
        state = "UNVERIFIED"
    return {
        "verification_state": state,
        "source_id": source_id,
        "source_status": source_status,
        "decision_safe": state == "VERIFIED",
    }
