# URBION HORIZON — MASTER REPAIR / HANDOFF PROMPT

## ROLE
You are the engineering + product-design agent responsible for finishing URBION HORIZON for the PlanMalaysia / UrbanMind AI Challenge. Treat this repository as an existing championship project, not a new app and not a generic dashboard redesign.

Do not restart the project. Do not replace the planning engines. Do not create a second dashboard. Reuse the existing planning, GIS, evidence, What-If, decision, recommendation, policy, LCP and orchestration engines already present in the repository.

The objective is to make one coherent, decision-grade planning command centre whose visible UI, runtime behaviour, evidence model, and deployment state all agree.

## WHAT HAPPENED / ROOT-CAUSE CONTEXT
A previous release was incorrectly declared production-ready because automated CI was green while the Render deployment was still serving an older commit. The live Render service was serving commit `47e5477d3ef56920fd8aa8db2fee0467fbf2a328`, while the repository `main` later advanced to:

- `2984fe1ed0c0dfb64f13a0b291eca284258922e9` — restore landing entry and isolate championship presentation.
- `fe29f52d11dfc2b720a33560681aac8adea54ba4` — restore championship visual hierarchy and workflow framing.

Therefore screenshots taken from Render reflected the older build, not the latest repaired source. This caused apparently missing/wrong features to persist in production even though source and CI had moved forward.

Never again equate “CI green” with “live visual product approved”. The final gate is: source commit verified -> all required automated gates green -> Render deployed to the exact same commit -> live browser inspection -> only then production-ready.

## CURRENT PRODUCT VISION
URBION HORIZON is a premium spatial-policy-decision intelligence platform for planners.

Canonical user flow:

LANDING / WELCOME
→ DEFINE PLANNING CASE
→ CANONICAL SITE / LOT IDENTITY
→ SPATIAL EVIDENCE / MAP
→ SITE INTELLIGENCE / ASSESSMENT
→ WHAT-IF SCENARIO
→ DECISION / RECOMMENDATION
→ LCP / POLICY / IMPACT SUPPORT
→ OUTPUT / EXPLAINABLE DECISION PACKET

The user should always understand where they are in this chain.

## NON-NEGOTIABLE ARCHITECTURE
1. One primary dashboard / Planning Command Centre only.
2. No duplicate floating workstation or legacy Decision OS surfaces leaking into the main experience.
3. Existing deterministic planning engines remain authoritative.
4. Existing GIS/evidence sources remain source-aware.
5. No fabricated geometry, zoning, flood, environment or statutory claims.
6. i-Plan candidate geometry is not legal cadastral confirmation; JUPEM remains the authoritative cadastral verification boundary.
7. Evidence states must remain distinct: LIVE_QUERY, NO_FEATURE, QUERY_ERROR, EVIDENCE_GAP, SOURCE_CONTEXT, and other explicit states already implemented.
8. What-If is scenario analysis, not statutory approval.
9. A change to case inputs must propagate through one canonical shared state into spatial evidence, intelligence, What-If, decision and output.
10. No visual change may silently break engine/API contracts.

## VISUAL DIRECTION
Premium URBION HORIZON command-centre aesthetic:
- Deep navy / blue-black background.
- Cyan + mint intelligence accents with restrained blue support.
- Subtle spatial grid / network graphics / atmospheric radial gradients.
- High information density but readable hierarchy.
- Rounded premium panels with controlled borders and depth.
- Map is the hero evidence surface.
- Avoid generic SaaS cards, toy-like UI, flat black backgrounds, excessive glow, excessive tiny labels, or decoration with no planning meaning.
- Preserve the locked dark and light URBION HORIZON logo variants and proportions.

## TYPOGRAPHY RULES
Do not allow the left case form to visually overpower the intelligence rail.

Hierarchy must be obvious:
1. Hero / workspace title
2. Major section title
3. Card title
4. Body / action text
5. Labels / metadata

Never use tiny 7–9 px text as the default for important readable content. Metadata may be small, but primary intelligence, headings, action labels, form values and decision states must be comfortably readable at desktop judging distance.

## DESKTOP LAYOUT TARGET
Use a balanced command-centre composition:
- Left: case/input panel with readable hierarchy.
- Centre: large map / spatial evidence panel.
- Right: intelligence rail sized enough to read decision metrics and evidence.
- Avoid huge dead space under the map.
- Avoid giant empty sections created only by fixed viewport heights.
- Keep map height visually proportional to the rest of the workspace.
- The right rail must never look like tiny footnotes next to a giant left form.
- Panels should align to a consistent baseline and spacing system.

## MAP / GIS REQUIREMENTS
The map must support:
- JALAN / SATELIT / HYBRID / LAPISAN base map choices where supported.
- Search / coordinate positioning.
- Site marker / canonical site identity.
- TOD / transit context.
- 400 m, 800 m, 1 km, and 1.5 km screening/context rings where the current engine supports them.
- Site-to-TOD relationship cue.
- Grouped layer drawer.
- Opacity controls.
- Scrollable layer content.
- Visible source/status indicators.

Hard rule: NO GEOMETRY = NO MAP LAYER.
Do not visually imply a live geometry result when only source context or an evidence gap exists.

## LAYER DRAWER REQUIREMENTS
The layer drawer must be a single, usable, scrollable container.

Required groups should cover the current supported families, including where available:
- Current Land Use
- Zoning
- Committed Land Use
- RFN / structure-plan context
- Cadastral / lot candidate context
- Flood / risk / disaster
- Ecology / KSAS / environmental context
- Heritage
- Terrain / topography
- Geology / MyGEMS
- Mobility / CFS / TOD

Every row needs an understandable name, source/status, toggle and opacity where supported.

The drawer must scroll through all available layers. Do not clamp each group to a hidden internal height. Group bodies must not create inaccessible content. The drawer must not block the map close control or overflow outside the viewport.

## CASE INPUT REQUIREMENTS
The case panel is the entry point, not a decorative form.

It must make clear:
- Project / site name
- Latitude / longitude
- State
- PBT
- District
- Lot / UP reference when relevant
- Project / planning reference
- Existing land-use context
- Development category / typology inputs
- Development intensity / plot ratio where relevant
- TOD / transit context
- Other conditional fields exposed by the chosen development type

The fields must drive the canonical shared state used downstream.

## INTELLIGENCE RAIL REQUIREMENTS
The intelligence rail should explain:
- Decision readiness
- Planning fit
- Spatial access
- Environment
- Evidence confidence
- Development intensity
- Site intelligence
- Evidence health by domain
- Next action

Do not make the right rail tiny. Decision-grade numbers, section titles and recommendations must be readable.

## EVIDENCE / PROVENANCE
For meaningful planning findings, make the evidence chain visible:
SOURCE → STATUS → FINDING → PLANNING IMPLICATION → NEXT ACTION

Never hide important source qualification in tiny metadata if it changes the meaning of the result.

## WHAT-IF
What-If must visibly support:
- Baseline state
- Modified scenario state
- Delta / impact comparison
- Reset to baseline
- Clear handoff into the decision surface

It must not be a disconnected utility panel.

## DECISION
The decision surface should clearly communicate outcomes such as:
- Recommended
- Conditional / Review
- Not Recommended

and show:
- rationale
- evidence coverage
- key risks
- policy implications
- relevant planning conditions
- recommended next action

Recommendations must be grounded in the deterministic planning/evidence chain.

## OUTPUT / LCP / POLICY / IMPACT
Where the current engines support them, consolidate policy, impact, recommendation and LCP intelligence into the same decision chain rather than spawning unrelated dashboards.

## LANDING / WELCOME
Root `/` should be the public welcoming page.
It must communicate:
- what URBION HORIZON is
- the planning problem it solves
- its spatial-policy-decision intelligence value
- evidence / traceability principle
- a clear CTA into the Planning Command Centre
- premium HORIZON visual identity

`/championship.html` is the actual command-centre workspace.

## BM / EN
Language switching must cover the full visible experience.
Test:
EN → BM → EN
and ensure:
- no missing labels
- no overflow
- no mixed terminology
- no broken action buttons
- no state reset caused by language change

## DARK / LIGHT
Both themes must be intentional, not merely inverted.
Check:
- contrast
- logos
- map chrome
- buttons
- panels
- borders
- drawer
- form controls
- decision states

## RESPONSIVE MATRIX
Validate at minimum:
375, 390, 430, 768, 820, 1120, 1280, 1440, 1600, 1920.

At smaller widths:
- collapse columns logically
- preserve readable text
- preserve map usability
- allow drawer access without blocking page
- avoid horizontal clipping

## UI STATES
Explicitly test:
- initial / empty
- loading
- live data
- no feature
- query error
- evidence gap
- analysis ready
- What-If baseline
- What-If modified
- reset state
- decision ready
- disabled / unavailable action

## INTERACTION / ACCESSIBILITY
Check:
- buttons actually invoke their actions
- keyboard focus is visible
- Enter / Escape behaviour where defined
- reduced-motion preference is respected
- no duplicate selectors or semantic class collisions
- close buttons use close-only semantics
- scrolling containers actually scroll
- no overlay traps the user

## CROSS-BROWSER
Validate the actual command-centre interaction/visual behaviour in:
- Chromium
- Firefox
- WebKit

Do not treat a single functional pass as a full visual sign-off.

## TEST STRATEGY
Do not invent a fake “100%” status.
Use evidence:
1. targeted browser tests
2. full regression
3. responsive visual QA
4. UX contract
5. cross-browser QA
6. live Render inspection

If one test passes while the screenshot is visibly wrong, the product is not done.

## DEPLOYMENT DISCIPLINE
Render service is:
- service: `urbion-master-61o`
- service id: `srv-daclsgh5efls73et5mg0`
- repo: `Syamradd/urbion-master-61o`
- branch: `main`
- deployment auto-deploy is off

Before declaring production ready:
- verify `main` HEAD SHA
- verify all required GitHub checks for that SHA
- manually deploy that exact SHA to Render
- verify Render deployment commit exactly matches SHA
- verify `/health`
- verify `/`
- verify `/championship.html`
- visually inspect actual live UI
- only then freeze

Never deploy a stale commit just because an older deployment is green.

## SAFE CHANGE RULE
Do not rewrite or delete working planning engines merely to simplify the UI.
Prefer:
- small additive visual/interaction fixes
- isolated visual-system files
- explicit selectors
- deterministic state bridges
- targeted regression tests

Do not create duplicate dashboards or parallel sources of truth.

## DONE CRITERIA
The work is complete only when:
- root landing page exists and is the real public entry
- championship workspace is reached intentionally from landing
- map-first hierarchy is visually obvious
- typography hierarchy is balanced
- no giant unexplained dead space exists
- layer drawer is fully scrollable and usable
- all supported layer groups are reachable
- case inputs propagate through canonical state
- spatial evidence and evidence statuses are visible
- What-If baseline / modify / delta / reset works
- decision recommendation is evidence-backed
- policy/impact/LCP handoff remains connected
- BM/EN is consistent
- dark/light is coherent
- responsive matrix is acceptable
- Chromium/Firefox/WebKit are acceptable
- loading/empty/error/evidence-gap states are understandable
- no duplicate/legacy dashboard leaks into the primary UI
- all required automated gates are green on the release SHA
- Render is LIVE on the exact release SHA
- live browser QA matches the intended product

## FINAL COMMUNICATION RULE
When reporting status, distinguish:
- CODED
- TESTED
- DEPLOYED
- LIVE-VERIFIED

Never call a feature “done” merely because it exists in source code.
Never call the product “final” merely because CI is green.
Never claim a visual issue is fixed until the live or test-rendered screenshot shows the intended result.
