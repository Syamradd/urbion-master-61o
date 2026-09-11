# URBION HORIZON — Workspace V5.1 Audit

## Audit rule
Green means the capability is present and wired in source. Amber means UI exists but binding/presentation is incomplete. Red means the required capability is not yet implemented in the canonical workspace. Existing backend engines must be reused; do not duplicate planning logic.

## 1. Runtime / Architecture
- [x] Isolated preview app excludes legacy HTML/JS/CSS frontend routes.
- [x] Canonical workspace served at `/`.
- [x] Existing backend APIs/engines reused.
- [x] Single desktop workspace shell.
- [x] No legacy Championship UI dependency in canonical HTML.

## 2. Desktop Workspace Layout
- [x] Three-column layout: Case Builder / GIS / Planning Intelligence.
- [x] Left panel has independent vertical scrolling.
- [x] Centre contains map workspace and bottom intelligence dock.
- [x] Right rail scrolls independently.
- [ ] Left sections must be compacted further to eliminate unnecessary vertical whitespace.
- [ ] Bottom dock must be populated dynamically from analysis results.
- [ ] No large empty voids at common desktop resolutions.

## 3. Case Builder Inputs
- [x] Project/site name.
- [x] State.
- [x] District.
- [x] PBT.
- [x] Mukim.
- [x] Lot/UPI.
- [x] Latitude/longitude.
- [x] Map selection.
- [x] Locate.
- [x] Development type/class.
- [x] Activity/function.
- [x] Guna Tanah 1/2/3.
- [x] Plot ratio.
- [x] Building height.
- [x] Units.
- [x] GFA.
- [x] TOD coordinates/context inputs.
- [x] Perimeter planting.
- [x] Pedestrian walkway.
- [ ] Environmental inputs need complete visible section/binding.
- [ ] Infrastructure inputs need complete visible section/binding.
- [ ] Constraints/risk inputs need complete visible section/binding.
- [ ] Supporting evidence section needs complete visible controls.
- [ ] AI analysis/output section needs complete visible controls.

## 4. GIS Map
- [x] Leaflet map container.
- [x] OSM base layer.
- [x] Satellite base layer.
- [x] Map/Satellite controls.
- [x] Site marker concept.
- [x] Map click selection.
- [ ] Force `invalidateSize()` after layout/render.
- [ ] Robust tile/error fallback.
- [ ] 400 m ring.
- [ ] 800 m ring.
- [ ] 1 km context ring.
- [ ] Spatial-tech graphic overlay tied to actual site.

## 5. GIS Layer Drawer
- [x] Layer drawer UI.
- [x] Independent layer drawer scrolling.
- [x] Existing source catalogue available in backend/data layer.
- [ ] Actual i-Plan WMS/ArcGIS layers must be attached to Leaflet.
- [ ] Layer ON/OFF must add/remove real map layers, not just show a toast.
- [ ] Source/status metadata shown per layer.
- [ ] Layer loading/error state shown.
- [ ] Key layers to verify: current land use, zoning, committed land use, flood/risk, KSAS/CFS/ecology, heritage, topography, JPS/MyGEMS/MyEQMS/JUPEM pathways.

## 6. Assessment
- [x] Run Site Analysis button.
- [x] `/workstation/analysis` request path.
- [x] Existing integrated workstation engine reused.
- [ ] Response must populate readiness from actual evidence/compliance state, not a decorative/static score.
- [ ] Spatial findings must be surfaced.
- [ ] Planning implications must be surfaced.
- [ ] Evidence gaps must be surfaced.

## 7. RT / Planning Compliance
- [x] Existing RT MBMB rule retrieval engine.
- [x] Existing compliance engine.
- [x] Deterministic statuses include COMPLY, NON-COMPLIANCE, CONDITIONAL NON-COMPLIANCE and REQUIRES REVIEW.
- [ ] Compliance cards need dynamic UI binding.
- [ ] Show proposed value vs requirement.
- [ ] Show reason/why.
- [ ] Show source document/section/traceability.
- [ ] Preserve authority boundary: no statutory approval claim.

## 8. GP / Guidelines
- [x] Existing guideline intelligence engine/candidate concept.
- [ ] UI must display relevant GP/GPP candidates.
- [ ] Show candidate/review status.
- [ ] Show topic and source.
- [ ] Provide source navigation where available.

## 9. Evidence
- [x] Evidence model/source catalogue exists.
- [x] Evidence states/source classifications exist.
- [ ] Evidence health/count must be dynamically bound.
- [ ] Evidence register must show source, status, finding, implication.
- [ ] Evidence gaps must be visible.
- [ ] Distinguish live source context from statutory verification.

## 10. Planning Intelligence Rail
- [x] Readiness card shell.
- [x] Key findings shell.
- [x] Compliance shell.
- [x] Decision support shell.
- [x] Quick action shell.
- [ ] Populate all shells from actual assessment response.
- [ ] Show RT compliance.
- [ ] Show GP candidates.
- [ ] Show evidence health.
- [ ] Show constraints/risks.
- [ ] Show planner action.

## 11. What-If
- [x] What-If UI/control exists.
- [x] Existing `/what-if` backend exists.
- [ ] UI must call `/what-if` directly.
- [ ] Baseline vs scenario comparison.
- [ ] Scenario impacts.
- [ ] Ranking/decision support where returned by engine.
- [ ] No fake numerical simulation.

## 12. Decision
- [x] Existing decision engine/API exists.
- [ ] UI must show actual decision-support result.
- [ ] Evidence-backed rationale.
- [ ] Planner action.
- [x] No APPROVED/REJECTED authority claim.

## 13. Output
- [x] Output UI shell.
- [ ] Full case summary from actual state.
- [ ] RT/GP compliance summary.
- [ ] Evidence gaps.
- [ ] Decision-support summary.
- [ ] Source traceability.
- [ ] Print/export.

## 14. Global Controls
- [ ] BM/EN must translate all visible canonical UI strings.
- [ ] Dark/light theme must preserve contrast.
- [ ] Reset case.
- [ ] Fullscreen.
- [ ] Print.
- [ ] Export.
- [ ] Help.
- [ ] Data Sources.
- [ ] System Status.
- [ ] About Us.

## 15. Premium Visual Target
- [x] Dark premium foundation.
- [x] Cyan/mint URBION accent.
- [x] Map-first workstation.
- [ ] Proper horizontal URBION lockup scale.
- [ ] Premium spatial-tech graphic treatment.
- [ ] Subtle city/grid/route geometry.
- [ ] Site halo and contextual rings.
- [ ] Dense but readable information hierarchy.
- [ ] 90% visual match to locked generated reference.

## 16. Final Judge Journey — must pass end-to-end
1. Open workspace.
2. Define location.
3. Select site on map.
4. Set development / land-use / category / activity.
5. Set intensity.
6. Run assessment.
7. See spatial evidence.
8. See RT compliance.
9. See relevant GP.
10. See evidence health/gaps.
11. Run What-If.
12. Compare baseline/scenario.
13. Open Decision Support.
14. Generate planner-ready Output.
15. Print/export.

## Current conclusion
The V5 architecture is the correct foundation, but the canonical workspace is NOT final yet. The highest-priority remaining work is real GIS layer binding, dynamic assessment/RT/GP/evidence presentation, direct What-If/Decision/Output binding, compact geometry, and premium graphics. Do not declare Render-ready until these P0 items pass source-level QA.