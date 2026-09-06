from fastapi.testclient import TestClient

import urbion_spatial_api
from championship_server import app


def test_network_access_returns_source_context_without_statutory_claim(monkeypatch):
    monkeypatch.setattr(
        urbion_spatial_api,
        "network_distance_m",
        lambda *args, **kwargs: {
            "status": "LIVE_QUERY",
            "provider": "OSRM public routing service",
            "distance_m": 1320.5,
            "duration_s": 181.2,
            "evidence_state": "SOURCE_CONTEXT",
            "method": "network route",
        },
    )
    client = TestClient(app)
    response = client.post(
        "/spatial/network-access",
        json={"site_lat": 2.285, "site_lon": 102.196, "target_lat": 2.286, "target_lon": 102.197},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["network"]["evidence_state"] == "SOURCE_CONTEXT"
    assert body["network"]["distance_m"] == 1320.5
    assert body["decision_boundary"] == "NETWORK_MOBILITY_SCREENING"
    assert body["statutory_verification"] == "NOT_CLAIMED"


def test_network_access_validates_target():
    client = TestClient(app)
    response = client.post("/spatial/network-access", json={"site_lat": 2.285, "site_lon": 102.196})
    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "INVALID_NETWORK_TARGET"
