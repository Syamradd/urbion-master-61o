import unittest

from server import km_readiness


class KMEndpointContractTests(unittest.TestCase):
    def test_km_readiness_exposes_transparent_workflow_boundary(self):
        result = km_readiness(
            pbt="Majlis Bandaraya Melaka Bersejarah",
            development_type="TOD Development / Mixed Use",
            documents=["Location Plan", "Site Plan", "Development Proposal Report"],
            km_category="SEDERHANA",
            technical_reviews={"JPS": "CLEAR"},
        )
        self.assertEqual(result["readiness"], "READY_FOR_WORKFLOW_REVIEW")
        self.assertIn("decision_boundary", result)
        self.assertIn("statutory approval", result["decision_boundary"])


if __name__ == "__main__":
    unittest.main()
