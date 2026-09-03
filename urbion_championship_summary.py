"""Compact championship readiness summary for URBION.

This module summarizes existing evidence and review boundaries without inventing
verification. It is presentation/readiness metadata only.
"""
from __future__ import annotations
from typing import Any


def build_championship_summary(*, spatial: dict[str, Any] | None = None, environment: dict[str, Any] | None = None, environment_implications: dict[str, Any] | None = None, agencies: dict[str, Any] | None = None, impacts: dict[str, Any] | None = None, policy: dict[str, Any] | None = None, recommendations: dict[str, Any] | None = None, grounding: dict[str, Any] | None = None, what_if: dict[str, Any] | None = None, km: dict[str, Any] | None = None, review_gaps: list[Any] | None = None) -> dict[str, Any]:
    modules = {
        "SPATIAL": spatial or {},
        "ENVIRONMENT": environment or {},
        "ENVIRONMENT_IMPLICATIONS": environment_implications or {},
        "AGENCIES": agencies or {},
        "IMPACT": impacts or {},
        "POLICY": policy or {},
        "RECOMMENDATION": recommendations or {},
        "RECOMMENDATION_GROUNDING": grounding or {},
        "WHAT_IF": what_if or {},
        "KM_READINESS": km or {},
    }
    gaps = list(dict.fromkeys(str(x) for x in (review_gaps or []) if x))
    rec_items = list((recommendations or {}).get("recommendations", []) or [])
    grounded = int((grounding or {}).get("grounded_count", 0) or 0)
    scenario_items = list((what_if or {}).get("scenarios", []) or [])
    module_status = {}
    for name, payload in modules.items():
        if not payload:
            module_status[name] = "NOT_PROVIDED"
        elif payload.get("review_gaps"):
            module_status[name] = "REVIEW_REQUIRED"
        else:
            module_status[name] = "READY_FOR_REVIEW"
    return {
        "version": "MASTER-250",
        "status": "READY_FOR_PLANNER_REVIEW" if not gaps else "REVIEW_REQUIRED",
        "module_status": module_status,
        "metrics": {
            "review_gap_count": len(gaps),
            "recommendation_count": len(rec_items),
            "grounded_recommendation_count": grounded,
            "scenario_count": len(scenario_items),
        },
        "guardrails": {
            "decision_boundary": "INTEGRATED_LCP_PLANNING_SUPPORT",
            "statutory_verification": "NOT_CLAIMED",
            "authority_decision": "NONE",
        },
        "trace": "MODULES → EVIDENCE → REVIEW GAPS → PLANNER REVIEW",
    }
