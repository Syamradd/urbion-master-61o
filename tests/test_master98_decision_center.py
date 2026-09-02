from urbion_decision_center import build_decision_center


def test_decision_center_is_single_judge_ready_payload():
    assessment = {
        "final_status": "COMPLY",
        "site": {"latitude": 2.3, "longitude": 102.2, "lot_no": "11213"},
        "site_analysis": {"suitability_score": 86},
        "recommendation": {"level": "POSITIVE"},
        "decision_confidence": {"band": "HIGH"},
        "planning_value": {"findings": ["Good planning fit"]},
        "evidence_intelligence": {"safe_for_decision": False},
        "decision_trace": ["SITE", "POLICY", "DECISION"],
    }
    result = build_decision_center(assessment=assessment)
    assert result["decision"]["status"] == "COMPLY"
    assert result["decision"]["confidence"]["band"] == "HIGH"
    assert result["map"]["features"][0]["geometry"]["coordinates"] == [102.2, 2.3]
    assert "statutory approval" in result["guardrail"]
