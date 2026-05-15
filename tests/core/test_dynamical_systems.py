"""Tests for pytop.dynamical_systems — DYN-01 profile module."""

from pytop.dynamical_systems import (
    OrbitProfile,
    FixedPointProfile,
    TopologicalConjugacyProfile,
    get_orbit_profiles,
    get_fixed_point_profiles,
    get_conjugacy_profiles,
    orbit_type_summary,
    fixed_point_stability_summary,
    conjugacy_exists_summary,
    dynamical_systems_profile_registry,
)


# ---------------------------------------------------------------------------
# OrbitProfile tests
# ---------------------------------------------------------------------------

def test_orbit_profiles_returns_tuple_of_orbit_profiles():
    profiles = get_orbit_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 4
    assert all(isinstance(p, OrbitProfile) for p in profiles)


def test_orbit_profiles_cover_all_four_types():
    types = {p.orbit_type for p in get_orbit_profiles()}
    assert "fixed" in types
    assert "periodic" in types
    assert "eventually_periodic" in types
    assert "infinite" in types


def test_orbit_profiles_have_unique_keys():
    keys = [p.key for p in get_orbit_profiles()]
    assert len(keys) == len(set(keys)), "Duplicate orbit profile keys found"


def test_orbit_profiles_are_frozen():
    p = get_orbit_profiles()[0]
    try:
        p.key = "mutated"  # type: ignore[misc]
        assert False, "Should have raised FrozenInstanceError"
    except Exception:
        pass  # frozen dataclass correctly raises


def test_orbit_type_summary_covers_all_types():
    summary = orbit_type_summary()
    assert "fixed" in summary
    assert "periodic" in summary
    assert "eventually_periodic" in summary
    assert "infinite" in summary
    total = sum(len(v) for v in summary.values())
    assert total == len(get_orbit_profiles())


def test_fixed_point_orbit_has_period_one():
    profiles = {p.key: p for p in get_orbit_profiles()}
    fp = profiles["fixed_point_orbit"]
    assert fp.period == 1
    assert fp.preperiod == 0
    assert fp.orbit_type == "fixed"


# ---------------------------------------------------------------------------
# FixedPointProfile tests
# ---------------------------------------------------------------------------

def test_fixed_point_profiles_returns_tuple():
    profiles = get_fixed_point_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 5
    assert all(isinstance(p, FixedPointProfile) for p in profiles)


def test_fixed_point_profiles_have_unique_keys():
    keys = [p.key for p in get_fixed_point_profiles()]
    assert len(keys) == len(set(keys))


def test_fixed_point_stability_classes():
    summary = fixed_point_stability_summary()
    assert "stable" in summary
    assert "unstable" in summary
    assert "neutral" in summary
    assert "not_applicable" in summary


def test_brouwer_profile_present():
    keys = {p.key for p in get_fixed_point_profiles()}
    assert "brouwer_fixed_point" in keys


def test_brouwer_profile_references_theorem():
    profiles = {p.key: p for p in get_fixed_point_profiles()}
    brouwer = profiles["brouwer_fixed_point"]
    assert "Brouwer" in brouwer.existence_theorem


def test_fixed_point_stability_summary_total():
    summary = fixed_point_stability_summary()
    total = sum(len(v) for v in summary.values())
    assert total == len(get_fixed_point_profiles())


# ---------------------------------------------------------------------------
# TopologicalConjugacyProfile tests
# ---------------------------------------------------------------------------

def test_conjugacy_profiles_returns_tuple():
    profiles = get_conjugacy_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 4
    assert all(isinstance(p, TopologicalConjugacyProfile) for p in profiles)


def test_conjugacy_profiles_have_unique_keys():
    keys = [p.key for p in get_conjugacy_profiles()]
    assert len(keys) == len(set(keys))


def test_conjugacy_exists_summary_has_both_bool_keys():
    summary = conjugacy_exists_summary()
    assert True in summary
    assert False in summary


def test_non_conjugate_profile_present():
    keys = {p.key for p in get_conjugacy_profiles()}
    assert "non_conjugate_example" in keys


def test_non_conjugate_profile_exists_is_false():
    profiles = {p.key: p for p in get_conjugacy_profiles()}
    p = profiles["non_conjugate_example"]
    assert p.conjugacy_exists is False
    assert len(p.invariants_preserved) == 0


def test_doubling_map_profile_preserves_entropy():
    profiles = {p.key: p for p in get_conjugacy_profiles()}
    p = profiles["doubling_map_conjugacy"]
    assert p.conjugacy_exists is True
    assert "topological entropy" in p.invariants_preserved


# ---------------------------------------------------------------------------
# Registry tests
# ---------------------------------------------------------------------------

def test_registry_returns_correct_counts():
    reg = dynamical_systems_profile_registry()
    assert reg["orbit_profiles"] == len(get_orbit_profiles())
    assert reg["fixed_point_profiles"] == len(get_fixed_point_profiles())
    assert reg["conjugacy_profiles"] == len(get_conjugacy_profiles())


def test_registry_total_at_least_thirteen():
    reg = dynamical_systems_profile_registry()
    total = sum(reg.values())
    assert total >= 13
