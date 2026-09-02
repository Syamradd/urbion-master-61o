# MASTER-131 — Live Release Verification

## Verification contract

The deployed service must expose the same release identity as GitHub `main` before it is treated as the championship deployment.

Required checks:

1. GitHub `main` release identity.
2. Backend `/health` release identity.
3. Backend `/metadata` release identity.
4. Assessment endpoint remains reachable and deterministic.
5. Frontend release identity matches the deployed backend where applicable.

## Stale deployment rule

If a deployed endpoint reports an older MASTER version than GitHub `main`, the deployment is **STALE** and must not be presented as the current championship release.

## Boundary

This verification does not claim deployment success from source control alone. Live deployment status must be confirmed from the deployed service.
