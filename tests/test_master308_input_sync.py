from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_input_sync_asset_is_present_and_covers_site_contract():
    text = (ROOT / 'urbion_championship_input_sync.js').read_text(encoding='utf-8')
    for token in [
        "['lat','lon','todlat','todlon','state','pbt','devtype','devclass','ratio','lot']",
        "urbion:site-change",
        "urbion:inputs-change",
        "urbion:inputs-ready",
        "side-status",
        "Run analysis to refresh the decision chain",
    ]:
        assert token in text
    assert 'fetch(' not in text
    assert 'location.origin' not in text


def test_championship_server_wires_input_sync_asset():
    text = (ROOT / 'championship_server.py').read_text(encoding='utf-8')
    assert 'urbion_championship_input_sync.js' in text
    assert 'ALLOWED_ASSETS' in text
