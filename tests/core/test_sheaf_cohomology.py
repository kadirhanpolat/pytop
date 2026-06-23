"""Tests for sheaf_cohomology.py — Čech sheaf cohomology on finite spaces."""

from __future__ import annotations

from pytop.sheaf_cohomology import (
    cech_cohomology,
    constant_sheaf,
    sheaf_cohomology,
    skyscraper_sheaf,
)

# ---------------------------------------------------------------------------
# Helpers: small finite topological spaces
# ---------------------------------------------------------------------------

# Sierpiński space: X={0,1}, opens = {∅, {1}, {0,1}}
# Contractible (one connected component, homotopy type of a point)
_SIERPINSKI_OPENS = [frozenset(), frozenset({1}), frozenset({0, 1})]
_SIERPINSKI_UNIV = frozenset({0, 1})

# 2-point discrete space: opens = {∅, {0}, {1}, {0,1}}
# Two connected components
_DISC2_OPENS = [frozenset(), frozenset({0}), frozenset({1}), frozenset({0, 1})]
_DISC2_UNIV = frozenset({0, 1})

# 3-point chain: 0 < 1 < 2 in specialisation order (opens = upsets of opposite)
# Opens = {∅, {0}, {0,1}, {0,1,2}}  (the Alexandroff topology for 0>1>2)
_CHAIN3_OPENS = [
    frozenset(),
    frozenset({0}),
    frozenset({0, 1}),
    frozenset({0, 1, 2}),
]
_CHAIN3_UNIV = frozenset({0, 1, 2})

# Indiscrete 2-point: opens = {∅, {0,1}}  (one connected component, trivially)
_INDISC2_OPENS = [frozenset(), frozenset({0, 1})]
_INDISC2_UNIV = frozenset({0, 1})

# 3-point minimal circle model (4-point diamond poset minus one level):
# Use a concrete T₀ model: X={a,b,c,d} with specialisation a<b, a<c, b<d, c<d
# Opens (upsets of opposite specialisation) for 4-point circle:
# Points {0,1,2,3}; topology = {∅,{3},{2,3},{1,3},{1,2,3},{0,1,2,3}}
# This is NOT the standard circle model. Use instead:
# 4-point space with H^0=ℤ, H^1=ℤ (homotopy S¹)
# The "finite circle" from pytop uses 4 pts; we build a simple one here:
# X={a,b,c,d} where opens = {∅, {a}, {b}, {a,b}, {c}, {a,c}, ...}
# For simplicity, just test Sierpiński and discrete.


# ---------------------------------------------------------------------------
# FiniteSheaf
# ---------------------------------------------------------------------------


class TestFiniteSheaf:
    def test_constant_sheaf_nonempty_rank_one(self) -> None:
        F = constant_sheaf(_SIERPINSKI_OPENS)
        assert F.section_rank(frozenset({1})) == 1
        assert F.section_rank(frozenset({0, 1})) == 1

    def test_constant_sheaf_empty_rank_zero(self) -> None:
        F = constant_sheaf(_SIERPINSKI_OPENS)
        assert F.section_rank(frozenset()) == 0

    def test_constant_sheaf_restriction_is_identity(self) -> None:
        F = constant_sheaf(_SIERPINSKI_OPENS)
        res = F.restrict(frozenset({0, 1}), frozenset({1}))
        assert res == [[1]]

    def test_constant_sheaf_self_restriction_is_identity(self) -> None:
        F = constant_sheaf(_SIERPINSKI_OPENS)
        res = F.restrict(frozenset({1}), frozenset({1}))
        assert res == [[1]]

    def test_skyscraper_sheaf_stalk_rank(self) -> None:
        F = skyscraper_sheaf(_SIERPINSKI_OPENS, frozenset({1}), rank=1)
        assert F.section_rank(frozenset({1})) == 1
        assert F.section_rank(frozenset({0, 1})) == 1

    def test_skyscraper_sheaf_zero_outside_stalk(self) -> None:
        # Using discrete 2-pt space; stalk at {0}
        F = skyscraper_sheaf(_DISC2_OPENS, frozenset({0}), rank=1)
        assert F.section_rank(frozenset({1})) == 0
        assert F.section_rank(frozenset({0})) == 1
        assert F.section_rank(frozenset({0, 1})) == 1

    def test_skyscraper_higher_rank(self) -> None:
        F = skyscraper_sheaf(_DISC2_OPENS, frozenset({0}), rank=3)
        assert F.section_rank(frozenset({0})) == 3

    def test_constant_sheaf_name(self) -> None:
        F = constant_sheaf(_SIERPINSKI_OPENS, name="ℤ")
        assert F.name == "ℤ"

    def test_constant_sheaf_open_sets_stored(self) -> None:
        F = constant_sheaf(_SIERPINSKI_OPENS)
        assert frozenset() in F.open_sets
        assert frozenset({1}) in F.open_sets
        assert frozenset({0, 1}) in F.open_sets


# ---------------------------------------------------------------------------
# cech_cohomology — explicit cover tests
# ---------------------------------------------------------------------------


class TestCechCohomologyExplicit:
    """Tests that pass an explicit cover to cech_cohomology."""

    def test_sierpinski_contractible_h0(self) -> None:
        F = constant_sheaf(_SIERPINSKI_OPENS)
        cover = [frozenset({1}), frozenset({0, 1})]
        H = cech_cohomology(cover, F, max_degree=2)
        assert H[0].free_rank == 1

    def test_sierpinski_h1_zero(self) -> None:
        F = constant_sheaf(_SIERPINSKI_OPENS)
        cover = [frozenset({1}), frozenset({0, 1})]
        H = cech_cohomology(cover, F, max_degree=2)
        assert H[1].free_rank == 0

    def test_sierpinski_h0_no_torsion(self) -> None:
        F = constant_sheaf(_SIERPINSKI_OPENS)
        cover = [frozenset({1}), frozenset({0, 1})]
        H = cech_cohomology(cover, F)
        assert H[0].torsion == ()

    def test_discrete2_minimal_cover_h0_rank2(self) -> None:
        # Minimal cover of the discrete space: each point's minimal nbhd
        F = constant_sheaf(_DISC2_OPENS)
        cover = [frozenset({0}), frozenset({1})]  # disjoint opens
        H = cech_cohomology(cover, F, max_degree=1)
        assert H[0].free_rank == 2

    def test_discrete2_minimal_cover_h1_zero(self) -> None:
        F = constant_sheaf(_DISC2_OPENS)
        cover = [frozenset({0}), frozenset({1})]
        H = cech_cohomology(cover, F, max_degree=1)
        assert H[1].free_rank == 0

    def test_single_open_h0_equals_rank(self) -> None:
        # Indiscrete space: cover = [universe], C^0 = ℤ, no higher
        F = constant_sheaf(_INDISC2_OPENS)
        cover = [frozenset({0, 1})]
        H = cech_cohomology(cover, F, max_degree=1)
        assert H[0].free_rank == 1
        assert H[1].free_rank == 0

    def test_empty_cover_returns_empty(self) -> None:
        F = constant_sheaf(_SIERPINSKI_OPENS)
        H = cech_cohomology([], F)
        assert H == {}

    def test_cover_with_empty_set_dropped(self) -> None:
        F = constant_sheaf(_SIERPINSKI_OPENS)
        cover = [frozenset(), frozenset({1}), frozenset({0, 1})]
        H = cech_cohomology(cover, F, max_degree=2)
        # Same result as without empty set
        H2 = cech_cohomology([frozenset({1}), frozenset({0, 1})], F, max_degree=2)
        assert H[0].free_rank == H2[0].free_rank

    def test_skyscraper_h0_rank_one(self) -> None:
        F = skyscraper_sheaf(_SIERPINSKI_OPENS, frozenset({1}), rank=1)
        cover = [frozenset({1}), frozenset({0, 1})]
        H = cech_cohomology(cover, F, max_degree=1)
        assert H[0].free_rank == 1

    def test_skyscraper_h1_zero(self) -> None:
        F = skyscraper_sheaf(_SIERPINSKI_OPENS, frozenset({1}), rank=1)
        cover = [frozenset({1}), frozenset({0, 1})]
        H = cech_cohomology(cover, F, max_degree=1)
        assert H[1].free_rank == 0

    def test_rank2_skyscraper_h0(self) -> None:
        F = skyscraper_sheaf(_DISC2_OPENS, frozenset({0}), rank=2)
        cover = [frozenset({0})]
        H = cech_cohomology(cover, F, max_degree=0)
        assert H[0].free_rank == 2

    def test_three_point_chain_contractible(self) -> None:
        F = constant_sheaf(_CHAIN3_OPENS)
        # Minimal nbhds: U_0={0}, U_1={0,1}, U_2={0,1,2}
        cover = [frozenset({0}), frozenset({0, 1}), frozenset({0, 1, 2})]
        H = cech_cohomology(cover, F, max_degree=2)
        assert H[0].free_rank == 1

    def test_three_point_chain_h1_zero(self) -> None:
        F = constant_sheaf(_CHAIN3_OPENS)
        cover = [frozenset({0}), frozenset({0, 1}), frozenset({0, 1, 2})]
        H = cech_cohomology(cover, F, max_degree=2)
        assert H[1].free_rank == 0

    def test_abelian_group_str(self) -> None:
        F = constant_sheaf(_SIERPINSKI_OPENS)
        cover = [frozenset({1}), frozenset({0, 1})]
        H = cech_cohomology(cover, F)
        assert str(H[0]) == "Z"


# ---------------------------------------------------------------------------
# sheaf_cohomology — uses minimal open cover automatically
# ---------------------------------------------------------------------------


class TestSheafCohomology:
    def test_sierpinski_h0(self) -> None:
        F = constant_sheaf(_SIERPINSKI_OPENS)
        r = sheaf_cohomology(_SIERPINSKI_OPENS, _SIERPINSKI_UNIV, F)
        assert r["betti_numbers"][0] == 1

    def test_sierpinski_euler_characteristic(self) -> None:
        F = constant_sheaf(_SIERPINSKI_OPENS)
        r = sheaf_cohomology(_SIERPINSKI_OPENS, _SIERPINSKI_UNIV, F)
        assert r["euler_characteristic"] == 1

    def test_discrete2_h0_two_components(self) -> None:
        F = constant_sheaf(_DISC2_OPENS)
        r = sheaf_cohomology(_DISC2_OPENS, _DISC2_UNIV, F)
        assert r["betti_numbers"][0] == 2

    def test_discrete2_euler_characteristic(self) -> None:
        F = constant_sheaf(_DISC2_OPENS)
        r = sheaf_cohomology(_DISC2_OPENS, _DISC2_UNIV, F)
        assert r["euler_characteristic"] == 2

    def test_chain3_contractible_h0(self) -> None:
        F = constant_sheaf(_CHAIN3_OPENS)
        r = sheaf_cohomology(_CHAIN3_OPENS, _CHAIN3_UNIV, F)
        assert r["betti_numbers"][0] == 1

    def test_sheaf_name_in_result(self) -> None:
        F = constant_sheaf(_SIERPINSKI_OPENS, name="ℤ")
        r = sheaf_cohomology(_SIERPINSKI_OPENS, _SIERPINSKI_UNIV, F)
        assert r["sheaf"] == "ℤ"

    def test_cover_size_positive(self) -> None:
        F = constant_sheaf(_SIERPINSKI_OPENS)
        r = sheaf_cohomology(_SIERPINSKI_OPENS, _SIERPINSKI_UNIV, F)
        assert r["cover_size"] >= 1

    def test_cohomology_dict_keys(self) -> None:
        F = constant_sheaf(_SIERPINSKI_OPENS)
        r = sheaf_cohomology(_SIERPINSKI_OPENS, _SIERPINSKI_UNIV, F)
        assert "cohomology" in r
        assert "betti_numbers" in r
        assert "euler_characteristic" in r
        assert "cover_size" in r

    def test_indiscrete_h0_one_component(self) -> None:
        F = constant_sheaf(_INDISC2_OPENS)
        r = sheaf_cohomology(_INDISC2_OPENS, _INDISC2_UNIV, F)
        assert r["betti_numbers"][0] == 1

    def test_skyscraper_h0_one(self) -> None:
        F = skyscraper_sheaf(_SIERPINSKI_OPENS, frozenset({1}))
        r = sheaf_cohomology(_SIERPINSKI_OPENS, _SIERPINSKI_UNIV, F)
        assert r["betti_numbers"][0] == 1

    def test_max_degree_respected(self) -> None:
        F = constant_sheaf(_CHAIN3_OPENS)
        r = sheaf_cohomology(_CHAIN3_OPENS, _CHAIN3_UNIV, F, max_degree=0)
        assert len(r["betti_numbers"]) == 1

    def test_betti_numbers_list_length(self) -> None:
        F = constant_sheaf(_DISC2_OPENS)
        r = sheaf_cohomology(_DISC2_OPENS, _DISC2_UNIV, F, max_degree=2)
        assert len(r["betti_numbers"]) == 3


# ---------------------------------------------------------------------------
# Consistency checks
# ---------------------------------------------------------------------------


class TestConsistency:
    def test_constant_sheaf_h0_counts_components(self) -> None:
        # Any finite T₀ space: H^0 = number of connected components
        # Sierpiński: 1 component
        F = constant_sheaf(_SIERPINSKI_OPENS)
        r = sheaf_cohomology(_SIERPINSKI_OPENS, _SIERPINSKI_UNIV, F)
        assert r["betti_numbers"][0] == 1

        # Discrete 2-point: 2 components
        F2 = constant_sheaf(_DISC2_OPENS)
        r2 = sheaf_cohomology(_DISC2_OPENS, _DISC2_UNIV, F2)
        assert r2["betti_numbers"][0] == 2

    def test_euler_char_alternating_sum_of_betti(self) -> None:
        F = constant_sheaf(_CHAIN3_OPENS)
        r = sheaf_cohomology(_CHAIN3_OPENS, _CHAIN3_UNIV, F, max_degree=2)
        expected_chi = sum((-1) ** p * r["betti_numbers"][p] for p in range(3))
        assert r["euler_characteristic"] == expected_chi

    def test_cech_and_sheaf_cohomology_agree_on_sierpinski(self) -> None:
        F = constant_sheaf(_SIERPINSKI_OPENS)
        cover = [frozenset({1}), frozenset({0, 1})]
        H_direct = cech_cohomology(cover, F, max_degree=1)
        r = sheaf_cohomology(_SIERPINSKI_OPENS, _SIERPINSKI_UNIV, F, max_degree=1)
        assert H_direct[0].free_rank == r["betti_numbers"][0]
        assert H_direct[1].free_rank == r["betti_numbers"][1]

    def test_h0_abelian_group_is_free(self) -> None:
        F = constant_sheaf(_DISC2_OPENS)
        cover = [frozenset({0}), frozenset({1})]
        H = cech_cohomology(cover, F, max_degree=1)
        assert H[0].torsion == ()

    def test_cover_singleton_gives_rank_of_stalk(self) -> None:
        F = constant_sheaf(_DISC2_OPENS)
        cover = [frozenset({0, 1})]
        H = cech_cohomology(cover, F, max_degree=0)
        assert H[0].free_rank == F.section_rank(frozenset({0, 1}))
