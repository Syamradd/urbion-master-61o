# URBION HORIZON — Master Release Checklist

Status: `CURRENT-CANDIDATE REPAIR / RELEASE LOCKED`

This is the single release-control checklist for the current canonical release. The only active release branch is `feature/canonical-workspace-v2`. Historical, parallel, temporary, forensic and legacy branches are retained as reference only and must not be deployed over the canonical release.

## 1. Canonical architecture

- [x] One active release branch: `feature/canonical-workspace-v2`
- [x] One production architecture: V5 Planning Workspace
- [x] One planning engine contract: `PHASE-E.8`
- [x] One evidence contract: `PHASE1.2`
- [x] One browser/API error contract: `URBION_ERROR_V1`
- [x] One canonical application entrypoint: `landing_server:app`
- [x] Existing Render launcher is a compatibility shim only: `workspace_v4_server:app → landing_server:app`
- [x] One canonical workspace route: `/workspace`
- [x] Deterministic planning/scoring engine preserved; no parallel planning/scoring engine introduced
- [x] Statutory boundary preserved: `NOT_CLAIMED`
- [x] Decision authority preserved: `NONE`

## 2. Functional / evidence capability

- [x] Site assessment and planning taxonomy
- [x] TOD 400 m / 800 m logic
- [x] Rule applicability/compliance and provenance
- [x] KPI evidence-state presentation
- [x] Canonical evidence packet propagation
- [x] What-If scenario flow
- [x] Decision Center + planner handoff
- [x] Bounded Copilot / agent convergence
- [x] Road Intelligence evidence attachment
- [x] Mobility / station source-context integrations
- [x] JPS station adapter preserved
- [x] MyGEMS lithology adapter preserved
- [x] MyEQMS/APIMS adapter preserved
- [x] GIS 25-layer runtime contract
- [x] KM / OSC readiness path
- [x] Output / decision-story path
- [x] BM / EN and theme controls
- [x] Existing Welcome page preserved
- [x] Canonical About Us page preserved

## 3. Deep repair pass — recovered from the laptop-night branch history

### Analysis / data contract

- [x] Legacy `Yes/No` perimeter-planting and pedestrian-walkway values no longer hard-fail canonical assessment; unknown values remain unverified rather than fabricated.
- [x] Workstation development inputs are propagated into the canonical proposal/evidence packet.
- [x] GFA + plot ratio can produce a transparent calculated site-area input when explicit site area is absent.
- [x] Development Impact reads explicit units/GFA/jobs/population/trips/road/flood/facility inputs and preserves `REVIEW_REQUIRED` where evidence is missing.
- [x] Development Impact UI is registered in the canonical workspace and now served by the production compatibility wrapper without importing the FastAPI app into the computational engine.
- [ ] Fresh end-to-end browser proof that `RUN SITE ANALYSIS` completes on the canonical case.

### GIS / map rendering

- [x] i-Plan WMS rendering uses the same-origin `/map/wms` proxy.
- [x] Critical Melaka Current Land Use is routed to the proven i-Plan ArcGIS service `GTsemasa_04/MapServer` for deterministic imagery.
- [x] Critical Melaka Zoning is routed to the proven i-Plan ArcGIS service `GTzoning_04/MapServer` for deterministic imagery.
- [x] ArcGIS imagery uses the same-origin `/map/arcgis` proxy.
- [x] Decorative map veil is forced below Leaflet imagery so overlay visibility is not visually masked by the workspace chrome.
- [x] GIS layer controls are reclaimed exactly once after the canonical catalogue renders; stale checkbox handlers are removed by cloning before binding.
- [x] Per-layer opacity sliders added to the visible GIS controls.
- [x] GIS layer states remain explicit: loading / rendered / source-connected / error.
- [x] Critical Current Land Use + Zoning can be auto-enabled for the initial planning view.
- [x] JMG Major Fault rendering has an authoritative MapServer + FeatureServer fallback path and bounded upstream timeouts.
- [ ] Fresh browser proof for each required 25-layer toggle + actual map imagery.
- [ ] Fresh GIS end-to-end audit of layer render success/failure states.

### Road / transport intelligence

- [x] Road Intelligence uses live OSM/Overpass source context without claiming Malaysian statutory hierarchy.
- [x] Multiple Overpass endpoints are attempted before reporting source unavailability.
- [x] Road results retain centroid coordinates so the UI can visualise nearby road context on the map.
- [x] Road hierarchy levels are presented explicitly in the Road Access drawer.
- [x] Road Access UI refreshes from the current site coordinates and can attach the result to the canonical evidence packet when analysis has run.
- [ ] Fresh browser proof of Road Access open → query → hierarchy result → map context.

### Visual / right rail

- [x] Development Impact compact visual surface.
- [x] Decision Story / Live Evidence Story / Review Gaps presentation owners retained.
- [x] Right rail spacing compacted for usable single-screen scanning.
- [x] Map controls retain Map / Satellite / Hybrid / Layers.
- [x] Canonical About raster master is served by production and remains the immutable visual source.
- [ ] Fresh visual regression after the complete repair pass.

## 4. Duplicate / overlap audit

### Code/runtime

- [x] `landing_server.py` is the canonical public production wrapper.
- [x] `championship_server.py` is the shared FastAPI application base, not a second planning engine.
- [x] `workspace_v2_server.py` is historical/preview-only.
- [x] `workspace_v4_server.py` is a compatibility launcher only.
- [x] New GIS visual hardening runs inside the existing workspace runtime compatibility path; no second planning engine is introduced.
- [x] Historical frontends remain isolated from `/workspace`.
- [x] Development Impact computation no longer imports `server.app`, removing the app import cycle; the UI asset is exposed only by the canonical compatibility wrapper.

### Render

- [x] Selected canonical deployment target: `urbion-horizon-workspace-v4`
- [x] Selected Render branch: `feature/canonical-workspace-v2`
- [x] Auto deploy remains OFF so Git ref movement cannot silently replace LIVE
- [x] Legacy Render surfaces are untouched
- [x] No new Render service is required

## 5. Selected Render target contract

Target service: `urbion-horizon-workspace-v4` (`srv-dahm749594qs73fk2tag`)

- runtime: `python`
- region: `singapore`
- plan: `free`
- build: `pip install -r requirements.txt`
- branch: `feature/canonical-workspace-v2`
- start: `uvicorn workspace_v4_server:app --host 0.0.0.0 --port $PORT`
- auto deploy: `off`

## 6. Laptop-night recovery trace (15 September 2026)

The branch history preserves the requested repair sequence from the laptop session. The recovered work, in order, was:

1. `01db...` — `fix(workspace): tolerate legacy Yes No analysis inputs`
2. `dfeb...` — `fix(workspace): normalize legacy boolean analysis inputs`
3. `995...` — `fix(ui): compact development impact panel`
4. `c718...` — `fix(analysis): enrich canonical assessment inputs for impact and evidence`
5. `20d1...` — `fix(ui): compact development impact presentation`
6. `cf239...` — `fix(workspace): harden defaults and critical map visibility`
7. `c3bfe390...` — `fix(gis): harden critical i-Plan land use proxy fallback`
8. `073...` — `fix(workspace): stabilize canonical defaults after taxonomy boot`
9. `700...` — `fix(analysis): expose canonical spatial context to evidence packet`
10. `5eb...` — `fix(workspace): harden map layers and road intelligence UI`
11. `f413...` — `fix(workspace): bootstrap GIS visual hardening layer`
12. `c420...` — `fix(road): harden live hierarchy source and retain map coordinates`
13. `68ab...` — `docs(release): record deep pre-render hardening pass`
14. `e5d60...` — `fix(workspace): serve bundled GIS visual hardening asset`
15. `fbf408...` — `fix(workspace): load bundled GIS hardening locally`
16. `ca55...` — `fix(workspace): harden canonical runtime presentation fallbacks`
17. `67d07...` — `fix(road): resolve canonical site coordinates in road UI`
18. `bfb596...` — `fix(road): expose canonical road action to runtime`
19. `f9897741...` — `fix(workspace): preserve canonical road action after hardening load`
20. `c997c7d...` — `fix(impact): register canonical development impact UI asset`
21. `fa62fa5...` — `fix(road): bound Overpass discovery latency and preserve live context`
22. `b25e01c...` — `fix(impact): remove app import cycle from planning engine`

Immediately after the laptop-night sequence, the About production asset repair was committed as `d29eb491...` (`fix(about): serve canonical About visual master`). The current-day recovery then added `78ce14c...` (`fix(ui): serve canonical development impact asset from production wrapper`) so the `b25e01...` import-cycle repair did not strand the canonical Development Impact UI asset.

## 7. Current candidate / CI truth

- [x] Current branch head is `78ce14c32780c4f9fe4588b48b74cd5ea87a80ef`.
- [x] Workspace Source Gate for current head: PASS (`35047772743`).
- [ ] Workspace Browser Gate for current head is still running (`35047772810`).
- [ ] Canonical Release Audit for current head is still running (`35047772883`).
- [x] Previous Browser Gate failure was isolated to `mygems-faults` in the strict 25-layer regression; other browser/dashboard stages passed.
- [x] Previous Canonical Release Audit completed its runtime topology / About / deep-browser stages; release remained blocked by GIS end-to-end/preflight evidence.
- [ ] Fresh current-head GIS proof is still required; do not mark green until the live regression proves the actual layer state.

## 8. Known non-blocking product gaps

These remain deliberately outside certification scope:

- 3D massing / buildable envelope
- persistent baseline vs alternatives comparison surface
- deeper existing-conditions metrics
- richer chart language / visual analytics
- stakeholder collaboration / saved scenarios
- advanced environmental simulation
- enterprise GIS/BIM connectors

## 9. Final certification sequence

- [x] Preserve pre-convergence canonical snapshot
- [x] Keep `feature/canonical-workspace-v2` as the sole active release branch
- [x] Reconcile release documentation to canonical branch
- [x] Integrate WMS proxy + GIS render truth repair
- [x] Integrate browser/GIS audit into canonical release workflow
- [x] Complete deep repair pass across analysis, GIS, road and visual surfaces
- [x] Recover and record the laptop-night repair sequence
- [x] Repair About visual asset serving in production
- [x] Repair Development Impact UI asset serving in production without reintroducing the app import cycle
- [ ] Fresh required CI on final candidate
- [ ] Fresh full functional workspace audit
- [ ] Fresh 25-layer GIS end-to-end audit
- [ ] Fresh Road Intelligence browser proof
- [ ] Fresh visual regression
- [ ] Controlled live smoke on the exact final deployed SHA
- [ ] Final release SHA lock
- [ ] Final release identity/tag

## Release gate

`RENDER = LOCKED`

The application is not declared production-ready until fresh current-head gates prove the complete repaired canonical workspace and controlled live smoke proves the exact deployed SHA. The currently LIVE Render revision remains the earlier About-repair deployment (`d29eb491...`) until a final candidate is deliberately deployed and verified.
