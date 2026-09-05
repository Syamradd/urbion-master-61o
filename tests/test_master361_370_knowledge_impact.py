from urbion_knowledge_orchestrator import build_knowledge_pack
from urbion_impact_intelligence import build_impact_intelligence
from urbion_agent_orchestrator import run_agents


def test_knowledge_pack_is_traceable_and_authority_bounded():
    pack = build_knowledge_pack("residential", "MBMB")
    assert pack["mode"] == "DETERMINISTIC_RETRIEVAL"
    assert pack["generation_ready"] is True
    assert pack["evidence_boundary"] == "RETRIEVAL_IS_NOT_STATUTORY_VERIFICATION"
    assert all("source_document" in item for item in pack["source_register"])
    assert build_knowledge_pack("residential", "OTHER") ["candidate_rules"] == []


def test_impact_intelligence_never_upgrades_evidence():
    impact = build_impact_intelligence(spatial={"flood": {"status": "screening"}})
    assert impact["status"] == "REVIEW_REQUIRED"
    assert impact["evidence_state"] == "SOURCE_CONTEXT"
    assert impact["statutory_verification"] == "NOT_CLAIMED"
    assert impact["authority"] == "NONE"


def test_agent_chain_contains_knowledge_and_impact():
    assessment = {
        "site": {"latitude": 2.2, "longitude": 102.25},
        "development_type": "residential",
        "retrieved_rules": [],
        "compliance_results": [],
        "final_status": "REVIEW_REQUIRED",
    }
    result = run_agents(assessment=assessment, spatial={"flood": {"status": "screening"}})
    assert result["mode"] == "BOUNDED_MULTI_AGENT"
    assert result["decision_authority"] == "NONE"
    impact = next(a for a in result["agents"] if a["agent"] == "IMPACT")
    policy = next(a for a in result["agents"] if a["agent"] == "POLICY")
    assert impact["status"] == "REVIEW_REQUIRED"
    assert "knowledge" in policy["output"]
