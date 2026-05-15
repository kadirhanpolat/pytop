"""Tests for pytop.degree_theory -- DEG-01."""

from pytop.degree_theory import (
    CircleDegreeProfile,
    RetractionDegreeProfile,
    circle_degree_by_value,
    circle_degree_summary,
    degree_theory_profile_registry,
    get_circle_degree_profiles,
    get_retraction_degree_profiles,
    retraction_degree_summary,
)


def test_circle_degree_profiles_returns_tuple():
    profiles = get_circle_degree_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 4
    assert all(isinstance(p, CircleDegreeProfile) for p in profiles)


def test_circle_degree_profiles_have_unique_keys():
    keys = [p.key for p in get_circle_degree_profiles()]
    assert len(keys) == len(set(keys))


def test_circle_degree_profiles_are_frozen():
    profile = get_circle_degree_profiles()[0]
    try:
        profile.key = "mutated"  # type: ignore[misc]
        assert False
    except Exception:
        pass


def test_identity_has_degree_one():
    profiles = {p.key: p for p in get_circle_degree_profiles()}
    profile = profiles["identity_circle_degree_one"]
    assert profile.degree == 1
    assert profile.orientation_behavior == "orientation_preserving"
    assert "n |-> n" in profile.induced_fundamental_group_map


def test_constant_map_has_degree_zero():
    profiles = {p.key: p for p in get_circle_degree_profiles()}
    profile = profiles["constant_circle_degree_zero"]
    assert profile.degree == 0
    assert profile.homotopy_class == "null_homotopic"


def test_power_map_has_degree_two():
    profiles = {p.key: p for p in get_circle_degree_profiles()}
    profile = profiles["power_map_degree_two"]
    assert profile.degree == 2
    assert "2n" in profile.induced_fundamental_group_map


def test_conjugation_has_negative_degree():
    profiles = {p.key: p for p in get_circle_degree_profiles()}
    profile = profiles["conjugation_degree_minus_one"]
    assert profile.degree == -1
    assert profile.orientation_behavior == "orientation_reversing"


def test_circle_degree_by_value_filters_profiles():
    degree_two = circle_degree_by_value(2)
    assert len(degree_two) == 1
    assert degree_two[0].key == "power_map_degree_two"


def test_circle_degree_summary_groups_all_profiles():
    summary = circle_degree_summary()
    total = sum(len(keys) for keys in summary.values())
    assert total == len(get_circle_degree_profiles())
    assert "orientation_reversing" in summary


def test_retraction_degree_profiles_returns_tuple():
    profiles = get_retraction_degree_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 3
    assert all(isinstance(p, RetractionDegreeProfile) for p in profiles)


def test_retraction_degree_profiles_have_unique_keys():
    keys = [p.key for p in get_retraction_degree_profiles()]
    assert len(keys) == len(set(keys))


def test_disk_to_circle_has_degree_obstruction():
    profiles = {p.key: p for p in get_retraction_degree_profiles()}
    profile = profiles["disk_to_circle_no_retraction"]
    assert profile.retraction_exists is False
    assert "degree 1" in profile.degree_obstruction
    assert "degree 0" in profile.degree_obstruction


def test_annulus_positive_retraction_present():
    profiles = {p.key: p for p in get_retraction_degree_profiles()}
    profile = profiles["annulus_to_core_circle_retraction"]
    assert profile.retraction_exists is True
    assert "degree 1" in profile.degree_obstruction


def test_retraction_degree_summary_has_both_flags():
    summary = retraction_degree_summary()
    assert "retraction_exists" in summary
    assert "no_retraction" in summary
    assert len(summary["no_retraction"]) >= 2
    assert len(summary["retraction_exists"]) >= 1


def test_degree_theory_registry_counts_match_getters():
    registry = degree_theory_profile_registry()
    assert registry["circle_degree_profiles"] == len(get_circle_degree_profiles())
    assert registry["retraction_degree_profiles"] == len(get_retraction_degree_profiles())
    assert sum(registry.values()) >= 7
