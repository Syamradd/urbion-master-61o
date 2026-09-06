# MASTER-353 — Decision-Grade Spatial Validation

## Purpose
Validate that the championship workspace is a single connected planning decision flow rather than a collection of independent dashboard surfaces.

## Canonical flow

USER / PROJECT REFERENCE
→ OFFICIAL PUBLIC GIS
→ VERIFIED CANDIDATE
→ JUPEM CADASTRAL VERIFICATION (when authoritative cadastral confirmation is required)
→ CANONICAL SITE IDENTITY
→ CURRENT LAND USE / ZONING / FLOOD / TERRAIN / GEOLOGY / TOD / POLICY
→ WHAT-IF
→ DECISION

## Acceptance matrix

| Capability | Backend / source | API / bridge | UI surface | Map / evidence | Decision handoff |
|---|---|---|---|---|---|
| Case inputs | Required | Required | Required | Context only | Required |
| Lot identity | i-Plan LOT candidate | Required | Required | Real geometry only | Required |
| Cadastral authority | JUPEM verification channel | Explicit status | Visible qualification | No fake layer | Authority caveat |
| Current land use | i-Plan GTsemasa | Required | Required | Geometry when returned | Required |
| Zoning | i-Plan GTzoning | Required | Required | Geometry when returned | Required |
| Flood / risk | Official public spatial sources where available | Required | Required | Geometry when returned | Required |
| Terrain | i-Plan contour / terrain context | Required | Required | Geometry when returned | Required |
| Geology | MyGEMS public spatial services where available | Required | Required | Geometry when returned | Required |
| Mobility / TOD | Real station / network evidence | Required | Required | Catchments only when backed by geometry | Required |
| Evidence | Source + status model | Required | Visible | Source-linked | Required |
| What-If | Existing deterministic engine | Required | Existing surface | Uses canonical site state | Required |
| Decision | Existing explainable decision layer | Required | Existing workstation surface | Evidence-backed | Final output |

## Hard acceptance rules

1. **NO GEOMETRY = NO MAP LAYER.** A layer control must not imply live geometry when no geometry is available.
2. `VERIFIED_CANDIDATE` from i-Plan is a planning-source candidate, not legal cadastral verification. JUPEM verification remains explicit where authoritative cadastral claims are required.
3. `LIVE_QUERY`, `NO_FEATURE`, `QUERY_ERROR`, `EVIDENCE_GAP`, and `SOURCE_CONTEXT` remain distinguishable; absence is not converted into fake certainty.
4. The current V4/V5 command-center remains the primary UI. No second dashboard or duplicate floating workstation is introduced.
5. Evidence → What-If → Decision remains the decision pathway.
6. Existing deterministic planning engines and MASTER-330 release identity are preserved.
7. The unified workspace bridge is the state handoff layer; downstream surfaces consume the canonical state rather than maintaining disconnected copies.
8. Visual QA is a separate final gate: CI contract success is not treated as human visual approval.

## Orphan / duplicate audit targets

- Duplicate utility chrome or theme controls.
- Legacy Decision OS / workstation surfaces leaking into the primary dashboard.
- GIS controls without a geometry-producing source.
- Endpoints that do not feed a visible downstream surface.
- Visible surfaces that do not consume canonical state.
- MASTER modules that duplicate current engines instead of acting as compatibility layers.
- Claims that exceed the authority of the underlying public source.

## Final gate

MASTER-353 is complete only when the acceptance matrix is green, no unsafe fake spatial layers remain, no duplicate dashboard surface remains, and the live deployment has been visually inspected after merge. Render deployment is intentionally outside CI and must not be claimed from CI success alone.
