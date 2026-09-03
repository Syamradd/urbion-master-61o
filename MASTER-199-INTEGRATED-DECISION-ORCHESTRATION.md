# MASTER-199 — Integrated Decision Orchestration

## Capability
The integrated LCP endpoint now exposes the existing decision-center surface and can optionally execute the existing What-If engine from the same assessment input.

## Trace
SITE → SPATIAL → STATION → IMPACT → POLICY/SDG → RECOMMENDATION → WHAT-IF → DECISION CENTER → LCP/PLANNER REVIEW

## Contract
- What-If remains optional; no scenario input means no fabricated scenario result.
- Scenario variants are capped at 12 and inherit the baseline assessment input before explicit overrides.
- Decision Center is composed from the same deterministic assessment and does not alter statutory outcomes.
- Scenario ranking is decision support only.
- Evidence gaps and statutory boundaries remain disclosed.

## Acceptance
Regression coverage verifies baseline LCP behaviour, integrated What-If output, invalid scenario input handling and the `NOT_CLAIMED` statutory boundary.
