# URBION HORIZON

**AI-Assisted Spatial & Planning Decision Intelligence**

URBION turns a development site into an explainable planning-screening workflow:

**SITE → SPATIAL → TYPOLOGY → POLICY → EVIDENCE → COMPLIANCE → KM/OSC → DECISION → WHAT-IF**

## What it demonstrates
- Site and TOD spatial intelligence
- Development-class and typology-aware screening
- Verified RT MBMB 2035 rule retrieval for supported typologies
- Applicability and compliance evaluation
- Suitability scoring
- Decision confidence and recommendation
- Evidence-state transparency and decision trace
- Planning-value findings, blockers and next actions
- i-Plan point context and official committed-land-use WMS visualisation
- Elysian project-reference reconciliation against official context
- KM/OSC workflow-readiness support
- Deterministic showcase scenarios for judging
- Executable What-If scenario comparison and ranking

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

### KM / OSC readiness contract
`POST /km/readiness` accepts the PBT, development type, submitted core documents, KM category and technical-review states. It returns category state, missing core evidence, technical-review status, blockers and `READY_FOR_WORKFLOW_REVIEW` or `REQUIRES_REVIEW`. It does **not** grant or predict statutory approval.

### What-If contract
`POST /what-if` accepts a `baseline` assessment payload and up to 12 `variants`. Each variant contains an `id`, optional `name`, and `overrides` object. URBION evaluates each variant independently through the same assessment engine, then returns status change, score delta, blockers, evidence gaps, ranked scenarios, best candidate and a decision pathway.

## Verified local policy coverage
MBMB / RT MBMB 2035 for the supported verified typologies. Other PBTs can be screened for spatial context, but their local statutory rule sets are not presented as loaded evidence.

## Evidence principle
URBION separates `USER_PROVIDED`, `CALCULATED`, `SOURCE_CONTEXT`, `VERIFIED` and `UNVERIFIED` evidence states. Discovery, planned or unavailable external sources are never promoted to fake verified evidence. External GIS availability is disclosed separately from statutory verification.

## Demo cases
`TOD-COMPLY` · `SHOP-COMPLY` · `SHOP-FAIL` · `OFFICE-REVIEW` · `NON-MBMB`

See `judge_demo.md` for the 90-second judging flow and `MASTER-69_FINAL_FREEZE.md` for the release checklist.

**Planning decision-support only — not statutory approval.**