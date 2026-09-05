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
from server import assess_core, AssessmentRequest


def build_copilot_packet(inputs: dict, variants=None, radii=(400, 800), constraints=None):
    raw = dict(inputs or {})
    assessment = assess_core(AssessmentRequest(**raw))
    site = assessment["site"]
    spatial = build_spatial_intelligence(
        site["latitude"], site["longitude"], raw.get("tod_lat"), raw.get("tod_lon"),
        tuple(radii or (400, 800)), constraints,
    )
    knowledge = build_knowledge_pack(
        assessment.get("development_type") or raw.get("development_type") or "",
        site.get("pbt") or raw.get("pbt") or "MBMB",
        spatial,
    )
    impact = build_impact_intelligence(spatial=spatial, assessment=assessment)
    decision = build_decision_center(assessment=assessment)
    agent_packet = run_agents(
        assessment=assessment,
        spatial=spatial,
        scenarios=None,
        decision=decision,
    )
    return {
        "mode": "BOUNDED_PLANNER_COPILOT",
        "assessment": assessment,
        "spatial": spatial,
        "knowledge": knowledge,
        "impact": impact,
        "agents": agent_packet,
        "decision": decision,
        "next_actions": [
            "Review retrieved policy evidence and source traceability.",
            "Validate spatial and environmental context against authoritative sources.",
            "Review impact gaps before relying on any planning recommendation.",
            "Use What-If scenarios before preparing an LCP handoff.",
        ],
        "decision_authority": "NONE",
        "statutory_verification": "NOT_CLAIMED",
        "generation_boundary": "DETERMINISTIC_CONTEXT_ONLY; FUTURE_GENERATION_MUST_PRESERVE_TRACEABILITY",
    }
