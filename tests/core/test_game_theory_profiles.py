"""Tests for pytop.game_theory_profiles — FPT-02."""

from pytop.game_theory_profiles import (
    KakutaniProfile,
    NashEquilibriumProfile,
    EconomicEquilibriumProfile,
    get_kakutani_profiles,
    get_nash_profiles,
    get_economic_equilibrium_profiles,
    kakutani_fixed_point_summary,
    nash_equilibrium_type_summary,
    game_theory_profile_registry,
)


# ---------------------------------------------------------------------------
# KakutaniProfile tests
# ---------------------------------------------------------------------------

def test_kakutani_profiles_returns_tuple():
    profiles = get_kakutani_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 4
    assert all(isinstance(p, KakutaniProfile) for p in profiles)


def test_kakutani_profiles_unique_keys():
    keys = [p.key for p in get_kakutani_profiles()]
    assert len(keys) == len(set(keys))


def test_kakutani_profiles_are_frozen():
    p = get_kakutani_profiles()[0]
    try:
        p.key = "mutated"  # type: ignore[misc]
        assert False
    except Exception:
        pass


def test_kakutani_all_conditions_met_has_fixed_point():
    profiles = {p.key: p for p in get_kakutani_profiles()}
    p = profiles["kakutani_conditions_all_met"]
    assert p.domain_is_compact is True
    assert p.domain_is_convex is True
    assert p.values_are_nonempty_convex is True
    assert p.graph_is_closed is True
    assert p.fixed_point_exists is True


def test_kakutani_nonconvex_values_no_fixed_point():
    profiles = {p.key: p for p in get_kakutani_profiles()}
    p = profiles["kakutani_nonconvex_values_fails"]
    assert p.values_are_nonempty_convex is False
    assert p.fixed_point_exists is False


def test_kakutani_open_graph_no_fixed_point():
    profiles = {p.key: p for p in get_kakutani_profiles()}
    p = profiles["kakutani_open_graph_fails"]
    assert p.graph_is_closed is False
    assert p.fixed_point_exists is False


def test_kakutani_simplex_references_nash():
    profiles = {p.key: p for p in get_kakutani_profiles()}
    p = profiles["kakutani_simplex"]
    assert p.fixed_point_exists is True
    assert "Nash" in p.notes


def test_kakutani_fixed_point_summary_has_both_keys():
    summary = kakutani_fixed_point_summary()
    assert "fixed_point_exists" in summary
    assert "no_fixed_point" in summary
    total = sum(len(v) for v in summary.values())
    assert total == len(get_kakutani_profiles())


# ---------------------------------------------------------------------------
# NashEquilibriumProfile tests
# ---------------------------------------------------------------------------

def test_nash_profiles_returns_tuple():
    profiles = get_nash_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 4
    assert all(isinstance(p, NashEquilibriumProfile) for p in profiles)


def test_nash_profiles_unique_keys():
    keys = [p.key for p in get_nash_profiles()]
    assert len(keys) == len(set(keys))


def test_nash_prisoners_dilemma_is_pure_equilibrium():
    profiles = {p.key: p for p in get_nash_profiles()}
    p = profiles["nash_prisoners_dilemma"]
    assert p.equilibrium_type == "pure"
    assert p.players == 2
    assert "D, D" in p.nash_equilibria or "(D,D)" in p.nash_equilibria


def test_nash_matching_pennies_no_pure_equilibrium():
    profiles = {p.key: p for p in get_nash_profiles()}
    p = profiles["nash_matching_pennies"]
    assert p.equilibrium_type == "none_pure"
    assert "1/2" in p.nash_equilibria


def test_nash_battle_of_sexes_has_both():
    profiles = {p.key: p for p in get_nash_profiles()}
    p = profiles["nash_battle_of_sexes"]
    assert p.equilibrium_type == "both"
    assert len(p.nash_equilibria) > 0


def test_nash_general_theorem_uses_kakutani():
    profiles = {p.key: p for p in get_nash_profiles()}
    p = profiles["nash_general_finite_game"]
    assert "Kakutani" in p.existence_proof
    assert p.players == -1  # general n


def test_nash_equilibrium_type_summary_covers_types():
    summary = nash_equilibrium_type_summary()
    assert "pure" in summary
    assert "none_pure" in summary
    assert "both" in summary
    assert "mixed" in summary
    total = sum(len(v) for v in summary.values())
    assert total == len(get_nash_profiles())


# ---------------------------------------------------------------------------
# EconomicEquilibriumProfile tests
# ---------------------------------------------------------------------------

def test_economic_equilibrium_profiles_returns_tuple():
    profiles = get_economic_equilibrium_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 2
    assert all(isinstance(p, EconomicEquilibriumProfile) for p in profiles)


def test_economic_equilibrium_profiles_unique_keys():
    keys = [p.key for p in get_economic_equilibrium_profiles()]
    assert len(keys) == len(set(keys))


def test_walrasian_uses_brouwer():
    profiles = {p.key: p for p in get_economic_equilibrium_profiles()}
    p = profiles["walrasian_equilibrium_brouwer"]
    assert p.fixed_point_theorem_used == "Brouwer"
    assert len(p.key_topological_ingredients) >= 4


def test_arrow_debreu_uses_kakutani():
    profiles = {p.key: p for p in get_economic_equilibrium_profiles()}
    p = profiles["arrow_debreu_equilibrium_kakutani"]
    assert p.fixed_point_theorem_used == "Kakutani"
    assert "Arrow" in p.display_name or "Debreu" in p.display_name


def test_arrow_debreu_topological_ingredients_include_simplex():
    profiles = {p.key: p for p in get_economic_equilibrium_profiles()}
    p = profiles["arrow_debreu_equilibrium_kakutani"]
    assert any("simplex" in ing.lower() or "compact" in ing.lower()
               for ing in p.key_topological_ingredients)


# ---------------------------------------------------------------------------
# Registry tests
# ---------------------------------------------------------------------------

def test_registry_has_all_categories():
    reg = game_theory_profile_registry()
    assert "kakutani_profiles" in reg
    assert "nash_profiles" in reg
    assert "economic_equilibrium_profiles" in reg


def test_registry_counts_match_getters():
    reg = game_theory_profile_registry()
    assert reg["kakutani_profiles"] == len(get_kakutani_profiles())
    assert reg["nash_profiles"] == len(get_nash_profiles())
    assert reg["economic_equilibrium_profiles"] == len(get_economic_equilibrium_profiles())


def test_registry_total_at_least_ten():
    reg = game_theory_profile_registry()
    assert sum(reg.values()) >= 10
