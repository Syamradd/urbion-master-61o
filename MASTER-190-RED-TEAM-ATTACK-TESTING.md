# MASTER-190 — Red-Team Attack Testing

## Attack classes
- Placeholder / non-finite spatial inputs
- Missing assessment contract
- Missing evidence and policy references
- Untrusted text reaching HTML surfaces
- Source-context versus calculated/verified confusion
- Recommendation without traceable policy basis
- KM readiness mistaken for approval
- External/live-source failure propagation

## Expected behavior
Reject invalid spatial input; preserve review gaps; escape untrusted UI values; isolate provider failures; retain evidence states; keep recommendations planner-review only; never claim statutory approval.

## Release gate
The red-team suite must pass together with the complete regression suite before championship lock.
