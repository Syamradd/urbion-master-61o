# MASTER-81 — Planning Value Hardening

Phase C hardening checkpoint.

## Purpose

Make the Planning Value layer deterministic, explainable and safe for the judge workflow.

## Contract

Every planning-value response exposes the same top-level fields: title, version, band, score, score_label, headline, status, key_findings, blockers, decision_drivers, evidence_gaps, strengths, next_actions, rationale and disclaimer.

## Safety rules

- NON-COMPLIANCE remains BLOCKED and produces redesign actions.
- NOT APPLICABLE remains a reposition/reconsideration outcome.
- REQUIRES REVIEW remains REVIEW and does not become approval.
- PBTs without a loaded local rule engine explicitly require local policy evidence.
- Evidence gaps remain visible rather than being converted into verified evidence.
- Planning Value is decision support only, not statutory approval.
