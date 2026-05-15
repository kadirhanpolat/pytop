from pytop.hereditary_local_profiles import get_named_hereditary_local_profiles
from pytop.experimental.hereditary_local_profiles import (
    get_named_hereditary_local_profiles as get_wrapper_profiles,
    hereditary_local_chapter32_entry_bridge,
    hereditary_local_lane_summary,
    hereditary_local_quantifier_summary,
    render_hereditary_local_strengthening_report,
)


def test_hereditary_local_registry_has_expected_keys():
    profiles = get_wrapper_profiles()
    keys = {profile.key for profile in profiles}
    assert "global_vs_hereditary_density" in keys
    assert "local_good_global_large_sum" in keys
    assert "second_countable_safe_region" in keys


def test_hereditary_local_registry_quantifier_surfaces_and_lanes_are_curated():
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


def test_hereditary_local_wrapper_matches_core_surface():
    assert get_wrapper_profiles() == get_named_hereditary_local_profiles()


def test_hereditary_local_wrapper_exposes_v078_strengthening_helpers():
    bridge = hereditary_local_chapter32_entry_bridge()
    assert bridge["second_countable_safe_region"] == (
        "character_controls_tightness",
        "network_vs_weight_control",
    )
    assert "Chapter 32 entry bridge" in render_hereditary_local_strengthening_report()
