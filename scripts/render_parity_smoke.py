#!/usr/bin/env python3
"""Smoke the canonical app using the same command shape as Render."""
from __future__ import annotations
import os
import httpx

BASE = os.getenv('URBION_BASE_URL', 'http://127.0.0.1:8000')
ACTIVE_ASSETS = [
    '/urbion_workspace_bridge.js',
    '/urbion_workspace_runtime.js',
    '/urbion_layer_runtime_fix.js',
    '/urbion_workspace_canonical_ui.js',
    '/urbion_workspace_modal_owner.js',
    '/urbion_workspace_pbt_catalog.js',
    '/urbion_workspace_utility_owner.js',
    '/urbion_workspace_review_gaps_owner.js',
    '/urbion_workspace_environment_owner.js',
    '/urbion_workspace_mobility_owner.js',
    '/urbion_workspace_development_impact_owner_v4.js',
    '/urbion_workspace_ratio_owner.js',
    '/urbion_workspace_road_intelligence_owner.js',
    '/urbion_workspace_analysis_summary_owner.js',
    '/urbion_workspace_station_map_owner.js',
]

def assert_ok(client: httpx.Client, path: str) -> None:
    r = client.get(BASE + path)
    assert r.status_code == 200, f'{path} -> {r.status_code}: {r.text[:300]}'

def main() -> None:
    with httpx.Client(timeout=20, follow_redirects=True) as client:
        assert_ok(client, '/health')
        assert_ok(client, '/workstation/metadata')
        workspace = client.get(BASE + '/workspace')
        assert workspace.status_code == 200
        assert workspace.headers.get('x-urbion-ui') == 'CANONICAL-V5-ISOLATED'
        for path in ACTIVE_ASSETS:
            assert_ok(client, path)
        layers = client.get(BASE + '/map/layers?state=Melaka')
        assert layers.status_code == 200, f'/map/layers -> {layers.status_code}: {layers.text[:300]}'
        assert 'workspace_v2.html' not in workspace.text
        assert 'workspace_v3.html' not in workspace.text
        assert 'workspace_v4.html' not in workspace.text
        assert 'function loadOwners()' not in client.get(BASE + '/urbion_workspace_station_map_owner.js').text
    print('RENDER PARITY SMOKE PASS')

if __name__ == '__main__':
    main()
