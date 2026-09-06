from fastapi.testclient import TestClient

from championship_server import app


INPUTS = {
    'site_lat': 2.285,
    'site_lon': 102.196,
    'tod_lat': 2.286,
    'tod_lon': 102.197,
    'plot_ratio': 4.5,
    'development_type': 'TOD Development / Mixed Use',
    'development_class': 'Mixed Use',
    'state': 'Melaka',
    'district': 'Melaka Tengah',
    'pbt': 'Majlis Bandaraya Melaka Bersejarah',
}


def test_final_judge_to_planner_e2e_preserves_evidence_and_guardrails():
    client = TestClient(app)
    variants = [
        {'id': 'v1', 'name': 'Lower Intensity', 'overrides': {'plot_ratio': 3.5}},
        {'id': 'v2', 'name': 'Higher Intensity', 'overrides': {'plot_ratio': 5.5}},
    ]
    judge = client.post('/judge/demo', json={'assessment_inputs': INPUTS})
    assert judge.status_code == 200
    packet = judge.json()
    assert packet['flow'] == ['ASSESSMENT', 'SPATIAL', 'KNOWLEDGE', 'IMPACT', 'SCENARIO', 'DECISION', 'EVIDENCE LEDGER']
    assert packet['guardrails']['decision_authority'] == 'NONE'
    assert packet['guardrails']['statutory_verification'] == 'NOT_CLAIMED'
    assert packet['snapshot']['evidence_items'] >= 1

    handoff = client.post('/planner/handoff', json={'assessment_inputs': INPUTS, 'variants': variants})
    assert handoff.status_code == 200
    body = handoff.json()
    assert body['project'] == 'URBION HORIZON'
    assert body['mode'] == 'BOUNDED_PLANNER_COPILOT'
    assert body['handoff']['workflow'][-1] == 'HANDOFF'
    assert body['handoff']['decision_authority'] == 'NONE'
    assert body['handoff']['statutory_verification'] == 'NOT_CLAIMED'
    assert body['copilot']['evidence_ledger']['total_items'] >= 1
    assert body['handoff']['review_items'] is not None


def test_final_e2e_rejects_missing_site_consistently():
    client = TestClient(app)
    for path in ('/judge/demo', '/planner/handoff', '/copilot/run'):
        response = client.post(path, json={'assessment_inputs': {'plot_ratio': 2.0}})
        assert response.status_code == 422
        assert response.json()['detail']['code'] == 'SITE_INPUT_REQUIRED'
