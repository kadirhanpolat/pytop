from pytop.tightness_network_profiles import (
    get_named_tightness_network_profiles,
    render_tightness_network_lane_report,
    tightness_network_advanced_profiles,
    tightness_network_chapter_index,
    tightness_network_entry_advanced_split,
    tightness_network_entry_profiles,
    tightness_network_lane_summary,
    tightness_network_layer_summary,
)


def test_core_tightness_network_profiles_have_expected_keys_layers_and_lanes():
    profiles = get_named_tightness_network_profiles()
    keys = {profile.key for profile in profiles}
    assert "character_controls_tightness" in keys
    assert "network_vs_weight_control" in keys
    assert "sequential_warning_surface" in keys
    assert tightness_network_layer_summary() == {
        "main_text": 2,
        "selected_block": 1,
        "advanced_note": 1,
    }
    assert tightness_network_lane_summary() == {"entry": 3, "advanced": 1}


def test_core_tightness_network_profiles_build_chapter_index():
    chapter_index = tightness_network_chapter_index()
    assert chapter_index["32"][0] == "character_controls_tightness"
    assert "sequential_warning_surface" in chapter_index["36"]


def test_core_tightness_network_entry_advanced_split_is_explicit():
    split = tightness_network_entry_advanced_split()
    assert split["entry"] == (
        "character_controls_tightness",
        "network_vs_weight_control",
        "discrete_extreme_behavior",
    )
    assert split["advanced"] == ("sequential_warning_surface",)
    assert [profile.key for profile in tightness_network_entry_profiles()] == list(split["entry"])
    assert [profile.key for profile in tightness_network_advanced_profiles()] == list(split["advanced"])


def test_core_tightness_network_lane_report_mentions_warning_delay():
    report = render_tightness_network_lane_report()
    assert "Tightness/network teaching-lane split" in report
    assert "entry: character_controls_tightness" in report
    assert "advanced: sequential_warning_surface" in report
    assert "delays sequential warning-lines" in report
