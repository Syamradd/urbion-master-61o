# URBION HORIZON — Release Identity

Status: `CANONICAL REPAIR CANDIDATE / RENDER VALIDATION PENDING`

## Current release candidate

- Product: `URBION HORIZON`
- Active release branch: `feature/canonical-workspace-v2`
- Canonical HEAD candidate: `b46067bbf51d5598bd80e2b5304a4beca3c9610e`
- Current repair lineage includes WMS proxy normalization, real tile-load state handling, 25-layer end-to-end GIS test hardening, browser release-gate hardening, and canonical documentation reconciliation.
- Previous baseline: `645fca153fea6ea2332229cf913b22a6d07db559`
- Render target: `urbion-horizon-workspace-v4`
- Render service ID: `srv-dahm749594qs73fk2tag`
- Render branch: `feature/canonical-workspace-v2`
- Render currently serving: `ae91eabc6dcc4df9d5312294526ff65f9b7616c6`; this is an intermediate build and is not yet certified as the final release.
- Auto deploy: `off`

## Engineering identity

- Engine contract: `PHASE-E.8`
- Evidence packet: `PHASE1.2`
- Canonical UI: `V5 Planning Workspace`
- Canonical application entrypoint: `landing_server:app`
- Existing Render launcher: `workspace_v4_server:app`
- Launcher invariant: `workspace_v4_server:app -> landing_server:app`
- Canonical route: `/workspace`
- Public root: `/` → canonical Welcome
- About route: `/about` → canonical About Us
- Canonical runtime topology: `bridge → compatibility bootstrap → layer manager → canonical UI → specialist owners`
- Error contract: `URBION_ERROR_V1`
- Evidence states: `USER_PROVIDED`, `CALCULATED`, `SOURCE_CONTEXT`, `VERIFIED`, `UNVERIFIED`
- Statutory verification: `NOT_CLAIMED`
- Decision authority: `NONE`

## Integrated repair on current candidate lineage

- i-Plan WMS tile requests are routed through the same-origin `/map/wms` proxy instead of direct browser requests to the upstream WMS host.
- WMS proxy query parameters are normalized case-insensitively before validation/forwarding.
- ArcGIS imagery remains routed through the same-origin `/map/arcgis` proxy.
- GIS layers are only reported `ON · RENDERED` after an actual Leaflet `tileload` event; timeout/error states are not promoted to success.
- About controls are guarded to navigate to `/about`.
- English workspace label normalization is retained.
- The 24 core GIS API layers plus explicit i-Plan cadastral layer remain the canonical layer contract.
- Existing Render service, build command and launcher are preserved.

## Branch / deployment rule

Only `feature/canonical-workspace-v2` is the active release branch. `main` may mirror the same release SHA when the release is accepted, but it is not the Render control branch. Historical, parallel, temporary, forensic and legacy branches are reference snapshots only and must not be used for deployment.

## Certification gates

- [x] Architecture identity established
- [x] Render service target established
- [x] WMS proxy exists and is allow-listed
- [x] GIS layer runtime repair integrated
- [x] About navigation repair integrated
- [x] Prior canonical full regression passed on `ae91eabc`
- [ ] Fresh current-head full regression after GIS hardening
- [ ] Fresh browser/GIS smoke after GIS hardening
- [ ] Controlled live smoke on exact final deployed SHA
- [ ] Final release SHA lock
- [ ] Release tag
