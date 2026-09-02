# MASTER-166 — Live Frontend + i-Plan Source Upgrade

## Delivered

- Render service now serves `index.html` from the FastAPI root instead of exposing only the API response.
- `/index.html` uses the same live frontend contract.
- Frontend API routing is normalised to `location.origin` to remove stale Render-host assumptions.
- Root UI release identity is runtime-aligned to `PHASE-E.7`.
- Official PLANMalaysia i-Plan committed land-use WMS is wired for Melaka:
  `https://iplan.planmalaysia.gov.my/geoserver/iplan/wms`
  layer: `iplan:gunatanah_komited_04`.
- Added a visible i-Plan committed-land-use map control and thematic land-use explorer overlay.
- Added i-Plan hierarchy navigation for land use → activity → category, including commercial examples reflected by the official thematic-search workflow.
- Added regression tests for the live frontend contract and committed WMS contract.

## Evidence boundary

The committed layer is treated as official source context, not automatic statutory verification. Attribute-level filtering/querying may require the authorised i-Plan GeoServer workflow or portal/data-request route.

## Next attack surface

- Verify deployed `/` release identity after Render auto-deploy.
- Audit all workspace pages for stale release labels and same-origin API routing.
- Continue official-source integration for planning, cadastral, geology and environmental layers.
- Add stronger distinction between coordinate-derived screening and authoritative spatial verification without breaking deterministic demo fixtures.
