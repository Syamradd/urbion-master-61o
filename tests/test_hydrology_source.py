from urbion_data_sources import map_layer_catalog, source_catalog


def test_public_infobanjir_is_registered_as_live_portal_context():
    sources = {item["id"]: item for item in source_catalog()}
    assert sources["jps-public-infobanjir"]["status"] == "PUBLIC_REAL_TIME_PORTAL"
    layers = {item["id"]: item for item in map_layer_catalog("Melaka")}
    assert layers["jps-infobanjir"]["group"] == "HYDROLOGY"
    assert layers["jps-infobanjir"]["evidence"] == "SOURCE_CONTEXT"
