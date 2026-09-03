# MASTER-141 — Championship Loop

## Objective
Move URBION from release completeness toward judge-visible product strength.

## Operating loop
1. Build the decision capability.
2. Integrate it into the judge-facing UI.
3. Protect the integration with regression tests.
4. Run CI on main.
5. Verify deployment identity separately from source control.
6. Red-team the decision boundary and evidence provenance.
7. Repeat until no material judge-facing gap remains.

## Product standard
A capability is not considered complete merely because an API or module exists. It is complete when a judge can discover it, interact with it, understand the result, inspect evidence/provenance, and continue to the next planning action.

## Priority surfaces
- Dashboard command centre
- Map Studio spatial evidence
- Evidence/provenance visibility
- What-If scenario comparison
- Decision Center
- KM/OSC planner review
- Judge Mode pathway
- Bilingual and theme controls
- Deterministic safety and evidence guardrails

## Boundary
URBION provides planning decision support. It must not fabricate statutory controls, imply approval, or present unverified GIS geometry as verified fact.
