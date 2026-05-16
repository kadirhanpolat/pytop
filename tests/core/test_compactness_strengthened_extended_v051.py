"""Coverage-targeted tests for compactness_strengthened_profiles.py (v0.5.1)."""
from pytop.compactness_strengthened_profiles import (
    CompactnessStrengthenedProfile,
    get_named_compactness_strengthened_profiles,
)


# ---------------------------------------------------------------------------
# writing_layer property — line 33 (backward-compatible alias)
# ---------------------------------------------------------------------------

def test_writing_layer_alias():
    profiles = get_named_compactness_strengthened_profiles()
    assert len(profiles) > 0
    p = profiles[0]
    assert p.writing_layer == p.presentation_layer


def test_writing_layer_direct():
    p = CompactnessStrengthenedProfile(
        key="test_key",
        display_name="Test",
        compactness_family="compact",
        presentation_layer="main_text",
        teaching_lane="entry",
        focus="testing the alias",
        chapter_targets=("35",),
        prerequisite_profile_keys=(),
        benchmark_question="Is writing_layer == presentation_layer?",
    )
    assert p.writing_layer == "main_text"
