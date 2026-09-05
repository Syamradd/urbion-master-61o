from urbion_what_if import execute_what_if


def _inputs():
    return {
        "site_lat": 2.2, "site_lon": 102.2,
        "tod_lat": 2.21, "tod_lon": 102.21,
        "land_use": "residential", "density": 120,
    }


def test_what_if_preserves_raw_baseline_inputs_and_returns_comparison():
    baseline = _inputs()
    before = dict(baseline)
    result = execute_what_if(
        baseline,
        [{"name": "Higher density", "overrides": {"density": 180}}],
    )
    assert baseline == before
    assert result["baseline_inputs"] == before
    assert result["scenarios"]
    assert result["scenarios"][0]["inputs"]["density"] == 180
    assert result["scenarios"][0]["inputs"] != baseline


def test_what_if_accepts_multiple_variants_deterministically():
    variants = [
        {"name": "Base-plus", "overrides": {"density": 130}},
        {"name": "Lower", "overrides": {"density": 90}},
    ]
    a = execute_what_if(_inputs(), variants)
    b = execute_what_if(_inputs(), variants)
    assert a == b
    assert len(a["scenarios"]) == 2
