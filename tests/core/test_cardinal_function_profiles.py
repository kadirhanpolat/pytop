from pytop.cardinal_function_profiles import (
    cardinal_function_chapter_index,
    cardinal_function_layer_summary,
    get_named_cardinal_function_profiles,
)


def test_core_cardinal_function_profiles_have_expected_keys_and_layers():
    profiles = get_named_cardinal_function_profiles()
    keys = {profile.key for profile in profiles}
    assert "character_lindelof_size_bounds" in keys
    assert "compact_hausdorff_improvements" in keys
    assert cardinal_function_layer_summary() == {
        "main_text": 2,
        "selected_block": 2,
        "advanced_note": 1,
    }


def test_core_cardinal_function_profiles_build_chapter_index():
    chapter_index = cardinal_function_chapter_index()
    assert chapter_index["34"][0] == "character_lindelof_size_bounds"
    assert "tightness_network_contribution" in chapter_index["32"]
