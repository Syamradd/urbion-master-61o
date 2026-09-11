#!/usr/bin/env python3
"""Static release gate for the canonical URBION HORIZON workspace.

This gate deliberately checks source wiring only. It does not claim browser or
Render proof; those remain explicit runtime/release gates.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    "landing_server.py",
    "workspace_v5.html",
    "urbion_workspace_final.js",
    "urbion_workspace_bridge.js",
    "urbion_workspace_runtime.js",
)
REQUIRED_IDS = (
    "run",
    "layerBtn",
    "landuse1",
    "landuse2",
    "landuse3",
    "map",
    "evidenceBtn",
    "whatifBtn",
    "decisionBtn",
    "outputBtn",
    "themeBtn",
    "langBtn",
)
REQUIRED_ENDPOINTS = (
    "/workstation/analysis",
    "/what-if",
    "/decision-center",
    "/metadata",
    "/map/layers",
)
FORBIDDEN_LEGACY_TERMS = ("Perdagangan",)


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"[ OK ] {message}")


def node_check(path: Path) -> None:
    proc = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True)
    if proc.returncode:
        fail(f"node --check failed for {path.name}: {proc.stderr.strip()}")
    ok(f"JavaScript syntax: {path.name}")


def main() -> None:
    for name in REQUIRED_FILES:
        path = ROOT / name
        if not path.is_file():
            fail(f"missing required file: {name}")
    ok("canonical workspace files present")

    landing = (ROOT / "landing_server.py").read_text(encoding="utf-8")
    workspace = (ROOT / "workspace_v5.html").read_text(encoding="utf-8")
    final_js = (ROOT / "urbion_workspace_final.js").read_text(encoding="utf-8")
    bridge = (ROOT / "urbion_workspace_bridge.js").read_text(encoding="utf-8")
    runtime = (ROOT / "urbion_workspace_runtime.js").read_text(encoding="utf-8")

    for path_name, text in (("landing_server.py", landing), ("workspace_v5.html", workspace),
                            ("urbion_workspace_final.js", final_js), ("urbion_workspace_bridge.js", bridge),
                            ("urbion_workspace_runtime.js", runtime)):
        for term in FORBIDDEN_LEGACY_TERMS:
            if term in text:
                fail(f"legacy land-use term {term!r} found in {path_name}")
    ok("legacy Guna Tanah term absent")

    for element_id in REQUIRED_IDS:
        if not re.search(rf"(?:id|data-testid)=[\"']{re.escape(element_id)}[\"']", workspace):
            fail(f"required workspace control/id missing: {element_id}")
    ok("required workspace controls present")

    for endpoint in REQUIRED_ENDPOINTS:
        if endpoint not in workspace and endpoint not in runtime:
            fail(f"required endpoint wiring missing: {endpoint}")
    ok("core endpoint wiring present")

    expected_scripts = (
        '/urbion_workspace_final.js',
        '/urbion_workspace_bridge.js',
        '/urbion_workspace_runtime.js',
    )
    positions = [landing.find(x) for x in expected_scripts]
    if any(p < 0 for p in positions) or positions != sorted(positions):
        fail("canonical script injection order is not final -> bridge -> runtime")
    ok("canonical script injection order verified")

    if "window.URBION_FINAL" not in bridge or "window.URBION_FINAL" not in runtime:
        fail("stable URBION_FINAL bridge/runtime contract missing")
    ok("stable runtime contract verified")

    if not all(token in final_js for token in ("Komersial", "Perumahan", "Pengangkutan")):
        fail("latest source-aligned taxonomy markers missing from function layer")
    ok("current Guna Tanah taxonomy markers present")

    node_check(ROOT / "urbion_workspace_final.js")
    node_check(ROOT / "urbion_workspace_bridge.js")
    node_check(ROOT / "urbion_workspace_runtime.js")

    print("\nWORKSPACE SOURCE GATE: PASS")
    print("Browser interaction, visual QA and Render remain explicit release gates.")


if __name__ == "__main__":
    main()
