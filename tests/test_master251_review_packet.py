from __future__ import annotations

from urbion_review_packet import build_review_packet


def test_review_packet_preserves_boundary_and_identity() -> None:
    lcp = {
        "version": "MASTER-199",
        "decision_boundary": "INTEGRATED_LCP_PLANNING_SUPPORT",
        "statutory_verification": "NOT_CLAIMED",
        "evidence_summary": {"counts": {"CALCULATED": 2}},
        "recommendations": [{"recommendation": "Review access strategy", "status": "PLANNER_REVIEW", "evidence_refs": ["impact:1"]}],
        "recommendation_grounding": {"status": "GROUNDED", "grounded_recommendation_count": 1},
        "what_if": {"status": "READY", "ranked_scenarios": [{"id": "baseline"}]},
        "review_gaps": [],
        "trace": "SITE → SPATIAL → IMPACT → GUIDELINES/POLICY → RECOMMENDATION → WHAT-IF → DECISION CENTER → LCP/PLANNER REVIEW",
    }
    packet = build_review_packet(lcp=lcp)
    assert packet["version"] == "MASTER-251"
    assert packet["release_identity"] == "MASTER-199"
    assert packet["status"] == "READY_FOR_PLANNER_REVIEW"
    assert packet["statutory_verification"] == "NOT_CLAIMED"
    assert packet["recommendations"][0]["evidence_refs"] == ["impact:1"]
    assert packet["what_if"]["scenario_count"] == 1


def test_review_packet_never_hides_review_gaps() -> None:
    packet = build_review_packet(lcp={"review_gaps": ["RECOMMENDATION_LACKS_TRACEABLE_EVIDENCE"]})
    assert packet["status"] == "REVIEW_REQUIRED"
    assert packet["evidence"]["review_gap_count"] == 1
    assert packet["review_gaps"] == ["RECOMMENDATION_LACKS_TRACEABLE_EVIDENCE"]
