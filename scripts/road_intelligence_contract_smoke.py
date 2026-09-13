"""Contract smoke for Road Access workspace integration."""
from __future__ import annotations

from starlette.testclient import TestClient

from landing_server import app
from urbion_road_intelligence import build_road_intelligence


def main() -> None:
    sample = build_road_intelligence(
        site_lat=2.20,
        site_lon=102.25,
        nearest_road_name="TEST ARTERIAL",
        nearest_road_distance_m=850,
        road_hierarchy="arterial",
        road_source="TEST_SOURCE",
        centres=[
            {"name": "CENTRE-A", "type": "district", "lat": 2.201, "lon": 102.251, "source": "TEST_SOURCE"},
            {"name": "CENTRE-B", "type": "regional", "distance_km": 6.25, "source": "TEST_SOURCE"},
        ],
    )
    assert sample["version"] == "ROAD-1.0"
    assert sample["road_access"]["nearest_road"]["distance_km"] == 0.85
    assert sample["road_access"]["hierarchy_chain"] == ["SITE", "ARTERIAL"]
    assert len(sample["radius_analysis"]) == 5
    assert sample["centre_proximity"][0]["name"] == "CENTRE-A"
    assert sample["centre_proximity"][0]["evidence_status"] == "SOURCE_CONTEXT"
    assert any("CENTRE-A" in ring["centres_inside"] for ring in sample["radius_analysis"])

    client = TestClient(app)
    workspace = client.get("/workspace")
    assert workspace.status_code == 200, workspace.text
    assert "/urbion_workspace_road_intelligence_owner.js" in workspace.text

    asset = client.get("/urbion_workspace_road_intelligence_owner.js")
    assert asset.status_code == 200
    assert "__URBION_ROAD_INTELLIGENCE_OWNER_V1__" in asset.text

    response = client.post(
        "/road-intelligence",
        json={
            "site_lat": 2.20,
            "site_lon": 102.25,
            "nearest_road_name": "TEST ARTERIAL",
            "nearest_road_distance_m": 850,
            "road_hierarchy": "arterial",
            "road_source": "TEST_SOURCE",
            "centres": [
                {"name": "CENTRE-A", "type": "district", "lat": 2.201, "lon": 102.251, "source": "TEST_SOURCE"},
            ],
        },
    )
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["version"] == "ROAD-1.0"
    assert payload["road_access"]["nearest_road"]["evidence_status"] == "SOURCE_CONTEXT"
    assert len(payload["radius_analysis"]) == 5

    print("ROAD INTELLIGENCE INTEGRATION PASS")
    print({"workspace_asset": "PASS", "route": "PASS", "version": payload["version"], "radius_count": len(payload["radius_analysis"])})


if __name__ == "__main__":
    main()
