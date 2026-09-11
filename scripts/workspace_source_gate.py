#!/usr/bin/env python3
"""Static source gate for the canonical URBION HORIZON workspace."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = ["landing_server.py", "workspace_v5.html", "urbion_workspace_final.js", "urbion_workspace_bridge.js", "urbion_workspace_runtime.js"]
IDS = ["run", "layerBtn", "landuse1", "landuse2", "landuse3", "map", "evidenceBtn", "whatifBtn", "decisionBtn", "outputBtn", "themeBtn", "langBtn"]
ENDPOINTS = ["/workstation/analysis", "/what-if", "/decision-center", "/metadata", "/map/layers"]


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

    # Reject only actual legacy taxonomy entries/options, not explanatory copy.
    for pattern in (r"['\"]Perdagangan['\"]\s*:", r"value=['\"]Perdagangan['\"]", r"<option[^>]*>\s*Perdagangan\s*</option>"):
        if re.search(pattern, all_source, flags=re.I):
            fail(f"legacy Guna Tanah entry detected: {pattern}")
    ok("current Komersial taxonomy gate passed")

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

    bridge_runtime = texts["urbion_workspace_bridge.js"] + texts["urbion_workspace_runtime.js"]
    for token in ("window.URBION_FINAL", "GT", "analyse", "whatif", "decision", "output"):
        if token not in bridge_runtime:
            fail(f"runtime contract token missing: {token}")
    ok("bridge/runtime contract verified")

    # Basic source integrity without depending on a runner-specific Node install.
    for name in ("urbion_workspace_final.js", "urbion_workspace_bridge.js", "urbion_workspace_runtime.js"):
        text = texts[name]
        if text.count("{") != text.count("}") or text.count("(") != text.count(")"):
            fail(f"unbalanced JavaScript delimiters in {name}")
    ok("JavaScript source delimiter integrity passed")

    print("WORKSPACE SOURCE GATE: PASS")
    print("Browser interaction, visual QA and Render remain separate release gates.")


if __name__ == "__main__":
    main()
