from pathlib import Path

from fastapi.testclient import TestClient

from championship_server import app


def test_production_root_is_championship_workstation():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "URBION HORIZON — Championship Workstation" in response.text
    assert 'id="urbion-championship"' in response.text
    assert "/urbion_championship_ui.js" in response.text
    assert "/urbion_championship_upgrade.js" in response.text
    assert "Site + Development Inputs" not in response.text


def test_championship_assets_are_served_from_same_app():
    client = TestClient(app)
    for asset in ("urbion_ui.js", "urbion_championship_ui.js", "urbion_championship_upgrade.js"):
        response = client.get(f"/{asset}")
        assert response.status_code == 200, asset
        assert response.headers["content-type"].startswith("application/javascript")


def test_championship_html_exists():
    assert (Path(__file__).resolve().parent / "championship.html").is_file()
