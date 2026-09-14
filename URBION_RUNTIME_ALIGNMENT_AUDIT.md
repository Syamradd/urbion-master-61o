# URBION HORIZON — Runtime Alignment Audit

Status: `ENGINEERING CONVERGENCE — RELEASE HARDENING`

## 1. Canonical runtime

- Active hardening branch: `feature/championship-convergence-v1`
- Canonical baseline: `feature/canonical-workspace-v2`
- Production entrypoint: `landing_server:app`
- Render command shape: `uvicorn landing_server:app --host 0.0.0.0 --port $PORT`
- Render Python target: `3.11.11`
- Canonical workspace: `workspace_v5.html`
- Canonical evidence packet: `PHASE1.2`
- Decision authority: `NONE`
- Statutory verification: `NOT_CLAIMED`

## 2. Active served frontend ownership

The `/workspace` page is served by `landing_server.py` and loads one deterministic V5 script chain:

`bridge → runtime → GIS layer manager → canonical UI → modal → PBT → utilities → review gaps → environment → mobility → development impact → ratio → road intelligence → analysis summary → station/Judge/KM-OSC owner`

`urbion_workspace_analysis_summary_owner.js` owns the analysis snapshot, bounded AI presentation, Decision Story, and Live Evidence Story.

`urbion_workspace_station_map_owner.js` owns station-map presentation, Judge Snapshot, presentation mode, and KM/OSC readiness presentation.

No specialist owner is dynamically imported at runtime.

## 3. Removed duplicate ownership

Superseded files removed from the active branch:

- `urbion_workspace_judge_owner_v1.js`
- `urbion_workspace_decision_story_owner_v1.js`
- `urbion_workspace_decision_story_owner_v2.js`
- `urbion_workspace_live_evidence_owner_v1.js`

Historical workspace V2/V3/V4 assets remain non-served for reference only and are not part of the canonical `/workspace` script chain.

## 4. Canonical data flow

`deterministic assessment → canonical result cache → canonical evidence packet → V5 presentation owners`

Presentation owners must not calculate planning scores, alter rule applicability, approve development, or promote source context to statutory verification.

## 5. Evidence boundaries

Allowed evidence states:

`USER_PROVIDED`, `CALCULATED`, `SOURCE_CONTEXT`, `VERIFIED`, `UNVERIFIED`

Live JPS/MyEQMS/MyGEMS context is displayed with its source/timestamp/query state. Live context does not itself establish adopted-plan applicability, parcel authority, or statutory approval.

## 6. Required gates

- canonical runtime topology
- error envelope
- canonical convergence
- What-If canonical packet
- bounded agent contract
- downstream planner handoff
- road intelligence
- frontend owner lifecycle
- P1 Judge UX
- P2 Presentation Mode
- P3 Decision Story
- P4 Live Evidence Story
- P5 KM/OSC readiness
- P6 planner output
- Phase 1 evidence packet
- rule provenance
- browser smoke
- GIS 25-layer regression
- MyEQMS station contract
- Render parity smoke using Python 3.11.11

## 7. Release blockers

Release remains blocked until all current gates are green, the final release SHA is locked, production branch parity is proven, and live production smoke has been run on the approved release.

Render remains intentionally on `HOLD` until the explicit deployment command is given.
