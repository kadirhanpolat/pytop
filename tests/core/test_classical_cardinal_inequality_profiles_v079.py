from pytop.classical_inequality_profiles import (
    classical_inequality_chapter_index,
    classical_inequality_entry_profiles,
    classical_inequality_lane_summary,
    classical_inequality_layer_summary,
    classical_inequality_prerequisite_bridge,
    classical_inequality_selected_profiles,
    classical_inequality_warning_profiles,
    get_named_classical_inequality_profiles,
    render_classical_inequality_strengthening_report,
)


def test_core_classical_inequality_profiles_have_expected_keys_layers_and_lanes():
    profiles = get_named_classical_inequality_profiles()
    keys = {profile.key for profile in profiles}
    assert keys == {
        "hausdorff_density_character_code",
        "countable_network_continuum_line",
        "lindelof_character_benchmark",
        "compact_hausdorff_character_benchmark",
        "hereditary_local_warning_line",
    }
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


def test_core_classical_inequality_profiles_build_chapter_index_and_bridges():
    chapter_index = classical_inequality_chapter_index()
    bridge = classical_inequality_prerequisite_bridge()
    assert "hausdorff_density_character_code" in chapter_index["34"]
    assert "compact_hausdorff_character_benchmark" in chapter_index["35"]
    assert bridge["countable_network_continuum_line"] == (
        "character_controls_tightness",
        "network_vs_weight_control",
    )
    assert "local_good_global_large_sum" in bridge["hereditary_local_warning_line"]


def test_core_classical_inequality_profiles_expose_entry_selected_and_warning_views():
    assert [profile.key for profile in classical_inequality_entry_profiles()] == [
        "hausdorff_density_character_code",
        "countable_network_continuum_line",
    ]
    assert [profile.key for profile in classical_inequality_selected_profiles()] == [
        "lindelof_character_benchmark",
        "compact_hausdorff_character_benchmark",
    ]
    assert [profile.key for profile in classical_inequality_warning_profiles()] == [
        "hereditary_local_warning_line",
    ]


def test_core_classical_inequality_strengthening_report_names_questionbank_handoff():
    report = render_classical_inequality_strengthening_report()
    assert "Classical cardinal inequalities strengthening" in report
    assert "Prerequisite bridge" in report
    assert "hereditary_local_warning_line" in report
    assert "Questionbank alignment should reuse these lane labels" in report
