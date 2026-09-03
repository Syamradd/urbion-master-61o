from urbion_championship_summary import build_championship_summary


def test_master250_summary_is_explicitly_non_statutory():
    result = build_championship_summary(
        spatial={"metrics": []},
        environment={"summary": {}},
        recommendations={"recommendations": [{"domain": "flood"}]},
        grounding={"grounded_count": 1},
        review_gaps=[],
    )
    assert result["version"] == "MASTER-250"
    assert result["status"] == "READY_FOR_PLANNER_REVIEW"
    assert result["metrics"]["recommendation_count"] == 1
    assert result["metrics"]["grounded_recommendation_count"] == 1
    assert result["guardrails"]["statutory_verification"] == "NOT_CLAIMED"
    assert result["guardrails"]["authority_decision"] == "NONE"


def test_master250_summary_surfaces_review_gaps():
    result = build_championship_summary(review_gaps=["FLOOD:EVIDENCE_REQUIRED"])
    assert result["status"] == "REVIEW_REQUIRED"
    assert result["metrics"]["review_gap_count"] == 1
