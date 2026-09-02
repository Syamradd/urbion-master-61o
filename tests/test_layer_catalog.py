from urbion_data_sources import map_layer_catalog, source_catalog


def test_melaka_catalog_contains_official_iplan_wms_context_layers():
    layers = {item["id"]: item for item in map_layer_catalog("Melaka")}
    assert layers["iplan-committed"]["layers"] == "iplan:gunatanah_komited_04"
    assert layers["iplan-flood"]["layers"] == "iplan:banjir"
    assert layers["iplan-disaster-risk"]["layers"] == "iplan:risiko_bencana"
    assert layers["iplan-ksas"]["layers"] == "iplan:ksas"
    assert layers["iplan-ecology"]["layers"] == "iplan:rangkaian_ekologi"
    assert layers["iplan-heritage"]["layers"] == "iplan:warisan"
    assert layers["iplan-affordable-housing"]["layers"] == "iplan:rumah_mampu_milik"


def test_project_reference_is_separate_from_authoritative_sources():
    sources = {item["id"]: item for item in source_catalog()}
    assert sources["elysian-legacy-gis"]["status"] == "REFERENCE_REGISTERED"
    assert sources["elysian-legacy-gis"]["category"] == "PROJECT_REFERENCE"
