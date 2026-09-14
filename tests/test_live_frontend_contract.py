from fastapi.testclient import TestClient

from landing_server import app


client = TestClient(app)


def test_root_serves_public_welcome_contract():
    response = client.get('/')
    assert response.status_code == 200
    assert 'URBION HORIZON' in response.text
    assert 'AI-Assisted Urban Planning Intelligence' in response.text
    assert 'START PLANNING' in response.text
    assert 'Spatial Intelligence' in response.text
    assert 'ABOUT URBION HORIZON' in response.text
    assert 'href="/workspace"' in response.text


def test_health_exposes_frontend_identity():
    payload = client.get('/health').json()
    assert payload['status'] == 'healthy'
    assert payload['engine'] == 'URBION PHASE-E.8'
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
