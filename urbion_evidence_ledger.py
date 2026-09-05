"""Deterministic evidence ledger for URBION planner review.

The ledger normalizes major decision inputs into explicit evidence states.
It never upgrades source context or user-provided data into verification.
"""
from __future__ import annotations
from typing import Any

EVIDENCE_STATES = ("USER_PROVIDED", "CALCULATED", "SOURCE_CONTEXT", "VERIFIED", "UNVERIFIED")


def _item(item_id: str, domain: str, label: str, state: str, detail: Any = None, action: str | None = None) -> dict[str, Any]:
    if state not in EVIDENCE_STATES:
        state = "UNVERIFIED"
    return {"id": item_id, "domain": domain, "label": label, "evidence_state": state, "detail": detail, "review_action": action}


def build_evidence_ledger(*, assessment: dict | None = None, spatial: dict | None = None,
                          knowledge: dict | None = None, impact: dict | None = None,
                          scenarios: dict | None = None, decision: dict | None = None) -> dict[str, Any]:
    assessment = assessment or {}
    spatial = spatial or {}
    knowledge = knowledge or {}
    impact = impact or {}
    scenarios = scenarios or {}
    decision = decision or {}
    evidence = assessment.get("evidence_state", {}) or {}
    items = [
        _item("SITE-COORD", "site", "Site coordinates", evidence.get("site_coordinates", "UNVERIFIED"), (assessment.get("site") or {}).get("latitude"), "Confirm parcel location against authoritative cadastral/PBT evidence."),
        _item("TOD-DIST", "spatial", "TOD distance", evidence.get("tod_distance", "CALCULATED"), assessment.get("tod_distance_m"), "Confirm the relevant station/transport feature and measurement basis."),
        _item("POLICY", "policy", "Planning rule evidence", evidence.get("planning_rules", "UNVERIFIED"), len(assessment.get("retrieved_rules", []) or []), "Confirm current applicable local-plan rule set."),
        _item("FINAL", "decision", "Assessment outcome", evidence.get("final_decision", "CALCULATED"), assessment.get("final_status"), "Planner review remains required before relying on the outcome."),
    ]
    spatial_model = spatial.get("evidence_model", {}) or {}
    for key, value in spatial_model.items():
        state = "SOURCE_CONTEXT" if value and str(value).upper() in {"SOURCE_CONTEXT", "SOURCE_CONTEXT ONLY"} else "CALCULATED"
        items.append(_item(f"SPATIAL-{str(key).upper()}", "spatial", str(key), state, value, "Verify source currency and applicability."))
    knowledge_state = knowledge.get("evidence_state") or ("SOURCE_CONTEXT" if knowledge.get("retrieval_count") else "UNVERIFIED")
    items.append(_item("KNOWLEDGE", "policy", "Knowledge retrieval", knowledge_state, knowledge.get("retrieval_count"), "Inspect retrieved rule trace before decision use."))
    impact_state = impact.get("evidence_state", "UNVERIFIED")
    items.append(_item("IMPACT", "impact", "Impact intelligence", impact_state, impact.get("signal_count"), "Review environmental/social/mobility gaps and supporting evidence."))
    if scenarios.get("count"):
        items.append(_item("SCENARIO", "scenario", "What-If comparison", "CALCULATED", scenarios.get("count"), "Verify each ranked scenario before advancing."))
    else:
        items.append(_item("SCENARIO", "scenario", "What-If comparison", "UNVERIFIED", 0, "Run scenario variants when proposal alternatives need comparison."))
    decision_status = (decision.get("decision") or {}).get("status") or decision.get("status")
    items.append(_item("DECISION", "decision", "Decision center", "CALCULATED", decision_status, "Treat as planner decision support only."))
    counts = {state: sum(1 for item in items if item["evidence_state"] == state) for state in EVIDENCE_STATES}
    review_required = sum(1 for item in items if item["evidence_state"] in {"UNVERIFIED", "SOURCE_CONTEXT", "USER_PROVIDED"})
    return {"version": "PHASE-E.8", "items": items, "counts": counts, "total_items": len(items), "review_required_items": review_required, "verification_boundary": "SOURCE_CONTEXT and USER_PROVIDED items require planner/agency verification; no statutory verification is inferred.", "decision_authority": "NONE", "statutory_verification": "NOT_CLAIMED"}
