from fastapi.testclient import TestClient

from championship_server import app


def _inputs():
    return {
        'site_lat': 2.1896,
        'site_lon': 102.2501,
        'tod_lat': 2.1961,
        'tod_lon': 102.2460,
        'development_type': 'residential',
        'plot_ratio': 2.0,
    }


def test_public_decision_surfaces_keep_authority_boundary_explicit():
    client = TestClient(app)
    for path, payload in [
        ('/intelligence/decision', _inputs()),
        ('/planner/handoff', {'assessment_inputs': _inputs()}),
    ]:
        response = client.post(path, json=payload)
        assert response.status_code == 200
        text = str(response.json())
        assert 'NOT_CLAIMED' in text
        assert 'NONE' in text


def test_invalid_site_coordinates_are_rejected_by_public_spatial_surface():
    client = TestClient(app)
    bad = _inputs()
    bad['site_lat'] = 999
    response = client.post('/spatial/intelligence', json=bad)
    assert response.status_code in (400, 422)


# Final-release retarget trigger: rerun this isolated audit against current main.
