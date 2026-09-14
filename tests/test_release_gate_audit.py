import json
from pathlib import Path

from fastapi.testclient import TestClient
from landing_server import app


ROOT = Path(__file__).resolve().parents[1]


def test_release_manifest_keeps_explicit_authority_and_verification_boundaries():
    manifest = json.loads((ROOT / 'DEPLOYMENT_MANIFEST.json').read_text(encoding='utf-8'))
    assert manifest['project'] == 'URBION HORIZON'
    assert manifest['engine_version'] == 'PHASE-E.8'
    assert manifest['decision_authority'] == 'NONE'
    assert manifest['statutory_verification'] == 'NOT_CLAIMED'
    assert manifest['deployment_ready'] is False
    assert 'HOLD_UNTIL_FINAL_MAIN_CI_AND_LIVE_QA' == manifest['release_gate']
    assert 'LIVE SOURCE CONTEXT IS NOT AUTOMATIC STATUTORY VERIFICATION' == manifest['evidence_policy'].upper()


def test_production_frontend_contract_serves_canonical_same_origin_assets():
    client = TestClient(app)
    root = client.get('/workspace')
    assert root.status_code == 200
    assert '<title>URBION HORIZON — Planning Workspace</title>' in root.text
    assert 'X-URBION-UI' not in root.text
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
        assert response.status_code == 200
        assert response.text.strip()


def test_production_health_and_assessment_remain_available():
    client = TestClient(app)
    health = client.get('/health')
    assert health.status_code == 200
    assert health.json()['status'] == 'healthy'
    assessment = client.post('/assess', json={
        'site_lat': 2.285,
        'site_lon': 102.196,
        'tod_lat': 2.286,
        'tod_lon': 102.197,
        'plot_ratio': 4.5,
        'development_type': 'TOD Development / Mixed Use',
        'development_class': 'Mixed Use',
        'state': 'Melaka',
        'district': 'Melaka Tengah',
        'pbt': 'Majlis Bandaraya Melaka Bersejarah',
    })
    assert assessment.status_code == 200
