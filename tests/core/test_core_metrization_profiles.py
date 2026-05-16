from pytop.metrization_profiles import (
    get_named_metrization_profiles,
    metrization_chapter_index,
    metrization_layer_summary,
)


def test_core_metrization_profiles_have_expected_keys_and_layers():
    profiles = get_named_metrization_profiles()
    keys = {profile.key for profile in profiles}
    assert {
        'urysohn_second_countable_regular_route',
        'compact_hausdorff_second_countable_route',
        'moore_developable_regular_route',
        'nagata_smirnov_sigma_lf_base_route',
        'bing_sigma_discrete_base_route',
    } <= keys
    summary = metrization_layer_summary()
    assert summary.get('main_text', 0) >= 1
    assert summary.get('selected_block', 0) >= 1
    assert summary.get('advanced_note', 0) >= 1


def test_core_metrization_profiles_build_chapter_index():
    chapter_index = metrization_chapter_index()
    assert 'urysohn_second_countable_regular_route' in chapter_index['23']
    assert 'compact_hausdorff_second_countable_route' in chapter_index['14']
    assert 'moore_developable_regular_route' in chapter_index['36']
