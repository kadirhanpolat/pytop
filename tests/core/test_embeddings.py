"""Tests for pytop.embeddings -- EMB-01."""

from pytop.embeddings import (
    AlexanderHornedSphereProfile,
    EmbeddingProfile,
    JordanCurveProfile,
    embedding_profile_registry,
    embedding_status_summary,
    get_alexander_horned_sphere_profiles,
    get_embedding_profiles,
    get_jordan_curve_profiles,
)


def test_embedding_profiles_return_turkish_records():
    profiles = get_embedding_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 3
    assert all(isinstance(p, EmbeddingProfile) for p in profiles)
    assert any("gömü" in p.display_name.lower() for p in profiles)


def test_embedding_profiles_have_embedding_and_non_embedding_examples():
    summary = embedding_status_summary()
    assert "embedding" in summary
    assert "not_embedding" in summary
    assert len(summary["embedding"]) >= 2
    assert len(summary["not_embedding"]) >= 1


def test_figure_eight_is_not_embedding():
    profiles = {p.key: p for p in get_embedding_profiles()}
    profile = profiles["figure_eight_immersion_not_embedding"]
    assert profile.is_embedding is False
    assert "birebir" in profile.teaching_note


def test_jordan_curve_profiles_state_two_regions():
    profiles = get_jordan_curve_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 2
    assert all(isinstance(p, JordanCurveProfile) for p in profiles)
    assert all("iç" in p.inside_region.lower() or "disk" in p.inside_region.lower()
               for p in profiles)
    assert all("dış" in p.outside_region.lower() for p in profiles)


def test_standard_circle_jordan_curve_mentions_two_components():
    profiles = {p.key: p for p in get_jordan_curve_profiles()}
    profile = profiles["standard_circle_jordan_curve"]
    assert "iki bileşen" in profile.theorem_statement
    assert "Jordan" in profile.display_name


def test_alexander_horned_sphere_profile_is_wild():
    profiles = get_alexander_horned_sphere_profiles()
    assert len(profiles) == 1
    profile = profiles[0]
    assert isinstance(profile, AlexanderHornedSphereProfile)
    assert profile.tame_or_wild == "wild"
    assert "vahşi" in profile.display_name.lower() or "vahşi" in profile.teaching_note.lower()


def test_embedding_registry_counts_match_getters():
    registry = embedding_profile_registry()
    assert registry["embedding_profiles"] == len(get_embedding_profiles())
    assert registry["jordan_curve_profiles"] == len(get_jordan_curve_profiles())
    assert registry["alexander_horned_sphere_profiles"] == len(
        get_alexander_horned_sphere_profiles()
    )
    assert sum(registry.values()) >= 6
