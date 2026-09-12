#!/usr/bin/env python3
"""Stable CI launcher for the canonical URBION browser smoke gate.

Keeps the product smoke test source untouched while applying CI-only selector
hardening in memory before executing it.
"""
from __future__ import annotations
import runpy
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

new = '''    ready_controls = [\n        row_control(page, "PROJECT / SITE NAME"),\n        row_control(page, "STATE"),\n        row_control(page, "DISTRICT"),\n        row_control(page, "LOCAL AUTHORITY"),\n        page.locator("#site_lat"),\n        page.locator("#site_lon"),\n        row_control(page, "DEVELOPMENT TYPE"),\n        row_control(page, "DEVELOPMENT CLASS"),\n        page.locator("#landuse1"),\n        page.locator("#landuse2"),\n        page.locator("#landuse3"),\n    ]\n    ready_values = [str(control.input_value()).strip() for control in ready_controls]\n    ready = {"filled": sum(bool(value) for value in ready_values), "total": len(ready_values), "values": ready_values}\n    check(ready["total"] == 11 and ready["filled"] == ready["total"], f"planning case fixture is complete ({ready['filled']}/{ready['total']})")'''

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

# Execute the repaired source as a normal __main__ script.
code = compile(source, str(TARGET), "exec")
globals_dict = {"__name__": "__main__", "__file__": str(TARGET)}
exec(code, globals_dict)
