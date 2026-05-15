from pytop.cardinal_function_profiles import get_named_cardinal_function_profiles
from pytop_experimental.advanced_cardinal_functions import (
    get_named_inequality_profiles,
    inequality_profile_layer_summary,
)


def test_advanced_cardinal_functions_registry_has_expected_keys():
    profiles = get_named_inequality_profiles()
    keys = {profile.key for profile in profiles}
    assert "character_lindelof_size_bounds" in keys
    assert "tightness_network_contribution" in keys
    assert "compact_hausdorff_improvements" in keys


def test_advanced_cardinal_functions_layers_are_curated():
    assert inequality_profile_layer_summary() == {
        "main_text": 2,
        "selected_block": 2,
        "advanced_note": 1,
    }


def test_advanced_cardinal_functions_wrapper_matches_core_surface():
    assert get_named_inequality_profiles() == get_named_cardinal_function_profiles()
