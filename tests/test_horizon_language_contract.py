from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_language_contract_is_loaded_before_horizon_ui():
    server = (ROOT / "championship_server.py").read_text(encoding="utf-8")
    lang = '<script src="/urbion_horizon_language_contract.js"></script>'
    horizon = '<script src="/urbion_championship_horizon_ui.js"></script>'
    assert lang in server
    assert server.index(lang) < server.index(horizon)


def test_language_contract_has_persistent_global_switch():
    js = (ROOT / "urbion_horizon_language_contract.js").read_text(encoding="utf-8")
    required = [
        "window.__URBION_HORIZON_LANG_CONTRACT__=true",
        "localStorage.getItem('urbion-language')",
        "localStorage.setItem('urbion-language'",
        "window.__URBION_HORIZON_SET_LANG__",
        "document.documentElement.lang=ms?'ms':'en'",
        "stopImmediatePropagation",
    ]
    for marker in required:
        assert marker in js, marker


def test_default_interface_copy_is_english_first():
    js = (ROOT / "urbion_horizon_language_contract.js").read_text(encoding="utf-8")
    assert "let lang=(localStorage.getItem('urbion-language')||'en')" in js
    assert "lang==='ms'?'ms':'en'" in js


def test_key_planning_labels_have_both_language_forms():
    js = (ROOT / "urbion_horizon_language_contract.js").read_text(encoding="utf-8")
    for marker in (
        "'Command Centre':'Pusat Kawalan'",
        "'Site Intelligence':'Kecerdasan Tapak'",
        "'AI Assessment':'Penilaian AI'",
        "'What-If Studio':'Studio Bagaimana Jika'",
        "'Decision Centre':'Pusat Keputusan'",
        "'LCP Intelligence':'Kecerdasan LCP'",
        "'RUN SITE ANALYSIS':'JALANKAN ANALISIS TAPAK'",
        "'MAP LAYERS':'LAPISAN PETA'",
        "'Current Land Use':'Guna Tanah Semasa'",
        "'Zoning':'Zon Guna Tanah'",
    ):
        assert marker in js, marker
