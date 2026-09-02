from urbion_gis_lot import lot_area_summary, lot_feature


def test_lot_area_summary_converts_to_hectares():
    result = lot_area_summary(12500)
    assert result["area_m2"] == 12500.0
    assert result["area_ha"] == 1.25
    assert result["area_status"] == "AVAILABLE"


def test_missing_area_never_invents_value():
    result = lot_area_summary(None)
    assert result["area_m2"] is None
    assert result["area_status"] == "EVIDENCE REQUIRED"


def test_lot_polygon_uses_geojson_coordinate_order():
    feature = lot_feature(lot_no="11213", coordinates=[[101.9, 2.2], [101.91, 2.2], [101.91, 2.21], [101.9, 2.2]], area_m2=5000)
    assert feature["geometry"]["type"] == "Polygon"
    assert feature["geometry"]["coordinates"][0][0] == [101.9, 2.2]
    assert feature["properties"]["area_ha"] == 0.5
