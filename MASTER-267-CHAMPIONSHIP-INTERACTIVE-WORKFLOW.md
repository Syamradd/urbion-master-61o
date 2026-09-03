# MASTER-267 — Championship Interactive Planning Workflow

Built as one coherent product batch over MASTER-266.

## Visible upgrade
- Planner Action Board
- Site / spatial / environment / policy / impact / evidence surfaces
- What-If decision lens
- Decision Centre / Judge Mode / presentation shortcuts
- LCP handoff messaging and decision-boundary disclosure

## Architecture
The upgrade is a presentation layer over the existing URBION endpoints. It does not replace the existing assessment, evidence, What-If, Decision Centre, Judge Mode or LCP engines.

## Guardrails
- Planning decision-support only; not statutory approval.
- Evidence states remain explicit.
- Source availability is not treated as statutory verification.
- Existing MASTER-266 APIs remain the source of truth.
