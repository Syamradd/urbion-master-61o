"""Integrated LCP intelligence orchestration for URBION.

The orchestrator connects existing deterministic planning-support modules into
one traceable LCP evidence package. It never upgrades source context into
statutory verification and never invents missing measurements or policy links.
"""
from __future__ import annotations
from typing import Any

from urbion_development_impact import build_development_impact
from urbion_multi_source import build_spatial_intelligence
from urbion_policy_graph import build_policy_graph
from urbion_recommendation_engine import build_recommendations
from urbion_kebenaran_merancang import build_km_readiness
from urbion_decision_center import build_decision_center


def _dedupe(values: list[Any]) -> list[Any]:
    return list(dict.fromkeys(str(v) for v in values if v))


def build_lcp_intelligence(*, assessment: dict[str, Any], development_inputs: dict[str, Any] | None = None,
                           policy_links: list[dict[str, Any]] | None = None,
                           national_links: list[dict[str, Any]] | None = None,
                           sdg_links: list[dict[str, Any]] | None = None,
                           spatial_inputs: dict[str, Any] | None = None,
                           station_snapshot: dict[str, Any] | None = None,
                           km_inputs: dict[str, Any] | None = None,
                           what_if_summary: dict[str, Any] | None = None) -> dict[str, Any]:
    """Compose assessment, spatial, station, impact, policy, recommendation, decision and KM evidence."""
    assessment = assessment or {}
    dev = development_inputs or {}
    spatial = spatial_inputs or {}
    impacts = build_development_impact(
        development_type=dev.get("development_type", assessment.get("development_type", "")),
        units=dev.get("units"), site_area_ha=dev.get("site_area_ha"),
        commercial_gfa_m2=dev.get("commercial_gfa_m2"), jobs=dev.get("jobs"),
        population=dev.get("population"), daily_trips=dev.get("daily_trips"),
        road_distance_m=dev.get("road_distance_m", spatial.get("road_distance_m")),
        flood_exposure=dev.get("flood_exposure", spatial.get("flood_exposure")),
        nearby_facilities=dev.get("nearby_facilities"),
        source_context=dev.get("source_context"),
    )
    spatial_result = build_spatial_intelligence(
        source_context=spatial.get("source_context"),
        road_distance_m=spatial.get("road_distance_m"),
        elevation_m=spatial.get("elevation_m"),
        flood_exposure=spatial.get("flood_exposure"),
        include_domains=True,
    )
    policy = build_policy_graph(
        impacts=impacts.get("impacts"), policy_links=policy_links,
        national_links=national_links, sdg_links=sdg_links,
    )
    recommendations = build_recommendations(impacts=impacts, policy_graph=policy)

    km = None
    if km_inputs:
        km = build_km_readiness(
            pbt=km_inputs.get("pbt", assessment.get("pbt", "")),
            development_type=km_inputs.get("development_type", assessment.get("development_type", "")),
            documents=km_inputs.get("documents"), km_category=km_inputs.get("km_category"),
            technical_reviews=km_inputs.get("technical_reviews"),
        )

    gaps = _dedupe(
        list(assessment.get("review_gaps", []) or [])
        + list(spatial_result.get("review_gaps", []) or [])
        + list(impacts.get("review_gaps", []) or [])
        + list(policy.get("review_gaps", []) or [])
        + list(recommendations.get("review_gaps", []) or [])
        + list((km or {}).get("review_gaps", []) or [])
    )
    evidence_counts = {"USER_PROVIDED": 0, "CALCULATED": 0, "SOURCE_CONTEXT": 0, "VERIFIED": 0, "UNVERIFIED": 0}
    for item in (spatial_result.get("metrics", []) or []):
        evidence_counts[item.get("evidence", "UNVERIFIED")] = evidence_counts.get(item.get("evidence", "UNVERIFIED"), 0) + 1
    if station_snapshot:
        evidence_counts[station_snapshot.get("evidence", "SOURCE_CONTEXT")] = evidence_counts.get(station_snapshot.get("evidence", "SOURCE_CONTEXT"), 0) + 1

    decision_center = build_decision_center(assessment=assessment, evidence=policy.get("nodes", {}).get("links", []))
    if what_if_summary:
        decision_center["what_if"] = {
            "baseline_status": what_if_summary.get("baseline_status"),
            "baseline_score": what_if_summary.get("baseline_score"),
            "best_candidate": what_if_summary.get("best_candidate"),
            "ranked_scenarios": what_if_summary.get("ranked_scenarios", []),
        }

    return {
        "version": "MASTER-199",
        "project": "URBION HORIZON",
        "site": assessment.get("site", {}),
        "assessment": {"final_status": assessment.get("final_status"), "decision_confidence": assessment.get("decision_confidence"), "recommendation": assessment.get("recommendation")},
        "spatial_intelligence": spatial_result,
        "station_intelligence": station_snapshot or {"status": "NOT_PROVIDED", "evidence": "UNVERIFIED", "review_gaps": ["station:LIVE_SNAPSHOT_NOT_PROVIDED"]},
        "development_impact": impacts,
        "policy_graph": policy,
        "recommendations": recommendations,
        "what_if": what_if_summary or {"status": "NOT_PROVIDED", "disclaimer": "Scenario comparison is optional and remains decision support only."},
        "decision_center": decision_center,
        "km_readiness": km,
        "evidence_summary": {"counts": evidence_counts, "review_gap_count": len(gaps)},
        "review_gaps": gaps,
        "trace": "SITE → SPATIAL → STATION → IMPACT → ISSUE → POLICY/SDG → RECOMMENDATION → WHAT-IF → DECISION CENTER → LCP/PLANNER REVIEW",
        "decision_boundary": "INTEGRATED_LCP_PLANNING_SUPPORT",
        "statutory_verification": "NOT_CLAIMED",
    }
