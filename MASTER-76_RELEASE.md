# MASTER-76/78 Release Readiness

## Runtime contract
- FastAPI application served by Uvicorn.
- `/health` is the deployment health check.
- `/assess` is the primary decision endpoint.
- `/metadata`, `/demo-scenarios`, and `/evidence-summary` expose explainability and judging context.

## Decision safety
- MBMB / RT MBMB 2035 remains the verified local rule-engine coverage.
- Other PBTs remain spatial-demo coverage until local statutory rules are loaded and verified.
- External GIS discovery is never promoted to verified evidence without supporting evidence state.
- Suitability and confidence are screening indicators, not approval probability.

## Deterministic judge cases
`TOD-COMPLY`, `SHOP-COMPLY`, `SHOP-FAIL`, `OFFICE-REVIEW`, `NON-MBMB`.

## Release gate
GitHub Actions must pass the complete pytest regression suite before a judging freeze is declared. Render deployment status must be verified separately; repository readiness does not by itself prove the public service is live.
