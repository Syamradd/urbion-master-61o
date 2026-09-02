"""Indicative development-intensity analytics for URBION."""
from __future__ import annotations
from typing import Any


def development_intensity(*, area_m2: float | None, plot_ratio: float | None) -> dict[str, Any]:
    """Calculate indicative GFA from verified/supplied lot area and plot ratio.

    This is a planning-analysis metric, not a statutory approval calculation.
    """
    if area_m2 is None or area_m2 <= 0:
        return {"lot_area_m2": None, "plot_ratio": plot_ratio, "indicative_gfa_m2": None, "status": "EVIDENCE REQUIRED"}
    if plot_ratio is None or plot_ratio <= 0:
        return {"lot_area_m2": round(float(area_m2), 2), "plot_ratio": None, "indicative_gfa_m2": None, "status": "EVIDENCE REQUIRED"}
    gfa = float(area_m2) * float(plot_ratio)
    return {
        "lot_area_m2": round(float(area_m2), 2),
        "plot_ratio": float(plot_ratio),
        "indicative_gfa_m2": round(gfa, 2),
        "status": "INDICATIVE",
    }


def intensity_band(*, plot_ratio: float | None) -> str:
    """Describe relative intensity without asserting a statutory threshold."""
    if plot_ratio is None or plot_ratio <= 0:
        return "UNKNOWN"
    if plot_ratio <= 2:
        return "LOW"
    if plot_ratio <= 4:
        return "MODERATE"
    return "HIGH"
