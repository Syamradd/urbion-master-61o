from pathlib import Path

from fastapi.testclient import TestClient

from championship_server import app

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / 'urbion_map_identify_runtime.js'


def test_map_identify_runtime_is_served_by_canonical_root():
    client = TestClient(app)
    html = client.get('/').text
    assert '/urbion_map_identify_runtime.js' in html
    response = client.get('/urbion_map_identify_runtime.js')
    assert response.status_code == 200
    assert response.headers['content-type'].startswith('application/javascript')
    assert response.text.strip()


def test_map_identify_runtime_discovers_real_leaflet_layers_and_uses_same_origin_spatial_context():
    text = RUNTIME.read_text(encoding='utf-8')
    for token in (
        'window.__URBION_FCC_MAP__',
        'm._layers',
        '__urbionSource',
        '/spatial/site-context?',
        "item.status==='LIVE_QUERY'?'LIVE_QUERY':item.status",
        "evidence_state:item.evidence||'EVIDENCE_GAP'",
    ):
        assert token in text
    assert "credentials:'same-origin'" in text
    assert '/identify?' not in text


def test_map_identify_runtime_keeps_evidence_conservative():
    text = RUNTIME.read_text(encoding='utf-8')
    assert 'decision_safe:false' in text
    assert 'requires_rule_binding:true' in text
    assert 'statutory_approval_claim:false' in text
    assert 'rule_binding_required:true' in text


def test_map_identify_runtime_handles_query_errors_without_promoting_evidence():
    text = RUNTIME.read_text(encoding='utf-8')
    assert "query_status:'QUERY_ERROR'" in text
    assert "evidence_state:'REVIEW'" in text
    assert "decision_safe:false" in text
