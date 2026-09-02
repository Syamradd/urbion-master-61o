# URBION HORIZON

**AI-Assisted Spatial & Planning Decision Intelligence**

URBION turns a development site into an explainable planning-screening workflow:

**SITE → SPATIAL → TYPOLOGY → POLICY → EVIDENCE → COMPLIANCE → KM/OSC → DECISION → WHAT-IF**

## Core workflow
1. **SITE** — location, PBT, district and parcel inputs.
2. **SPATIAL** — TOD distance, spatial bands and map-source context.
3. **TYPOLOGY** — development class/type determines which planning controls are relevant.
4. **POLICY** — verified RT MBMB 2035 rules are retrieved for supported typologies.
5. **EVIDENCE** — every important input is labelled by evidence state rather than assumed authoritative.
6. **COMPLIANCE** — applicable controls are evaluated against proposal inputs.
7. **KM/OSC** — submission readiness, missing evidence and technical-review blockers are surfaced.
8. **DECISION** — recommendation, confidence, planning value and trace are returned.
9. **WHAT-IF** — alternative proposal variants are independently assessed and ranked.

## API
- `GET /health`
- `GET /metadata`
- `GET /evidence-summary`
- `GET /sources`
- `GET /map/layers`
- `GET /iplan/context`
- `GET /elysian/reconcile`
- `POST /assess`
- `POST /km/readiness`
- `GET /demo-scenarios`
- `POST /demo-scenarios/{scenario_id}`
- `POST /planning-value`
- `POST /what-if`
- `POST /decision-center`
- `GET /judge-mode`

### KM / OSC readiness
`POST /km/readiness` accepts the PBT, development type, submitted core documents, KM category and technical-review states. It returns category state, missing core evidence, technical-review status, blockers and `READY_FOR_WORKFLOW_REVIEW` or `REQUIRES_REVIEW`.

**Boundary:** KM/OSC readiness support is not statutory approval and does not predict approval outcomes.

### What-If
`POST /what-if` accepts a `baseline` assessment payload and up to 12 variants. Each variant contains an `id`, optional `name`, and `overrides` object. Every variant is evaluated through the same assessment engine before ranking.

## Evidence model
URBION uses five explicit evidence states:

`USER_PROVIDED` · `CALCULATED` · `SOURCE_CONTEXT` · `VERIFIED` · `UNVERIFIED`

Live/public GIS availability is treated as **source context** unless verification evidence supports a stronger state. Missing evidence becomes an explicit review gap instead of fabricated certainty.

## Data-source boundary
The platform separates official public GIS/map services, public portals, project-reference data and planning-rule evidence. i-Plan point queries and official WMS layers provide spatial source context; statutory currency and applicability must still be verified against the authoritative plan/PBT workflow.

## Demo cases
`TOD-COMPLY` · `SHOP-COMPLY` · `SHOP-FAIL` · `OFFICE-REVIEW` · `NON-MBMB`

See `judge_demo.md` for the 90-second judging flow and `MASTER-69_FINAL_FREEZE.md` for the release checklist.

**Planning decision-support only — not statutory approval.**