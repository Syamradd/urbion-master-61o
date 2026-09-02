# MASTER-88 — Judge Dashboard Integration

## Objective
Connect the Phase-D What-If workspace to the main judging flow without changing the verified backend engine.

## Current integration contract
- Main assessment remains the primary site-screening workflow.
- `what-if.html` is the dedicated scenario workspace.
- The workspace calls the live `/what-if` endpoint on the same Render backend.
- Scenario outputs are ranked by compliance outcome, blockers, evidence burden and suitability score.
- Non-MBMB scenarios remain evidence-gated.
- The What-If layer is decision support only and never statutory approval.

## Judge flow
1. Run the site assessment.
2. Open the What-If workspace.
3. Change one planning assumption.
4. Execute the variant through the same engine.
5. Compare status, score delta, evidence gaps and pathway.
6. Advance the strongest candidate to planner review.

## Deployment principle
Keep the existing static Render frontend and FastAPI Render backend. No Railway dependency is required for this phase.
