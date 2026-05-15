from pytop.special_example_profiles import (
    get_named_special_example_profiles,
    special_example_chapter_index,
    special_example_role_summary,
    special_example_route_index,
)


def test_special_example_profiles_have_expected_keys_and_roles():
    profiles = get_named_special_example_profiles()
    keys = {profile.key for profile in profiles}
    assert 'safe_zone_benchmark_space' in keys
    assert 'local_small_global_large_warning_space' in keys
    assert 'registry_alignment_demo_space' in keys
    assert special_example_role_summary() == {
        'safe_zone': 1,
        'warning_line': 1,
        'upgrade_route': 1,
        'counterexample_anchor': 1,
        'inventory_demo': 1,
    }


def test_special_example_profiles_index_chapters_and_routes():
    chapter_index = special_example_chapter_index()
    assert '33' in chapter_index
    assert '36' in chapter_index
    route_index = special_example_route_index()
    assert route_index['counterexample_search_route'] == (
        'local_small_global_large_warning_space',
        'countably_compact_warning_anchor',
    )
    assert 'module_and_research_inventory' in route_index
