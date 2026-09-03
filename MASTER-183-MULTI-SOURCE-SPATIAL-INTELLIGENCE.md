# MASTER-183 — Multi-Source Spatial Intelligence

## Objective
Connect the existing national geospatial source inventory into an explicit spatial-intelligence contract without fabricating unavailable measurements or treating portal availability as statutory verification.

## Source matrix
| Domain | Source | Current capability | Safe decision role |
|---|---|---|---|
| Land use | PLANMalaysia i-Plan | Current land use, zoning, committed WMS | Source context |
| Terrain | i-Plan | 5m contours + topography layer | Source context; derive terrain metrics only from returned geometry |
| Flood | i-Plan + JPS Public Infobanjir | Flood/disaster layers + public hydrology portal | Hazard/source context |
| Environment | JAS MyEQMS/EQMP | Monitoring portal | Environmental source context |
| Cadastral | i-Plan + JUPEM MyLot | Lot query + public lot reference | Parcel/source context |
| Geology | JMG MyGEMS | Faults, lithology, groundwater, seismic, mines/quarries, minerals, geoheritage | Geohazard/source context |
| Ecology | i-Plan | CFS, ecological network, KSAS | Environmental/ecological context |
| Heritage | i-Plan | Heritage layer | Heritage context |
| Access | OpenStreetMap | Basemap/road context | Access context; network metrics require explicit network data |

## Analytical boundary
The next implementation may calculate a metric only when the required geometry/data is actually returned. Portal-only sources remain explicit `SOURCE_CONTEXT` and must not silently become numeric scores. Missing/live-query failures become review gaps.

## Priority analytics
1. Site-to-road/access context.
2. Terrain elevation/contour and slope derivation where geometry supports it.
3. Flood exposure flag from spatial hazard context.
4. Environmental monitoring proximity/context where official station data is available.
5. Geohazard screening from MyGEMS layers.
6. Cadastral reconciliation between i-Plan, JUPEM and project reference.
7. Composite spatial-risk/opportunity summary feeding Evidence → Decision, without replacing statutory planning rules.

## Required evidence states
`USER_PROVIDED` · `CALCULATED` · `SOURCE_CONTEXT` · `VERIFIED` · `UNVERIFIED`.

## Guardrail
URBION is planning decision support. Spatial intelligence is a screening aid, not a survey, engineering certification, environmental approval, flood guarantee, cadastral determination, or statutory planning approval.
