# URBION HORIZON — GIS Capability Matrix

## Rule

**NO GEOMETRY = NO MAP LAYER.**

A source may be registered without being queryable. A rendered map layer is not automatically decision-safe evidence. URBION keeps `SOURCE_CONTEXT`, `CALCULATED`, `USER_PROVIDED`, `EVIDENCE_GAP` and authoritative verification separate.

## Current implementation

| Layer / source | Geometry route | Render | Site query | Spatial relationship | Decision-safe |
|---|---|---:|---:|---:|---:|
| i-Plan Current Land Use | GeoServer WMS + WFS | YES | YES | YES | NO — source context |
| i-Plan Zoning | GeoServer WMS + WFS | YES | YES | YES | NO — source context |
| i-Plan Committed Land Use | GeoServer WMS + WFS | YES | YES | YES | NO — source context |
| i-Plan Cadastral Parcels | iPLAN ArcGIS REST Feature Layer (`LOT_XX`) | YES | YES | YES | NO — source context |
| i-Plan Flood | GeoServer WMS + WFS | YES | YES* | YES* | NO — source context |
| i-Plan Disaster Risk | GeoServer WMS + WFS | YES | YES* | YES* | NO — source context |
| i-Plan KSAS | GeoServer WMS + WFS | YES | YES* | YES* | NO — source context |
| i-Plan CFS / Ecological Network | GeoServer WMS + WFS | YES | YES* | YES* | NO — source context |
| i-Plan Heritage | GeoServer WMS + WFS | YES | YES* | YES* | NO — source context |
| i-Plan RFN / Topography | GeoServer WMS + WFS | YES | YES* | YES* | NO — source context |
| JMG MyGEMS Lithology | ArcGIS REST feature query | YES | YES | YES | NO — source context |
| JMG MyGEMS Major Faults | ArcGIS REST feature query | YES | YES | YES | NO — source context |
| JMG MyGEMS Quarries | ArcGIS REST feature query | YES | YES | YES | NO — source context |
| JMG MyGEMS Groundwater | ArcGIS REST feature query | YES | YES | YES | NO — source context |
| JMG MyGEMS Geoheritage | ArcGIS REST feature query | YES | YES | YES | NO — source context |
| JUPEM MyLot | Public portal | REF | NO direct geometry claim | NO | NO |
| PBT GIS / MelGIS | Public portal / discovered architecture | REF | NO direct live query claim | NO | NO |
| JPS Public Infobanjir | Public portal | REF | NO direct API claim | NO | NO |
| JAS MyEQMS / EQMP | Public portal | REF | NO direct live geometry claim | NO | NO |
| Elysian legacy GIS | Project reference | REF | NO automatic authoritative claim | NO | NO |

`*` The connector attempts the configured public query and returns `QUERY_ERROR` / `EVIDENCE_GAP` when the service does not provide a usable feature response. It never fabricates geometry.

## Architecture

1. `urbion_data_sources.py` — source and visual layer registry.
2. `urbion_spatial_context.py` — parallel WFS / ArcGIS geometry query engine.
3. `urbion_spatial_context_api.py` — `/spatial/site-context` endpoint, including the explicit iPLAN cadastral bridge.
4. `urbion_cadastral_context.py` — state-aware iPLAN `LOT_XX` ArcGIS parcel query adapter.
5. `urbion_spatial_context_upgrade.js` — renders returned GeoJSON on the existing Leaflet map.
6. `urbion_spatial_context_intelligence_bridge.js` — binds live GIS hits to the V5 Planning Intelligence rail.
7. `urbion_spatial_context_engine_bridge.js` — feeds the live context into the existing deterministic `/spatial/intelligence` engine.
8. `urbion_map_identify_runtime.js` — multi-layer identify, source/evidence detail, and cadastral parcel highlighting.
9. Existing `urbion_spatial_intelligence.py` — retains the final spatial decision-support model and its statutory disclaimer.

## Site-centric outputs

For each queried layer URBION can expose:

- feature count within the screening radius;
- whether the site point falls inside a returned polygon;
- nearest geometry distance for supported line / polygon / point geometry;
- source name and query mode;
- source-context state;
- selected source attributes in the map popup;
- explicit evidence gaps when the source cannot be queried.

## Planned / not claimed yet

- authoritative JUPEM parcel geometry resolution;
- live MelGIS / PBT parcel query;
- direct JPS flood-service geometry integration;
- direct MyEQMS spatial monitoring geometry;
- reconciliation of Elysian geometry against authoritative cadastral/planning geometry;
- walking-network distance and multimodal accessibility from a verified transport network.

These remain integration targets, not hidden assumptions.
