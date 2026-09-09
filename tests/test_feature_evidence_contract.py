from urbion_feature_evidence_contract import feature_evidence


def test_live_source_feature_is_binding_eligible_but_not_decision_safe():
    result = feature_evidence({
        "layer_id": "iplan-zoning",
        "feature_id": "Z-12",
        "layer_name": "Zoning",
        "source": "https://example.invalid/MapServer",
        "query_status": "LIVE_QUERY",
        "evidence_state": "SOURCE_CONTEXT",
    })
    assert result["eligible_for_rule_binding"] is True
    assert result["decision_safe"] is False
    assert result["rule_binding_required"] is True
    assert result["statutory_approval_claim"] is False


def test_gap_or_error_cannot_enter_rule_binding():
    for state, query in (("EVIDENCE_GAP", "LIVE_QUERY"), ("REVIEW", "QUERY_ERROR")):
        result = feature_evidence({"evidence_state": state, "query_status": query, "source": "x"})
        assert result["eligible_for_rule_binding"] is False
        assert result["decision_safe"] is False
