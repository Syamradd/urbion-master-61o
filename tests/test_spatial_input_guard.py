import unittest

from fastapi import HTTPException

from server import AssessmentRequest, assess


class SpatialInputGuardTests(unittest.TestCase):
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
        "lot_no": "TEST-TOD-01",
    }

    def test_placeholder_site_coordinates_are_rejected(self):
        payload = self.BASE | {"site_lat": -90, "site_lon": -180}
        with self.assertRaises(HTTPException) as ctx:
            assess(AssessmentRequest(**payload))
        self.assertEqual(ctx.exception.status_code, 422)
        self.assertEqual(ctx.exception.detail["code"], "INVALID_SPATIAL_INPUT")

    def test_placeholder_tod_coordinates_are_rejected(self):
        payload = self.BASE | {"tod_lat": -90, "tod_lon": -180}
        with self.assertRaises(HTTPException) as ctx:
            assess(AssessmentRequest(**payload))
        self.assertEqual(ctx.exception.status_code, 422)
        self.assertEqual(ctx.exception.detail["code"], "INVALID_SPATIAL_INPUT")

    def test_valid_coordinates_preserve_tod_compliance(self):
        result = assess(AssessmentRequest(**self.BASE))
        self.assertEqual(result["classification"], "TOD 400m")
        self.assertEqual(result["final_status"], "COMPLY")
        self.assertEqual(result["final_rule"], "RT-MBMB-2035-TOD-01")


if __name__ == "__main__":
    unittest.main()
