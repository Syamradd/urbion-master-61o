# MASTER-181 — Live UI, Bilingual & Theme Polish

## Objective
Turn the existing shared UI controller into judge-visible consistency across the live frontend without changing deterministic planning logic.

## Acceptance gates
- English and Bahasa Melayu controls are visible on the live dashboard.
- System, Dark and Light theme choices are visible and persisted.
- PHASE-E.7 identity remains consistent after UI changes.
- Navigation links remain available to Map Studio, What-If and Decision Center.
- No remote data is rendered without escaping on upgraded judge-facing surfaces.
- Same-origin API contract remains intact.

## Boundary
Language/theme controls are presentation features. They do not alter assessment rules, evidence states, statutory status, or approval outcomes.
