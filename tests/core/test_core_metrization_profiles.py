from pytop.metrization_profiles import (
    get_named_metrization_profiles,
    metrization_chapter_index,
    metrization_layer_summary,
)


def test_core_metrization_profiles_have_expected_keys_and_layers():
    profiles = get_named_metrization_profiles()
    keys = {profile.key for profile in profiles}
    assert keys == {
        'urysohn_second_countable_regular_route',
        'compact_hausdorff_second_countable_route',
        'moore_developable_regular_route',
    }
    assert metrization_layer_summary() == {
        'main_text': 1,
        'selected_block': 1,
        'advanced_note': 1,
    }


def test_core_metrization_profiles_build_chapter_index():
    chapter_index = metrization_chapter_index()
    assert 'urysohn_second_countable_regular_route' in chapter_index['23']
    assert 'compact_hausdorff_second_countable_route' in chapter_index['14']
    assert 'moore_developable_regular_route' in chapter_index['36']
