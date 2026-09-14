# URBION HORIZON — Branch Convergence Policy

Status: `ACTIVE — FINAL RELEASE CONVERGENCE`

## Canonical branch topology

| Role | Branch | Rule |
|---|---|---|
| Release candidate | `feature/championship-convergence-v1` | Sole active P0/P1 engineering and release-hardening branch until explicit release/merge authorization. |
| Production release | `main` | Must be aligned to the exact approved release SHA before production deployment. |
| Historical baseline | `feature/canonical-workspace-v2` | Frozen historical/reference branch; not an active implementation path. |

The old canonical-workspace branch is retained for rollback/reference only. New feature or bug-fix work must not fork from or target it during final convergence.

## Historical branch policy

Existing feature and `codex/*` branches are historical references unless explicitly promoted into the active topology. Their existence does not make them active implementation paths.

A historical branch may be deleted only after all of the following are proven:

1. Its required work is represented in the release candidate or production release.
2. It has no unique release-critical commits remaining.
3. No open PR or deployment depends on it.
4. A final release tag/checkpoint provides a rollback reference.

## Release convergence rule

The release candidate must converge to one SHA, one frontend architecture, one production entrypoint, and one evidence/decision contract. Historical branches must not be merged back into the release path unless a specific unique commit is first demonstrated to be missing from the release candidate.

## Render topology rule

Only the existing `urbion-master-61o` Render service is a production release target. Legacy Render services are reference/preview surfaces and must not become alternate production paths.

The production service must use:
- branch: `feature/championship-convergence-v1` until release is promoted/aligned to `main`;
- start command: `uvicorn landing_server:app --host 0.0.0.0 --port $PORT`;
- health check: `/health`.

No deployment is permitted while the service configuration disagrees with the release boundary.

## Deletion boundary

Branch and Render-service cleanup is intentionally deferred until P0 + P1 + live QA are complete and a release tag/rollback checkpoint exists.
