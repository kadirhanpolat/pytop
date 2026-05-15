from pytop.tightness_network_profiles import get_named_tightness_network_profiles
from pytop.experimental.tightness_network_profiles import (
    get_named_tightness_network_profiles as get_wrapper_profiles,
    render_tightness_network_lane_report,
    tightness_network_entry_advanced_split,
    tightness_network_lane_summary,
    tightness_network_layer_summary,
)


def test_tightness_network_registry_has_expected_keys():
    profiles = get_wrapper_profiles()
    keys = {profile.key for profile in profiles}
    assert "character_controls_tightness" in keys
    assert "network_vs_weight_control" in keys
    assert "sequential_warning_surface" in keys


def test_tightness_network_registry_layers_and_lanes_are_curated():
    assert tightness_network_layer_summary() == {
        "main_text": 2,
        "selected_block": 1,
        "advanced_note": 1,
    }
    assert tightness_network_lane_summary() == {"entry": 3, "advanced": 1}
    assert tightness_network_entry_advanced_split()["advanced"] == ("sequential_warning_surface",)


def test_tightness_network_wrapper_matches_core_surface():
    assert get_wrapper_profiles() == get_named_tightness_network_profiles()
    assert "entry:" in render_tightness_network_lane_report()
