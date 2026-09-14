"""Release guard: fail if convergence drops a release-critical capability asset."""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = {
    "planning": ["server.py", "urbion_rules.py", "urbion_rule_provenance.py", "urbion_canonical_evidence.py"],
    "evidence": ["urbion_evidence_ledger.py", "urbion_evidence_quality.py", "urbion_error_contract.py"],
    "ai": ["urbion_copilot.py", "urbion_agent_orchestrator.py", "urbion_what_if.py", "urbion_decision_os.py", "urbion_planner_handoff.py", "urbion_judge_demo.py"],
    "gis": ["urbion_iplan.py", "urbion_mygems_adapter.py", "urbion_jps_adapter.py", "urbion_myeqms_adapter.py", "urbion_road_intelligence.py"],
    "workspace": ["workspace_v5.html", "landing_server.py", "urbion_workspace_bridge.js", "urbion_workspace_runtime.js", "urbion_layer_runtime_fix.js", "urbion_workspace_canonical_ui.js", "urbion_workspace_modal_owner.js", "urbion_workspace_review_gaps_owner.js", "urbion_workspace_environment_owner.js", "urbion_workspace_mobility_owner.js", "urbion_workspace_development_impact_owner_v4.js", "urbion_workspace_ratio_owner.js", "urbion_workspace_road_intelligence_owner.js", "urbion_workspace_analysis_summary_owner.js", "urbion_workspace_station_map_owner.js"],
    "contracts": ["BRANCH_CAPABILITY_PRESERVATION_MATRIX.md", "JUDGE_FLOW_CONTRACT.md", "scripts/downstream_canonical_contract_smoke.py"],
}


def main() -> None:
    missing: list[str] = []
    for group, paths in REQUIRED.items():
        for rel in paths:
            if not (ROOT / rel).is_file():
                missing.append(f"{group}:{rel}")
    if missing:
        raise SystemExit("CAPABILITY PRESERVATION FAIL: " + ", ".join(missing))
    print("CAPABILITY PRESERVATION PASS")


if __name__ == "__main__":
    main()
