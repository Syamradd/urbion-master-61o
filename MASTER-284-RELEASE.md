# MASTER-284 — Unified Site Intelligence

## Scope
- Adds one-click site intelligence orchestration across i-PLAN current land use, zoning, cadastral, JMG fault/lithology, JPS station intelligence and championship health.
- Shows actual returned feature counts/statuses before downstream decision handoff.
- Adds direct evidence-chain build from the existing public-source bridge.
- Preserves MASTER-283 classification, public GIS feature layers, What-If, Decision Centre, LCP and Judge Mode.

## Safety / evidence boundary
- Public GIS results are source-context evidence; calculated outputs remain calculated.
- No source response is represented as statutory approval or planning permission.
- External ArcGIS browser access remains dependent on source CORS/runtime behaviour.

## Deployment
- One atomic commit.
- GitHub CI must pass before production deployment.
- Render production is not changed by this commit.