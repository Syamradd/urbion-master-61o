from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_ui_repair_asset_exists_and_covers_live_qa_gaps():
    js = (ROOT / 'urbion_championship_ui_repair.js').read_text(encoding='utf-8')
    for token in ('STREET','SATELLITE','HYBRID','CASE HISTORY','FINAL COMMAND','station-intelligence','copilot/run','Guna Tanah 2','Guna Tanah 3','Selected site'):
        assert token in js
