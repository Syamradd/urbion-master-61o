# MASTER-279 — Championship Reliability Bridge

## Scope
- Keep MASTER-278 unified dashboard as the primary workspace.
- Add a post-load reliability bridge without replacing existing dashboard contracts.
- Repair the Championship Gate button rendering path.
- Harden live i-PLAN layer toggles with loading/error states.
- Harden What-If A/B controls against the existing `/what-if` contract.
- Align championship polish, focus, hover and print rules with the `v276-*` primary workspace classes.
- Add a compact live-source/provenance rail.

## Guardrails
- No statutory approval is inferred.
- i-PLAN/DPFDN outputs remain source context and require authoritative verification.
- One atomic commit; Render is not changed by this commit.
