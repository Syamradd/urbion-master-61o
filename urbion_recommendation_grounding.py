"""Evidence-grounded recommendation gate for integrated planning support."""
from __future__ import annotations
from typing import Any


def build_recommendation_grounding(*, recommendations: dict[str, Any] | None = None, environment_implications: dict[str, Any] | None = None, impacts: dict[str, Any] | None = None, policy_graph: dict[str, Any] | None = None) -> dict[str, Any]:
    recommendations = recommendations or {}
    environment_implications = environment_implications or {}
    impacts = impacts or {}
    policy_graph = policy_graph or {}
    recs = recommendations.get("recommendations", []) or []
    grounded = []
    for rec in recs:
        if not isinstance(rec, dict):
            continue
        refs = []
        if rec.get("policy_reference"):
            refs.append({"type": "POLICY", "reference": rec["policy_reference"]})
        if environment_implications.get("implications"):
            refs.append({"type": "ENVIRONMENT", "count": len(environment_implications["implications"])})
        if impacts.get("impacts"):
            refs.append({"type": "IMPACT", "count": len(impacts["impacts"])})
        grounded.append({"recommendation": rec, "evidence_refs": refs, "grounded": bool(refs), "status": "PLANNER_REVIEW" if refs else "REVIEW_REQUIRED"})
    if not grounded:
        gaps = ["NO_TRACEABLE_RECOMMENDATION"]
    else:
        gaps = ["RECOMMENDATION_LACKS_TRACEABLE_EVIDENCE"] if any(not x["grounded"] for x in grounded) else []
    return {"version": "MASTER-234", "items": grounded, "count": len(grounded), "grounded_count": sum(x["grounded"] for x in grounded), "review_gaps": gaps, "trace": "EVIDENCE → IMPACT/POLICY → RECOMMENDATION → PLANNER REVIEW", "decision_boundary": "PLANNING_RECOMMENDATION_SUPPORT", "statutory_verification": "NOT_CLAIMED"}
