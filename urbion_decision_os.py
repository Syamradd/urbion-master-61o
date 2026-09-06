"""Evidence-gated decision operating layer for URBION HORIZON.

This module does not replace the deterministic assessment. It translates the
existing assessment, scenario and evidence-quality packet into an auditable
planner gate. No statutory approval or compliance claim is inferred.
"""
from __future__ import annotations
from typing import Any


def _score(value: Any) -> float:
    try:
        return max(0.0, min(100.0, float(value)))
    except (TypeError, ValueError):
        return 0.0


def build_decision_os(packet: dict[str, Any]) -> dict[str, Any]:
    evidence = packet.get("evidence_quality") or {}
    quality = _score(evidence.get("score"))
    coverage = _score(evidence.get("coverage"))
    verified = _score(evidence.get("verified_ratio"))
    review_items = list(evidence.get("review_required_items") or [])
    assessment = packet.get("assessment") or {}
    status = str((packet.get("decision") or {}).get("decision", {}).get("status") or assessment.get("final_status") or "REQUIRES REVIEW").upper()
    scenario = packet.get("scenario_intelligence") or {}
    ranked = list(scenario.get("ranked_scenarios") or [])

    blockers: list[str] = []
    if quality < 60:
        blockers.append("Evidence quality is below the planner-review threshold.")
    if coverage < 60:
        blockers.append("Evidence coverage is below the planner-review threshold.")
    if review_items:
        blockers.append(f"{len(review_items)} evidence item(s) still require review or verification.")
    if status == "NON-COMPLIANCE":
        blockers.append("The deterministic assessment reports non-compliance; revise the affected control(s) and re-run.")

    if status == "NON-COMPLIANCE":
        gate = "REVISE_AND_REASSESS"
    elif quality >= 75 and coverage >= 75 and not review_items:
        gate = "PLANNER_REVIEW_READY"
    elif quality >= 60 and coverage >= 60:
        gate = "REVIEW_REQUIRED"
    else:
        gate = "EVIDENCE_REQUIRED"

    scenario_delta: dict[str, Any] | None = None
    if ranked:
        best = ranked[0]
        if isinstance(best, dict):
            baseline = _score(scenario.get("baseline_score"))
            candidate = _score(best.get("score", best.get("suitability_score", baseline)))
            scenario_delta = {"candidate": best.get("id") or best.get("name") or "TOP_SCENARIO", "baseline_score": baseline, "candidate_score": candidate, "delta": round(candidate - baseline, 2)}
        else:
            scenario_delta = {"candidate": str(best), "baseline_score": _score(scenario.get("baseline_score")), "candidate_score": None, "delta": None}

    return {
        "version": "SIGMA-1.0",
        "gate": gate,
        "decision_status": status,
        "evidence": {"score": round(quality, 2), "coverage": round(coverage, 2), "verified_ratio": round(verified, 2), "review_required_count": len(review_items)},
        "blockers": blockers[:8],
        "scenario_delta": scenario_delta,
        "planner_ready": gate == "PLANNER_REVIEW_READY",
        "next_actions": (packet.get("next_actions") or [])[:5],
        "decision_authority": "NONE",
        "statutory_verification": "NOT_CLAIMED",
        "boundary": "EVIDENCE_GATED_PLANNER_DECISION_SUPPORT_ONLY",
    }
