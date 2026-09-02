# MASTER-101 — GIS Lot Intelligence

URBION now has a GIS-ready contract for parcel/lot polygons and area metrics.

## Spatial output
- GeoJSON Polygon support with `[longitude, latitude]` coordinates.
- Lot number carried as explicit spatial metadata.
- Area shown in square metres and hectares when evidence is supplied.
- Missing area remains `EVIDENCE REQUIRED`; no geometry or area is fabricated.

## Championship direction
The next GIS layer can bind verified parcel geometry from PBT GIS / MelGIS / JUPEM evidence into the decision map, while preserving source and verification status.
