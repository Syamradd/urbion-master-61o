# URBION HORIZON — Master Release Checklist

Status: `PRE-RENDER REPAIR / DEPLOYMENT LOCKED`

This is the single release-control checklist for final championship convergence. Historical worklists remain reference material; this file is the release gate summary.

## 1. Canonical architecture

- [x] One active release branch: `feature/championship-convergence-v1`
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
- [x] GIS 25-layer runtime regression
- [x] KM / OSC readiness path
- [x] Output / decision-story path
- [x] BM / EN and theme controls
- [x] Existing Welcome page preserved
- [x] Canonical About Us page preserved

## 3. Browser / regression proof

Audited candidate tree before the current Render-target reconciliation patch:
`c4555f505c9ef1c41d677eee85cff35d1a7e5a5d`

- [x] 17 regression lanes passed
- [x] Runtime smoke passed
- [x] Full regression passed
- [x] Workspace Browser Gate passed
- [x] Render Parity Gate passed
- [x] UX Contract passed
- [x] Final Command Centre Contract passed
- [x] Browser evidence upload passed
- [x] Main parity proven at audit time (`behind_by=0`)
- [x] Preservation matrix reviewed
- [ ] Fresh gates required again after current Render-target reconciliation patch

## 4. Duplicate / overlap audit

### Code/runtime

- [x] `landing_server.py` is the canonical public production wrapper.
- [x] `championship_server.py` is the shared FastAPI application base imported by `landing_server.py`; it is not a second planning engine.
- [x] `workspace_v2_server.py` remains historical/preview-only.
- [x] `workspace_v4_server.py` is now a compatibility launcher only and contains no competing app/routes/engine.
- [x] Historical frontends are isolated from the canonical `/workspace` runtime.

### Render services — fixed target

The `URBION HORIZON` Render workspace contains four existing web services. The user-selected deployment target is the existing V4 service below:

| Service | Role | Status |
|---|---|---|
| `urbion-horizon-workspace-v4` | **selected canonical deployment target** | **KEEP — RECONCILE BRANCH BEFORE DEPLOY** |
| `urbion-master-61o` | historical production surface | **LEGACY / DO NOT DEPLOY FOR THIS RELEASE** |
| `urbion-workspace-v2-preview` | legacy V2 preview | **LEGACY / DO NOT DEPLOY** |
| `urbion-horizon-championship` | legacy championship surface | **LEGACY / DO NOT DEPLOY** |

No new Render service is required. Legacy surfaces remain untouched until release is proven.

## 5. Selected Render target contract

Target service: `urbion-horizon-workspace-v4` (`srv-dahm749594qs73fk2tag`)

### Existing configuration

- runtime: `python`
- region: `singapore`
- plan: `free`
- build: `pip install -r requirements.txt`
- current branch: `feature/canonical-workspace-v2`
- current start: `uvicorn workspace_v4_server:app --host 0.0.0.0 --port $PORT`
- auto deploy: `off`

### Required release behavior

- branch must be promoted/reconciled to the approved release branch: `feature/championship-convergence-v1`
- keep the existing start command `uvicorn workspace_v4_server:app --host 0.0.0.0 --port $PORT`
- `workspace_v4_server:app` must resolve directly to the canonical `landing_server:app` application
- `/` must serve the canonical Welcome page
- `/about` must serve the canonical About Us page
- `/workspace` must serve the canonical V5 Planning Workspace
- canonical backend/API routes must remain available through the same app

This design deliberately preserves the user's existing Render service and its Welcome/About work while removing the V4 application as a competing runtime.

## 6. Known non-blocking product gaps

These are deliberate post-release enhancement items, not grounds for changing the planning engine during final freeze:

- 3D massing / buildable envelope
- persistent baseline vs alternatives comparison surface
- deeper existing-conditions metrics
- richer chart language / visual analytics
- stakeholder collaboration / saved scenarios
- advanced environmental simulation
- enterprise GIS/BIM connectors

They remain tracked in `DASHBOARD_WORLD_GAP_WORKLIST.md`.

## 7. Final release sequence

- [x] Repair code contracts and stale tests
- [x] Prove canonical browser/runtime behavior on the prior candidate tree
- [x] Prove main parity at the prior candidate tree
- [x] Audit Render workspace and identify the user's selected target service
- [x] Replace the V4 server's competing application with a canonical compatibility shim
- [x] Reconcile release documents to the selected target service
- [ ] Fresh required CI on the final post-repair SHA
- [ ] Confirm selected Render service branch is the approved release branch
- [ ] Do not trigger deployment yet
- [ ] Final release SHA lock after fresh gates
- [ ] Deploy the existing `urbion-horizon-workspace-v4` service only
- [ ] Controlled live smoke across Welcome / About / Workspace / decision / GIS / evidence routes
- [ ] Verify live commit equals final release SHA
- [ ] Record release identity/tag
- [ ] Only then remove/decommission legacy Render surfaces if explicitly authorized

## Release gate

`RENDER = LOCKED`

The application is not declared production-ready until the selected existing Render service is running the canonical application from the approved release SHA and controlled live smoke passes.
