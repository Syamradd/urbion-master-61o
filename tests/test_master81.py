from urbion_planning_value import build_planning_value


def _build(status, coverage="FULL_RULE_ENGINE", evidence=None, compliance=None):
    return build_planning_value(
        site={"state": "Melaka", "district": "Melaka Tengah", "pbt": "Majlis Bandaraya Melaka Bersejarah", "lot_no": "11213", "tod_distance_m": 220},
        final_status=status,
        policy_coverage={"coverage": coverage},
        site_analysis={"score": 86 if status == "COMPLY" else 40, "recommendation": {"reason": "assessment result"}},
        evidence_intelligence={"items": evidence or []},
        retrieved_rules=[{"rule_id": "R1"}] if coverage == "FULL_RULE_ENGINE" else [],
        compliance_results=compliance if compliance is not None else ([{"rule_id": "R1", "status": status, "reason": "Control result"}] if status != "REQUIRES REVIEW" else []),
    )


def test_planning_value_compliance_is_actionable():
    result = _build("COMPLY", evidence=[{"source": "MyGEMS", "status": "PLANNED", "evidence": "Geology"}])
    assert result["band"] == "READY FOR FURTHER REVIEW"
    assert result["next_actions"]
    assert result["decision_drivers"]
    assert result["disclaimer"]


def test_planning_value_non_compliance_prioritises_redesign():
    result = _build("NON-COMPLIANCE", compliance=[{"rule_id": "R1", "status": "NON-COMPLIANCE", "reason": "Height exceeds verified control"}])
    assert result["band"] == "BLOCKED"
    assert result["next_actions"]
    assert "redesign" in result["headline"].lower()


def test_planning_value_non_mbmb_requires_evidence():
    result = _build("REQUIRES REVIEW", coverage="SPATIAL_DEMO_ONLY", evidence=[{"source": "PBT GIS / MelGIS", "status": "DISCOVERY_COMPLETE", "evidence": "Parcel / zoning architecture"}], compliance=[{"rule_id": None, "status": "REQUIRES REVIEW", "reason": "Local statutory rule set is not loaded."}])
    assert result["band"] == "REVIEW"
    assert any("local planning" in x.lower() for x in result["next_actions"])
