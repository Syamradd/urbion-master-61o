from urbion_gis_decision import decision_feature, decision_map_payload


def test_feature_uses_geojson_coordinate_order():
    feature = decision_feature(latitude=2.3, longitude=102.2, status="COMPLY", lot_no="11213")
    assert feature["geometry"]["coordinates"] == [102.2, 2.3]
    assert feature["properties"]["lot_no"] == "11213"


def test_map_payload_derives_center_and_keeps_legend():
    features = [
        decision_feature(latitude=2.0, longitude=102.0, status="COMPLY"),
        decision_feature(latitude=4.0, longitude=104.0, status="REQUIRES REVIEW"),
    ]
    payload = decision_map_payload(features)
    assert payload["center"] == {"latitude": 3.0, "longitude": 103.0}
    assert "NON-COMPLIANCE" in payload["legend"]
