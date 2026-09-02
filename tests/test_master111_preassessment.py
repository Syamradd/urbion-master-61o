from urbion_preassessment import build_preassessment

def test_preassessment_schema():
    out = build_preassessment(assessment={"final_status":"COMPLY","site":{"lot_no":"11213"},"tod_distance_m":220,"retrieved_rules":[{"rule_id":"R1"}],"site_analysis":{},"planning_value":{"evidence_gaps":[],"next_actions":["Review"]},"decision_trace":[]})
    assert out["version"] == "MASTER-111"
    assert out["planning_decision"] == "COMPLY"
    assert [x["stage"] for x in out["workflow"]] == ["SITE","SPATIAL","POLICY","COMPLIANCE","SUITABILITY","EVIDENCE","DECISION"]
