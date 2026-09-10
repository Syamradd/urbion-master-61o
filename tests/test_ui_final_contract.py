from fastapi.testclient import TestClient

from championship_server import app


LEGACY_ARCHIVE_ASSETS = (
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

CANONICAL_WORKSTATION_ASSETS = (
    'urbion_championship_command_shell.js',
    'urbion_horizon_language_contract.js',
    'urbion_map_identify_runtime.js',
    'urbion_championship_horizon_ui.js',
)


def test_championship_entrypoint_keeps_single_curated_workflow_stack():
    client = TestClient(app)
    root = client.get('/championship.html')
    assert root.status_code == 200
    html = root.text
    assert '<title>URBION HORIZON — Planning Command Centre</title>' in html
    assert 'PHASE-E.8 ENGINE ONLINE' in html
    assert 'window.__URBION_FRONTEND_BOOT__' in html
    assert 'release:"MASTER-331"' in html
    assert 'id="urbion-championship-shell"' in html
    for asset in CANONICAL_WORKSTATION_ASSETS:
        assert f'src="/{asset}"' in html
    for asset in LEGACY_ARCHIVE_ASSETS:
        assert f'src="/{asset}"' not in html
    for legacy_marker in ('Decision OS', 'Planner Workstation', 'Site + Development Inputs'):
        assert legacy_marker not in html


def test_public_landing_does_not_boot_the_workstation():
    client = TestClient(app)
    landing = client.get('/')
    assert landing.status_code == 200
    assert '<title>URBION HORIZON — Spatial Decision Intelligence</title>' in landing.text
    assert 'href="/championship.html"' in landing.text
    assert 'id="urbion-championship-shell"' not in landing.text


def test_archived_workstation_ui_remains_reachable_without_booting_on_landing():
    client = TestClient(app)
    workstation = client.get('/urbion_championship_workstation_v2.js')
    assert workstation.status_code == 200
    js = workstation.text
    for label in ('Assessment', 'Spatial', 'What-If', 'Decision', 'LCP', 'KM'):
        assert label in js
    assert 'RUN ANALYSIS' in js
    assert '/workstation/analysis' in js
    assert 'does not claim statutory approval' in js


def test_decision_ui_and_workflow_assets_are_reachable_without_legacy_boot():
    client = TestClient(app)
    for asset in ('urbion_decision_intelligence_ui.js', 'urbion_championship_decision_chain.js', 'urbion_championship_workflow.js'):
        response = client.get('/' + asset)
        assert response.status_code == 200
        assert response.text.strip()
