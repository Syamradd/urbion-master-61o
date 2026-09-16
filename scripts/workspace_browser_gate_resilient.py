#!/usr/bin/env python3
"""Execute the canonical URBION workspace browser smoke directly."""
from __future__ import annotations

from pathlib import Path

TARGET = Path(__file__).with_name("workspace_browser_smoke.py")
source = TARGET.read_text(encoding="utf-8")
code = compile(source, str(TARGET), "exec")
ns = {"__name__": "__main__", "__file__": str(TARGET)}
exec(code, ns)
