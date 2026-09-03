# MASTER-191 — Deployment Smoke & Route Integrity

## Smoke targets
- `/health` reports PHASE-E.7 and frontend serving
- `/metadata`, `/sources`, `/map/layers` are reachable
- core judge surfaces are present
- `/lcp/intelligence` is registered
- no missing LCP frontend surface

## Boundary
Smoke tests verify deployment wiring and route integrity only; they do not convert live-source context into statutory verification.
