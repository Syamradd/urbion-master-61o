# URBION HORIZON — FINAL BROWSER RELEASE GATE

## Release rule

Render stays **LOCKED** until every browser gate below is manually verified on `/workspace` from the canonical branch.

## 1. Presentation / routing

- [ ] `/` opens Welcome page with locked URBION HORIZON branding.
- [ ] `/about` opens About Us with the 3 correct team members and team photo.
- [ ] `/workspace` opens only the canonical Planning Workspace.
- [ ] No legacy championship/premium frontend is injected into the canonical workspace.
- [ ] Desktop layout matches the approved 3-column command-centre composition.
- [ ] Map, left Case Builder, right Planning Intelligence and bottom intelligence docks remain readable without overlap.
- [ ] Dark/light theme does not destroy contrast or layout.

## 2. Case Builder / GT cascade

- [ ] State, district, PBT, mukim and site fields accept input.
- [ ] Guna Tanah 1 is populated from the current core taxonomy.
- [ ] Guna Tanah 2 changes when GT1 changes.
- [ ] Guna Tanah 3 changes when GT2 changes.
- [ ] No legacy `Perdagangan` value appears.
- [ ] GT1 → GT2 → GT3 selection survives into analysis payload/results.
- [ ] Numeric planning inputs accept valid values and do not throw console errors.

## 3. GIS map

- [ ] Street / Satellite / Hybrid basemaps switch visibly and exclusively.
- [ ] Map click updates the selected site coordinates/marker.
- [ ] Locate recentres the map to entered coordinates.
- [ ] 400 m / 800 m / 1000 m context rings toggle ON/OFF correctly.
- [ ] Road context toggle visibly adds/removes its layer.
- [ ] Layers panel opens and closes.
- [ ] Official catalogue layers can be toggled ON/OFF and show their state/error.
- [ ] Search returns location choices and selecting one recentres the map + updates coordinates.

## 4. Planning intelligence flow

- [ ] `RUN SITE ANALYSIS` executes without console/runtime error.
- [ ] Readiness/metrics update after analysis.
- [ ] Evidence register is populated or explicitly reports no structured evidence.
- [ ] EVIDENCE opens the evidence chain modal.
- [ ] WHAT-IF opens the scenario interface.
- [ ] DECISION opens the decision-support interface.
- [ ] OUTPUT opens the planner-ready output interface.
- [ ] Generate Output reaches the same canonical output flow.
- [ ] Print invokes browser print without breaking the workspace.

## 5. Navigation / utility controls

- [ ] PLAN closes active modal and returns to workspace.
- [ ] EVIDENCE / WHAT-IF / DECISION / OUTPUT invoke the corresponding canonical view.
- [ ] ABOUT routes to `/about`.
- [ ] HELP opens useful instructions.
- [ ] SOURCES opens source information.
- [ ] STATUS reports health/metadata/map-catalogue state.
- [ ] FULLSCREEN toggles when supported.
- [ ] RESET reloads the planning case only after confirmation.
- [ ] Language toggle changes visible supported labels without mixed-language corruption.

## 6. Browser console / network gate

- [ ] Zero uncaught JavaScript exceptions during cold load.
- [ ] Zero uncaught exceptions during every interaction above.
- [ ] `/urbion_workspace_final.js` loads successfully.
- [ ] `/urbion_workspace_bridge.js` loads successfully.
- [ ] `/urbion_workspace_runtime.js` loads successfully.
- [ ] No legacy frontend asset is requested by `/workspace`.
- [ ] No failed critical API request during the core journey.

## 7. Visual freeze

- [ ] 1440×900 desktop: no clipping/overlap.
- [ ] 1366×768 desktop: no clipping/overlap of critical controls.
- [ ] 1920×1080 desktop: composition remains balanced.
- [ ] Typography hierarchy matches approved visual direction.
- [ ] Cyan/mint accent remains restrained and professional.
- [ ] Map remains the visual hero, not a generic dashboard chart.
- [ ] No duplicate buttons, ghost controls, broken overlays or stale legacy labels.

## Sign-off

**Source gate:** GREEN when canonical files are present and ordered `final → bridge → runtime`.

**Browser gate:** GREEN only after live interactive browser inspection confirms Sections 1–7.

**Render gate:** remains LOCKED until Browser gate = GREEN and the user explicitly authorizes `DEPLOY RENDER NOW`.
