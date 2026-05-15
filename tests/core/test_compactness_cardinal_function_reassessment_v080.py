from pytop.compactness_strengthened_profiles import (
    compactness_strengthened_entry_profiles,
    compactness_strengthened_lane_summary,
    compactness_strengthened_prerequisite_bridge,
    compactness_strengthened_selected_profiles,
    compactness_strengthened_warning_profiles,
    render_compactness_strengthened_report,
)


def test_compactness_strengthened_lane_split_and_selectors_v080():
    assert compactness_strengthened_lane_summary() == {
        "entry": 2,
        "selected": 2,
        "warning": 1,
    }
    assert {profile.key for profile in compactness_strengthened_entry_profiles()} == {
        "compact_lindelof_collapse",
        "compact_hausdorff_first_countable_continuum",
    }
    assert {profile.key for profile in compactness_strengthened_selected_profiles()} == {
        "one_point_compactification_bridge",
        "fine_cardinal_compactness_upgrade",
    }
    assert [profile.key for profile in compactness_strengthened_warning_profiles()] == [
        "countably_compact_warning_omega1"
    ]


def test_compactness_strengthened_prerequisite_bridge_and_report_v080():
    bridge = compactness_strengthened_prerequisite_bridge()
    assert bridge["compact_hausdorff_first_countable_continuum"] == (
        "compact_hausdorff_character_benchmark",
    )
    assert bridge["fine_cardinal_compactness_upgrade"] == (
        "compact_hausdorff_first_countable_continuum",
        "countably_compact_warning_omega1",
    )
    report = render_compactness_strengthened_report()
    assert "Questionbank alignment should reuse these lane labels" in report
    assert "countably_compact_warning_omega1" in report
