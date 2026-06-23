"""Tests for the six Phase-9 Space representations.

P9.1 OnePointCompactificationSpace — Alexandroff one-point compactification αX
P9.2 StoneCechSpace (βℕ) — Stone–Čech compactification of ℕ
P9.3 HilbertCubeSpace ([0,1]^ω) — Hilbert cube
P9.4 SolenoidSpace (Σ_dyadic) — dyadic solenoid
P9.5 UniformSpace / UniformProduct / UniformSubspace — uniform structure
P9.6 ProfiniteSpace — inverse limit of finite discrete groups; p-adic integers ℤ_p
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from pytop.experimental.spaces import (
    HilbertCubeSpace,
    OnePointCompactificationSpace,
    ProfiniteSpace,
    SolenoidSpace,
    StoneCechSpace,
    UniformProduct,
    UniformSpace,
    UniformSubspace,
    discrete_finite_space,
    dyadic_solenoid,
    hilbert_cube,
    is_compact,
    is_connected,
    is_first_countable,
    is_hausdorff,
    is_lindelof,
    is_normal,
    is_regular,
    is_second_countable,
    is_separable,
    is_t0,
    is_t1,
    is_t5,
    is_t6,
    is_tychonoff,
    metric_uniform_space,
    one_point_compactification,
    p_adic_integers,
    profinite_space,
    rational_uniform_space,
    stone_cech_n,
)
from pytop.experimental.spaces.cardinal_invariants import (
    cellularity,
    character,
    density,
    weight,
)
from pytop.experimental.spaces.core import CardinalValue, CarrierKind, Decidability

# ==========================================================================
# P9.1  OnePointCompactificationSpace
# ==========================================================================


class TestOnePointCompactificationSpace:

    def _discrete2(self) -> OnePointCompactificationSpace:
        return one_point_compactification(discrete_finite_space({0, 1}), "αD₂")

    def _sierpinski(self) -> OnePointCompactificationSpace:
        from pytop.experimental.spaces import FiniteSpace
        s = FiniteSpace("Sier", {0, 1}, [set(), {0}, {0, 1}])
        return one_point_compactification(s, "αSier")

    # -- construction -------------------------------------------------------

    def test_factory_name(self):
        alpha = self._discrete2()
        assert alpha.name == "αD₂"

    def test_default_name(self):
        alpha = one_point_compactification(discrete_finite_space({0, 1}))
        assert "∞" not in alpha.name or "α" in alpha.name

    def test_carrier_kind_preserved_finite(self):
        alpha = self._discrete2()
        assert alpha.carrier_kind is CarrierKind.FINITE

    # -- contains -----------------------------------------------------------

    def test_infinity_always_in_space(self):
        alpha = self._discrete2()
        assert alpha.contains("∞")

    def test_base_points_in_space(self):
        alpha = self._discrete2()
        assert alpha.contains(0)
        assert alpha.contains(1)

    def test_non_member_not_in_space(self):
        alpha = self._discrete2()
        assert not alpha.contains(99)

    # -- points and open_sets -----------------------------------------------

    def test_points_count(self):
        alpha = self._discrete2()
        pts = list(alpha.points())
        assert len(pts) == 3  # {0, 1, ∞}

    def test_points_include_infinity(self):
        alpha = self._discrete2()
        assert "∞" in list(alpha.points())

    def test_open_sets_count_discrete2(self):
        alpha = self._discrete2()
        # opens of D₂: ∅,{0},{1},{0,1}; each union {∞} → 8 opens
        assert len(list(alpha.open_sets())) == 8

    def test_open_sets_include_infinity_singleton(self):
        # compact X → {∞} is open
        alpha = self._discrete2()
        inf_set = frozenset(["∞"])
        assert inf_set in alpha.open_sets()

    def test_open_sets_sierpinski(self):
        alpha = self._sierpinski()
        # Sier has 3 opens → αSier has 6 opens
        assert len(list(alpha.open_sets())) == 6

    def test_infinity_open_in_sierpinski(self):
        alpha = self._sierpinski()
        assert frozenset(["∞"]) in alpha.open_sets()

    # -- point_separation ---------------------------------------------------

    def test_separation_finite_x_from_infinity(self):
        alpha = self._discrete2()
        v = alpha.point_separation(0, "∞")
        assert v.value is True
        assert v.decidability is Decidability.DECIDED

    def test_separation_infinity_from_finite_x_symmetric(self):
        alpha = self._discrete2()
        v = alpha.point_separation("∞", 1)
        assert v.value is True

    def test_separation_two_base_points_uses_base(self):
        alpha = self._discrete2()
        v = alpha.point_separation(0, 1)
        # D₂ is discrete, so 0 and 1 are separated
        assert v.value is True

    # -- certificate --------------------------------------------------------

    def test_compact(self):
        alpha = self._discrete2()
        v = is_compact(alpha)
        assert v.value is True

    def test_connected_false_when_base_compact(self):
        # compact X → αX = X ⊔ {∞} → disconnected
        alpha = self._discrete2()
        v = alpha.certificate("connected")
        assert v is not None
        assert v.value is False

    def test_lindelof(self):
        alpha = self._discrete2()
        v = is_lindelof(alpha)
        assert v.value is True

    def test_t0_inherited(self):
        alpha = self._discrete2()
        v = is_t0(alpha)
        assert v.value is True

    def test_t1_inherited(self):
        alpha = self._discrete2()
        v = is_t1(alpha)
        assert v.value is True


# ==========================================================================
# P9.2  StoneCechSpace (βℕ)
# ==========================================================================


class TestStoneCechSpace:

    def _beta(self) -> StoneCechSpace:
        return stone_cech_n()

    # -- construction -------------------------------------------------------

    def test_factory_name(self):
        assert self._beta().name == "βℕ"

    def test_custom_name(self):
        assert stone_cech_n("myβℕ").name == "myβℕ"

    def test_carrier_kind_uncountable(self):
        assert self._beta().carrier_kind is CarrierKind.UNCOUNTABLE

    # -- contains -----------------------------------------------------------

    def test_natural_numbers_in_beta_n(self):
        beta = self._beta()
        assert beta.contains(0)
        assert beta.contains(100)
        assert beta.contains(999999)

    def test_negative_not_in_beta_n(self):
        assert not self._beta().contains(-1)

    def test_float_not_in_beta_n(self):
        assert not self._beta().contains(0.5)

    def test_string_not_in_beta_n(self):
        assert not self._beta().contains("∞")

    # -- point_separation ---------------------------------------------------

    def test_separate_distinct_naturals(self):
        beta = self._beta()
        v = beta.point_separation(3, 7)
        assert v.value is True
        assert v.decidability is Decidability.DECIDED

    def test_separation_with_clopen_witness(self):
        beta = self._beta()
        v = beta.point_separation(0, 1)
        assert v.witness is not None

    def test_undecidable_for_ultrafilter_pairs(self):
        # Cannot separate non-integer "ultrafilter" inputs
        beta = self._beta()
        v = beta.point_separation(Fraction(1, 2), Fraction(3, 4))
        assert v.decidability is Decidability.UNDECIDABLE

    # -- certificates -------------------------------------------------------

    def test_compact(self):
        assert is_compact(self._beta()).value is True

    def test_hausdorff(self):
        assert is_hausdorff(self._beta()).value is True

    def test_normal(self):
        assert is_normal(self._beta()).value is True

    def test_tychonoff(self):
        assert is_tychonoff(self._beta()).value is True

    def test_not_connected(self):
        assert is_connected(self._beta()).value is False

    def test_lindelof(self):
        assert is_lindelof(self._beta()).value is True

    def test_separable(self):
        # ℕ is a countable dense subspace of βℕ
        assert is_separable(self._beta()).value is True

    def test_not_first_countable(self):
        assert is_first_countable(self._beta()).value is False

    def test_not_second_countable(self):
        assert is_second_countable(self._beta()).value is False

    def test_not_t6(self):
        # compact Hausdorff is T6 iff metrizable; βℕ is not metrizable
        assert is_t6(self._beta()).value is False

    def test_t0(self):
        assert is_t0(self._beta()).value is True

    def test_t1(self):
        assert is_t1(self._beta()).value is True

    # -- cardinal invariants ------------------------------------------------

    def test_weight_continuum(self):
        v = weight(self._beta())
        assert v == CardinalValue.continuum()

    def test_density_aleph0(self):
        v = density(self._beta())
        assert v == CardinalValue.aleph_0()

    def test_character_continuum(self):
        v = character(self._beta())
        assert v == CardinalValue.continuum()


# ==========================================================================
# P9.3  HilbertCubeSpace
# ==========================================================================


class TestHilbertCubeSpace:

    def _hc(self) -> HilbertCubeSpace:
        return hilbert_cube()

    # -- construction -------------------------------------------------------

    def test_factory_name(self):
        assert self._hc().name == "[0,1]^ω"

    def test_custom_name(self):
        assert HilbertCubeSpace("I^ω").name == "I^ω"

    def test_carrier_kind_uncountable(self):
        assert self._hc().carrier_kind is CarrierKind.UNCOUNTABLE

    # -- contains -----------------------------------------------------------

    def test_zero_tuple(self):
        assert self._hc().contains((Fraction(0),))

    def test_one_tuple(self):
        assert self._hc().contains((Fraction(1),))

    def test_midpoint(self):
        assert self._hc().contains((Fraction(1, 2), Fraction(1, 3), Fraction(3, 4)))

    def test_out_of_range(self):
        assert not self._hc().contains((Fraction(3, 2),))

    def test_negative_out_of_range(self):
        assert not self._hc().contains((Fraction(-1, 2),))

    def test_non_tuple(self):
        assert not self._hc().contains(Fraction(1, 2))
        assert not self._hc().contains([Fraction(1, 2)])

    # -- point_separation ---------------------------------------------------

    def test_separate_at_first_coord(self):
        hc = self._hc()
        x = (Fraction(1, 4), Fraction(1, 2))
        y = (Fraction(3, 4), Fraction(1, 2))
        v = hc.point_separation(x, y)
        assert v.value is True
        assert v.witness["coord"] == 0
        assert v.witness["radius"] == Fraction(1, 4)

    def test_separate_at_second_coord(self):
        hc = self._hc()
        x = (Fraction(1, 2), Fraction(1, 4))
        y = (Fraction(1, 2), Fraction(3, 4))
        v = hc.point_separation(x, y)
        assert v.value is True
        assert v.witness["coord"] == 1

    def test_undecidable_when_all_coords_match(self):
        hc = self._hc()
        x = (Fraction(1, 2),)
        y = (Fraction(1, 2),)
        v = hc.point_separation(x, y)
        assert v.decidability is Decidability.UNDECIDABLE

    # -- certificates -------------------------------------------------------

    def test_compact(self):
        assert is_compact(self._hc()).value is True

    def test_connected(self):
        assert is_connected(self._hc()).value is True

    def test_hausdorff(self):
        assert is_hausdorff(self._hc()).value is True

    def test_t6(self):
        assert is_t6(self._hc()).value is True

    def test_t5(self):
        assert is_t5(self._hc()).value is True

    def test_regular(self):
        assert is_regular(self._hc()).value is True

    def test_normal(self):
        assert is_normal(self._hc()).value is True

    def test_tychonoff(self):
        assert is_tychonoff(self._hc()).value is True

    def test_separable(self):
        assert is_separable(self._hc()).value is True

    def test_second_countable(self):
        assert is_second_countable(self._hc()).value is True

    def test_first_countable(self):
        assert is_first_countable(self._hc()).value is True

    def test_lindelof(self):
        assert is_lindelof(self._hc()).value is True

    # -- cardinal invariants ------------------------------------------------

    def test_weight_aleph0(self):
        assert weight(self._hc()) == CardinalValue.aleph_0()

    def test_density_aleph0(self):
        assert density(self._hc()) == CardinalValue.aleph_0()

    def test_character_aleph0(self):
        assert character(self._hc()) == CardinalValue.aleph_0()

    def test_cellularity_aleph0(self):
        assert cellularity(self._hc()) == CardinalValue.aleph_0()


# ==========================================================================
# P9.4  SolenoidSpace
# ==========================================================================


class TestSolenoidSpace:

    def _sol(self) -> SolenoidSpace:
        return dyadic_solenoid()

    # -- construction -------------------------------------------------------

    def test_factory_name(self):
        assert self._sol().name == "Σ_dyadic"

    def test_custom_name(self):
        assert SolenoidSpace("Σ₂").name == "Σ₂"

    def test_carrier_kind_uncountable(self):
        assert self._sol().carrier_kind is CarrierKind.UNCOUNTABLE

    # -- contains: valid compatible sequences --------------------------------

    def test_valid_single_level(self):
        sol = self._sol()
        assert sol.contains((Fraction(1, 3),))

    def test_valid_two_levels(self):
        # θ₀=1/3, θ₁=2/3: 2*(2/3) mod 1 = 4/3 mod 1 = 1/3 ✓
        sol = self._sol()
        assert sol.contains((Fraction(1, 3), Fraction(2, 3)))

    def test_valid_two_levels_alt(self):
        # θ₀=1/3, θ₁=1/6: 2*(1/6) = 1/3 mod 1 = 1/3 ✓
        sol = self._sol()
        assert sol.contains((Fraction(1, 3), Fraction(1, 6)))

    def test_valid_three_levels(self):
        # θ₀=1/3, θ₁=2/3, θ₂=1/3: 2*(1/3) mod 1 = 2/3 ✓
        sol = self._sol()
        assert sol.contains((Fraction(1, 3), Fraction(2, 3), Fraction(1, 3)))

    def test_invalid_angle_out_of_range(self):
        sol = self._sol()
        assert not sol.contains((Fraction(1),))  # 1 is not in [0,1)

    def test_invalid_angle_negative(self):
        sol = self._sol()
        assert not sol.contains((Fraction(-1, 3),))

    def test_invalid_incompatible(self):
        # θ₀=1/3, θ₁=1/2: 2*(1/2)=1 mod 1 = 0 ≠ 1/3
        sol = self._sol()
        assert not sol.contains((Fraction(1, 3), Fraction(1, 2)))

    def test_non_tuple(self):
        assert not self._sol().contains(Fraction(1, 3))

    # -- point_separation ---------------------------------------------------

    def test_separate_at_level_0(self):
        sol = self._sol()
        v = sol.point_separation(
            (Fraction(1, 3), Fraction(2, 3)),
            (Fraction(2, 3), Fraction(1, 3)),
        )
        assert v.value is True
        assert v.witness["level"] == 0

    def test_separate_at_level_1(self):
        sol = self._sol()
        v = sol.point_separation(
            (Fraction(1, 3), Fraction(2, 3)),
            (Fraction(1, 3), Fraction(1, 6)),
        )
        assert v.value is True
        assert v.witness["level"] == 1

    def test_undecidable_same_coords(self):
        sol = self._sol()
        v = sol.point_separation((Fraction(1, 3),), (Fraction(1, 3),))
        assert v.decidability is Decidability.UNDECIDABLE

    # -- certificates -------------------------------------------------------

    def test_compact(self):
        assert is_compact(self._sol()).value is True

    def test_connected(self):
        assert is_connected(self._sol()).value is True

    def test_hausdorff(self):
        assert is_hausdorff(self._sol()).value is True

    def test_t6(self):
        assert is_t6(self._sol()).value is True

    def test_t5(self):
        assert is_t5(self._sol()).value is True

    def test_second_countable(self):
        assert is_second_countable(self._sol()).value is True

    def test_separable(self):
        assert is_separable(self._sol()).value is True

    def test_lindelof(self):
        assert is_lindelof(self._sol()).value is True

    def test_locally_connected_false(self):
        sol = self._sol()
        v = sol.certificate("locally_connected")
        assert v is not None
        assert v.value is False

    # -- cardinal invariants ------------------------------------------------

    def test_weight_aleph0(self):
        assert weight(self._sol()) == CardinalValue.aleph_0()

    def test_density_aleph0(self):
        assert density(self._sol()) == CardinalValue.aleph_0()

    def test_character_aleph0(self):
        assert character(self._sol()) == CardinalValue.aleph_0()


# ==========================================================================
# P9.5  UniformSpace / UniformProduct / UniformSubspace
# ==========================================================================


class TestUniformSpace:

    def _u(self) -> UniformSpace:
        return rational_uniform_space()

    def _u_custom(self) -> UniformSpace:
        return metric_uniform_space(
            "uniform(ℤ)",
            distance=lambda a, b: abs(a - b),
            member=lambda p: isinstance(p, int),
            carrier_kind=CarrierKind.COUNTABLE,
        )

    # -- construction -------------------------------------------------------

    def test_factory_name(self):
        assert self._u().name == "uniform(ℚ)"

    def test_custom_metric(self):
        u = self._u_custom()
        assert u.name == "uniform(ℤ)"

    def test_carrier_kind(self):
        assert self._u().carrier_kind is CarrierKind.COUNTABLE

    # -- contains -----------------------------------------------------------

    def test_rational_member(self):
        u = self._u()
        assert u.contains(Fraction(1, 2))
        assert u.contains(0)
        assert u.contains(-3)

    def test_non_rational(self):
        u = self._u()
        assert not u.contains(0.5)

    def test_integer_member_custom(self):
        u = self._u_custom()
        assert u.contains(5)
        assert not u.contains(Fraction(1, 2))

    # -- entourage ----------------------------------------------------------

    def test_entourage_contains_close_pair(self):
        u = self._u()
        E = u.entourage(Fraction(1, 2))
        assert E(Fraction(1, 4), Fraction(1, 3))  # |1/4 - 1/3| = 1/12 < 1/2

    def test_entourage_excludes_far_pair(self):
        u = self._u()
        E = u.entourage(Fraction(1, 10))
        assert not E(Fraction(0), Fraction(1, 2))  # 1/2 >= 1/10

    def test_entourage_diagonal(self):
        u = self._u()
        E = u.entourage(Fraction(1, 100))
        assert E(Fraction(1, 3), Fraction(1, 3))  # d = 0 < eps

    # -- uniform_neighbourhood ----------------------------------------------

    def test_uniform_neighbourhood_dict(self):
        u = self._u()
        nb = u.uniform_neighbourhood(Fraction(1, 2), Fraction(1, 4))
        assert nb["centre"] == Fraction(1, 2)
        assert nb["radius"] == Fraction(1, 4)

    # -- is_cauchy ----------------------------------------------------------

    def test_cauchy_tight_sequence(self):
        u = self._u()
        seq = [Fraction(k, 1000) for k in range(5)]
        assert u.is_cauchy(seq, Fraction(1, 10))

    def test_not_cauchy_spread_sequence(self):
        u = self._u()
        seq = [Fraction(0), Fraction(1)]
        assert not u.is_cauchy(seq, Fraction(1, 10))

    def test_cauchy_singleton(self):
        u = self._u()
        assert u.is_cauchy([Fraction(1, 2)])

    # -- point_separation ---------------------------------------------------

    def test_separate_distinct(self):
        u = self._u()
        v = u.point_separation(Fraction(0), Fraction(1))
        assert v.value is True
        assert v.witness["radius"] == Fraction(1, 2)

    def test_same_point_not_positive_distance(self):
        u = self._u()
        v = u.point_separation(Fraction(1, 3), Fraction(1, 3))
        assert v.value is False

    # -- certificates -------------------------------------------------------

    def test_hausdorff(self):
        assert is_hausdorff(self._u()).value is True

    def test_t5(self):
        assert is_t5(self._u()).value is True

    def test_t6(self):
        assert is_t6(self._u()).value is True

    def test_first_countable(self):
        assert is_first_countable(self._u()).value is True


class TestUniformProduct:

    def _q2(self) -> UniformProduct:
        u = rational_uniform_space()
        return UniformProduct(u, u, name="uniform(ℚ²)")

    def test_name(self):
        assert self._q2().name == "uniform(ℚ²)"

    def test_contains_rational_pair(self):
        q2 = self._q2()
        assert q2.contains((Fraction(1, 2), Fraction(1, 3)))

    def test_does_not_contain_single(self):
        q2 = self._q2()
        assert not q2.contains(Fraction(1, 2))

    def test_does_not_contain_triple(self):
        q2 = self._q2()
        assert not q2.contains((Fraction(1, 2), Fraction(1, 3), Fraction(1, 4)))

    def test_sup_metric_separation(self):
        q2 = self._q2()
        x = (Fraction(0), Fraction(0))
        y = (Fraction(3, 4), Fraction(1, 4))
        v = q2.point_separation(x, y)
        assert v.value is True
        # sup-metric = max(3/4, 1/4) = 3/4; radius = 3/8
        assert v.witness["radius"] == Fraction(3, 8)

    def test_hausdorff(self):
        assert is_hausdorff(self._q2()).value is True

    def test_construction_attribute(self):
        q2 = self._q2()
        assert q2.construction is not None
        assert q2.construction[0] == "uniform_product"


class TestUniformSubspace:

    def _unit(self) -> UniformSubspace:
        u = rational_uniform_space()
        return UniformSubspace(u, lambda x: Fraction(0) <= x <= Fraction(1), "uniform([0,1]∩ℚ)")

    def test_name(self):
        assert self._unit().name == "uniform([0,1]∩ℚ)"

    def test_contains_in_range(self):
        sub = self._unit()
        assert sub.contains(Fraction(1, 2))
        assert sub.contains(Fraction(0))
        assert sub.contains(Fraction(1))

    def test_excludes_outside_range(self):
        sub = self._unit()
        assert not sub.contains(Fraction(2))
        assert not sub.contains(Fraction(-1, 2))

    def test_separation_within_subspace(self):
        sub = self._unit()
        v = sub.point_separation(Fraction(1, 4), Fraction(3, 4))
        assert v.value is True

    def test_construction_attribute(self):
        sub = self._unit()
        assert sub.construction is not None
        assert sub.construction[0] == "uniform_subspace"

    def test_hausdorff(self):
        assert is_hausdorff(self._unit()).value is True


# ==========================================================================
# P9.6  ProfiniteSpace
# ==========================================================================


class TestProfiniteSpace:

    def _z5(self) -> ProfiniteSpace:
        return p_adic_integers(5)

    def _z2(self) -> ProfiniteSpace:
        return p_adic_integers(2)

    def _generic(self) -> ProfiniteSpace:
        # lim← ℤ/2 ← ℤ/4 ← ℤ/8 (binary inverse limit)
        return profinite_space("bin", [2, 4, 8], lambda a, k: a % (2 ** (k + 1)))

    # -- construction -------------------------------------------------------

    def test_p_adic_name(self):
        assert self._z5().name == "ℤ_5"

    def test_p_adic_2_name(self):
        assert self._z2().name == "ℤ_2"

    def test_invalid_prime_raises(self):
        with pytest.raises(ValueError):
            p_adic_integers(1)

    def test_carrier_kind_uncountable(self):
        assert self._z5().carrier_kind is CarrierKind.UNCOUNTABLE

    # -- contains: p-adic integers -------------------------------------------

    def test_valid_single_level(self):
        z5 = self._z5()
        assert z5.contains((3,))

    def test_valid_two_levels(self):
        # (3, 8): a₁=8 ∈ ℤ/25; 8 mod 5 = 3 = a₀ ✓
        assert self._z5().contains((3, 8))

    def test_valid_three_levels(self):
        # (3, 8, 33): a₂=33 ∈ ℤ/125; 33 mod 25 = 8 = a₁ ✓
        assert self._z5().contains((3, 8, 33))

    def test_invalid_out_of_range(self):
        z5 = self._z5()
        assert not z5.contains((5,))  # 5 ≥ 5 is out of ℤ/5

    def test_invalid_incompatible(self):
        # (3, 9): 9 mod 5 = 4 ≠ 3
        assert not self._z5().contains((3, 9))

    def test_empty_tuple_invalid(self):
        assert not self._z5().contains(())

    def test_non_tuple_invalid(self):
        assert not self._z5().contains(3)

    def test_z2_valid_point(self):
        # ℤ/2: (0, 2): 2 mod 2 = 0 ✓; 2 ∈ ℤ/4 ✓
        assert self._z2().contains((0, 2))

    def test_z2_another_valid(self):
        # (1, 3): 3 mod 2 = 1 ✓; 3 ∈ ℤ/4 ✓
        assert self._z2().contains((1, 3))

    # -- point_separation ---------------------------------------------------

    def test_separate_at_level_0(self):
        z5 = self._z5()
        v = z5.point_separation((0, 5), (1, 6))
        assert v.value is True
        assert v.witness["level"] == 0

    def test_separate_at_level_1(self):
        z5 = self._z5()
        # Same level-0, differ at level-1
        v = z5.point_separation((3, 8), (3, 13))  # 13 mod 5 = 3 = a₀ ✓; differ at level 1
        assert v.value is True
        assert v.witness["level"] == 1

    def test_undecidable_same_coords(self):
        z5 = self._z5()
        v = z5.point_separation((3,), (3,))
        assert v.decidability is Decidability.UNDECIDABLE

    # -- certificates -------------------------------------------------------

    def test_compact(self):
        assert is_compact(self._z5()).value is True

    def test_hausdorff(self):
        assert is_hausdorff(self._z5()).value is True

    def test_not_connected(self):
        assert is_connected(self._z5()).value is False

    def test_t6(self):
        assert is_t6(self._z5()).value is True

    def test_t5(self):
        assert is_t5(self._z5()).value is True

    def test_regular(self):
        assert is_regular(self._z5()).value is True

    def test_normal(self):
        assert is_normal(self._z5()).value is True

    def test_tychonoff(self):
        assert is_tychonoff(self._z5()).value is True

    def test_second_countable(self):
        assert is_second_countable(self._z5()).value is True

    def test_separable(self):
        assert is_separable(self._z5()).value is True

    def test_first_countable(self):
        assert is_first_countable(self._z5()).value is True

    def test_lindelof(self):
        assert is_lindelof(self._z5()).value is True

    # -- cardinal invariants ------------------------------------------------

    def test_weight_aleph0(self):
        assert weight(self._z5()) == CardinalValue.aleph_0()

    def test_density_aleph0(self):
        assert density(self._z5()) == CardinalValue.aleph_0()

    def test_character_aleph0(self):
        assert character(self._z5()) == CardinalValue.aleph_0()

    def test_cellularity_aleph0(self):
        assert cellularity(self._z5()) == CardinalValue.aleph_0()

    # -- generic profinite_space factory ------------------------------------

    def test_generic_factory(self):
        g = self._generic()
        assert g.name == "bin"

    def test_generic_valid_point(self):
        g = self._generic()
        # (1, 1): 1 ∈ ℤ/2; a₁=1 ∈ ℤ/4; 1 mod 2 = 1 ✓
        assert g.contains((1, 1))

    def test_generic_invalid_point(self):
        g = self._generic()
        # (1, 2): 2 mod 2 = 0 ≠ 1
        assert not g.contains((1, 2))
