# URBION HORIZON — Final Pre-Render Functional Audit

## Status key
✅ Implemented in canonical source
🟡 Implemented; browser/runtime proof still required
❌ Not implemented

## 1. Public presentation / architecture
- [x] ✅ `/` → `welcome.html`
- [x] ✅ `/about` → dedicated About Us page
- [x] ✅ `/workspace` → `workspace_v5.html`
- [x] ✅ Legacy championship presentation injection removed
- [x] ✅ Single canonical workspace function layer: `urbion_workspace_final.js`
- [x] ✅ Existing backend/engines preserved; no duplicate planning engine

## 2. Latest PLANMalaysia land-use hierarchy
Source authority: PLANMalaysia, **Manual GIS Rancangan Pemajuan Versi 3 (2025)**.
- [x] ✅ 12 GT1 categories
- [x] ✅ 55 GT2 categories
- [x] ✅ 381 GT3 activities
- [x] ✅ Cascading GT1 → GT2 → GT3/activity
- [x] ✅ Current top-level commercial terminology is `Komersial`, not legacy `Perdagangan`
- [x] ✅ Residential hierarchy aligned to V3
- [x] ✅ Commercial hierarchy aligned to V3
- [x] ✅ Industrial hierarchy aligned to V3

## 3. Case Builder
- [x] ✅ Project/site, state, district, PBT, mukim, lot/UPI
- [x] ✅ Latitude / longitude
- [x] ✅ Development type / class / activity
- [x] ✅ GT1 / GT2 / GT3 cascading controls
- [x] ✅ Plot ratio / height / units / GFA
- [x] ✅ TOD / transport context
- [x] ✅ Environment / infrastructure / constraints / evidence / AI sections
- [ ] 🟡 Every control still needs one final browser click-through

## 4. GIS map + basemap
- [x] ✅ Leaflet map
- [x] ✅ OSM / MAP base
- [x] ✅ Esri Satellite
- [x] ✅ Hybrid = Satellite + reference labels
- [x] ✅ Map click/site selection
- [x] ✅ Locate control
- [x] ✅ 400 m ring
- [x] ✅ 800 m ring
- [x] ✅ 1 km context ring
- [x] ✅ `invalidateSize()` resize handling
- [ ] 🟡 Final browser proof that tiles, marker and rings paint/alignment remain correct

## 5. GIS layer drawer
- [x] ✅ `/map/layers?state=...` catalogue is loaded dynamically
- [x] ✅ Groups, source/type metadata and independent scrolling
- [x] ✅ GeoServer WMS support
- [x] ✅ XYZ/TILE support
- [x] ✅ ArcGIS MapServer tile support
- [x] ✅ Portal-only sources are explicitly marked `PORTAL` / `OPEN SOURCE` instead of faking a map layer
- [x] ✅ ON adds a real Leaflet layer
- [x] ✅ OFF removes the real Leaflet layer
- [x] ✅ Error state is shown when a layer fails
- [ ] 🟡 Final browser proof for the critical i-Plan / risk / ecology / heritage / technical layers

## 6. Planning Intelligence / Assessment
- [x] ✅ `/workstation/analysis` is called from canonical function layer
- [x] ✅ Readiness derived from returned response fields
- [x] ✅ Spatial signals surfaced
- [x] ✅ Planning implications surfaced
- [x] ✅ Evidence gaps surfaced
- [x] ✅ Bottom spatial/compliance docks updated from returned result
- [ ] 🟡 Final browser proof with a real case payload

## 7. RT compliance
- [x] ✅ Existing deterministic compliance engine reused
- [x] ✅ Dynamic rule cards
- [x] ✅ Proposed value
- [x] ✅ Requirement
- [x] ✅ Status
- [x] ✅ Reason / why
- [x] ✅ Source / traceability field
- [x] ✅ No statutory approval claim
- [ ] 🟡 Final browser proof of populated RT cards

## 8. GP / GPP intelligence
- [x] ✅ Existing guideline intelligence reused
- [x] ✅ Candidate guidelines rendered
- [x] ✅ Candidate/review status rendered
- [x] ✅ Topic/title and source rendered
- [x] ✅ Surfaced in Planning Intelligence
- [ ] 🟡 Final browser proof with returned guideline candidates

## 9. Evidence
- [x] ✅ Existing evidence model reused
- [x] ✅ Evidence health/count bound when returned
- [x] ✅ Evidence source/status/finding/implication fields supported
- [x] ✅ Evidence gaps surfaced
- [x] ✅ Live source context is not represented as statutory verification
- [ ] 🟡 Final browser proof of evidence register/gap rendering

## 10. What-If
- [x] ✅ Direct `/what-if` call
- [x] ✅ Baseline payload
- [x] ✅ Scenario overrides
- [x] ✅ Baseline vs scenario result UI
- [x] ✅ Returned ranking/best-candidate fields supported
- [x] ✅ No fabricated simulation values
- [ ] 🟡 Final browser proof

## 11. Decision
- [x] ✅ Direct `/decision-center` call
- [x] ✅ Decision status/recommendation
- [x] ✅ Rationale
- [x] ✅ Planner action / next actions
- [x] ✅ No APPROVED / REJECTED authority claim
- [ ] 🟡 Final browser proof

## 12. Output
- [x] ✅ Current case summary
- [x] ✅ GT1 → GT2 → GT3 summary
- [x] ✅ RT summary
- [x] ✅ GP/GPP count
- [x] ✅ Evidence gaps
- [x] ✅ Decision status
- [x] ✅ Print / PDF action
- [ ] 🟡 Final browser proof of complete generated output

## 13. Global controls
- [x] ✅ Print
- [x] ✅ Export/generate output shell
- [x] ✅ Reset/fullscreen family exists in canonical workspace family
- [x] ✅ About Us navigation
- [ ] 🟡 BM/EN full-string sweep
- [ ] 🟡 Dark/light contrast sweep

## 14. Visual acceptance
- [x] ✅ Premium dark urban-tech foundation
- [x] ✅ Cyan/mint URBION accent system
- [x] ✅ Horizontal URBION logo lockup
- [x] ✅ Map-first centre
- [x] ✅ Bottom intelligence dock
- [x] ✅ City/grid/route spatial-tech treatment in presentation pages
- [ ] 🟡 Final screenshot comparison against locked generated Workspace / Welcome / About references

## 15. Final judge journey
1. Welcome
2. Planning Workspace
3. Location + site selection
4. GT1 → GT2 → GT3
5. Development + intensity
6. Run analysis
7. GIS + layer evidence
8. RT compliance
9. GP/GPP
10. Evidence health/gaps
11. What-If
12. Decision Support
13. Planner-ready Output
14. Print/PDF
15. About Us

## Release gate
**FUNCTIONAL SOURCE LAYER: COMPLETE.**

**NO FINAL RENDER DEPLOY UNTIL ALL 🟡 ITEMS PASS ONE LOCAL BROWSER/JUDGE-FLOW QA RUN.**

This gate intentionally separates source implementation from visual/runtime proof. No additional frontend repair stack should be introduced unless a new defect is confirmed.
