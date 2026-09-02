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


if __name__ == "__main__":
    unittest.main()
