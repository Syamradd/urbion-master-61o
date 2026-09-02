import unittest
from pathlib import Path


class MapStudioContractTests(unittest.TestCase):
    def test_map_studio_uses_live_same_origin_and_verified_layer_contract(self):
        html = (Path(__file__).resolve().parents[1] / "map-studio.html").read_text(encoding="utf-8")
        required = [
            "const API=location.origin",
            "L.tileLayer.wms",
            "GEOSERVER_WMS",
            "gunatanah_komited_",
            "/map/layers?state=Melaka",
            "/iplan/context?site_lat=",
        ]
        for token in required:
            self.assertIn(token, html)

    def test_map_studio_does_not_hardcode_urbion_render_api(self):
        html = (Path(__file__).resolve().parents[1] / "map-studio.html").read_text(encoding="utf-8")
        self.assertNotIn("urbion-master-61o.onrender.com", html)
        self.assertNotIn("urbion-master-61o-1.onrender.com", html)


if __name__ == "__main__":
    unittest.main()
