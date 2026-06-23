"""Tests for computed cardinal invariants (weight, density, character, cellularity).

Each test is labelled with the mathematical fact it verifies.
"""

from __future__ import annotations

import pytest

from pytop.experimental.spaces import (
    CardinalValue,
    CofiniteSpace,
    DiscreteCountableSpace,
    FiniteSpace,
    OrderTopologySpace,
    SorgenfreyLineSpace,
    discrete_finite_space,
    rational_metric_space,
)
from pytop.experimental.spaces.cardinal_invariants import (
    cellularity,
    character,
    density,
    weight,
)

# --------------------------------------------------------------------------
# CardinalValue
# --------------------------------------------------------------------------

class TestCardinalValue:
    def test_finite(self):
        cv = CardinalValue.of(3)
        assert cv.finite == 3
        assert cv.symbol is None
        assert cv.is_finite_cardinal()
        assert repr(cv) == "3"

    def test_aleph_0(self):
        cv = CardinalValue.aleph_0()
        assert cv.finite is None
        assert cv.symbol == "ℵ₀"
        assert not cv.is_finite_cardinal()
        assert repr(cv) == "ℵ₀"

    def test_continuum(self):
        cv = CardinalValue.continuum()
        assert cv.symbol == "𝔠"

    def test_unknown(self):
        cv = CardinalValue.unknown()
        assert cv.symbol == "unknown"

    def test_invalid_negative(self):
        with pytest.raises(ValueError):
            CardinalValue(finite=-1)

    def test_invalid_both_none(self):
        with pytest.raises(ValueError):
            CardinalValue()


# --------------------------------------------------------------------------
# Weight
# --------------------------------------------------------------------------

class TestWeight:
    def test_discrete_3_weight_equals_3(self):
        # Discrete space on n points has weight n (singletons form a minimum base).
        d = discrete_finite_space({0, 1, 2})
        assert weight(d) == CardinalValue.of(3)

    def test_indiscrete_weight_is_0(self):
        # Indiscrete: only ∅ and X open; empty set needs no base element; whole space
        # is the only non-empty open.  Minimum base = {X}, so weight = 1... wait:
        # Actually minimum base for {∅, X} requires {X} (since X must be covered).
        # But ∅ is always covered (union of empty family). So weight = 1.
        ind = FiniteSpace("indiscrete", {0, 1}, [set(), {0, 1}])
        assert weight(ind) == CardinalValue.of(1)

    def test_sierpinski_weight(self):
        # Sierpinski opens: ∅, {0}, {0,1}. Minimum base: {{0}} suffices since
        # {0,1} = union of {0} ∪ {0,1}... wait: we need to cover {0,1}.
        # Is {0} alone a base?  We need to cover {0,1}: for every x in {0,1},
        # ∃ B_i in base with x in B_i ⊆ {0,1}.
        # For x=0: {0} ⊆ {0,1} ✓. For x=1: need B_i with 1 in B_i ⊆ {0,1}.
        # The only open containing 1 is {0,1} itself. So {0,1} must be in the base.
        # Minimum base: {{0}, {0,1}}, weight = 2.
        s = FiniteSpace("Sierpinski", {0, 1}, [set(), {0}, {0, 1}])
        assert weight(s) == CardinalValue.of(2)

    def test_cofinite_weight_is_aleph_0(self):
        assert weight(CofiniteSpace()) == CardinalValue.aleph_0()

    def test_order_topology_weight_is_aleph_0(self):
        assert weight(OrderTopologySpace()) == CardinalValue.aleph_0()

    def test_sorgenfrey_weight_is_aleph_0(self):
        assert weight(SorgenfreyLineSpace()) == CardinalValue.aleph_0()

    def test_discrete_countable_weight_is_aleph_0(self):
        assert weight(DiscreteCountableSpace()) == CardinalValue.aleph_0()

    def test_metric_q_weight_unknown(self):
        # Generic MetricTopologySpace has no weight certificate (honest).
        assert weight(rational_metric_space()) == CardinalValue.unknown()


# --------------------------------------------------------------------------
# Density
# --------------------------------------------------------------------------

class TestDensity:
    def test_indiscrete_density_is_1(self):
        # Every nonempty open is the whole space; any single point is dense.
        ind = FiniteSpace("indiscrete", {0, 1, 2}, [set(), {0, 1, 2}])
        assert density(ind) == CardinalValue.of(1)

    def test_discrete_3_density_is_3(self):
        # Every singleton {x} is open and disjoint from {y} for x≠y,
        # so any dense set must contain all points.
        d = discrete_finite_space({0, 1, 2})
        assert density(d) == CardinalValue.of(3)

    def test_sierpinski_density(self):
        # Sierpinski opens: ∅, {0}, {0,1}. Dense D iff D ∩ {0} ≠ ∅, D ∩ {0,1} ≠ ∅.
        # {0} satisfies both. So density = 1.
        s = FiniteSpace("Sierpinski", {0, 1}, [set(), {0}, {0, 1}])
        assert density(s) == CardinalValue.of(1)

    def test_cofinite_density_is_aleph_0(self):
        assert density(CofiniteSpace()) == CardinalValue.aleph_0()

    def test_sorgenfrey_density_is_aleph_0(self):
        assert density(SorgenfreyLineSpace()) == CardinalValue.aleph_0()

    def test_discrete_countable_density_is_aleph_0(self):
        assert density(DiscreteCountableSpace()) == CardinalValue.aleph_0()


# --------------------------------------------------------------------------
# Character
# --------------------------------------------------------------------------

class TestCharacter:
    def test_discrete_character_is_1(self):
        # Each point x has {x} as a local base of size 1.
        d = discrete_finite_space({0, 1, 2})
        assert character(d) == CardinalValue.of(1)

    def test_indiscrete_character_is_1(self):
        # The only open containing any point is the whole space; local base = {X}.
        ind = FiniteSpace("indiscrete", {0, 1}, [set(), {0, 1}])
        assert character(ind) == CardinalValue.of(1)

    def test_sorgenfrey_character_is_aleph_0(self):
        assert character(SorgenfreyLineSpace()) == CardinalValue.aleph_0()

    def test_metric_space_character_is_aleph_0(self):
        # Every metric space is first countable.
        m = rational_metric_space()
        assert character(m) == CardinalValue.aleph_0()

    def test_discrete_countable_character_is_1(self):
        # Discrete N: singleton {x} is a local base of size 1 at each x.
        assert character(DiscreteCountableSpace()) == CardinalValue.of(1)

    def test_cofinite_character_is_aleph_0(self):
        assert character(CofiniteSpace()) == CardinalValue.aleph_0()


# --------------------------------------------------------------------------
# Cellularity
# --------------------------------------------------------------------------

class TestCellularity:
    def test_discrete_3_cellularity_is_3(self):
        # Singletons {0}, {1}, {2} are pairwise disjoint opens.
        d = discrete_finite_space({0, 1, 2})
        assert cellularity(d) == CardinalValue.of(3)

    def test_indiscrete_cellularity_is_1(self):
        # Only one nonempty open (the whole space); max disjoint family size = 1.
        ind = FiniteSpace("indiscrete", {0, 1, 2}, [set(), {0, 1, 2}])
        assert cellularity(ind) == CardinalValue.of(1)

    def test_sierpinski_cellularity(self):
        # Opens: ∅, {0}, {0,1}. {0} and {0,1} intersect. Only family of size 1.
        s = FiniteSpace("Sierpinski", {0, 1}, [set(), {0}, {0, 1}])
        assert cellularity(s) == CardinalValue.of(1)

    def test_cofinite_cellularity_is_1(self):
        # Any two nonempty cofinite opens intersect (their union complement is finite).
        assert cellularity(CofiniteSpace()) == CardinalValue.of(1)

    def test_sorgenfrey_cellularity_is_aleph_0(self):
        assert cellularity(SorgenfreyLineSpace()) == CardinalValue.aleph_0()

    def test_discrete_countable_cellularity_is_aleph_0(self):
        assert cellularity(DiscreteCountableSpace()) == CardinalValue.aleph_0()

    def test_order_topology_cellularity_is_aleph_0(self):
        assert cellularity(OrderTopologySpace()) == CardinalValue.aleph_0()
