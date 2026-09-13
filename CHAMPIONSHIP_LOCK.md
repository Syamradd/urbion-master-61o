# URBION HORIZON — CHAMPIONSHIP RELEASE LOCK

**Current posture:** `ENGINEERING P0 CONVERGENCE — NOT RELEASE LOCKED`
**Canonical workspace:** `feature/canonical-workspace-v2`
**Hardening branch:** `feature/championship-convergence-v1`
**Production Render:** `HOLD`

## What is locked

| Workstream | Status | Action |
|---|---|---|
| Core planning engines | GREEN | DO NOT REWRITE |
| GIS layer runtime | GREEN | DO NOT REWRITE |
| Evidence-state model | GREEN | PRESERVE |
| Statutory boundary | GREEN | PRESERVE `NOT_CLAIMED` |
| Canonical V5 workspace | CANONICAL | CONVERGE / HARDEN |
| API convergence | IN PROGRESS | REPAIR |
| What-If convergence | IN PROGRESS | REPAIR |
| Frontend owner topology | IN PROGRESS | AUDIT |
| Release identity | IN PROGRESS | RECONCILE |
| Production parity | NOT ALIGNED | BLOCK RELEASE |
| Render deployment | HOLD | DO NOT DEPLOY |
| Live Render QA | NOT RUN | BLOCK RELEASE |
| Cinematic demo/video | NOT STARTED | AFTER RELEASE GATE |

## Release rule

No Render deployment is considered the championship release until one canonical SHA, one production entrypoint, one frontend architecture, and one evidence/decision contract are proven together by CI and live smoke.

## Explicit deployment boundary

The production deployment remains frozen until the final release gate is green and the user explicitly authorizes deployment with:

`DEPLOY RENDER NOW`
