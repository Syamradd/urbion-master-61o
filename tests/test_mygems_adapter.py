from urbion_mygems_adapter import layer_id_for_state, query_mygems_lithology


class _Response:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


def test_mygems_state_layer_contract():
    assert layer_id_for_state("Melaka") == 22
    assert layer_id_for_state("Johor") == 24
    assert layer_id_for_state("Unknown") is None


def test_mygems_adapter_normalises_live_geojson():
    calls = {}

    def fake_get(url, params):
        calls["url"] = url
        calls["params"] = params
        return _Response(
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "properties": {"FNM": "Alluvium", "NAM": "Melaka"},
                        "geometry": {"type": "Polygon", "coordinates": []},
                    }
                ],
            }
        )

    result = query_mygems_lithology(2.2, 102.25, state="Melaka", http_get=fake_get)
    assert result["status"] == "LIVE_QUERY"
    assert result["evidence_state"] == "SOURCE_CONTEXT"
    assert result["feature_count"] == 1
    assert calls["url"].endswith("/FeatureServer/22/query")
    assert calls["params"]["outSR"] == "4326"
    assert calls["params"]["f"] == "geojson"


def test_mygems_adapter_explicit_no_feature():
    result = query_mygems_lithology(
        2.2,
        102.25,
        state="Melaka",
        http_get=lambda url, params: _Response({"type": "FeatureCollection", "features": []}),
    )
    assert result["status"] == "NO_FEATURE"
    assert result["feature_count"] == 0


def test_mygems_adapter_rejects_invalid_coordinates():
    try:
        query_mygems_lithology(91, 102.25, state="Melaka")
    except ValueError as exc:
        assert str(exc) == "INVALID_SPATIAL_INPUT"
    else:
        raise AssertionError("invalid coordinates must be rejected")
