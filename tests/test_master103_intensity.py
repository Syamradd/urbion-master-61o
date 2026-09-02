from urbion_development_intensity import development_intensity, intensity_band


def test_gfa_from_lot_area_and_plot_ratio():
    result = development_intensity(area_m2=5000, plot_ratio=4.5)
    assert result["indicative_gfa_m2"] == 22500.0
    assert result["status"] == "INDICATIVE"


def test_missing_area_requires_evidence():
    result = development_intensity(area_m2=None, plot_ratio=4.5)
    assert result["indicative_gfa_m2"] is None
    assert result["status"] == "EVIDENCE REQUIRED"


def test_intensity_band_is_descriptive_only():
    assert intensity_band(plot_ratio=1.5) == "LOW"
    assert intensity_band(plot_ratio=3) == "MODERATE"
    assert intensity_band(plot_ratio=5) == "HIGH"
