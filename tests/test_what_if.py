from urbion_what_if import build_scenario_plan, compare_assessments


def test_scenario_plan_does_not_mutate_baseline():
    base = {"plot_ratio": 4.5, "landscaped_pedestrian_walkway": 0.5}
    plan = build_scenario_plan(base, [{"id": "WALKWAY-FIX", "overrides": {"landscaped_pedestrian_walkway": 1.5}}])
    assert base["landscaped_pedestrian_walkway"] == 0.5
    assert plan[0]["inputs"]["landscaped_pedestrian_walkway"] == 1.5


def test_compare_surfaces_status_change_and_blocker_delta():
    baseline = {"final_status": "NON-COMPLIANCE", "site_analysis": {"score": 45}, "planning_value": {"blockers": ["R-01 failed"], "evidence_gaps": []}}
    scenario = {"id": "WALKWAY-FIX", "name": "Fix walkway", "assessment": {"final_status": "COMPLY", "site_analysis": {"score": 82}, "planning_value": {"band": "READY FOR FURTHER REVIEW", "blockers": [], "evidence_gaps": []}}}
    result = compare_assessments(baseline, [scenario])
    assert result["version"] == "PHASE-D"
    assert result["scenarios"][0]["status_changed"] is True
    assert result["scenarios"][0]["score_delta"] == 37
    assert result["best_candidate"] == "WALKWAY-FIX"


def test_empty_scenarios_are_safe():
    result = compare_assessments({"final_status": "REQUIRES REVIEW"}, [])
    assert result["scenarios"] == []
    assert result["best_candidate"] is None
