"""Kebenaran Merancang / OSC 3.0 Plus workflow intelligence.

This module models process readiness, not approval. It deliberately avoids
inventing PBT-specific approval rules where the verified rule set is absent.
"""
from __future__ import annotations

KM_CATEGORIES = ("KECIL", "SEDERHANA", "BESAR")
DEFAULT_TECHNICAL_AGENCIES = (
    "Jabatan Perancang", "Jabatan Kejuruteraan", "JAS", "JPS", "JKR", "IWK",
    "TNB", "SAMB", "JMG", "SKMM", "BOMBA", "PTG", "PTD"
)


def build_km_readiness(
    *,
    pbt: str,
    development_type: str,
    documents: list[str] | None = None,
    km_category: str | None = None,
    technical_reviews: dict[str, str] | None = None,
) -> dict:
    """Return a transparent OSC/KM readiness checklist."""
    docs = {str(x).strip().lower() for x in (documents or []) if str(x).strip()}
    reviews = technical_reviews or {}
    category = km_category.upper() if km_category else None
    category_valid = category in KM_CATEGORIES if category else False
    required_core = {"location plan", "site plan", "development proposal report"}
    missing = sorted(required_core - docs)
    review_states = {agency: reviews.get(agency, "NOT_CHECKED") for agency in DEFAULT_TECHNICAL_AGENCIES}
    checked = [v for v in review_states.values() if v != "NOT_CHECKED"]
    blockers = []
    if not category_valid:
        blockers.append("KM category not explicitly classified")
    if missing:
        blockers.append("Core submission evidence missing")
    if any(v in {"OBJECTION", "REQUIRES REVISION"} for v in checked):
        blockers.append("Technical review requires resolution")
    return {
        "pbt": pbt,
        "development_type": development_type,
        "km_category": category,
        "km_category_state": "EXPLICIT" if category_valid else "REQUIRES_REVIEW",
        "core_document_check": {"missing": missing, "state": "READY" if not missing else "INCOMPLETE"},
        "technical_review": review_states,
        "blockers": blockers,
        "readiness": "READY_FOR_WORKFLOW_REVIEW" if not blockers else "REQUIRES_REVIEW",
        "decision_boundary": "KM/OSC readiness support only; URBION does not grant or predict statutory approval.",
        "workflow_basis": "OSC 3.0 Plus categories and submission/review workflow; PBT-specific checklist must be confirmed with the relevant PBT.",
    }
