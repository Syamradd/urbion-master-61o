# URBION HORIZON — World Benchmark Dashboard Gap Worklist

Status: `FINAL RELEASE GAP REGISTER` for `feature/championship-convergence-v1`.
Scope: distinguish release-critical convergence work from post-release benchmark enhancements without changing the deterministic planning engine or statutory boundary.

## Benchmark signal

| Capability | URBION HORIZON | ArcGIS Urban | Autodesk Forma | UrbanFootprint | OpenCities Planner |
|---|---|---|---|---|---|
| 2D GIS / live layers | Strong | Strong | Strong via ArcGIS | Strong | Strong |
| Parcel / zoning planning context | Strong foundation | Strong | Strong | Strong | Strong |
| Rule-aware scenario testing | Strong foundation | Strong | Strong | Strong | Moderate |
| 3D massing / buildable envelope | Gap | Strong | Strong | Strong | Strong |
| Multi-metric scenario comparison | Partial | Strong | Strong | Strong | Moderate |
| Existing-conditions dashboard | Partial | Strong | Moderate | Strong | Moderate |
| Population / jobs / housing impact | Partial | Strong | Strong | Strong | Moderate |
| Environmental simulation | Partial (risk screening) | Moderate | Strong | Strong resilience analytics | Strong |
| Evidence / provenance / review-gaps | **URBION differentiator** | Moderate | Moderate | Moderate | Moderate |
| Malaysian statutory-planning workflow | **URBION differentiator** | Generic / configurable | Generic | U.S.-focused | Generic |
| KM / OSC readiness | **URBION differentiator / early** | Limited direct fit | Limited direct fit | Limited direct fit | Limited direct fit |
| Public/stakeholder review | Basic | Strong | Strong | Moderate | Strong |
| Export / presentation | Good | Good | Strong | Strong | Strong |

## P0 — correctness before release

- [x] Plot ratio presentation uses planning convention `1 : X` while engine value remains numeric.
- [x] CI installs Chromium before browser contract smokes.
- [x] Decision Center convergence smoke exposes the canonical packet on successful decision builds and returns canonical errors on invalid input.
- [x] `URBION_ERROR_V1` canonical API/browser error envelope is enforced for request/downstream failures.
- [x] Displayed decision KPIs carry evidence-state/provenance through the canonical packet or are explicitly calculated.
- [x] Statutory boundary wording avoids implying authority approval; `NOT_CLAIMED` is preserved.
- [x] Production manifest points to `landing_server:app` and `/workspace`.
- [x] Final feature branch is at main parity (`behind_by=0` at audited candidate tree).
- [x] Regression, runtime, browser, Render-parity, UX and final command-centre gates passed on the audited candidate tree.

## P0 operational blocker — Render

- [ ] Reconcile existing `urbion-master-61o` service branch from `main` to the approved release branch/promotion target.
- [ ] Reconcile existing `urbion-master-61o` start command from `championship_server:app` to `landing_server:app`.
- [ ] Deploy only after final SHA is locked and live smoke passes.

This is a configuration drift issue in the existing Render service, not a planning-engine defect. No deployment is being triggered during this repair phase.

## P1 — benchmark/product gaps, not current release blockers

### A. Existing conditions / context

Improve with dense baseline metrics, source timestamp, parcel identity state, access indicators and environmental summary where authoritative data exists.

### B. Scenario comparison

Improve What-If into persistent `BASELINE | OPTION A | OPTION B` comparison with deltas and explicit trade-offs.

### C. 3D / development envelope

**Gap remains.** Future integration only; do not introduce a second 3D engine during the freeze.

### D. Metrics / indicators

Expand decision KPI families for capacity, access, environment, evidence quality and implementation readiness.

### E. Evidence & provenance

Current differentiator is implemented. Continue polishing source badges, timestamps, verification boundaries and review-gap categories.

### F. Planning rule explainer

Improve one-glance `RULE → APPLIES? → PROPOSED → REQUIREMENT → RESULT → SOURCE → NEXT ACTION` cards.

### G. KM / OSC implementation path

Current readiness path exists. Continue surfacing missing documents, agency review state, unresolved gaps and next submission action.

### H. Collaboration / stakeholder review

Future saved cases, comments, review notes, read-only share and feedback capture.

## P2 — visual / premium layer after release lock

- [x] GIS 25-layer regression coverage in canonical Browser Gate.
- [ ] persistent scenario timeline;
- [ ] cleaner map legend + layer provenance drawer;
- [ ] richer chart language;
- [ ] visual site card with parcel identity and source timestamp;
- [ ] presentation mode refinements;
- [ ] high-quality PDF/PNG/CSV export with source footer;
- [ ] optional 3D view after core 2D evidence flow is stable.

## P3 — advanced / later

- [ ] automatic layout generation / site automation;
- [ ] richer environmental simulation;
- [ ] citywide portfolio view;
- [ ] target tracking / plan monitoring;
- [ ] saved scenario history;
- [ ] enterprise GIS/BIM connectors.

## Judge-winning priority order

1. **Evidence-first executive dashboard** — implemented as the current differentiator.
2. **Persistent Baseline vs Alternatives** — next benchmark upgrade.
3. **Rule explainer** — next readability upgrade.
4. **KM/OSC readiness** — current signature path; deepen after release.
5. **Existing conditions metrics** — next data-density upgrade.
6. **3D / massing** — later, after decision data model remains stable.

## Architectural guardrail

Do not replace the canonical engine. Do not create parallel analysis logic. Dashboard improvements must consume the canonical evidence packet / deterministic assessment and keep `NOT_CLAIMED` statutory boundaries visible.
