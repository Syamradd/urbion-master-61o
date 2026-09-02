from urbion_environment import environment_evidence, environment_summary


def test_unavailable_environment_stays_a_gap():
    item = environment_evidence(layer="GEOLOGY")
    result = environment_summary([item])
    assert result["verified_count"] == 0
    assert result["decision_safe"] is False
    assert result["status"] == "EVIDENCE_REQUIRED"


def test_verified_environment_can_be_decision_safe():
    item = environment_evidence(layer="AIR_QUALITY", value={"index": "good"}, status="VERIFIED", confidence="HIGH")
    result = environment_summary([item])
    assert result["verified_count"] == 1
    assert result["decision_safe"] is True
