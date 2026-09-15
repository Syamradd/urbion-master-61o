# URBION HORIZON — Master Release Checklist

Status: `PRE-RENDER DEEP REPAIR / DEPLOYMENT LOCKED`

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

## 3. Deep pre-render repair pass

### Analysis / data contract

- [x] Legacy `Yes/No` perimeter-planting and pedestrian-walkway values no longer hard-fail canonical assessment; unknown values remain unverified rather than fabricated.
- [x] Workstation development inputs are propagated into the canonical proposal/evidence packet.
- [x] GFA + plot ratio can produce a transparent calculated site-area input when explicit site area is absent.
- [x] Development Impact reads explicit units/GFA/jobs/population/trips/road/flood/facility inputs and preserves `REVIEW_REQUIRED` where evidence is missing.
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
- [ ] Fresh visual regression after the complete repair pass.

## 4. Duplicate / overlap audit

### Code/runtime

- [x] `landing_server.py` is the canonical public production wrapper.
- [x] `championship_server.py` is the shared FastAPI application base, not a second planning engine.
- [x] `workspace_v2_server.py` is historical/preview-only.
- [x] `workspace_v4_server.py` is a compatibility launcher only.
- [x] New GIS visual hardening runs inside the existing workspace runtime compatibility path; no second planning engine is introduced.
- [x] Historical frontends remain isolated from `/workspace`.

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

Current branch is intentionally **not being rendered by this checklist pass**. Live state must not be treated as proof of the new repairs until controlled deployment + smoke is explicitly performed.

## 6. Known non-blocking product gaps

These remain deliberately outside certification scope:

- 3D massing / buildable envelope
- persistent baseline vs alternatives comparison surface
- deeper existing-conditions metrics
- richer chart language / visual analytics
- stakeholder collaboration / saved scenarios
- advanced environmental simulation
- enterprise GIS/BIM connectors

## 7. Final certification sequence

- [x] Preserve pre-convergence canonical snapshot
- [x] Keep `feature/canonical-workspace-v2` as the sole active release branch
- [x] Reconcile release documentation to canonical branch
- [x] Integrate WMS proxy + GIS render truth repair
- [x] Integrate browser/GIS audit into canonical release workflow
- [x] Complete deep pre-render repair pass across analysis, GIS, road and visual surfaces
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

The application is not declared production-ready until fresh current-head gates prove the complete repaired canonical workspace and controlled live smoke proves the exact deployed SHA.
