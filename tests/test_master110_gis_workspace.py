from pathlib import Path


def test_gis_workspace_exposes_required_spatial_layers():
    text = Path("gis-workspace.html").read_text(encoding="utf-8")
    for label in ("Parcel / Lot", "Land Use", "Zoning", "TOD 400m / 800m", "Decision"):
        assert label in text
    assert "5,000 m²" in text
    assert "0.5000 ha" in text


def test_gis_workspace_discloses_evidence_limitations():
    text = Path("gis-workspace.html").read_text(encoding="utf-8")
    assert "demonstration layers" in text
    assert "not treated as statutory evidence" in text
