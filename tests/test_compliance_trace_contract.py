from urbion_compliance_trace_contract import compliance_trace


def test_supported_trace_is_complete_and_explicitly_traceable():
    result = compliance_trace(
        status="COMPLY",
        rule="RT MBMB 2040",
        requirement="Allowed land use",
        why="Identified zoning supports the proposed use.",
        evidence="i-Plan zoning feature Z-12",
        reference="Page 84 / Clause 4.2",
        confidence="SUPPORTED",
        planner_action="Verify current authority requirements.",
    )
    assert result["decision_safe"] is True
    assert result["statutory_approval_claim"] is False


def test_missing_reference_or_non_supported_confidence_is_not_decision_safe():
    assert compliance_trace(
        status="REVIEW", rule="GP", requirement="Buffer", why="Needs checking",
        evidence="source", reference=None, confidence="GAP"
    )["decision_safe"] is False
    assert compliance_trace(
        status="COMPLY", rule="GP", requirement="Buffer", why="Needs checking",
        evidence="source", reference="Clause 2", confidence="REVIEW"
    )["decision_safe"] is False
