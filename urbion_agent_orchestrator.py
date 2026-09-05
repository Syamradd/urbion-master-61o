"""Deterministic multi-agent planning orchestrator for URBION HORIZON.

Agents are bounded planning functions, not autonomous statutory authorities.
Each agent consumes explicit evidence and returns a traceable contribution.
"""
from __future__ import annotations
from typing import Any
from urbion_knowledge_orchestrator import build_knowledge_pack
from urbion_impact_intelligence import build_impact_intelligence

AGENTS = ("SITE", "SPATIAL", "POLICY", "COMPLIANCE", "IMPACT", "SCENARIO", "DECISION")

def _result(agent: str, status: str, payload: Any, *, evidence: str = "CALCULATED") -> dict[str, Any]:
    return {"agent": agent, "status": status, "evidence_state": evidence, "output": payload}

def run_agents(*, assessment: dict[str, Any], spatial: dict[str, Any] | None = None,
               scenarios: dict[str, Any] | None = None, decision: dict[str, Any] | None = None) -> dict[str, Any]:
    """Run bounded specialist agents and aggregate a deterministic handoff trace."""
    spatial = spatial or assessment.get("spatial_intelligence") or {}
    knowledge = build_knowledge_pack(
        assessment.get("development_type", ""),
        assessment.get("authority", "MBMB"),
        spatial,
    )
    impact = build_impact_intelligence(spatial=spatial, assessment=assessment)
    outputs = [
        _result("SITE", "COMPLETE", {"site": assessment.get("site"), "development_type": assessment.get("development_type")}, evidence="USER_PROVIDED"),
        _result("SPATIAL", "COMPLETE", spatial, evidence="CALCULATED"),
        _result("POLICY", "COMPLETE" if assessment.get("retrieved_rules") else "REVIEW_REQUIRED", {"rule_count": len(assessment.get("retrieved_rules", []) or []), "coverage": assessment.get("policy_coverage"), "knowledge": knowledge}, evidence="SOURCE_CONTEXT" if assessment.get("retrieved_rules") else "UNVERIFIED"),
        _result("COMPLIANCE", "COMPLETE" if assessment.get("compliance_results") else "REVIEW_REQUIRED", {"results": assessment.get("compliance_results", []), "status": assessment.get("final_status")}, evidence="CALCULATED"),
        _result("IMPACT", impact["status"], impact, evidence=impact["evidence_state"]),
        _result("SCENARIO", "COMPLETE" if scenarios else "READY", scenarios or {"message": "Scenario inputs not supplied."}, evidence="CALCULATED" if scenarios else "UNVERIFIED"),
        _result("DECISION", "COMPLETE" if decision else "READY", decision or {"message": "Decision centre output not supplied."}, evidence="CALCULATED" if decision else "UNVERIFIED"),
    ]
    review = [x["agent"] for x in outputs if x["status"] == "REVIEW_REQUIRED"]
    return {"version": "PHASE-E.8", "mode": "BOUNDED_MULTI_AGENT", "agents": outputs, "agent_order": list(AGENTS), "review_required": review, "decision_authority": "NONE", "statutory_verification": "NOT_CLAIMED", "guardrail": "Agents provide decision-support contributions only; no agent grants statutory approval."}
