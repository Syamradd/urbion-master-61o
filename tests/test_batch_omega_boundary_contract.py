from fastapi.testclient import TestClient
from championship_server import app


def test_core_planner_surfaces_keep_boundary_contracts():
    client = TestClient(app)
    payload = {'assessment_inputs': {'site_lat': 2.285, 'site_lon': 102.196, 'tod_lat': 2.286, 'tod_lon': 102.197, 'plot_ratio': 4.5, 'precinct': 'Terminal Sg. Udang', 'development_type': 'TOD Development / Mixed Use', 'development_class': 'Mixed Use', 'state': 'Melaka', 'district': 'Melaka Tengah', 'pbt': 'Majlis Bandaraya Melaka Bersejarah', 'lot_no': '11213'}}
    for path in ('/copilot/run', '/planner/handoff', '/judge/demo'):
        response = client.post(path, json=payload)
        assert response.status_code == 200
        body = response.json()
        assert body.get('decision_authority') in (None, 'NONE') or body.get('guardrails', {}).get('decision_authority') == 'NONE'
        assert body.get('statutory_verification') in (None, 'NOT_CLAIMED') or body.get('guardrails', {}).get('statutory_verification') == 'NOT_CLAIMED'
