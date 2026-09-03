# MASTER-184 — Live Station Intelligence

## Goal
Turn a selected development site into an LCP-ready observation snapshot by finding nearby official monitoring stations and exposing their latest available readings with distance, timestamp and provenance.

## Current live adapter
- **JPS Public Infobanjir:** public rainfall table + station information; nearest stations are ranked by haversine distance.
- **DOE APIMS:** adapter accepts a configured authorised/public JSON endpoint; without one, URBION explicitly reports `SOURCE_CONTEXT` and does not invent API/IPU values.

## LCP observation fields
`station_name` · `station_id` · `distance_m` · `reading` · `unit` · `timestamp` · `status` · `source` · `evidence`.

## Planned expansion
The same station-selection contract can be extended to water level, stream flow, air quality, noise and other official monitoring datasets when their public/authorised machine-readable feeds are confirmed. Each provider must preserve source timestamp and evidence state.

## Safety boundary
A live observation is not a statutory determination, engineering certification, environmental approval, flood guarantee or planning approval. Provider outages and stale readings are surfaced as unavailable/context rather than silently scored.

## Endpoint
`GET /stations/nearby?site_lat=...&site_lon=...&state=Melaka&limit=5`
