from urbion_cadastral_context import cadastral_service_url, query_cadastral


def test_cadastral_service_uses_official_iplan_lot_service_by_state():
    assert cadastral_service_url("Melaka").endswith("/iPLAN/LOT_04/MapServer/0")
    assert cadastral_service_url("Negeri Sembilan").endswith("/iPLAN/LOT_05/MapServer/0")


def test_cadastral_query_contract_is_conservative(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "type": "FeatureCollection",
                "features": [{
                    "type": "Feature",
                    "properties": {"LOT": "123", "UPI": "0401010000123", "KELUASAN": 1.25},
                    "geometry": {"type": "Polygon", "coordinates": [[[102.2, 2.2], [102.21, 2.2], [102.21, 2.21], [102.2, 2.2]]]}
                }]
            }

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
        def get(self, *args, **kwargs):
            return FakeResponse()

    monkeypatch.setattr("urbion_cadastral_context.httpx.Client", FakeClient)
    result = query_cadastral(2.2, 102.2, 120, "Melaka")
    assert result["status"] == "LIVE_QUERY"
    assert result["id"] == "iplan-cadastral"
    assert result["features"][0]["properties"]["LOT"] == "123"
    assert result["source"].endswith("/LOT_04/MapServer/0")
    assert result["decision_safe"] is False
