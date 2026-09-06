# MASTER-351 — Cross-Source Lot Identity

## Finding

URBION's earlier GIS work already established direct official PLANMalaysia S-CHARMs / i-Plan Melaka services for `GTsemasa_04`, `GTzoning_04`, `LOT_04` and `KONTUR5M_04`. The historical MASTER-277 integration also used official ArcGIS REST query/export services and parallel planning intelligence. This is reused rather than replaced.

## New lot-resolution chain

`site coordinate / lot number / UPI`
→ `PLANMalaysia i-Plan LOT_<state code>`
→ `live polygon + LOT + UPI + administrative identifiers + area`
→ `exact identity match / project-reference reconciliation`
→ `Planning Intelligence + map`
→ `JUPEM MyLot verification channel`

## Evidence boundary

`VERIFIED_CANDIDATE` means the requested lot identity matches an official public i-Plan feature. It does **not** mean URBION has legal cadastral authority.

JUPEM remains the cadastral verification authority/reference. MyLot is an online service for locating surveyed land lots and boundaries, while JUPEM also identifies eKadaster / MyGeoServe and cadastral products as official cadastral channels. URBION therefore does not scrape MyLot or invent an API that is not publicly documented.

## Cross-source reconciliation

- i-Plan LOT geometry: live official planning/GIS anchor.
- i-Plan current land use / zoning / committed: planning context.
- i-Plan DPFDN: flood, slope, landslide, seismic, fault, KSAS, CFS, protected area, river and catchment screening already present in the existing connector.
- MyGEMS: geology/geohazard context.
- JPS Public Infobanjir: hydrology portal context; direct geometry/API remains a separate integration boundary.
- JAS MyEQMS/EQMP: environmental monitoring source context; direct spatial API remains a separate integration boundary.
- MelGIS/PBT: retained as a source-discovery / reconciliation target unless a stable public geometry/query contract is demonstrated.
- Elysian: project reference only; existing reconciliation policy keeps official sources ahead of project-reference conflicts.

## User-facing behaviour

The map may show a real polygon when a live geometry source returns one. The right rail may report the lot identity and calculated spatial relationships. If a source is unavailable or cannot be reconciled, URBION exposes an evidence gap rather than fabricating a polygon or declaring statutory verification.
