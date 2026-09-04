import unittest
from pathlib import Path


class MasterDecisionRenderingTests(unittest.TestCase):
    def setUp(self):
        self.js = (Path(__file__).resolve().parents[1] / "urbion_championship_decision_layer.js").read_text(encoding="utf-8")

    def test_decision_layer_reads_site_score_and_indicator_arrays(self):
        self.assertIn("s?.indicators??s?.dimensions??s?.dimension_scores", self.js)
        self.assertIn("candidates=[s.score,s.overall_score,s.suitability_score", self.js)

    def test_decision_layer_does_not_render_array_indexes_as_dimension_names(self):
        self.assertIn("name:v?.name||`Dimension ${i+1}`", self.js)
        self.assertNotIn("Object.entries(x.dimensions||{})", self.js)

    def test_decision_layer_exposes_confidence_and_evidence_status(self):
        self.assertIn("confidence?.score", self.js)
        self.assertIn("v.status||v.method", self.js)
        self.assertIn("Source context is not the same as verified evidence.", self.js)


if __name__ == "__main__":
    unittest.main()
