from fastapi.testclient import TestClient

from championship_server import app


def test_championship_workstation_ui_asset_is_served_and_injected():
    client = TestClient(app)
    root = client.get('/')
    assert root.status_code == 200
    assert '/urbion_championship_workstation_v2.js' in root.text
    asset = client.get('/urbion_championship_workstation_v2.js')
    assert asset.status_code == 200
    assert 'Decision chain control' in asset.text
    assert '/workstation/analysis' in asset.text


def test_spatial_endpoint_is_reachable_from_production_entrypoint():
    client = TestClient(app)
    response = client.post('/spatial/intelligence', json={
        'site_lat': 2.285, 'site_lon': 102.196,
        'tod_lat': 2.286, 'tod_lon': 102.197,
    })
    assert response.status_code == 200
    assert response.json()['project'] == 'URBION HORIZON'
