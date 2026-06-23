"""Incremental Phase 1/2 improvements:
  - Alexandroff factory functions (finite_circle, finite_sphere, finite_wedge_circles)
  - Stronger Tietze simplification (cyclic reduction + deduplication)
  - persistence_betti_numbers utility
"""

from __future__ import annotations

import math

import pytest

from pytop.experimental.spaces import (
    AlexandroffSpace,
    finite_circle,
    finite_sphere,
    finite_wedge_circles,
)
from pytop.experimental.spaces.pi1 import pi1_space
from pytop.persistent_homology import (
    PersistencePair,
    persistence_betti_numbers,
    persistence_pairs,
    vietoris_rips_filtration,
)
from pytop.van_kampen import (
    _cyclically_reduce,
    _dedup_relators,
    _tietze_simplify,
)

# ==========================================================================
# Factory: finite_circle
# ==========================================================================

class TestFiniteCircle:
    def test_returns_alexandroff_space(self):
        s = finite_circle()
        assert isinstance(s, AlexandroffSpace)

    def test_has_4_points(self):
        s = finite_circle()
        assert len(list(s.points())) == 4

    def test_pi1_is_Z(self):
        r = pi1_space(finite_circle())
        assert r.group_type == "infinite_cyclic"
        assert r.abelianization_betti == 1
        assert r.abelianization_torsion == ()

    def test_name(self):
        s = finite_circle()
        assert "1" in s.name  # "S^1"

    def test_not_hausdorff(self):
        from pytop.experimental.spaces import is_hausdorff
        v = is_hausdorff(finite_circle())
        # Finite T0 non-discrete → generally not Hausdorff
        assert v.value is False


# ==========================================================================
# Factory: finite_sphere
# ==========================================================================

class TestFiniteSphere:
    def test_s0_has_2_points(self):
        s = finite_sphere(0)
        assert len(list(s.points())) == 2

    def test_s1_is_circle(self):
        s = finite_sphere(1)
        r = pi1_space(s)
        assert r.group_type == "infinite_cyclic"

    def test_s2_has_6_points(self):
        # Suspension of S^1 (4 pts) adds 2 → 6 pts
        s = finite_sphere(2)
        assert len(list(s.points())) == 6

    def test_s2_pi1_is_trivial(self):
        s = finite_sphere(2)
        r = pi1_space(s)
        assert r.is_trivial()

    def test_s3_has_8_points(self):
        s = finite_sphere(3)
        assert len(list(s.points())) == 8

    def test_s3_pi1_is_trivial(self):
        s = finite_sphere(3)
        r = pi1_space(s)
        assert r.is_trivial()

    def test_point_count_formula(self):
        # S^n has 2(n+1) points for n >= 1; S^0 has 2
        assert len(list(finite_sphere(0).points())) == 2
        for n in range(1, 5):
            assert len(list(finite_sphere(n).points())) == 2 * (n + 1)

    def test_negative_n_raises(self):
        with pytest.raises(ValueError):
            finite_sphere(-1)

    def test_name_contains_n(self):
        assert "2" in finite_sphere(2).name
        assert "3" in finite_sphere(3).name


# ==========================================================================
# Factory: finite_wedge_circles
# ==========================================================================

class TestFiniteWedgeCircles:
    def test_k0_is_point(self):
        s = finite_wedge_circles(0)
        assert len(list(s.points())) == 1
        r = pi1_space(s)
        assert r.is_trivial()

    def test_k1_is_circle(self):
        s = finite_wedge_circles(1)
        assert len(list(s.points())) == 4
        r = pi1_space(s)
        assert r.group_type == "infinite_cyclic"

    def test_k2_has_7_points(self):
        s = finite_wedge_circles(2)
        assert len(list(s.points())) == 7

    def test_k2_pi1_is_free_rank_2(self):
        s = finite_wedge_circles(2)
        r = pi1_space(s)
        assert r.is_free()
        assert r.abelianization_betti == 2

    def test_k3_pi1_is_free_rank_3(self):
        s = finite_wedge_circles(3)
        r = pi1_space(s)
        assert r.is_free()
        assert r.abelianization_betti == 3

    def test_point_count_formula(self):
        # k circles → 1 + 3k points
        for k in range(0, 5):
            expected = 1 if k == 0 else 1 + 3 * k
            assert len(list(finite_wedge_circles(k).points())) == expected

    def test_negative_k_raises(self):
        with pytest.raises(ValueError):
            finite_wedge_circles(-1)

    def test_custom_name(self):
        s = finite_wedge_circles(2, name="my_wedge")
        assert s.name == "my_wedge"


# ==========================================================================
# Tietze: _cyclically_reduce
# ==========================================================================

class TestCyclicallyReduce:
    def test_already_reduced(self):
        w = (("a", 1), ("b", 1))
        assert _cyclically_reduce(w) == w

    def test_removes_outer_inverse_pair(self):
        # a · b · a^{-1}: first=a, last=a^{-1} — mutual inverses → reduce to b
        w = (("a", 1), ("b", 1), ("a", -1))
        result = _cyclically_reduce(w)
        assert result == (("b", 1),)

    def test_removes_multiple_layers(self):
        # a · b · b^{-1} · a^{-1}: reduce outer (a, a^{-1}) → b · b^{-1} → empty
        w = (("a", 1), ("b", 1), ("b", -1), ("a", -1))
        result = _cyclically_reduce(w)
        assert result == ()

    def test_empty_word_unchanged(self):
        assert _cyclically_reduce(()) == ()

    def test_single_letter_unchanged(self):
        w = (("a", 1),)
        assert _cyclically_reduce(w) == w

    def test_no_outer_cancellation_when_different_gens(self):
        w = (("a", 1), ("b", 1), ("c", -1))
        result = _cyclically_reduce(w)
        assert result == w


# ==========================================================================
# Tietze: _dedup_relators
# ==========================================================================

class TestDedupRelators:
    def test_removes_exact_duplicate(self):
        w = (("a", 1), ("b", 1))
        result = _dedup_relators([w, w])
        assert len(result) == 1

    def test_removes_inverse_duplicate(self):
        w = (("a", 1), ("b", 1))
        inv_w = (("b", -1), ("a", -1))
        result = _dedup_relators([w, inv_w])
        assert len(result) == 1

    def test_removes_cyclic_conjugate(self):
        # (a, b) and (b, a) are cyclic conjugates
        w1 = (("a", 1), ("b", 1))
        w2 = (("b", 1), ("a", 1))
        result = _dedup_relators([w1, w2])
        assert len(result) == 1

    def test_keeps_distinct_relators(self):
        w1 = (("a", 1), ("b", 1))
        w2 = (("a", 2),)
        result = _dedup_relators([w1, w2])
        assert len(result) == 2

    def test_empty_list(self):
        assert _dedup_relators([]) == []


# ==========================================================================
# Tietze: _tietze_simplify — improved behavior
# ==========================================================================

class TestTietzeSimplifyImproved:
    def test_eliminates_trivial_relator_via_cyclic_reduction(self):
        # Relator a·a^{-1} cyclically reduces to empty → trivial relator removed
        # After cleaning: no relators, so presentation is free
        gens = ["a", "b"]
        rels = [
            (("a", 1), ("a", -1)),  # trivially empty
            (("b", 2),),
        ]
        new_gens, new_rels = _tietze_simplify(gens, rels)
        # Trivial relator removed; b^2 stays
        assert (("a", 1), ("a", -1)) not in new_rels

    def test_dedup_applied_before_elimination(self):
        # a·b and b·a are cyclic conjugates → dedup leaves one
        # Then Tietze can potentially eliminate
        gens = ["a", "b"]
        rels = [
            (("a", 1), ("b", 1)),
            (("b", 1), ("a", 1)),  # cyclic conjugate of first
        ]
        new_gens, new_rels = _tietze_simplify(gens, rels)
        # Only one unique relator should remain
        assert len(new_rels) <= 1

    def test_generator_eliminated_via_relator(self):
        # ⟨a, b | b⟩ → b = 1 → ⟨a |⟩
        gens = ["a", "b"]
        rels = [(("b", 1),)]
        new_gens, new_rels = _tietze_simplify(gens, rels)
        assert "b" not in new_gens
        assert new_rels == []

    def test_cyclic_reduction_simplifies_relator(self):
        # Relator x·a·x^{-1}: if x can be eliminated, a = 1
        gens = ["x", "a"]
        rels = [(("x", 1), ("a", 1), ("x", -1))]
        new_gens, new_rels = _tietze_simplify(gens, rels)
        # After cyclic reduction: (a,) — then a eliminated
        assert "a" not in new_gens or new_rels == []


# ==========================================================================
# persistence_betti_numbers
# ==========================================================================

class TestPersistenceBettiNumbers:
    def _trivial_pairs(self):
        return (
            PersistencePair(0, 0.0, math.inf),  # one essential H_0
        )

    def _circle_pairs(self):
        return (
            PersistencePair(0, 0.0, math.inf),   # H_0
            PersistencePair(1, 0.5, math.inf),    # H_1 (loop)
            PersistencePair(1, 0.1, 0.3),         # finite H_1 pair
        )

    def test_empty_pairs(self):
        assert persistence_betti_numbers(()) == {}

    def test_single_essential(self):
        result = persistence_betti_numbers(self._trivial_pairs())
        assert result == {0: 1}

    def test_circle_betti_numbers(self):
        result = persistence_betti_numbers(self._circle_pairs())
        assert result[0] == 1
        assert result[1] == 1

    def test_finite_pairs_not_counted(self):
        # Only essential (death=inf) pairs contribute
        pairs = (PersistencePair(1, 0.1, 0.3),)  # finite → not essential
        result = persistence_betti_numbers(pairs)
        assert result == {}

    def test_multiple_dims(self):
        pairs = (
            PersistencePair(0, 0.0, math.inf),
            PersistencePair(0, 0.0, math.inf),
            PersistencePair(2, 0.0, math.inf),
        )
        result = persistence_betti_numbers(pairs)
        assert result[0] == 2
        assert result[2] == 1
        assert 1 not in result

    def test_vr_filtration_integration(self):
        # 4 unit-square vertices: adjacent edges = √2 ≈ 1.414, diagonals = 2.
        # With max_scale=1.5 only the 4 adjacent edges form (the 4-cycle).
        # max_dimension=1 means no triangles. The 4-cycle has β₀=1, β₁=1.

        class SquareCloud:
            carrier = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            def distance_between(self, a, b):
                return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

        filt = vietoris_rips_filtration(SquareCloud(), max_dimension=1, max_scale=1.5)
        pairs = persistence_pairs(filt)
        betti = persistence_betti_numbers(pairs)
        assert betti.get(0, 0) == 1   # connected
        assert betti.get(1, 0) == 1   # one loop (4-cycle, diagonals excluded)
