# URBION HORIZON — Execution Worklist

## Phase 0 — Core Functional Gate
- [x] Workspace route / title / map boot
- [x] Canonical script ownership and duplicate-DOM guards
- [x] State → District → Mukim hierarchy
- [x] Local Authority canonical select
- [x] Single frontend PBT catalogue owner
- [x] Full 16-state/territory PBT catalogue exposed
- [x] GT1 → GT2 → GT3 taxonomy cascade
- [x] Street / Satellite / Hybrid basemap switching
- [x] 25/25 mandatory live GIS layers rendered in Browser Gate checkpoint
- [x] Map click coordinate update
- [x] Readiness fixture + Run Site Analysis gate
- [x] Analysis Complete + deterministic result state
- [x] AI / Copilot response path
- [x] Evidence modal
- [x] What-If exactly-once request
- [x] Decision center
- [x] Output generation / print
- [x] Utility buttons / theme / language / responsive checks
- [x] Browser Gate GREEN — run 149 / commit `ab043127a55899a923608bc7cd240dbf29134600`

## Phase 1 — Data / Decision Integrity (CURRENT)
Principle: **do not rewrite the deterministic engine; converge existing intelligence into one evidence-backed canonical site packet.**

### P0 — Canonical evidence convergence
- [x] Define canonical evidence-packet contract: site identity → source context → calculations → policy → risks → decision → review gaps
- [x] Assessment presentation surface now attaches the canonical packet and converges existing site / policy / evidence-intelligence fields; external station / LCP enrichment remains pending
- [x] Preserve evidence states: `USER_PROVIDED` · `CALCULATED` · `SOURCE_CONTEXT` · `VERIFIED` · `UNVERIFIED`
- [ ] Make `review_gaps` first-class and visible in downstream Decision / Evidence surfaces
- [ ] Ensure AI/Copilot can only explain the canonical deterministic packet
- [x] Add packet-contract tests and a live `/assess` integration smoke; downstream UI consistency remains pending until CI verification

### P0 — Planning-rule provenance hardening
- [ ] Audit every RT / GP rule for document title, edition/amendment, page/table/clause, spatial condition and traceability
- [ ] Resolve current RT MBMB amendment/version status before treating a control as current
- [ ] Expand only high-value deterministic controls first; target ~15–25 decision-relevant controls, not a bloated rule database
- [ ] Keep unsupported controls as `REQUIRES REVIEW`; never invent local standards
- [ ] Add provenance freshness / source-status fields without overstating verification

### P1 — Cadastral / site identity
- [ ] Reconcile project-reference / i-Plan LOT / JUPEM MyLot identity chain
- [ ] Expose `PROJECT_REFERENCE → i-Plan CANDIDATE → JUPEM VERIFICATION` states
- [ ] Never claim statutory cadastral verification from i-Plan or MyLot portal visibility alone

### P1 — Environmental / hazard enrichment
- [ ] Promote existing i-Plan/DPFDN flood, KSAS, slope, geohazard, seismic, river, catchment and ecology context into the canonical packet
- [ ] Add JPS rainfall + water-level observations with timestamp, station, distance and alert thresholds where machine-readable data is available
- [ ] Add JAS MyEQMS/EQMP station context where an official machine-readable route is confirmed
- [ ] Add JMG NaTSIS as the preferred future terrain/slope/geological-disaster source where access is available
- [ ] Keep all live-source failures as `QUERY_ERROR` / `EVIDENCE_GAP`; never fabricate values

### P1 — Mobility / TOD
- [ ] Preserve current Haversine screening as explicit straight-line distance
- [ ] Add nearest verified station / network evidence
- [ ] Add network/walking distance only when real network geometry exists
- [ ] Distinguish `straight_line`, `network`, and `walking` metrics in evidence metadata

### P1 — Development impact / LCP
- [ ] Connect existing physical / social / economic impact engine to canonical site evidence
- [ ] Collect only explicit inputs for units, site area, GFA, jobs, population, trips and facility access
- [ ] Surface missing inputs as review gaps, not estimated facts
- [ ] Strengthen LCP-ready snapshot: site, impacts, policy, agencies, environment, recommendations and KM/OSC readiness

### P1 — Policy / guideline / SDG grounding
- [ ] Seed a controlled national policy reference catalogue (RFN4 / DPN2 / DPFDN / SDG) with provenance
- [ ] Keep local applicability as `CANDIDATE_REVIEW` until verified
- [ ] Expand guideline catalogue only with source-backed references
- [ ] Ensure recommendation grounding traces `IMPACT → ISSUE → POLICY → STRATEGY → SDG → EVIDENCE`

### P1 — Restore lost evidence UX without fake map layers
- [ ] Add dedicated `LIVE EVIDENCE` surface for JPS Public Infobanjir, MyEQMS/EQMP and JUPEM MyLot
- [x] Do **not** re-add portal-only sources to interactive map layers
- [ ] Show source type, last checked, availability, evidence state and action/open-source link where appropriate

### P2 — RAG / AI quality
- [ ] Prefer document-grounded retrieval with exact source/page/clause references before introducing vector infrastructure
- [ ] Keep LLM as explanation/synthesis only; no rule, score, approval or statutory-status authority

### Phase 1 Exit Gate
- [ ] One canonical site packet feeds Assess / Evidence / What-If / Decision / Output
- [ ] Every decision-relevant rule has traceable provenance or explicit review status
- [ ] Cadastral, environment, mobility and LCP evidence states are explicit
- [ ] No unsupported source is presented as verified
- [ ] AI narrative is demonstrably bounded by deterministic evidence
- [ ] Phase 1 integrity tests GREEN

## Phase 2 — Judge UX / Journey
- [ ] First 10-second comprehension
- [ ] Map storytelling
- [ ] Evidence storytelling
- [ ] What-If storytelling
- [ ] Decision Center hierarchy
- [ ] Planner Review / KM / OSC transition
- [ ] Remove dead-end or orphaned surfaces

## Phase 3 — Premium Visual / Responsive Polish
- [ ] Visual hierarchy
- [ ] Typography / spacing
- [ ] Data-density balance
- [ ] Motion / state transitions
- [ ] Responsive visual QA
- [ ] Judge-facing cinematic moments

## Phase 4 — Demo Scenario / Presentation Logic
- [ ] Primary judge case
- [ ] Problem → URBION → Assess → Evidence → What-If → Decide → Planner Review
- [ ] 90–120 second live walkthrough
- [ ] Final slide / narrative alignment

## Phase 5 — Cinematic AI Video
- [ ] Google Flow AI visuals
- [ ] Screen recording
- [ ] AI voice-over
- [ ] Music / SFX
- [ ] 2:00–2:20 final cut

## Phase 6 — Final Release / Deployment
- [ ] Final functional QA
- [ ] Final data/provenance QA
- [ ] Final visual QA
- [ ] Final judge-path QA
- [ ] Final release identity / freeze
- [ ] Live smoke after deployment

## Deployment Lock
- **NO Render deployment during functional development.**
- Deploy only after explicit `DEPLOY RENDER NOW` instruction.
