from urbion_myeqms_adapter import fetch_myeqms_stations, normalize_feature


def test_normalize_feature_preserves_authoritative_geometry_and_timestamp():
    feature = {
        "attributes": {
            "STATION_ID": "CA01R",
            "DATETIME": 1778270400000,
            "API": 37,
            "CLASS": "Good",
            "STATE_NAME": "Perlis",
            "STATION_LOCATION": "Kangar, PERLIS",
            "LONGITUDE": 100.210937,
            "LATITUDE": 6.429928,
            "PLACE": "Institut Latihan Perindustrian (Kangar)",
            "PM10": 12.0,
        }
    }
    record = normalize_feature(feature)
    assert record is not None
    assert record["station_id"] == "CA01R"
    assert record["lat"] == 6.429928
    assert record["lon"] == 100.210937
    assert record["reading"] == 37
    assert record["pm10"] == 12.0
    assert record["evidence_state"] == "VERIFIED"


def test_missing_geometry_is_excluded_without_invention():
    feature = {"attributes": {"STATION_ID": "CA01R", "API": 37}}
    assert normalize_feature(feature) is None


def test_fetcher_filters_state_and_uses_injected_transport():
    payload = {
        "features": [
            {"attributes": {"STATION_ID": "A", "DATETIME": 1778270400000, "STATE_NAME": "Melaka", "LATITUDE": 2.2, "LONGITUDE": 102.2, "API": 20}},
            {"attributes": {"STATION_ID": "B", "DATETIME": 1778270400000, "STATE_NAME": "Johor", "LATITUDE": 1.5, "LONGITUDE": 103.7, "API": 30}},
        ]
    }
    seen = {}

    def fake_get(url, params):
        seen["url"] = url
        seen["params"] = params
        return payload

    records = fetch_myeqms_stations(state="Melaka", http_get=fake_get)
    assert [r["station_id"] for r in records] == ["A"]
    assert seen["params"]["returnGeometry"] == "true"
    assert seen["params"]["outSR"] == "4326"
