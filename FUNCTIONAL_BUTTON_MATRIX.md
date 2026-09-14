# URBION HORIZON — Functional Button Matrix

Branch: `feature/canonical-workspace-v2`

Rule: a control is **PASS** only when its click produces a visible state change, modal/result, map update, endpoint response, navigation, or browser utility action. Automated browser evidence is the release proof; source presence alone is not enough.

| Control | Canonical action | Expected visible result | Source |
|---|---|---|---|
| PLAN | activate planning view | closes modal / returns workspace view | canonical UI owner |
| EVIDENCE | evidence view | evidence register + gaps modal | canonical UI owner |
| WHAT-IF | `/what-if` | baseline/scenario comparison | core function layer |
| DECISION | `/decision-center` | status + rationale + planner action | core function layer |
| OUTPUT | output renderer | planner-ready case summary | core function layer |
| MAP | OSM basemap | map tiles visible | runtime basemap controller |
| SATELLITE | Esri World Imagery | imagery switch | runtime basemap controller |
| HYBRID | imagery + reference | imagery + labels switch | runtime basemap controller |
| LAYERS | `/map/layers?state=...` | dynamic catalogue opens/refreshes | GIS layer manager |
| USE MAP | map selection mode | user can click map to set site | workspace map handler |
| LOCATE | recenter | marker/rings recenter | runtime takeover |
| 400m | ring toggle | 400m ring shown/hidden | runtime takeover |
| 800m | ring toggle | 800m ring shown/hidden | runtime takeover |
| 1km | ring toggle | 1km ring shown/hidden | runtime takeover |
| RUN SITE ANALYSIS | `/workstation/analysis` | RT/GP/evidence/intelligence populate | deterministic core function layer |
| View Evidence | evidence view | evidence register modal | canonical evidence owner |
| Generate Output | output renderer | output modal | core function layer |
| Print / PDF | `window.print()` | browser print dialog | workspace handler |
| CLOSE | close modal | modal disappears | modal owner |
| ABOUT | `/about` | dedicated canonical About Us page | runtime guard |
| HELP | help modal | usage guidance appears | utility owner |
| SOURCES | sources modal | source/basemap provenance | utility owner |
| STATUS | health/metadata/layer checks | online/error states | utility owner |
| FULLSCREEN | browser Fullscreen API | page enters/exits fullscreen | utility owner |
| RESET | reload after confirmation | clean case state | utility owner |
| BM/EN | language toggle | visible navigation labels switch | utility owner |
| Dark/Light | theme toggle | workspace contrast/theme switches | utility owner |

## Land-use control contract

`Land Use Level 1` → `Land Use Level 2` → `Land Use Level 3 / Activity` must be cascading.

The visible selectors are rebound to the canonical `URBION_FINAL.GT` taxonomy after the core layer loads. The final user-facing GT1 term is `Commercial`; legacy Malay labels are not part of the final user-facing contract.

## Location hierarchy contract

State and PBT options are locally available from the canonical PBT catalogue. District fallback data is locally embedded so a temporary failure of the external geography JSON does not leave the State → District chain empty. External geography may enrich subdistrict/mukim detail when available; missing external data must never be treated as statutory verification.

## Map control contract

Basemap switching is deliberately handled by the canonical UI owner so Satellite/Hybrid do not stack on top of the existing OSM base.

GIS overlay rendering is source-backed: a layer is displayed as `ON · RENDERED` only after a real tile/image load event. Network timeout or tile errors remain visible as failure states.

## Duplicate-handler containment

The canonical UI owner removes competing handlers from the controls it owns and rebinds the visible control set once. Compatibility/bootstrap assets must not introduce a second planning engine or a second owner for the same control.

## Release gate

Source implementation is considered complete only for controls that have deterministic handlers. Browser evidence is required for final judge acceptance. Render remains frozen until the final GitHub gates are green and exact-SHA live QA is explicitly started.