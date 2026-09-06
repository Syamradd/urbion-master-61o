from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_ux_v3_design_contract_is_preserved_in_current_premium_stack():
    legacy = (ROOT / 'urbion_championship_ux_v3.js').read_text(encoding='utf-8')
    premium_v3 = (ROOT / 'urbion_championship_premium_v3.js').read_text(encoding='utf-8')
    premium_v4 = (ROOT / 'urbion_championship_premium_v4.js').read_text(encoding='utf-8')
    final = (ROOT / 'urbion_championship_final_command_center.js').read_text(encoding='utf-8')
    for token in ('01 · START / CASE', '02 · MAP / EVIDENCE', '03 · WHAT-IF', '04 · DECISION / LCP', 'Land use category', 'Land use activity', 'Development / proposal type'):
        assert token in legacy or token in final
    for token in ('screening', '400', '800', '1000', '1500', 'reduced motion'):
        assert token.lower() in premium_v3.lower() or token.lower() in premium_v4.lower()
    assert 'setOpacity' in legacy
    assert "urbion-workstation-v2" in legacy
    assert "urbion-decision-os" in legacy


def test_current_premium_stack_is_wired_and_release_identity_is_preserved():
    server = (ROOT / 'championship_server.py').read_text(encoding='utf-8')
    assert 'urbion_championship_premium_v3.js' in server
    assert 'urbion_championship_premium_v4.js' in server
    assert 'app.state.frontend_release="MASTER-331"' in server
