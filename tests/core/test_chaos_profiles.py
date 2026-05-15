"""Tests for pytop.chaos_profiles — DYN-02 chaos profile module."""

from pytop.chaos_profiles import (
    ChaosProperty,
    ChaosProfile,
    ChaoticMapProfile,
    SymbolicDynamicsProfile,
    get_devaney_chaos_properties,
    get_chaos_profiles,
    get_chaotic_map_profiles,
    get_symbolic_dynamics_profiles,
    chaos_status_summary,
    chaos_profile_registry,
)


# ---------------------------------------------------------------------------
# Devaney chaos properties
# ---------------------------------------------------------------------------

def test_devaney_properties_returns_exactly_three():
    props = get_devaney_chaos_properties()
    assert isinstance(props, tuple)
    assert len(props) == 3
    assert all(isinstance(p, ChaosProperty) for p in props)


def test_devaney_properties_cover_all_three_ingredients():
    names = {p.name for p in get_devaney_chaos_properties()}
    assert any("sensitive" in n.lower() for n in names)
    assert any("transitiv" in n.lower() for n in names)
    assert any("periodic" in n.lower() for n in names)


def test_devaney_properties_are_frozen():
    p = get_devaney_chaos_properties()[0]
    try:
        p.name = "mutated"  # type: ignore[misc]
        assert False, "Should have raised FrozenInstanceError"
    except Exception:
        pass


# ---------------------------------------------------------------------------
# ChaosProfile tests
# ---------------------------------------------------------------------------

def test_chaos_profiles_returns_tuple_of_chaos_profiles():
    profiles = get_chaos_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 5
    assert all(isinstance(p, ChaosProfile) for p in profiles)


def test_chaos_profiles_have_unique_keys():
    keys = [p.key for p in get_chaos_profiles()]
    assert len(keys) == len(set(keys))


def test_chaos_profiles_are_frozen():
    p = get_chaos_profiles()[0]
    try:
        p.key = "mutated"  # type: ignore[misc]
        assert False
    except Exception:
        pass


def test_tent_map_is_chaotic():
    profiles = {p.key: p for p in get_chaos_profiles()}
    tent = profiles["tent_map_chaotic"]
    assert tent.is_chaotic is True
    assert tent.has_sensitive_dependence is True
    assert tent.has_topological_transitivity is True
    assert tent.has_dense_periodic_orbits is True
    assert "log 2" in tent.topological_entropy


def test_logistic_map_r4_is_chaotic():
    profiles = {p.key: p for p in get_chaos_profiles()}
    log4 = profiles["logistic_map_r4_chaotic"]
    assert log4.is_chaotic is True
    assert "log 2" in log4.topological_entropy


def test_logistic_map_small_r_is_not_chaotic():
    profiles = {p.key: p for p in get_chaos_profiles()}
    small = profiles["logistic_map_r_small_non_chaotic"]
    assert small.is_chaotic is False
    assert small.has_sensitive_dependence is False
    assert small.topological_entropy == "0"


def test_irrational_rotation_transitive_but_not_chaotic():
    profiles = {p.key: p for p in get_chaos_profiles()}
    rot = profiles["irrational_rotation_non_chaotic"]
    assert rot.is_chaotic is False
    assert rot.has_topological_transitivity is True
    assert rot.has_dense_periodic_orbits is False
    assert rot.has_sensitive_dependence is False


def test_chaos_status_summary_has_both_keys():
    summary = chaos_status_summary()
    assert "chaotic" in summary
    assert "non_chaotic" in summary
    total = sum(len(v) for v in summary.values())
    assert total == len(get_chaos_profiles())


# ---------------------------------------------------------------------------
# ChaoticMapProfile tests
# ---------------------------------------------------------------------------

def test_chaotic_map_profiles_returns_tuple():
    profiles = get_chaotic_map_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 4
    assert all(isinstance(p, ChaoticMapProfile) for p in profiles)


def test_chaotic_map_profiles_have_unique_keys():
    keys = [p.key for p in get_chaotic_map_profiles()]
    assert len(keys) == len(set(keys))


def test_tent_map_profile_entropy_log2():
    profiles = {p.key: p for p in get_chaotic_map_profiles()}
    assert "log 2" in profiles["tent_map"].topological_entropy_formula


def test_logistic_map_profile_has_feigenbaum_reference():
    profiles = {p.key: p for p in get_chaotic_map_profiles()}
    log = profiles["logistic_map"]
    assert "Feigenbaum" in log.notes or "feigenbaum" in log.notes.lower()


def test_shift_map_profile_present():
    keys = {p.key for p in get_chaotic_map_profiles()}
    assert "shift_map" in keys


def test_doubling_map_profile_present():
    keys = {p.key for p in get_chaotic_map_profiles()}
    assert "doubling_map" in keys


# ---------------------------------------------------------------------------
# SymbolicDynamicsProfile tests
# ---------------------------------------------------------------------------

def test_symbolic_dynamics_profiles_returns_tuple():
    profiles = get_symbolic_dynamics_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 3
    assert all(isinstance(p, SymbolicDynamicsProfile) for p in profiles)


def test_symbolic_dynamics_profiles_have_unique_keys():
    keys = [p.key for p in get_symbolic_dynamics_profiles()]
    assert len(keys) == len(set(keys))


def test_binary_coding_tent_map_present():
    keys = {p.key for p in get_symbolic_dynamics_profiles()}
    assert "binary_coding_tent_map" in keys


def test_binary_coding_tent_map_is_semiconjugacy():
    profiles = {p.key: p for p in get_symbolic_dynamics_profiles()}
    p = profiles["binary_coding_tent_map"]
    assert any("semi-conjugacy" in prop or "σ ∘ h" in prop for prop in p.coding_map_properties)


def test_subshift_of_finite_type_present():
    keys = {p.key for p in get_symbolic_dynamics_profiles()}
    assert "subshift_of_finite_type" in keys


def test_sft_entropy_formula_references_spectral_radius():
    profiles = {p.key: p for p in get_symbolic_dynamics_profiles()}
    sft = profiles["subshift_of_finite_type"]
    assert any("spectral radius" in prop for prop in sft.coding_map_properties)


# ---------------------------------------------------------------------------
# Registry tests
# ---------------------------------------------------------------------------

def test_registry_returns_all_categories():
    reg = chaos_profile_registry()
    assert "devaney_chaos_properties" in reg
    assert "chaos_profiles" in reg
    assert "chaotic_map_profiles" in reg
    assert "symbolic_dynamics_profiles" in reg


def test_registry_counts_match_getters():
    reg = chaos_profile_registry()
    assert reg["devaney_chaos_properties"] == len(get_devaney_chaos_properties())
    assert reg["chaos_profiles"] == len(get_chaos_profiles())
    assert reg["chaotic_map_profiles"] == len(get_chaotic_map_profiles())
    assert reg["symbolic_dynamics_profiles"] == len(get_symbolic_dynamics_profiles())


def test_registry_total_at_least_fifteen():
    reg = chaos_profile_registry()
    assert sum(reg.values()) >= 15
