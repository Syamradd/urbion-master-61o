from urbion_evidence_contract import build_evidence, contract_summary


def test_verified_evidence_is_decision_safe():
    item = build_evidence(source="JUPEM", layer="PARCEL", value="11213", evidence_type="CADASTRAL", status="VERIFIED")
    assert item["decision_safe"] is True
    assert item["status"] == "VERIFIED"


def test_unavailable_evidence_is_disclosed_not_verified():
    item = build_evidence(source="MyGEMS", layer="GEOLOGY", evidence_type="GEOLOGY", status="QUERY_UNAVAILABLE")
    assert item["decision_safe"] is False
    summary = contract_summary([item])
    assert summary["disclosed_gaps"] == 1
    assert summary["safe_for_decision"] is False


def test_unknown_state_falls_back_to_no_evidence():
    item = build_evidence(source="Unknown", layer="TEST", status="MAGIC_VERIFIED")
    assert item["status"] == "NO_EVIDENCE"
    assert item["decision_safe"] is False
