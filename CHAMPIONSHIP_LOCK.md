# URBION HORIZON — CHAMPIONSHIP RELEASE LOCK

**Current posture:** `ENGINEERING P0 CONVERGENCE — RELEASE CANDIDATE`
**Canonical workspace:** `feature/championship-convergence-v1`
**Production Render:** `HOLD`

## What is locked

| Workstream | Status | Action |
|---|---|---|
| Core planning engines | GREEN | DO NOT REWRITE |
| GIS layer runtime | GREEN | DO NOT REWRITE |
| Evidence-state model | GREEN | PRESERVE |
| Statutory boundary | GREEN | PRESERVE `NOT_CLAIMED` |
| Canonical V5 workspace | GREEN / CANONICAL | PRESERVE |
| API convergence | GREEN BY CORE CONTRACTS | PRESERVE |
| What-If convergence | GREEN BY CORE CONTRACTS | PRESERVE |
| Frontend owner topology | GREEN BY BROWSER GATE | PRESERVE |
| P1 Judge UX | GREEN | PRESERVE |
| P2 Presentation Mode | GREEN | PRESERVE |
| P3 Decision Story | GREEN | PRESERVE |
| P4 Live Evidence Story | GREEN | PRESERVE |
| P5 KM/OSC Readiness | GREEN | PRESERVE |
| P6 Output lifecycle | GREEN | PRESERVE |
| Core CI convergence | GREEN | CONTINUE FINAL RELEASE AUDIT |
| Main content parity | ACHIEVED | VERIFY FINAL MAIN CI |
| Release identity | IN PROGRESS | LOCK AFTER FINAL MAIN GREEN |
| Live Render QA | NOT RUN | BLOCK RELEASE |
| Render deployment | HOLD | DO NOT DEPLOY |
| Cinematic demo/video | NOT STARTED | AFTER RELEASE GATE |

## Evidence boundary

Live source context does not automatically constitute statutory verification. The canonical evidence packet remains the sole evidence source, with statutory verification `NOT_CLAIMED` and decision authority `NONE` unless independently verified outside the system.

## Release rule

No Render deployment is considered the championship release until one canonical release SHA, one production entrypoint, one frontend architecture, and one evidence/decision contract are proven together by CI and live smoke.

## Explicit deployment boundary

The production deployment remains frozen until the final release gate is green and the user explicitly authorizes deployment with:

`DEPLOY RENDER NOW`
