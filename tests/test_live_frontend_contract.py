from fastapi.testclient import TestClient

from server import app


client = TestClient(app)


def test_root_serves_championship_frontend_contract():
    response = client.get('/')
    assert response.status_code == 200
    assert 'URBION HORIZON — Championship Workstation' in response.text
    assert 'CHAMPIONSHIP PLANNING WORKSTATION' in response.text
    assert 'PHASE-E.7 ENGINE ONLINE' in response.text
    assert 'id="urbion-championship"' in response.text
    assert 'urbion_championship_ui.js' in response.text
    assert 'urbion_championship_upgrade.js' in response.text
    assert "window.__URBION_FRONTEND_BOOT__" in response.text


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


def test_shared_ui_controller_is_present_and_non_destructive():
    response = client.get('/index.html')
    assert response.status_code == 200
    assert 'urbion_ui.js' in response.text or 'URBION_UI' in response.text
