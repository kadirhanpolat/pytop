from pytop.compactness_strengthened_profiles import (
    compactness_strengthened_lane_summary,
    get_named_compactness_strengthened_profiles,
)
from pytop.experimental.compactness_strengthened_profiles import (
    compactness_strengthened_entry_profiles,
    compactness_strengthened_prerequisite_bridge,
    compactness_strengthened_selected_profiles,
    compactness_strengthened_warning_profiles,
    get_named_compactness_strengthened_profiles as get_wrapper_profiles,
    render_compactness_strengthened_report,
)


def test_compactness_strengthened_wrapper_matches_v080_core_surface():
    assert get_wrapper_profiles() == get_named_compactness_strengthened_profiles()
    assert compactness_strengthened_lane_summary() == {
        "entry": 2,
        "selected": 2,
        "warning": 1,
    }


def test_compactness_strengthened_wrapper_exposes_lane_helpers_v080():
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
    assert "compact_lindelof_collapse" in compactness_strengthened_prerequisite_bridge()
    assert "Questionbank alignment should reuse these lane labels" in render_compactness_strengthened_report()
