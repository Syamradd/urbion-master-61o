# URBION HORIZON — Final Repair Worklist

## Release objective
Close every verified blocker on the canonical branch without weakening assertions, inventing GIS data, changing decision authority, merging branches, or deploying Render.

## A. Authoritative GIS
- [x] Recover `urbion_wms_proxy.py` from the known-good canonical implementation after placeholder corruption.
- [x] Guard WMTS fallback when upstream returns `None`.
- [x] Align i-Plan WMS/WMTS/TMS fallback routing with the official GWC service surface.
- [x] Repair i-Plan Warisan render path; confirm browser regression no longer reports `iplan-heritage` as the blocker.
- [x] Confirm JMG Quarries has a healthy official MapServer/FeatureServer response path.
- [x] Add bounded Major Fault FeatureServer fallback and preserve official MapServer fallback.
- [x] Prove Major Fault failures are upstream-side: MapServer export, FeatureServer spatial query, `returnIdsOnly`, and `returnCountOnly` all timed out from CI probes.
- [ ] Obtain a successful authoritative Major Fault render/query within the browser regression budget, or document the external upstream outage/blocker with current evidence if the service remains unavailable.
- [ ] Re-run the 25-layer browser GIS regression and require 25/25 truthful `ON · RENDERED` states.
- [ ] Re-run the 14-layer authoritative i-Plan upstream/proxy preflight.

## B. Canonical application / planning workflow
- [x] Preserve canonical workspace and three-column presentation contract.
- [x] Preserve synchronous `/workstation/analysis` path and bounded enrichment.
- [x] Preserve deterministic What-If ranking.
- [x] Preserve `decision_authority = NONE`.
- [x] Preserve `statutory_verification = NOT_CLAIMED`.
- [ ] Final repaired-head regression audit.

## C. Evidence / provenance
- [x] Preserve evidence packets and provenance links.
- [x] Preserve cadastral as source-context only.
- [x] No placeholder, fabricated geometry, or dummy authoritative evidence introduced.
- [ ] Final rule-provenance gate on the final HEAD.

## D. Browser / UX / integrations
- [x] Runtime topology smoke passes on repaired code.
- [x] About smoke passes on repaired code.
- [x] P1–P6 browser contract sequence passes on the latest repaired-head run checked so far.
- [ ] Complete deep browser gate on final HEAD after the last cleanup commit.
- [ ] Complete MyEQMS / downstream integration tail on final HEAD.

## E. Release discipline
- [x] No branch merge.
- [x] No Render deployment.
- [x] No architecture rewrite.
- [x] No duplicate frontend/engine.
- [x] No weakened assertions to force green CI.
- [ ] Update `FINAL_BLOCKER_CHECKLIST.md` only after fresh final-head evidence is available.

## Verified current blocker
`mygems-faults` / JMG Major Fault is the only material GIS blocker still evidenced by direct upstream tests. Current JMG MapServer and FeatureServer endpoints are catalogued as official services, but the tested render/query paths are timing out from GitHub CI. The canonical implementation must not substitute fabricated geometry or falsely mark the layer rendered.
