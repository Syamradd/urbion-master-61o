#!/usr/bin/env python3
"""Static source gate for the canonical URBION HORIZON workspace."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    "landing_server.py",
    "workspace_v5.html",
    "urbion_workspace_final.js",
    "urbion_workspace_bridge.js",
    "urbion_workspace_runtime.js",
]
IDS = [
    "run", "layerBtn", "landuse1", "landuse2", "landuse3", "map",
    "evidenceBtn", "whatifBtn", "decisionBtn", "outputBtn", "themeBtn", "langBtn",
]
ENDPOINTS = ["/workstation/analysis", "/what-if", "/decision-center", "/metadata", "/map/layers"]
JS_FILES = ["urbion_workspace_final.js", "urbion_workspace_bridge.js", "urbion_workspace_runtime.js"]


def fail(message: str) -> None:
    raise SystemExit(f"[FAIL] {message}")


def ok(message: str) -> None:
    print(f"[ OK ] {message}")


def main() -> None:
    for name in FILES:
        if not (ROOT / name).is_file():
            fail(f"missing canonical file: {name}")
    ok("canonical workspace files present")

    texts = {name: (ROOT / name).read_text(encoding="utf-8") for name in FILES}
    all_source = "\n".join(texts.values())

    for pattern in (r"['\"]Perdagangan['\"]\s*:", r"value=['\"]Perdagangan['\"]"):
        if re.search(pattern, all_source, flags=re.I):
            fail(f"legacy Guna Tanah entry detected: {pattern}")
    ok("Guna Tanah uses current Komersial taxonomy, with no legacy Perdagangan entry")

    workspace = texts["workspace_v5.html"]
    missing_ids = [x for x in IDS if f'id="{x}"' not in workspace and f"id='{x}'" not in workspace]
    if missing_ids:
        fail("missing workspace controls: " + ", ".join(missing_ids))
    ok("required workspace controls present")

    missing_endpoints = [x for x in ENDPOINTS if x not in all_source]
    if missing_endpoints:
        fail("missing endpoint wiring: " + ", ".join(missing_endpoints))
    ok("core endpoint wiring present")

    landing = texts["landing_server.py"]
    scripts = ["/urbion_workspace_final.js", "/urbion_workspace_bridge.js", "/urbion_workspace_runtime.js"]
    positions = [landing.find(x) for x in scripts]
    if any(p < 0 for p in positions) or positions != sorted(positions):
        fail("canonical script order must be final -> bridge -> runtime")
    ok("canonical script injection order verified")

    for token in ("window.URBION_FINAL", "GT", "analyse", "whatif", "decision", "output"):
        if token not in texts["urbion_workspace_bridge.js"] + texts["urbion_workspace_runtime.js"]:
            fail(f"runtime contract token missing: {token}")
    ok("bridge/runtime contract verified")

    for name in JS_FILES:
        proc = subprocess.run(["node", "--check", str(ROOT / name)], capture_output=True, text=True)
        if proc.returncode:
            fail(f"JavaScript syntax error in {name}: {proc.stderr.strip()}")
    ok("JavaScript syntax checks passed")

    print("WORKSPACE SOURCE GATE: PASS")
    print("Browser interaction, visual QA and Render remain separate release gates.")


if __name__ == "__main__":
    main()
