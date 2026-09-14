# URBION HORIZON — CHAMPIONSHIP RELEASE LOCK

**Current posture:** `ENGINEERING P0 CONVERGED — RELEASE CANDIDATE / RENDER HOLD`
**Canonical release branch:** `feature/canonical-workspace-v2`
**Production Render:** `HOLD UNTIL FINAL EXACT-SHA QA`

## What is locked

| Workstream | Status | Action |
|---|---|---|
| Core planning engines | GREEN | DO NOT REWRITE |
| GIS layer runtime | REPAIRED / REVALIDATING | PRESERVE; certify real tile results |
| Evidence-state model | GREEN | PRESERVE |
| Statutory boundary | GREEN | PRESERVE `NOT_CLAIMED` |
| Canonical V5 workspace | GREEN / CANONICAL | PRESERVE |
| API convergence | GREEN BY CORE CONTRACTS | PRESERVE |
| What-If convergence | GREEN BY CORE CONTRACTS | PRESERVE |
| Frontend owner topology | GREEN BY BROWSER GATE | PRESERVE |
| P1 Judge UX | GREEN BY BROWSER GATE | PRESERVE |
| P2 Presentation Mode | GREEN BY CONTRACT | PRESERVE |
| P3 Decision Story | GREEN BY CONTRACT | PRESERVE |
| P4 Live Evidence Story | GREEN BY CONTRACT | PRESERVE |
| P5 KM/OSC Readiness | GREEN BY CONTRACT | PRESERVE |
| P6 Output lifecycle | GREEN BY CONTRACT | PRESERVE |
| Core CI convergence | GREEN on `ae91eabc`; rerun required after current GIS/docs hardening | RE-RUN |
| Release identity | RECONCILED to canonical branch | UPDATE ON FINAL SHA |
| Live Render QA | NOT CERTIFIED | BLOCK RELEASE |
| Render deployment | CURRENTLY LIVE ON INTERMEDIATE `ae91eabc` | REPLACE ONLY WITH FINAL EXACT SHA |
| Cinematic demo/video | NOT STARTED | AFTER RELEASE GATE |

## Evidence boundary

Live source context does not automatically constitute statutory verification. The canonical evidence packet remains the sole evidence source, with statutory verification `NOT_CLAIMED` and decision authority `NONE` unless independently verified outside the system.

## Release rule

No Render deployment is considered the championship release until one canonical release SHA, one production entrypoint, one frontend architecture, and one evidence/decision contract are proven together by fresh CI and live smoke.

## GIS truth rule

A GIS layer is not considered rendered merely because its Leaflet layer object was created. The UI may show `ON · RENDERED` only after an actual tile/image load event. Timeout and tile errors must remain visible as failure states for diagnosis and evidence review.

## Explicit deployment boundary

The production deployment remains frozen for final certification until the final release gate is green and the exact candidate SHA has been reviewed. Manual Render deployment is the final promotion step, not the validation mechanism.
