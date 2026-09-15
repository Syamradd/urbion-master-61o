# URBION HORIZON — Final Blocker Checklist

## 1. Authoritative GIS
- [ ] 14-layer authoritative i-Plan upstream preflight passes
- [ ] 14-layer canonical `/map/wms` proxy preflight passes
- [ ] 25 canonical layer IDs hydrate in the workspace
- [ ] 25/25 layers render as `ON · RENDERED`
- [ ] i-Plan cached fallbacks remain authoritative (TMS/WMTS/WMS/official ArcGIS only)
- [ ] JMG Major Fault / Quarries render through official MapServer/FeatureServer paths
- [ ] Cadastral remains authoritative source-context only; no fabricated parcel geometry

## 2. Canonical Planning Workflow
- [ ] State → PBT → District → Mukim → Lot/UPI cascade works
- [ ] Project reference → land use → development → intensity flow remains canonical
- [ ] `/workstation/analysis` completes without timeout or silent failure
- [ ] What-If scenarios execute and rank deterministically
- [ ] Decision Centre remains informational only
- [ ] `decision_authority = NONE`
- [ ] `statutory_verification = NOT_CLAIMED`

## 3. Evidence / Provenance
- [ ] Evidence packet is attached to assessment/workstation outputs
- [ ] Source context is not presented as statutory verification
- [ ] Planning rules/guidelines retain provenance links
- [ ] No dummy, placeholder, fabricated or invented authoritative evidence

## 4. LCP / KM / Agent Enrichment
- [ ] LCP intelligence path returns structured output
- [ ] KM readiness path returns structured output
- [ ] Bounded agents return deterministic structured synthesis
- [ ] Parallel enrichment does not block the canonical assessment path

## 5. Browser / UI
- [ ] Canonical workspace title and presentation surface pass
- [ ] Layer drawer owns the live 25-layer catalogue
- [ ] Layer state transitions are truthful (`OFF`, `LOADING`, `ON · RENDERED`, `ERROR`)
- [ ] About route guard works
- [ ] Deep browser functional smoke passes
- [ ] Responsive / cross-browser checks pass where included by CI

## 6. Release / CI
- [ ] Source gate green
- [ ] Rule provenance gate green
- [ ] Full regression green
- [ ] Runtime topology smoke green
- [ ] About functional smoke green
- [ ] Deep browser functional smoke green
- [ ] GIS preflight green
- [ ] 25-layer GIS render audit green
- [ ] Canonical release audit green

## 7. Release Discipline
- [ ] No branch merge performed
- [ ] No Render deployment performed unless explicitly requested
- [ ] No architecture rewrite
- [ ] No duplicate frontend/engine
- [ ] No weakened assertions solely to obtain green CI
