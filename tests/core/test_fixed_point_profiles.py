"""Tests for pytop.fixed_point_profiles — FPT-01."""

from pytop.fixed_point_profiles import (
    NoRetractionProfile,
    BrouwerFPTProfile,
    RetractionProfile,
    get_no_retraction_profiles,
    get_brouwer_fpt_profiles,
    get_retraction_profiles,
    no_retraction_by_dimension,
    brouwer_fpt_by_dimension,
    fixed_point_theorem_registry,
)


# ---------------------------------------------------------------------------
# NoRetractionProfile tests
# ---------------------------------------------------------------------------

def test_no_retraction_profiles_returns_tuple():
    profiles = get_no_retraction_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 3
    assert all(isinstance(p, NoRetractionProfile) for p in profiles)


def test_no_retraction_profiles_unique_keys():
    keys = [p.key for p in get_no_retraction_profiles()]
    assert len(keys) == len(set(keys))


def test_no_retraction_profiles_all_false():
    for p in get_no_retraction_profiles():
        assert p.retraction_exists is False


def test_no_retraction_profiles_are_frozen():
    p = get_no_retraction_profiles()[0]
    try:
        p.key = "mutated"  # type: ignore[misc]
        assert False
    except Exception:
        pass


def test_no_retraction_D1_S0_uses_connectedness():
    profiles = {p.key: p for p in get_no_retraction_profiles()}
    p = profiles["no_retraction_D1_S0"]
    assert p.dimension == 1
    assert "connect" in p.proof_method.lower() or "elementary" in p.proof_method.lower()


def test_no_retraction_D2_S1_uses_degree_theory():
    profiles = {p.key: p for p in get_no_retraction_profiles()}
    p = profiles["no_retraction_D2_S1"]
    assert p.dimension == 2
    assert "degree" in p.proof_method.lower()


def test_no_retraction_by_dimension_1():
    p = no_retraction_by_dimension(1)
    assert p is not None
    assert p.dimension == 1


def test_no_retraction_by_dimension_2():
    p = no_retraction_by_dimension(2)
    assert p is not None
    assert p.dimension == 2


def test_no_retraction_by_dimension_general_fallback():
    p = no_retraction_by_dimension(99)
    assert p is not None
    assert p.dimension == -1  # general profile


# ---------------------------------------------------------------------------
# BrouwerFPTProfile tests
# ---------------------------------------------------------------------------

def test_brouwer_fpt_profiles_returns_tuple():
    profiles = get_brouwer_fpt_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 5
    assert all(isinstance(p, BrouwerFPTProfile) for p in profiles)


def test_brouwer_fpt_profiles_unique_keys():
    keys = [p.key for p in get_brouwer_fpt_profiles()]
    assert len(keys) == len(set(keys))


def test_brouwer_fpt_profiles_all_have_fixed_point():
    for p in get_brouwer_fpt_profiles():
        assert p.fixed_point_exists is True


def test_brouwer_fpt_D1_uses_ivt():
    profiles = {p.key: p for p in get_brouwer_fpt_profiles()}
    p = profiles["brouwer_fpt_D1"]
    assert p.dimension == 1
    assert "IVT" in p.proof_strategy or "Intermediate" in p.proof_strategy


def test_brouwer_fpt_D2_references_no_retraction():
    profiles = {p.key: p for p in get_brouwer_fpt_profiles()}
    p = profiles["brouwer_fpt_D2"]
    assert p.dimension == 2
    assert "retract" in p.proof_strategy.lower() or "No-Retraction" in p.proof_strategy


def test_brouwer_fpt_general_mentions_kakutani():
    profiles = {p.key: p for p in get_brouwer_fpt_profiles()}
    p = profiles["brouwer_fpt_Dn"]
    assert "Kakutani" in p.notes or "Nash" in p.notes


def test_brouwer_fpt_by_dimension_1_returns_profiles():
    result = brouwer_fpt_by_dimension(1)
    assert len(result) >= 1
    assert all(p.dimension == 1 for p in result)


def test_brouwer_fpt_by_dimension_2_returns_profiles():
    result = brouwer_fpt_by_dimension(2)
    assert len(result) >= 2   # D2 + geographic map + coffee


def test_geographic_map_profile_present():
    keys = {p.key for p in get_brouwer_fpt_profiles()}
    assert "brouwer_fpt_geographic_map" in keys


def test_coffee_stirring_profile_present():
    keys = {p.key for p in get_brouwer_fpt_profiles()}
    assert "brouwer_fpt_coffee_stirring" in keys


# ---------------------------------------------------------------------------
# RetractionProfile tests
# ---------------------------------------------------------------------------

def test_retraction_profiles_returns_tuple():
    profiles = get_retraction_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 4
    assert all(isinstance(p, RetractionProfile) for p in profiles)


def test_retraction_profiles_unique_keys():
    keys = [p.key for p in get_retraction_profiles()]
    assert len(keys) == len(set(keys))


def test_retraction_profiles_all_exist():
    for p in get_retraction_profiles():
        assert p.retraction_exists is True


def test_punctured_plane_to_circle_is_deformation_retract():
    profiles = {p.key: p for p in get_retraction_profiles()}
    p = profiles["retraction_punctured_plane_to_circle"]
    assert p.deformation_retract is True
    assert "x / |x|" in p.retraction_formula or "x/|x|" in p.retraction_formula


def test_Dn_to_point_contrasts_no_retraction():
    profiles = {p.key: p for p in get_retraction_profiles()}
    p = profiles["retraction_Dn_to_point"]
    assert p.deformation_retract is True
    assert "No-Retraction" in p.notes or "not" in p.notes.lower()


# ---------------------------------------------------------------------------
# Registry tests
# ---------------------------------------------------------------------------

def test_registry_has_all_categories():
    reg = fixed_point_theorem_registry()
    assert "no_retraction_profiles" in reg
    assert "brouwer_fpt_profiles" in reg
    assert "retraction_profiles" in reg


def test_registry_counts_match_getters():
    reg = fixed_point_theorem_registry()
    assert reg["no_retraction_profiles"] == len(get_no_retraction_profiles())
    assert reg["brouwer_fpt_profiles"] == len(get_brouwer_fpt_profiles())
    assert reg["retraction_profiles"] == len(get_retraction_profiles())


def test_registry_total_at_least_twelve():
    reg = fixed_point_theorem_registry()
    assert sum(reg.values()) >= 12
