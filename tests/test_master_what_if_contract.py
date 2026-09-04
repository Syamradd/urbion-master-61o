from urbion_what_if import compare_assessments, execute_what_if


def _assessment(score, status, indicators):
    return {"final_status": status, "site_analysis": {"score": score, "indicators": indicators}, "planning_value": {"score": score, "evidence_gaps": []}}


def test_compare_exposes_rank_reason_and_deltas():
    baseline = _assessment(60, "REQUIRES REVIEW", [{"name": "Transit Access", "score": 50}])
    scenario = _assessment(72, "COMPLY", [{"name": "Transit Access", "score": 70}])
    out = compare_assessments(baseline, [{"id": "A", "name": "Improve transit", "inputs": {"plot_ratio": 3}, "baseline_inputs": {"plot_ratio": 4}, "assessment": scenario}])
    item = out["scenarios"][0]
    assert item["rank"] == 1
    assert item["score_delta"] == 12.0
    assert item["decision_delta"] == "IMPROVED"
    assert item["indicator_deltas"][0]["delta"] == 20.0
    assert item["input_changes"][0]["field"] == "plot_ratio"
    assert item["reason"]
    assert out["decision_pathway"]


def test_execute_preserves_baseline_inputs_for_change_explanation():
    seen = []
    def assess(inputs):
        seen.append(inputs)
        return _assessment(float(inputs.get("plot_ratio", 4)) * 10, "REQUIRES REVIEW", [{"name": "Planning Fit", "score": 50}])
    out = execute_what_if({"plot_ratio": 4}, [{"id": "A", "name": "Lower", "overrides": {"plot_ratio": 3}}], assess)
    assert len(seen) == 2
    assert out["scenarios"][0]["input_changes"][0]["before"] == 4
    assert out["scenarios"][0]["input_changes"][0]["after"] == 3
