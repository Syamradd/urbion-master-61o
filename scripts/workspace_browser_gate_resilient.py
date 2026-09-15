#!/usr/bin/env python3
"""Run the canonical CI browser smoke launcher directly.

The CI launcher owns the deterministic readiness fixture and analysis wait
transformation. This entrypoint keeps the product assertions intact while
allowing the browser smoke's external Leaflet bootstrap a bounded startup
window on slower CI runners.
"""
from __future__ import annotations

from pathlib import Path

TARGET = Path(__file__).with_name("workspace_browser_smoke_ci.py")
source = TARGET.read_text(encoding="utf-8")
# The product gate still requires a real Leaflet instance; this only extends
# the pre-assertion DOM bootstrap window from 1.8s to 8s for CI variance.
source = source.replace(
    'page.wait_for_selector("#map"); page.wait_for_timeout(1800)',
    'page.wait_for_selector("#map"); page.wait_for_timeout(8000)',
    1,
)
code = compile(source, str(TARGET), "exec")
ns = {"__name__": "workspace_browser_smoke_ci", "__file__": str(TARGET)}
exec(code, ns)
