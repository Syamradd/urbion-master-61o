# URBION HORIZON — Final Functional Audit / Pre-Render Gate

## Status key
✅ source implementation complete
🟡 browser/runtime proof required
❌ confirmed defect

## Current checkpoint
Branch: `feature/canonical-workspace-v2`
Latest source checkpoint: `a98fd47d4a44127d68eeed7731c19a69f816c304`
Render: **LOCKED — no deployment / no iteration**.

## Latest source trace
PLANMalaysia currently publishes **Manual Sistem Maklumat Geografi (GIS) Rancangan Pemajuan Versi 3.0 / Versi 3 (2025)**. The official Version 3 manual contains the updated Guna Tanah 1 / 2 / 3 classification tables.

The public i-Plan analysis module still contains explanatory text referencing Version 2.0 for Level 1/2/3 terminology. The project therefore uses the latest official PLANMalaysia publication as the taxonomy source while recording that public-page distinction instead of falsely claiming the public analysis page has already migrated.

## 1. Canonical runtime
- [x] ✅ `/` → `welcome.html`
- [x] ✅ `/about` → `urbion_horizon_about.html`
- [x] ✅ `/workspace` → `workspace_v5.html`
- [x] ✅ Legacy championship frontend injection removed from canonical routes
- [x] ✅ Existing FastAPI planning engines preserved
- [x] ✅ `urbion_workspace_final.js` is the canonical planning function layer
- [x] ✅ `urbion_workspace_runtime.js` is the final visible-control takeover layer
- [x] ✅ Competing listeners on visible buttons/selectors are stripped before final bindings are attached

## 2. Guna Tanah 1 / 2 / 3 — latest classification
- [x] ✅ Canonical GT hierarchy is taken from `URBION_FINAL.GT`
- [x] ✅ GT1 → GT2 → GT3 is cascading and internally consistent
- [x] ✅ `Komersial` is the commercial GT1 term
- [x] ✅ Legacy `Perdagangan` is excluded from the visible runtime selectors
- [x] ✅ Selected GT1/GT2/GT3 values are included in the assessment payload
- [x] ✅ Runtime selector takeover prevents the older inline taxonomy from overriding the canonical taxonomy after load

## 3. Map / GIS controls
- [x] ✅ Leaflet map
- [x] ✅ MAP / OSM
- [x] ✅ SATELLITE / Esri World Imagery
- [x] ✅ HYBRID / imagery + reference labels
- [x] ✅ Site marker + map click
- [x] ✅ Locate / recenter
- [x] ✅ 400 m / 800 m / 1 km rings
- [x] ✅ Ring visibility toggles
- [x] ✅ Search → coordinates → map update
- [x] ✅ Road / transit context toggle
- [x] ✅ Basemap switch now removes existing workspace basemap first, preventing Satellite/Hybrid stacking over OSM

## 4. i-Plan layer drawer
- [x] ✅ `/map/layers?state=...`
- [x] ✅ Dynamic groups / source / type
- [x] ✅ GeoServer WMS renderer
- [x] ✅ TILE renderer
- [x] ✅ ArcGIS MapServer renderer
- [x] ✅ ON = real Leaflet layer added
- [x] ✅ OFF = real Leaflet layer removed
- [x] ✅ Error state / portal-only handling
- [x] ✅ Current land use / zoning / committed land use
- [x] ✅ Topography / heritage / CFS / ecology / KSAS / disaster-risk pathways through live catalogue

## 5. Planning analysis
- [x] ✅ `/workstation/analysis`
- [x] ✅ Case payload includes GT1 / GT2 / GT3
- [x] ✅ Readiness derived from returned state
- [x] ✅ Spatial findings
- [x] ✅ Planning implications
- [x] ✅ Review gaps
- [x] ✅ RT rule cards with proposed / requirement / status / reason / source
- [x] ✅ GP/GPP candidates
- [x] ✅ Evidence health / register hooks

## 6. What-If / Decision / Output
- [x] ✅ `/what-if` baseline + scenario
- [x] ✅ `/decision-center` status + rationale + planner action
- [x] ✅ Planner-ready Output with land-use hierarchy / RT / GP / gaps / authority boundary
- [x] ✅ Print / PDF
- [x] ✅ No APPROVED / REJECTED statutory claim

## 7. Utilities
- [x] ✅ About
- [x] ✅ Help
- [x] ✅ Sources
- [x] ✅ Status
- [x] ✅ Fullscreen
- [x] ✅ Reset
- [x] ✅ BM/EN visible toggle
- [x] ✅ Dark/light toggle

## 8. Release checklist — browser proof only
- [ ] 🟡 Open `/workspace`
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

## 9. Source-side verdict
### **FUNCTION SET: 100% WIRED IN SOURCE ✅**

The latest source pass specifically addressed the previous risk of multiple competing click listeners. The runtime now takes ownership of the visible controls after the canonical core loads and uses the workspace's actual Leaflet objects for basemap/ring/site operations.

### **RUNTIME VERDICT: PENDING BROWSER PROOF 🟡**

No claim of 100% runtime-tested acceptance is made until the browser/judge journey above has been executed.

## 10. Render rule
**DO NOT TOUCH RENDER.**

After every browser-gate item passes, and only after explicit user authorization, perform one final Render deployment. No preview-service iteration and no automatic deployment loop.
