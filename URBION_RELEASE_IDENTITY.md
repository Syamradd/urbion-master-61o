# URBION HORIZON — Release Identity

Status: `CANONICAL REPAIR CANDIDATE / RENDER VALIDATION PENDING`

## Current release candidate

- Product: `URBION HORIZON`
- Active release branch: `feature/canonical-workspace-v2`
- Canonical HEAD candidate: `f5b321906d5b7e8c035c939e1c9b3f67e5993c6f`
- Parent baseline: `645fca153fea6ea2332229cf913b22a6d07db559`
- Render target: `urbion-horizon-workspace-v4`
- Render service ID: `srv-dahm749594qs73fk2tag`
- Render branch: `feature/canonical-workspace-v2`
- Render currently serving: `645fca153fea6ea2332229cf913b22a6d07db559`
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

## Integrated repair in candidate `f5b3219`

- i-Plan WMS tile requests are routed through the same-origin `/map/wms` proxy instead of direct browser requests to the upstream WMS host.
- ArcGIS imagery remains routed through the same-origin `/map/arcgis` proxy.
- About controls are guarded to navigate to `/about`.
- English workspace label normalization is retained.
- The 24 core GIS API layers plus explicit i-Plan cadastral layer remain the canonical layer contract.
- Existing Render service, build command and launcher are preserved.

## Branch / deployment rule

Only `feature/canonical-workspace-v2` is the active release branch. `main` may mirror the same release SHA, but it is not the Render control branch. Historical, parallel, temporary, forensic and legacy branches are reference snapshots only and must not be used for deployment.

## Certification gates

- [x] Architecture identity established
- [x] Render service target established
- [x] WMS proxy exists and is allow-listed
- [x] GIS layer runtime repair integrated
- [x] About navigation repair integrated
- [ ] Fresh current-head regression
- [ ] Fresh browser/GIS smoke
- [ ] Controlled live smoke
- [ ] Final release SHA lock
- [ ] Release tag
