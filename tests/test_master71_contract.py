from urbion_demo_scenarios import demo_scenarios
from urbion_evidence import summarise_sources, decision_trace


def test_demo_catalog_is_deterministic_and_complete():
    scenarios = demo_scenarios()
    assert len(scenarios) == 5
    ids = [item["id"] for item in scenarios]
    assert ids == ["TOD-COMPLY", "SHOP-COMPLY", "SHOP-FAIL", "OFFICE-REVIEW", "NON-MBMB"]
    assert len(set(ids)) == len(ids)
    for item in scenarios:
        assert item["name"]
        assert item["tag"]
        assert isinstance(item["inputs"], dict)


def test_evidence_policy_never_promotes_unsafe_states():
    registry = [
        {"source": "live", "status": "AVAILABLE", "evidence": ["verified"]},
        {"source": "planned", "status": "PLANNED", "evidence": ["planned"]},
        {"source": "portal", "status": "QUERY_UNAVAILABLE", "evidence": ["discovered"]},
        {"source": "gis", "status": "DISCOVERY_COMPLETE", "evidence": ["architecture"]},
    ]
    result = summarise_sources(registry)
    safe = {x["source"]: x["safe_for_decision"] for x in result["items"]}
    assert safe == {"live": True, "planned": False, "portal": False, "gis": False}


def test_decision_trace_always_closes_with_decision():
    trace = decision_trace("COMPLY", [{"rule_id": "R1"}], [{"rule_id": "R1"}], [{"rule_id": "R1"}])
    assert trace[-1]["stage"] == "DECISION"
    assert trace[-1]["status"] == "COMPLY"
    assert [x["stage"] for x in trace] == ["SITE", "SPATIAL", "POLICY", "APPLICABILITY", "COMPLIANCE", "DECISION"]
