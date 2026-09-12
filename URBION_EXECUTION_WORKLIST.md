# URBION HORIZON — Execution Worklist

## Phase 0 — Core Functional Gate (NOW)
- [x] Workspace route / title / map boot
- [x] Canonical script ownership and duplicate-DOM guards
- [x] State → District → Mukim hierarchy
- [x] Local Authority canonical select
- [x] Single frontend PBT catalogue owner
- [x] Full 16-state/territory PBT catalogue exposed
- [x] GT1 → GT2 → GT3 taxonomy cascade
- [x] Street / Satellite / Hybrid basemap switching
- [x] 25/25 mandatory live GIS layers rendered in Browser Gate checkpoint
- [x] Map click coordinate update
- [ ] Readiness fixture + Run Site Analysis gate
- [ ] Analysis Complete + deterministic result state
- [ ] AI / Copilot response path
- [ ] Evidence modal
- [ ] What-If exactly-once request
- [ ] Decision center
- [ ] Output generation / print
- [ ] Utility buttons / theme / language / responsive checks
- [ ] Browser Gate GREEN

## Phase 1 — Core Integrity Freeze
- [ ] Reconcile final button matrix against runtime selectors
- [ ] Final duplicate-handler / shared-state audit
- [ ] English-only UI/content cleanup after functional gate
- [ ] Update freeze/release documentation

## Phase 2 — Live Environmental Context (APPROVED NEXT)
Principle: **additive and failure-safe; never make external monitoring a mandatory core-layer dependency.**

### A. Generic monitoring contract
- [ ] `EnvironmentalMonitoringSource` contract
- [ ] station metadata: id, name, agency, type, coordinates
- [ ] latest observation + timestamp + unit
- [ ] official classification/status
- [ ] distance / spatial relevance
- [ ] freshness
- [ ] source status / evidence gap
- [ ] confidence tier

### B. Pilot integrations
- [ ] JAS MyEQMS / EQMP — Air Quality station context
- [ ] JPS Public Infobanjir — rainfall station context
- [ ] JPS Public Infobanjir — river level / alert-threshold context
- [ ] JAS EQMP — river water quality context (continuous/manual where available)
- [ ] JAS EQMP — marine water quality context (continuous/manual where available)

### C. Spatial intelligence
- [ ] Show nearby monitoring stations on map
- [ ] Station popup / source detail
- [ ] Rank nearest relevant station, not distance-only where network relationship matters
- [ ] Feed selected station context into Planning Intelligence
- [ ] Never convert station observation into a direct site measurement claim
- [ ] Graceful `QUERY_ERROR` / `EVIDENCE_GAP` handling

## Phase 3 — Basemap Gallery
- [ ] Streets
- [ ] Satellite
- [ ] Hybrid
- [ ] Topographic
- [ ] Navigation
- [ ] Light Gray
- [ ] Dark Gray
- [ ] Streets Night
- [ ] Keep current core basemap switching contract intact

## Phase 4 — Advanced Environmental Intelligence
- [ ] trend direction
- [ ] observation freshness
- [ ] historical / rolling context
- [ ] rainfall + river-level event correlation
- [ ] upstream/downstream relevance where verified
- [ ] monitoring confidence score

## Phase 5 — Championship UX / Demo
- [ ] premium visual polish
- [ ] final map choreography
- [ ] Google Flow AI video
- [ ] AI voice-over
- [ ] music / SFX
- [ ] final judge walkthrough

## Deployment Lock
- **NO Render deployment during functional development.**
- Deploy only after explicit `DEPLOY RENDER NOW` instruction.
