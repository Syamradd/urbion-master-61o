import unittest

from server import AssessmentRequest, assess
from urbion_elysian import compare_official_context


class EvidenceStateAndElysianTests(unittest.TestCase):
    BASE = {
        "site_lat": 2.3,
        "site_lon": 102.2,
        "tod_lat": 2.302,
        "tod_lon": 102.2,
        "plot_ratio": 4.5,
        "precinct": "Terminal Sg. Udang",
        "development_type": "TOD Development / Mixed Use",
        "development_class": "Mixed Use",
        "state": "Melaka",
        "district": "Melaka Tengah",
        "pbt": "Majlis Bandaraya Melaka Bersejarah",
        "lot_no": "TEST-EVIDENCE-01",
    }

    def test_assessment_exposes_explicit_evidence_states(self):
        result = assess(AssessmentRequest(**self.BASE))
        states = result["evidence_state"]
        self.assertEqual(states["site_coordinates"], "USER_PROVIDED")
        self.assertEqual(states["tod_distance"], "CALCULATED")
        self.assertEqual(states["planning_rules"], "SOURCE_CONTEXT")
        self.assertEqual(states["statutory_verification"], "NOT_CLAIMED")

    def test_elysian_flags_land_use_conflict(self):
        result = compare_official_context({"status": "LIVE_ARCGIS_REST", "attributes": {"gunatanah1": "Perumahan"}})
        self.assertTrue(result["conflicts"])
        self.assertEqual(result["conflicts"][0]["official"], "Perumahan")
        self.assertFalse(result["decision_safe"])

    def test_elysian_reconciles_area_lot_district_and_mukim_when_exposed(self):
        result = compare_official_context({
            "status": "LIVE_ARCGIS_REST",
            "attributes": {
                "gunatanah1": "Pertanian",
                "area_ha": 1.200,
                "lot_no": "11213",
                "district": "Melaka Tengah",
                "mukim": "Padang Semabok",
            },
        })
        fields = {item["field"] for item in result["conflicts"]}
        self.assertEqual(fields, {"area_ha"})
        self.assertEqual(result["conflict_count"], 1)
        self.assertEqual(result["official_values"]["lot_no"], "11213")


if __name__ == "__main__":
    unittest.main()
