from pathlib import Path


def test_shared_ui_controller_has_bilingual_theme_runtime_contract():
    p = Path(__file__).resolve().parents[1] / "urbion_ui.js"
    text = p.read_text(encoding="utf-8")
    assert "urbion-lang" in text
    assert "urbion-theme" in text
    assert "setLang" in text
    assert "setTheme" in text
    assert "dispatchEvent(new CustomEvent('urbion-ui'" in text
    assert "dict={en:" in text
    assert "ms:" in text
    assert "English" in text
    assert "Bahasa Melayu" in text
    assert "Dark" in text
    assert "Light" in text
    assert "System" in text


def test_shared_ui_controller_has_safe_storage_defaults():
    p = Path(__file__).resolve().parents[1] / "urbion_ui.js"
    text = p.read_text(encoding="utf-8")
    assert "||'en'" in text
    assert "||'system'" in text
    assert "eval(" not in text
