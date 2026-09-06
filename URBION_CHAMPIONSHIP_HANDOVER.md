# URBION HORIZON — Championship Handover

## Active release state
- Repository: `Syamradd/urbion-master-61o`
- Championship branch: `feature/champion-command-center-consolidation`
- Production baseline branch: `main` (do not deploy championship work here)
- Release identity: `MASTER-132`
- Engine: `PHASE-E.8`
- Frontend release contract: `MASTER-331`
- Championship PR: `#111` (OPEN)

## Current command-centre architecture
The public championship root is intentionally a single final Planning Command Centre runtime. Historical browser modules remain available for backend/source audit but are not booted together on the public root.

Primary root runtime order:
1. `urbion_championship_premium_v3.js` — captures Leaflet map before final centre; premium shell/map settings
2. `urbion_championship_final_command_center.js` — core planning workflow
3. final command-centre hotfix/polish/policy/review
4. `urbion_championship_unified_bridge.js` — shared state / planning rail bridge
5. `urbion_championship_premium_v2.js`
6. `urbion_championship_premium_v4.js` — grouped layers, Site↔TOD line, settings, footer, focus states
7. `urbion_championship_gap_closure.js` — AI explain, station/mobility, judge surface, unified export, input cascade
8. inert compatibility runtime enforcer

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
- unified case package export
- explicit Judge View surface
- AI Explain surface backed by `/copilot/run`
- station/mobility surface backed by `/station-intelligence`
- real Land Use → Category → Activity → Development cascade

## Remaining scope boundary
Document validation workflow is still not implemented and must not be represented as complete. It remains optional championship scope until a real validation engine and regression coverage are added.

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
