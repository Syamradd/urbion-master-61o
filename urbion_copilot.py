"""Unified bounded planner copilot orchestration for URBION HORIZON.

The copilot composes existing deterministic planning services into one
traceable packet. It does not call an LLM, grant statutory approval, or
upgrade source context into verified evidence.
"""
from urbion_knowledge_orchestrator import build_knowledge_pack
from urbion_spatial_intelligence import build_spatial_intelligence
from urbion_impact_intelligence import build_impact_intelligence
from urbion_decision_center import build_decision_center
from urbion_agent_orchestrator import run_agents
from urbion_what_if import execute_what_if
from urbion_scenario_ranking import rank_scenarios
from server import assess_core, AssessmentRequest


def build_copilot_packet(inputs: dict, variants=None, radii=(400, 800), constraints=None, environmental_context=None):
    raw = dict(inputs or {})
    assessment = assess_core(AssessmentRequest(**raw))
    site = assessment["site"]
    spatial = build_spatial_intelligence(
        site["latitude"], site["longitude"], raw.get("tod_lat"), raw.get("tod_lon"),
        tuple(radii or (400, 800)), constraints,
    )
    if environmental_context:
        spatial["environment"] = environmental_context
        spatial["evidence_model"]["environmental_overlay"] = "SOURCE_CONTEXT ONLY"
    knowledge = build_knowledge_pack(
        assessment.get("development_type") or raw.get("development_type") or "",
        site.get("pbt") or raw.get("pbt") or "MBMB",
        spatial,
    )
    impact = build_impact_intelligence(
        spatial=spatial,
        assessment=assessment,
        environmental_context=environmental_context,
    )

    variant_list = variants or []
    if not isinstance(variant_list, list) or len(variant_list) > 12:
        raise ValueError("variants must be a list with at most 12 items")
    if variant_list:
        scenario_intelligence = execute_what_if(
            raw,
            variant_list,
            lambda scenario_inputs: assess_core(AssessmentRequest(**scenario_inputs)),
        )
        scenario_intelligence = rank_scenarios(scenario_intelligence)
        scenario_intelligence["status"] = "COMPLETE"
        scenario_intelligence["count"] = len(scenario_intelligence.get("scenarios", []))
    else:
        scenario_intelligence = {
            "title": "What-If Scenario Comparison",
            "version": "PHASE-D.2",
            "baseline": assessment,
            "baseline_status": assessment.get("final_status", "REQUIRES REVIEW"),
            "baseline_score": (assessment.get("site_analysis", {}) or {}).get("score", 0),
            "scenarios": [],
            "ranked_scenarios": [],
            "best_candidate": None,
            "count": 0,
            "status": "SKIPPED",
            "decision_pathway": ["Supply scenario variants to run a comparative What-If analysis."],
            "disclaimer": "Scenario comparison is decision support only; it does not replace statutory assessment or authority review.",
        }

    decision = build_decision_center(assessment=assessment, scenario_comparison=scenario_intelligence)
    agent_packet = run_agents(
        assessment=assessment,
        spatial=spatial,
        knowledge=knowledge,
        scenarios=scenario_intelligence if scenario_intelligence["count"] else None,
        decision=decision,
    )
    ranked = scenario_intelligence.get("ranked_scenarios", [])
    preferred = ranked[0] if ranked else None
    next_actions = [
        "Review retrieved policy evidence and source traceability.",
        "Validate spatial and environmental context against authoritative sources.",
        "Review impact gaps before relying on any planning recommendation.",
    ]
    if preferred:
        next_actions.insert(0, f"Review ranked scenario {preferred} and verify its evidence before advancing.")
    else:
        next_actions.append("Use What-If scenarios before preparing an LCP handoff.")
    return {
        "mode": "BOUNDED_PLANNER_COPILOT",
        "assessment": assessment,
        "spatial": spatial,
        "knowledge": knowledge,
        "impact": impact,
        "scenario_intelligence": scenario_intelligence,
        "preferred_scenario": preferred,
        "agents": agent_packet,
        "decision": decision,
        "next_actions": next_actions[:5],
        "decision_authority": "NONE",
        "statutory_verification": "NOT_CLAIMED",
        "generation_boundary": "DETERMINISTIC_CONTEXT_ONLY; FUTURE_GENERATION_MUST_PRESERVE_TRACEABILITY",
    }
