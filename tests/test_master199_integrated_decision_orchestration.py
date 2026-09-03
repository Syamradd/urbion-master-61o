from pathlib import Path

from fastapi.testclient import TestClient

from server import app


BASE = {
    "site_lat": 2.2, "site_lon": 102.25,
    "tod_lat": 2.205, "tod_lon": 102.255,
    "development_type": "Mixed Use", "development_class": "Mixed Use",
    "state": "Melaka", "district": "Melaka Tengah",
    "pbt": "Majlis Bandaraya Melaka Bersejarah",
}


def test_master199_contract_is_documented():
    text = Path('MASTER-199-INTEGRATED-DECISION-ORCHESTRATION.md').read_text(encoding='utf-8')
    for token in ('Integrated Decision Orchestration', 'What-If', 'Decision Center', 'NOT_CLAIMED', 'capped at 12'):
        assert token in text


def test_lcp_intelligence_integrates_decision_center():
    client = TestClient(app)
    response = client.post('/lcp/intelligence', json={
        "assessment": BASE,
        "development_inputs": {"units": 100, "site_area_ha": 2, "daily_trips": 400},
        "policy_links": [{"domain":"physical", "impact":"Flood exposure", "issue":"Flood risk", "reference":"RT MBMB 2035", "strategy":"Review drainage mitigation", "sdg":"SDG 11"}],
        "station_snapshot": {"status":"LIVE", "evidence":"SOURCE_CONTEXT"},
    })
    assert response.status_code == 200
    body = response.json()
    assert body['version'] == 'MASTER-199'
    assert body['decision_center']['statutory_verification'] == 'NOT_CLAIMED'
    assert body['decision_center']['decision']['status'] == body['assessment']['final_status']
    assert 'what_if' in body
    assert body['what_if']['status'] == 'NOT_PROVIDED'


def test_lcp_intelligence_integrates_what_if_into_decision_center():
    client = TestClient(app)
    response = client.post('/lcp/intelligence', json={
        "assessment": BASE,
        "scenario_variants": [{"id":"LOWER-INTENSITY", "name":"Lower intensity", "overrides":{"plot_ratio":2.5}}],
    })
    assert response.status_code == 200
    body = response.json()
    assert body['what_if']['best_candidate'] == 'LOWER-INTENSITY'
    assert body['decision_center']['what_if']['best_candidate'] == 'LOWER-INTENSITY'
    assert body['what_if']['scenarios'][0]['id'] == 'LOWER-INTENSITY'
    assert body['statutory_verification'] == 'NOT_CLAIMED'


def test_lcp_intelligence_rejects_invalid_scenario_variants():
    client = TestClient(app)
    response = client.post('/lcp/intelligence', json={"assessment": BASE, "scenario_variants": {"bad": True}})
    assert response.status_code == 422
    assert response.json()['detail']['code'] == 'INVALID_SCENARIO_VARIANTS'


def test_lcp_intelligence_rejects_more_than_12_scenarios():
    client = TestClient(app)
    variants = [{"id": f"S{i}"} for i in range(13)]
    response = client.post('/lcp/intelligence', json={"assessment": BASE, "scenario_variants": variants})
    assert response.status_code == 422
    assert response.json()['detail']['code'] == 'INVALID_SCENARIO_VARIANTS'
