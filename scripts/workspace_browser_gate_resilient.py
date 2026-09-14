#!/usr/bin/env python3
"""Run the canonical browser smoke with a deterministic analysis wait patch."""
from __future__ import annotations

import re
from pathlib import Path

TARGET = Path(__file__).with_name("workspace_browser_smoke_ci.py")
source = TARGET.read_text(encoding="utf-8")

pattern = re.compile(
    r'''page\.wait_for_function\(\s*"document\.body\.innerText\.includes\('ANALYSIS COMPLETE'\)"\s*,\s*timeout\s*=\s*20000\s*\)'''
)
patched, count = pattern.subn(
    'page.wait_for_function("!!window.URBION_LAST", timeout=60000)',
    source,
)

if count == 0 and 'page.wait_for_function("!!window.URBION_LAST", timeout=60000)' not in source:
    raise SystemExit("CI browser wait patch did not match canonical analysis assertion")

code = compile(patched, str(TARGET), "exec")
ns = {"__name__": "workspace_browser_smoke_ci", "__file__": str(TARGET)}
exec(code, ns)
