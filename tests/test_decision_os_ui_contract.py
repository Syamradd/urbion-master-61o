from fastapi.testclient import TestClient

from championship_server import app


def test_decision_os_ui_asset_is_reachable():
    response = TestClient(app).get('/urbion_decision_os_ui.js')
    assert response.status_code == 200
    assert 'SIGMA · DECISION OS' in response.text
    assert '/intelligence/decision-os' in response.text
