from urbion_agent_orchestrator import run_agents

def test_bounded_multi_agent_orchestrator_is_deterministic_and_guarded():
    assessment = {"site":{"latitude":2.285,"longitude":102.196},"development_type":"TOD Development / Mixed Use","retrieved_rules":[{"rule_id":"R1"}],"policy_coverage":{"status":"AVAILABLE"},"compliance_results":[{"status":"COMPLY"}],"final_status":"COMPLY"}
    spatial = {"classification":"TOD 400m","distance_m":157.0}
    scenarios = {"ranked_scenarios":[{"id":"LOWER_DENSITY"}]}
    decision = {"status":"COMPLY","confidence":{"score":0.8}}
    a = run_agents(assessment=assessment, spatial=spatial, scenarios=scenarios, decision=decision)
    b = run_agents(assessment=assessment, spatial=spatial, scenarios=scenarios, decision=decision)
    assert a == b
    assert a["mode"] == "BOUNDED_MULTI_AGENT"
    assert [x["agent"] for x in a["agents"]] == ["SITE","SPATIAL","POLICY","COMPLIANCE","IMPACT","SCENARIO","DECISION"]
    assert a["decision_authority"] == "NONE"
    assert a["statutory_verification"] == "NOT_CLAIMED"
    assert "IMPACT" in a["review_required"]
