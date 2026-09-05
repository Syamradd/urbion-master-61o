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


def test_championship_flow_is_connected_end_to_end():
    client = TestClient(app)
    inputs = _inputs()

    assessment = client.post('/assess', json=inputs)
    assert assessment.status_code == 200
    assessment_body = assessment.json()
    assert assessment_body['project'] == 'URBION HORIZON'

    spatial = client.post('/spatial/intelligence', json=inputs)
    assert spatial.status_code == 200
    spatial_body = spatial.json()
    assert spatial_body['project'] == 'URBION HORIZON'
    assert spatial_body['statutory_verification'] == 'NOT_CLAIMED'

    decision = client.post('/intelligence/decision', json=inputs)
    assert decision.status_code == 200
    decision_body = decision.json()
    assert decision_body['decision_authority'] == 'NONE'
    assert decision_body['statutory_verification'] == 'NOT_CLAIMED'

    handoff = client.post('/planner/handoff', json={
        'assessment_inputs': inputs,
        'variants': [
            {'id': 'v1', 'name': 'Lower density', 'overrides': {'plot_ratio': 1.5}},
        ],
    })
    assert handoff.status_code == 200
    handoff_body = handoff.json()['handoff']
    assert handoff_body['workflow'][-1] == 'HANDOFF'
    assert handoff_body['scenario_summary']['executed'] >= 1
    assert handoff_body['decision_authority'] == 'NONE'
    assert handoff_body['statutory_verification'] == 'NOT_CLAIMED'


def test_workstation_exposes_complete_decision_chain():
    client = TestClient(app)
    response = client.post('/workstation/analysis', json={
        'assessment_inputs': _inputs(),
        'variants': [
            {'id': 'v1', 'name': 'Lower density', 'overrides': {'plot_ratio': 1.5}},
        ],
    })
    assert response.status_code == 200
    body = response.json()
    assert body['project'] == 'URBION HORIZON'
    assert body['workflow'] == ['ASSESSMENT', 'SPATIAL', 'WHAT_IF', 'DECISION', 'LCP', 'KM', 'AGENTS']
    assert isinstance(body['agents'], list)
    assert len(body['agents']) == 7
