"""Compact, auditable championship evidence packet for URBION."""
from __future__ import annotations
from typing import Any


def build_release_packet(lcp: dict[str, Any]) -> dict[str, Any]:
    """Summarise an integrated LCP result without upgrading evidence certainty."""
    lcp = lcp or {}
    gaps = list(lcp.get("review_gaps", []) or [])
    recs = (lcp.get("recommendations") or {}).get("recommendations", []) or []
    return {
        "version": "MASTER-195",
        "project": "URBION HORIZON",
        "status": "READY_FOR_PLANNER_REVIEW" if lcp.get("statutory_verification") == "NOT_CLAIMED" else "REVIEW_REQUIRED",
        "trace": lcp.get("trace"),
        "evidence_summary": lcp.get("evidence_summary", {}),
        "review_gap_count": len(gaps),
        "review_gaps": gaps,
        "top_recommendations": [
            {"action": r.get("action"), "status": r.get("status"), "reason": r.get("reason")}
            for r in recs[:5]
        ],
        "decision_boundary": lcp.get("decision_boundary", "INTEGRATED_LCP_PLANNING_SUPPORT"),
        "statutory_verification": "NOT_CLAIMED",
        "disclaimer": "Planning decision support only; planner/PBT and authorised-agency verification remains required.",
    }
