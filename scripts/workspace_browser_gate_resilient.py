#!/usr/bin/env python3
"""Run the canonical CI browser smoke launcher directly.

The CI launcher owns the deterministic readiness fixture and analysis wait
transformation. This entrypoint must not inspect its source text or perform a
second layer of rewriting; doing so can falsely fail before Playwright starts.
"""
from __future__ import annotations

from pathlib import Path

TARGET = Path(__file__).with_name("workspace_browser_smoke_ci.py")
source = TARGET.read_text(encoding="utf-8")
code = compile(source, str(TARGET), "exec")
ns = {"__name__": "workspace_browser_smoke_ci", "__file__": str(TARGET)}
exec(code, ns)
