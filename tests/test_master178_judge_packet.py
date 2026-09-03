from pathlib import Path


def test_final_judge_packet_covers_championship_path():
    text = Path('MASTER-178-FINAL-JUDGE-PACKET.md').read_text(encoding='utf-8')
    for token in ['Site Assessment', 'Map Studio', 'Evidence', 'What-If', 'Decision Center', 'Planner Review', 'KM/OSC']:
        assert token in text
    assert 'statutory approval remains outside URBION' in text
    assert 'Actual GitHub Actions success' in text
