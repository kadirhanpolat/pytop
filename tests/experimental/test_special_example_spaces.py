from pytop.experimental.special_example_spaces import (
    get_named_special_example_profiles,
    special_example_chapter_index,
    special_example_role_summary,
)


def test_special_example_wrapper_exposes_promoted_registry():
    profiles = get_named_special_example_profiles()
    assert len(profiles) == 5
    compactness = next(profile for profile in profiles if profile.key == 'compactification_upgrade_benchmark_space')
    assert compactness.example_role == 'upgrade_route'
    assert compactness.example_bank_file == 'compactness_cardinal_functions_examples.md'
    assert 'compactness_variant_comparison' in compactness.research_path_keys
    assert special_example_role_summary()['warning_line'] == 1
    assert '36' in special_example_chapter_index()
