from urbion_decision_center import build_decision_center


def test_master303_decision_center_exposes_explainable_contract():
    assessment = {
        "final_status": "REQUIRES REVIEW",
        "site": {"latitude": 2.285, "longitude": 102.196, "lot_no": "Not specified", "tod_distance_m": 180},
        "site_analysis": {
            "score": 76.5,
            "indicators": [
                {"name": "Planning Fit", "score": 80},
                {"name": "Transit Access", "score": 100},
            ],
        },
        "recommendation": {"headline": "PLANNER REVIEW", "reason": "Evidence and local interpretation remain required."},
        "decision_confidence": {"score": 72, "band": "MEDIUM"},
        "planning_value": {"evidence_gaps": ["Cadastral verification"], "next_actions": ["Verify parcel", "Pre-consult planner"]},
        "evidence_intelligence": {"items": []},
        "evidence_state": {"site_coordinates": "USER_PROVIDED"},
        "decision_trace": [],
    }
    result = build_decision_center(assessment=assessment)
    assert result["version"] == "PHASE-E.8"
    assert result["decision"]["score_breakdown"][0]["dimension"] == "Planning Fit"
    assert result["decision"]["justification"]
    assert result["evidence_coverage"]["review_required"] is True
    assert result["next_actions"] == ["Verify parcel", "Pre-consult planner"]
    assert result["decision_boundary"] == "PLANNER_DECISION_SUPPORT_ONLY"
    assert result["statutory_verification"] == "NOT_CLAIMED"
