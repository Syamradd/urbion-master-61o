"""Deterministic proposal what-if utilities for URBION Phase D."""
from __future__ import annotations
from typing import Any


def _get(obj: Any, key: str, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def compare_assessments(baseline: dict[str, Any], scenarios: list[dict[str, Any]]) -> dict[str, Any]:
    """Compare baseline and scenario assessment outputs without mutating inputs."""
    base = baseline or {}
    base_status = base.get("final_status", "REQUIRES REVIEW")
    base_sa = base.get("site_analysis", {}) or {}
    base_pv = base.get("planning_value", {}) or {}
    base_score = float(base_sa.get("score", base_pv.get("score", 0)) or 0)
    results = []
    for item in scenarios or []:
        scenario_id = str(item.get("id") or item.get("name") or f"SCENARIO-{len(results)+1}")
        result = item.get("assessment", item.get("result", {})) or {}
        sa = result.get("site_analysis", {}) or {}
        pv = result.get("planning_value", {}) or {}
        score = float(sa.get("score", pv.get("score", 0)) or 0)
        status = result.get("final_status", "REQUIRES REVIEW")
        results.append({
            "id": scenario_id,
            "name": item.get("name", scenario_id),
            "status": status,
            "status_changed": status != base_status,
            "score": score,
            "score_delta": round(score - base_score, 2),
            "band": sa.get("suitability_band") or sa.get("band") or pv.get("band"),
            "recommendation": (sa.get("recommendation") or {}).get("headline") or pv.get("headline"),
            "blockers": list(pv.get("blockers", [])),
            "evidence_gaps": list(pv.get("evidence_gaps", [])),
        })
    ranked = sorted(results, key=lambda x: (x["status"] == "COMPLY", not x["blockers"], x["score"]), reverse=True)
    return {
        "title": "What-If Scenario Comparison",
        "version": "PHASE-D",
        "baseline_status": base_status,
        "baseline_score": base_score,
        "scenarios": results,
        "ranked_scenarios": [x["id"] for x in ranked],
        "best_candidate": ranked[0]["id"] if ranked else None,
        "disclaimer": "Scenario comparison is decision support only; it does not replace statutory assessment or authority review.",
    }


def build_scenario_plan(baseline_inputs: dict[str, Any], variants: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return isolated input payloads for scenario execution."""
    base = dict(baseline_inputs or {})
    return [{"id": str(v.get("id") or f"SCENARIO-{i}"), "name": v.get("name", str(v.get("id") or f"Scenario {i}")), "inputs": {**base, **dict(v.get("overrides", {}))}} for i, v in enumerate(variants or [], 1)]
