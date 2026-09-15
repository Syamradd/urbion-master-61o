"""Evidence-aware development impact screening for URBION.

This is a planning-support model, not a statutory SIA/EIA/LCP certification.
Only explicit development inputs are quantified; missing inputs become review
items instead of fabricated estimates.
"""
from __future__ import annotations
from typing import Any

IMPACT_DOMAINS = ("physical", "social", "economic")


def _number(value: Any) -> float | None:
    try:
        n = float(value)
        return n if n == n and abs(n) != float("inf") else None
    except (TypeError, ValueError):
        return None


def _metric(metric_id: str, label: str, value: Any = None, unit: str | None = None, evidence: str = "UNVERIFIED", status: str = "REVIEW_REQUIRED", basis: str | None = None) -> dict[str, Any]:
    return {"id": metric_id, "label": label, "value": value, "unit": unit, "evidence": evidence, "status": status, "basis": basis}


def _derived(id_: str, label: str, value: float | None, unit: str, basis: str) -> dict[str, Any]:
    if value is None:
        return _metric(id_, label, None, unit, "UNVERIFIED", "REVIEW_REQUIRED", basis)
    return _metric(id_, label, round(value, 3), unit, "CALCULATED", "CALCULATED", basis)


def build_development_impact(*, development_type: str = "", units: float | None = None, site_area_ha: float | None = None, commercial_gfa_m2: float | None = None, jobs: float | None = None, population: float | None = None, daily_trips: float | None = None, road_distance_m: float | None = None, flood_exposure: bool | None = None, nearby_facilities: dict[str, float] | None = None, source_context: dict | None = None) -> dict[str, Any]:
    """Create a transparent physical/social/economic impact screen."""
    units_n, area_n, gfa_n, jobs_n, pop_n, trips_n, road_n = map(_number, (units, site_area_ha, commercial_gfa_m2, jobs, population, daily_trips, road_distance_m))
    impacts: dict[str, list[dict[str, Any]]] = {k: [] for k in IMPACT_DOMAINS}
    gaps: list[str] = []

    # Physical: intensity, movement, access and environmental exposure.
    density = units_n / area_n if units_n is not None and area_n and area_n > 0 else None
    impacts["physical"] += [
        _derived("development_intensity", "Residential intensity", density, "units/ha", "units ÷ site_area_ha"),
        _derived("trip_generation", "Daily movement demand", trips_n, "trips/day", "user-provided development trip estimate"),
        _derived("road_access", "Nearest road context", road_n, "m", "spatial evidence"),
        _metric("flood_exposure", "Flood exposure flag", flood_exposure, None, "CALCULATED" if flood_exposure is not None else "UNVERIFIED", "FLAGGED" if flood_exposure else ("NO_FLAG" if flood_exposure is False else "REVIEW_REQUIRED"), "spatial/flood evidence"),
    ]
    if density is None: gaps.append("physical:DEVELOPMENT_INTENSITY_INPUT")
    if trips_n is None: gaps.append("physical:TRIP_GENERATION_INPUT")
    if road_n is None: gaps.append("physical:ROAD_ACCESS_INPUT")
    if flood_exposure is None: gaps.append("physical:FLOOD_EXPOSURE_INPUT")

    # Social: population, community demand and facility accessibility.
    residents = pop_n if pop_n is not None else units_n
    impacts["social"] += [
        _derived("additional_population", "Potential additional population", residents, "persons", "user-provided population; unit count only used as an explicit proxy"),
        _derived("housing_units", "Proposed residential units", units_n, "units", "development input"),
    ]
    if nearby_facilities:
        for key, distance in nearby_facilities.items():
            d = _number(distance)
            impacts["social"].append(_derived(f"facility_{key}", f"Nearest {key} context", d, "m", "provided facility distance"))
    else:
        impacts["social"].append(_metric("facility_access", "Community facility accessibility", None, "m", "UNVERIFIED", "REVIEW_REQUIRED", "facility network evidence"))
        gaps.append("social:FACILITY_ACCESS_INPUT")
    if residents is None: gaps.append("social:POPULATION_INPUT")

    # Economic: jobs, commercial activity and development scale.
    impacts["economic"] += [
        _derived("employment", "Potential employment", jobs_n, "jobs", "user-provided employment estimate"),
        _derived("commercial_floor_area", "Commercial floor area", gfa_n, "m²", "development input"),
    ]
    if jobs_n is None: gaps.append("economic:EMPLOYMENT_INPUT")
    if gfa_n is None: gaps.append("economic:COMMERCIAL_GFA_INPUT")

    return {
        "version": "MASTER-185",
        "development": {"type": development_type, "units": units_n, "site_area_ha": area_n, "commercial_gfa_m2": gfa_n},
        "impacts": impacts,
        "impact_summary": {d: {"metric_count": len(impacts[d]), "review_required": any(m["status"] == "REVIEW_REQUIRED" for m in impacts[d])} for d in IMPACT_DOMAINS},
        "source_context": source_context or {},
        "review_gaps": list(dict.fromkeys(gaps)),
        "decision_boundary": "PLANNING_SCREENING_ONLY",
        "statutory_verification": "NOT_CLAIMED",
    }
