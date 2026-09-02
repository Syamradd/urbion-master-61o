from urbion_parcel_evidence import parcel_evidence, parcel_summary


def test_planned_parcel_is_not_verified():
    item = parcel_evidence(lot_no="11213")
    assert item["decision_safe"] is False
    assert parcel_summary([item])["status"] == "EVIDENCE_REQUIRED"


def test_verified_parcel_is_decision_safe():
    item = parcel_evidence(lot_no="11213", status="VERIFIED", confidence="HIGH")
    assert item["decision_safe"] is True
    assert parcel_summary([item])["verified_count"] == 1
