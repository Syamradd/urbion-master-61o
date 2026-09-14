from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def test_release_critical_capabilities_are_present_in_convergence():
    required = (
        "urbion_canonical_evidence.py",
        "urbion_copilot.py",
        "urbion_decision_os.py",
        "urbion_judge_demo.py",
        "urbion_planner_handoff.py",
        "urbion_what_if.py",
        "urbion_error_contract.py",
        "urbion_road_intelligence.py",
        "urbion_mygems_adapter.py",
        "urbion_jps_adapter.py",
        "urbion_myeqms_adapter.py",
        "workspace_v5.html",
        "urbion_workspace_canonical_ui.js",
        "urbion_workspace_road_intelligence_owner.js",
        "urbion_workspace_station_map_owner.js",
        "urbion_championship_visual_overhaul.js",
        "urbion_championship_visual_cleanup.js",
        "urbion_logo_dark.svg",
        "urbion_logo_light.svg",
        "JUDGE_FLOW_CONTRACT.md",
        "P7_JUDGE_GOLDEN_PATH.md",
    )
    missing = [name for name in required if not (ROOT / name).exists()]
    assert not missing, f"release-critical capability files missing: {missing}"


def test_convergence_preserves_statutory_and_authority_boundaries():
    manifest = json.loads((ROOT / "DEPLOYMENT_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["production_entrypoint"] == "landing_server:app"
    assert manifest["statutory_verification"] == "NOT_CLAIMED"
    assert manifest["decision_authority"] == "NONE"
    assert manifest["deployment_ready"] is False


def test_live_adapter_boundaries_are_explicit():
    mygems = (ROOT / "urbion_mygems_adapter.py").read_text(encoding="utf-8")
    jps = (ROOT / "urbion_jps_adapter.py").read_text(encoding="utf-8")
    assert "SOURCE_CONTEXT" in mygems
    assert "NOT_CLAIMED" in mygems
    assert "LIVE_READING_NOT_MACHINE_VERIFIED" in jps
    assert "VERIFIED" in jps
