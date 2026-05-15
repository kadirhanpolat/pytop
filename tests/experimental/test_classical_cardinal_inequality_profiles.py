from pytop.classical_inequality_profiles import get_named_classical_inequality_profiles
from pytop_experimental.classical_inequality_profiles import (
    classical_inequality_entry_profiles,
    classical_inequality_lane_summary,
    classical_inequality_layer_summary,
    classical_inequality_prerequisite_bridge,
    get_named_classical_inequality_profiles as get_wrapper_profiles,
    render_classical_inequality_strengthening_report,
)


def test_classical_inequality_wrapper_matches_core_surface():
    assert get_wrapper_profiles() == get_named_classical_inequality_profiles()


def test_classical_inequality_wrapper_exposes_v079_strengthening_helpers():
    assert classical_inequality_layer_summary() == {
        "main_text": 2,
        "selected_block": 2,
        "advanced_note": 1,
    }
    assert classical_inequality_lane_summary() == {
        "entry": 2,
        "selected": 2,
        "warning": 1,
    }
    assert [profile.key for profile in classical_inequality_entry_profiles()] == [
        "hausdorff_density_character_code",
        "countable_network_continuum_line",
    ]
    assert "global_vs_hereditary_density" in classical_inequality_prerequisite_bridge()[
        "hereditary_local_warning_line"
    ]
    assert "Questionbank alignment should reuse these lane labels" in render_classical_inequality_strengthening_report()
