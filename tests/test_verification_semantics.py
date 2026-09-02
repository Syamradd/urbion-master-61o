from urbion_verification import spatial_evidence, rule_evidence


def test_spatial_inputs_are_not_called_verified_by_default():
    result = spatial_evidence()
    assert result["verification_state"] == "SOURCE_CONTEXT"
    assert result["decision_language"] == "SCREENED / CALCULATED"
    assert result["verification_state"] != "VERIFIED"


def test_authoritative_confirmation_can_be_explicit():
    result = spatial_evidence(source="VERIFIED")
    assert result["verification_state"] == "VERIFIED"
    assert result["decision_language"] == "VERIFIED"


def test_rule_context_does_not_equal_verified_rule():
    result = rule_evidence("COMPLY", source_id="iplan", source_status="LIVE_ARCGIS_REST")
    assert result["verification_state"] == "SOURCE_CONTEXT"
    assert result["decision_safe"] is False
