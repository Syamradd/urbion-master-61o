# URBION HORIZON — Final Functional Audit / Pre-Render Gate

## Status key
✅ source implementation complete
🟡 browser/runtime proof required
❌ confirmed defect

## Current checkpoint
Branch: `feature/canonical-workspace-v2`.
Latest source repair: `8f8751a5bddebf40ac03bc98e75b09f8b90b315a`.
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
- [x] Bridge waits for the actual core functions before publishing the API
- [x] `urbion_workspace_runtime.js` remains the final visible-control runtime layer
- [x] Duplicate runtime boot is guarded
- [x] Runtime map/global access is defensive
- [x] Runtime takeover is now scoped only to runtime-owned controls; canonical case-builder handlers are preserved

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

The runtime previously cloned every button on the page before rebinding its own controls. The takeover is now scoped to runtime-owned controls only, preserving native case-builder interactions and preventing silent handler loss. A source-gate regression check now protects this contract.

## 9. Browser proof gate — NOT CLAIMED UNTIL EXECUTED
- [ ] 🟡 Open `/workspace`
- [ ] 🟡 No console boot error
- [ ] 🟡 GT1 list matches canonical latest taxonomy
- [ ] 🟡 Selecting GT1 changes valid GT2 choices
- [ ] 🟡 Selecting GT2 changes valid GT3 activity choices
- [ ] 🟡 `Perdagangan` never appears
- [ ] 🟡 MAP → SATELLITE → HYBRID → MAP
- [ ] 🟡 Layer catalogue loads and at least one real WMS/TILE layer paints
- [ ] 🟡 Layer OFF removes the painted layer
- [ ] 🟡 Map click / Locate moves marker and rings
- [ ] 🟡 Search selects a location and recentres map
- [ ] 🟡 Run Site Analysis populates RT / GP / evidence / intelligence
- [ ] 🟡 What-If returns a baseline/scenario result
- [ ] 🟡 Decision Support returns status/rationale/action
- [ ] 🟡 Output contains the case + GT hierarchy + planning results + gaps
- [ ] 🟡 Print/PDF launches print flow
- [ ] 🟡 BM/EN does not leave mixed labels or broken controls
- [ ] 🟡 Dark/light does not clip or destroy contrast
- [ ] 🟡 Welcome / Workspace / About visual check against locked references

**Browser limitation:** source/connector inspection is available in this working environment, but a full interactive browser session with console inspection is not exposed here. Therefore the browser gate remains honestly marked 🟡 rather than falsely marked PASS.

## 10. Source-side verdict
### **SOURCE FUNCTION SET: WIRED + HARDENED ✅**

The canonical chain is explicitly bridged and the runtime takeover is protected against duplicate boot, missing map globals, and unrelated case-builder handler loss.

### **RUNTIME VERDICT: PENDING BROWSER PROOF 🟡**

No claim of 100% runtime-tested acceptance is made until the browser/judge journey above has been executed.

## 11. Render rule
**DO NOT TOUCH RENDER.**

Only after the browser gate passes, and only after explicit user authorization, perform one final Render deployment. No preview-service iteration and no automatic deployment loop.
