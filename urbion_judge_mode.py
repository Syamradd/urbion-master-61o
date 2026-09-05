"""Deterministic judge-mode showcase orchestration for URBION."""
from __future__ import annotations
from typing import Any


def _dimension_drivers(assessment: dict[str, Any]) -> list[dict[str, Any]]:
    """Expose actual assessment dimensions as judge-facing score drivers."""
    analysis = assessment.get("site_analysis") or {}
    indicators = list(analysis.get("indicators", []) or [])
    drivers = []
    for item in indicators:
        if not isinstance(item, dict):
            continue
        score = item.get("score")
        drivers.append({
            "dimension": str(item.get("name", "Unnamed dimension")),
            "score": score,
            "status": item.get("status") or ("SCORED" if score is not None else "UNVERIFIED"),
            "method": item.get("method") or item.get("note") or "Assessment indicator",
        })
    return drivers


def build_judge_mode(*, scenarios: list[dict[str, Any]]) -> dict[str, Any]:
    """Turn executed demo assessments into a compact championship scoreboard."""
    rows = []
    for item in scenarios or []:
        assessment = item.get("assessment", {})
        rows.append({
            "id": item.get("id"),
            "name": item.get("name", item.get("id")),
            "status": assessment.get("final_status", "REQUIRES REVIEW"),
            "suitability": (assessment.get("site_analysis") or {}).get("suitability_score"),
            "confidence": (assessment.get("decision_confidence") or {}).get("band"),
            "recommendation": (assessment.get("recommendation") or {}).get("headline", ""),
            "evidence_state": (assessment.get("evidence_state") or {}).get("final_decision", "UNVERIFIED"),
            "statutory_verification": (assessment.get("evidence_state") or {}).get("statutory_verification", "NOT_CLAIMED"),
            "score_breakdown": _dimension_drivers(assessment),
            "decision_trace": assessment.get("decision_trace", []),
            "review_gaps": assessment.get("review_gaps", []) or (assessment.get("planning_value") or {}).get("evidence_gaps", []),
            "next_actions": (assessment.get("planning_value") or {}).get("next_actions", []),
        })
    counts = {}
    for row in rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    return {
        "project": "URBION HORIZON",
        "version": "PHASE-E.8",
        "headline": "See the site. Read the policy. Make the decision.",
        "scoreboard": rows,
        "status_counts": counts,
        "scenario_count": len(rows),
        "decision_boundary": "Deterministic showcase and decision-support output; not statutory approval.",
        "statutory_verification": "NOT_CLAIMED",
        "disclaimer": "Deterministic showcase scenarios for judging; evidence and statutory verification remain explicitly bounded.",
    }
