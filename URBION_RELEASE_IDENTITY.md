# URBION HORIZON — Release Identity

Status: `RELEASE CANDIDATE — ENGINEERING P0 CONVERGENCE`

## Current canonical baseline

- Product: `URBION HORIZON`
- Canonical workspace: `feature/canonical-workspace-v2`
- Latest merged baseline: `ce3d86473953d4a55c4eabab2b9ef2992cd761e5`
- Current hardening branch: `feature/championship-convergence-v1`
- Current hardening HEAD: `75e58725dbfa444bcf6579629f44d6502e7f1ebb`
- Current hardening PR: `#131`

## Engineering identity

- Engine contract: `PHASE-E.8`
- Evidence packet: `PHASE1.2`
- Canonical UI: `V5 Planning Workspace`
- Evidence states: `USER_PROVIDED`, `CALCULATED`, `SOURCE_CONTEXT`, `VERIFIED`, `UNVERIFIED`
- Statutory verification: `NOT_CLAIMED`
- Decision authority: `NONE`

## P0 convergence scope

- `URBION_ERROR_V1` canonical API/browser error envelope
- Decision Center failure visibility without silent fallback
- KPI evidence-state presentation
- Public What-If route convergence onto canonical evidence packets
- Bounded Copilot downstream convergence into the canonical packet
- Agent/Copilot API failure-contract convergence
- Frontend owner/lifecycle hardening
- Production manifest and release-document consistency

## Current hardening gates

- Workspace Source: `GREEN` on prior canonical baseline
- Rule Provenance: `GREEN` on prior canonical baseline
- Road Intelligence: `GREEN` on prior canonical baseline
- Workspace Browser: `GREEN` on prior canonical baseline
- New convergence/owner contract checks: `PENDING` until CI completes on HEAD `75e58725dbfa444bcf6579629f44d6502e7f1ebb`

## Deployment gates

- Production Render: `HOLD`
- Production branch parity: `NOT YET PROVEN`
- Live production smoke: `NOT RUN`
- Deployment readiness: `FALSE` until final convergence + parity + live smoke

## Render boundary

Do not treat any existing Render deployment as the current championship release until its deployed commit matches this approved canonical release identity and passes live smoke.

Existing production service configuration is tracked separately from this release identity and must be reconciled before deployment.
