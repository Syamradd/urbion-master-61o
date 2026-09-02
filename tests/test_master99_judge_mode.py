from urbion_judge_mode import build_judge_mode


def test_judge_mode_builds_compact_scoreboard():
    result = build_judge_mode(scenarios=[
        {"id": "TOD-COMPLY", "name": "TOD Mixed-Use Candidate", "assessment": {
            "final_status": "COMPLY",
            "site_analysis": {"suitability_score": 86},
            "decision_confidence": {"band": "HIGH"},
            "recommendation": {"headline": "STRONG CANDIDATE FOR FURTHER STUDY"},
        }},
        {"id": "SHOP-FAIL", "assessment": {"final_status": "NON-COMPLIANCE"}},
    ])
    assert result["scenario_count"] == 2
    assert result["status_counts"]["COMPLY"] == 1
    assert result["scoreboard"][0]["confidence"] == "HIGH"
    assert "Deterministic showcase" in result["disclaimer"]
