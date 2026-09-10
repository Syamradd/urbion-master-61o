# URBION HORIZON — CHAMPIONSHIP LOCK

**Lock baseline:** `main`
**Locked commit baseline:** `9b9b0be8308c4c4bd720747862927299bc80079a`
**Previous baseline:** `baf22725d32b236953163500fc3ff744a6ea276b`

## Locked workstreams

| Workstream | Status | Action |
|---|---|---|
| Core planning engines | GREEN | LOCK |
| Regression lanes | GREEN | LOCK |
| Runtime smoke | GREEN | LOCK |
| Responsive QA | GREEN | LOCK |
| UX Contract | GREEN | LOCK |
| Landing / welcoming page | GREEN | KEEP |
| Dashboard visual system | GREEN | KEEP |
| Theme BM/EN | GREEN | LOCK |
| Layer drawer | GREEN | LOCK after verified browser gate |
| Browser QA | GREEN | LOCK |
| Cross-browser QA | GREEN | LOCK |
| Final integrity / release audit | GREEN | LOCK |
| Render deployment | LIVE | LOCK |
| Live Render QA | VERIFIED at deployment gate | LOCK |
| Cinematic smart-city artwork | SKIPPED | DO NOT BLOCK |

## Verification baseline

- Championship Full CI: PASS
- Runtime Smoke: PASS
- Browser QA: PASS
- Full Regression: PASS
- UX Contract: PASS
- Responsive Visual QA: PASS
- Render deployment for locked baseline: LIVE

## Freeze rule

No application-logic, planning-engine, UI-behaviour, or visual-system changes should be made after this lock unless a newly observed release-blocking failure is reproduced and documented.

Documentation and submission-material changes may proceed independently, provided they do not alter the locked application baseline.
