# MASTER-134 — Deployment-Safe Decision Center

## Change
Decision Center now resolves the URBION API from `location.origin` instead of a hard-coded Render hostname.

## Why
The Judge Flow must remain portable across preview, production and alternate deployments. A stale or mismatched API hostname can make the shell report the wrong engine state even when the current deployment is healthy.

## Regression gate
`tests/test_decision_center_contract.py` verifies same-origin API usage, removal of the legacy Render hosts, and preservation of the core Assess → Map → What-If navigation.

## Boundary
No decision rules, planning evidence, GIS semantics or statutory claims were changed.
