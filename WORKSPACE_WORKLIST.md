# URBION HORIZON — Current Workspace Worklist

Branch: `feature/canonical-workspace-v2`
Render: **LOCKED until all functional gates are green.**

## A. Functional gate — P0
- [x] Canonical `/workspace` route and isolated V5 presentation path.
- [x] Leaflet map instance + base imagery verified by browser gate.
- [x] GT1 → GT2 → GT3 cascade verified.
- [x] Duplicate legacy workspace bundle is not requested.
- [x] Root cause identified for Layer drawer toggle race: canonical UI and layer runtime were both binding `#layerBtn`.
- [x] Layer drawer ownership repaired so canonical UI is the sole drawer-toggle owner.
- [ ] Browser gate must pass from start to finish after the ownership fix.
- [ ] Every advertised live GIS layer must be checked end-to-end: select → Leaflet layer mounted → map tile/image rendered → no render error → deselect removes layer.
- [ ] Verify layer catalogue has no broken/placeholder visual entries.
- [ ] Verify state change refreshes catalogue and clears previous live layers safely.
- [ ] Verify analysis, What-If, Decision Support, Planner Output, utilities, language and theme after layer testing.
- [ ] Final console/request/legacy-asset audit must be clean.

## B. Planning Case layout — P1 visual polish
- [ ] Remove the large unused vertical whitespace inside Section 01 after the input controls.
- [ ] Audit Sections 02, 03, 04, 05 and subsequent sections for the same post-input empty-space issue.
- [ ] Make each section height/content-driven while preserving scroll, accordion, validation and control hitboxes.
- [ ] Recheck at 1366×768, 1440×900 and 1920×1080 after the spacing repair.
- [ ] Do not let visual tightening break the map viewport or the case-builder workflow.

## C. Layer UX — P1
- [ ] Every layer row remains discoverable by group/source/type.
- [ ] Every layer has a clear OFF / LOADING / ON · RENDERED / ERROR state.
- [ ] Layer group open/close remains independent from the main drawer toggle.
- [ ] Clear Map removes all live overlays without removing the active basemap.
- [ ] Refresh rebuilds the authoritative catalogue without duplicating rows/handlers.

## D. Release gate — P0
- [ ] Source Gate GREEN on the final functional commit.
- [ ] Browser Gate GREEN on the final functional commit.
- [ ] No unresolved P0/P1 functional defects.
- [ ] Only after the above: targeted visual/background polish.
- [ ] Only after all review passes: **explicit Render deployment**.
- [ ] After Render: live route, map, layers, analysis and critical interactions re-audited on the actual Render URL.
