#!/usr/bin/env python3
"""Static source gate for the canonical URBION HORIZON workspace."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = ["landing_server.py", "workspace_v5.html", "urbion_workspace_final.js", "urbion_workspace_bridge.js", "urbion_workspace_runtime.js"]
IDS = [
    "run", "layerBtn", "landuse1", "landuse2", "landuse3", "map",
    "evidenceBtn", "whatifBtn", "decisionBtn", "outputBtn", "generateOutput",
    "printBtn", "closeModal", "useMap", "locate", "context400", "context800",
    "context1000", "ring400", "ring800", "ring1000", "roadCtx", "roadCtxMap",
    "themeBtn", "langBtn", "search",
]
RUNTIME_IDS = ["runtimeAbout", "runtimeHelp", "runtimeSources", "runtimeStatus", "runtimeFullscreen", "runtimeReset"]
ENDPOINTS = ["/workstation/analysis", "/what-if", "/decision-center", "/map/layers", "/copilot/explain", "/knowledge/retrieve"]


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

    runtime = texts["urbion_workspace_runtime.js"]
    if "document.querySelectorAll('button').forEach(replaceNode)" in runtime:
        fail("runtime takeover must not clone every button")
    if "const owned=[" not in runtime or "#run" not in runtime or "#langBtn" not in runtime:
        fail("runtime owned-control takeover contract missing")
    ok("runtime takeover scope protected")

    for control_id in RUNTIME_IDS:
        if control_id not in runtime:
            fail(f"runtime utility control missing: {control_id}")
    for token in ("help.onclick", "sources.onclick", "status.onclick", "fs.onclick", "reset.onclick"):
        if token not in runtime:
            fail(f"runtime utility handler missing: {token}")
    ok("runtime utility controls wired")

    for token in ("grid-template-columns:330px minmax(0,1fr) 380px", ".layout", ".left", ".center", ".right", "#map"):
        if token not in workspace:
            fail(f"presentation layout contract missing: {token}")
    ok("three-column presentation contract present")

    for name in ("urbion_workspace_final.js", "urbion_workspace_bridge.js", "urbion_workspace_runtime.js"):
        text = texts[name]
        if text.count("{") != text.count("}") or text.count("(") != text.count(")"):
            fail(f"unbalanced JavaScript delimiters in {name}")
    ok("JavaScript source delimiter integrity passed")

    print("WORKSPACE SOURCE GATE: PASS")
    print("Browser interaction, visual QA and Render remain separate release gates.")


if __name__ == "__main__":
    main()
