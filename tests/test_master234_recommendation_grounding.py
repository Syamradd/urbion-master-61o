from urbion_recommendation_grounding import build_recommendation_grounding


def test_recommendation_with_policy_is_grounded():
    result = build_recommendation_grounding(
        recommendations={"recommendations": [{"text": "Require mitigation", "policy_reference": "RFN"}]},
        environment_implications={"implications": [{"domain": "flood"}]},
        impacts={"impacts": [{"domain": "physical"}]},
    )
    assert result["version"] == "MASTER-234"
    assert result["grounded_count"] == 1
    assert result["items"][0]["grounded"] is True


def test_recommendation_without_trace_is_review_required():
    result = build_recommendation_grounding(recommendations={"recommendations": [{"text": "Proceed"}]})
    assert result["items"][0]["grounded"] is False
    assert result["items"][0]["status"] == "REVIEW_REQUIRED"
    assert "RECOMMENDATION_LACKS_TRACEABLE_EVIDENCE" in result["review_gaps"]
