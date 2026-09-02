from urbion_evidence_binding import bind_evidence_to_rules
from urbion_evidence_contract import build_evidence


def test_verified_evidence_supports_matching_rule():
    evidence = [build_evidence(source="JUPEM", layer="PARCEL", value="11213", status="VERIFIED")]
    rules = [{"rule_id": "PARCEL-01", "evidence_layer": "PARCEL"}]
    result = bind_evidence_to_rules(evidence, rules)[0]
    assert result["evidence_status"] == "SUPPORTED"
    assert result["decision_safe_evidence"] == 1


def test_discovery_evidence_remains_a_gap():
    evidence = [build_evidence(source="MelGIS", layer="ZONING", value="Mixed Use", status="DISCOVERY_COMPLETE")]
    rules = [{"rule_id": "ZONE-01", "evidence_layer": "ZONING"}]
    assert bind_evidence_to_rules(evidence, rules)[0]["evidence_status"] == "GAP"


def test_no_matching_evidence_is_explicit():
    rules = [{"rule_id": "ENV-01", "evidence_layer": "ENVIRONMENT"}]
    assert bind_evidence_to_rules([], rules)[0]["evidence_status"] == "NO_EVIDENCE"
