from urbion_planning_value import build_planning_value


def _base(status="COMPLY", coverage="FULL_RULE_ENGINE"):
    return build_planning_value(
        site={"state":"Melaka","district":"Melaka Tengah","pbt":"Majlis Bandaraya Melaka Bersejarah","lot_no":"11213","tod_distance_m":220},
        final_status=status,
        policy_coverage={"coverage":coverage},
        retrieved_rules=[{"rule_id":"RT-MBMB-2035-TOD-01"}] if coverage == "FULL_RULE_ENGINE" else [],
        compliance_results=[{"rule_id":"RT-MBMB-2035-TOD-01","status":status,"applicability":"APPLICABLE","reason":"test reason"}] if status != "REQUIRES REVIEW" else [{"rule_id":"R-01","status":"REQUIRES REVIEW","applicability":"APPLICABLE","reason":"verification gap"}],
        site_analysis={"score":82.0,"recommendation":{"reason":"screening result"}},
        evidence_intelligence={"items":[{"source":"Manual Planner Verification","status":"AVAILABLE","evidence":"Site observation"},{"source":"MyGEMS","status":"QUERY_UNAVAILABLE","evidence":"Geology / lithology"}]},
    )


def test_compliance_generates_actionable_next_steps():
    result = _base("COMPLY")
    assert result["band"] == "READY FOR FURTHER REVIEW"
    assert result["next_actions"]
    assert result["evidence_gaps"]
    assert "approval" in result["disclaimer"].lower()


def test_non_compliance_is_blocked_and_points_to_redesign():
    result = _base("NON-COMPLIANCE")
    assert result["band"] == "BLOCKED"
    assert result["blockers"]
    assert any("Re-run URBION" in action for action in result["next_actions"])


def test_non_mbmb_requires_local_policy_evidence():
    result = build_planning_value(
        site={"state":"Selangor","district":"Klang","pbt":"Majlis Bandaraya DiRaja Klang","lot_no":"DEMO-01","tod_distance_m":500},
        final_status="REQUIRES REVIEW",
        policy_coverage={"coverage":"SPATIAL_DEMO_ONLY"},
        retrieved_rules=[],
        compliance_results=[{"status":"REQUIRES REVIEW","rule_id":None,"reason":"Local statutory rule set is not loaded."}],
        site_analysis={"score":61.0,"recommendation":{"reason":"Local statutory rules are not loaded."}},
        evidence_intelligence={"items":[{"source":"PBT GIS / MelGIS","status":"DISCOVERY_COMPLETE","evidence":"Parcel / zoning / land-use architecture"}]},
    )
    assert result["band"] == "REVIEW"
    assert any("local planning policy" in x.lower() for x in result["next_actions"])
