#!/usr/bin/env python3
"""Verify the canonical V5 runtime topology as served by the production entrypoint."""
from __future__ import annotations
import os
import httpx

BASE = os.getenv("URBION_BASE_URL", "http://127.0.0.1:8000")
EXPECTED = [
    "/urbion_workspace_bridge.js",
    "/urbion_workspace_runtime.js",
    "/urbion_layer_runtime_fix.js",
    "/urbion_workspace_canonical_ui.js",
    "/urbion_workspace_modal_owner.js",
    "/urbion_workspace_pbt_catalog.js",
    "/urbion_workspace_utility_owner.js",
    "/urbion_workspace_review_gaps_owner.js",
    "/urbion_workspace_environment_owner.js",
    "/urbion_workspace_mobility_owner.js",
    "/urbion_workspace_development_impact_owner_v4.js",
    "/urbion_workspace_ratio_owner.js",
    "/urbion_workspace_road_intelligence_owner.js",
    "/urbion_workspace_analysis_summary_owner.js",
    "/urbion_workspace_station_map_owner.js",
]
FORBIDDEN_MARKERS = (
    "workspace_v2.html",
    "workspace_v3.html",
    "workspace_v4.html",
    "workspace_v4_server.py",
    "urbion_workspace_v2.py",
    "function loadOwners()",
    "urbion_workspace_decision_story_owner_v1.js",
    "urbion_workspace_decision_story_owner_v2.js",
    "urbion_workspace_live_evidence_owner_v1.js",
    "urbion_workspace_judge_owner_v1.js",
)

def main() -> None:
    with httpx.Client(timeout=15, follow_redirects=True) as client:
        r = client.get(BASE + "/workspace")
        r.raise_for_status()
        html = r.text
        assert 'X-URBION-UI' not in html  # header is out-of-band; content must stay canonical HTML
        positions = []
        for path in EXPECTED:
            marker = f'<script src="{path}"></script>'
            assert marker in html, f"missing canonical script: {path}"
            positions.append(html.index(marker))
            asset = client.get(BASE + path)
            assert asset.status_code == 200, f"active asset not served: {path} -> {asset.status_code}"
            assert "application/javascript" in asset.headers.get("content-type", ""), path
        assert positions == sorted(positions), "canonical script order drifted"
        for marker in FORBIDDEN_MARKERS:
            assert marker not in html, f"forbidden legacy/dynamic marker reached served workspace: {marker}"
        station = client.get(BASE + "/urbion_workspace_station_map_owner.js").text
        assert "function loadOwners()" not in station
        summary = client.get(BASE + "/urbion_workspace_analysis_summary_owner.js").text
        assert "__URBION_ANALYSIS_SUMMARY_OWNER_V5__" in summary
        assert "__URBION_DECISION_STORY_OWNER_V1__" in summary
        assert "__URBION_LIVE_EVIDENCE_OWNER_V1__" in summary
    print("CANONICAL RUNTIME TOPOLOGY PASS")

if __name__ == "__main__":
    main()
