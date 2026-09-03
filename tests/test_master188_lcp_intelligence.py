from urbion_lcp_intelligence import build_lcp_intelligence


def assessment():
    return {
        "site": {"latitude": 2.2, "longitude": 102.25, "pbt": "Majlis Bandaraya Melaka Bersejarah"},
        "final_status": "CONDITIONAL RISK",
        "decision_confidence": "MEDIUM",
        "recommendation": "Planner review required",
        "review_gaps": [],
    }


def test_master188_connects_end_to_end_trace():
    result = build_lcp_intelligence(
        assessment=assessment(),
        development_inputs={"development_type": "Mixed Use", "units": 120, "site_area_ha": 2.0, "daily_trips": 500, "road_distance_m": 80, "flood_exposure": True},
        spatial_inputs={"road_distance_m": 80, "elevation_m": 8, "flood_exposure": True, "source_context": {"iplan": {"status": "LIVE_QUERY"}}},
        policy_links=[{"domain": "physical", "impact": "Flood exposure", "issue": "Flood risk", "reference": "RT MBMB 2035", "strategy": "Apply flood mitigation and drainage review", "sdg": "SDG 11", "evidence": "SOURCE_CONTEXT"}],
        station_snapshot={"status": "LIVE", "evidence": "SOURCE_CONTEXT", "nearest": {"station_id": "26195"}},
        km_inputs={"pbt": "Majlis Bandaraya Melaka Bersejarah", "development_type": "Mixed Use", "km_category": "SEDERHANA", "documents": ["location plan", "site plan", "development proposal report"]},
    )
    assert result["version"] == "MASTER-188"
    assert result["trace"].startswith("SITE → SPATIAL → STATION")
    assert result["development_impact"]["impacts"]["physical"]
    assert result["policy_graph"]["edge_count"] == 1
    assert result["recommendations"]["recommendations"][0]["policy_reference"] == "RT MBMB 2035"
    assert result["station_intelligence"]["status"] == "LIVE"
    assert result["km_readiness"]["readiness"] == "READY_FOR_WORKFLOW_REVIEW"
    assert result["statutory_verification"] == "NOT_CLAIMED"


def test_master188_missing_evidence_stays_reviewable():
    result = build_lcp_intelligence(assessment=assessment())
    assert result["review_gaps"]
    assert result["station_intelligence"]["evidence"] == "UNVERIFIED"
    assert result["development_impact"]["review_gaps"]
    assert result["policy_graph"]["review_gaps"]
    assert result["recommendations"]["review_gaps"]
