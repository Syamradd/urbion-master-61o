# MASTER-145 — Red-Team Matrix

Attack the product at the boundaries that matter to a planning judge:

| Attack | Expected safe behaviour |
|---|---|
| Missing coordinates | Reject / request spatial input; never fabricate a site |
| Non-finite coordinates | Reject as invalid spatial input |
| Placeholder coordinates | Reject; never return false zero-distance evidence |
| Missing source feature | Mark evidence gap / unverified |
| Project-reference GIS conflict | Official/source context wins; conflict remains traceable |
| Unsupported PBT rule | Do not invent a local statutory control |
| Scenario change | Show deterministic delta; preserve baseline |
| KM request | Return workflow readiness only; never approval |
| Stale deployment | Flag release identity mismatch |
| Dead navigation | Fail regression contract |

The objective is not to make URBION always say YES. The objective is to make every decision traceable, bounded, reproducible, and useful for planner review.
