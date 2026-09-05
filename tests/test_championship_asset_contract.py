from fastapi.testclient import TestClient
from championship_server import app


def test_critical_championship_assets_are_same_origin_and_served():
    client = TestClient(app)
    for asset in ('urbion_championship_workstation_v2.js', 'urbion_decision_intelligence_ui.js', 'urbion_championship_workflow.js', 'urbion_championship_decision_chain.js'):
        response = client.get('/' + asset)
        assert response.status_code == 200
        assert 'javascript' in response.headers.get('content-type', '')


def test_championship_root_is_same_origin_entrypoint():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == 200
    body = response.text
    assert 'urbion_championship_workstation_v2.js' in body
    assert 'urbion_decision_intelligence_ui.js' in body
