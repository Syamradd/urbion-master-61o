# MASTER-188 — Integrated LCP Intelligence

## Objective
Unify URBION's deterministic planning chain into one LCP-ready evidence package.

## End-to-end chain
SITE → SPATIAL → STATION → IMPACT → ISSUE → POLICY/SDG → RECOMMENDATION → LCP/PLANNER REVIEW

## Integrated surfaces
- Existing site assessment and compliance context
- Multi-source spatial screening
- Live station observation context when supplied or explicitly requested
- Physical, social and economic development impact screening
- Impact → policy / national / SDG trace graph
- Evidence-backed planning recommendations
- KM/OSC workflow readiness when checklist inputs are supplied
- Consolidated review gaps and evidence counts

## Safety / evidence boundary
- Missing data stays `UNVERIFIED` or `REVIEW_REQUIRED`.
- Source context is never silently upgraded to `VERIFIED`.
- Calculations remain traceable to explicit inputs.
- Recommendations remain planner-review outputs.
- URBION does not grant, predict or imply statutory approval.

## API
`POST /lcp/intelligence`

The endpoint accepts the normal `/assess` input under `assessment`, plus optional `development_inputs`, `spatial_inputs`, policy/national/SDG links, station snapshot, and KM inputs. `live_stations=true` explicitly requests the live station adapter.

## Release gate
MASTER-188 is only GREEN after the dedicated LCP lane and full regression suite complete successfully in GitHub Actions.
