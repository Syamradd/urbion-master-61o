from fastapi.testclient import TestClient
from server import app


def test_environment_engine_requires_missing_evidence_to_be_reviewed():
    client = TestClient(app)
    response = client.post('/environment/intelligence', json={'environment_context': {}})
    assert response.status_code == 200
    body = response.json()
    assert body['version'] == 'MASTER-226'
    assert body['status'] == 'EVIDENCE_REQUIRED'
    assert body['summary']['domain_count'] == 11
    assert body['summary']['screened_count'] == 0
    assert len(body['review_gaps']) == 11
    assert body['statutory_verification'] == 'NOT_CLAIMED'


def test_environment_engine_flags_explicit_flood_and_ksas_evidence():
    client = TestClient(app)
    response = client.post('/environment/intelligence', json={'environment_context': {
        'flood': {'value': True, 'evidence': 'SOURCE_CONTEXT', 'source': 'JPS Public Infobanjir'},
        'ksas': {'value': True, 'evidence': 'SOURCE_CONTEXT', 'source': 'PLANMalaysia i-Plan'},
        'slope': {'value': 12, 'evidence': 'CALCULATED', 'source': 'JMG NaTSIS'},
    }})
    assert response.status_code == 200
    body = response.json()
    assert body['status'] == 'RISK_FLAGGED'
    metrics = {item['id']: item for item in body['metrics']}
    assert metrics['flood']['risk_flag'] is True
    assert metrics['ksas']['risk_flag'] is True
    assert metrics['slope']['status'] == 'SCREENED'
    assert 'environment:flood' not in body['review_gaps']


def test_lcp_accepts_environment_context_and_surfaces_it():
    client = TestClient(app)
    assessment = {
        'site_lat': 2.285, 'site_lon': 102.196, 'tod_lat': 2.286, 'tod_lon': 102.197,
        'plot_ratio': 4.5, 'precinct': 'Terminal Sg. Udang',
        'development_type': 'TOD Development / Mixed Use', 'development_class': 'Mixed Use',
        'state': 'Melaka', 'district': 'Melaka Tengah',
        'pbt': 'Majlis Bandaraya Melaka Bersejarah', 'lot_no': '11213'
    }
    response = client.post('/lcp/intelligence', json={'assessment': assessment, 'environment_context': {
        'flood': {'value': False, 'evidence': 'SOURCE_CONTEXT'},
        'ksas': {'value': False, 'evidence': 'SOURCE_CONTEXT'},
    }})
    assert response.status_code == 200
    body = response.json()
    assert 'environment_intelligence' in body
    assert body['environment_intelligence']['summary']['screened_count'] == 2
    assert 'ENVIRONMENT/HAZARD' in body['trace']
