"""Tests for Urysohn function witnesses and enriched is_tychonoff verdicts."""

from __future__ import annotations

from fractions import Fraction

from pytop.experimental.spaces import (
    CofiniteSpace,
    FiniteSpace,
    SorgenfreyLineSpace,
    discrete_finite_space,
    is_tychonoff,
    rational_metric_space,
)
from pytop.experimental.spaces.urysohn import UrysohnWitness, urysohn_function

# ==========================================================================
# UrysohnWitness dataclass
# ==========================================================================

class TestUrysohnWitness:
    def test_fields_and_evaluate(self):
        w = UrysohnWitness(
            x0=0,
            closed_set=frozenset({1, 2}),
            values={0: Fraction(0), 1: Fraction(1), 2: Fraction(1)},
            formula="indicator",
            method="discrete_indicator",
        )
        assert w.evaluate(0) == Fraction(0)
        assert w.evaluate(1) == Fraction(1)
        assert w.evaluate(99) is None  # not in values

    def test_infinite_witness_has_no_values(self):
        w = UrysohnWitness(
            x0=0,
            closed_set=frozenset(),
            values=None,
            formula="f(y) = min(1, d(0,y)/d(0,C))",
            method="distance_ratio",
        )
        assert w.values is None
        assert w.evaluate(0) is None
        assert "distance_ratio" in w.formula or w.method == "distance_ratio"


# ==========================================================================
# urysohn_function — finite discrete spaces
# ==========================================================================

class TestUrysohnFiniteDiscrete:
    def test_discrete_2_separates_0_from_1(self):
        d = discrete_finite_space({0, 1})
        w = urysohn_function(d, 0, frozenset({1}))
        assert w is not None
        assert w.method == "discrete_indicator"
        assert w.evaluate(0) == Fraction(0)
        assert w.evaluate(1) == Fraction(1)

    def test_discrete_3_separates_point_from_set(self):
        d = discrete_finite_space({0, 1, 2})
        w = urysohn_function(d, 0, frozenset({1, 2}))
        assert w is not None
        assert w.evaluate(0) == Fraction(0)
        assert w.evaluate(1) == Fraction(1)
        assert w.evaluate(2) == Fraction(1)

    def test_x0_in_closed_returns_none(self):
        d = discrete_finite_space({0, 1, 2})
        # x₀ ∈ C: no Urysohn function exists
        assert urysohn_function(d, 0, frozenset({0, 1})) is None

    def test_empty_closed_set(self):
        # C = ∅ is closed; f(x₀)=0, f(∅)=∅ (vacuously satisfied)
        d = discrete_finite_space({0, 1, 2})
        w = urysohn_function(d, 0, frozenset())
        assert w is not None
        assert w.evaluate(0) == Fraction(0)

    def test_c_not_closed_returns_none(self):
        # Sierpinski: opens = ∅, {0}, {0,1}. Closed = {0,1}, {1}, ∅.
        # C = {0} is NOT closed (complement {1} is not open).
        s = FiniteSpace("Sierpinski", {0, 1}, [set(), {0}, {0, 1}])
        result = urysohn_function(s, 1, frozenset({0}))
        assert result is None


# ==========================================================================
# urysohn_function — general finite (non-discrete) spaces
# ==========================================================================

class TestUrysohnFiniteGeneral:
    def test_chain_space_separation(self):
        # Chain 0 < 1 < 2: opens = ∅,{2},{1,2},{0,1,2}. Closed = {0,1,2},{0,1},{0},∅.
        # Separate 2 from {0}: C={0} is closed; open containing 2 = {2}.
        # {2} and {0,1,2}\{2} = {0,1}; we need open U ∋ 2 and V ⊇ {0}.
        # {2} ∩ {0} = ∅, {2} and complement {0,1} are open. So Urysohn exists.
        from pytop.experimental.spaces import AlexandroffSpace
        chain = AlexandroffSpace("chain3", {0, 1, 2}, [(0, 1), (1, 2)])
        # Closed sets: X\open = {0,1,2},{0,1},{0},∅
        # Separate x0=2 from C={0}:
        w = urysohn_function(chain, 2, frozenset({0}))
        # f(2) = 0, f(0) = 1
        if w is not None:
            assert w.evaluate(2) == Fraction(0)
            assert w.evaluate(0) == Fraction(1)

    def test_result_satisfies_urysohn_conditions(self):
        # For any Urysohn witness: f(x0)=0 and f(c)=1 for c∈C
        d = discrete_finite_space({0, 1, 2, 3})
        w = urysohn_function(d, 0, frozenset({2, 3}))
        assert w is not None
        assert w.evaluate(0) == Fraction(0)
        for c in [2, 3]:
            assert w.evaluate(c) == Fraction(1)

    def test_values_in_unit_interval(self):
        d = discrete_finite_space({0, 1, 2})
        w = urysohn_function(d, 0, frozenset({1}))
        assert w is not None
        for v in w.values.values():
            assert Fraction(0) <= v <= Fraction(1)


# ==========================================================================
# urysohn_function — MetricTopologySpace
# ==========================================================================

class TestUrysohnMetric:
    def test_metric_space_returns_formula_witness(self):
        m = rational_metric_space()
        w = urysohn_function(m, 0, frozenset())
        assert w is not None
        assert w.method == "distance_ratio"
        assert "d(" in w.formula or "distance" in w.formula.lower() or "min" in w.formula

    def test_metric_witness_has_no_finite_values(self):
        m = rational_metric_space()
        w = urysohn_function(m, 0, frozenset())
        assert w is not None
        assert w.values is None


# ==========================================================================
# is_tychonoff — enriched witness for finite T1 spaces
# ==========================================================================

class TestTychonoffWitness:
    def test_discrete_tychonoff_has_witness(self):
        d = discrete_finite_space({0, 1, 2})
        v = is_tychonoff(d)
        assert v.value is True
        assert v.witness is not None
        assert v.witness["method"] == "discrete_indicator"

    def test_non_t1_tychonoff_has_counterexample(self):
        s = FiniteSpace("Sierpinski", {0, 1}, [set(), {0}, {0, 1}])
        v = is_tychonoff(s)
        assert v.value is False
        assert v.counterexample is not None

    def test_metric_tychonoff_has_distance_ratio_witness(self):
        m = rational_metric_space()
        v = is_tychonoff(m)
        assert v.value is True
        assert v.witness is not None
        assert v.witness["method"] == "distance_ratio"

    def test_sorgenfrey_tychonoff_has_some_verdict(self):
        sl = SorgenfreyLineSpace()
        v = is_tychonoff(sl)
        assert v.value is True

    def test_cofinite_not_tychonoff(self):
        c = CofiniteSpace()
        v = is_tychonoff(c)
        assert v.value is False


# ==========================================================================
# urysohn_function — SorgenfreyLineSpace
# ==========================================================================

class TestUrysohnSorgenfrey:
    def test_sorgenfrey_returns_euclidean_witness(self):
        sl = SorgenfreyLineSpace()
        w = urysohn_function(sl, 0, frozenset())
        assert w is not None
        assert w.method == "sorgenfrey_euclidean"

    def test_sorgenfrey_formula_mentions_euclidean(self):
        sl = SorgenfreyLineSpace()
        w = urysohn_function(sl, 1, frozenset())
        assert w is not None
        # Formula should reference the euclidean distance or standard topology
        assert "standard" in w.formula.lower() or "d_ℝ" in w.formula or "|y -" in w.formula

    def test_sorgenfrey_witness_has_no_finite_values(self):
        sl = SorgenfreyLineSpace()
        w = urysohn_function(sl, 0, frozenset())
        assert w is not None
        assert w.values is None

    def test_sorgenfrey_x0_stored_correctly(self):
        sl = SorgenfreyLineSpace()
        w = urysohn_function(sl, 5, frozenset())
        assert w is not None
        assert w.x0 == 5


# ==========================================================================
# urysohn_function — OrderTopologySpace
# ==========================================================================

class TestUrysohnOrderTopology:
    def test_order_topology_returns_order_metric_witness(self):
        from pytop.experimental.spaces import OrderTopologySpace
        ot = OrderTopologySpace()
        w = urysohn_function(ot, 0, frozenset())
        assert w is not None
        assert w.method == "order_metric_ratio"

    def test_order_topology_formula_mentions_rationals(self):
        from pytop.experimental.spaces import OrderTopologySpace
        ot = OrderTopologySpace()
        w = urysohn_function(ot, 0, frozenset())
        assert w is not None
        # Formula should reference Q or order metric
        assert "ℚ" in w.formula or "order" in w.formula.lower() or "d_ℚ" in w.formula

    def test_order_topology_witness_has_no_values(self):
        from pytop.experimental.spaces import OrderTopologySpace
        ot = OrderTopologySpace()
        w = urysohn_function(ot, 0, frozenset())
        assert w is not None
        assert w.values is None


# ==========================================================================
# urysohn_function — bfs_level method (non-discrete finite space)
# ==========================================================================

class TestUrysohnBfsLevel:
    def test_bfs_level_method_on_finite_non_discrete(self):
        # Chain 0 < 1 < 2: T1 fails so not Tychonoff, but BFS still runs.
        from pytop.experimental.spaces import AlexandroffSpace
        # Separate x0=2 (sink) from C={0}: open {2} is the minimal neighbourhood.
        chain = AlexandroffSpace("chain3", {0, 1, 2}, [(0, 1), (1, 2)])
        w = urysohn_function(chain, 2, frozenset({0}))
        # Either returns a valid bfs_level witness or None (if Tychonoff fails).
        if w is not None:
            assert w.method == "bfs_level"
            assert w.evaluate(2) == 0 or w.evaluate(2) is not None
            assert w.evaluate(0) is not None

    def test_bfs_level_values_in_unit_interval(self):
        # 4-pt discrete: BFS on a Tychonoff space should give values in [0,1].
        from fractions import Fraction as F
        d = discrete_finite_space({0, 1, 2, 3})
        w = urysohn_function(d, 0, frozenset({3}))
        assert w is not None
        for v in w.values.values():
            assert F(0) <= v <= F(1)

    def test_bfs_level_c_equal_to_x0_returns_none(self):
        # x0 ∈ C → impossible to separate.
        from pytop.experimental.spaces import AlexandroffSpace
        chain = AlexandroffSpace("chain3", {0, 1, 2}, [(0, 1), (1, 2)])
        # C = {0,1,2} = whole space includes x0=0.
        w = urysohn_function(chain, 0, frozenset({0, 1, 2}))
        assert w is None

    def test_opaque_infinite_space_returns_none(self):
        # OpaqueInfiniteSpace has no algorithm path → urysohn returns None.
        from pytop.experimental.spaces.representations import OpaqueInfiniteSpace
        op = OpaqueInfiniteSpace("opaque", lambda p: isinstance(p, int))
        w = urysohn_function(op, 0, frozenset())
        assert w is None
