from urbion_recommendation_grounding import build_recommendation_grounding


def test_recommendation_grounding_requires_traceable_basis():
    result = build_recommendation_grounding(recommendations={"recommendations": [{"action": "Review mitigation"}]})
    assert result["count"] == 1
    assert result["grounded_count"] == 0
    assert result["review_gaps"] == ["RECOMMENDATION_LACKS_TRACEABLE_EVIDENCE"]


def test_recommendation_grounding_accepts_policy_basis():
    result = build_recommendation_grounding(
        recommendations={"recommendations": [{"action": "Review", "policy_reference": "RFN"}]}
    )
    assert result["grounded_count"] == 1
    assert result["items"][0]["status"] == "PLANNER_REVIEW"
    assert result["items"][0]["evidence_refs"][0]["type"] == "POLICY"
