# URBION HORIZON — Release Identity

Status: `RELEASE CANDIDATE — P0 ENGINEERING CONVERGED / RENDER HOLD`

## Current release candidate

- Product: `URBION HORIZON`
- Active release branch: `feature/championship-convergence-v1`
- Audited candidate HEAD: `c4555f505c9ef1c41d677eee85cff35d1a7e5a5d`
- Main parity: `PROVEN` (`behind_by=0` at audit time)
- PR #131: `OPEN / MERGEABLE` — do not merge without explicit release authorization
- Release SHA: lock only after the final documentation commit and its fresh gates

## Engineering identity

- Engine contract: `PHASE-E.8`
- Evidence packet: `PHASE1.2`
- Canonical UI: `V5 Planning Workspace`
- Canonical production entrypoint: `landing_server:app`
- Canonical route: `/workspace`
- Canonical runtime topology: `bridge → compatibility bootstrap → layer manager → canonical UI → specialist owners`
- Error contract: `URBION_ERROR_V1`
- Evidence states: `USER_PROVIDED`, `CALCULATED`, `SOURCE_CONTEXT`, `VERIFIED`, `UNVERIFIED`
- Statutory verification: `NOT_CLAIMED`
- Decision authority: `NONE`

## Verified P0 gates at audited candidate tree

- Regression matrix: `PASS` — 17 regression lanes
- Runtime smoke: `PASS`
- Full regression: `PASS`
- Workspace Browser Gate: `PASS`
- Render Parity Gate: `PASS`
- UX Contract: `PASS`
- Final Command Centre Contract: `PASS`
- Rule-provenance, Road Intelligence, browser evidence upload, GIS 25-layer, MyEQMS station and downstream P0 checks: `PASS`
- Workspace Source Gate: `PASS` on the identical tested tree before the parity-only merge; source tree unchanged by the parity merge

## Render operational reconciliation — PRE-DEPLOY BLOCKERS

Target Render workspace: `URBION HORIZON`

Target service:
- Name: `urbion-master-61o`
- Service ID: `srv-daclsgh5efls73et5mg0`
- Expected region: `oregon`
- Expected runtime: `python`
- Expected build: `pip install -r requirements.txt`
- Expected start: `uvicorn landing_server:app --host 0.0.0.0 --port $PORT`
- Expected health: `/health`

Observed target service configuration at audit time:
- Branch: `main` — `MISMATCH`
- Start command: `uvicorn championship_server:app --host 0.0.0.0 --port $PORT` — `MISMATCH`
- Latest live deploy commit: `795284b849188c1499a9f86530dee8564f60669f` — `NOT APPROVED RELEASE SHA`
- Auto deploy: `off`

Operational rule: **DO NOT DEPLOY** until the existing target service is manually reconciled to the approved release branch/entrypoint and the resulting live deployment matches the final release SHA.

## Existing Render overlap / legacy surfaces

The `URBION HORIZON` Render workspace currently contains three legacy web services in addition to the canonical target:

- `urbion-horizon-workspace-v4` — `srv-dahm749594qs73fk2tag` — `feature/canonical-workspace-v2` — `workspace_v4_server:app`
- `urbion-workspace-v2-preview` — `srv-dahlenbm8hqs73ca6u2g` — `feature/canonical-workspace-v2` — `workspace_v2_server:app`
- `urbion-horizon-championship` — `srv-daes2f6q1p3s73algrmg` — `feature/champion-command-center-consolidation` — `championship_server:app`

These are **historical/legacy surfaces, not release targets**. Do not route the championship release through them and do not delete/suspend them during P0 without explicit authorization. Cleanup is a post-release operation.

## Architecture overlap clarification

`landing_server.py` intentionally imports the shared FastAPI application from `championship_server.py` and adds the canonical public presentation routes/middleware. `championship_server.py` is therefore a shared application base, not a second planning engine. The production deployment boundary remains `landing_server:app`.

## Deployment gates

- Production Render: `HOLD`
- Production branch parity: `BLOCKED BY SERVICE CONFIG DRIFT`
- Live production smoke: `NOT RUN`
- Deployment readiness: `FALSE`

## Final release condition

The release is ready for Render only after one final release SHA is locked, that SHA has fresh required CI, the target `urbion-master-61o` service is reconciled to the canonical branch and `landing_server:app`, and controlled live smoke proves `/health`, `/`, `/workspace`, `/assess`, `/what-if`, `/decision-center`, `/copilot/run`, GIS/layer runtime and evidence behavior.
