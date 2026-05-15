from pytop.compactness_strengthened_profiles import (
    compactness_strengthened_chapter_index,
    compactness_strengthened_layer_summary,
    get_named_compactness_strengthened_profiles,
)


def test_core_compactness_strengthened_profiles_have_expected_keys_and_layers():
    profiles = get_named_compactness_strengthened_profiles()
    keys = {profile.key for profile in profiles}
    assert "compact_lindelof_collapse" in keys
    assert "compact_hausdorff_first_countable_continuum" in keys
    assert "one_point_compactification_bridge" in keys
    assert compactness_strengthened_layer_summary() == {
        "advanced_note": 1,
        "main_text": 2,
        "selected_block": 2,
    }


def test_core_compactness_strengthened_profiles_build_chapter_index():
    chapter_index = compactness_strengthened_chapter_index()
    assert "compact_lindelof_collapse" in chapter_index["31"]
    assert "one_point_compactification_bridge" in chapter_index["22"]
    assert "fine_cardinal_compactness_upgrade" in chapter_index["32"]
