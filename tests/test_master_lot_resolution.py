import urbion_lot_resolver as resolver


def _feature(lot="11213", upi="040101010112213"):
    return {
        "type":"Feature",
        "properties":{"LOT":lot,"UPI":upi,"NEGERI":"04","DAERAH":"01","MUKIM":"01","SEKSYEN":"01","KELUASAN":1.145},
        "geometry":{"type":"Polygon","coordinates":[[[102.2,2.3],[102.201,2.3],[102.201,2.301],[102.2,2.301],[102.2,2.3]]]},
    }


def test_lot_resolver_returns_live_polygon_and_identity(monkeypatch):
    monkeypatch.setattr(resolver, "_query_layer", lambda *args, **kwargs: {"status":"LIVE_QUERY","url":"test","feature_count":1,"features":[_feature()]})
    result = resolver.resolve_lot(2.3,102.2,"Melaka")
    assert result["status"] == "SOURCE_CONTEXT"
    assert result["selected"]["identity"]["lot_no"] == "11213"
    assert result["selected"]["geometry"]["type"] == "Polygon"
    assert result["decision_safe"] is False


def test_lot_resolver_exact_lot_becomes_verified_candidate_not_statutory_authority(monkeypatch):
    monkeypatch.setattr(resolver, "_query_layer", lambda *args, **kwargs: {"status":"LIVE_QUERY","url":"test","feature_count":1,"features":[_feature()]})
    result = resolver.resolve_lot(2.3,102.2,"Melaka",lot_no="11213")
    assert result["status"] == "VERIFIED_CANDIDATE"
    assert "LOT" in result["corroboration"]
    assert result["authority_model"].startswith("OFFICIAL_SOURCE_CANDIDATE")
    assert any(source["id"] == "jupem-mylot" and source["evidence"] == "MANUAL_VERIFICATION" for source in result["sources"])
    assert result["decision_safe"] is False


def test_lot_resolver_discloses_source_gap(monkeypatch):
    monkeypatch.setattr(resolver, "_query_layer", lambda *args, **kwargs: {"status":"QUERY_UNAVAILABLE","url":"test","features":[]})
    result = resolver.resolve_lot(2.3,102.2,"Melaka")
    assert result["status"] == "EVIDENCE_GAP"
    assert result["decision_safe"] is False
