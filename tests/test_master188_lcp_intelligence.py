from pathlib import Path

from fastapi.testclient import TestClient

from server import app


def assessment():
    return {
        "site": {"latitude": 2.2, "longitude": 102.25, "state": "Melaka", "district": "Melaka Tengah", "pbt": "Majlis Bandaraya Melaka Bersejarah", "lot_no": "Not specified"},
        "final_status": "REQUIRES REVIEW",
        "decision_confidence": {"level": "MEDIUM"},
        "recommendation": {"headline": "Planner review required"},
        "review_gaps": [],
    }


def test_master188_connects_end_to_end_trace():
    from urbion_lcp_intelligence import build_lcp_intelligence
    result = build_lcp_intelligence(
        assessment=assessment(),
        development_inputs={"development_type": "Mixed Use", "units": 120, "site_area_ha": 2.0, "daily_trips": 500, "road_distance_m": 80, "flood_exposure": True},
        spatial_inputs={"road_distance_m": 80, "elevation_m": 8, "flood_exposure": True, "source_context": {"iplan": {"status": "LIVE_QUERY"}}},
        policy_links=[{"domain": "physical", "impact": "Flood exposure", "issue": "Flood risk", "reference": "RT MBMB 2035", "strategy": "Apply flood mitigation and drainage review", "sdg": "SDG 11", "evidence": "SOURCE_CONTEXT"}],
        station_snapshot={"status": "LIVE", "evidence": "SOURCE_CONTEXT", "nearest": {"station_id": "26195"}},
        km_inputs={"pbt": "Majlis Bandaraya Melaka Bersejarah", "development_type": "Mixed Use", "km_category": "SEDERHANA", "documents": ["location plan", "site plan", "development proposal report"]},
    )
    assert result["version"] == "MASTER-199"
    assert result["statutory_verification"] == "NOT_CLAIMED"
    assert "WHAT-IF" in result["trace"]
    assert "DECISION CENTER" in result["trace"]


def test_master188_legacy_contract_is_superseded_by_master199():
    text = Path('MASTER-199-INTEGRATED-DECISION-ORCHESTRATION.md').read_text(encoding='utf-8')
    assert 'MASTER-199' in text
    assert 'MASTER-188' in text
