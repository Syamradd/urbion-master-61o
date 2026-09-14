# URBION HORIZON — Data / AI / Planning Readiness Audit

**Branch:** `feature/canonical-workspace-v2`  
**Purpose:** judge-facing functional readiness of the canonical workspace without replacing the deterministic planning core.

## 1. Canonical evidence chain

`Case → Location → Spatial Evidence → Planning Rules → What-If → Decision Support → Output`

The canonical presentation is isolated as:

`workspace_v5.html → urbion_workspace_final.js → urbion_workspace_bridge.js → urbion_workspace_runtime.js`

## 2. Data domains traced in source

| Domain | Current source modules | Readiness | Boundary |
|---|---|---:|---|
| Guna Tanah | `urbion_workspace_final.js` | GREEN | PLANMalaysia GIS taxonomy, GT1→GT2→GT3 cascade |
| RT / deterministic rules | `urbion_rules.py`, `urbion_retrieval.py` | GREEN* | Current seeded RT MBMB rule set only |
| Applicability | `urbion_applicability.py` | GREEN* | Spatial/typology verification gates are explicit |
| Compliance | `urbion_compliance.py` | GREEN* | Deterministic comparison only for established rule IDs |
| GP / guideline intelligence | `urbion_guideline_intelligence.py` | GREEN* | Candidate references; adopted/local applicability still needs verification |
| Spatial / GIS | `urbion_spatial.py`, `urbion_spatial_intelligence.py`, `urbion_spatial_context.py`, GIS adapters | GREEN* | Depends on live/available spatial source response |
| i-Plan / planning source context | `urbion_iplan.py`, `urbion_planning_sources.py`, public-source modules | GREEN* | Source context is not statutory verification |
| Evidence ledger | `urbion_evidence.py`, `urbion_evidence_ledger.py`, `urbion_evidence_quality.py` | GREEN* | Evidence status remains distinct from calculated values |
| AI orchestration | `urbion_agent_api.py`, `urbion_agent_orchestrator.py`, `urbion_copilot.py` | GREEN* | Deterministic packet remains source of truth |
| LLM narrative | `urbion_llm_provider.py` | GREEN* | Optional Gemini narrative; no rule/approval authority |
| RAG / knowledge | `urbion_knowledge_orchestrator.py`, `urbion_retrieval.py` | AMBER→GREEN | Current implementation is bounded deterministic retrieval, not embedding/vector semantic search |
| LCP / development impact | `urbion_lcp_intelligence.py`, `urbion_development_impact.py` | GREEN* | Evidence-driven support layer |
| Environment / agency intelligence | `urbion_environment_intelligence.py`, multi-source adapters | GREEN* | Live source availability and source currency remain variable |

`* GREEN means the source/contract exists and is wired; it does not assert that every jurisdiction or every planning control is fully populated.`

## 3. AI / LLM / RAG operating model

### Deterministic layer
Rules, applicability, spatial calculations, compliance comparisons, evidence ledger and decision outputs are produced by the existing deterministic engines.

### Retrieval layer
`urbion_retrieval.py` selects candidate rules and `urbion_knowledge_orchestrator.py` builds a traceable source register. Retrieval is explicitly separated from statutory verification.

### LLM layer
`urbion_llm_provider.py` is optional and reads `GEMINI_API_KEY`. It is constrained to planner-facing narrative synthesis over the deterministic packet. It must not change score, ranking, approval, statutory status or source classification.

### Required judge interpretation
URBION is an evidence-backed decision-support system. It does **not** claim automatic statutory approval or legal compliance solely from an AI response.

## 4. Current RT / GP readiness

The seeded deterministic RT MBMB stack currently carries the established rule IDs:

- `RT-MBMB-2035-COM-01`
- `RT-MBMB-2035-COM-02`
- `RT-MBMB-2035-COM-03`
- `RT-MBMB-2035-COM-04`
- `RT-MBMB-2035-TOD-01`
- `RT-MBMB-2035-TOD-02`

Compliance comparisons are deterministic for these established controls. Other retrieved rules intentionally remain `REQUIRES REVIEW` until a deterministic comparison has been established.

The guideline catalogue intentionally returns `CANDIDATE_REVIEW` references. The system must not convert a generic PLANMalaysia guideline reference into an adopted local control without jurisdiction/source verification.

## 5. Map readiness

The presentation map supports:

- MAP / STREET
- SATELLITE
- HYBRID
- site selection / coordinates
- 400 m / 800 m / 1000 m context rings
- road / transit context
- layer catalogue from `/map/layers`
- WMS / TILE / ArcGIS MapServer layer rendering through the existing layer loader
- search / geocoding through Nominatim

The map is a spatial evidence interface, not a replacement for cadastral or statutory confirmation.

## 6. Button / interaction readiness

Critical judge-facing controls audited by browser automation include:

- GT1 / GT2 / GT3 cascade
- basemap switching
- context rings
- layer drawer
- Run Site Analysis
- Evidence
- What-If
- Decision
- Output
- theme toggle
- BM / EN toggle
- runtime Help / Sources / Status / About / Fullscreen / Reset utilities

The browser gate is the release proof for these controls.

## 7. Data-quality rules

1. No legacy `Perdagangan` option in the current GT taxonomy.
2. No hard-coded API credential pattern in the audited source gate.
3. Source context, calculated evidence, user-provided input and verification state remain distinct.
4. LLM narrative never becomes the authority for compliance.
5. Missing or stale external evidence must surface as review / uncertainty, not be silently promoted to verified.
6. Render stays LOCKED until browser and visual gates are green.

## 8. Remaining external-data gate

A source contract being present is not the same as proving that every external endpoint is currently available. Final release therefore requires the browser/runtime gate to demonstrate successful loading and graceful handling of live map/source responses, followed by visual inspection at the supported judge sizes.
