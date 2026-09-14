# URBION HORIZON — Release Identity

Status: `RELEASE CANDIDATE — P0 ENGINEERING CONVERGED / RENDER HOLD`

## Current release candidate

- Product: `URBION HORIZON`
- Active release branch: `feature/championship-convergence-v1`
- Render target: `urbion-horizon-workspace-v4`
- Render service ID: `srv-dahm749594qs73fk2tag`
- Previous audited candidate HEAD: `c4555f505c9ef1c41d677eee85cff35d1a7e5a5d`
- Release SHA: lock only after this Render-target repair patch and its fresh gates

## Engineering identity

- Engine contract: `PHASE-E.8`
- Evidence packet: `PHASE1.2`
- Canonical UI: `V5 Planning Workspace`
- Canonical application entrypoint: `landing_server:app`
- Existing Render launcher: `workspace_v4_server:app`
- Launcher invariant: `workspace_v4_server:app -> landing_server:app`
- Canonical route: `/workspace`
- Public root: `/` → canonical Welcome
- About route: `/about` → canonical About Us
- Canonical runtime topology: `bridge → compatibility bootstrap → layer manager → canonical UI → specialist owners`
- Error contract: `URBION_ERROR_V1`
- Evidence states: `USER_PROVIDED`, `CALCULATED`, `SOURCE_CONTEXT`, `VERIFIED`, `UNVERIFIED`
- Statutory verification: `NOT_CLAIMED`
- Decision authority: `NONE`

## Verified P0 gates at previous audited tree

- Regression matrix: `PASS` — 17 regression lanes
- Runtime smoke: `PASS`
- Full regression: `PASS`
- Workspace Browser Gate: `PASS`
- Render Parity Gate: `PASS`
- UX Contract: `PASS`
- Final Command Centre Contract: `PASS`
- Rule-provenance, Road Intelligence, browser evidence upload, GIS 25-layer, MyEQMS station and downstream P0 checks: `PASS`
- Main parity: `PROVEN` (`behind_by=0` at audited tree)

## Selected Render target — pre-deploy reconciliation

Target workspace: `URBION HORIZON`
Target service: `urbion-horizon-workspace-v4`
Service ID: `srv-dahm749594qs73fk2tag`

Observed existing configuration:
- Branch: `feature/canonical-workspace-v2`
- Start: `uvicorn workspace_v4_server:app --host 0.0.0.0 --port $PORT`
- Build: `pip install -r requirements.txt`
- Region: `singapore`
- Plan: `free`
- Auto deploy: `off`

Required release configuration:
- Branch: `feature/championship-convergence-v1`
- Keep existing start command; its module is now a compatibility shim to the canonical `landing_server:app`
- Build remains `pip install -r requirements.txt`
- Health endpoint: `/health`

The branch reconciliation must be done in Render before deployment. No deploy is triggered by this repository repair because auto deploy is off.

## Existing Render overlap

The same Render workspace also contains:
- `urbion-master-61o` — historical surface
- `urbion-workspace-v2-preview` — historical preview
- `urbion-horizon-championship` — historical championship surface

These services remain untouched. The selected V4 service is the only intended deployment target for this release.

## Architecture overlap clarification

`workspace_v4_server.py` no longer owns a FastAPI app, frontend routes, or planning logic. It only imports/re-exports the canonical application from `landing_server.py`. This preserves the existing Render service launcher while removing a competing runtime implementation.

`landing_server.py` imports the shared application base from `championship_server.py` and adds the canonical public presentation routes, middleware, and workspace composition. `championship_server.py` is a shared application base, not a second planning engine.

## Deployment gates

- Production Render: `HOLD`
- Branch reconciliation: `REQUIRED`
- Fresh final-head CI: `REQUIRED`
- Live production smoke: `NOT RUN`
- Deployment readiness: `FALSE`

## Final release condition

The release is eligible for deployment only after the selected existing `urbion-horizon-workspace-v4` service is reconciled to `feature/championship-convergence-v1`, fresh required gates pass on the final release SHA, and controlled live smoke proves Welcome, About, Workspace, health, assessment, What-If, Decision Center, Copilot, GIS/layer and evidence behavior on that exact SHA.
