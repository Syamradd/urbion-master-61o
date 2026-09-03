from pathlib import Path
from fastapi.testclient import TestClient
from server import app
from urbion_development_impact import build_development_impact
from urbion_station_intelligence import build_station_intelligence


def test_invalid_coordinates_are_rejected_by_lcp():
    client = TestClient(app)
    r = client.post('/lcp/intelligence', json={'assessment': {'site_lat': 91, 'site_lon': 102.2, 'tod_lat': 2.2, 'tod_lon': 102.3}})
    assert r.status_code == 422


def test_missing_impact_inputs_are_review_gaps_not_fabricated():
    result = build_development_impact(development_type='Housing')
    assert result['review_gaps']
    assert result['statutory_verification'] == 'NOT_CLAIMED'


def test_unconfigured_station_adapters_do_not_fabricate_values():
    result = build_station_intelligence(2.2, 102.25, 'Melaka')
    assert result['review_gaps']
    assert result['statutory_verification'] == 'NOT_CLAIMED'


def test_frontend_has_explicit_boundary():
    text = Path('lcp-intelligence.html').read_text(encoding='utf-8')
    assert 'NOT_CLAIMED' in text
    assert 'review' in text.lower()
