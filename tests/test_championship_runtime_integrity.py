from pathlib import Path
import shutil
import subprocess

from fastapi.testclient import TestClient

from championship_server import app

ROOT = Path(__file__).resolve().parents[1]
CRITICAL_ASSETS = (
    'urbion_championship_final_command_center.js',
    'urbion_championship_final_command_center_hotfix.js',
    'urbion_championship_final_command_center_polish.js',
    'urbion_championship_final_command_center_policy.js',
    'urbion_championship_champion_review.js',
    'urbion_championship_final_runtime_enforcer.js',
)


def test_critical_final_assets_exist_and_are_served_from_canonical_entrypoint():
    client = TestClient(app)
    root = client.get('/')
    assert root.status_code == 200
    html = root.text
    assert 'window.__URBION_FRONTEND_BOOT__' in html
    assert app.state.frontend_release == 'MASTER-331'
    assert app.state.frontend_entrypoint == 'championship.html'
    assert 'id="urbion-championship"' in html
    assert 'Site + Development Inputs' not in html
    for asset in CRITICAL_ASSETS:
        assert f'/{asset}' in html
        response = client.get(f'/{asset}')
        assert response.status_code == 200, asset
        assert response.headers['content-type'].startswith('application/javascript')
        assert response.text.strip(), asset


def test_canonical_root_has_no_legacy_dashboard_mount_markers():
    client = TestClient(app)
    html = client.get('/').text
    for marker in ('urbion-workstation-v2', 'urbion-decision-os', 'Decision OS', 'Planner Workstation'):
        assert marker not in html


def test_all_critical_final_javascript_assets_pass_node_syntax_check_when_available():
    node = shutil.which('node')
    if not node:
        return
    for asset in CRITICAL_ASSETS:
        subprocess.run(
            [node, '--check', str(ROOT / asset)],
            check=True,
            capture_output=True,
            text=True,
        )


def test_championship_workflow_javascript_passes_node_syntax_check_when_available():
    node = shutil.which('node')
    if not node:
        return
    subprocess.run(
        [node, '--check', str(ROOT / 'urbion_championship_workflow.js')],
        check=True,
        capture_output=True,
        text=True,
    )
