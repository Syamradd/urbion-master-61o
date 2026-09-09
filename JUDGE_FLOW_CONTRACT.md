# URBION HORIZON — Judge Flow Contract

This is a presentation contract, not a UI rewrite. The canonical shell remains
responsible for rendering the actual workflow.

## Golden path

`ASSESS → MAP → EVIDENCE → WHAT-IF → DECIDE → PLANNER REVIEW → KM/OSC`

## Judge-visible proof at each stage

| Stage | Judge must see | Failure-safe state |
|---|---|---|
| Assess | site + typology + initial result | INPUT REQUIRED |
| Map | selected spatial layer / site context | SOURCE UNAVAILABLE / NO FEATURE |
| Evidence | source + evidence state + gaps | EVIDENCE GAP |
| What-If | scenario delta + independent result | SCENARIO ERROR |
| Decide | recommendation + confidence + WHY trace | REVIEW REQUIRED |
| Planner Review | gaps + next action | VERIFICATION REQUIRED |
| KM/OSC | readiness + blockers | NOT READY |

## Presentation rules

1. Never hide a source error behind an empty panel.
2. Never present source context as statutory approval.
3. Keep the map as the visual focal point during spatial steps.
4. Make the next planning action obvious after every decision.
5. Preserve the evidence-state vocabulary: `USER_PROVIDED`, `CALCULATED`,
   `SOURCE_CONTEXT`, `VERIFIED`, `UNVERIFIED`.
6. Do not introduce decorative claims, invented live readings, or fake
   verification to improve the judge experience.
