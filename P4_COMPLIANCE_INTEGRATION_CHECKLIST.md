# URBION HORIZON — P4 Compliance Integration Gate

## Goal
Move from candidate rule retrieval to evidence-aware applicability and explainable planning justification without overstating statutory certainty.

## Required decision chain
`RULE CANDIDATE → TYPOLOGY MATCH → SPATIAL CONDITION → INPUT EVIDENCE → APPLICABILITY → COMPLIANCE → WHY → GAP → PLANNER ACTION`

## Mandatory outputs
Every evaluated rule should expose:
- `rule_id`
- requirement/value/unit
- source document + source section
- evidence classification / traceability
- applicability state
- compliance state where determinable
- reason / WHY
- verification gap when required
- planner action

## Safety gates
- Non-MBMB authority: do not apply RT MBMB rules.
- Typology mismatch: do not leak rules across development types.
- Spatial-dependent rule without spatial evidence: `VERIFICATION_REQUIRED`.
- Missing proposal input: `INPUT_REQUIRED` rather than assumed compliance.
- Partial traceability: disclose it.
- No result may claim statutory approval.

## Integration gate
1. Unit/contract tests pass.
2. Demo comply case produces traceable WHY.
3. Demo fail case identifies the unsatisfied requirement.
4. Spatial-dependent case without TOD evidence remains verification-required.
5. Non-MBMB case does not inherit MBMB controls.
6. Canonical shell/server remains untouched until controlled integration.
7. Browser QA checks visible evidence/source/gap states.
