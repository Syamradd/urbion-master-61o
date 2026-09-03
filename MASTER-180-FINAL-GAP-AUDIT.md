# MASTER-180 — Final Gap Audit

## Objective
Attack the remaining championship risks after the MASTER-179 lock. Do not add speculative features; harden judge-visible coherence, navigation, evidence visibility, bilingual/theme UX, GIS credibility, and deployment smoke coverage.

## Locked product loop
**Site Assessment → Map Studio → Evidence → What-If → Decision Center → Planner Review → KM/OSC**

## Audit gates
- Live frontend uses the deployment origin for API calls.
- Judge-facing surfaces expose a consistent PHASE-E.7 identity.
- Navigation exposes the full judge path without dead-end pages.
- Evidence state remains distinguishable from statutory verification.
- What-If visibly explains baseline/scenario delta.
- Planner Review exposes blockers and next evidence/action.
- Map Studio exposes declared judge controls and official-source provenance.
- Invalid spatial placeholders cannot produce a positive decision.
- Remote values rendered into judge-facing surfaces are escaped.
- Actual GitHub Actions full regression success is required before GREEN.

## Out of scope
No claim of statutory approval, no prediction of approval probability, no unauthorised private/public-service API bypass, and no fabricated local planning controls.

## Next sequence
MASTER-181 — live UI/bilingual/theme polish.
MASTER-182 — judge navigation and 90-second flow hardening.
MASTER-183 — evidence/GIS credibility pass.
MASTER-184 — deployment smoke contract.
MASTER-185 — final red-team.
MASTER-186 — championship release.
