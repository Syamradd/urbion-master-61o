"""Deterministic judge-mode showcase orchestration for URBION."""
from __future__ import annotations
from typing import Any


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
        })
    counts = {}
    for row in rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    return {
        "project": "URBION HORIZON",
        "version": "PHASE-E.6",
        "headline": "See the site. Read the policy. Make the decision.",
        "scoreboard": rows,
        "status_counts": counts,
        "scenario_count": len(rows),
        "disclaimer": "Deterministic showcase scenarios for judging; not statutory approval.",
    }
