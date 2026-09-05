"""Single-response championship decision center orchestration for URBION."""
from __future__ import annotations
from typing import Any
from urbion_evidence_contract import contract_summary
from urbion_gis_decision import decision_feature, decision_map_payload
from urbion_multi_source import build_spatial_intelligence


def _score_breakdown(analysis: dict[str, Any]) -> list[dict[str, Any]]:
    """Expose the score as auditable dimensions without inventing missing values."""
    items = list(analysis.get("indicators", []) or [])
    return [
        {"dimension": str(item.get("name", "Unnamed dimension")), "score": item.get("score"), "evidence_state": "SOURCE_CONTEXT" if item.get("score") is not None else "UNVERIFIED"}
        for item in items
    ]


def _next_actions(assessment: dict[str, Any], review_gaps: list[Any], scenario_comparison: dict[str, Any] | None = None) -> list[str]:
    value = assessment.get("planning_value", {}) or {}
    actions = list(value.get("next_actions", []) or [])
    scenario = scenario_comparison or {}
    best = scenario.get("best_candidate")
    if best:
        actions.insert(0, f"Review ranked scenario {best} and verify its evidence before advancing.")
    if actions:
        return actions[:5]
    status = str(assessment.get("final_status", "REQUIRES REVIEW")).upper()
    if status == "NON-COMPLIANCE":
        return ["Review the failed planning control(s).", "Revise the affected proposal parameter(s).", "Re-run the assessment before planner review."]
    if review_gaps:
        return ["Resolve the disclosed evidence gaps.", "Confirm the applicable local planning controls.", "Re-run URBION with verified evidence."]
    return ["Proceed to planner pre-consultation.", "Validate cadastral and technical evidence.", "Re-run if any material proposal parameter changes."]


def build_decision_center(*, assessment: dict[str, Any], evidence: list[dict[str, Any]] | None = None, scenario_comparison: dict[str, Any] | None = None) -> dict[str, Any]:
    """Compose decision, scenario, evidence and spatial intelligence without changing statutory outcomes."""
    site = assessment.get("site", {})
    status = assessment.get("final_status", "REQUIRES REVIEW")
    analysis = assessment.get("site_analysis", {}) or {}
    feature = decision_feature(latitude=float(site.get("latitude", 0)), longitude=float(site.get("longitude", 0)), status=status, suitability=analysis.get("suitability_score", analysis.get("score")), lot_no=str(site.get("lot_no", "")), label="URBION Decision Site")
    evidence_items = list(evidence or [])
    evidence_summary = contract_summary(evidence_items) if evidence_items else assessment.get("evidence_intelligence", {})
    spatial = assessment.get("spatial_intelligence")
    if spatial is None:
        spatial = build_spatial_intelligence(source_context={"iplan":{"status":"LIVE_QUERY"},"jupem-mylot":{"status":"PORTAL_REFERENCE"},"jps":{"status":"PUBLIC_REAL_TIME_PORTAL"},"jmg-mygems":{"status":"LIVE_QUERY"},"doe-myeqms":{"status":"PUBLIC_PORTAL"}}, include_domains=True)
    review_gaps = list(assessment.get("review_gaps", []) or [])
    if not review_gaps:
        review_gaps = list((assessment.get("planning_value", {}) or {}).get("evidence_gaps", []) or [])
    confidence = assessment.get("decision_confidence", {}) or {}
    coverage = evidence_summary.get("total", 0) if isinstance(evidence_summary, dict) else 0
    safe = evidence_summary.get("decision_safe", 0) if isinstance(evidence_summary, dict) else 0
    scenario = scenario_comparison or {"scenarios": [], "ranked_scenarios": [], "best_candidate": None}
    return {
        "project": "URBION HORIZON",
        "version": "PHASE-E.8",
        "decision": {"status": status, "recommendation": assessment.get("recommendation", {}), "confidence": confidence, "suitability": analysis.get("suitability_score", analysis.get("score")), "score_breakdown": _score_breakdown(analysis), "justification": (assessment.get("recommendation", {}) or {}).get("reason", "Decision is derived from the declared planning evidence and rule coverage.")},
        "site": site,
        "planning_value": assessment.get("planning_value", {}),
        "evidence": evidence_summary,
        "evidence_state": assessment.get("evidence_state", {}),
        "evidence_coverage": {"total_items": coverage, "decision_safe_items": safe, "review_required": bool(review_gaps)},
        "spatial_intelligence": spatial,
        "scenario_intelligence": {
            "count": len(scenario.get("scenarios", []) or []),
            "ranked_scenarios": scenario.get("ranked_scenarios", []),
            "best_candidate": scenario.get("best_candidate"),
            "decision_pathway": scenario.get("decision_pathway", []),
            "disclaimer": scenario.get("disclaimer", "Scenario comparison is decision support only; it does not replace statutory assessment or authority review."),
        },
        "decision_trace": assessment.get("decision_trace", []),
        "review_gaps": review_gaps,
        "review_required": bool(review_gaps),
        "next_actions": _next_actions(assessment, review_gaps, scenario),
        "map": decision_map_payload([feature]),
        "guardrail": "Decision support only; evidence gaps remain disclosed and no statutory approval is inferred.",
        "decision_boundary": "PLANNER_DECISION_SUPPORT_ONLY",
        "statutory_verification": "NOT_CLAIMED",
    }
