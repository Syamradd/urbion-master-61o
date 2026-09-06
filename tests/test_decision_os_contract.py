from urbion_decision_os import build_decision_os


def test_decision_os_requires_evidence_when_quality_is_low():
    result = build_decision_os({
        "assessment": {"final_status": "SUITABLE"},
        "decision": {"decision": {"status": "SUITABLE"}},
        "evidence_quality": {"score": 40, "coverage": 45, "verified_ratio": 0, "review_required_items": ["flood"]},
    })
    assert result["gate"] == "EVIDENCE_REQUIRED"
    assert result["planner_ready"] is False
    assert result["decision_authority"] == "NONE"
    assert result["statutory_verification"] == "NOT_CLAIMED"


def test_decision_os_allows_planner_review_only_with_strong_clean_evidence():
    result = build_decision_os({
        "assessment": {"final_status": "SUITABLE"},
        "decision": {"decision": {"status": "SUITABLE"}},
        "evidence_quality": {"score": 90, "coverage": 95, "verified_ratio": 80, "review_required_items": []},
        "next_actions": ["Validate final source package."],
    })
    assert result["gate"] == "PLANNER_REVIEW_READY"
    assert result["planner_ready"] is True


def test_decision_os_non_compliance_always_requires_revision():
    result = build_decision_os({
        "assessment": {"final_status": "NON-COMPLIANCE"},
        "decision": {"decision": {"status": "NON-COMPLIANCE"}},
        "evidence_quality": {"score": 99, "coverage": 99, "verified_ratio": 99, "review_required_items": []},
    })
    assert result["gate"] == "REVISE_AND_REASSESS"
    assert result["planner_ready"] is False
    assert result["blockers"]
