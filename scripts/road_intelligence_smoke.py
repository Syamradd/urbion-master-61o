from urbion_road_intelligence import build_road_intelligence


def main():
    packet = build_road_intelligence(
        site_lat=2.2000,
        site_lon=102.2500,
        nearest_road_name="Example Road",
        nearest_road_distance_m=125.0,
        road_hierarchy="ARTERIAL",
        road_source="EXPLICIT_GEOSPATIAL_SOURCE",
        centres=[
            {"name": "Local Centre", "type": "LOCAL", "distance_km": 2.0, "source": "EXPLICIT_PLACE_SOURCE"},
            {"name": "District Centre", "type": "DISTRICT", "distance_km": 12.5, "source": "EXPLICIT_PLACE_SOURCE"},
        ],
    )
    assert packet["version"] == "ROAD-1.0"
    road = packet["road_access"]["nearest_road"]
    assert road["distance_km"] == 0.125
    assert road["hierarchy"] == "ARTERIAL"
    assert road["evidence_status"] == "SOURCE_CONTEXT"
    assert packet["centre_proximity"][0]["name"] == "Local Centre"
    assert packet["centre_proximity"][1]["distance_km"] == 12.5
    assert packet["radius_analysis"][0]["radius_km"] == 1
    assert packet["radius_analysis"][-1]["radius_km"] == 50
    print("ROAD INTELLIGENCE CONTRACT PASS")


if __name__ == "__main__":
    main()
