from urbion_iplan import query_iplan_context


def test_iplan_unknown_state_is_explicit():
    result = query_iplan_context(2.3, 102.2, "Atlantis")
    assert result["status"] == "UNSUPPORTED_STATE"


def test_iplan_melaka_contract(monkeypatch):
    calls = []

    def fake(service, lat, lon, timeout=8.0):
        calls.append(service)
        return {
            "status": "LIVE_QUERY",
            "attributes": {"gunatanah1": "Komersial", "tahun_data": 2025},
            "geometry": {"rings": []},
        }

    monkeypatch.setattr("urbion_iplan._query_layer", fake)
    result = query_iplan_context(2.3, 102.2, "Melaka")
    assert result["provider"] == "PLANMalaysia i-Plan"
    assert result["current_land_use"]["attributes"]["gunatanah1"] == "Komersial"
    assert result["zoning"]["attributes"]["tahun_data"] == 2025
    assert result["committed_land_use"]["status"] == "LIVE_WMS"
    assert result["committed_land_use"]["url"].endswith("/geoserver/iplan/wms")
    assert result["committed_land_use"]["layers"] == "iplan:gunatanah_komited_04"
    assert result["cadastral_lot"]["status"] == "LIVE_QUERY"
    assert result["terrain_contour_5m"]["status"] == "LIVE_QUERY"
    assert calls == ["GTsemasa_04", "GTzoning_04", "LOT_04", "KONTUR5M_04"]
