from fastapi.testclient import TestClient

from server import app


client = TestClient(app)


def test_root_serves_live_frontend_contract():
    response = client.get('/')
    assert response.status_code == 200
    assert 'PHASE-E.7 ENGINE ONLINE' in response.text
    assert 'PHASE-E.7 LIVE DECISION LAYER' in response.text
    assert "const API=location.origin;" in response.text
    assert 'iplan:gunatanah_komited_04' in response.text


def test_health_exposes_frontend_identity():
    payload = client.get('/health').json()
    assert payload['status'] == 'healthy'
    assert payload['engine'] == 'URBION PHASE-E.7'
    assert payload['frontend'] == 'SERVING_INDEX_HTML'


def test_metadata_evidence_states_are_consistent():
    payload = client.get('/metadata').json()
    assert payload['evidence_model'] == [
        'USER_PROVIDED', 'CALCULATED', 'SOURCE_CONTEXT', 'VERIFIED', 'UNVERIFIED'
    ]


def test_map_layer_controls_are_declared():
    payload = client.get('/map/layers?state=Melaka').json()
    assert payload['layers']
    assert 'toggle' in payload['layer_controls']
    assert 'opacity' in payload['layer_controls']
