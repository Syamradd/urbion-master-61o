import asyncio

import httpx

import urbion_wms_proxy


class _FakeResponse:
    def __init__(self):
        self.status_code = 200
        self.headers = {"content-type": "application/json"}

    def json(self):
        return {"features": []}


async def _fake_client_get(url, params):
    assert url == "https://mygems.jmg.gov.my/server/rest/services/GeologiAsas/Major_Fault/FeatureServer/5/query"
    assert params["returnGeometry"] == "true"
    assert params["outSR"] == "3857"
    return _FakeResponse()


def test_empty_jmg_major_fault_tile_is_a_valid_authoritative_render(monkeypatch):
    monkeypatch.setattr(urbion_wms_proxy, "_client_get", _fake_client_get)
    params = {
        "bbox": "11349369.95978297,273950.30937407166,11388505.718264982,313086.06785608083",
        "width": "256",
        "height": "256",
        "bboxSR": "3857",
    }

    response = asyncio.run(
        urbion_wms_proxy._jmg_feature_image_fallback(
            "/server/rest/services/GeologiAsas/Major_Fault/MapServer", params
        )
    )

    assert response is not None
    assert response.status_code == 200
    assert response.media_type == "image/svg+xml"
    assert response.headers["X-URBION-GIS-Fallback"] == "JMG-FeatureServer-EmptyTile"
    assert response.body.startswith(b"<svg")
