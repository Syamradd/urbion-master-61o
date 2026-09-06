from fastapi.testclient import TestClient

import urbion_spatial_context as ctx
from championship_server import app


def _fake_geojson(layer_name="demo"):
    return {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {"NAME": layer_name, "USE": "Commercial"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[102.195, 2.284], [102.197, 2.284], [102.197, 2.286], [102.195, 2.286], [102.195, 2.284]]],
            },
        }],
    }


def test_site_context_keeps_source_geometry_and_calculated_relationship(monkeypatch):
    ctx.clear_spatial_context_cache()
    monkeypatch.setattr(ctx, "_http_json", lambda url, params: _fake_geojson(params.get("typeName", "arcgis")))
    body = ctx.build_site_context(2.285, 102.196, 800, "Melaka", ["iplan-current"])
    layer = body["layers"][0]
    assert layer["status"] == "LIVE_QUERY"
    assert layer["feature_count"] == 1
    assert layer["inside_count"] == 1
    assert layer["features"][0]["geometry"]["type"] == "Polygon"
    assert layer["decision_safe"] is False
    assert body["query"]["parallel"] is True


def test_site_context_endpoint_discloses_query_errors(monkeypatch):
    ctx.clear_spatial_context_cache()
    def fail(*_args, **_kwargs):
        raise RuntimeError("source unavailable")
    monkeypatch.setattr(ctx, "_http_json", fail)
    client = TestClient(app)
    response = client.post("/spatial/site-context", json={
        "site_lat": 2.285,
        "site_lon": 102.196,
        "radius_m": 800,
        "state": "Melaka",
        "layer_ids": ["mygems-faults"],
    })
    assert response.status_code == 200
    layer = response.json()["layers"][0]
    assert layer["status"] == "QUERY_ERROR"
    assert layer["evidence"] == "EVIDENCE_GAP"
    assert layer["decision_safe"] is False


def test_site_context_rejects_placeholder_coordinates():
    client = TestClient(app)
    response = client.post("/spatial/site-context", json={"site_lat": -90, "site_lon": -180})
    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "INVALID_SPATIAL_INPUT"
