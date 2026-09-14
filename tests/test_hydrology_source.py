from urbion_data_sources import source_catalog


def test_public_infobanjir_is_registered_as_live_portal_context():
    sources = {item["id"]: item for item in source_catalog()}
    source = sources["jps-public-infobanjir"]
    assert source["status"] == "PUBLIC_REAL_TIME_PORTAL"
    assert source["category"] == "HYDROLOGY"
    assert source["url"] == "https://publicinfobanjir.water.gov.my/"
