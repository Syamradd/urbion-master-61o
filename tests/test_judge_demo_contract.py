from fastapi.testclient import TestClient
from championship_server import app


def test_judge_demo_returns_evidence_snapshot():
    client = TestClient(app)
    r = client.post('/judge/demo', json={'assessment_inputs': {
        'site_lat': 2.285, 'site_lon': 102.196,
        'tod_lat': 2.286, 'tod_lon': 102.197,
        'plot_ratio': 4.5, 'development_type': 'TOD Development / Mixed Use',
        'development_class': 'Mixed Use', 'state': 'Melaka',
        'district': 'Melaka Tengah', 'pbt': 'Majlis Bandaraya Melaka Bersejarah'
    }})
    assert r.status_code == 200
    body = r.json()
    assert body['demo_mode'] == 'CHAMPIONSHIP_JUDGE_DEMO'
    assert body['flow'][-1] == 'EVIDENCE LEDGER'
    assert body['guardrails']['decision_authority'] == 'NONE'
    assert body['guardrails']['statutory_verification'] == 'NOT_CLAIMED'
    assert body['snapshot']['evidence_items'] >= 1


def test_judge_demo_rejects_missing_site():
    client = TestClient(app)
    r = client.post('/judge/demo', json={'assessment_inputs': {'plot_ratio': 2.0}})
    assert r.status_code == 422
    assert r.json()['detail']['code'] == 'SITE_INPUT_REQUIRED'
