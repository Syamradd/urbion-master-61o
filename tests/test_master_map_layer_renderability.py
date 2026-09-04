import unittest

from urbion_data_sources import map_layer_catalog


class MasterMapLayerRenderabilityTests(unittest.TestCase):
    def test_melaka_core_iplan_layers_are_browser_renderable(self):
        layers = {item["id"]: item for item in map_layer_catalog("Melaka")}
        for layer_id, expected_name in (
            ("iplan-current", "gunatanah_semasa_04"),
            ("iplan-zoning", "gunatanah_zoning_04"),
            ("iplan-committed", "gunatanah_komited_04"),
        ):
            item = layers[layer_id]
            self.assertEqual(item["type"], "GEOSERVER_WMS")
            self.assertEqual(item["url"], "https://iplan.planmalaysia.gov.my/geoserver/iplan/wms")
            self.assertEqual(item["layers"], f"iplan:{expected_name}")

    def test_query_only_layers_are_not_advertised_as_visual_layers(self):
        layers = map_layer_catalog("Melaka")
        self.assertFalse(any(item.get("type") == "ARCGIS_QUERY" for item in layers))

    def test_unknown_state_does_not_fabricate_state_specific_iplan_layer_names(self):
        layers = {item["id"]: item for item in map_layer_catalog("Unknown State")}
        self.assertIsNone(layers["iplan-current"]["layers"])
        self.assertIsNone(layers["iplan-zoning"]["layers"])


if __name__ == "__main__":
    unittest.main()
