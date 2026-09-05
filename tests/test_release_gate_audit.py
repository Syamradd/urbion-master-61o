import json
from pathlib import Path

from fastapi.testclient import TestClient
from championship_server import app


ROOT = Path(__file__).resolve().parents[1]


def test_release_manifest_keeps_explicit_authority_and_verification_boundaries():
    manifest = json.loads((ROOT / 'DEPLOYMENT_MANIFEST.json').read_text(encoding='utf-8'))
    assert manifest['project'] == 'URBION HORIZON'
    assert manifest['engine_version'] == 'PHASE-E.8'
    assert manifest['decision_authority'] == 'NONE'
    assert manifest['statutory_verification'] == 'NOT_CLAIMED'
    assert manifest['deployment_ready'] is True
    assert 'NOT AUTOMATIC STATUTORY VERIFICATION' in manifest['evidence_policy'].upper()


def test_production_frontend_contract_serves_same_origin_assets():
    client = TestClient(app)
    root = client.get('/')
    assert root.status_code == 200
    assert 'urbion_championship_workstation_v2.js' in root.text
    asset = client.get('/urbion_championship_workstation_v2.js')
    assert asset.status_code == 200
    assert '/workstation/analysis' in asset.text


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
