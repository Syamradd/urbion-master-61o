from fastapi.testclient import TestClient

import urbion_spatial_context_api
from championship_server import app


def test_spatial_context_can_return_cadastral_without_external_network(monkeypatch):
    monkeypatch.setattr(
        urbion_spatial_context_api,
        "build_site_context",
        lambda *args, **kwargs: {"layers": [], "query": {"layer_count": 0}},
    )
    monkeypatch.setattr(
        urbion_spatial_context_api,
        "query_cadastral",
        lambda *args, **kwargs: {
            "id": "iplan-cadastral",
            "status": "LIVE_QUERY",
            "features": [{"type": "Feature", "properties": {"LOT": "123"}, "geometry": {"type": "Polygon", "coordinates": []}}],
            "source": "https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN/LOT_04/MapServer/0",
            "evidence": "SOURCE_CONTEXT",
            "decision_safe": False,
        },
    )
    response = TestClient(app).get(
        "/spatial/site-context",
        params={"site_lat": 2.20, "site_lon": 102.20, "state": "Melaka", "layers": "iplan-cadastral"},
    )
    assert response.status_code == 200
    layer = next(item for item in response.json()["layers"] if item["id"] == "iplan-cadastral")
    assert layer["status"] == "LIVE_QUERY"
    assert layer["features"][0]["properties"]["LOT"] == "123"
    assert layer["decision_safe"] is False
