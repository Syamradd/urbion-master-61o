from fastapi.testclient import TestClient

from championship_server import app


REQUIRED_ASSETS = (
    'urbion_championship_input_sync.js',
    'urbion_championship_spatial_studio.js',
    'urbion_championship_intelligence_upgrade.js',
    'urbion_championship_decision_layer.js',
    'urbion_championship_workflow.js',
    'urbion_championship_decision_chain.js',
    'urbion_spatial_workstation_upgrade.js',
    'urbion_spatial_implication_bridge.js',
    'urbion_championship_workstation_v2.js',
    'urbion_decision_intelligence_ui.js',
)


def test_championship_root_keeps_single_same_origin_workflow_stack():
    client = TestClient(app)
    root = client.get('/')
    assert root.status_code == 200
    html = root.text
    assert 'PHASE-E.8 ENGINE ONLINE' in html
    for asset in REQUIRED_ASSETS:
        assert f'src="/{asset}"' in html


def test_workstation_ui_exposes_core_judge_workflow_and_guardrail_copy():
    client = TestClient(app)
    workstation = client.get('/urbion_championship_workstation_v2.js')
    assert workstation.status_code == 200
    js = workstation.text
    for label in ('Assessment', 'Spatial', 'What-If', 'Decision', 'LCP', 'KM'):
        assert label in js
    assert 'RUN ANALYSIS' in js
    assert '/workstation/analysis' in js
    assert 'does not claim statutory approval' in js


def test_decision_ui_and_workflow_assets_are_reachable():
    client = TestClient(app)
    for asset in ('urbion_decision_intelligence_ui.js', 'urbion_championship_decision_chain.js', 'urbion_championship_workflow.js'):
        response = client.get('/' + asset)
        assert response.status_code == 200
        assert response.text.strip()
