# MASTER-72 Judge Attack Test

Use these questions to pressure-test the product before judging.

## 1. "Is this an approval system?"
Answer: No. URBION is a spatial planning decision-support and screening platform. Statutory approval remains with the planner/PBT.

## 2. "Where does your policy come from?"
Answer: Covered MBMB scenarios use the integrated RT MBMB 2035 rule engine. Other PBTs are deliberately kept in spatial-demo mode until their local rules are loaded and verified.

## 3. "Are the GIS portals live?"
Answer: URBION only labels an external source as decision evidence when its evidence state supports that claim. Discovery-only or unavailable connectors remain visible as gaps.

## 4. "Why should I trust the score?"
Answer: The suitability score is a transparent screening indicator based on defined inputs and weights. It is not approval probability.

## 5. "Show me failure."
Run `SHOP-FAIL`. Explain that the system does not hide a non-compliance outcome; it produces a redesign-oriented recommendation.

## 6. "Show me uncertainty."
Run `OFFICE-REVIEW`. Explain that missing verification produces a review state rather than a guessed pass.

## 7. "Can you reproduce the demo?"
Yes. The five demo scenarios are deterministic inputs, so the same scenario can be rerun consistently.

## 8. "What makes this different?"
The value proposition is the chain from **site → spatial context → policy → applicability → compliance → suitability → evidence → explainable decision**, rather than a black-box score.
