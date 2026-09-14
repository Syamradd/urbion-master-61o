#!/usr/bin/env python3
"""Run the canonical CI browser smoke launcher directly.

The CI launcher already owns deterministic readiness fixtures and the analysis
wait contract. This wrapper intentionally performs no source rewriting so the
gate cannot fail because a second patcher stops matching the launcher text.
"""
from __future__ import annotations

from pathlib import Path

TARGET = Path(__file__).with_name("workspace_browser_smoke_ci.py")
source = TARGET.read_text(encoding="utf-8")
if 'page.wait_for_function("!!window.URBION_LAST", timeout=60000)' not in source:
    raise SystemExit("CI browser launcher is missing the canonical analysis readiness wait")

code = compile(source, str(TARGET), "exec")
ns = {"__name__": "workspace_browser_smoke_ci", "__file__": str(TARGET)}
exec(code, ns)
