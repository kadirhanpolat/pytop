from pytop_experimental.theorem_drafts import (
    benchmark_class_summary,
    chapter_draft_summary,
    get_named_theorem_draft_profiles,
)


def test_theorem_draft_registry_has_expected_keys_and_split():
    profiles = get_named_theorem_draft_profiles()
    keys = {profile.key for profile in profiles}
    assert 'hausdorff_density_character_bound' in keys
    assert 'compact_first_countable_continuum_bound' in keys
    summary = benchmark_class_summary()
    assert summary == {'proved_main_text': 4, 'selected_block': 1, 'warning_line': 2}


def test_theorem_draft_registry_spans_chapters_32_to_35():
    summary = chapter_draft_summary()
    assert summary['32'] == 1
    assert summary['33'] == 2
    assert summary['34'] == 2
    assert summary['35'] == 2
