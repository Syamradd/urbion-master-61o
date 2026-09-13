# URBION HORIZON — Branch Convergence Policy

Status: `ACTIVE — P0 CONVERGENCE`

## Canonical branch topology

| Role | Branch | Rule |
|---|---|---|
| Canonical baseline | `feature/canonical-workspace-v2` | Protected development baseline; do not fork new competing workspaces from historical branches. |
| Active hardening / release candidate | `feature/championship-convergence-v1` | Only active P0/P1 engineering branch until final release SHA is locked. |
| Production release | `main` | Must be aligned to the exact approved release SHA before production deployment. |

## Historical branch policy

Existing feature and `codex/*` branches are treated as historical references unless explicitly promoted into the active topology. Their existence does not make them active implementation paths.

Do not add new features, bug fixes, deployment changes, or competing UI/runtime work to historical branches during the championship convergence phase.

A historical branch may be deleted only after all of the following are proven:

1. Its required work is already represented in the canonical baseline or active hardening branch.
2. It has no unique release-critical commits remaining.
3. No open PR or deployment depends on it.
4. A final release tag/checkpoint provides a rollback reference.

## Verified historical relationships

- `feature/road-intelligence-v1` is behind `feature/canonical-workspace-v2` by one commit with no commits ahead of the canonical baseline; its Road Intelligence work is already represented in the canonical merge baseline.
- `feature/ux-v5-command-center` is behind the canonical baseline with no commits ahead; it is historical and not an active implementation path.
- `feature/champion-command-center-consolidation` is behind the canonical baseline with no commits ahead; it is historical and not an active implementation path.

## Release convergence rule

The release candidate must converge to one SHA, one frontend architecture, one production entrypoint, and one evidence/decision contract. Historical branches must not be merged back into the release path unless a specific unique commit is first demonstrated to be missing from the canonical release.

## Deletion boundary

Branch deletion is intentionally deferred until P0 + P1 + live QA are complete. Preserve historical branches as rollback/reference points during engineering convergence.
