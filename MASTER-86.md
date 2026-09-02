# MASTER-86 — Phase D Contract Lock

Phase D moves URBION from static decision output into executable scenario intelligence.

## Contract
- Baseline is assessed through the same core engine used by `/assess`.
- Each What-If variant is isolated from the baseline and applies only explicit field overrides.
- A maximum of 12 variants is accepted per request.
- Every scenario returns decision status, status change, score delta, suitability band, blockers and evidence gaps.
- Scenarios are ranked by decision outcome, blocker state, evidence burden and suitability score.
- The result includes a best candidate and an explainable decision pathway.

## Guardrails
- What-If output is decision support only.
- Scenario changes do not mutate the baseline request.
- Non-MBMB scenarios remain evidence-gated when local statutory rules are not loaded.
- The engine does not invent planning controls or represent scenario ranking as statutory approval.

## Next
Frontend integration will expose the What-If layer as a judge-facing scenario workspace without changing the underlying decision engine.
