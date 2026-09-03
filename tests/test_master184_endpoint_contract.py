from fastapi.testclient import TestClient

from server import app


def test_station_intelligence_endpoint_rejects_placeholder_coordinates():
    client = TestClient(app)
    response = client.get('/station-intelligence?site_lat=-90&site_lon=-180&state=Melaka')
    assert response.status_code == 422
    assert response.json()['detail']['code'] == 'INVALID_SPATIAL_INPUT'


def test_station_intelligence_endpoint_exposes_lcp_contract():
    client = TestClient(app)
    response = client.get('/station-intelligence?site_lat=2.2&site_lon=102.25&state=Melaka')
    assert response.status_code == 200
    body = response.json()
    assert body['status'] == 'LIVE_STATION_INTELLIGENCE'
    assert 'nearest' in body
    assert 'lcp_snapshot' in body
    assert 'review_gaps' in body
    assert body['statutory_verification'] == 'NOT_CLAIMED'
