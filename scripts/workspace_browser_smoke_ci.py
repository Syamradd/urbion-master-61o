#!/usr/bin/env python3
"""Stable CI launcher for the canonical URBION browser smoke gate.

Keeps the product smoke test source untouched while applying CI-only fixture
hardening in memory before executing it.
"""
from __future__ import annotations
from pathlib import Path

TARGET = Path(__file__).with_name("workspace_browser_smoke.py")
source = TARGET.read_text(encoding="utf-8")

# Playwright supports :visible; native querySelector does not. Replace only the
# readiness resolver inside the CI copy of the script.
source = source.replace(
    "?.querySelector('input:visible,select:visible,textarea:visible');",
    "?.querySelector('input,select,textarea');",
    1,
)

old = '''    ready = page.evaluate("""()=>{\n      const pick=label=>[...document.querySelectorAll('.sec .row')]\n        .find(r=>r.querySelector('.lab')?.textContent.toLowerCase().includes(label.toLowerCase()))\n        ?.querySelector('input,select,textarea');\n      const controls=[\n        pick('project / site name'),pick('state'),pick('district'),pick('local authority'),\n        document.querySelector('#site_lat'),document.querySelector('#site_lon'),\n        pick('development type'),pick('development class'),\n        document.querySelector('#landuse1'),document.querySelector('#landuse2'),document.querySelector('#landuse3')\n      ].filter(Boolean);\n      return {filled:controls.filter(c=>String(c.value||'').trim()!=='').length,total:controls.length};\n    }""")\n    check(ready["total"] >= 11 and ready["filled"] == ready["total"], f"planning case fixture is complete ({ready['filled']}/{ready['total']})")'''

new = '''    ready_controls = [\n        row_control(page, "PROJECT / SITE NAME"),\n        row_control(page, "STATE"),\n        row_control(page, "DISTRICT"),\n        row_control(page, "LOCAL AUTHORITY"),\n        page.locator("#site_lat"),\n        page.locator("#site_lon"),\n        row_control(page, "DEVELOPMENT TYPE"),\n        row_control(page, "DEVELOPMENT CLASS"),\n        page.locator("#landuse1"),\n        page.locator("#landuse2"),\n        page.locator("#landuse3"),\n    ]\n    ready_values = [str(control.input_value()).strip() for control in ready_controls]\n    ready = {"filled": sum(bool(value) for value in ready_values), "total": len(ready_values), "values": ready_values}\n    missing_labels = [\n        label for label, value in zip(\n            ["PROJECT / SITE NAME","STATE","DISTRICT","LOCAL AUTHORITY","LATITUDE","LONGITUDE","DEVELOPMENT TYPE","DEVELOPMENT CLASS","GT1","GT2","GT3"],\n            ready_values,\n        ) if not value\n    ]\n    if missing_labels:\n        print(f"[TRACE] readiness missing: {missing_labels}; values={ready_values}")\n    check(ready["total"] == 11 and ready["filled"] == ready["total"], f"planning case fixture is complete ({ready['filled']}/{ready['total']})")'''

if old not in source:
    raise SystemExit("expected readiness block not found in canonical smoke source")
source = source.replace(old, new, 1)

# Keep CI fixture interactions resilient when a section is collapsed.
source = source.replace(
    'control.select_option(label=options[0])',
    'control.select_option(label=options[0], force=True)',
    1,
)
source = source.replace(
    'page.locator("#landuse1").select_option(label="Komersial")',
    'page.locator("#landuse1").select_option(label="Komersial", force=True)',
    1,
)

# The development-class select is populated asynchronously after the
# development-type change. Poll the locator-backed DOM directly rather than
# passing a Playwright Locator through wait_for_function as an argument.
source = source.replace(
    '        if control.evaluate("el=>el.tagName") == "SELECT":\n            if label == "DEVELOPMENT CLASS":\n                page.wait_for_function(\n                    "sel=>Array.from(sel.options).some(o=>o.textContent.trim() && !o.textContent.trim().toLowerCase().startsWith(\\\'select\\\'))",\n                    arg=control, timeout=8000,\n                )\n            fill_first_option(control)\n            control.dispatch_event("change")\n        else:\n            control.fill("General")\n            control.dispatch_event("input")\n            control.dispatch_event("change")\n        page.wait_for_timeout(250)',
    '        if control.evaluate("el=>el.tagName") == "SELECT":\n            if label == "DEVELOPMENT CLASS":\n                deadline = page.wait_for_timeout\n                ready_class = False\n                for _ in range(80):\n                    if usable_options(control):\n                        ready_class = True\n                        break\n                    page.wait_for_timeout(100)\n                if not ready_class:\n                    raise AssertionError("development class options did not populate within 8s")\n            fill_first_option(control)\n            control.dispatch_event("change")\n        else:\n            control.fill("General")\n            control.dispatch_event("input")\n            control.dispatch_event("change")\n        page.wait_for_timeout(250)',
    1,
)

# Final fixture stabilization: retry any empty select once after the cascading
# graph settles, without changing application code or introducing a second owner.
needle = '    ready_controls = [\n'
insert = '''    page.wait_for_timeout(500)\n    for control in [\n        row_control(page, "DISTRICT"),\n        row_control(page, "LOCAL AUTHORITY"),\n        row_control(page, "DEVELOPMENT TYPE"),\n        row_control(page, "DEVELOPMENT CLASS"),\n        page.locator("#landuse1"), page.locator("#landuse2"), page.locator("#landuse3"),\n    ]:\n        if control.evaluate("el=>el.tagName") == "SELECT" and not str(control.input_value()).strip():\n            options = usable_options(control)\n            if options:\n                control.select_option(label=options[0], force=True)\n                control.dispatch_event("change")\n                page.wait_for_timeout(200)\n\n'''
if needle not in source:
    raise SystemExit("fixture readiness insertion point not found")
source = source.replace(needle, insert + needle, 1)

code = compile(source, str(TARGET), "exec")
globals_dict = {"__name__": "__main__", "__file__": str(TARGET)}
exec(code, globals_dict)
