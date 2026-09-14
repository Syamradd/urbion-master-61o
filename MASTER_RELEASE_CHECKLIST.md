# URBION HORIZON — Master Release Checklist

Status: `REPAIR INTEGRATED / FRESH VALIDATION RUNNING`

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
- [x] Deterministic planning/scoring engine preserved; no parallel scoring engine introduced
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

## 3. Current repair integrated on canonical head

- [x] i-Plan WMS rendering uses the same-origin `/map/wms` proxy
- [x] WMS query parameters are normalized case-insensitively before validation/forwarding
- [x] ArcGIS imagery uses the same-origin `/map/arcgis` proxy
- [x] About navigation is guarded to `/about`
- [x] English workspace label normalization retained
- [x] GIS layer catalogue remains restricted to the 24 core API IDs plus the explicit cadastral layer
- [x] GIS UI only reports `ON · RENDERED` after actual tile-load success; timeout/error remains a failure state
- [x] Existing Render service and launcher remain unchanged
- [x] Canonical release CI now includes browser + GIS end-to-end gates

## 4. Browser / regression proof

Prior candidate evidence remains historical reference only.

- [x] Prior candidate regression matrix: 17 lanes passed
- [x] Prior candidate runtime smoke passed
- [x] Prior candidate full regression passed
- [x] Prior candidate Workspace Browser Gate passed
- [x] Prior candidate Render Parity Gate passed
- [x] Prior candidate UX Contract passed
- [x] Prior candidate Final Command Centre Contract passed
- [x] Prior candidate browser evidence upload passed
- [x] Fresh current-head full regression passed on `ae91eabc` before subsequent hardening
- [ ] Fresh current-head regression after latest GIS/browser/docs hardening
- [ ] Fresh browser functional smoke after latest hardening
- [ ] Fresh 25-layer end-to-end GIS render audit after latest hardening
- [ ] Controlled live smoke on exact final deployed SHA

## 5. Duplicate / overlap control

### Code/runtime

- [x] `landing_server.py` is the canonical public production wrapper.
- [x] `championship_server.py` is the shared FastAPI application base, not a second planning engine.
- [x] `workspace_v2_server.py` is historical/preview-only.
- [x] `workspace_v4_server.py` is a compatibility launcher only.
- [x] Historical frontends are isolated from `/workspace`.

### Render

- [x] Selected canonical deployment target: `urbion-horizon-workspace-v4`
- [x] Selected Render branch: `feature/canonical-workspace-v2`
- [x] Auto deploy remains OFF so Git ref movement cannot silently replace LIVE
- [x] Legacy Render surfaces are untouched
- [x] No new Render service is required

## 6. Selected Render target contract

Target service: `urbion-horizon-workspace-v4` (`srv-dahm749594qs73fk2tag`)

- runtime: `python`
- region: `singapore`
- plan: `free`
- build: `pip install -r requirements.txt`
- branch: `feature/canonical-workspace-v2`
- start: `uvicorn workspace_v4_server:app --host 0.0.0.0 --port $PORT`
- auto deploy: `off`

Current live deployment: `ae91eabc6dcc4df9d5312294526ff65f9b7616c6` (intermediate validation build).
Current branch candidate: `59dba5abeccedf48af4417c215af3f8b27bdf72f`.
The branch candidate is not yet live because auto-deploy remains OFF.

## 7. Known non-blocking product gaps

These remain deliberately outside certification scope:

- 3D massing / buildable envelope
- persistent baseline vs alternatives comparison surface
- deeper existing-conditions metrics
- richer chart language / visual analytics
- stakeholder collaboration / saved scenarios
- advanced environmental simulation
- enterprise GIS/BIM connectors

## 8. Final certification sequence

- [x] Preserve pre-convergence canonical snapshot
- [x] Keep `feature/canonical-workspace-v2` as the sole active release branch
- [x] Reconcile release documentation to canonical branch
- [x] Integrate WMS proxy + GIS render truth repair
- [x] Integrate browser/GIS audit into canonical release workflow
- [ ] Fresh required CI on final candidate
- [ ] Fresh full functional workspace audit
- [ ] Fresh 25-layer GIS end-to-end audit
- [ ] Controlled live smoke on the exact final deployed SHA
- [ ] Final release SHA lock
- [ ] Final release identity/tag

## Release gate

`RENDER = LIVE ON AE91EABC / BRANCH CANDIDATE 59DBA5A NOT YET DEPLOYED`

The application is not declared production-ready until the fresh current-head gates pass and controlled live smoke proves the repaired canonical build on the exact deployed SHA.
