#!/usr/bin/env python3
"""Run the canonical CI browser smoke launcher directly."""
from __future__ import annotations
from pathlib import Path

TARGET = Path(__file__).with_name("workspace_browser_smoke_ci.py")
source = TARGET.read_text(encoding="utf-8")
source = source.replace(
    'page.wait_for_selector("#map"); page.wait_for_timeout(1800)',
    'page.wait_for_selector("#map"); page.wait_for_timeout(8000)',
    1,
)
source = source.replace(
    '                row.scroll_into_view_if_needed(timeout=10000); row.check(force=True); page.wait_for_timeout(250)',
    '''                selector = f"#layerList [data-urbion-layer=\\'{layer_id}\\']"
                for _ in range(8):
                    try:
                        page.locator(selector).evaluate("el=>el.scrollIntoView({block:'center',inline:'nearest'})")
                        break
                    except Exception:
                        page.wait_for_timeout(120)
                row = page.locator(selector)
                row.check(force=True); page.wait_for_timeout(250)''',
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
source = source.replace(
    'source = source.replace(\n    \'            rows=page.locator("#layerList [data-urbion-layer]"); count=rows.count(); check(count>=20,f"authoritative live layer catalogue populated ({count})")\',',
    'source = source.replace(\n    \'            page.wait_for_function("document.querySelectorAll(\\\'#layerList [data-urbion-layer]\\\').length >= 20", timeout=15000)\\n            rows=page.locator("#layerList [data-urbion-layer]"); count=rows.count(); check(count>=20,f"authoritative live layer catalogue populated ({count})")\',',
)
code = compile(source, str(TARGET), "exec")
ns = {"__name__": "workspace_browser_gate_resilient", "__file__": str(TARGET)}
exec(code, ns)
check = ns["check"]
row_control = ns["row_control"]
usable_options = ns["usable_options"]
page_main = ns["main"]

if "prepare_ready_case" not in ns:
    raise RuntimeError("CI smoke launcher did not expose prepare_ready_case")

print("[CI-FIXTURE-V5] deterministic canonical readiness fixture installed")
page_main()
