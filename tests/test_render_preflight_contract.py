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
    for path in REQUIRED_ROUTES:
        response = client.get(path) if path == '/health' else None
        if response is not None:
            assert response.status_code == 200
    root = client.get('/')
    assert root.status_code == 200
    assert 'urbion_championship_workstation_v2.js' in root.text


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
