# URBION HORIZON — Final Functional Audit / Pre-Render Gate

## Status key
✅ source implementation complete
🟡 browser/runtime proof required
❌ confirmed defect

## Current checkpoint
Branch: `feature/canonical-workspace-v2`.
Latest source hardening: `2b98dc1441c7cd4d044a5295d610b5e0a5d9dfe1`.
Latest browser-gate tooling: `cb9ecfd0a686f7cb82b2805bb20fa42dbcdcc339`.
Render: **LOCKED — no deployment / no iteration**.

## Current source trace
The canonical judge path is explicitly chained as:

`workspace_v5.html` → `urbion_workspace_final.js` → `urbion_workspace_bridge.js` → `urbion_workspace_runtime.js`

The presentation adapter injects the bridge between the planning function layer and the final visible-control runtime. The bridge is timing-safe and exposes the existing core functions without cloning the planning engines.

PLANMalaysia source basis remains **Manual Sistem Maklumat Geografi (GIS) Rancangan Pemajuan Versi 3.0 / Versi 3 (2025)** for the Guna Tanah 1 / 2 / 3 hierarchy. Legacy `Perdagangan` is not used as the commercial GT1 label; runtime uses `Komersial`.

## 1. Canonical runtime
- [x] `/` → `welcome.html`
- [x] `/about` → `urbion_horizon_about.html`
- [x] `/workspace` → `workspace_v5.html`
- [x] Legacy championship frontend injection removed from canonical routes
- [x] Existing FastAPI planning engines preserved
- [x] `urbion_workspace_final.js` remains the canonical planning function layer
- [x] `urbion_workspace_bridge.js` exposes the existing core functions through `window.URBION_FINAL`
- [x] Bridge waits for the actual function definitions before publishing the API
- [x] `urbion_workspace_runtime.js` remains the final visible-control runtime layer
- [x] Duplicate runtime boot is guarded
- [x] Runtime map/global access is defensive
- [x] Runtime takeover is scoped only to runtime-owned controls; canonical case-builder handlers are preserved

## 2. Guna Tanah 1 / 2 / 3 — latest classification
- [x] Canonical GT hierarchy is Version 3-aligned
- [x] GT1 → GT2 → GT3 is cascading
- [x] `Komersial` is the commercial GT1 term
- [x] Legacy `Perdagangan` is excluded from visible runtime selectors
- [x] Selected GT1/GT2/GT3 values are included in the assessment payload
- [x] Runtime selector setup remains authoritative without cloning unrelated case controls

## 3. Map / GIS controls
- [x] Leaflet map
- [x] MAP / OSM
- [x] SATELLITE / Esri World Imagery
- [x] HYBRID / imagery + reference labels
- [x] Site marker + map click
- [x] Locate / recenter
- [x] 400 m / 800 m / 1 km rings
- [x] Ring visibility toggles
- [x] Search → coordinates → map update
- [x] Road / transit context toggle
- [x] Basemap switching removes the previous workspace basemap first

## 4. i-Plan layer drawer
- [x] `/map/layers?state=...`
- [x] Dynamic groups / source / type
- [x] GeoServer WMS renderer
- [x] TILE renderer
- [x] ArcGIS MapServer renderer
- [x] ON = real Leaflet layer added
- [x] OFF = real Leaflet layer removed
- [x] Error state / portal-only handling
- [x] Current land use / zoning / committed land use pathways
- [x] Topography / heritage / CFS / ecology / KSAS / disaster-risk pathways through live catalogue

## 5. Planning analysis
- [x] `/workstation/analysis`
- [x] Case payload includes GT1 / GT2 / GT3
- [x] Readiness derived from returned state
- [x] Spatial findings
- [x] Planning implications
- [x] Review gaps
- [x] RT rule cards with proposed / requirement / status / reason / source
- [x] GP/GPP candidates
- [x] Evidence health / register hooks

## 6. What-If / Decision / Output
- [x] `/what-if` baseline + scenario
- [x] `/decision-center` status + rationale + planner action
- [x] Planner-ready Output with land-use hierarchy / RT / GP / gaps / authority boundary
- [x] Print / PDF
- [x] No APPROVED / REJECTED statutory claim

## 7. Utilities
- [x] About
- [x] Help
- [x] Sources
- [x] Status
- [x] Fullscreen
- [x] Reset
- [x] BM/EN visible toggle
- [x] Dark/light toggle

## 8. Source-side hardening completed
### Defect A — canonical runtime bridge missing
**Status: REPAIRED ✅**

The visible-control runtime waited for `window.URBION_FINAL`, while the original planning function layer defined the required functions without publishing that object. A canonical bridge was added without rewriting the planning engines.

### Defect B — bridge timing could race the core
**Status: REPAIRED ✅**

The bridge now waits for the actual function definitions and publishes the stable API only when those functions exist. It also has its own boot guard.

### Defect C — runtime duplicate boot / undefined map globals
**Status: REPAIRED ✅**

The runtime now self-guards and checks map/base/ring globals before using them.

### Defect D — runtime takeover could destroy unrelated case-builder handlers
**Status: REPAIRED ✅**

The runtime previously cloned every button on the page before rebinding its own controls. The takeover is now scoped to runtime-owned controls only, preserving native case-builder interactions and preventing silent handler loss.

### Defect E — release gate did not fully protect the repaired control contract
**Status: REPAIRED ✅**

The source gate now checks the runtime takeover scope, critical workspace controls, endpoint wiring, canonical script order and JavaScript source integrity.

### Defect F — browser gate was only documented, not executable
**Status: REPAIRED AS TEST INFRASTRUCTURE ✅**

A Playwright browser smoke test and GitHub Actions browser-gate workflow were added. The test starts the canonical `landing_server.py`, exercises routing, GT cascade, basemap switching, rings, layers drawer, Evidence/What-If/Decision/Output modals, utility controls, language/theme toggles, desktop overflow at 1440×900 / 1366×768 / 1920×1080, and legacy asset-request detection. Browser artifacts are uploaded for inspection.

## 9. Browser proof gate — NOT CLAIMED UNTIL EXECUTED
- [ ] 🟡 Browser workflow passes on the canonical branch
- [ ] 🟡 Open `/workspace` without boot error
- [ ] 🟡 GT1/GT2/GT3 cascade passes
- [ ] 🟡 `Perdagangan` never appears
- [ ] 🟡 MAP → SATELLITE → HYBRID → MAP
- [ ] 🟡 Rings and Layers interactions pass
- [ ] 🟡 Planning intelligence modals pass
- [ ] 🟡 Utilities pass
- [ ] 🟡 Zero uncaught browser console errors
- [ ] 🟡 Zero critical workspace request failures
- [ ] 🟡 No legacy frontend assets requested
- [ ] 🟡 No page overflow at all three judge desktop sizes
- [ ] 🟡 Browser screenshots visually acceptable

The browser workflow is now executable, but its result has not been falsely marked PASS until an actual workflow run completes.

## 10. Source-side verdict
### **SOURCE FUNCTION SET: WIRED + HARDENED ✅**

The canonical chain is explicitly bridged and the runtime takeover is protected against duplicate boot, missing map globals, unrelated case-builder handler loss, and regression of the control contract.

### **BROWSER VERDICT: PENDING ACTUAL WORKFLOW RUN 🟡**

### **VISUAL VERDICT: PENDING CURRENT-BUILD SCREENSHOT REVIEW 🟡**

## 11. Render rule
**DO NOT TOUCH RENDER.**

Only after the browser gate passes, visual review is green, and the user explicitly authorizes `DEPLOY RENDER NOW`, perform one final Render deployment. No preview-service iteration and no automatic deployment loop.
