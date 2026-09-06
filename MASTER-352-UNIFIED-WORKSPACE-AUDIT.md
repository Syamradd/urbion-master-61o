# MASTER-352 — Unified Workspace Audit

## Objective

Consolidate the recovered MASTER capability families into the current UX V5 command-center without reviving legacy popups or duplicate workstations.

## Trace map

| Capability family | Recovered lineage | Current disposition |
|---|---|---|
| Site intelligence / suitability | MASTER-62, 275, hardening batch | Keep deterministic assessment engine; evidence-aware scoring remains authoritative |
| Visual decision dashboard | MASTER-65, 273, 305, visual-overhaul branch | Keep premium map-first visual hierarchy; no decorative/fake evidence |
| Evidence / provenance | MASTER-68, 80, 106, 110, 114–116, 171 | Keep source-aware evidence chain and explicit gaps |
| Scenario / What-If | MASTER-84, 89, 172, 199, 263–264, 300–302 | Keep scenario deltas behind one decision pathway |
| Decision Center / judge mode | MASTER-88, 92, 98, 134–140, 235, 258–278, 303, 317–321 | Consolidate into the V5 right rail and existing decision surfaces |
| GIS / parcel / planning layers | MASTER-97, 101–106, 110, 183–184, 277–284, 299, 304 | Keep real geometry only; live sources feed the existing Leaflet map |
| Impact / policy / recommendations / LCP | MASTER-185–188, 199 | Retain backend engines and evidence/action handoff; avoid extra UI surfaces |
| Workflow / state / orchestration | MASTER-308–314, 317–324 | Use shared assessment state and decision-chain contracts |
| Release / integrity | MASTER-325–350, current CI and UX contracts | Preserve gates; no merge or Render deployment before green validation |
| Cross-source lot identity | MASTER-351 | Link official i-Plan candidate geometry to case/map; JUPEM remains cadastral verification boundary |

## UX consolidation rule

The user-facing workstation has one visual hierarchy:

`CASE INPUT → MAP / SPATIAL EVIDENCE → INTELLIGENCE RAIL → WHAT-IF → DECISION / OUTPUT`

Legacy `urbion-workstation-v2` and `urbion-decision-os` surfaces remain backend/compatibility assets where required by contracts, but must not become additional floating UI surfaces.

## Interconnection rule

A change to site inputs invalidates the shared assessment state and propagates through the existing spatial-context, lot-resolution and decision pathways. Live GIS hits, lot identity and assessment completion update the existing V5 rail rather than creating new cards or popups.

## Safety / evidence boundary

- No fabricated geometry.
- No statutory cadastral claim from i-Plan.
- No hidden fallback presented as live evidence.
- WMS/ArcGIS layers remain source context unless the underlying engine explicitly marks a stronger evidence state.
- What-If remains scenario analysis, not a statutory approval.

## Current finding

The current feature branch already contains the recovered GIS, workstation, decision, workflow and lot-resolution foundations. The separate visual-overhaul branch is intentionally not merged wholesale because it diverged from the current feature branch; its visual changes are used only where they are additive and non-conflicting. The unified bridge is therefore a small orchestration layer, not a second dashboard.
