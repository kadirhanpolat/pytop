from pytop.metrization_profiles import get_named_metrization_profiles
from pytop_experimental.advanced_metrization import (
    get_named_metrization_profiles as get_wrapper_profiles,
    metrization_chapter_index,
    metrization_layer_summary,
)


def test_advanced_metrization_wrapper_exposes_promoted_profiles():
    profiles = get_wrapper_profiles()
    keys = {profile.key for profile in profiles}
    assert 'urysohn_second_countable_regular_route' in keys
    assert 'compact_hausdorff_second_countable_route' in keys
    assert 'moore_developable_regular_route' in keys


def test_advanced_metrization_wrapper_matches_core_surface():
    assert get_wrapper_profiles() == get_named_metrization_profiles()
    assert metrization_layer_summary() == {
        'main_text': 1,
        'selected_block': 1,
        'advanced_note': 1,
    }
    assert 'urysohn_second_countable_regular_route' in metrization_chapter_index()['23']
