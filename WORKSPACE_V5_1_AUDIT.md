# URBION HORIZON — Final Functional Audit / Pre-Render Gate

## Status key
✅ verified / complete
🟡 remaining visual or release review
❌ confirmed defect

## Current checkpoint
Branch: `feature/canonical-workspace-v2`.
Latest UI checkpoint: `7d167ae6b7d7d324b91c607850f99b5595371f94`.
Render: **LOCKED — no deployment / no iteration**.

## Verified automated gates
- Source Gate run **34573597019** — **GREEN / SUCCESS**.
- Browser Gate run **34573597055** — **GREEN / SUCCESS**.
- Browser smoke executed on the canonical presentation server and completed successfully.
- Browser evidence artifact was generated.

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
- [x] Canonical presentation-boundary compatibility for workspace decision payload

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
### Defects A–F
**ALL REPAIRED / VERIFIED ✅**

The canonical bridge, timing guard, runtime boot guard, defensive map access, scoped control takeover, source contract gate and executable Playwright browser gate are all in place. The browser gate now confirms the repaired control chain in an actual Chromium run.

## 9. Browser proof gate — VERIFIED
- [x] Browser workflow passes on the canonical branch
- [x] Open `/workspace` without boot error
- [x] GT1/GT2/GT3 cascade passes
- [x] `Perdagangan` never appears
- [x] MAP → SATELLITE → HYBRID switching passes
- [x] Rings and Layers interactions pass
- [x] Planning intelligence modals pass
- [x] Utilities pass
- [x] Zero uncaught browser console errors in the smoke run
- [x] Zero critical workspace request failures
- [x] No legacy frontend assets requested
- [x] No page overflow at 1440×900 / 1366×768 / 1920×1080
- [x] Browser evidence screenshots generated

## 10. Visual convergence checkpoint
**Latest visual repair pass:** Welcome + About.

### Welcome
- [x] Generated-reference navigation hierarchy aligned
- [x] Hero headline aligned to “From Spatial Evidence / to Better Planning / Decisions.”
- [x] Cyan/mint futuristic palette retained
- [x] Starfield retained
- [x] Smart-city skyline treatment strengthened
- [x] Site highlight / route / planning callouts added
- [x] Four capability blocks aligned to reference language
- [x] Bottom metrics / quote band added to match generated composition

### About
- [x] Generated-reference navigation hierarchy aligned
- [x] “Planning for a Better Tomorrow.” hero restored
- [x] Smart-city atmospheric hero graphic strengthened
- [x] Mission / Vision composition aligned to reference
- [x] Team section retained with the three confirmed members
- [x] UiTM / Town and Regional Planning identity retained
- [x] Starfield / grid / cyan-mint visual language retained

### Workspace
- [x] GIS-first 3-column planning command-centre architecture preserved
- [x] Dark/cyan/mint visual system preserved
- [x] Smart-city/starfield atmosphere retained without obstructing GIS content
- [x] Functional structure intentionally not replaced by marketing UI
- [x] Browser gate confirms current workspace interactions

## 11. Current release verdict
### **FUNCTIONAL: GREEN ✅**
Source gate + browser gate are both successful on the latest UI checkpoint.

### **VISUAL: IMPROVED / FINAL SCREEN REVIEW REMAINS 🟡**
Welcome and About have been brought materially closer to the generated references. Workspace remains intentionally GIS-first and should receive only targeted visual polish if a remaining concrete mismatch is identified.

## 12. Render rule
**DO NOT TOUCH RENDER.**

Only after the final visual review is green and the user explicitly authorizes `DEPLOY RENDER NOW`, perform one final Render deployment. No preview-service iteration and no automatic deployment loop.