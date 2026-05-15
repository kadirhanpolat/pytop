from pytop.hereditary_local_profiles import (
    get_named_hereditary_local_profiles,
    hereditary_local_chapter32_entry_bridge,
    hereditary_local_chapter_index,
    hereditary_local_entry_profiles,
    hereditary_local_lane_summary,
    hereditary_local_quantifier_summary,
    hereditary_local_warning_profiles,
    render_hereditary_local_strengthening_report,
)


def test_core_hereditary_local_profiles_have_expected_keys_surfaces_and_lanes():
    profiles = get_named_hereditary_local_profiles()
    keys = {profile.key for profile in profiles}
    assert "global_vs_hereditary_density" in keys
    assert "local_good_global_large_sum" in keys
    assert "second_countable_safe_region" in keys
    assert hereditary_local_quantifier_summary() == {
        "hereditary": 2,
        "local_warning": 1,
        "safe_region": 1,
    }
    assert hereditary_local_lane_summary() == {
        "bridge": 2,
        "warning": 1,
        "entry": 1,
    }


def test_core_hereditary_local_profiles_build_chapter_index():
    chapter_index = hereditary_local_chapter_index()
    assert chapter_index["33"][0] == "global_vs_hereditary_density"
    assert "local_good_global_large_sum" in chapter_index["34"]


def test_core_hereditary_local_profiles_expose_entry_and_warning_lanes():
    entry_keys = [profile.key for profile in hereditary_local_entry_profiles()]
    warning_keys = [profile.key for profile in hereditary_local_warning_profiles()]
    assert entry_keys == ["second_countable_safe_region"]
    assert warning_keys == ["local_good_global_large_sum"]
    assert all(profile.has_chapter32_entry_bridge for profile in get_named_hereditary_local_profiles())


def test_core_hereditary_local_chapter32_bridge_is_explicit():
    bridge = hereditary_local_chapter32_entry_bridge()
    assert bridge["second_countable_safe_region"] == (
        "character_controls_tightness",
        "network_vs_weight_control",
    )
    assert "discrete_extreme_behavior" in bridge["global_vs_hereditary_density"]
    assert "character_controls_tightness" in bridge["local_good_global_large_sum"]


def test_core_hereditary_local_strengthening_report_names_next_handoff():
    report = render_hereditary_local_strengthening_report()
    assert "Hereditary/local cardinal-function strengthening" in report
    assert "Chapter 32 entry bridge" in report
    assert "second_countable_safe_region" in report
    assert "Chapter 34" in report
