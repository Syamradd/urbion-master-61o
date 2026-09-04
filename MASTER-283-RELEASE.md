# MASTER-283 — Public Spatial Intelligence

## Scope
- Adds source-aligned Guna Tanah → Aktiviti → Kategori planning helper.
- Adds live public spatial queries around the active site for JMG MyGEMS Major Fault and Lithology, plus SCHARMS education, health and transport facilities.
- Adds map rendering of returned public features through the existing Leaflet workspace.
- Adds parallel site-intelligence execution and visible result counts.
- Preserves existing MASTER-282 public-source bridge, dashboard, LCP, What-If and Judge Mode surfaces.

## Evidence boundary
Public-source responses are displayed as source-context evidence. No response is represented as statutory approval or planning permission. Authoritative plans, guidelines and agency verification remain required for official decisions.

## Verified public service families
- PLANMalaysia / SCHARMS i-PLAN services
- JMG MyGEMS public ArcGIS FeatureServer services
- JPS station intelligence already exposed by the URBION gateway

## Deployment
- One atomic commit.
- GitHub CI must pass before production deployment.
- Render production is not changed by this commit.
