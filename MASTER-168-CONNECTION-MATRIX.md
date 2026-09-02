# MASTER-168 — URBION Connection Matrix

## Live / queryable spatial context
- **PLANMalaysia i-Plan** — ArcGIS REST for current land use, zoning, cadastral and contours; official GeoServer WMS for committed land use and additional planning/hazard/environment layers.
- **JMG MyGEMS** — public ArcGIS services for major faults, mines/quarries, groundwater, geoheritage/geopark, lithology, seismic and mineral-resource context.

## Public portal / controlled workflow
- **JUPEM MyLot** — surveyed-lot location/boundary reference. Do not treat portal visibility as cadastral verification.
- **PLANMalaysia Melaka Geospatial** — state planning GIS/data service and AOI information workflow.
- **PLANMalaysia MyPLAN** — national planning documents, publications and GIS manuals.
- **OSC 3.0 Plus Online** — development-control / Kebenaran Merancang workflow context, technical review and status workflow. Authentication/PBT access rules remain external.
- **JAS MyEQMS / EQMP** — environmental monitoring context for air, river-water and marine-water data; detailed dataset access follows the official data-access route.

## Project-reference reconciliation
- **Elysian GIS** remains a traceable historical/project reference. It is explicitly separated from authoritative source context. Conflicts are surfaced rather than silently merged.

## Decision boundary
URBION may calculate, screen, compare, rank and explain planning scenarios. A live endpoint or successful query is **not** automatically a statutory verification. The system must expose evidence state and source provenance for every decision-critical claim.

## Next integration targets
1. Adaptive i-Plan field/taxonomy normalisation for current land use → activity → category → RT class.
2. Elysian ↔ i-Plan ↔ JUPEM lot reconciliation with area/lot/mukim mismatch flags.
3. WMS layer identify/legend/opacity controls for hazard, KSAS, ecology, heritage and committed land use.
4. JAS station/data provenance workflow with timestamp and confidence.
5. OSC/KM readiness graph: category → core documents → technical agencies → review blockers → escalation.
6. Statutory-plan evidence graph: RFN/RSN/RT/RKK/GPP with document/page/source provenance.
7. Spatial verification states: USER_PROVIDED → CALCULATED → SOURCE_CONTEXT → SOURCE_CONFIRMED → VERIFIED, never implicit promotion.
8. Automated regression suite for source availability, stale-source detection and unsafe “verified” language.
