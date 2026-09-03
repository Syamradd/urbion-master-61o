# MASTER-133 — Autonomous Runbook

## Purpose
Keep the URBION release pipeline moving without requiring a conversational approval checkpoint.

## Execution order
1. Inspect the latest `main` release identity.
2. Identify the highest-value incomplete product or regression contract.
3. Make one focused additive change.
4. Add or update a deterministic regression contract.
5. Commit the implementation and test together where practical.
6. Wait for CI and treat a failed check as a blocker to the next release.
7. Continue only from the green head.

## Priority
- Release/deployment identity integrity
- Judge-facing decision workflow
- GIS evidence safety and spatial provenance
- Bilingual UI and theme controls
- Map controls and evidence presentation
- Planning/KM workflow boundaries
- Documentation and demo readiness

## Safety boundary
URBION may calculate, compare, disclose evidence state, and prepare workflow readiness. It must not present an automated result as statutory approval, gazetted-plan verification, or applicant-specific OSC approval without authoritative evidence.

## Release rule
A release is not considered complete merely because code exists. It needs a deterministic regression contract and a green CI result on the resulting `main` head.
