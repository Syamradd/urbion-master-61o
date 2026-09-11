# URBION HORIZON — Functional Button Matrix

Branch: `feature/canonical-workspace-v2`

Rule: a control is only considered PASS when its click produces a visible state change, modal/result, map update, endpoint response, navigation, or browser utility action.

| Control | Canonical action | Expected visible result | Source |
|---|---|---|---|
| PLAN | activate planning view | closes modal / returns workspace view | runtime takeover |
| EVIDENCE | evidence view | evidence register + gaps modal | runtime takeover |
| WHAT-IF | `/what-if` | baseline/scenario comparison | core function layer |
| DECISION | `/decision-center` | status + rationale + planner action | core function layer |
| OUTPUT | output renderer | planner-ready case summary | core function layer |
| MAP | OSM basemap | map tiles switch | runtime basemap controller |
| SATELLITE | Esri World Imagery | imagery switch | runtime basemap controller |
| HYBRID | imagery + reference | imagery + labels switch | runtime basemap controller |
| LAYERS | `/map/layers?state=...` | dynamic catalogue opens/refreshes | core function layer |
| USE MAP | map selection mode | user can click map to set site | workspace map handler |
| LOCATE | recenter | marker/rings recenter | runtime takeover |
| 400m | ring toggle | 400m ring shown/hidden | runtime takeover |
| 800m | ring toggle | 800m ring shown/hidden | runtime takeover |
| 1km | ring toggle | 1km ring shown/hidden | runtime takeover |
| RUN SITE ANALYSIS | `/workstation/analysis` | RT/GP/evidence/intelligence populate | core function layer |
| View Evidence | evidence view | evidence register modal | runtime takeover |
| Generate Output | output renderer | output modal | core function layer |
| Print / PDF | `window.print()` | browser print dialog | workspace handler |
| CLOSE | close modal | modal disappears | runtime takeover |
| ABOUT | `/about` | dedicated About Us page | runtime utility |
| HELP | help modal | usage guidance appears | runtime utility |
| SOURCES | sources modal | source/basemap provenance | runtime utility |
| STATUS | health/metadata/layer checks | online/error states | runtime utility |
| FULLSCREEN | browser Fullscreen API | page enters/exits fullscreen | runtime utility |
| RESET | reload after confirmation | clean case state | runtime utility |
| BM/EN | language toggle | visible navigation labels switch | runtime utility |
| Dark/Light | theme toggle | workspace contrast/theme switches | runtime utility |

## Land-use control contract

`Guna Tanah 1` → `Guna Tanah 2` → `Guna Tanah 3 / Activity` must be cascading.

The visible selectors are rebound to the canonical `URBION_FINAL.GT` taxonomy after the core layer loads. Legacy `Perdagangan` is excluded from the visible runtime options; the commercial GT1 term is `Komersial`.

## Map control contract

Basemap switching is deliberately handled by the final runtime takeover instead of the core `setBase()` helper, because the workspace already owns the Leaflet base-layer objects. This prevents Satellite/Hybrid from stacking on top of the existing OSM base.

## Duplicate-handler containment

The runtime takeover clones the existing visible buttons and relevant controls after the canonical core script becomes available. This removes competing inline/core listeners before rebinding the visible control set once.

## Release gate

Source implementation is considered complete only for controls that have a deterministic handler. Browser proof is still required for final judge acceptance. Render remains intentionally locked until that browser gate passes.
