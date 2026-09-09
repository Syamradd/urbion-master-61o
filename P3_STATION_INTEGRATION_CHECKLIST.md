# URBION HORIZON — P3 Station Integration Gate

## Purpose
Define the safe integration contract for JPS / JAS station intelligence before any live adapter is allowed into the canonical workflow.

## Evidence rules
- `VERIFIED` requires an authoritative response with a timestamp and identifiable station/source.
- `SOURCE_CONTEXT` is allowed for public GIS/service context but is not a verified reading.
- `UNVERIFIED` / `EVIDENCE_GAP` must remain visible to the planner.
- No adapter may fabricate a reading, station geometry, warning state, freshness value, or statutory conclusion.

## Adapter contract
A station adapter must return zero or more records containing:
- `name`
- `station_id`
- `lat`, `lon`
- optional `reading`
- optional `last_updated`
- `source`
- `evidence_state`

The station engine may calculate site-to-station distance and freshness only from supplied coordinates/timestamps.

## Source boundaries
- JPS Public Infobanjir: portal/reference until a verified machine-query contract is established.
- JAS MyEQMS/APIMS: public environmental monitoring source; machine-query use must be verified before treating values as live evidence.
- JMG MyGEMS: spatial source context can be queried where the registered public service supports it.

## Release gate
1. Adapter contract test passes.
2. Invalid/missing geometry produces a review gap.
3. Missing query configuration produces `LIVE_QUERY_NOT_CONFIGURED`.
4. Query failure is surfaced, never converted to a reading.
5. Freshness is derived only from supplied timestamps.
6. Canonical shell/server is untouched until integration review.
7. Browser QA confirms state labels and source provenance.
8. Render verification confirms the production path before release.
