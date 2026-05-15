from pytop.compactness_bridges import (
    compactness_bridge_chapter_index,
    compactness_bridge_layer_summary,
    get_named_compactness_bridge_profiles,
)


def test_core_compactness_bridges_have_expected_keys_and_layers():
    profiles = get_named_compactness_bridge_profiles()
    keys = {profile.key for profile in profiles}
    assert "compact_hausdorff_size_improvements" in keys
    assert "lindelof_to_compactness_transition" in keys
    assert compactness_bridge_layer_summary() == {
        "main_text": 2,
        "selected_block": 2,
        "advanced_note": 1,
    }


def test_core_compactness_bridges_build_chapter_index():
    chapter_index = compactness_bridge_chapter_index()
    assert "countably_compact_warning_line" in chapter_index["31"]
    assert "fine_cardinal_compactness_questions" in chapter_index["32"]
