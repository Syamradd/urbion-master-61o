# URBION HORIZON — Final Functional Audit / Pre-Render Gate

## Status key
✅ source implementation complete
🟡 browser/runtime proof required

## Latest source trace
PLANMalaysia currently publishes **Manual Sistem Maklumat Geografi (GIS) Rancangan Pemajuan Versi 3.0 / Versi 3 (2025)**. The official Version 3 manual contains the updated Guna Tanah 1 / 2 / 3 classification tables. citeturn556067search0turn556067search6

The public i-Plan analysis module still contains explanatory text referencing Version 2.0 for the Level 1/2/3 terminology, so the project records that source distinction explicitly rather than pretending the two pages say the same thing. citeturn556067search4

## 1. Canonical runtime
- [x] ✅ `/` → `welcome.html`
- [x] ✅ `/about` → `urbion_horizon_about.html`
- [x] ✅ `/workspace` → `workspace_v5.html`
- [x] ✅ Legacy championship frontend injection removed from canonical routes
- [x] ✅ Existing FastAPI planning engines preserved
- [x] ✅ `urbion_workspace_final.js` is the canonical planning function layer
- [x] ✅ `urbion_workspace_runtime.js` supplies final utility/runtime integration

## 2. Guna Tanah 1 / 2 / 3 — latest classification
- [x] ✅ Runtime taxonomy uses the repo's latest traced PLANMalaysia Version 3 (2025) classification data
- [x] ✅ GT1 → GT2 → GT3 is cascading and internally consistent
- [x] ✅ `Komersial` is used as the commercial GT1 term
- [x] ✅ Legacy `Perdagangan` is removed from runtime selector options
- [x] ✅ Residential GT2/GT3 hierarchy is populated from GT1 selection
- [x] ✅ Commercial GT2/GT3 hierarchy is populated from GT1 selection
- [x] ✅ Industrial GT2/GT3 hierarchy is populated from GT1 selection
- [x] ✅ Institutional/community facilities, recreation, development land, transport, infrastructure/utilities, agriculture, forest, water body and coastal classes are represented by the runtime taxonomy
- [x] ✅ Selected GT1/GT2/GT3 values are included in the assessment payload

## 3. Case Builder — functional controls
- [x] ✅ Project/site name
- [x] ✅ State / district / PBT / mukim / lot-UPI
- [x] ✅ Latitude / longitude
- [x] ✅ Map selection / locate
- [x] ✅ Development type / project reference / development class
- [x] ✅ GT1 / GT2 / GT3
- [x] ✅ Plot ratio / height / units / GFA
- [x] ✅ Perimeter planting / pedestrian walkway
- [x] ✅ TOD coordinates / precinct
- [x] ✅ Environmental / risk notes
- [x] ✅ Infrastructure / utilities notes
- [x] ✅ Constraints / supporting evidence
- [x] ✅ Analysis focus
- [x] ✅ Output controls

## 4. GIS map / basemap
- [x] ✅ Leaflet map
- [x] ✅ MAP / OpenStreetMap
- [x] ✅ SATELLITE / Esri World Imagery
- [x] ✅ HYBRID / satellite + reference labels
- [x] ✅ Site marker
- [x] ✅ Map click updates site
- [x] ✅ Locate recentres map
- [x] ✅ 400 m ring
- [x] ✅ 800 m ring
- [x] ✅ 1 km ring
- [x] ✅ Ring ON/OFF controls
- [x] ✅ `invalidateSize(true)` refresh
- [x] ✅ Search → coordinate → map workflow
- [x] ✅ Road/context overlay

## 5. i-Plan layer drawer / real rendering
- [x] ✅ `/map/layers?state=...` catalogue is loaded dynamically
- [x] ✅ Layer groups / source / type metadata
- [x] ✅ Independent layer drawer scrolling
- [x] ✅ GeoServer WMS renderer
- [x] ✅ XYZ/TILE renderer
- [x] ✅ ArcGIS MapServer tile renderer
- [x] ✅ Actual ON = add Leaflet layer
- [x] ✅ Actual OFF = remove Leaflet layer
- [x] ✅ Layer error state
- [x] ✅ Portal-only sources are not faked as map layers
- [x] ✅ Current land use / zoning / committed land use support
- [x] ✅ Topography / heritage / CFS / ecology / KSAS / disaster-risk support through the dynamic catalogue

PLANMalaysia's current GeoWebCache exposes the land-use, zoning, committed-use and related spatial layer families used by this workflow. citeturn200549search0

## 6. Site Analysis / Planning Intelligence
- [x] ✅ `/workstation/analysis`
- [x] ✅ Actual case payload sent to engine
- [x] ✅ Readiness derived from returned fields
- [x] ✅ Spatial signals surfaced
- [x] ✅ Planning implications surfaced
- [x] ✅ Evidence gaps surfaced
- [x] ✅ Bottom docks updated from returned result

## 7. RT compliance
- [x] ✅ Existing deterministic compliance engine reused
- [x] ✅ Dynamic rule cards
- [x] ✅ Proposed value
- [x] ✅ Requirement / target
- [x] ✅ Status
- [x] ✅ Reason / why
- [x] ✅ Source / traceability
- [x] ✅ No statutory approval claim

## 8. GP / GPP
- [x] ✅ Existing guideline intelligence reused
- [x] ✅ Candidate guidelines rendered
- [x] ✅ Candidate/review state supported
- [x] ✅ Topic/title/source supported
- [x] ✅ Surface in Planning Intelligence

## 9. Evidence
- [x] ✅ Existing evidence model reused
- [x] ✅ Source/status/finding/implication fields supported
- [x] ✅ Evidence health/count displayed when returned
- [x] ✅ Review gaps displayed
- [x] ✅ Live source context explicitly separated from statutory verification

## 10. What-If
- [x] ✅ Direct `/what-if`
- [x] ✅ Baseline
- [x] ✅ Scenario overrides
- [x] ✅ Baseline vs scenario comparison
- [x] ✅ Decision delta / ranking supported when returned
- [x] ✅ No fabricated numerical simulation

## 11. Decision Support
- [x] ✅ Direct `/decision-center`
- [x] ✅ Decision status / recommendation
- [x] ✅ Rationale
- [x] ✅ Planner action / next action
- [x] ✅ No APPROVED / REJECTED authority claim

## 12. Output
- [x] ✅ Case summary
- [x] ✅ GT1 → GT2 → GT3 summary
- [x] ✅ RT summary
- [x] ✅ GP/GPP summary
- [x] ✅ Evidence gaps
- [x] ✅ Decision-support status
- [x] ✅ Print / PDF

## 13. Global controls
- [x] ✅ BM/EN control
- [x] ✅ Dark/light theme
- [x] ✅ Reset
- [x] ✅ Fullscreen
- [x] ✅ Print / PDF
- [x] ✅ Data Sources
- [x] ✅ System Status
- [x] ✅ Help
- [x] ✅ About Us

## 14. Visual presentation preserved
- [x] ✅ Current three-column premium workspace presentation retained
- [x] ✅ Map-first centre retained
- [x] ✅ Existing visual hierarchy retained while functions were repaired
- [x] ✅ Horizontal URBION logo lockup retained
- [x] ✅ No new legacy repair stack introduced

## 15. FUNCTIONAL VERDICT
### **100% SOURCE-WIRED FUNCTION SET ✅**

The requested functional set is implemented in canonical source: Version 3 GT hierarchy, cascading GT1/GT2/GT3, MAP/SATELLITE/HYBRID, real i-Plan layer ON/OFF, spatial rings, analysis, RT, GP, evidence, What-If, Decision, Output and utility controls.

## 16. FINAL BROWSER GATE — NOT MISSING FEATURES
These are proof checks only:
- [ ] 🟡 Open `/workspace`
- [ ] 🟡 Confirm GT1/GT2/GT3 visibly matches the runtime Version 3 taxonomy
- [ ] 🟡 Confirm `Perdagangan` never appears in the visible selectors
- [ ] 🟡 Click MAP → SATELLITE → HYBRID
- [ ] 🟡 Open LAYERS and turn a real i-Plan layer ON
- [ ] 🟡 Turn the same layer OFF and confirm it disappears
- [ ] 🟡 Move the site and confirm 400m / 800m / 1km rings move with it
- [ ] 🟡 Run Site Analysis
- [ ] 🟡 Verify RT + GP + Evidence + right-rail intelligence populate
- [ ] 🟡 Run What-If
- [ ] 🟡 Run Decision Support
- [ ] 🟡 Generate Output / Print PDF
- [ ] 🟡 Check BM/EN and dark/light behavior
- [ ] 🟡 Compare final desktop viewport with locked visual reference

## 17. Render rule
**NO ITERATIVE RENDER.**

Only after all browser-gate checks pass: perform **ONE FINAL RENDER DEPLOYMENT**.

