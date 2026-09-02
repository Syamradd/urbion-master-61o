"""Decision pathway and scenario ranking utilities for URBION Phase D."""
from __future__ import annotations
from typing import Any

_STATUS_ORDER = {"COMPLY": 3, "REQUIRES REVIEW": 2, "NOT APPLICABLE": 1, "NON-COMPLIANCE": 0}


def rank_scenarios(comparison: dict[str, Any]) -> dict[str, Any]:
    """Rank scenarios by decision outcome, blockers, score and evidence burden."""
    items = list((comparison or {}).get("scenarios", []))
    def key(item: dict[str, Any]):
        return (
            _STATUS_ORDER.get(str(item.get("status", "REQUIRES REVIEW")), -1),
            not bool(item.get("blockers")),
            -len(item.get("evidence_gaps", [])),
            float(item.get("score", 0) or 0),
        )
    ranked = sorted(items, key=key, reverse=True)
    for i, item in enumerate(ranked, 1):
        item["rank"] = i
    pathway = []
    if ranked:
        best = ranked[0]
        if best.get("status") == "COMPLY":
            pathway.append("Advance the strongest compliant scenario to planner review.")
        elif best.get("status") == "REQUIRES REVIEW":
            pathway.append("Resolve evidence and planning-review gaps before advancing.")
        elif best.get("status") == "NON-COMPLIANCE":
            pathway.append("Redesign the proposal before proceeding.")
        else:
            pathway.append("Reconsider the development position or scenario assumptions.")
        if best.get("evidence_gaps"):
            pathway.append("Close the listed evidence gaps before treating the scenario as decision-ready.")
    return {**(comparison or {}), "scenarios": ranked, "ranked_scenarios": [x["id"] for x in ranked], "best_candidate": ranked[0]["id"] if ranked else None, "decision_pathway": pathway, "version": "PHASE-D.2"}
