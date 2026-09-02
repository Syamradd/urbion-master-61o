import unittest

from server import AssessmentRequest, assess


class AssessmentRuleMappingTests(unittest.TestCase):
    BASE = {
        "site_lat": 2.302,
        "site_lon": 102.2,
        "tod_lat": 2.302,
        "tod_lon": 102.2,
        "plot_ratio": 4.5,
    }

    def assessment(self, **overrides):
        return assess(AssessmentRequest(**(self.BASE | overrides)))

    def assert_rule(self, development_type, rule_id, **overrides):
        result = self.assessment(development_type=development_type, **overrides)
        self.assertEqual(result["final_rule"], rule_id)
        self.assertEqual([rule["rule_id"] for rule in result["retrieved_rules"]], [rule_id])
        return result

    def test_free_standing_commercial_retrieves_com_01(self):
        result = self.assessment(development_type="Free-Standing Commercial")
        self.assertEqual([rule["rule_id"] for rule in result["retrieved_rules"]], ["RT-MBMB-2035-COM-01"])
        self.assertIsNone(result["final_rule"])
        self.assertEqual(result["final_status"], "REQUIRES REVIEW")
        self.assertEqual(result["evidence_state"]["final_decision"], "CALCULATED")

    def test_free_standing_building_retrieves_com_02(self):
        self.assert_rule("Free-Standing Building", "RT-MBMB-2035-COM-02", perimeter_planting=3)

    def test_shop_frontage_retrieves_com_03(self):
        self.assert_rule(
            "Commercial Shop Frontage", "RT-MBMB-2035-COM-03",
            landscaped_pedestrian_walkway=1.5, shop_frontage_verified=True,
        )

    def test_shop_office_retrieves_com_04(self):
        self.assert_rule(
            "Commercial Shop-Office", "RT-MBMB-2035-COM-04",
            building_height=4, shop_office_verified=True,
        )

    def test_shop_office_valid_height_and_verification_complies(self):
        result = self.assert_rule(
            "Commercial Shop-Office", "RT-MBMB-2035-COM-04",
            building_height=4, shop_office_verified=True,
        )
        self.assertEqual(result["final_status"], "COMPLY")

    def test_shop_office_missing_height_requires_review(self):
        result = self.assert_rule(
            "Commercial Shop-Office", "RT-MBMB-2035-COM-04",
            shop_office_verified=True,
        )
        self.assertEqual(result["final_status"], "REQUIRES REVIEW")

    def test_shop_office_excessive_height_is_non_compliant(self):
        result = self.assert_rule(
            "Commercial Shop-Office", "RT-MBMB-2035-COM-04",
            building_height=5, shop_office_verified=True,
        )
        self.assertEqual(result["final_status"], "NON-COMPLIANCE")

    def test_tod_400m_complies(self):
        result = self.assessment(development_type="TOD Development / Mixed Use")
        self.assertEqual(result["final_rule"], "RT-MBMB-2035-TOD-01")
        self.assertEqual(
            [rule["rule_id"] for rule in result["retrieved_rules"]],
            ["RT-MBMB-2035-TOD-01", "RT-MBMB-2035-TOD-02"],
        )
        self.assertEqual(result["classification"], "TOD 400m")
        self.assertEqual(result["final_status"], "COMPLY")


if __name__ == "__main__":
    unittest.main()
