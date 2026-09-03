from urbion_decision_center import build_decision_center


def test_decision_center_discloses_review_boundary():
    result = build_decision_center(assessment={"site": {"latitude": 2.2, "longitude": 102.2}, "final_status": "REQUIRES REVIEW"})
    assert result["statutory_verification"] == "NOT_CLAIMED"
    assert "evidence" in result
    assert "guardrail" in result


def test_decision_center_preserves_trace():
    trace = ["SITE", "SPATIAL", "IMPACT", "RECOMMENDATION", "PLANNER REVIEW"]
    result = build_decision_center(assessment={"site": {"latitude": 2.2, "longitude": 102.2}, "decision_trace": trace})
    assert result["decision_trace"] == trace
