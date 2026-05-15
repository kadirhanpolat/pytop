from pytop.research_bridge_profiles import (
    get_named_research_bridge_profiles,
    research_bridge_chapter_index,
    research_bridge_layer_summary,
)


def test_core_research_bridge_profiles_have_expected_keys_and_layers():
    profiles = get_named_research_bridge_profiles()
    keys = {profile.key for profile in profiles}
    assert 'safe_zone_sharpness_route' in keys
    assert 'compactification_upgrade_route' in keys
    assert 'future_threshold_release_route' in keys
    assert research_bridge_layer_summary() == {
        'main_text': 2,
        'selected_block': 2,
        'advanced_note': 1,
    }


def test_core_research_bridge_profiles_build_chapter_index():
    chapter_index = research_bridge_chapter_index()
    assert 'compactification_upgrade_route' in chapter_index['22']
    assert 'future_threshold_release_route' in chapter_index['32']
    assert 'hereditary_local_warning_route' in chapter_index['33']
