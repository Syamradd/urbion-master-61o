from urbion_planning_value import build_planning_value


def test_planning_value_compliance_is_actionable():
    result = build_planning_value(
        final_status="COMPLY",
        policy_coverage={"coverage": "FULL_RULE_ENGINE"},
        site_analysis={"score": 86, "band": "HIGH POTENTIAL"},
        evidence_intelligence={"counts": {"REFERENCE_REGISTERED": 1, "PLANNED": 2}},
        retrieved_rules=[{"rule_id": "R1"}],
        compliance_results=[{"rule_id": "R1", "status": "COMPLY", "reason": "Control satisfied"}],
    )
    assert result["readiness"]["band"] in {"READY FOR PLANNER REVIEW", "PROMISING"}
    assert result["next_actions"]
    assert result["decision_drivers"]
    assert result["disclaimer"]


def test_planning_value_non_compliance_prioritises_redesign():
    result = build_planning_value(
        final_status="NON-COMPLIANCE",
        policy_coverage={"coverage": "FULL_RULE_ENGINE"},
        site_analysis={"score": 40, "band": "REQUIRES FURTHER STUDY"},
        evidence_intelligence={"counts": {"REFERENCE_REGISTERED": 1}},
        retrieved_rules=[{"rule_id": "R1"}],
        compliance_results=[{"rule_id": "R1", "status": "NON-COMPLIANCE", "reason": "Height exceeds verified control"}],
    )
    assert result["readiness"]["band"] == "BLOCKED"
    assert result["next_actions"][0]["priority"] == "IMMEDIATE"
    assert "redesign" in result["next_actions"][0]["action"].lower()


def test_planning_value_non_mbmb_requires_evidence():
    result = build_planning_value(
        final_status="REQUIRES REVIEW",
        policy_coverage={"coverage": "SPATIAL_DEMO_ONLY"},
        site_analysis={"score": 62, "band": "REQUIRES FURTHER STUDY"},
        evidence_intelligence={"counts": {"PLANNED": 3, "QUERY_UNAVAILABLE": 1}},
        retrieved_rules=[],
        compliance_results=[],
    )
    assert result["readiness"]["band"] == "EVIDENCE GATED"
    assert any("local planning" in x["action"].lower() for x in result["next_actions"])
