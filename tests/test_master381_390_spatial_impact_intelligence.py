from urbion_spatial_intelligence import build_spatial_intelligence
from urbion_impact_intelligence import build_impact_intelligence
from urbion_copilot import build_copilot_packet


def _inputs():
    return {
        "site_lat": 2.285,
        "site_lon": 102.196,
        "tod_lat": 2.286,
        "tod_lon": 102.197,
        "plot_ratio": 4.5,
        "development_type": "TOD Development / Mixed Use",
        "development_class": "Mixed Use",
        "state": "Melaka",
        "district": "Melaka Tengah",
        "pbt": "Majlis Bandaraya Melaka Bersejarah",
    }


def test_spatial_signals_are_deterministic_and_evidence_bounded():
    result = build_spatial_intelligence(2.285, 102.196, 2.286, 102.197, (400, 800), {"flood": True})
    ids = {item["id"] for item in result["planning_signals"]}
    assert {"tod_access", "catchment_coverage", "constraint_flags"} <= ids
    assert result["constraints"]["flagged_count"] == 1
    assert result["planning_signals"][0]["evidence"] == "CALCULATED"
    assert result["evidence_model"]["authoritative_overlay"] == "SOURCE_CONTEXT ONLY"
    assert result["review_gaps"]


def test_impact_links_spatial_signals_without_fabricating_environment():
    spatial = build_spatial_intelligence(2.285, 102.196, 2.286, 102.197, (400, 800), {"flood": True})
    impact = build_impact_intelligence(spatial=spatial, assessment={})
    signals = {(s["domain"], s["signal"]): s for s in impact["signals"]}
    assert ("mobility", "tod_access_screening") in signals
    assert signals[("environment", "user_constraint_flag")]["evidence_state"] == "USER_PROVIDED"
    assert impact["status"] == "REVIEW_REQUIRED"
    assert "unverified" in " ".join(impact["review_gaps"]).lower()
    assert impact["statutory_verification"] == "NOT_CLAIMED"


def test_environment_source_context_propagates_but_never_becomes_verified():
    env = {"layers": {
        "flood": {"status": "LIVE_QUERY", "feature_count": 2},
        "slope": {"status": "NO_FEATURE", "feature_count": 0},
    }}
    impact = build_impact_intelligence(spatial={}, assessment={}, environmental_context=env)
    states = {s["signal"]: s["evidence_state"] for s in impact["signals"]}
    assert states["flood_source_context"] == "SOURCE_CONTEXT"
    assert states["slope_screened_no_feature"] == "SOURCE_CONTEXT"
    assert "VERIFIED" not in states.values()
    assert impact["impact_readiness"]["environment"] == "SOURCE_CONTEXT"


def test_copilot_exposes_spatial_impact_handoff():
    packet = build_copilot_packet(_inputs(), constraints={"flood": True})
    assert packet["spatial"]["planning_signals"]
    assert packet["impact"]["signal_count"] >= 4
    assert packet["impact"]["status"] == "REVIEW_REQUIRED"
    assert packet["decision_authority"] == "NONE"
    assert packet["statutory_verification"] == "NOT_CLAIMED"
