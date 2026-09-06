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

ACTIVE_ROOT_ASSETS = (
    'urbion_championship_premium_v3.js',
    'urbion_championship_final_command_center.js',
    'urbion_championship_final_command_center_hotfix.js',
    'urbion_championship_final_command_center_polish.js',
    'urbion_championship_final_command_center_policy.js',
    'urbion_championship_champion_review.js',
    'urbion_championship_unified_bridge.js',
    'urbion_championship_premium_v2.js',
    'urbion_championship_premium_v4.js',
)


def test_championship_root_keeps_single_curated_workflow_stack():
    client = TestClient(app)
    root = client.get('/')
    assert root.status_code == 200
    html = root.text
    assert 'PHASE-E.8 ENGINE ONLINE' in html
    assert 'window.__URBION_FRONTEND_BOOT__' in html
    assert 'release:"MASTER-331"' in html
    assert 'id="urbion-championship"' in html
    for asset in ACTIVE_ROOT_ASSETS:
        assert f'src="/{asset}"' in html
    for asset in LEGACY_ARCHIVE_ASSETS:
        assert f'src="/{asset}"' not in html
    for legacy_marker in ('Decision OS', 'Planner Workstation', 'Site + Development Inputs'):
        assert legacy_marker not in html


def test_archived_workstation_ui_remains_reachable_without_booting_on_root():
    client = TestClient(app)
    workstation = client.get('/urbion_championship_workstation_v2.js')
    assert workstation.status_code == 200
    js = workstation.text
    for label in ('Assessment', 'Spatial', 'What-If', 'Decision', 'LCP', 'KM'):
        assert label in js
    assert 'RUN ANALYSIS' in js
    assert '/workstation/analysis' in js
    assert 'does not claim statutory approval' in js


def test_decision_ui_and_workflow_assets_are_reachable_without_legacy_root_boot():
    client = TestClient(app)
    for asset in ('urbion_decision_intelligence_ui.js', 'urbion_championship_decision_chain.js', 'urbion_championship_workflow.js'):
        response = client.get('/' + asset)
        assert response.status_code == 200
        assert response.text.strip()
