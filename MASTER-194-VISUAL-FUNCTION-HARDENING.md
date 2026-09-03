# MASTER-194 — VISUAL + FUNCTION HARDENING

## Objective
Turn the championship loop into a judge-safe, deployment-safe interface: every major surface must be reachable, use the same-origin API, expose evidence boundaries, and avoid unsafe remote-value rendering.

## Judge-facing surfaces
- Dashboard
- Site Assessment
- Map Studio
- Evidence / provenance
- What-If
- Decision Center
- LCP Intelligence
- Planner Review
- KM/OSC

## UI hardening rules
1. Navigation must use stable local routes.
2. API calls must resolve from `location.origin` rather than a stale deployment host.
3. Remote strings must be escaped before insertion into HTML.
4. Loading, error and unavailable-source states must remain visible.
5. Spatial placeholders and malformed coordinates must be rejected.
6. Theme/language controls must not break the core decision path.
7. Statutory approval language must remain explicitly bounded.

## Functional hardening
The release must preserve the chain:
SITE → SPATIAL → STATION → IMPACT → POLICY/SDG → RECOMMENDATION → WHAT-IF → DECISION → PLANNER REVIEW → KM/OSC.

MASTER-194 is complete only when its regression contract passes and the resulting GitHub Actions release run is GREEN.
