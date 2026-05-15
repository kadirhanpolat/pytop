from pytop.compactness_strengthened_profiles import get_named_compactness_strengthened_profiles
from pytop.experimental.compactness_strengthened_profiles import (
    compactness_strengthened_layer_summary,
    get_named_compactness_strengthened_profiles as get_wrapper_profiles,
)


def test_compactness_strengthened_registry_has_expected_keys():
    profiles = get_named_compactness_strengthened_profiles()
    keys = {profile.key for profile in profiles}
    assert "compact_lindelof_collapse" in keys
    assert "compact_hausdorff_first_countable_continuum" in keys
    assert "one_point_compactification_bridge" in keys


def test_compactness_strengthened_registry_layers_are_curated():
    assert compactness_strengthened_layer_summary() == {
        "advanced_note": 1,
        "main_text": 2,
        "selected_block": 2,
    }


def test_compactness_strengthened_wrapper_matches_core_surface():
    assert get_wrapper_profiles() == get_named_compactness_strengthened_profiles()
