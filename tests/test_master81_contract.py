from urbion_planning_value import build_planning_value


def _value(status, coverage="FULL_RULE_ENGINE", evidence=None):
    return build_planning_value(
        site={"state": "Melaka", "district": "Melaka Tengah", "pbt": "Majlis Bandaraya Melaka Bersejarah", "lot_no": "11213", "tod_distance_m": 220},
        final_status=status,
        policy_coverage={"coverage": coverage},
        retrieved_rules=[{"rule_id": "RT-MBMB-2035-TOD-01"}] if coverage == "FULL_RULE_ENGINE" else [],
        compliance_results=[{"rule_id": "R-01", "status": status, "applicability": "APPLICABLE", "reason": "control reason"}],
        site_analysis={"score": 82, "recommendation": {"reason": "assessment reason"}},
        evidence_intelligence={"items": evidence or []},
    )


def test_phase_c_schema_is_stable_and_traceable():
    result = _value("COMPLY", evidence=[{"source": "MyGEMS", "status": "QUERY_UNAVAILABLE", "evidence": "Geology"}])
    required = {"title", "version", "band", "score", "score_label", "headline", "status", "key_findings", "blockers", "decision_drivers", "evidence_gaps", "strengths", "next_actions", "rationale", "disclaimer"}
    assert required <= result.keys()
    assert result["version"] == "PHASE-C"
    assert result["status"] == "COMPLY"
    assert result["evidence_gaps"]
    assert "approval" in result["disclaimer"].lower()


def test_phase_c_non_compliance_never_looks_approved():
    result = _value("NON-COMPLIANCE")
    assert result["band"] == "BLOCKED"
    assert result["blockers"]
    assert result["next_actions"]
    assert "redesign" in result["headline"].lower()


def test_phase_c_not_applicable_has_reposition_path():
    result = _value("NOT APPLICABLE")
    assert result["band"] == "REPOSITION"
    assert any("development position" in action.lower() for action in result["next_actions"])


def test_phase_c_non_mbmb_explicitly_gates_local_policy():
    result = _value("REQUIRES REVIEW", coverage="SPATIAL_DEMO_ONLY", evidence=[{"source": "PBT GIS / MelGIS", "status": "DISCOVERY_COMPLETE", "evidence": "Parcel / zoning architecture"}])
    assert result["band"] == "REVIEW"
    assert any("local planning policy" in action.lower() for action in result["next_actions"])
    assert any("DISCOVERY_COMPLETE" in gap for gap in result["evidence_gaps"])
