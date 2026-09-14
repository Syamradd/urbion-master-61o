"""Unified bounded planner copilot orchestration for URBION HORIZON.

The copilot composes existing deterministic planning services into one
traceable packet. It does not call an LLM, grant statutory approval, or
upgrade source context into verified evidence.
"""
import server
from urbion_knowledge_orchestrator import build_knowledge_pack
from urbion_spatial_intelligence import build_spatial_intelligence
from urbion_impact_intelligence import build_impact_intelligence
from urbion_decision_center import build_decision_center
from urbion_agent_orchestrator import run_agents
from urbion_what_if import execute_what_if
from urbion_scenario_ranking import rank_scenarios
from urbion_evidence_ledger import build_evidence_ledger
from urbion_evidence_quality import build_evidence_quality
from server import AssessmentRequest
from urbion_network_intelligence import network_distance_m
from urbion_canonical_evidence import build_canonical_evidence_packet


def _enrich_canonical_packet(packet: dict, *, spatial: dict, knowledge: dict, impact: dict, scenarios: dict, decision: dict, evidence_ledger: dict, evidence_quality: dict) -> dict:
    """Attach deterministic downstream intelligence to the one canonical packet."""
    packet = dict(packet or {})
    evidence = dict(packet.get("evidence") or {})
    evidence.update({
        "spatial": spatial or {},
        "development_impact": impact or {},
        "policy_graph": knowledge.get("policy_graph") if isinstance(knowledge, dict) else {},
    })
    packet["evidence"] = evidence
    packet["knowledge"] = knowledge or {}
    packet["what_if"] = scenarios or {}
    packet["decision_center"] = decision or {}
    packet["evidence_ledger"] = evidence_ledger or {}
    packet["evidence_quality"] = evidence_quality or {}
    packet["review_gaps"] = list(dict.fromkeys(list(packet.get("review_gaps", []) or []) + list((impact or {}).get("review_gaps", []) or []) + list((scenarios or {}).get("review_gaps", []) or []) + list((decision or {}).get("review_gaps", []) or [])))
    packet["trace"] = "SITE → SPATIAL → POLICY → ENVIRONMENT/IMPACT → WHAT-IF → DECISION → REVIEW"
    packet["convergence"] = {"status": "CANONICAL", "downstream_modules": ["SPATIAL", "KNOWLEDGE", "IMPACT", "WHAT_IF", "DECISION", "EVIDENCE_LEDGER", "EVIDENCE_QUALITY"]}
    packet["statutory_verification"] = "NOT_CLAIMED"
    return packet


def build_copilot_packet(inputs: dict, variants=None, radii=(400, 800), constraints=None,
                         environmental_context=None, canonical_evidence_packet=None):
    raw = dict(inputs or {})
    assessment = server.assess_core(AssessmentRequest(**raw))
    site = assessment["site"]
    canonical_packet = canonical_evidence_packet if isinstance(canonical_evidence_packet, dict) else build_canonical_evidence_packet(
        assessment=assessment,
        spatial=assessment.get("site_analysis"),
        environment=assessment.get("evidence_intelligence"),
        policy_graph={"policy_coverage": assessment.get("policy_coverage")},
    )
    spatial = build_spatial_intelligence(site["latitude"], site["longitude"], raw.get("tod_lat"), raw.get("tod_lon"), tuple(radii or (400, 800)), constraints, environmental_context)
    if environmental_context:
        spatial["environment"] = environmental_context
        spatial["evidence_model"]["environmental_overlay"] = "SOURCE_CONTEXT ONLY"
    network_target = raw.get("network_target_lat"), raw.get("network_target_lon")
    if all(value is not None for value in network_target):
        spatial["network_access"] = network_distance_m(site["latitude"], site["longitude"], float(network_target[0]), float(network_target[1]))
        spatial["evidence_model"]["network_access"] = spatial["network_access"].get("evidence_state", "UNVERIFIED")
    knowledge = build_knowledge_pack(assessment.get("development_type") or raw.get("development_type") or "", site.get("pbt") or raw.get("pbt") or "MBMB", spatial)
    impact = build_impact_intelligence(spatial=spatial, assessment=assessment, environmental_context=environmental_context)
    variant_list = variants or []
    if not isinstance(variant_list, list) or len(variant_list) > 12:
        raise ValueError("variants must be a list with at most 12 items")
    if variant_list:
        scenario_intelligence = execute_what_if(raw, variant_list, lambda scenario_inputs: server.assess_core(AssessmentRequest(**scenario_inputs)))
        scenario_intelligence = rank_scenarios(scenario_intelligence)
        scenario_intelligence["status"] = "COMPLETE"
        scenario_intelligence["count"] = len(scenario_intelligence.get("scenarios", []))
    else:
        scenario_intelligence = {
            "title": "What-If Scenario Comparison", "version": "PHASE-D.2", "baseline": assessment,
            "baseline_status": assessment.get("final_status", "REQUIRES REVIEW"),
            "baseline_score": (assessment.get("site_analysis", {}) or {}).get("score", 0),
            "scenarios": [], "ranked_scenarios": [], "best_candidate": None, "count": 0,
            "status": "SKIPPED", "decision_pathway": ["Supply scenario variants to run a comparative What-If analysis."],
            "disclaimer": "Scenario comparison is decision support only; it does not replace statutory assessment or authority review.",
        }
    decision = build_decision_center(assessment=assessment, scenario_comparison=scenario_intelligence)
    agent_packet = run_agents(assessment=assessment, spatial=spatial, knowledge=knowledge, scenarios=scenario_intelligence if scenario_intelligence["count"] else None, decision=decision)
    ranked = scenario_intelligence.get("ranked_scenarios", [])
    preferred = ranked[0] if ranked else None
    evidence_ledger = build_evidence_ledger(assessment=assessment, spatial=spatial, knowledge=knowledge, impact=impact, scenarios=scenario_intelligence, decision=decision)
    evidence_quality = build_evidence_quality(evidence_ledger)
    canonical_packet = _enrich_canonical_packet(canonical_packet, spatial=spatial, knowledge=knowledge, impact=impact, scenarios=scenario_intelligence, decision=decision, evidence_ledger=evidence_ledger, evidence_quality=evidence_quality)
    next_actions = [
        "Review retrieved policy evidence and source traceability.",
        "Validate spatial and environmental context against authoritative sources.",
        "Review impact gaps before relying on any planning recommendation.",
    ]
    if preferred:
        next_actions.insert(0, f"Review ranked scenario {preferred} and verify its evidence before advancing.")
    else:
        next_actions.append("Use What-If scenarios before preparing an LCP handoff.")
    explanation = {
        "source": "CANONICAL_EVIDENCE_PACKET",
        "status": canonical_packet.get("assessment", {}).get("final_status"),
        "review_gaps": list(canonical_packet.get("review_gaps", [])),
        "statutory_verification": canonical_packet.get("statutory_verification", "NOT_CLAIMED"),
        "instruction": "Explain only what is present in the canonical evidence packet; do not invent rules, approvals, scores, or verified status.",
    }
    return {
        "mode": "BOUNDED_PLANNER_COPILOT", "assessment": assessment, "spatial": spatial, "knowledge": knowledge,
        "impact": impact, "scenario_intelligence": scenario_intelligence, "preferred_scenario": preferred,
        "agents": agent_packet, "decision": decision, "evidence_ledger": evidence_ledger,
        "evidence_quality": evidence_quality, "canonical_evidence_packet": canonical_packet,
        "explanation": explanation,
        "next_actions": next_actions[:5], "decision_authority": "NONE", "statutory_verification": "NOT_CLAIMED",
        "generation_boundary": "CANONICAL_PACKET_ONLY; DETERMINISTIC_CONTEXT_ONLY; FUTURE_GENERATION_MUST_PRESERVE_TRACEABILITY",
    }
