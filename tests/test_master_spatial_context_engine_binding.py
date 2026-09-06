from fastapi.testclient import TestClient

from championship_server import app


def test_spatial_intelligence_accepts_live_environment_context():
    client = TestClient(app)
    response = client.post('/spatial/intelligence', json={
        'site_lat': 2.285,
        'site_lon': 102.196,
        'tod_lat': 2.286,
        'tod_lon': 102.197,
        'environmental_context': {
            'layers': {
                'iplan-flood': {'status': 'LIVE_QUERY', 'feature_count': 2},
                'mygems-lithology': {'status': 'NO_FEATURE', 'feature_count': 0},
            }
        },
    })
    assert response.status_code == 200
    body = response.json()
    assert body['environment']['layers']['iplan-flood']['status'] == 'LIVE_QUERY'
    assert any(x['id'] == 'environment_iplan-flood' for x in body['planning_signals'])
    assert body['evidence_model']['environmental_overlay'] == 'SOURCE_CONTEXT ONLY'
