from fastapi.testclient import TestClient

from championship_server import app


def test_chapter5_canonical_cases_execute_from_production_surface():
    client = TestClient(app)
    listed = client.get('/validation/cases')
    assert listed.status_code == 200
    cases = listed.json()['cases']
    assert [case['id'] for case in cases] == ['TC-01', 'TC-02', 'TC-03']

    results = {}
    for case_id in ('TC-01', 'TC-02', 'TC-03'):
        response = client.post(f'/validation/run/{case_id}')
        assert response.status_code == 200
        body = response.json()
        assert body['case']['id'] == case_id
        assert body['result']
        assert body['evidence_card']['validation_path']
        results[case_id] = body

    assert 'spatial' in results['TC-01']['evidence_card']
    assert 'assessment' in results['TC-02']['evidence_card']
    assert 'evidence_ledger' in results['TC-03']['evidence_card']
    assert results['TC-03']['evidence_card']['evidence_ledger']['total_items'] >= 1
    assert results['TC-03']['evidence_card']['guardrails']['decision_authority'] == 'NONE'
    assert results['TC-03']['evidence_card']['guardrails']['statutory_verification'] == 'NOT_CLAIMED'
