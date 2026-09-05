from fastapi.testclient import TestClient

from championship_server import app


def test_validation_cases_are_canonical_and_ordered():
    client = TestClient(app)
    response = client.get('/validation/cases')
    assert response.status_code == 200
    body = response.json()
    assert body['project'] == 'URBION HORIZON'
    assert [case['id'] for case in body['cases']] == ['TC-01', 'TC-02', 'TC-03']


def test_validation_cases_execute_real_production_paths():
    client = TestClient(app)
    for case_id in ('TC-01', 'TC-02', 'TC-03'):
        response = client.post(f'/validation/run/{case_id}')
        assert response.status_code == 200
        card = response.json()['evidence_card']
        assert card['validation_path']
        if case_id == 'TC-01':
            assert 'spatial' in card
            assert card['spatial']['statutory_verification'] == 'NOT_CLAIMED'
        elif case_id == 'TC-02':
            assert 'rules' in card['assessment']
            assert card['assessment']['rules']['retrieved_count'] >= 0
        else:
            assert card['guardrails']['decision_authority'] == 'NONE'
            assert card['mode'] == 'BOUNDED_PLANNER_COPILOT'
            assert card['evidence_ledger']['total_items'] >= 1


def test_validation_unknown_case_is_404():
    client = TestClient(app)
    response = client.post('/validation/run/TC-99')
    assert response.status_code == 404
    assert response.json()['detail']['code'] == 'VALIDATION_CASE_NOT_FOUND'
