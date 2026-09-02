"""Unified planner-facing pre-assessment orchestration for URBION."""
from __future__ import annotations
from typing import Any

def build_preassessment(*, assessment: dict[str, Any]) -> dict[str, Any]:
    a = assessment or {}
    status = str(a.get("final_status", "REQUIRES REVIEW")).upper()
    pv = a.get("planning_value") or {}
    site = a.get("site") or {}
    return {
        "title": "URBION Planning Pre-Assessment",
        "version": "MASTER-111",
        "site": site,
        "planning_decision": status,
        "planning_value": pv,
        "workflow": [
            {"stage": "SITE", "status": "COMPLETE" if site else "EVIDENCE REQUIRED"},
            {"stage": "SPATIAL", "status": "COMPLETE" if a.get("tod_distance_m") is not None else "EVIDENCE REQUIRED"},
            {"stage": "POLICY", "status": "COMPLETE" if a.get("retrieved_rules") else "REVIEW"},
            {"stage": "COMPLIANCE", "status": status},
            {"stage": "SUITABILITY", "status": "AVAILABLE" if a.get("site_analysis") else "EVIDENCE REQUIRED"},
            {"stage": "EVIDENCE", "status": "DISCLOSED"},
            {"stage": "DECISION", "status": status},
        ],
        "decision_trace": a.get("decision_trace", []),
        "evidence_gaps": pv.get("evidence_gaps", []),
        "next_actions": pv.get("next_actions", []),
        "disclaimer": "Planning pre-assessment and decision-support only; not statutory approval or an authority decision.",
    }
