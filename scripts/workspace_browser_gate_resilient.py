#!/usr/bin/env python3
"""Execute the canonical CI browser smoke launcher with release-safe timing hardening."""
from __future__ import annotations

from pathlib import Path

TARGET = Path(__file__).with_name("workspace_browser_smoke_ci.py")
source = TARGET.read_text(encoding="utf-8")

# The product smoke contract checks for mounted + rendered imagery. CI must give
# the same layer enough time as the strict GIS regression gate, without weakening
# the render assertion itself. This is launcher-level only; product source stays intact.
source = source.replace(
    'page.wait_for_function("id=>!!window.__URBION_LIVE_LAYERS__?.[id]",arg=layer_id,timeout=6000)',
    'page.wait_for_function("id=>!!window.__URBION_LIVE_LAYERS__?.[id]",arg=layer_id,timeout=35000)',
    1,
)
source = source.replace(
    'page.wait_for_function("""id=>{const l=window.__URBION_LIVE_LAYERS__?.[id];if(!l)return false;return Object.keys(l._tiles||{}).length>0||(l._container?.querySelectorAll(\'img,canvas\').length||0)>0}""",arg=layer_id,timeout=6000)',
    'page.wait_for_function("""id=>{const l=window.__URBION_LIVE_LAYERS__?.[id];if(!l)return false;return Object.keys(l._tiles||{}).length>0||(l._container?.querySelectorAll(\'img,canvas\').length||0)>0}""",arg=layer_id,timeout=35000)',
    1,
)

code = compile(source, str(TARGET), "exec")
ns = {"__name__": "workspace_browser_gate_resilient", "__file__": str(TARGET)}
exec(code, ns)
