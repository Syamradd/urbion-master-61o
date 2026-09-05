from urbion_what_if import build_scenario_plan


def test_scenario_plan_preserves_baseline_and_applies_only_overrides():
    baseline = {'site_lat': 2.285, 'plot_ratio': 4.5, 'precinct': 'Terminal Sg. Udang'}
    plan = build_scenario_plan(baseline, [{'id': 'LOW', 'name': 'Lower density', 'overrides': {'plot_ratio': 3.5}}])[0]
    assert plan['baseline_inputs'] == baseline
    assert plan['inputs']['plot_ratio'] == 3.5
    assert plan['inputs']['site_lat'] == 2.285
    assert plan['overrides'] == {'plot_ratio': 3.5}
