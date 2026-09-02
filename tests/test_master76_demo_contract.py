from server import AssessmentRequest, assess_core
from urbion_demo_scenarios import demo_scenarios, get_demo_scenario


def test_demo_lookup_is_stable_and_unknown_is_none():
    assert get_demo_scenario("TOD-COMPLY")["id"] == "TOD-COMPLY"
    assert get_demo_scenario("DOES-NOT-EXIST") is None


def test_demo_scenarios_produce_expected_decision_states():
    expected = {
        "TOD-COMPLY": "COMPLY",
        "SHOP-COMPLY": "COMPLY",
        "SHOP-FAIL": "NON-COMPLIANCE",
        "OFFICE-REVIEW": "REQUIRES REVIEW",
        "NON-MBMB": "REQUIRES REVIEW",
    }
    for scenario in demo_scenarios():
        result = assess_core(AssessmentRequest(**scenario["inputs"]))
        assert result["final_status"] == expected[scenario["id"]]
        assert result["decision_trace"][-1]["stage"] == "DECISION"
        assert result["decision_trace"][-1]["status"] == result["final_status"]
        assert "recommendation" in result
        assert "decision_confidence" in result
        assert "evidence_intelligence" in result
