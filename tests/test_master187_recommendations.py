from urbion_recommendation_engine import build_recommendations


def test_recommendation_requires_traceable_policy_basis():
    result = build_recommendations(
        impacts={"physical": [{"id": "flood_exposure"}]},
        policy_graph={"nodes": {"links": [{"domain":"physical","impact":"flood_exposure","issue":"Flood risk","reference":"RT MBMB 2035","strategy":"Flood-sensitive planning","sdg":"SDG 11","evidence":"SOURCE_CONTEXT"}]}, "review_gaps": []},
    )
    assert len(result["recommendations"]) == 1
    assert result["recommendations"][0]["policy_reference"] == "RT MBMB 2035"
    assert result["recommendations"][0]["status"] == "PLANNER_REVIEW"
    assert result["statutory_verification"] == "NOT_CLAIMED"


def test_no_policy_edge_does_not_generate_fake_recommendation():
    result = build_recommendations(impacts={"social": [{"id":"facility_access"}]}, policy_graph={"nodes":{"links":[]},"review_gaps":[]})
    assert result["recommendations"] == []
    assert "NO_TRACEABLE_POLICY_RECOMMENDATION" in result["review_gaps"]
