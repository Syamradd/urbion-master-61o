# URBION HORIZON — Final Pre-Render Audit

## Status key
✅ Source-ready / implemented
🟡 Implemented but final browser proof still required
❌ Not yet safe to call final

## 1. Public presentation routes
- [x] ✅ Root `/` points directly to the locked Welcome page.
- [x] ✅ `/about` points to a dedicated About Us page.
- [x] ✅ `/workspace` points to the canonical workspace.
- [x] ✅ Legacy championship presentation injection removed from `landing_server.py`.
- [x] ✅ No new frontend repair middleware is being stacked.

## 2. Welcome Page
- [x] ✅ Premium dark urban-tech visual language.
- [x] ✅ Official URBION HORIZON dark logo.
- [x] ✅ Hero + GIS / Evidence / What-If / Decision feature treatment.
- [x] ✅ CTA enters Planning Workspace.
- [x] ✅ About navigation present.
- [ ] 🟡 Final desktop screenshot proof still required.

## 3. About Us
- [x] ✅ Dedicated page with same visual language as Welcome.
- [x] ✅ UiTM Puncak Alam identity and degree line.
- [x] ✅ Team photo embedded as a repository asset.
- [x] ✅ Team names shown without role labels.
- [x] ✅ Names: Muhammad Syamir Aidid; Wan Nur Alea Najihah; Nur Isam Fahmi.
- [ ] 🟡 Final desktop screenshot proof still required.

## 4. Canonical Workspace shell
- [x] ✅ Three-column Case Builder / GIS / Planning Intelligence structure.
- [x] ✅ Independent left and right scrolling.
- [x] ✅ Map-first centre workspace + bottom dock.
- [x] ✅ Compact left planning case controls.
- [x] ✅ Official horizontal logo scale in canonical source.
- [ ] 🟡 Final screenshot proof against locked generated reference.

## 5. Case Builder inputs
- [x] ✅ Location / state / district / PBT / mukim / lot-UPI / lat-long.
- [x] ✅ Map selection and locate.
- [x] ✅ Development type / category / activity.
- [x] ✅ Land use 1 / 2 / 3.
- [x] ✅ Plot ratio / height / units / GFA.
- [x] ✅ TOD / transport / environment / infrastructure / constraints / evidence / AI / output sections exist in the canonical workspace source.
- [ ] 🟡 Full interaction QA on every field still required.

## 6. GIS map
- [x] ✅ Leaflet map and OSM base layer.
- [x] ✅ Satellite + hybrid basemap controls.
- [x] ✅ Map click / site selection.
- [x] ✅ 400 m / 800 m / 1 km ring logic present in the improved workspace prototype.
- [x] ✅ Resize invalidation is present in the improved workspace prototype.
- [ ] 🟡 Final runtime proof that tiles always paint correctly.
- [ ] 🟡 Final runtime proof that rings and marker remain aligned after resize.

## 7. GIS layer drawer
- [x] ✅ Layer drawer UI and scroll.
- [x] ✅ `/map/layers` catalogue path exists.
- [ ] ❌ Final canonical source still needs proof that every selected i-Plan / risk / ecology / heritage / technical layer is really attached to Leaflet and removed on toggle.
- [ ] ❌ Final source must surface per-layer loading/error/source state consistently.

## 8. Assessment / Planning Intelligence
- [x] ✅ `/workstation/analysis` endpoint path is used.
- [x] ✅ Existing backend analysis engine is reused.
- [ ] ❌ Readiness must be proven dynamic from returned evidence/compliance state.
- [ ] ❌ Spatial findings, implications and gaps must be visibly bound to the right rail and bottom dock.

## 9. RT compliance
- [x] ✅ Deterministic RT / compliance engines remain available.
- [ ] ❌ Final workspace UI must show proposed value vs requirement, status, reason and source traceability dynamically.
- [x] ✅ Authority boundary retained: no statutory approval claim.

## 10. GP / Guidelines
- [x] ✅ Guideline intelligence engine/candidate concept exists.
- [ ] ❌ Final UI binding for relevant GP/GPP candidates, topic, source and review status still needs proof.

## 11. Evidence
- [x] ✅ Evidence model and source classifications exist.
- [ ] ❌ Final UI must show evidence health/count, register, source, status, gaps and live-vs-verified distinction dynamically.

## 12. What-If
- [x] ✅ Existing `/what-if` engine exists.
- [ ] 🟡 Improved workspace prototype calls `/what-if` directly and renders baseline/scenario results; final GitHub source still needs final proof that this is the active canonical runtime.

## 13. Decision
- [x] ✅ Existing `/decision-center` engine exists.
- [ ] 🟡 Improved workspace prototype calls `/decision-center`; final canonical runtime binding still needs proof.
- [x] ✅ No APPROVED / REJECTED authority claim.

## 14. Output
- [x] ✅ Print/export shell exists.
- [ ] 🟡 Final output must be proven to include current case state, RT/GP summary, evidence gaps, decision rationale and source traceability.

## 15. Global controls
- [x] ✅ Reset / fullscreen / print / export controls exist in the canonical workspace family.
- [ ] 🟡 BM/EN needs full-string QA with no mixed-language leftovers.
- [ ] 🟡 Light/dark needs final contrast QA.
- [x] ✅ About Us route exists.

## 16. Final judge journey
1. Open Welcome.
2. Enter Planning Workspace.
3. Define location and site.
4. Set development / land use / category / activity / intensity.
5. Run analysis.
6. Inspect GIS + evidence.
7. Inspect RT compliance + GP candidates.
8. Inspect evidence health and gaps.
9. Run What-If.
10. Open Decision Support.
11. Generate planner-ready Output.
12. Print/export.
13. Return to About Us.

## Release gate
**NO FINAL RENDER DEPLOY UNTIL ALL ❌ ITEMS IN SECTIONS 7–11 AND THE CANONICAL What-If/Decision/Output BINDINGS ARE PROVEN IN SOURCE + LOCAL BROWSER QA.**

Current direction is deliberate: backend/engines are preserved; the public presentation layer is being isolated instead of adding another repair overlay.