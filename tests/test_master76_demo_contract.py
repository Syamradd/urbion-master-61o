from server import AssessmentRequest, assess_core
from urbion_demo_scenarios import demo_scenarios, get_demo_scenario


def test_demo_lookup_is_stable_and_unknown_is_none():
    assert get_demo_scenario("TOD-COMPLY")["id"] == "TOD-COMPLY"
    assert get_demo_scenario("DOES-NOT-EXIST") is None


def test_demo_scenarios_keep_required_decision_semantics():
    results = {}
    for scenario in demo_scenarios():
        results[scenario["id"]] = assess_core(AssessmentRequest(**scenario["inputs"]))
    assert results["SHOP-FAIL"]["final_status"] == "NON-COMPLIANCE"
    assert results["OFFICE-REVIEW"]["final_status"] == "REQUIRES REVIEW"
    assert results["NON-MBMB"]["final_status"] == "REQUIRES REVIEW"
    assert results["TOD-COMPLY"]["final_status"] in {"COMPLY", "REQUIRES REVIEW"}
    assert results["SHOP-COMPLY"]["final_status"] in {"COMPLY", "REQUIRES REVIEW"}
    for result in results.values():
        assert result["decision_trace"][-1]["stage"] == "DECISION"
        assert result["decision_trace"][-1]["status"] == result["final_status"]
        assert "recommendation" in result
        assert "decision_confidence" in result
        assert "evidence_intelligence" in result
