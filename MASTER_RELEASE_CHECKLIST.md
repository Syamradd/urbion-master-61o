# URBION HORIZON — MASTER RELEASE + DASHBOARD REPAIR CHECKLIST

Status: `DASHBOARD REPAIR INTEGRATED / FRESH VALIDATION REQUIRED`

Canonical branch: `feature/canonical-workspace-v2`
Canonical app: `landing_server:app`
Canonical workspace: `/workspace` → `workspace_v5.html`
Render target: `urbion-horizon-workspace-v4` (`srv-dahm749594qs73fk2tag`)
Render auto-deploy: OFF

## 1. Non-negotiable architecture

- [x] Single canonical V5 Planning Workspace.
- [x] Single deterministic planning engine contract: `PHASE-E.8`.
- [x] Single evidence contract: `PHASE1.2`.
- [x] Single browser/API error contract: `URBION_ERROR_V1`.
- [x] No second planning/scoring engine introduced.
- [x] `workspace_v4_server.py` remains a compatibility launcher only.
- [x] Statutory verification remains `NOT_CLAIMED`.
- [x] Decision authority remains `NONE`.
- [x] GIS source context is not represented as statutory verification.

## 2. Laptop-night repair requirements recovered from the missing chat

### A — Explain URBION before asking the viewer to interact

- [x] Dashboard now has an explicit URBION introduction layer.
- [x] Introduction explains what URBION is.
- [x] Introduction explains the core objective: connect fragmented planning inputs into an evidence-aware, traceable workflow.
- [x] Introduction exposes the main capabilities: GIS, site analysis, planning rules/policy, development impact, AI-assisted narrative, What-If and Decision Center.
- [x] Introduction explains the output: explainable findings, evidence trace, review gaps and planner handoff.
- [x] Statutory boundary is visible in the introduction.

### B — Connect the dashboard into one planning story

- [x] Visible workflow: `SITE → SPATIAL → EVIDENCE → ASSESS → WHAT-IF → DECIDE`.
- [x] One-click entry points for Site Analysis, Evidence, What-If and Decision Center.
- [x] Existing canonical owners/functions are reused rather than duplicated.
- [x] Existing GIS map remains the spatial evidence surface.
- [x] Existing canonical evidence packet remains the source of truth after analysis.
- [x] Existing Decision Center remains the decision-support endpoint.
- [x] Existing Output / planner handoff remains preserved.

### C — Make the dashboard visibly substantive

- [x] Canonical live/demo case context is shown without fabricating evidence.
- [x] Deterministic demo scenario catalogue is surfaced from `/demo-scenarios`.
- [x] Existing Development Impact surface remains connected to the canonical packet.
- [x] Existing Decision Story / Live Evidence Story / Review Gaps owners remain active.
- [x] GIS layer catalogue and layer states remain visible.
- [x] Road Intelligence remains connected to live source context where available.
- [x] Evidence states remain explicit: `USER_PROVIDED`, `CALCULATED`, `SOURCE_CONTEXT`, `VERIFIED`, `UNVERIFIED`.

## 3. Existing deep repair work — preserved

- [x] Legacy Yes/No planning inputs no longer hard-fail assessment.
- [x] Workstation development inputs propagate into canonical proposal/evidence data.
- [x] GFA + plot ratio transparent site-area calculation path preserved.
- [x] Development Impact explicit-input/review-required boundary preserved.
- [x] i-Plan WMS same-origin proxy preserved.
- [x] Critical Melaka Current Land Use / Zoning ArcGIS routing preserved.
- [x] ArcGIS same-origin proxy preserved.
- [x] Leaflet imagery z-order hardening preserved.
- [x] GIS layer controls + opacity + explicit loading/render/error states preserved.
- [x] JMG Major Fault MapServer + FeatureServer fallback preserved.
- [x] Road Intelligence Overpass fallback and map-coordinate context preserved.
- [x] KM / OSC readiness path preserved.
- [x] Bounded Copilot narrative preserved.
- [x] Canonical About visual master serving repaired.
- [x] Development Impact UI asset serving repaired without reintroducing the app import cycle.

## 4. Current dashboard repair implementation

- [x] Added `urbion_workspace_demo_command_layer.js` as a presentation-only layer.
- [x] Added explicit URBION intro/objective/capability/output cards.
- [x] Added connected six-stage workflow framing.
- [x] Added one-click Analysis / Evidence / What-If / Decision entry points.
- [x] Added deterministic demo-scenario visibility using the existing `/demo-scenarios` endpoint.
- [x] Added live demo-case context for Lot 11213 / Padang Semabok / Melaka without inventing missing evidence.
- [x] Served and injected the new layer through the existing `workspace_v4_server.py` compatibility path.
- [x] No new FastAPI application introduced.
- [x] No duplicate planning engine introduced.
- [x] No fake GIS data introduced.

## 5. Current GIS / release truth

- [x] Previous browser regression isolated the remaining strict GIS failure to `mygems-faults`; other browser/dashboard stages passed.
- [x] JMG Major Fault repair was integrated before the current About/dashboard work.
- [ ] Fresh 25-layer GIS audit must prove actual map imagery/states.
- [ ] Fresh i-Plan upstream preflight evidence required.
- [ ] Fresh Road Intelligence browser proof required.
- [ ] Fresh browser proof that `RUN SITE ANALYSIS` completes and populates the dashboard packet.
- [ ] Fresh browser proof that Analysis → Evidence → What-If → Decision flow is connected.
- [ ] Fresh visual regression of the repaired dashboard.

## 6. About / presentation surface

- [x] Canonical `urbion_horizon_about.html` preserved.
- [x] Canonical `about_master.png` preserved as immutable visual source.
- [x] Production `/about_master.png` route added.
- [x] Render deployment containing the About route reached `LIVE`.
- [ ] User live smoke should confirm the full canonical About visual and hitboxes.

## 7. Render truth

- [x] Existing service retained; no new service created.
- [x] Branch is `feature/canonical-workspace-v2`.
- [x] Start command remains `uvicorn workspace_v4_server:app --host 0.0.0.0 --port $PORT`.
- [x] Latest confirmed About deployment: `dep-dakna8p594qs73f4fj8g` → `LIVE`.
- [ ] Dashboard repair candidate must be deployed only after fresh required checks are accepted.
- [ ] Controlled live smoke must verify the exact deployed SHA.

## 8. Final certification gate

All items below must be true before the release is called green:

- [ ] Fresh CI required gates PASS.
- [ ] Full workspace functional audit PASS.
- [ ] 25-layer GIS end-to-end audit PASS or explicitly records authoritative upstream limitations without false success.
- [ ] Dashboard narrative / objective / capability layer PASS.
- [ ] Analysis → Evidence → What-If → Decision workflow PASS.
- [ ] Development Impact / Road Intelligence / KM-OSC surfaces PASS.
- [ ] About visual live smoke PASS.
- [ ] No duplicate frontend/engine owner introduced.
- [ ] Exact Render SHA matches final release SHA.
- [ ] Final release SHA locked.
- [ ] Final release identity/tag recorded.

## Release rule

`DO NOT CLAIM GREEN WITHOUT ACTUAL GREEN EVIDENCE.`

The dashboard repair is now integrated in Git. The remaining work is validation, deployment of the repaired candidate, and controlled live proof — not a restart or architecture rewrite.
