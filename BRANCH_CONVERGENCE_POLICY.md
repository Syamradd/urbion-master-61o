# URBION HORIZON — Branch Convergence Policy

Status: `ACTIVE — P0 CONVERGENCE`

## Canonical branch topology

| Role | Branch | Rule |
|---|---|---|
| Canonical baseline | `feature/canonical-workspace-v2` | Canonical engineering baseline; do not fork new competing workspaces from historical branches. |
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

## Frozen historical refs

The following legacy branches were audited against `feature/canonical-workspace-v2`, had no open PR, and had zero commits ahead of the canonical baseline. Their refs have been fast-forwarded to the canonical baseline as frozen pointers rather than deleted during P0:

- `feature/road-intelligence-v1`
- `feature/ux-v5-command-center`
- `feature/champion-command-center-consolidation`

The underlying historical commits remain reachable through repository history; these branch names are no longer valid development paths.

## Release convergence rule

The release candidate must converge to one SHA, one frontend architecture, one production entrypoint, and one evidence/decision contract. Historical branches must not be merged back into the release path unless a specific unique commit is first demonstrated to be missing from the canonical release.

## Deletion boundary

Branch deletion is intentionally deferred until P0 + P1 + live QA are complete. Preserve rollback/reference coverage during engineering convergence. After final release tagging, obsolete frozen refs may be deleted as a cleanup operation.
