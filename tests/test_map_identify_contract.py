from urbion_map_identify_contract import evidence_handoff, identify_payload


def test_identify_payload_is_source_aware_and_not_decision_safe():
    payload = identify_payload(
        layer={
            "id": "iplan-zoning",
            "name": "Zoning",
            "group": "PLANNING",
            "source": "i-Plan",
        },
        feature={
            "id": "zone-42",
            "properties": {"ZONE": "Residential", "OBJECTID": 42, "EMPTY": ""},
            "geometry": {"type": "Polygon", "coordinates": []},
        },
    )

    assert payload["layer_id"] == "iplan-zoning"
    assert payload["feature_id"] == "zone-42"
    assert payload["source"] == "i-Plan"
    assert payload["geometry_type"] == "Polygon"
    assert payload["properties"] == {"ZONE": "Residential", "OBJECTID": 42}
    assert payload["decision_safe"] is False
    assert payload["use_as_evidence"]["available"] is True
    assert payload["use_as_evidence"]["requires_rule_binding"] is True


def test_identify_payload_never_promotes_query_error_to_evidence():
    payload = identify_payload(
        layer={"id": "mygems-faults", "source": "JMG MyGEMS"},
        feature={"attributes": {"OBJECTID": 9}},
        query_status="QUERY_ERROR",
        evidence_state="EVIDENCE_GAP",
    )

    assert payload["query_status"] == "QUERY_ERROR"
    assert payload["evidence_state"] == "EVIDENCE_GAP"
    assert payload["use_as_evidence"]["available"] is False
    assert payload["decision_safe"] is False


def test_evidence_handoff_requires_rule_binding():
    payload = identify_payload(
        layer={"id": "iplan-flood", "source": "i-Plan"},
        feature={"properties": {"RISK": "HIGH"}},
    )
    handoff = evidence_handoff(payload)

    assert handoff["layer_id"] == "iplan-flood"
    assert handoff["rule_binding_required"] is True
    assert handoff["decision_safe"] is False
    assert handoff["statutory_approval_claim"] is False
