from urbion_policy_graph import build_policy_graph


def test_policy_graph_keeps_traceable_reference_chain():
    result = build_policy_graph(
        impacts={"physical": [{"id": "flood_exposure"}], "social": [{"id": "facility_access"}]},
        policy_links=[{"domain": "physical", "impact": "flood_exposure", "issue": "Flood-sensitive development", "level": "LOCAL", "reference": "RT MBMB 2035", "clause": "provided-by-planner", "strategy": "Flood-sensitive planning", "sdg": "SDG 11", "evidence": "SOURCE_CONTEXT", "status": "REVIEW_REQUIRED"}],
        national_links=[{"domain": "social", "impact": "facility_access", "level": "NATIONAL", "reference": "National planning reference", "evidence": "SOURCE_CONTEXT"}],
    )
    assert result["edge_count"] == 2
    assert "physical" in result["linked_domains"]
    assert "social" in result["linked_domains"]
    assert result["statutory_verification"] == "NOT_CLAIMED"


def test_missing_policy_reference_is_review_gap_not_fabricated():
    result = build_policy_graph(impacts={"economic": [{"id": "employment"}]}, policy_links=[{"domain": "economic"}])
    assert "POLICY_REFERENCE_REQUIRED" in result["review_gaps"]
    assert result["edge_count"] == 0


def test_unlinked_impact_domain_is_flagged():
    result = build_policy_graph(impacts={"physical": [{"id": "road_access"}]})
    assert "physical:POLICY_LINK_REQUIRED" in result["review_gaps"]
