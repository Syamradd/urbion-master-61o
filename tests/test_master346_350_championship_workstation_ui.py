from fastapi.testclient import TestClient

from landing_server import app


def test_canonical_workspace_ui_assets_are_served_and_injected():
    client = TestClient(app)
    workspace = client.get('/workspace')
    assert workspace.status_code == 200
    assert '<title>URBION HORIZON — Planning Workspace</title>' in workspace.text
    for asset in (
        '/urbion_workspace_bridge.js',
        '/urbion_workspace_runtime.js',
        '/urbion_layer_runtime_fix.js',
        '/urbion_workspace_canonical_ui.js',
        '/urbion_workspace_modal_owner.js',
        '/urbion_workspace_pbt_catalog.js',
        '/urbion_workspace_utility_owner.js',
        '/urbion_workspace_review_gaps_owner.js',
        '/urbion_workspace_environment_owner.js',
        '/urbion_workspace_mobility_owner.js',
        '/urbion_workspace_development_impact_owner_v4.js',
        '/urbion_workspace_ratio_owner.js',
        '/urbion_workspace_road_intelligence_owner.js',
        '/urbion_workspace_analysis_summary_owner.js',
        '/urbion_workspace_station_map_owner.js',
    ):
        response = client.get(asset)
        assert response.status_code == 200, asset
        assert response.text.strip(), asset


def test_spatial_endpoint_is_reachable_from_canonical_production_entrypoint():
    client = TestClient(app)
    response = client.post('/spatial/intelligence', json={
        'site_lat': 2.285, 'site_lon': 102.196,
        'tod_lat': 2.286, 'tod_lon': 102.197,
    })
    assert response.status_code == 200
    assert response.json()['project'] == 'URBION HORIZON'
