from pathlib import Path


HTML = Path("decision-center.html").read_text(encoding="utf-8")


def test_decision_center_exposes_decision_first_workstation():
    required = [
        "DECISION INTELLIGENCE · LIVE",
        "SCORE BREAKDOWN",
        "WHY THIS DECISION",
        "DECISION TRACE",
        "SPATIAL CONTEXT",
        "REVIEW GAPS",
        "NEXT ACTIONS",
        "PLANNER DECISION SUPPORT ONLY",
    ]
    for token in required:
        assert token in HTML


def test_decision_center_renders_structured_decision_fields():
    required = [
        "j.decision",
        "d.score_breakdown",
        "j.decision_trace",
        "j.spatial_intelligence",
        "j.review_gaps",
        "j.next_actions",
        "renderBreakdown",
        "renderTrace",
        "renderSpatial",
        "renderList",
    ]
    for token in required:
        assert token in HTML


def test_decision_center_keeps_statutory_guardrail_and_no_fake_evidence():
    assert "No decision output was fabricated." in HTML
    assert "NOT_STATUTORY_APPROVAL" not in HTML
    assert "Statutory approval or compliance is not claimed." in HTML
