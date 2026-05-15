from pytop.research_path_profiles import (
    get_named_research_path_profiles,
    research_path_chapter_index,
    research_path_layer_summary,
    research_path_route_index,
)


def test_research_path_profiles_have_expected_keys_and_cross_links():
    profiles = get_named_research_path_profiles()
    keys = {profile.key for profile in profiles}
    assert 'hypothesis_sensitivity_of_size_bounds' in keys
    assert 'compactness_variant_comparison' in keys
    assert 'module_and_research_inventory' in keys

    compactness = next(profile for profile in profiles if profile.key == 'compactness_variant_comparison')
    assert 'compactification_upgrade_route' in compactness.bridge_route_keys
    assert 'countably_compact_warning_anchor' in compactness.special_example_keys
    assert 'compact_lindelof_transition' in compactness.theorem_alignment_keys


def test_research_path_profiles_index_layers_chapters_and_routes():
    assert research_path_layer_summary() == {
        'main_text': 2,
        'selected_block': 2,
        'advanced_note': 1,
    }
    chapter_index = research_path_chapter_index()
    assert '36' in chapter_index
    route_index = research_path_route_index()
    assert 'fine_cardinal_warning_lines' in route_index['local_small_global_large_warning_space']
    assert 'module_and_research_inventory' in route_index['registry_alignment_demo_space']
