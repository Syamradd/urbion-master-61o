from pathlib import Path
from fastapi.testclient import TestClient

from server import app


def test_night_release_engine_identity_and_core_chain():
    client = TestClient(app)
    health = client.get('/health').json()
    assert health['status'] == 'healthy'
    assert health['engine'] == 'URBION PHASE-E.8'
    meta = client.get('/metadata').json()
    assert meta['version'] == 'PHASE-E.8'
    assert meta['decision_layer']
    assert meta['evidence_model'] == ['USER_PROVIDED', 'CALCULATED', 'SOURCE_CONTEXT', 'VERIFIED', 'UNVERIFIED']


def test_night_release_spatial_policy_decision_chain():
    client = TestClient(app)
    payload = {
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
        'lot_no': '11213',
    }
    assessment = client.post('/assess', json=payload)
    assert assessment.status_code == 200
    body = assessment.json()
    assert body['version'] == 'PHASE-E.8'
    assert body['classification'] in {'TOD 400m', 'TOD 800m', 'OUTSIDE TOD 800m'}
    assert 'policy_coverage' in body
    assert 'compliance_results' in body
    assert 'recommendation' in body
    assert 'decision_trace' in body
    assert body['evidence_state']['statutory_verification'] == 'NOT_CLAIMED'


def test_night_release_scenario_and_decision_surfaces():
    client = TestClient(app)
    payload = {
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
        'lot_no': '11213',
    }
    what_if = client.post('/what-if', json={'baseline': payload, 'variants': []})
    assert what_if.status_code == 200
    decision = client.post('/decision-center', json=payload)
    assert decision.status_code == 200
    judge = client.get('/judge-mode')
    assert judge.status_code == 200
    assert judge.json()['version'] == 'PHASE-E.8'
    gate = client.get('/championship-gate')
    assert gate.status_code == 200


def test_night_release_spatial_and_source_surfaces():
    client = TestClient(app)
    layers = client.get('/map/layers?state=Melaka')
    assert layers.status_code == 200
    data = layers.json()
    assert data['layers']
    assert {'toggle', 'opacity', 'identify', 'legend', 'fit-to-site', 'measure-distance', 'measure-area', 'basemap', 'share-location'} <= set(data['layer_controls'])
    sources = client.get('/sources')
    assert sources.status_code == 200
    public = client.get('/public-sources/map-services')
    assert public.status_code == 200
    assert public.json()['statutory_verification'] == 'NOT_CLAIMED'


def test_night_release_ui_workstation_and_judge_assets():
    client = TestClient(app)
    root = client.get('/')
    assert root.status_code == 200
    html = root.text
    for token in (
        'URBION HORIZON — Championship Workstation',
        'PHASE-E.8 ENGINE ONLINE',
        'urbion_ui.js',
        'urbion_championship_ui.js',
        'urbion_championship_upgrade.js',
        'window.__URBION_FRONTEND_BOOT__',
    ):
        assert token in html
    for page in ('map-studio.html', 'what-if.html', 'decision-center.html', 'planner-review.html', 'lcp-intelligence.html', 'judge-mode.html'):
        response = client.get('/' + page)
        assert response.status_code == 200, page


def test_night_release_no_stale_phase_e7_in_release_contracts():
    root = Path(__file__).resolve().parents[1]
    candidates = [
        root / 'tests/test_live_frontend_contract.py',
        root / 'tests/test_master191_deployment_smoke.py',
        root / 'tests/test_master192_judge_run.py',
    ]
    for path in candidates:
        text = path.read_text(encoding='utf-8')
        assert 'URBION PHASE-E.7' not in text, str(path)
