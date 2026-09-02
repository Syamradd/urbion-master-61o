from fastapi.testclient import TestClient

from server import app


def test_root_serves_live_frontend_contract():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == 200
    assert 'PHASE-E.7 ENGINE ONLINE' in response.text
    assert 'PHASE-E.7 LIVE DECISION LAYER' in response.text
    assert "const API=location.origin;" in response.text
    assert 'iplan:gunatanah_komited_04' in response.text


def test_health_exposes_frontend_identity():
    client = TestClient(app)
    payload = client.get('/health').json()
    assert payload['status'] == 'healthy'
    assert payload['engine'] == 'URBION PHASE-E.7'
    assert payload['frontend'] == 'SERVING_INDEX_HTML'
