from urbion_recommendation_grounding import build_recommendation_grounding

def test_recommendation_grounding_uses_policy_and_environment_evidence():
    result = build_recommendation_grounding(recommendations={"recommendations": [{"domain": "flood", "policy_reference": "RFN"}]}, environment_implications={"implications": [{"domain": "flood"}]}, impacts={"impacts": []})
    assert result["count"] == 1
    assert result["grounded_count"] == 1
    assert result["items"][0]["status"] == "PLANNER_REVIEW"

def test_recommendation_grounding_requires_traceable_evidence():
    result = build_recommendation_grounding(recommendations={"recommendations": [{"domain": "flood", "action": "Review mitigation"}]})
    assert result["grounded_count"] == 0
    assert result["review_gaps"] == ["RECOMMENDATION_LACKS_TRACEABLE_EVIDENCE"]
