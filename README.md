# URBION HORIZON

**AI-Assisted Spatial & Planning Decision Intelligence**

URBION turns a development site into an explainable planning-screening workflow:

**SITE → SPATIAL → TYPOLOGY → POLICY → EVIDENCE → COMPLIANCE → KM/OSC → DECISION → WHAT-IF**

## Judge workflow

**Assess → Map → Evidence → What-If → Decide → Planner Review → KM/OSC**

A capability is considered championship-ready only when a judge can discover it, interact with it, understand the result, inspect evidence/provenance, and continue to the next planning action.

## Core workflow
1. **SITE** — location, PBT, district and parcel inputs.
2. **SPATIAL** — TOD distance, spatial bands and map-source context.
3. **TYPOLOGY** — development class/type determines which planning controls are relevant.
4. **POLICY** — planning-rule evidence is surfaced for supported typologies.
5. **EVIDENCE** — important inputs are labelled by evidence state rather than assumed authoritative.
6. **COMPLIANCE** — applicable controls are evaluated against proposal inputs.
7. **KM/OSC** — submission readiness, missing evidence and technical-review blockers are surfaced.
8. **DECISION** — recommendation, confidence, planning value and trace are returned.
9. **WHAT-IF** — alternative proposal variants are independently assessed and ranked.
10. **PLANNER REVIEW** — evidence gaps, recommendation grounding and next review actions are consolidated.

## API

### Core
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

### Championship integration
- `POST /lcp/intelligence`
- `POST /lcp/release-packet`
- `GET /championship-gate`
- `GET /stations/nearby`
- `GET /station-intelligence`
- `POST /environment/intelligence`
- `GET /gemini/status`
- `POST /gemini/red-team`
- `POST /gemini/red-team-assessment`

## Evidence model

URBION uses five explicit evidence states:

`USER_PROVIDED` · `CALCULATED` · `SOURCE_CONTEXT` · `VERIFIED` · `UNVERIFIED`

Live/public GIS availability is treated as **source context** unless verification evidence supports a stronger state. Missing evidence becomes an explicit review gap instead of fabricated certainty.

## Scenario boundary

`POST /what-if` and `/lcp/intelligence` accept up to 12 scenario variants. Each variant is independently evaluated through the same assessment engine before ranking. Scenario ranking is decision support only.

## Data-source boundary

The platform separates official public GIS/map services, public portals, project-reference data and planning-rule evidence. i-Plan point queries and official WMS layers provide spatial source context; statutory currency and applicability must still be verified against the authoritative plan/PBT workflow.

## Demo cases
`TOD-COMPLY` · `SHOP-COMPLY` · `SHOP-FAIL` · `OFFICE-REVIEW` · `NON-MBMB`

## Safety boundary

Planning decision support only — not statutory approval. Automated results do not constitute gazetted-plan verification, authority decisions, or applicant-specific OSC approval. Planner/PBT and authorised-agency verification remains required.
