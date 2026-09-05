from fastapi.testclient import TestClient

from championship_server import app


def _inputs():
    return {
        "site_lat": 2.1896,
        "site_lon": 102.2501,
        "tod_lat": 2.1961,
        "tod_lon": 102.2460,
        "development_type": "residential",
        "plot_ratio": 2.0,
    }


def test_planner_handoff_is_review_bounded():
    client = TestClient(app)
    response = client.post('/planner/handoff', json={"assessment_inputs": _inputs()})
    assert response.status_code == 200
    body = response.json()
    assert body['project'] == 'URBION HORIZON'
    assert body['mode'] == 'BOUNDED_PLANNER_COPILOT'
    handoff = body['handoff']
    assert handoff['workflow'][-1] == 'HANDOFF'
    assert handoff['decision_authority'] == 'NONE'
    assert handoff['statutory_verification'] == 'NOT_CLAIMED'
    assert handoff['boundary']
    assert isinstance(handoff['priority_actions'], list)


def test_planner_handoff_accepts_variants():
    client = TestClient(app)
    response = client.post('/planner/handoff', json={
        "assessment_inputs": _inputs(),
        "variants": [{"id": "v1", "name": "Lower density", "overrides": {"plot_ratio": 1.5}}],
    })
    assert response.status_code == 200
    handoff = response.json()['handoff']
    assert handoff['scenario_summary']['executed'] >= 1


def test_planner_handoff_requires_site():
    client = TestClient(app)
    response = client.post('/planner/handoff', json={"assessment_inputs": {"plot_ratio": 2.0}})
    assert response.status_code == 422
    assert response.json()['detail']['code'] == 'SITE_INPUT_REQUIRED'
