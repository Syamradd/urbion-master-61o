# URBION HORIZON — Master Release Checklist

Status: `PRE-RENDER REPAIR / DEPLOYMENT LOCKED`

This is the single release-control checklist for final championship convergence. Historical worklists remain reference material; this file is the release gate summary.

## 1. Canonical architecture

- [x] One active release branch: `feature/championship-convergence-v1`
- [x] One production architecture: V5 Planning Workspace
- [x] One planning engine contract: `PHASE-E.8`
- [x] One evidence contract: `PHASE1.2`
- [x] One browser/API error contract: `URBION_ERROR_V1`
- [x] One production entrypoint: `landing_server:app`
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

## 3. Browser / regression proof

Audited candidate tree before this checklist commit:
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
- [ ] Fresh gates required again after this documentation-only release reconciliation commit

## 4. Duplicate / overlap audit

### Code/runtime

- [x] `landing_server.py` is the canonical public production wrapper.
- [x] `championship_server.py` is retained as the shared FastAPI application base imported by `landing_server.py`; it is not a second planning engine.
- [x] `workspace_v2_server.py` is a historical preview entrypoint.
- [x] `workspace_v4_server.py` is a historical preview entrypoint.
- [x] No `workspace_v3_server.py` exists at the audited candidate tree.
- [x] Historical frontends are isolated by the canonical `/workspace` runtime rather than used as the production entrypoint.

### Render services

The URBION HORIZON Render workspace currently contains four web services:

| Service | Role | Status |
|---|---|---|
| `urbion-master-61o` | canonical production target | **KEEP — RECONCILE BEFORE DEPLOY** |
| `urbion-horizon-workspace-v4` | legacy V4 surface | **LEGACY / DO NOT DEPLOY** |
| `urbion-workspace-v2-preview` | legacy V2 preview | **LEGACY / DO NOT DEPLOY** |
| `urbion-horizon-championship` | legacy championship surface | **LEGACY / DO NOT DEPLOY** |

No legacy service is a production release target. Cleanup is deferred until after release tag + live QA.

## 5. Render configuration blocker

Target service: `urbion-master-61o` (`srv-daclsgh5efls73et5mg0`)

### Required

- branch: approved release branch / promotion target
- start: `uvicorn landing_server:app --host 0.0.0.0 --port $PORT`
- health: `/health`
- build: `pip install -r requirements.txt`

### Observed at audit

- [ ] Branch is still `main` → **DRIFT**
- [ ] Start command is still `uvicorn championship_server:app --host 0.0.0.0 --port $PORT` → **DRIFT**
- [ ] Live deploy is still commit `795284b849188c1499a9f86530dee8564f60669f` → **NOT approved release SHA**
- [x] Auto deploy is off, so no background deployment is triggered by these documentation repairs

This is the only known operational release blocker after the code/test convergence audit. The available Render integration can inspect and deploy the service but does not expose a service-configuration update operation, so the branch/start-command reconciliation remains a controlled dashboard change before deployment.

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
- [x] Prove canonical browser/runtime behavior
- [x] Prove main parity at candidate tree
- [x] Audit Render workspace and detect service/config overlap
- [x] Reconcile release documents and create this single master checklist
- [ ] Fresh required CI on the final post-repair SHA
- [ ] Manually reconcile `urbion-master-61o` Render branch/start command
- [ ] Record final release SHA after the last code/documentation change
- [ ] Deploy the existing target service only
- [ ] Controlled live smoke across canonical public/workspace/decision/GIS/evidence routes
- [ ] Verify live commit equals final release SHA
- [ ] Record release identity/tag
- [ ] Only then remove/decommission legacy Render surfaces if explicitly authorized

## Release gate

`RENDER = LOCKED`

The application is not declared production-ready until the remaining operational configuration drift is reconciled and live smoke proves the final release SHA on the existing canonical Render service.
