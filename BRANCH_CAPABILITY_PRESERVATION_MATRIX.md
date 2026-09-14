# URBION HORIZON — Branch Capability Preservation Matrix

Status: `AUDITED — DO NOT DELETE HISTORICAL BRANCHES YET`
Canonical target: `feature/canonical-workspace-v2`

## Decision rule

A branch is **frozen**, not deleted, when its unique capability is either absorbed into the canonical convergence branch or intentionally retained as historical rollback/reference material. Deletion is deferred until final P0/P1 QA, release tagging, and deployment parity are proven.

| Branch | Unique work audited | Canonical status | Action | Risk |
|---|---|---|---|---|
| `feature/championship-visual-overhaul` | visual overhaul, basemap cleanup, input sync, logos, visual contract tests | **ABSORBED** for visual assets/runtime | Freeze; keep branch as visual rollback reference | Low after preservation guard |
| `feature/p7-judge-presentation-polish` | Judge Flow Contract + Judge Golden Path | **ABSORBED** | Freeze; keep docs as release contract | Low |
| `feature/post-deploy-contract-guard` | post-deploy surface contract test | **PARTIALLY ABSORBED / SUPERSEDED** by canonical capability guard | Do not port stale MASTER-330 assertions; retain branch for history | Medium |
| `feature/post-deploy-hardening-v2` | UX V3 JS + UX V3 tests/docs | **ABSORBED** | Freeze; canonical premium stack remains authoritative | Low |
| `feature/about-exact-reference` | exact About reference HTML | **REFERENCE ONLY**; required image asset is not present in convergence | Keep branch; do not merge incomplete snapshot | Medium |
| `feature/p3-1-mygems-live-adapter` | `urbion_mygems_adapter.py` + adapter tests | **RESTORED** into convergence | Keep adapter + tests on canonical branch | Low |
| `feature/p3-2-jps-source-adapter` | `urbion_jps_adapter.py` + adapter test | **RESTORED** into convergence | Keep adapter + tests on canonical branch | Low |
| `feature/p3-3-myeqms-source-adapter` | MyEQMS adapter + tests | **ALREADY PRESENT** in convergence | Freeze | Low |
| `feature/p3-3-myeqms-source-adapter-v2` | no unique commits vs convergence | **SUPERSEDED** | Freeze | Low |
| `feature/p3-station-intelligence-research` | station contract + integration checklist | **STATION CONTRACT ABSORBED**; checklist treated as historical research | Freeze | Low |
| `feature/development-impact-convergence` | development impact engine + integration work | **ABSORBED** | Freeze | Low |
| `feature/road-intelligence-v1` | road intelligence engine + UI lineage | **ABSORBED** and canonically merged into packet | Freeze; DO NOT DELETE capability | Low |
| `feature/road-intelligence-v1-fix` | earlier Road UI repair lineage | **SUPERSEDED** by active canonical Road owner | Freeze | Low |
| `feature/site-suitability-v2` | suitability work | **NO UNIQUE COMMITS** vs convergence | Freeze | Low |
| `feature/site-suitability-v2-fix` | suitability repair lineage | **NO UNIQUE COMMITS** vs convergence | Freeze | Low |
| `feature/suitability-v2` | suitability work | **NO UNIQUE COMMITS** vs convergence | Freeze | Low |
| `feature/suitability-v2-work` | suitability work | **NO UNIQUE COMMITS** vs convergence | Freeze | Low |
| `feature/suitability-myeqms-v1` | suitability/MyEQMS work | **NO UNIQUE COMMITS** vs convergence | Freeze | Low |
| `feature/suitability-myeqms-v1-work` | suitability/MyEQMS work | **NO UNIQUE COMMITS** vs convergence | Freeze | Low |
| `feature/canonical-presentation` | canonical presentation lineage | **NO UNIQUE COMMITS** | Freeze | Low |
| `feature/canonical-workspace-v2-deepfix` | workspace deepfix lineage | **NO UNIQUE COMMITS** | Freeze | Low |
| `feature/canonical-workspace-v2-temp` | temporary workspace lineage | **NO UNIQUE COMMITS** | Freeze | Low |
| `feature/canonical-workspace-v2b` | workspace lineage | **NO UNIQUE COMMITS** | Freeze | Low |
| `feature/canonical-welcome-about-v2` | welcome/about lineage | **NO UNIQUE COMMITS** | Freeze | Low |

## Canonical capabilities explicitly protected

### Planning engine
- deterministic assessment
- TOD 400 m / 800 m logic
- land-use and development taxonomy
- rule applicability and compliance
- planning value / recommendation / confidence
- LCP and KM readiness signals
- rule provenance and amendment-state review

### Evidence / AI
- canonical evidence packet `PHASE1.2`
- evidence states `USER_PROVIDED`, `CALCULATED`, `SOURCE_CONTEXT`, `VERIFIED`, `UNVERIFIED`
- evidence ledger + quality
- review gaps + traceability
- bounded Copilot / knowledge retrieval / agents
- What-If / Decision OS / Judge Demo / Planner Handoff
- statutory verification `NOT_CLAIMED`
- decision authority `NONE`

### Spatial / live source context
- authoritative i-PLAN source-context layer runtime
- 25 canonical browser-renderable overlays
- cadastral identity chain and explicit verification boundary
- Road Intelligence: nearest road, distance, hierarchy, centre proximity, rings, hierarchy chain
- JPS Public Infobanjir station context
- MyEQMS/APIMS source adapter
- MyGEMS public ArcGIS lithology adapter
- JPS station geometry adapter

### Presentation / judge flow
- V5 Planning Workspace
- canonical UI owner topology
- specialist owners
- premium visual overhaul
- basemap visual modes
- Judge Flow Contract
- Judge Golden Path
- failure-safe evidence states

## Explicitly not claimed

- authoritative JUPEM parcel geometry
- direct MelGIS/PBT parcel query as verified evidence
- direct JPS flood-service geometry
- direct MyEQMS spatial monitoring certification
- verified multimodal walking network
- statutory approval or authority decision

## Release gate

Historical branches remain available as rollback/reference material until:

1. canonical P0 gates are green on the final HEAD;
2. P1 judge-flow UX is verified;
3. one release SHA and one production entrypoint are established;
4. Render parity is proven;
5. controlled live smoke passes;
6. a release tag/identity is recorded.
