"""Single-response championship decision center orchestration for URBION."""
from __future__ import annotations
from typing import Any
from urbion_evidence_contract import contract_summary
from urbion_gis_decision import decision_feature, decision_map_payload
from urbion_multi_source import build_spatial_intelligence


def build_decision_center(*, assessment: dict[str, Any], evidence: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Compose decision, evidence and spatial intelligence without changing statutory outcomes."""
    site = assessment.get("site", {})
    status = assessment.get("final_status", "REQUIRES REVIEW")
    analysis = assessment.get("site_analysis", {})
    feature = decision_feature(latitude=float(site.get("latitude", 0)), longitude=float(site.get("longitude", 0)), status=status, suitability=analysis.get("suitability_score"), lot_no=str(site.get("lot_no", "")), label="URBION Decision Site")
    evidence_items = list(evidence or [])
    evidence_summary = contract_summary(evidence_items) if evidence_items else assessment.get("evidence_intelligence", {})
    spatial = assessment.get("spatial_intelligence")
    if spatial is None:
        spatial = build_spatial_intelligence(
            source_context={
                "iplan": {"status": "LIVE_QUERY"},
                "jupem-mylot": {"status": "PORTAL_REFERENCE"},
                "jps": {"status": "PUBLIC_REAL_TIME_PORTAL"},
                "jmg-mygems": {"status": "LIVE_QUERY"},
                "doe-myeqms": {"status": "PUBLIC_PORTAL"},
            },
            include_domains=True,
        )
    review_gaps = list(assessment.get("review_gaps", []) or [])
    return {
        "project": "URBION HORIZON",
        "version": "PHASE-E.7",
        "decision": {
            "status": status,
            "recommendation": assessment.get("recommendation", {}),
            "confidence": assessment.get("decision_confidence", {}),
            "suitability": analysis.get("suitability_score"),
        },
        "site": site,
        "planning_value": assessment.get("planning_value", {}),
        "evidence": evidence_summary,
        "evidence_state": assessment.get("evidence_state", {}),
        "spatial_intelligence": spatial,
        "decision_trace": assessment.get("decision_trace", []),
        "review_gaps": review_gaps,
        "review_required": bool(review_gaps),
        "map": decision_map_payload([feature]),
        "guardrail": "Decision support only; evidence gaps remain disclosed and no statutory approval is inferred.",
        "decision_boundary": "PLANNER_DECISION_SUPPORT_ONLY",
        "statutory_verification": "NOT_CLAIMED",
    }
