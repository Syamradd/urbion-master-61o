# URBION HORIZON — Branch Convergence Policy

Status: `ACTIVE — FINAL RELEASE CONVERGENCE`

## Canonical branch topology

| Role | Branch | Rule |
|---|---|---|
| Release candidate | `feature/canonical-workspace-v2` | Sole active P0/P1 engineering and release-hardening branch until explicit release/merge authorization. |
| Production release | `main` | May be aligned to the exact approved release SHA when the release is accepted; it is not the current Render control branch. |
| Historical references | all other feature / codex / repair branches | Frozen reference/rollback material unless explicitly promoted with a documented unique capability. |

`feature/canonical-workspace-v2` is the sole active implementation and release path. New feature or bug-fix work must not target historical branches during final convergence.

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

Only the existing `urbion-horizon-workspace-v4` Render service (`srv-dahm749594qs73fk2tag`) is the current production release target. Legacy Render services are reference/preview surfaces and must not become alternate production paths.

The production service must use:
- branch: `feature/canonical-workspace-v2`;
- start command: `uvicorn workspace_v4_server:app --host 0.0.0.0 --port $PORT`;
- canonical application entrypoint behind the launcher: `landing_server:app`;
- health endpoint: `/health`.

Auto-deploy remains OFF so branch movement cannot silently replace the live deployment. Manual deployment is allowed only after the exact candidate SHA passes the final gates.

## Deletion boundary

Branch and Render-service cleanup is intentionally deferred until P0 + P1 + live QA are complete and a release tag/rollback checkpoint exists.
