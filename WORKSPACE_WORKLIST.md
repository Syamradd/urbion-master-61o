# URBION HORIZON — Benchmark-Driven Workspace Worklist

Branch: `feature/canonical-workspace-v2`
Scope: **restore and surface previously-built capability without rebuilding engines or creating duplicate UI surfaces.**
Welcome + About Us: **DO NOT TOUCH in Workspace work.**

## 0. Architecture lock — P0
- [x] Canonical `/workspace` route and isolated V5 presentation path.
- [x] Single canonical UI owner.
- [x] Single modal owner.
- [x] Single live GIS layer manager.
- [x] Legacy `urbion_workspace_final.js` is not requested by Workspace.
- [x] Backend planning/data engines are reused rather than rebuilt.
- [ ] Keep functional contracts stable during all later visual work: IDs, data attributes, event contracts, shared state, API routes and GIS registry.
- [ ] No second dashboard, duplicate handler layer or parallel workspace surface may be introduced.

## 1. Capability benchmark recovery — P0
Use the previously-built URBION capability lineage as the benchmark, not only the latest visual comments.
- [ ] Case input / planning workflow fully surfaces the existing capability set.
- [ ] Spatial context / suitability intelligence is visible in the current V5 rail.
- [ ] Evidence + provenance chain is visible and tied to the active case.
- [ ] What-If scenario pathway remains connected to shared assessment state.
- [ ] Decision Support uses the same case state and evidence chain.
- [ ] Planner-Ready Output uses the same case state; no separate output engine/UI.
- [ ] Policy / impact / LCP intelligence is surfaced where already supported by existing backend contracts.
- [ ] Lot resolution / spatial context foundations remain connected; no reimplementation.
- [ ] Workflow / orchestration state remains shared across inputs → analysis → scenario → decision.

## 2. Planning Case — Location hierarchy — P0
- [ ] State dropdown contains the full Malaysian state / federal territory set required by the product.
- [ ] District dropdown is populated dynamically from selected state.
- [ ] Mukim dropdown is populated dynamically from selected district.
- [ ] State → District → Mukim cascade resets downstream values safely when an upstream value changes.
- [ ] Location hierarchy is data-driven, not a short hardcoded subset.
- [ ] Lot / UPI remains available as manual input and future resolver target.
- [ ] Latitude / Longitude remain synchronized with map selection / Locate.
- [ ] Map Selection updates the same canonical case state.

## 3. Planning Case — Case readiness / completion — P0
- [ ] Restore visible case completion percentage (for example `42% COMPLETE`).
- [ ] Progress reflects required field completion, not arbitrary animation.
- [ ] Show which major planning domains are complete / incomplete.
- [ ] Define mandatory fields separately from optional fields.
- [ ] `RUN SITE ANALYSIS` is unavailable until the minimum required case state is satisfied.
- [ ] Run gate must use the same canonical shared state as the analysis endpoint.
- [ ] Completion state updates immediately when inputs change.
- [ ] Changing upstream case inputs invalidates stale assessment state safely.

## 4. Planning Case — Section layout / compactness — P1
- [ ] Remove large post-input empty spaces in Section 01.
- [ ] Remove equivalent empty spaces in Sections 02, 03, 04, 05 and all later sections.
- [ ] Convert sections to content-driven height; do not use giant fixed heights.
- [ ] Keep accordion behaviour intact.
- [ ] Keep validation, labels, controls and hitboxes intact.
- [ ] Keep left-panel scrolling contained; prevent artificial full-page scrolling.
- [ ] Make collapsed sections compact and scannable.
- [ ] Re-test 1366×768, 1440×900 and 1920×1080 after tightening.
- [ ] Ensure compacting the left panel does not change map dimensions or right-rail behaviour.

## 5. Layer map UX — P0 functional / P1 presentation
- [x] Authoritative live layer catalogue populated.
- [x] 25 advertised live GIS layers have passed end-to-end browser checks: select → mount → rendered imagery → non-error state.
- [ ] Verify deselect consistently removes the overlay while preserving the active basemap.
- [ ] Verify State change clears prior live overlays and rebuilds the catalogue once.
- [ ] Verify Refresh does not duplicate layer rows or handlers.
- [ ] Keep layer grouping independent from the main Layers drawer toggle.
- [ ] Every row exposes a clear `OFF / LOADING / ON · RENDERED / ERROR` state.
- [ ] Add a compact source/type legend where useful without obscuring the map.
- [ ] Do not add fake imagery, placeholder geometry or a second GIS renderer.
- [ ] Treat external upstream cancellation/availability separately from core URBION application failures.

## 6. Map interaction / overlay controls — P1
- [ ] Basemap switching remains exclusive: Street ↔ Satellite ↔ Hybrid.
- [ ] Active basemap is never removed by `CLEAR MAP`.
- [ ] `CLEAR MAP` removes only live overlays / analysis layers.
- [ ] Layer drawer may support an explicit compact transparency/opacity control if it improves usability, but it must operate on existing layer objects only.
- [ ] Opacity UI must not introduce a second layer registry or duplicate toggle handlers.
- [ ] Search / Locate / Use Map Selection continue to update canonical site coordinates.

## 7. Core decision workflow — P0
- [x] Site analysis request executes once per Run click.
- [x] Analysis completion and readiness states update.
- [x] Evidence action opens expected surface.
- [x] What-If opens and reaches backend/result state.
- [x] Decision Support opens expected surface.
- [x] Planner-Ready Output opens expected surface.
- [ ] Verify output content is populated from current case state after real user input, not only demo defaults.
- [ ] Verify analysis/What-If/Decision do not retain stale results after material case changes.

## 8. Runtime / utility controls — P1
- [x] About, Help, Sources, Status, Fullscreen, Reset controls are injected once.
- [x] Help / Sources / Status open correctly.
- [x] Theme toggle works.
- [x] BM ↔ EN toggle works.
- [ ] Verify About button routes only to canonical About surface and does not alter About itself.
- [ ] Verify Reset clears the complete planning case state consistently.

## 9. Visual redesign — P1, ONLY after functional freeze
This is a **presentation-only pass**. It may change:
- [ ] layout/grid proportions
- [ ] typography
- [ ] spacing
- [ ] cards/panels
- [ ] colours/gradients
- [ ] icons
- [ ] map framing
- [ ] decorative graphics
- [ ] animation/micro-motion

It must NOT change without an explicit contract update + tests:
- [ ] canonical element IDs
- [ ] data attributes used by logic
- [ ] event ownership / handler guards
- [ ] shared state objects
- [ ] API routes
- [ ] GIS layer definitions
- [ ] backend response contracts

## 10. Visual target for the redesigned Planning Case — P1
- [ ] Left panel becomes a compact planning-case navigator rather than a sequence of tall empty cards.
- [ ] Case readiness percentage is persistent near the top of the case panel.
- [ ] Sections show clear completion state where available.
- [ ] Inputs remain readable and planner-oriented.
- [ ] Map gets the largest visual weight.
- [ ] Intelligence rail remains readable without competing with the map.
- [ ] Layers panel overlays the map cleanly and does not cover critical map controls.
- [ ] Responsive layout remains usable at common desktop widths.

## 11. Regression gates after every functional change — P0
- [ ] Source Gate GREEN.
- [ ] Deep Browser Gate GREEN.
- [ ] No duplicate DOM IDs.
- [ ] Canonical UI owner guard active.
- [ ] Single layer-manager guard active.
- [ ] Single modal-owner guard active.
- [ ] No legacy frontend asset requests.
- [ ] No unexpected core HTTP/request failures.
- [ ] GIS upstream events are classified separately and honestly.

## 12. Regression gates after visual redesign — P0
- [ ] Full functional Browser Gate rerun after visual changes.
- [ ] Visual screenshots compared at 1366×768, 1440×900 and 1920×1080.
- [ ] No page overflow.
- [ ] No panel overlap obscuring controls.
- [ ] No map resize regression.
- [ ] No lost event handlers / disabled controls.
- [ ] No Welcome regression.
- [ ] No About Us regression.

## 13. Release order — LOCKED
1. Restore / surface missing capabilities.
2. Complete Location hierarchy + Case Readiness.
3. Compact all Planning Case sections.
4. Stabilize map/layer UX.
5. Functional freeze.
6. Premium visual redesign using the preserved contracts.
7. Full functional + visual regression gates.
8. Explicit Render deployment.
9. Live Render route/map/layer/analysis/interactions audit.
10. Only then declare release candidate.
