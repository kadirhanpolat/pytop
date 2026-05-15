from pytop_experimental.research_notebook_registry import (
    get_research_notebook_profiles,
    notebook_profile_summary,
)


def test_research_notebook_registry_has_expected_keys():
    profiles = get_research_notebook_profiles()
    keys = {profile.key for profile in profiles}
    assert keys == {"invariant_experiments", "infinite_spaces_symbolic_support", "advanced_examples"}


def test_research_notebook_registry_covers_volume_three_chapters():
    summary = notebook_profile_summary()
    assert summary["34"] >= 1
    assert summary["35"] >= 1
    assert summary["36"] >= 1


def test_research_notebook_registry_carries_prerequisites_and_usage_notes():
    profiles = get_research_notebook_profiles()
    advanced = next(profile for profile in profiles if profile.key == "advanced_examples")
    assert "Chapter 36" in advanced.prerequisite_topics[-1]
    assert "research-route" in advanced.usage_note
