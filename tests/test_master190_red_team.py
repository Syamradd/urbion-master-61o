from pathlib import Path
from fastapi.testclient import TestClient

from server import app


def test_red_team_rejects_non_finite_spatial_input():
    client = TestClient(app)
    r = client.post('/lcp/intelligence', json={"assessment": {"site_lat": "NaN", "site_lon": 102.2, "tod_lat": 2.2, "tod_lon": 102.3}})
    assert r.status_code == 422


def test_red_team_preserves_statutory_boundary_and_planner_status():
    client = TestClient(app)
    base={"site_lat":2.2,"site_lon":102.25,"tod_lat":2.205,"tod_lon":102.255,"development_type":"Mixed Use","development_class":"Mixed Use","state":"Melaka","district":"Melaka Tengah","pbt":"Majlis Bandaraya Melaka Bersejarah"}
    r=client.post('/lcp/intelligence',json={"assessment":base,"policy_links":[{"domain":"physical","reference":"RT MBMB 2035","issue":"<script>alert(1)</script>","strategy":"Review mitigation"}]})
    assert r.status_code == 200
    body=r.json()
    assert body['statutory_verification']=='NOT_CLAIMED'
    assert body['recommendations']['recommendations'][0]['status']=='PLANNER_REVIEW'


def test_red_team_frontend_escapes_remote_values():
    text=Path('lcp-intelligence.html').read_text(encoding='utf-8')
    assert "const esc=" in text
    assert ".replace(" in text
    assert "innerHTML" in text
    assert "esc(j.trace)" in text
    assert "esc(x.action)" in text
