from urbion_station_contract import live_query_domains, station_source_contract


def test_myeqms_contract_is_machine_queryable_and_geometry_capable():
    contract = station_source_contract("air_quality")
    assert contract is not None
    assert contract["machine_query"] == "AVAILABLE_AS_FEATURE_QUERY"
    assert contract["geometry"] == "FEATURE_QUERY"
    assert "PM2.5" in contract["reading_fields"]
    assert "air_quality" in live_query_domains()
    assert contract["adapter"].endswith("fetch_myeqms_stations")
