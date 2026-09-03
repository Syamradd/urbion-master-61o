# MASTER-196 — ADVERSARIAL INTEGRITY GATE

The final competition build must survive hostile inputs and misleading evidence without producing false certainty.

## Attack classes
- NaN / infinity / out-of-range / placeholder coordinates
- Missing station observations
- Stale station timestamps
- Missing policy references
- Conflicting source context
- Unsafe HTML strings from remote or user-provided fields
- Missing development-impact inputs
- Unsupported statutory conclusions
- Scenario inputs that could be mistaken for baseline facts

## Expected behaviour
Reject invalid spatial input; preserve uncertainty as review gaps; label calculated values as calculated; escape UI values; keep source provenance; and retain the `NOT_CLAIMED` statutory boundary.

MASTER-196 is a red-team integrity gate, not a claim of mathematical perfection or permanent availability of external services.
