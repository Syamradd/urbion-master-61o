from urbion_review_packet import build_review_packet


def test_review_packet_reads_integrated_grounding_shape() -> None:
    lcp = {
        "version": "MASTER-199",
        "decision_boundary": "INTEGRATED_LCP_PLANNING_SUPPORT",
        "statutory_verification": "NOT_CLAIMED",
        "recommendations": [{"recommendation": "Review access strategy", "status": "PLANNER_REVIEW"}],
        "recommendation_grounding": {
            "version": "MASTER-234",
            "items": [{
                "recommendation": {"recommendation": "Review access strategy", "status": "PLANNER_REVIEW"},
                "evidence_refs": [{"type": "IMPACT", "count": 1}],
                "grounded": True,
                "status": "PLANNER_REVIEW",
            }],
            "count": 1,
            "grounded_count": 1,
            "review_gaps": [],
        },
        "review_gaps": [],
    }
    packet = build_review_packet(lcp=lcp)
    assert packet["grounding"]["grounded_recommendation_count"] == 1
    assert packet["grounding"]["status"] == "GROUNDED"
    assert packet["recommendations"][0]["status"] == "PLANNER_REVIEW"
    assert packet["recommendations"][0]["evidence_refs"] == [{"type": "IMPACT", "count": 1}]


def test_review_packet_surfaces_grounding_gap() -> None:
    lcp = {
        "recommendations": [{"recommendation": "Needs evidence"}],
        "recommendation_grounding": {
            "count": 1,
            "grounded_count": 0,
            "review_gaps": ["RECOMMENDATION_LACKS_TRACEABLE_EVIDENCE"],
        },
        "review_gaps": ["RECOMMENDATION_LACKS_TRACEABLE_EVIDENCE"],
    }
    packet = build_review_packet(lcp=lcp)
    assert packet["grounding"]["grounded_recommendation_count"] == 0
    assert packet["grounding"]["status"] == "REVIEW_REQUIRED"
    assert packet["recommendations"][0]["evidence_refs"] == []
