# URBION HORIZON — Release Identity

Status: `RELEASE CANDIDATE — ENGINEERING P0 CONVERGENCE`

## Current canonical baseline

- Product: `URBION HORIZON`
- Canonical workspace: `feature/canonical-workspace-v2`
- Latest merged baseline: `ce3d86473953d4a55c4eabab2b9ef2992cd761e5`
- Active hardening branch: `feature/championship-convergence-v1`
- Last audited hardening HEAD: `5104942930352487400d8ce9fdd4981b7d69caac`
- Release SHA: `LOCK AFTER FRESH CI + MAIN PARITY`

## Engineering identity

- Engine contract: `PHASE-E.8`
- Evidence packet: `PHASE1.2`
- Canonical UI: `V5 Planning Workspace`
- Canonical runtime topology: `bridge → compatibility bootstrap → layer manager → canonical UI → specialist owners`
- Evidence states: `USER_PROVIDED`, `CALCULATED`, `SOURCE_CONTEXT`, `VERIFIED`, `UNVERIFIED`
- Statutory verification: `NOT_CLAIMED`
- Decision authority: `NONE`

## P0 convergence scope

- `URBION_ERROR_V1` canonical API/browser error envelope
- Decision Center failure visibility without silent fallback
- KPI evidence-state presentation
- Public What-If canonical evidence packets
- Bounded Copilot downstream convergence
- Agent/Copilot API convergence
- Planner Handoff consumes the canonical packet
- Decision OS/Judge Demo contract checks
- Frontend owner/lifecycle hardening
- Canonical mobility/station evidence reuse
- Road Intelligence attached to canonical evidence when a packet exists
- Rule-provenance amendment-state check
- P3 JPS station geometry adapter preserved
- P3 MyGEMS lithology adapter preserved
- MyEQMS/APIMS adapter preserved
- Branch capability preservation matrix
- Production manifest and release-document consistency

## Candidate gates

- Workspace Source: `REQUIRES FRESH CI ON FINAL HEAD`
- Rule Provenance: `REQUIRES FRESH CI ON FINAL HEAD`
- Road Intelligence: `REQUIRES FRESH CI ON FINAL HEAD`
- Workspace Browser: `REQUIRES FRESH CI ON FINAL HEAD`
- Preservation guard: `ADDED`
- P0 downstream/error/owner checks: `REQUIRES FRESH CI ON FINAL HEAD`
- Full regression: `REQUIRES FRESH CI ON FINAL HEAD`

## Deployment gates

- Production Render: `HOLD`
- Production branch parity: `NOT YET PROVEN`
- Live production smoke: `NOT RUN`
- Deployment readiness: `FALSE` until final CI + parity + live smoke

## Render boundary

Do not treat any existing Render deployment as the current championship release until its deployed commit matches the approved release SHA and passes live smoke.

Existing production service configuration is tracked separately from this release identity and must be reconciled before deployment.
