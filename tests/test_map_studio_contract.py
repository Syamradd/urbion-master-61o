import unittest
from pathlib import Path


class MapStudioContractTests(unittest.TestCase):
    def test_map_studio_uses_live_same_origin_and_dynamic_layer_contract(self):
        html = (Path(__file__).resolve().parents[1] / "map-studio.html").read_text(encoding="utf-8")
        required = [
            "const API=location.origin",
            "L.tileLayer.wms",
            "GEOSERVER_WMS",
            "item.layers",
            "/map/layers?state=Melaka",
            "/iplan/context?site_lat=",
        ]
        for token in required:
            self.assertIn(token, html)

    def test_map_studio_renders_hydrology_group(self):
        html = (Path(__file__).resolve().parents[1] / "map-studio.html").read_text(encoding="utf-8")
        self.assertIn("'HYDROLOGY'", html)

    def test_map_studio_exposes_judge_controls(self):
        html = (Path(__file__).resolve().parents[1] / "map-studio.html").read_text(encoding="utf-8")
        for token in ["legendBtn", "share", "navigator.clipboard", "URLSearchParams", "?lat="]:
            self.assertIn(token, html)

    def test_map_studio_rejects_invalid_focus_coordinates(self):
        html = (Path(__file__).resolve().parents[1] / "map-studio.html").read_text(encoding="utf-8")
        self.assertIn("!Number.isFinite(a)||!Number.isFinite(b)", html)
        self.assertIn("a<-90||a>90||b<-180||b>180", html)

    def test_map_studio_does_not_hardcode_urbion_render_api(self):
        html = (Path(__file__).resolve().parents[1] / "map-studio.html").read_text(encoding="utf-8")
        self.assertNotIn("urbion-master-61o.onrender.com", html)
        self.assertNotIn("urbion-master-61o-1.onrender.com", html)


if __name__ == "__main__":
    unittest.main()
