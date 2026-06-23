"""Tests for π₁ computation via the order complex (McCord theorem).

Each test documents the mathematical fact being verified.
"""

from __future__ import annotations

import pytest

from pytop.experimental.spaces import (
    AlexandroffSpace,
    FiniteSpace,
    SubbaseSpace,
    discrete_finite_space,
)
from pytop.experimental.spaces.constructed import ProductSpace, SumSpace
from pytop.experimental.spaces.pi1 import pi1_space

# ==========================================================================
# Contractible / trivial π₁
# ==========================================================================

class TestTrivialPi1:
    def test_single_point(self):
        p = FiniteSpace("pt", {0}, [set(), {0}])
        r = pi1_space(p)
        assert r.is_trivial()

    def test_discrete_one_point(self):
        d = discrete_finite_space({0})
        r = pi1_space(d)
        assert r.is_trivial()

    def test_indiscrete_two_points(self):
        # Indiscrete: specialization order 0 <_spec 1 AND 1 <_spec 0 (both in each other's closure).
        # T0 quotient collapses to 1 point → trivial π₁.
        ind = FiniteSpace("indiscrete", {0, 1}, [set(), {0, 1}])
        r = pi1_space(ind)
        assert r.is_trivial()

    def test_chain_2_is_contractible(self):
        # AlexandroffSpace 0 < 1: order complex = single edge → contractible.
        c = AlexandroffSpace("chain2", {0, 1}, [(0, 1)])
        r = pi1_space(c)
        assert r.is_trivial()

    def test_chain_3_is_contractible(self):
        # 0 < 1 < 2: order complex has vertices {0,1,2}, edges {(0,1),(1,2),(0,2)},
        # face {(0,1),(1,2),(0,2)^{-1}} filling the triangle → contractible.
        c = AlexandroffSpace("chain3", {0, 1, 2}, [(0, 1), (1, 2)])
        r = pi1_space(c)
        assert r.is_trivial()

    def test_discrete_two_points_trivial(self):
        # Discrete 2 points: specialization order is empty → no edges → two
        # isolated vertices. Each connected component is contractible → trivial π₁.
        d = discrete_finite_space({0, 1})
        r = pi1_space(d)
        assert r.is_trivial()

    def test_sierpinski_is_contractible(self):
        # Sierpinski: 0 <_spec 1 (since 1 ∈ cl({0}) = {0,1}).
        # Order complex = single edge → contractible.
        s = FiniteSpace("Sierpinski", {0, 1}, [set(), {0}, {0, 1}])
        r = pi1_space(s)
        assert r.is_trivial()


# ==========================================================================
# Infinite cyclic π₁ = ℤ (minimal finite T0 model of S¹)
# ==========================================================================

class TestCirclePi1:
    def _diamond(self):
        """Diamond poset: 0 < 2, 0 < 3, 1 < 2, 1 < 3. Minimal T0 model of S¹."""
        return AlexandroffSpace("S1_4pt", {0, 1, 2, 3},
                                [(0, 2), (0, 3), (1, 2), (1, 3)])

    def test_diamond_pi1_is_infinite_cyclic(self):
        # McCord: |K(diamond)| ≃ S¹, so π₁ = ℤ.
        # Order complex: vertices {0,1,2,3}, edges {(0,2),(0,3),(1,2),(1,3)},
        # no 3-chains (0,1 incomparable; 2,3 incomparable).
        # This is K_{2,2} = 4-cycle → π₁ = ℤ.
        r = pi1_space(self._diamond())
        assert r.group_type == "infinite_cyclic"
        assert r.abelianization_betti == 1
        assert r.abelianization_torsion == ()

    def test_diamond_method(self):
        r = pi1_space(self._diamond())
        assert r.method == "order_complex"

    def test_diamond_presentation_has_one_generator(self):
        r = pi1_space(self._diamond())
        assert len(r.presentation.generators) == 1
        assert len(r.presentation.relators) == 0

    def test_diamond_is_free(self):
        r = pi1_space(self._diamond())
        assert r.is_free()


# ==========================================================================
# Free groups — wedge of circles (multiple "loops")
# ==========================================================================

class TestFreeGroupPi1:
    def _two_loops(self):
        """6-point minimal T0 model of S¹ ∨ S¹ (two diamonds sharing a vertex).

        Diamond 1: a < c, a < d, b < c, b < d
        Diamond 2: a < e, a < f, g < e, g < f
        (shared vertex a)
        """
        return AlexandroffSpace(
            "S1vS1", {0, 1, 2, 3, 4, 5, 6},
            [
                (0, 2), (0, 3), (1, 2), (1, 3),  # first loop: 0,1 → 2,3
                (0, 4), (0, 5), (6, 4), (6, 5),  # second loop: 0,6 → 4,5
            ],
        )

    def test_two_loop_space_has_free_pi1(self):
        # The order complex contains two 4-cycles sharing vertex 0.
        # π₁ should be F₂ (free group on 2 generators).
        r = pi1_space(self._two_loops())
        assert r.is_free()
        assert r.abelianization_betti == 2


# ==========================================================================
# Non-T0 spaces — T0 quotient
# ==========================================================================

class TestNonT0Pi1:
    def test_non_t0_collapses_correctly(self):
        # Space {0,1,2} with opens {∅, {0,1,2}}: indiscrete → non-T0.
        # T0 quotient = 1 point → π₁ = trivial.
        ind = FiniteSpace("ind3", {0, 1, 2}, [set(), {0, 1, 2}])
        r = pi1_space(ind)
        assert r.is_trivial()

    def test_notes_mention_quotient(self):
        ind = FiniteSpace("ind3", {0, 1, 2}, [set(), {0, 1, 2}])
        r = pi1_space(ind)
        # At least one note mentions the T0 quotient collapsing
        note_text = " ".join(r.notes)
        assert "T0" in note_text or "collaps" in note_text.lower()


# ==========================================================================
# ProductSpace π₁
# ==========================================================================

class TestProductPi1:
    def test_product_of_contractibles_is_trivial(self):
        # chain2 × chain2: both contractible → π₁ = trivial.
        chain = AlexandroffSpace("chain2", {0, 1}, [(0, 1)])
        prod = ProductSpace([chain, chain])
        r = pi1_space(prod)
        assert r.is_trivial()

    def test_product_method(self):
        chain = AlexandroffSpace("chain2", {0, 1}, [(0, 1)])
        prod = ProductSpace([chain, chain])
        r = pi1_space(prod)
        assert r.method == "product_theorem"

    def test_product_of_circle_and_contractible(self):
        # S¹ × chain2 ≃ S¹ → π₁ = ℤ
        diamond = AlexandroffSpace("S1_4pt", {0, 1, 2, 3},
                                   [(0, 2), (0, 3), (1, 2), (1, 3)])
        chain = AlexandroffSpace("chain2", {4, 5}, [(4, 5)])
        prod = ProductSpace([diamond, chain])
        r = pi1_space(prod)
        # π₁(S¹ × contractible) = π₁(S¹) × π₁(pt) = ℤ × 1 = ℤ
        assert r.group_type == "infinite_cyclic"
        assert r.abelianization_betti == 1


# ==========================================================================
# SumSpace π₁
# ==========================================================================

class TestSumPi1:
    def test_sum_uses_first_component(self):
        # A ⊔ B: π₁ = π₁(A) (basepoint in A).
        diamond = AlexandroffSpace("S1_4pt", {0, 1, 2, 3},
                                   [(0, 2), (0, 3), (1, 2), (1, 3)])
        chain = AlexandroffSpace("chain2", {4, 5}, [(4, 5)])
        s = SumSpace([diamond, chain])
        r = pi1_space(s)
        assert r.method == "sum_theorem"
        assert r.group_type == "infinite_cyclic"

    def test_sum_of_contractibles_is_trivial(self):
        chain = AlexandroffSpace("chain2", {0, 1}, [(0, 1)])
        s = SumSpace([chain, chain])
        r = pi1_space(s)
        assert r.is_trivial()


# ==========================================================================
# Pi1Result API
# ==========================================================================

class TestPi1ResultAPI:
    def _trivial(self):
        return pi1_space(AlexandroffSpace("chain2", {0, 1}, [(0, 1)]))

    def _circle(self):
        return pi1_space(AlexandroffSpace("S1_4pt", {0, 1, 2, 3},
                                          [(0, 2), (0, 3), (1, 2), (1, 3)]))

    def test_trivial_group_checks(self):
        r = self._trivial()
        assert r.is_trivial()
        assert r.is_free()
        assert r.abelianization_betti == 0

    def test_circle_group_checks(self):
        r = self._circle()
        assert not r.is_trivial()
        assert r.is_free()
        assert r.abelianization_betti == 1

    def test_presentation_string_format(self):
        r = self._trivial()
        s = r.presentation_string()
        assert "⟩" in s or "|" in s or "<" in s

    def test_notes_non_empty(self):
        r = self._trivial()
        assert len(r.notes) > 0

    def test_space_name_preserved(self):
        chain = AlexandroffSpace("my_chain", {0, 1}, [(0, 1)])
        r = pi1_space(chain)
        assert r.space_name == "my_chain"

    def test_infinite_space_raises(self):
        from pytop.experimental.spaces import CofiniteSpace
        with pytest.raises(NotImplementedError):
            pi1_space(CofiniteSpace())


# ==========================================================================
# SubbaseSpace π₁ computation
# ==========================================================================

class TestSubbasePi1:
    def test_indiscrete_subbase_is_trivial(self):
        # Empty subbase → indiscrete → single specialisation class → trivial π₁.
        s = SubbaseSpace("ind", {0, 1, 2}, [])
        r = pi1_space(s)
        assert r.is_trivial()

    def test_discrete_subbase_trivial_pi1(self):
        # Full discrete subbase on 2 points: each point forms its own connected
        # component; the component at the basepoint is contractible → trivial π₁.
        s = SubbaseSpace("D2", {0, 1}, [{0}, {1}])
        r = pi1_space(s)
        assert r.is_trivial()

    def test_subbase_single_point_trivial(self):
        s = SubbaseSpace("pt", {0}, [{0}])
        r = pi1_space(s)
        assert r.is_trivial()

    def test_subbase_preserves_space_name(self):
        s = SubbaseSpace("my_sub", {0, 1}, [{0}])
        r = pi1_space(s)
        assert r.space_name == "my_sub"


# ==========================================================================
# InverseLimitSpace π₁ computation
# ==========================================================================

class TestInverseLimitPi1:
    def test_inverse_limit_two_points_trivial(self):
        # lim← of two-point discrete spaces with identity: carrier = {(0,0),(1,1)},
        # two isolated points → each contractible component → trivial π₁ at basepoint.
        from pytop.experimental.spaces import discrete_finite_space
        d2 = discrete_finite_space({0, 1})
        from pytop.experimental.spaces.representations import InverseLimitSpace
        lim = InverseLimitSpace("lim←", [d2, d2], [lambda x: x])
        r = pi1_space(lim)
        assert r.is_trivial()

    def test_single_space_inverse_limit_trivial(self):
        # Single-space inverse limit on a contractible space.
        from pytop.experimental.spaces import AlexandroffSpace
        from pytop.experimental.spaces.representations import InverseLimitSpace
        chain = AlexandroffSpace("chain2", {0, 1}, [(0, 1)])
        lim = InverseLimitSpace("lim←1", [chain], [])
        r = pi1_space(lim)
        assert r.is_trivial()
