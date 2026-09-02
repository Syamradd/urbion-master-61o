from urbion_what_if import execute_what_if


def fake_assess(inputs):
    walkway = inputs.get("landscaped_pedestrian_walkway", 0)
    verified = inputs.get("shop_office_verified", False)
    if inputs.get("development_type") == "Commercial Shop-Office" and not verified:
        status = "REQUIRES REVIEW"
    elif inputs.get("development_type") == "Commercial Shop Frontage" and walkway < 1:
        status = "NON-COMPLIANCE"
    else:
        status = "COMPLY"
    return {"final_status": status, "site_analysis": {"score": 82 if status == "COMPLY" else 40}, "planning_value": {"band": "READY FOR FURTHER REVIEW" if status == "COMPLY" else "BLOCKED", "blockers": [] if status == "COMPLY" else ["control"], "evidence_gaps": []}}


def test_execute_what_if_finds_walkway_fix():
    base = {"development_type": "Commercial Shop Frontage", "landscaped_pedestrian_walkway": 0.5}
    result = execute_what_if(base, [{"id": "WALKWAY-FIX", "overrides": {"landscaped_pedestrian_walkway": 1.5}}], fake_assess)
    assert result["baseline"]["final_status"] == "NON-COMPLIANCE"
    assert result["scenarios"][0]["status"] == "COMPLY"
    assert result["best_candidate"] == "WALKWAY-FIX"


def test_execute_what_if_finds_shop_office_verification_path():
    base = {"development_type": "Commercial Shop-Office", "shop_office_verified": False}
    result = execute_what_if(base, [{"id": "VERIFY-OFFICE", "overrides": {"shop_office_verified": True}}], fake_assess)
    assert result["baseline"]["final_status"] == "REQUIRES REVIEW"
    assert result["scenarios"][0]["status"] == "COMPLY"
    assert result["scenarios"][0]["status_changed"] is True
