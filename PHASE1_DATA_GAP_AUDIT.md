# URBION HORIZON — Phase 1 Data Gap / Benchmark Audit

**Audit baseline:** `feature/canonical-workspace-v2` at `ab043127a55899a923608bc7cd240dbf29134600` before the Phase 1 worklist/contract commits.

## 1. Executive finding

URBION is functionally green, but the existing planning intelligence is more mature than the canonical assessment packet exposes. The main Phase 1 problem is **data convergence**, not missing technology.

Target:

`SITE IDENTITY → OFFICIAL SOURCE CONTEXT → CALCULATIONS → PLANNING POLICY → HAZARD / ENVIRONMENT → IMPACT → WHAT-IF → DECISION → LCP / KM / OSC`

All source observations remain qualified as decision-support context unless an authoritative verification state is explicitly established.

## 2. Historical vs current map catalogue

The earlier map catalogue included portal-reference entries for:

- JPS Public Infobanjir
- MyEQMS / EQMP
- JUPEM MyLot

The current map catalogue intentionally focuses on browser-renderable geometry-backed layers. The three portal-only sources should **not** be reintroduced as fake map overlays. They should return through a dedicated `LIVE EVIDENCE` / source-detail surface with availability, last-checked time and evidence state.

Current catalogue also contains additional geometry-backed context such as forest, coastal erosion, RMM and contour layers.

## 3. Current deterministic rule coverage

The seeded RT MBMB engine currently contains six established controls:

- `RT-MBMB-2035-COM-01` — Free-Standing Commercial plot ratio
- `RT-MBMB-2035-COM-02` — Perimeter planting
- `RT-MBMB-2035-COM-03` — Landscaped pedestrian walkway
- `RT-MBMB-2035-COM-04` — Shop-office building height
- `RT-MBMB-2035-TOD-01` — Terminal Sg. Udang TOD 400 m plot ratio
- `RT-MBMB-2035-TOD-02` — Terminal Sg. Udang TOD 800 m plot ratio

These rules are intentionally spatial/typology dependent and currently carry `PARTIALLY_TRACEABLE` provenance. Phase 1 must strengthen document edition/amendment, page/table/clause, effective status and spatial-condition metadata before expanding coverage.

## 4. Existing intelligence modules that are under-exposed by canonical assessment

The repository already contains separate capability for:

- i-Plan / DPFDN spatial context
- environmental and geohazard screening
- JPS live station/rainfall context
- JMG MyGEMS layers
- development-impact screening across physical/social/economic domains
- policy / SDG relationship graph
- guideline intelligence
- agency intelligence
- LCP orchestration
- KM readiness
- What-If / scenario ranking
- Decision Center

The key Phase 1 repair is to converge these into a canonical evidence envelope rather than build parallel engines.

## 5. Benchmark direction

PLANMalaysia's Manual GIS Rancangan Pemajuan Versi 3 (2025) emphasises standardised geospatial data, metadata, field structure, land-use classification, colour codes and geospatial quality control. PLANMalaysia's i-Plan description also emphasises collection, updating, verification, standardisation and storage of planning land-use data.

JMG identifies NaTSIS as a geospatial system for terrain, slope and geological-disaster information supporting planning and risk management.

JPS Public Infobanjir exposes rainfall, water-level and station status context and provides latest-update information; URBION must retain the provider timestamp and observation source rather than turn it into a direct site measurement claim.

## 6. Priority gaps

### P0 — must repair before premium presentation

1. Canonical evidence convergence.
2. Rule provenance/versioning.
3. First-class review gaps.
4. AI bounded to the canonical deterministic packet.

### P1 — strengthen decision quality

1. Cadastral identity reconciliation: project reference → i-Plan candidate → JUPEM verification state.
2. Environmental enrichment: flood / KSAS / slope / geohazard / seismic / river / catchment / ecology.
3. JPS rainfall + water-level context where machine-readable data is available.
4. MyEQMS/EQMP monitoring context where official machine-readable access is confirmed.
5. NaTSIS source path for terrain/slope/geological-disaster intelligence.
6. Mobility metrics distinguished as straight-line vs network vs walking.
7. Development-impact inputs and LCP-ready snapshot.
8. Controlled national policy / SDG references and recommendation grounding.
9. Dedicated Live Evidence surface for portal-only sources.

### P2 — only after P0/P1

Document-grounded RAG with exact source/page/clause references. Vector infrastructure is not required merely to score well; traceable retrieval is the priority.

## 7. Non-negotiable safety rules

- No geometry = no interactive map layer.
- No authoritative verification = no statutory verification claim.
- `NO_FEATURE` is not the same as `QUERY_ERROR`.
- Missing data becomes a review gap, not a fabricated value.
- Live observations remain source context.
- LLM output cannot change score, ranking, statutory status, approval status or rule classification.
- Existing deterministic planning engines remain the source of truth.
- Render remains locked until the explicit deployment instruction.
