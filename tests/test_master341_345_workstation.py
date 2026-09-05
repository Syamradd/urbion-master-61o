from fastapi.testclient import TestClient

from championship_server import app


def _payload():
    return {
        'site_lat': 2.285, 'site_lon': 102.196,
        'tod_lat': 2.286, 'tod_lon': 102.197,
        'plot_ratio': 4.5,
        'precinct': 'Terminal Sg. Udang',
        'development_type': 'TOD Development / Mixed Use',
        'development_class': 'Mixed Use',
        'state': 'Melaka', 'district': 'Melaka Tengah',
        'pbt': 'Majlis Bandaraya Melaka Bersejarah', 'lot_no': '11213',
    }


def test_workstation_completes_decision_chain():
    client = TestClient(app)
    response = client.post('/workstation/analysis', json={
        'assessment_inputs': _payload(),
        'variants': [
            {'id':'LOWER_DENSITY','name':'Lower density','plot_ratio':3.5},
            {'id':'HIGHER_DENSITY','name':'Higher density','plot_ratio':5.0},
        ],
        'constraints': {'flood': False, 'ksas': False},
    })
    assert response.status_code == 200
    body = response.json()
    assert body['version'] == 'PHASE-E.8'
    assert body['workflow']['completed'] == body['workflow']['total']
    assert {'ASSESSMENT','SPATIAL','WHAT_IF','DECISION','LCP','KM'} <= {x['id'] for x in body['workflow']['steps']}
    assert len(body['what_if']['scenarios']) == 2
    assert body['decision_authority'] == 'NONE'
    assert body['statutory_verification'] == 'NOT_CLAIMED'


def test_workstation_requires_assessment_input():
    client = TestClient(app)
    response = client.post('/workstation/analysis', json={'variants': []})
    assert response.status_code == 422
    assert response.json()['detail']['code'] == 'ASSESSMENT_INPUT_REQUIRED'
