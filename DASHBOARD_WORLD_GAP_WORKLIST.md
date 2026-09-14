# URBION HORIZON — World Benchmark Dashboard Gap Worklist

Status: active working list for `feature/canonical-workspace-v2`.
Scope: improve the judge-facing planning dashboard without changing the deterministic planning engine or statutory boundary.

## Benchmark signal

| Capability | URBION HORIZON | ArcGIS Urban | Autodesk Forma | UrbanFootprint | OpenCities Planner |
|---|---|---|---|---|---|
| 2D GIS / live layers | Strong | Strong | Strong via ArcGIS | Strong | Strong |
| Parcel / zoning planning context | Strong foundation | Strong | Strong | Strong | Strong |
| Rule-aware scenario testing | Partial | Strong | Strong | Strong | Moderate |
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

## P0 — repair / correctness before visual expansion

- [x] Plot ratio presentation uses planning convention `1 : X` while engine value remains numeric.
- [x] CI installs Chromium before browser contract smokes.
- [ ] Fix decision-center convergence smoke so the `/decision-center` response always exposes the canonical packet when the underlying decision build succeeds.
- [ ] Add a single canonical error envelope for browser/API failures.
- [ ] Verify every displayed KPI has an explicit source/evidence state or is clearly marked calculated.
- [ ] Eliminate any UI wording that can be mistaken for statutory approval.

## P1 — biggest dashboard gaps

### A. EXISTING CONDITIONS / CONTEXT
Current gap: dashboard is assessment-centric, but world-class planning products first establish baseline conditions with dense, queryable metrics.

Add to right rail / Evidence:
- population / households / jobs where authoritative data is available;
- land-use mix and area by category;
- key transport/access indicators;
- environmental/risk summary;
- parcel/cadastral identity state;
- timestamp and source per metric.

### B. SCENARIO COMPARISON
Current gap: What-If is present, but the main dashboard does not visually compare baseline vs alternatives as a persistent decision surface.

Add:
- `BASELINE | OPTION A | OPTION B` comparison strip;
- plot ratio, height, GFA, units, population/jobs, transport, environment and evidence coverage columns;
- delta arrows and explicit trade-off labels;
- best candidate only as a recommendation, never as an authority decision.

### C. 3D / DEVELOPMENT ENVELOPE
Current gap: URBION is visually map-first and rule-first, while leading planning platforms connect regulation directly to a 3D buildable envelope.

Add later:
- parcel/building massing preview;
- maximum/indicative envelope;
- height and floor-area visualization;
- scenario slider;
- simple camera/presentation mode.

Do not build a new 3D engine during the current freeze; first create a clean integration boundary for future massing.

### D. METRICS / INDICATORS
Current gap: URBION has readiness and evidence counts, but fewer decision KPIs than mature planning products.

Target metric families:
- development intensity: plot ratio, GFA, height, site area;
- capacity: units, population, jobs;
- access: TOD distance, road/transit access;
- environment: flood/risk indicators, live-query status;
- evidence: verified/source-context/unverified/review gaps;
- implementation: KM/OSC readiness.

### E. EVIDENCE & PROVENANCE — TURN DIFFERENTIATOR INTO HERO FEATURE
Current strength: canonical evidence packet, source context, review gaps, cadastral boundary, live environment/mobility evidence.

Improve presentation:
- every metric gets a compact source badge;
- `VERIFIED / SOURCE CONTEXT / CALCULATED / USER PROVIDED / UNVERIFIED` as visible status chips;
- click metric → source, timestamp, locator, verification boundary;
- classify gaps as `INPUT`, `SOURCE`, `VERIFICATION`, `BLOCKER`;
- show why a metric affects the decision.

### F. PLANNING RULE EXPLAINER
Current gap: rules appear as result rows, but the planner still has to interpret applicability.

Add a compact rule card:
`RULE → APPLIES? → PROPOSED → REQUIREMENT → RESULT → SOURCE → NEXT ACTION`

For plot ratio specifically:
`PROPOSED 1 : 4.5` vs `CONTROL 1 : 4.0` rather than displaying bare decimals.

### G. KM / OSC IMPLEMENTATION PATH
Current gap: most benchmark platforms stop at planning/design/scenario analysis.

Make URBION's downstream workflow a signature path:
`ASSESS → EVIDENCE → WHAT-IF → DECIDE → PLANNER REVIEW → KM READINESS → OSC PACKAGE`

Surface:
- missing submission documents;
- technical agency review state;
- unresolved evidence gaps;
- readiness score;
- next submission action.

### H. COLLABORATION / STAKEHOLDER REVIEW
Current gap: core workspace is primarily single-user.

Future:
- saved cases;
- scenario comments;
- review notes;
- shareable read-only view;
- stakeholder feedback capture.

## P2 — visual / premium layer

- [x] GIS 25-layer regression coverage added to canonical Browser Gate.
- [ ] persistent scenario timeline;
- [ ] cleaner map legend + layer provenance drawer;
- [ ] richer chart language (distribution, delta, small multiples);
- [ ] visual site card with parcel identity and source timestamp;
- [ ] presentation mode for judges;
- [ ] high-quality PDF/PNG/CSV export with source footer;
- [ ] optional 3D view after core 2D evidence flow is stable.

## P3 — advanced / later
- [ ] automatic layout generation / site automation;
- [ ] richer environmental simulation (sun, wind, noise, microclimate);
- [ ] citywide portfolio view;
- [ ] target tracking / plan monitoring;
- [ ] saved scenario history;
- [ ] API/import/export connectors for enterprise GIS/BIM.

## Judge-winning priority order

1. **Evidence-first executive dashboard** — make provenance visible without opening a modal.
2. **Persistent Baseline vs Alternatives** — turn What-If into a decision comparison surface.
3. **Rule explainer** — make every planning control readable in one glance.
4. **KM/OSC readiness** — connect planning intelligence to an actual Malaysian workflow.
5. **Existing conditions metrics** — make the site feel understood before the verdict.
6. **3D / massing** — high visual impact, but only after the decision data model is stable.

## Architectural guardrail

Do not replace the canonical engine. Do not create parallel analysis logic. Dashboard improvements must consume the canonical evidence packet / deterministic assessment and keep `NOT_CLAIMED` statutory boundaries visible.
