# URBION HORIZON — MASTER-69 FINAL FREEZE

## Product
URBION is an AI-assisted spatial and planning decision-support workflow that connects site context, development typology, verified planning rules, applicability, compliance, evidence intelligence and an explainable recommendation.

## Decision chain
SITE → SPATIAL → LAND/PLANNING CONTEXT → TYPOLOGY → POLICY RETRIEVAL → APPLICABILITY → COMPLIANCE → EVIDENCE → DECISION → RECOMMENDATION

## Verified local rule coverage
- MBMB / RT MBMB 2035
- Supported verified typologies include TOD Development / Mixed Use, Free-Standing Commercial, Free-Standing Building, Commercial Shop Frontage and Commercial Shop-Office.

## Evidence guard
External authoritative GIS portals are not represented as live verified data unless an explicit evidence state supports that claim. Planned, unavailable and discovery-only sources remain visible as evidence gaps.

## Showcase scenarios
- TOD-COMPLY
- SHOP-COMPLY
- SHOP-FAIL
- OFFICE-REVIEW
- NON-MBMB

## Judging message
URBION does not replace the planner. It reduces the first layer of planning intelligence into a transparent, traceable and explainable workflow so planners can screen faster and focus human attention where evidence or policy judgement is required.

## Final QA checklist
- [ ] `/health` returns healthy
- [ ] `/metadata` returns current version
- [ ] `/assess` returns decision + recommendation + confidence
- [ ] `/evidence-summary` exposes source states
- [ ] demo scenarios return deterministic showcase results
- [ ] frontend loads public API
- [ ] no external source is falsely labelled verified
- [ ] demo data is clearly labelled as showcase data

Planning decision-support only. Not statutory approval.
