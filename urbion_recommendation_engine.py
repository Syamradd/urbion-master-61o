"""Evidence-backed planning recommendation engine for URBION."""
from __future__ import annotations
from typing import Any


def build_recommendations(*, impacts: dict[str, Any] | None = None, policy_graph: dict[str, Any] | None = None) -> dict[str, Any]:
    """Translate traceable impact/policy edges into reviewable recommendations."""
    impacts = impacts or {}
    graph = policy_graph or {}
    links = graph.get("nodes", {}).get("links", []) or []
    recommendations = []
    gaps = list(graph.get("review_gaps", []) or [])
    for link in links:
        if not isinstance(link, dict):
            continue
        impact = link.get("impact") or link.get("issue") or link.get("domain")
        ref = link.get("reference")
        strategy = link.get("strategy")
        if not ref:
            gaps.append("RECOMMENDATION_POLICY_BASIS_REQUIRED")
            continue
        recommendations.append({
            "domain": link.get("domain"), "issue": link.get("issue"),
            "action": strategy or f"Review mitigation for {impact} against the cited planning reference",
            "policy_reference": ref, "clause": link.get("clause"), "sdg": link.get("sdg"),
            "evidence": link.get("evidence", "SOURCE_CONTEXT"), "status": "PLANNER_REVIEW",
        })
    if not recommendations and impacts:
        gaps.append("NO_TRACEABLE_POLICY_RECOMMENDATION")
    return {"version":"MASTER-187","recommendations":recommendations,"review_gaps":list(dict.fromkeys(gaps)),"trace":"IMPACT → POLICY → RECOMMENDATION","decision_boundary":"PLANNING_RECOMMENDATION_SUPPORT","statutory_verification":"NOT_CLAIMED"}
