# MASTER-170 — Map Studio Control Completion

## Objective
Complete the judge-visible Map Studio controls without changing statutory decision logic.

## Delivered
- Live same-origin API and dynamic i-Plan layer catalog preserved.
- Legend / Petunjuk control added.
- Share-location URL control added with coordinate/zoom state restoration.
- Existing distance and area measurement controls retained and syntax-checked.
- Evidence boundary remains explicit: live GIS is SOURCE_CONTEXT, not automatic statutory verification.
- Regression contract added for controls, same-origin API and legacy Render-host removal.

## Release rule
MASTER-170 is complete only when the full regression suite passes on the resulting main commit.
