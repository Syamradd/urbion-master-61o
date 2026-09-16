# URBION HORIZON — Final Blocker Checklist

## 1. Authoritative GIS
- [ ] 14-layer authoritative i-Plan upstream preflight passes on current release HEAD
- [ ] 14-layer canonical `/map/wms` proxy preflight passes on current release HEAD
- [ ] 25 canonical layer IDs hydrate in the workspace
- [ ] 25/25 layers render as `ON · RENDERED`
- [x] i-Plan cached fallbacks remain authoritative (TMS/WMTS/WMS/official ArcGIS only)
- [x] JMG Major Fault / Quarries use official MapServer/FeatureServer paths
- [x] Cadastral remains authoritative source-context only; no fabricated parcel geometry
- [x] JMG/i-Plan GIS surgical repair applied without fake geometry (`67e9055`)
- [x] GIS preflight path aligned with the canonical fallback path (`31a502a`)

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
- [x] Welcome page and About Us visual surfaces intentionally frozen; no logo/background changes in final hardening
- [x] Core browser contract/evidence suite has passed on prior clean validation
- [ ] Deep browser functional smoke passes on current post-repair HEAD
- [ ] 25-layer GIS browser regression passes on current post-repair HEAD

## 6. Release / CI
- [x] Source/full regression gates have passed on repaired lineage
- [ ] Runtime topology smoke green on current post-repair HEAD
- [ ] About functional smoke green on current post-repair HEAD
- [ ] Deep browser functional smoke green on current post-repair HEAD
- [ ] GIS preflight green on current post-repair HEAD
- [ ] 25-layer GIS render audit green on current post-repair HEAD
- [ ] Canonical release audit green on current post-repair HEAD

## 7. Release Discipline
- [x] No branch merge performed
- [x] No Render deployment performed unless explicitly requested
- [x] No architecture rewrite
- [x] No duplicate frontend/engine
- [x] No weakened assertions solely to obtain green CI

## 8. Current Worklist
- P0 — Revalidate current HEAD end-to-end through the real release/browser gates after GIS opacity persistence repair.
- P1 — If GIS still fails, identify exact layer/route evidence; repair only the verified source/runtime defect, never add speculative endpoints.
- P1 — Exercise re-analysis stale-state paths for AI, LCP, Decision Story, What-If and live station markers.
- P2 — Preserve strict GIS render assertions; improve only bounded synchronization/event-driven waits when a race is proven.
- P3 — Close only when strict 14-layer preflight, strict 25/25 render, browser gate, and release audit are all green on the same HEAD.

<!-- Welcome/About intentionally frozen. Current validation trigger: final-head GIS + stale-state hardening -->
