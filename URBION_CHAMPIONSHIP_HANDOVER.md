# URBION HORIZON — Championship Handover

## Active release state
- Repository: `Syamradd/urbion-master-61o`
- Championship branch: `feature/champion-command-center-consolidation`
- Production baseline branch: `main` (do not deploy championship work here)
- Release identity: `MASTER-132`
- Engine: `PHASE-E.8`
- Frontend release contract: `MASTER-331`
- Championship PR: `#111`

## Current command-centre architecture
The public championship root is intentionally a single final Planning Command Centre runtime. Historical browser modules remain available for backend/source audit but are not booted together on the public root.

Primary root runtime order:
1. `urbion_championship_premium_v3.js` — captures Leaflet map before final centre; premium shell/map settings
2. `urbion_championship_final_command_center.js` — core planning workflow
3. final command-centre hotfix/polish/policy/review
4. `urbion_championship_unified_bridge.js` — shared state / planning rail bridge
5. `urbion_championship_premium_v2.js`
6. `urbion_championship_premium_v4.js` — grouped layers, Site↔TOD line, settings, footer, focus states
7. inert compatibility runtime enforcer

## Non-negotiable safety/evidence boundary
- `NO GEOMETRY = NO MAP LAYER`
- `VERIFIED_CANDIDATE` is a planning-source candidate, not cadastral/legal verification.
- JUPEM remains the cadastral verification authority pathway.
- Live source context is not automatic statutory verification.
- The decision engine remains planner decision support only; no automatic statutory approval is claimed.
- Accessibility is spatial/proximity context, not guaranteed pedestrian routing.

## Championship checklist
- Core engine
- Case setup and Malaysian State/PBT vocabulary
- Coordinates + lot/UPI reference
- 400 m / 800 m / 1 km / 1.5 km screening context
- Site and TOD markers + relationship line
- i-Plan planning evidence
- MyGEMS geology/geohazard
- JPS Infobanjir
- JAS MyEQMS/EQMP
- JUPEM MyLot pathway
- grouped GIS layer architecture
- evidence status states
- Policy / Guideline / Act 172 / National Land Code / RFN / RSN / RTD / OSC context
- What-If
- Decision
- KM/OSC readiness
- LCP intelligence
- BM/EN
- Dark/Light
- Street/Dark map
- fullscreen / print / reset / help / About Us / sources / system status / footer
- official URBION HORIZON logo lockup
- responsive / reduced-motion / focus-visible intent

## Known gap register to close before final championship sign-off
1. Unified export package must expose the full unified contract: case, assessment, spatial context, evidence, policy/guideline, policy graph, recommendations, agency intelligence, KM readiness, what-if, decision, LCP intelligence, evidence gaps, authority boundary, next authority action.
2. Dedicated Judge View should be surfaced as an explicit premium view, not only backend/release-gate architecture.
3. AI Explain should be visibly surfaced in the final centre where backed by existing engine contracts.
4. Station/mobility intelligence should be visible where backed by existing spatial engines.
5. Land-use → category → activity → development dependency/cascade should be genuinely driven, not merely static option lists.
6. BM/EN translation should cover detailed command-centre labels, not only top-level controls.
7. Document validation workflow remains optional scope and must not be represented as complete until actually implemented.

## Auto-repair protocol
When CI/live QA fails:
1. identify the exact failing job/test/endpoint/assertion;
2. trace to the smallest responsible source file;
3. patch the source on this championship branch only;
4. commit with a diagnostic fix message;
5. rerun the failing validation (or full CI when appropriate);
6. repeat until the latest head is green;
7. only then deploy the isolated championship Render service and run live endpoint/performance checks.

Do not claim a feature is complete merely because a contract file says it should exist. Completion requires implementation + regression test + successful validation + live verification where relevant.
