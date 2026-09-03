from urbion_live_stations import build_live_station_snapshot, haversine_m


def test_master184_snapshot_contract_without_apims_configuration():
    result = build_live_station_snapshot(2.3, 102.2, "Melaka", 3)
    assert result["version"] == "MASTER-184"
    assert result["statutory_verification"] == "NOT_CLAIMED"
    assert result["air_quality"]["evidence"] == "SOURCE_CONTEXT"
    assert result["lcp_fields"] == ["station_name", "station_id", "distance_m", "reading", "unit", "timestamp", "status", "source", "evidence"]


def test_master184_distance_is_deterministic():
    assert haversine_m(2.3, 102.2, 2.3, 102.2) == 0.0
    assert haversine_m(2.3, 102.2, 2.31, 102.2) > 0


def test_master184_provider_values_never_become_verified():
    result = build_live_station_snapshot(2.3, 102.2, "Melaka", 1)
    assert result["jps_rainfall"]["evidence"] == "SOURCE_CONTEXT"
    assert result["air_quality"]["evidence"] == "SOURCE_CONTEXT"
