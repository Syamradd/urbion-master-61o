from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_final_workspace_and_source_contracts_exist():
    server = (ROOT / "championship_server.py").read_text(encoding="utf-8")
    v7 = (ROOT / "urbion_championship_premium_v7.js").read_text(encoding="utf-8")
    about = (ROOT / "about.html").read_text(encoding="utf-8")

    assert '"/about.html"' in server
    assert 'CANONICAL_ASSET = "urbion_championship_command_shell.js"' in server
    assert 'payload += "\\n" + companion.read_text' in server
    assert "https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN/" in v7
    for token in ("GTsemasa", "GTzoning", "KONTUR5M", "LOT", "STATE_CODES", "SOURCE UNAVAILABLE"):
        assert token in v7
    assert "Turning spatial evidence into" in about


def test_finalization_does_not_expose_temporary_probe_files():
    probe_files = list(ROOT.glob("tmp_probe*.js"))
    assert probe_files == []
