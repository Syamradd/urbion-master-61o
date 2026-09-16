#!/usr/bin/env python3
"""Execute the canonical CI browser smoke launcher without source rewriting."""
from __future__ import annotations

from pathlib import Path

TARGET = Path(__file__).with_name("workspace_browser_smoke_ci.py")
source = TARGET.read_text(encoding="utf-8")
code = compile(source, str(TARGET), "exec")
ns = {"__name__": "workspace_browser_gate_resilient", "__file__": str(TARGET)}
exec(code, ns)
