from pathlib import Path

from fastapi.testclient import TestClient

from championship_server import app


def test_public_root_is_landing_and_championship_is_workstation():
    client = TestClient(app)
    root = client.get("/")
    assert root.status_code == 200
    assert '<title>URBION HORIZON — Spatial Decision Intelligence</title>' in root.text
    assert 'href="/championship.html"' in root.text

    response = client.get("/championship.html")
    assert response.status_code == 200
    assert '<title>URBION HORIZON — Planning Command Centre</title>' in response.text
    assert 'id="urbion-championship-shell"' in response.text
    assert 'window.__URBION_FRONTEND_BOOT__' in response.text
    assert 'release:"MASTER-331"' in response.text
    assert "/urbion_championship_command_shell.js" in response.text
    assert "/urbion_map_identify_runtime.js" in response.text
    assert "/urbion_championship_horizon_ui.js" in response.text
    assert "Site + Development Inputs" not in response.text


def test_championship_assets_are_served_from_same_app():
    client = TestClient(app)
    for asset in (
        "urbion_ui.js",
        "urbion_championship_ui.js",
        "urbion_championship_upgrade.js",
        "urbion_championship_command_shell.js",
        "urbion_map_identify_runtime.js",
        "urbion_championship_horizon_ui.js",
    ):
        response = client.get(f"/{asset}")
        assert response.status_code == 200, asset
        assert response.headers["content-type"].startswith("application/javascript")


def test_championship_html_exists():
    assert (Path(__file__).resolve().parent / "championship.html").is_file()
