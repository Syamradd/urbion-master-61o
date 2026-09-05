"""Deterministic one-call championship demo packet for judge presentation."""
from __future__ import annotations
from typing import Any, Callable


def build_judge_demo(inputs: dict[str, Any], copilot_fn: Callable[..., dict[str, Any]]) -> dict[str, Any]:
    packet = copilot_fn(inputs)
    assessment = packet.get("assessment") or {}
    spatial = packet.get("spatial") or {}
    decision = packet.get("decision") or {}
    ledger = packet.get("evidence_ledger") or {}
    agents = packet.get("agents") or {}
    return {
        "project": "URBION HORIZON",
        "demo_mode": "CHAMPIONSHIP_JUDGE_DEMO",
        "headline": "Evidence-grounded planning copilot",
        "flow": ["ASSESSMENT", "SPATIAL", "KNOWLEDGE", "IMPACT", "SCENARIO", "DECISION", "EVIDENCE LEDGER"],
        "snapshot": {
            "decision": decision.get("status") or decision.get("decision_status"),
            "agent_mode": agents.get("mode"),
            "tod_distance_m": (spatial.get("tod") or {}).get("distance_m"),
            "evidence_items": ledger.get("total_items", 0),
            "review_required": ledger.get("review_required_items", 0),
            "next_actions": packet.get("next_actions") or [],
        },
        "assessment_status": assessment.get("status"),
        "guardrails": {
            "decision_authority": "NONE",
            "statutory_verification": "NOT_CLAIMED",
            "purpose": "Decision-support and planning workflow demonstration only.",
        },
    }
