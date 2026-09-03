# MASTER-173 CI Parallel Gate

Run the full regression suite plus targeted contracts in the same workflow invocation where supported. Target gates: What-If delta, evidence UI, Map Studio controls, KM readiness, spatial-input guard, UI controller, and deployment/frontend contracts.

A green gate requires the repository's actual GitHub Actions result to complete successfully; documentation alone never counts as CI verification.
