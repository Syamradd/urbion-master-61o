# MASTER-280 — Professional Planning Data Workspace

## Purpose
- Add an i-PLAN-style Planning Data workspace without replacing the MASTER-276/279 primary dashboard.
- Provide a live point query against official Melaka GTsemasa_04.
- Drive Guna Tanah Semasa → Aktiviti → Kategori as cascading planning inputs.
- Expose live i-PLAN current land use, zoning, cadastral and 5m contour map layers.
- Surface JPS Public Infobanjir and JMG MyGEMS as named evidence sources, with URBION environment checking where connected.
- Keep source-context and statutory guardrails explicit.

## Evidence boundary
- Official i-PLAN point-query fields are source context.
- Activity/category options are URBION planning taxonomy aligned to the i-PLAN workflow; they are not statutory approvals.
- JPS and MyGEMS remain authoritative external sources unless a public machine-readable layer is explicitly confirmed and connected.
- No statutory approval is inferred.

## Release discipline
- One atomic commit.
- Render is not changed by this commit.
