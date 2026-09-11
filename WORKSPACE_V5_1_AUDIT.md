# URBION HORIZON — Workspace V5.1 Final Functional Audit

## Release rule
A capability is GREEN only when the canonical presentation exposes the control and wires it to a real existing engine/source. Decorative shells do not count. Existing backend engines/APIs are reused; no duplicate planning logic and no statutory approval claims.

## 1. Runtime / Architecture
- [x] `/` and `/index.html` are isolated Welcome routes.
- [x] `/about` is isolated About route.
- [x] `/workspace` is isolated canonical workspace route.
- [x] Existing FastAPI planning engines remain the backend authority.
- [x] Legacy championship frontend injection removed from the canonical presentation entrypoint.
- [x] Function layer is a single explicit companion asset: `urbion_workspace_final.js`.

## 2. Workspace Geometry
- [x] Three-column desktop shell: Case Builder / GIS / Planning Intelligence.
- [x] Left panel independently scrollable.
- [x] Right rail independently scrollable.
- [x] Centre map is the hero surface.
- [x] Bottom dock contains Spatial Context / Evidence & Compliance / Site Intelligence.
- [x] Compact field spacing; reduced unnecessary vertical whitespace.
- [x] Responsive fallback for smaller widths.

## 3. Case Builder
- [x] Project/site name, State, District, PBT, Mukim, Lot/UPI.
- [x] Latitude / Longitude and map selection.
- [x] Development type, project reference, development class.
- [x] Guna Tanah 1 / 2 / 3 cascading hierarchy.
- [x] Plot ratio, height, units, GFA.
- [x] Perimeter planting and landscaped pedestrian walkway inputs.
- [x] TOD coordinates and precinct.
- [x] Environmental / risk notes.
- [x] Infrastructure / utility notes.
- [x] Constraints / supporting source note.
- [x] Analysis focus.

## 4. Guna Tanah Taxonomy
- [x] No `Perdagangan` category used as the top-level class.
- [x] Top-level taxonomy uses PLANMalaysia/i-Plan hierarchy terminology, including `Perumahan`, `Komersial`, `Industri`, `Institusi dan Kemudahan Masyarakat`, `Tanah Lapang dan Rekreasi`, `Pengangkutan dan Lalulintas`, `Infrastruktur dan Utiliti`, `Pertanian`, `Hutan`, `Badan Air`, `Pantai`.
- [x] Guna Tanah 2 is repopulated from the selected Guna Tanah 1.
- [x] Guna Tanah 3 / activity is repopulated from the selected Guna Tanah 2.
- [x] Land-use values are submitted in the assessment payload.
- [x] UI explicitly notes alignment to the PLANMalaysia GIS Rancangan Pemajuan Version 2.0 classification used by i-Plan.

## 5. GIS / Map
- [x] Leaflet map container.
- [x] OSM Map base layer.
- [x] Esri Satellite base layer.
- [x] Hybrid base layer.
- [x] Base-layer buttons visibly switch the active layer.
- [x] Map click updates site coordinates and marker.
- [x] Locate control recentres to entered coordinates.
- [x] `invalidateSize(true)` after presentation load/resize.
- [x] 400 m ring.
- [x] 800 m ring.
- [x] 1 km ring.
- [x] Ring visibility toggles.
- [x] Search box supports external location search and map recentering.
- [x] Road/transit context toggle provides an actual OSM overlay when enabled.

## 6. i-Plan Layer Drawer
- [x] Drawer is independently scrollable.
- [x] Current Land Use WMS.
- [x] Zoning / Proposed Land Use WMS.
- [x] Committed Land Use WMS.
- [x] Topography WMS.
- [x] Heritage WMS.
- [x] CFS / ecological network WMS.
- [x] Rangkaian Ekologi WMS.
- [x] KSAS WMS.
- [x] Disaster Risk WMS.
- [x] State-specific layer naming for key land-use layers (Melaka 04, Selangor 10, Johor 01, Perak 08).
- [x] Actual ON/OFF adds/removes the WMS overlay from Leaflet.
- [x] Layer loading state is shown.
- [x] Tile error fallback exists for current-land-use generic i-Plan layer when the state-specific endpoint fails.
- [x] Layer source is explicitly shown as i-Plan in the drawer.

## 7. Site Analysis
- [x] Run Site Analysis control.
- [x] Calls `/workstation/analysis`.
- [x] Land-use hierarchy is included in the assessment payload.
- [x] Actual response is bound into readiness, findings, rules, evidence health and dock summaries.
- [x] No decorative fixed score is used as the data source.
- [x] Error state shown to user.

## 8. RT / Planning Compliance
- [x] Existing deterministic compliance engine reused.
- [x] RT compliance rows are rendered from returned `compliance_results`.
- [x] Status shown.
- [x] Proposed value shown when supplied.
- [x] Requirement / target shown when supplied.
- [x] Reason / explanation / traceability shown when supplied.
- [x] RT / GP distinction preserved.
- [x] No statutory approval claim.

## 9. GP / Guidelines
- [x] Existing guideline intelligence response is read from multiple known response paths.
- [x] Relevant guideline candidates shown after analysis.
- [x] Candidate/review state shown when supplied.
- [x] Topic/title/source information surfaced from engine output where available.

## 10. Evidence
- [x] Evidence-chain modal.
- [x] Source / status / finding / implication table when structured evidence is returned.
- [x] Review gaps surfaced.
- [x] Evidence health summary on right rail.
- [x] Live/context vs verified/unverified counts surfaced when returned.
- [x] Explicit boundary: `LIVE SOURCE CONTEXT ≠ STATUTORY VERIFICATION`.

## 11. Planning Intelligence Rail
- [x] Decision Readiness.
- [x] Key Findings.
- [x] Planning Compliance.
- [x] Evidence Health.
- [x] Decision Support.
- [x] Quick actions.
- [x] Results are populated from analysis response where available.

## 12. What-If
- [x] Calls `/what-if` directly.
- [x] Baseline displayed.
- [x] Scenario controls displayed.
- [x] Scenario submitted as an engine variant.
- [x] Returned scenario status / decision delta / impacts displayed.
- [x] No fabricated numerical simulation.

## 13. Decision
- [x] Calls `/decision-center` when invoked.
- [x] Displays status.
- [x] Displays rationale / reasons when returned.
- [x] Displays planner action / next action when returned.
- [x] Keeps authority boundary explicit.

## 14. Output
- [x] Planner-ready output modal.
- [x] Full case identity summary.
- [x] Land-use hierarchy summary.
- [x] RT / GP counts.
- [x] Evidence gaps.
- [x] Authority boundary.
- [x] Print / PDF action.

## 15. Global Controls
- [x] EN/BM control retained.
- [x] Dark/light theme control.
- [x] Reset case.
- [x] Fullscreen.
- [x] Print / PDF.
- [x] Data Sources modal.
- [x] System Status modal checks `/health`, `/metadata`, `/map/layers`.
- [x] Help modal.
- [x] About Us navigation.

## 16. Premium Visual Contract
- [x] Near-black premium foundation.
- [x] Cyan / mint URBION accent system.
- [x] Horizontal URBION lockup.
- [x] Map-first composition.
- [x] Compact information hierarchy.
- [x] Subtle map overlay / spatial-tech treatment.
- [x] Context rings.
- [ ] Final visual screenshot comparison at target Render viewport remains a final QA gate.

## 17. Final Judge Journey
- [x] Open workspace.
- [x] Define location.
- [x] Select site on map.
- [x] Select synced Guna Tanah 1 → 2 → 3 activity hierarchy.
- [x] Set development / intensity.
- [x] Run assessment.
- [x] Surface spatial / planning findings.
- [x] Surface RT compliance.
- [x] Surface GP candidates.
- [x] Surface evidence health / gaps.
- [x] Run What-If.
- [x] Compare baseline / scenario.
- [x] Open Decision Support.
- [x] Generate planner-ready Output.
- [x] Print / PDF.

## 18. Release Gate
### Source-side status
- [x] Canonical presentation source updated.
- [x] Function layer committed.
- [x] Guna Tanah hierarchy corrected away from legacy `Perdagangan` terminology.
- [x] i-Plan WMS integration wired into Leaflet.
- [x] Base-map controls wired.
- [x] Spatial rings wired.
- [x] Evidence / compliance / GP / What-If / Decision / Output bindings wired.
- [x] Utility controls wired.

### Final external gate
- [ ] Run CI / static checks on the latest commit.
- [ ] One browser QA pass on the canonical `/workspace` route.
- [ ] Verify real map tiles and i-Plan WMS rendering in the target deployment environment.
- [ ] Verify BM/EN visual text sweep in target deployment.
- [ ] Verify target visual similarity against the locked generated Workspace reference.
- [ ] Only after the above pass: one final Render deployment.

## Source references
- PLANMalaysia i-Plan public analysis module confirms that Guna Tanah Level 1/2/3 are the general, semi-detailed and detailed classifications referenced to the Manual GIS Rancangan Pemajuan Version 2.0. It also states that the current planning activity/use information comes from the relevant Local Plan search. citeturn591750search0
- PLANMalaysia's current FAQ states that i-Plan data are collected/updated/verified/standardised and that planning land-use information is updated twice yearly; the FAQ page was updated 10/09/2026. citeturn591750search1
- PLANMalaysia's official GIS Manual Version 2.0 is the classification reference surfaced by the i-Plan module. citeturn307340search2
- The i-Plan GeoWebCache currently exposes the land-use current, zoning, committed-use, KSAS, CFS, ecological, heritage, risk and topography layers used by the workspace layer drawer. citeturn200549search0

## Current conclusion
**Source-side implementation is complete enough for the final QA gate. Do not iterate Render yet. The next action is one controlled source/browser validation pass; if it passes, perform one final Render deployment and stop.**
