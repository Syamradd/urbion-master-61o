# URBION HORIZON

**AI-Assisted Spatial & Planning Decision Intelligence**

URBION turns a development site into an explainable planning-screening workflow:

**SITE → SPATIAL → TYPOLOGY → POLICY → EVIDENCE → COMPLIANCE → DECISION → WHAT-IF**

## What it demonstrates
- Site and TOD spatial intelligence
- Development-class and typology-aware screening
- Verified RT MBMB 2035 rule retrieval for supported typologies
- Applicability and compliance evaluation
- Suitability scoring
- Decision confidence and recommendation
- Evidence-state transparency and decision trace
- Planning-value findings, blockers and next actions
- Deterministic showcase scenarios for judging
- Executable What-If scenario comparison and ranking

## API
- `GET /health`
- `GET /metadata`
- `GET /demo-scenarios`
- `GET /evidence-summary`
- `POST /assess`
- `POST /demo-scenarios/{scenario_id}`
- `POST /planning-value`
- `POST /what-if`

### What-If contract
`POST /what-if` accepts a `baseline` assessment payload and up to 12 `variants`. Each variant contains an `id`, optional `name`, and `overrides` object. URBION evaluates each variant independently through the same assessment engine, then returns status change, score delta, blockers, evidence gaps, ranked scenarios, best candidate and a decision pathway.

## Verified local policy coverage
MBMB / RT MBMB 2035 for the supported verified typologies. Other PBTs can be screened for spatial context, but their local statutory rule sets are not presented as loaded evidence.

## Evidence principle
URBION never converts discovery, planned or unavailable external sources into fake verified evidence. Missing evidence becomes an explicit planner action.

## Demo cases
`TOD-COMPLY` · `SHOP-COMPLY` · `SHOP-FAIL` · `OFFICE-REVIEW` · `NON-MBMB`

See `judge_demo.md` for the 90-second judging flow and `MASTER-69_FINAL_FREEZE.md` for the release checklist.

**Planning decision-support only — not statutory approval.**