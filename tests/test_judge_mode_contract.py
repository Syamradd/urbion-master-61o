from urbion_judge_mode import build_judge_mode


def test_judge_mode_is_deterministic_and_bounded():
    result = build_judge_mode(scenarios=[
        {"id": "A", "name": "Scenario A", "assessment": {
            "final_status": "COMPLY",
            "site_analysis": {"suitability_score": 82},
            "decision_confidence": {"band": "HIGH"},
            "recommendation": {"headline": "Advance for review"},
            "evidence_state": {"final_decision": "CALCULATED", "statutory_verification": "NOT_CLAIMED"},
        }}
    ])
    assert result["project"] == "URBION HORIZON"
    assert result["version"] == "PHASE-E.7"
    assert result["scenario_count"] == 1
    assert result["scoreboard"][0]["status"] == "COMPLY"
    assert result["scoreboard"][0]["evidence_state"] == "CALCULATED"
    assert result["scoreboard"][0]["statutory_verification"] == "NOT_CLAIMED"
    assert "not statutory approval" in result["decision_boundary"].lower()


def test_empty_judge_mode_is_safe():
    result = build_judge_mode(scenarios=[])
    assert result["scoreboard"] == []
    assert result["scenario_count"] == 0
    assert result["status_counts"] == {}
