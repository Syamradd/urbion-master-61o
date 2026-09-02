from server import AssessmentRequest, assess_core
from urbion_demo_scenarios import demo_scenarios, get_demo_scenario


def test_all_demo_scenarios_resolve_and_return_decision_contract():
    scenarios = demo_scenarios()
    assert len(scenarios) == 5
    for scenario in scenarios:
        resolved = get_demo_scenario(scenario["id"])
        assert resolved is not None
        result = assess_core(AssessmentRequest(**resolved["inputs"]))
        assert result["project"] == "URBION"
        assert result["final_status"] in {"COMPLY", "NON-COMPLIANCE", "REQUIRES REVIEW", "NOT APPLICABLE", "CONDITIONAL RISK"}
        assert result["recommendation"]["headline"]
        assert result["recommendation"]["level"]
        assert result["decision_confidence"]["band"] in {"HIGH", "MEDIUM", "LOW"}
        assert len(result["decision_trace"]) == 6
        assert result["decision_trace"][-1]["stage"] == "DECISION"


def test_unknown_demo_scenario_is_not_silently_resolved():
    assert get_demo_scenario("DOES-NOT-EXIST") is None


def test_non_mbmb_guard_does_not_claim_local_rule_coverage():
    item = get_demo_scenario("NON-MBMB")
    result = assess_core(AssessmentRequest(**item["inputs"]))
    assert result["policy_coverage"]["coverage"] == "SPATIAL_DEMO_ONLY"
    assert result["final_status"] == "REQUIRES REVIEW"
    assert result["recommendation"]["level"] == "REVIEW"
    assert "EVIDENCE" in result["recommendation"]["headline"]
