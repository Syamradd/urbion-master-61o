from urbion_rt_iplan import planning_source_evidence, bind_planning_sources

def test_reference_registered_is_decision_safe():
    item=planning_source_evidence(source="RT MBMB 2035",layer="RT",value="Reference",status="REFERENCE_REGISTERED")
    assert item["decision_safe"] is True

def test_empty_planning_binding_requires_evidence():
    assert bind_planning_sources(items=[])["status"] == "EVIDENCE_REQUIRED"
