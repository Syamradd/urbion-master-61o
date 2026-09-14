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
    canonical_packet: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a review-ready handoff from the canonical packet without claiming statutory approval."""
    packet = canonical_packet if isinstance(canonical_packet, dict) else {}
    evidence = packet.get("evidence") or {}
    assessment = packet.get("assessment") or assessment or {}
    spatial = evidence.get("spatial") or spatial or {}
    knowledge = packet.get("knowledge") or knowledge or {}
    impact = evidence.get("development_impact") or impact or {}
    scenario_payload = packet.get("what_if") or scenarios or {}
    decision = packet.get("decision_center") or decision or {}

    review_items: list[str] = []
    if packet.get("review_gaps"):
        review_items.extend(str(x) for x in packet["review_gaps"])
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
    if not preferred:
        preferred = packet.get("preferred_scenario")
    if preferred:
        preferred_label = (preferred.get("id") or preferred.get("name")) if isinstance(preferred, dict) else preferred
        actions.insert(0, f"Review preferred scenario: {preferred_label}.")

    executed = scenario_payload.get("ranked_scenarios") or scenario_payload.get("scenarios") or []
    evidence_states = packet.get("evidence_states") or {}

    return {
        "workflow": ["ASSESSMENT", "SPATIAL", "KNOWLEDGE", "IMPACT", "SCENARIO", "DECISION", "PLANNER_REVIEW", "KM_READINESS", "OSC", "HANDOFF"],
        "handoff_status": "REVIEW_REQUIRED" if review_items else "READY_FOR_PLANNER_REVIEW",
        "review_items": list(dict.fromkeys(review_items)),
        "priority_actions": actions[:8],
        "decision": decision,
        "scenario_summary": {"executed": len(executed), "preferred": preferred},
        "evidence_summary": {
            "assessment": evidence_states.get("assessment") or packet.get("evidence_state") or "UNVERIFIED",
            "spatial": evidence_states.get("spatial") or "UNVERIFIED",
            "knowledge": evidence_states.get("knowledge") or "UNVERIFIED",
            "impact": evidence_states.get("development_impact") or "UNVERIFIED",
        },
        "canonical_convergence": packet.get("convergence") or {"status": "UNKNOWN"},
        "statutory_verification": packet.get("statutory_verification", "NOT_CLAIMED"),
        "decision_authority": packet.get("decision_authority", "NONE"),
        "boundary": "Planner handoff and decision support only; authority determination remains with the relevant approving agency.",
    }


def build_planner_handoff_from_copilot(
    inputs: dict[str, Any],
    copilot_fn: Callable[..., dict[str, Any]],
) -> dict[str, Any]:
    """Run the production copilot once, then convert its canonical packet to a handoff."""
    packet = copilot_fn(inputs)
    canonical_packet = packet.get("canonical_evidence_packet") or {}
    return {
        "project": "URBION HORIZON",
        "mode": "BOUNDED_PLANNER_COPILOT",
        "copilot": packet,
        "canonical_evidence_packet": canonical_packet,
        "handoff": build_planner_handoff(
            assessment=packet.get("assessment") or {},
            spatial=packet.get("spatial") or {},
            knowledge=packet.get("knowledge") or {},
            impact=packet.get("impact") or {},
            scenarios=packet.get("scenario_intelligence") or {},
            decision=packet.get("decision") or {},
            canonical_packet=canonical_packet,
        ),
    }
