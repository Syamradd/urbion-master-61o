from urbion_elysian import ELYSIAN_LOT_11213, compare_official_context


def test_elysian_reference_is_explicitly_non_authoritative():
    assert ELYSIAN_LOT_11213["lot_no"] == "11213"
    assert ELYSIAN_LOT_11213["area_ha"] == 1.145
    assert ELYSIAN_LOT_11213["evidence_status"] == "PROJECT_REFERENCE"


def test_official_land_use_conflict_is_flagged():
    result = compare_official_context({"status":"LIVE_QUERY", "attributes":{"gunatanah1":"Perumahan"}})
    assert result["decision_safe"] is False
    assert result["conflicts"]
    assert result["conflicts"][0]["field"] == "current_land_use"
