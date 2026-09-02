from pathlib import Path


def test_gis_workspace_contains_spatial_stack():
    html = Path("gis-workspace.html").read_text()
    for token in ("Lot Area", "TOD", "OpenStreetMap", "what-if.html", "evidence-workspace.html"):
        assert token in html


def test_gis_workspace_discloses_demo_geometry():
    html = Path("gis-workspace.html").read_text()
    assert "illustrative until verified" in html
    assert "never converts missing geometry into verified evidence" in html
