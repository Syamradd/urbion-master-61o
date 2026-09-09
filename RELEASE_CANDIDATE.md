# URBION HORIZON Release Candidate

This marker intentionally contains no runtime logic. It creates a fresh main commit so the exact release candidate containing the HORIZON UI wiring is evaluated by the full GitHub Actions CI before production deployment.

## Required gates
- Full regression CI
- Championship browser QA
- Runtime smoke
- Exact release-candidate SHA validated before Render deployment

## Release scope
- HORIZON visual system wired into canonical production root
- Branded About page
- Bounded map/layer drawer and map attribution layout
- Existing planning, evidence, GIS and decision semantics unchanged
