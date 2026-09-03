"""Championship-facing audit helpers for deterministic planner review."""
from __future__ import annotations
from typing import Any


def build_review_packet(*, lcp: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build a compact judge/planner review packet from an LCP payload."""
    result = lcp or {}
    evidence = result.get("evidence_summary") or {}
    counts = evidence.get("counts") or {}
    recommendations = result.get("recommendations") or []
    grounding = result.get("recommendation_grounding") or {}
    scenarios = (result.get("what_if") or {}).get("ranked_scenarios", [])
    gaps = result.get("review_gaps") or []

    rec_items: list[dict[str, Any]] = []
    for rec in recommendations if isinstance(recommendations, list) else []:
        if isinstance(rec, dict):
            rec_items.append({
                "recommendation": rec.get("recommendation", rec.get("title", rec.get("action"))),
                "status": rec.get("status", "REVIEW_REQUIRED"),
                "evidence_refs": rec.get("evidence_refs", []),
            })
        else:
            rec_items.append({"recommendation": str(rec), "status": "REVIEW_REQUIRED", "evidence_refs": []})

    return {
        "version": "MASTER-251",
        "status": "READY_FOR_PLANNER_REVIEW" if not gaps else "REVIEW_REQUIRED",
        "release_identity": result.get("version"),
        "decision_boundary": result.get("decision_boundary"),
        "statutory_verification": result.get("statutory_verification"),
        "evidence": {"counts": counts, "review_gap_count": len(gaps)},
        "recommendations": rec_items,
        "grounding": {
            "status": grounding.get("status"),
            "grounded_recommendation_count": grounding.get("grounded_recommendation_count", 0),
        },
        "what_if": {
            "scenario_count": len(scenarios) if isinstance(scenarios, list) else 0,
            "status": (result.get("what_if") or {}).get("status"),
        },
        "review_gaps": gaps,
        "trace": result.get("trace"),
    }
