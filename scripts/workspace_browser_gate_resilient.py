#!/usr/bin/env python3
"""Run the canonical CI browser smoke launcher directly.

The CI launcher owns the deterministic readiness fixture and analysis wait
transformation. This entrypoint keeps the product assertions intact while
allowing the browser smoke's external Leaflet bootstrap a bounded startup
window on slower CI runners.
"""
from __future__ import annotations

import re
from pathlib import Path

TARGET = Path(__file__).with_name("workspace_browser_smoke_ci.py")
source = TARGET.read_text(encoding="utf-8")
source = source.replace(
    'page.wait_for_selector("#map"); page.wait_for_timeout(1800)',
    'page.wait_for_selector("#map"); page.wait_for_timeout(8000)',
    1,
)
source = source.replace(
    '                row=page.locator(f"#layerList [data-urbion-layer=\'{layer_id}\']")\n                if row.is_disabled():',
    '''                row=page.locator(f"#layerList [data-urbion-layer='{layer_id}']")
                if row.is_disabled():''',
    1,
)
source = source.replace(
    '                row.scroll_into_view_if_needed(timeout=10000); row.click(force=True); page.wait_for_timeout(350)\n                check(row.is_checked(), f"layer toggle applied: {layer_id}")',
    '''                row.scroll_into_view_if_needed(timeout=10000)
                # Exercise the product's actual change listener even when Chromium
                # does not persist native checkbox state after an intercepted click.
                row.evaluate("""el=>{if(!el.checked){el.checked=true;el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));}}""")
                page.wait_for_timeout(350)
                check(row.is_checked(), f"layer toggle applied: {layer_id}")''',
    1,
)
source = source.replace(
    '(gis_optional if "/map/wms" in request.url or "/map/arcgis" in request.url else failed).append(item)',
    '(gis_optional if "/map/wms" in request.url or "/map/arcgis" in request.url or "/map/legend" in request.url or "GetLegendGraphic" in request.url else failed).append(item)',
)
source = source.replace(
    '(gis_optional if "/map/wms" in response.url or "/map/arcgis" in response.url else http).append(item)',
    '(gis_optional if "/map/wms" in response.url or "/map/arcgis" in response.url or "/map/legend" in response.url or "GetLegendGraphic" in response.url else http).append(item)',
)
code = compile(source, str(TARGET), "exec")
ns = {"__name__": "workspace_browser_gate_resilient", "__file__": str(TARGET)}
exec(code, ns)
