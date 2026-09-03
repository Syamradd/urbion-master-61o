from fastapi.testclient import TestClient

from server import app


BASE = {
    "site_lat": 2.2, "site_lon": 102.25,
    "tod_lat": 2.205, "tod_lon": 102.255,
    "development_type": "Mixed Use", "development_class": "Mixed Use",
    "state": "Melaka", "district": "Melaka Tengah",
    "pbt": "Majlis Bandaraya Melaka Bersejarah",
}


def test_lcp_intelligence_endpoint_contract():
    client = TestClient(app)
    response = client.post('/lcp/intelligence', json={
        "assessment": BASE,
        "development_inputs": {"units": 100, "site_area_ha": 2, "daily_trips": 400},
        "spatial_inputs": {"road_distance_m": 75, "elevation_m": 8, "flood_exposure": False},
        "policy_links": [{"domain":"physical", "impact":"Flood exposure", "issue":"Flood risk", "reference":"RT MBMB 2035", "strategy":"Review drainage mitigation", "sdg":"SDG 11"}],
        "station_snapshot": {"status":"LIVE", "evidence":"SOURCE_CONTEXT"},
    })
    assert response.status_code == 200
    body = response.json()
    assert body['version'] == 'MASTER-188'
    assert body['station_intelligence']['status'] == 'LIVE'
    assert body['policy_graph']['edge_count'] == 1
    assert body['recommendations']['recommendations']
    assert body['statutory_verification'] == 'NOT_CLAIMED'


def test_lcp_intelligence_endpoint_rejects_missing_assessment():
    client = TestClient(app)
    response = client.post('/lcp/intelligence', json={})
    assert response.status_code == 422
    assert response.json()['detail']['code'] == 'ASSESSMENT_INPUT_REQUIRED'
