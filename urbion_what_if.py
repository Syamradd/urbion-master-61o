"""Executable what-if scenario orchestration for URBION Phase D."""
from __future__ import annotations
from typing import Any, Callable


def build_scenario_plan(baseline_inputs: dict[str, Any], variants: list[dict[str, Any]]) -> list[dict[str, Any]]:
    base = dict(baseline_inputs or {})
    return [
        {
            "id": str(v.get("id") or f"SCENARIO-{i}"),
            "name": v.get("name", str(v.get("id") or f"Scenario {i}")),
            "inputs": {**base, **dict(v.get("overrides", {}))},
        }
        for i, v in enumerate(variants or [], 1)
    ]


def _indicator_map(assessment: dict[str, Any]) -> dict[str, float]:
    items = (assessment or {}).get("site_analysis", {}).get("indicators", []) or []
    if isinstance(items, dict):
        items = [
            {"name": key, "score": value if isinstance(value, (int, float)) else (value or {}).get("score")}
            for key, value in items.items()
        ]
    out: dict[str, float] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or item.get("id") or "").strip()
        try:
            score = float(item.get("score"))
        except (TypeError, ValueError):
            continue
        if name:
            out[name] = score
    return out


def _input_changes(base_inputs: dict[str, Any], scenario_inputs: dict[str, Any]) -> list[dict[str, Any]]:
    keys = sorted(set((base_inputs or {}).keys()) | set((scenario_inputs or {}).keys()))
    return [
        {"field": key, "before": (base_inputs or {}).get(key), "after": (scenario_inputs or {}).get(key)}
        for key in keys
        if (base_inputs or {}).get(key) != (scenario_inputs or {}).get(key)
    ]


def _score(assessment: dict[str, Any]) -> float:
    site_analysis = (assessment or {}).get("site_analysis", {}) or {}
    planning_value = (assessment or {}).get("planning_value", {}) or {}
    value = site_analysis.get("score", planning_value.get("score", 0))
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def compare_assessments(baseline: dict[str, Any], scenarios: list[dict[str, Any]]) -> dict[str, Any]:
    base = baseline or {}
    base_status = base.get("final_status", "REQUIRES REVIEW")
    base_sa = base.get("site_analysis", {}) or {}
    base_pv = base.get("planning_value", {}) or {}
    base_score = _score(base)
    base_indicators = _indicator_map(base)
    results = []

    for item in scenarios or []:
        result = item.get("assessment", item.get("result", {})) or {}
        sa = result.get("site_analysis", {}) or {}
        pv = result.get("planning_value", {}) or {}
        score = _score(result)
        status = result.get("final_status", "REQUIRES REVIEW")
        scenario_indicators = _indicator_map(result)
        indicator_deltas = [
            {
                "name": name,
                "before": base_indicators.get(name),
                "after": after,
                "delta": round(after - base_indicators[name], 2) if name in base_indicators else None,
            }
            for name, after in scenario_indicators.items()
            if name in base_indicators
        ]
        scenario_inputs = item.get("inputs", {}) or {}
        baseline_inputs = item.get("baseline_inputs", {}) or {}
        blockers = list(pv.get("blockers", []))
        gaps = list(pv.get("evidence_gaps", []))
        recommendation = (
            (sa.get("recommendation") or {}).get("headline")
            or pv.get("headline")
            or result.get("recommendation")
        )
        reason = (
            (sa.get("recommendation") or {}).get("reason")
            or pv.get("reason")
            or result.get("reason")
            or recommendation
            or "Scenario outcome returned from the same assessment engine."
        )
        results.append(
            {
                "id": str(item.get("id") or item.get("name") or f"SCENARIO-{len(results)+1}"),
                "name": item.get("name"),
                "status": status,
                "status_changed": status != base_status,
                "score": score,
                "score_delta": round(score - base_score, 2),
                "decision_delta": (
                    "IMPROVED"
                    if status == "COMPLY" and base_status != "COMPLY"
                    else ("CHANGED" if status != base_status else "UNCHANGED")
                ),
                "band": sa.get("suitability_band") or sa.get("band") or pv.get("band"),
                "recommendation": recommendation,
                "reason": reason,
                "blockers": blockers,
                "evidence_gaps": gaps,
                "input_changes": _input_changes(baseline_inputs, scenario_inputs),
                "indicator_deltas": indicator_deltas,
            }
        )

    ranked = sorted(
        results,
        key=lambda x: (x["status"] == "COMPLY", not x["blockers"], x["score"]),
        reverse=True,
    )
    for rank, item in enumerate(ranked, 1):
        item["rank"] = rank

    return {
        "title": "What-If Scenario Comparison",
        "version": "PHASE-D",
        "baseline_status": base_status,
        "baseline_score": base_score,
        "baseline_indicators": base_indicators,
        "scenarios": results,
        "ranked_scenarios": [item["id"] for item in ranked],
        "best_candidate": ranked[0]["id"] if ranked else None,
        "decision_pathway": [
            "Baseline assessment established",
            "Scenario variants assessed with the same decision engine",
            "Scores, status and evidence gaps compared",
            "Planner verifies the strongest pathway against authoritative evidence",
        ],
        "disclaimer": "Scenario comparison is decision support only; it does not replace statutory assessment or authority review.",
    }


def execute_what_if(
    baseline_inputs: dict[str, Any],
    variants: list[dict[str, Any]],
    assess_fn: Callable[[dict[str, Any]], dict[str, Any]],
) -> dict[str, Any]:
    baseline_inputs = dict(baseline_inputs or {})
    plan = build_scenario_plan(baseline_inputs, variants)
    baseline = assess_fn(dict(baseline_inputs))
    executed = []
    for item in plan:
        scenario_inputs = dict(item["inputs"])
        assessment = assess_fn(scenario_inputs)
        executed.append(
            {
                "id": item["id"],
                "name": item["name"],
                "inputs": scenario_inputs,
                "baseline_inputs": dict(baseline_inputs),
                "assessment": assessment,
            }
        )
    comparison = compare_assessments(baseline, executed)
    comparison["baseline"] = baseline
    return comparison
