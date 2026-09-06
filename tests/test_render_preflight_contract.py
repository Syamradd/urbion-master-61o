import json
from pathlib import Path

from fastapi.testclient import TestClient
from championship_server import app


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_ROUTES = (
    '/health',
    '/assess',
    '/spatial/intelligence',
    '/copilot/run',
    '/workstation/analysis',
    '/planner/handoff',
    '/judge/demo',
)

ASSESSMENT = {
    'site_lat': 2.285,
    'site_lon': 102.196,
    'tod_lat': 2.286,
    'tod_lon': 102.197,
    'plot_ratio': 4.5,
    'precinct': 'Terminal Sg. Udang',
    'development_type': 'TOD Development / Mixed Use',
    'development_class': 'Mixed Use',
    'state': 'Melaka',
    'district': 'Melaka Tengah',
    'pbt': 'Majlis Bandaraya Melaka Bersejarah',
    'lot_no': '11213',
}


def test_render_manifest_uses_production_entrypoint_and_manual_deploy_gate():
    render = (ROOT / 'render.yaml').read_text(encoding='utf-8')
    assert 'name: urbion-master-61o' in render
    assert 'startCommand: uvicorn championship_server:app' in render
    assert 'healthCheckPath: /health' in render
    assert 'autoDeployTrigger: off' in render
    assert 'PYTHON_VERSION' in render
    assert 'GEMINI_API_KEY' in render


def test_release_manifest_and_production_surface_are_aligned():
    manifest = json.loads((ROOT / 'DEPLOYMENT_MANIFEST.json').read_text(encoding='utf-8'))
    assert manifest['project'] == 'URBION HORIZON'
    assert manifest['engine_version'] == 'PHASE-E.8'
    assert manifest['deployment_ready'] is True
    assert manifest['decision_authority'] == 'NONE'
    assert manifest['statutory_verification'] == 'NOT_CLAIMED'

    client = TestClient(app)
    assert client.get('/health').status_code == 200
    openapi = client.get('/openapi.json')
    assert openapi.status_code == 200
    documented_paths = set(openapi.json().get('paths', {}))
    assert set(REQUIRED_ROUTES).issubset(documented_paths)
    root = client.get('/')
    assert root.status_code == 200
    assert 'urbion_championship_workstation_v2.js' in root.text


def test_production_entrypoint_exposes_required_api_routes():
    client = TestClient(app)
    assert client.post('/spatial/intelligence', json=ASSESSMENT).status_code == 200
    assert client.post('/workstation/analysis', json={'assessment_inputs': ASSESSMENT, 'variants': []}).status_code == 200
    assert client.post('/copilot/run', json={'assessment_inputs': ASSESSMENT}).status_code == 200
    assert client.post('/planner/handoff', json={'assessment_inputs': ASSESSMENT, 'variants': []}).status_code == 200
    assert client.post('/judge/demo', json={'assessment_inputs': ASSESSMENT}).status_code == 200


def test_production_entrypoint_exposes_required_frontend_assets():
    client = TestClient(app)
    for asset in (
        'urbion_championship_workstation_v2.js',
        'urbion_decision_intelligence_ui.js',
        'urbion_championship_workflow.js',
        'urbion_championship_decision_chain.js',
    ):
        response = client.get('/' + asset)
        assert response.status_code == 200
        assert 'javascript' in response.headers.get('content-type', '')
