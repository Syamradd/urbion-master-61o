#!/usr/bin/env python3
"""Stable CI launcher for the canonical URBION browser smoke gate.

The product smoke source remains unchanged. CI loads its definitions without
executing main(), installs a deterministic readiness fixture, then runs the
original gate. This avoids brittle source-injection order and keeps fixture
hardening out of the product implementation.
"""
from __future__ import annotations
import re
from pathlib import Path

TARGET = Path(__file__).with_name("workspace_browser_smoke.py")
source = TARGET.read_text(encoding="utf-8")

# The original readiness helper contains a native querySelector selector that
# is not valid DOM CSS. The CI override does not depend on it, but remove the
# invalid form everywhere so no stale helper can trip parsing/runtime probes.
source = source.replace(
    "querySelector('input:visible,select:visible,textarea:visible')",
    "querySelector('input,select,textarea')",
)

# Strip the source's __main__ execution block. We will call main() only after
# installing the CI fixture override below.
source = re.sub(
    r"\nif __name__ == [\"']__main__[\"']:\n\s*main\(\)\s*\Z",
    "\n",
    source,
)

code = compile(source, str(TARGET), "exec")
globals_dict = {"__name__": "workspace_browser_smoke_ci", "__file__": str(TARGET)}
exec(code, globals_dict)

check = globals_dict["check"]
row_control = globals_dict["row_control"]
usable_options = globals_dict["usable_options"]
page_main = globals_dict["main"]


def prepare_ready_case(page):
    """Build a valid case through the same visible controls used by judges.

    The key reliability rule is to derive a GT2/GT3 path from the live
    taxonomy, rather than assuming the first GT2 item has a GT3 descendant.
    """
    def expand_owner(ident):
        page.locator(f"#{ident}").evaluate(
            """el=>{let p=el;while(p&&!(p.classList&&p.classList.contains('sec')))p=p.parentElement;if(p?.classList.contains('collapsed'))p.querySelector('.sechead button')?.click();}"""
        )
        page.wait_for_timeout(80)

    def choose(control, value=None, timeout_ms=8000):
        if value is None:
            deadline = timeout_ms
            while deadline > 0:
                options = usable_options(control)
                if options:
                    value = options[0]
                    break
                page.wait_for_timeout(250)
                deadline -= 250
            if value is None:
                raise AssertionError(f"no usable options for control {control}")
        control.select_option(label=value, force=True)
        control.dispatch_event("input")
        control.dispatch_event("change")
        return value

    row_control(page, "PROJECT / SITE NAME").fill("Browser Gate Planning Case")

    state = row_control(page, "STATE")
    if state.evaluate("el=>el.tagName") == "SELECT":
        choose(state, "Melaka")
    else:
        state.fill("Melaka")
        state.dispatch_event("change")
    page.wait_for_timeout(350)

    district = row_control(page, "DISTRICT")
    if district.evaluate("el=>el.tagName") == "SELECT":
        opts = usable_options(district)
        choose(district, "Alor Gajah" if "Alor Gajah" in opts else (opts[0] if opts else None))
    else:
        district.fill("Alor Gajah")
        district.dispatch_event("change")
    page.wait_for_timeout(350)

    pbt = row_control(page, "LOCAL AUTHORITY")
    if pbt.evaluate("el=>el.tagName") == "SELECT":
        choose(pbt, "Majlis Bandaraya Melaka Bersejarah")
    else:
        pbt.fill("Majlis Bandaraya Melaka Bersejarah")
        pbt.dispatch_event("change")

    page.locator("#site_lat").fill("2.285000")
    page.locator("#site_lon").fill("102.196000")

    for label in ["DEVELOPMENT TYPE", "DEVELOPMENT CLASS"]:
        control = row_control(page, label)
        if control.evaluate("el=>el.tagName") == "SELECT":
            choose(control)
        else:
            control.fill("General")
            control.dispatch_event("input")
            control.dispatch_event("change")
        page.wait_for_timeout(250)

    for ident in ["landuse1", "landuse2", "landuse3"]:
        expand_owner(ident)

    gt1 = page.locator("#landuse1")
    gt2 = page.locator("#landuse2")
    gt3 = page.locator("#landuse3")

    # Ask the running canonical taxonomy for a valid full cascade path.
    path = page.evaluate(
        """()=>{
          const gt=window.URBION_FINAL?.GT||{};
          const preferred='Komersial';
          const a=Object.prototype.hasOwnProperty.call(gt,preferred)?preferred:Object.keys(gt).find(k=>String(k).toLowerCase()!=='perdagangan');
          if(!a)return null;
          const l2=gt[a]||{};
          const b=Object.keys(l2).find(k=>Array.isArray(l2[k])&&l2[k].length>0);
          const c=b?(l2[b]||[])[0]:null;
          return {a,b,c};
        }"""
    )
    check(path and path.get("a"), "canonical taxonomy exposes a valid GT1 path")
    check(path.get("b") and path.get("c"), "canonical taxonomy exposes a valid GT2 → GT3 path")

    choose(gt1, path["a"])
    page.wait_for_timeout(300)

    # The canonical handler owns the cascade. Wait on actual option state,
    # replay GT1 only if asynchronous population has not settled yet.
    for _ in range(8):
        if len(usable_options(gt2)) >= 1:
            break
        choose(gt1, path["a"])
        page.wait_for_timeout(250)
    check(len(usable_options(gt2)) >= 1, "GT2 populated after canonical GT1 cascade")

    choose(gt2, path["b"])
    page.wait_for_timeout(300)
    for _ in range(8):
        if len(usable_options(gt3)) >= 1:
            break
        choose(gt2, path["b"])
        page.wait_for_timeout(250)
    check(len(usable_options(gt3)) >= 1, "GT3 populated after canonical GT2 cascade")
    choose(gt3, path["c"])
    page.wait_for_timeout(250)

    # Final value verification through Playwright locators, not stale DOM
    # handles or page.evaluate() CSS pseudo-classes.
    labels = [
        "PROJECT / SITE NAME", "STATE", "DISTRICT", "LOCAL AUTHORITY",
        "LATITUDE", "LONGITUDE", "DEVELOPMENT TYPE", "DEVELOPMENT CLASS",
        "GT1", "GT2", "GT3",
    ]
    controls = [
        row_control(page, "PROJECT / SITE NAME"), row_control(page, "STATE"),
        row_control(page, "DISTRICT"), row_control(page, "LOCAL AUTHORITY"),
        page.locator("#site_lat"), page.locator("#site_lon"),
        row_control(page, "DEVELOPMENT TYPE"), row_control(page, "DEVELOPMENT CLASS"),
        gt1, gt2, gt3,
    ]
    values = [str(c.input_value()).strip() for c in controls]
    missing = [label for label, value in zip(labels, values) if not value]
    if missing:
        print(f"[TRACE-CI-V3] readiness missing={missing}; values={values}; gt2={usable_options(gt2)}; gt3={usable_options(gt3)}")
    check(len(values) == 11 and all(values), f"planning case fixture is complete ({sum(bool(v) for v in values)}/{len(values)})")
    page.wait_for_function("document.querySelector('#run') && !document.querySelector('#run').disabled", timeout=10000)
    check(not page.locator("#run").is_disabled(), "Run Site Analysis unlocked by canonical readiness")


globals_dict["prepare_ready_case"] = prepare_ready_case
print("[CI-FIXTURE-V3] deterministic canonical readiness fixture installed")
page_main()
