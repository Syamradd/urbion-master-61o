# MASTER-186 — POLICY & SDG INTELLIGENCE GRAPH

## Objective
Connect development-impact findings to traceable planning issues, policy references, strategies, national references and SDG relationships without fabricating clauses or applicability.

## Graph
IMPACT → PLANNING ISSUE → POLICY / STRATEGY / GUIDELINE → REFERENCE → SDG → EVIDENCE → RECOMMENDATION

## Evidence discipline
Only caller-supplied policy references become graph edges. Missing references become `REVIEW_REQUIRED`; clause numbers and statutory applicability are never invented.

## Decision boundary
`PLANNING_POLICY_TRACE_ONLY` and `NOT_CLAIMED` statutory verification.

## Next
MASTER-187 will turn verified/traceable graph edges into evidence-backed planning recommendations.
