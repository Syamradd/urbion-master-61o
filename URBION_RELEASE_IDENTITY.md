# URBION HORIZON — Release Identity

Status: `RELEASE CANDIDATE — ENGINEERING P0 CONVERGENCE`

## Current canonical baseline

- Product: `URBION HORIZON`
- Canonical workspace: `feature/canonical-workspace-v2`
- Latest merged baseline: `ce3d86473953d4a55c4eabab2b9ef2992cd761e5`
- Current hardening branch: `feature/championship-convergence-v1`
- Current hardening HEAD: `ebc0cc3da168656b852857d30dbe7d63c1446434`
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
- Production manifest and release-document consistency

## Release gates

- Pre-convergence CI on merged baseline: `GREEN` — Workspace Source, Browser, Rule Provenance, Road Intelligence
- Current hardening CI: `PENDING` for latest HEAD
- Production Render: `HOLD`
- Production branch alignment: `NOT YET ALIGNED`
- Live production smoke: `NOT RUN`
- Deployment readiness: `FALSE` until final convergence + parity + live smoke

## Render boundary

Do not treat any existing Render deployment as the current championship release until its deployed commit matches this approved canonical release identity and passes live smoke.

Existing production service configuration is tracked separately from this release identity and must be reconciled before deployment.
