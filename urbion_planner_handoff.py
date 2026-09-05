"""Deterministic planner handoff packet for URBION's bounded decision workflow."""
from __future__ import annotations

from typing import Any, Callable


def build_planner_handoff(
    assessment: dict[str, Any],
    spatial: dict[str, Any] | None = None,
    knowledge: dict[str, Any] | None = None,
    impact: dict[str, Any] | None = None,
    scenarios: dict[str, Any] | None = None,
    decision: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a review-ready handoff without claiming statutory approval."""
    spatial = spatial or {}
    knowledge = knowledge or {}
    impact = impact or {}
    decision = decision or {}
    scenario_payload = scenarios or {}

    review_items: list[str] = []
    evidence = assessment.get("evidence") or {}
    if evidence.get("review_gaps"):
        review_items.extend(str(x) for x in evidence["review_gaps"])
    if spatial.get("review_gaps"):
        review_items.extend(str(x) for x in spatial["review_gaps"])
    if impact.get("status") == "REVIEW_REQUIRED":
        review_items.append("IMPACT_REVIEW_REQUIRED")
    if knowledge.get("review_gaps"):
        review_items.extend(str(x) for x in knowledge["review_gaps"])

    actions = list(decision.get("priority_actions") or decision.get("next_actions") or [])
    if not actions:
        actions = ["Review evidence and applicable planning requirements before authority submission."]

    preferred = scenario_payload.get("preferred_scenario") or scenario_payload.get("recommended_scenario")
    if preferred:
        actions.insert(0, f"Review preferred scenario: {preferred}.")

    return {
        "workflow": ["ASSESSMENT", "SPATIAL", "KNOWLEDGE", "IMPACT", "SCENARIO", "DECISION", "HANDOFF"],
        "handoff_status": "REVIEW_REQUIRED" if review_items else "READY_FOR_PLANNER_REVIEW",
        "review_items": list(dict.fromkeys(review_items)),
        "priority_actions": actions[:8],
        "decision": decision,
        "scenario_summary": {
            "executed": len(scenario_payload.get("ranked") or scenario_payload.get("scenarios") or []),
            "preferred": preferred,
        },
        "evidence_summary": {
            "assessment": evidence.get("state") or "UNVERIFIED",
            "spatial": spatial.get("evidence_model", {}).get("state") or "UNVERIFIED",
            "knowledge": knowledge.get("evidence_model", {}).get("state") or knowledge.get("evidence_state") or "UNVERIFIED",
            "impact": impact.get("evidence_state") or "UNVERIFIED",
        },
        "decision_authority": "NONE",
        "statutory_verification": "NOT_CLAIMED",
        "boundary": "Planner handoff and decision support only; authority determination remains with the relevant approving agency.",
    }


def build_planner_handoff_from_copilot(
    inputs: dict[str, Any],
    copilot_fn: Callable[..., dict[str, Any]],
) -> dict[str, Any]:
    """Run the production copilot once, then convert its packet to a handoff."""
    packet = copilot_fn(inputs)
    return {
        "project": "URBION HORIZON",
        "mode": "BOUNDED_PLANNER_COPILOT",
        "copilot": packet,
        "handoff": build_planner_handoff(
            assessment=packet.get("assessment") or {},
            spatial=packet.get("spatial") or {},
            knowledge=packet.get("knowledge") or {},
            impact=packet.get("impact") or {},
            scenarios=packet.get("scenario_intelligence") or {},
            decision=packet.get("decision") or {},
        ),
    }
