# URBION HORIZON — Final Blocker Checklist

## 1. Authoritative GIS
- [ ] 14-layer authoritative i-Plan upstream preflight passes
- [ ] 14-layer canonical `/map/wms` proxy preflight passes
- [ ] 25 canonical layer IDs hydrate in the workspace
- [ ] 25/25 layers render as `ON · RENDERED`
- [ ] i-Plan cached fallbacks remain authoritative (TMS/WMTS/WMS/official ArcGIS only)
- [ ] JMG Major Fault / Quarries render through official MapServer/FeatureServer paths
- [ ] Cadastral remains authoritative source-context only; no fabricated parcel geometry
- [x] Latest JMG repair applied through the canonical proxy path; no fake geometry introduced

## 2. Canonical Planning Workflow
- [x] State → PBT → District → Mukim → Lot/UPI cascade works
- [x] Project reference → land use → development → intensity flow remains canonical
- [x] `/workstation/analysis` completes without timeout or silent failure
- [x] What-If scenarios execute and rank deterministically
- [x] Decision Centre remains informational only
- [x] `decision_authority = NONE`
- [x] `statutory_verification = NOT_CLAIMED`

## 3. Evidence / Provenance
- [x] Evidence packet is attached to assessment/workstation outputs
- [x] Source context is not presented as statutory verification
- [x] Planning rules/guidelines retain provenance links
- [x] No dummy, placeholder, fabricated or invented authoritative evidence

## 4. LCP / KM / Agent Enrichment
- [x] LCP intelligence path returns structured output
- [x] KM readiness path returns structured output
- [x] Bounded agents return deterministic structured synthesis
- [x] Parallel enrichment does not block the canonical assessment path

## 5. Browser / UI
- [x] Canonical workspace title and presentation surface pass
- [x] Layer drawer owns the live 25-layer catalogue
- [x] Layer state transitions are truthful (`OFF`, `LOADING`, `ON · RENDERED`, `ERROR`)
- [x] About route guard works
- [x] Deep browser functional smoke passes
- [x] Responsive / cross-browser checks pass where included by CI

## 6. Release / CI
- [x] Source gate green on the latest validated pre-repair head
- [x] Rule provenance gate green on the latest validated pre-repair head
- [x] Full regression green on the latest validated pre-repair head
- [ ] Runtime topology smoke green on the repaired head
- [ ] About functional smoke green on the repaired head
- [ ] Deep browser functional smoke green on the repaired head
- [ ] GIS preflight green on the repaired head
- [ ] 25-layer GIS render audit green on the repaired head
- [ ] Canonical release audit green on the repaired head

## 7. Release Discipline
- [x] No branch merge performed
- [x] No Render deployment performed unless explicitly requested
- [x] No architecture rewrite
- [x] No duplicate frontend/engine
- [x] No weakened assertions solely to obtain green CI

<!-- Final validation trigger: JMG targeted render repair 7b2d7395ffad06d31f4a76f55a35c388c6869919 -->