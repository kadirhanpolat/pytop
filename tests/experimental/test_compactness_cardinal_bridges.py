from pytop.compactness_bridges import get_named_compactness_bridge_profiles as get_core_profiles
from pytop.experimental.compactness_cardinal_bridges import (
    compactness_bridge_layer_summary,
    get_named_compactness_bridge_profiles,
)


def test_compactness_bridge_registry_has_expected_keys():
    profiles = get_named_compactness_bridge_profiles()
    keys = {profile.key for profile in profiles}
    assert "compact_hausdorff_size_improvements" in keys
    assert "countably_compact_warning_line" in keys
    assert "lindelof_to_compactness_transition" in keys


def test_compactness_bridge_layers_are_curated():
    assert compactness_bridge_layer_summary() == {
        "main_text": 2,
        "selected_block": 2,
        "advanced_note": 1,
    }


def test_compactness_bridge_wrapper_matches_core_surface():
    assert get_named_compactness_bridge_profiles() == get_core_profiles()
