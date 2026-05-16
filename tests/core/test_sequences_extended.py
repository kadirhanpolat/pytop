"""Extended tests for sequences.py — branches not covered by existing tests."""

import pytest
from pytop.finite_spaces import FiniteTopologicalSpace
from pytop.infinite_spaces import InfiniteTopologicalSpace
from pytop.sequences import (
    SequenceError,
    analyze_sequences,
    sequence_cluster_point,
    sequence_converges_to,
    sequential_closure,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _discrete(a, b):
    return FiniteTopologicalSpace(
        carrier=(a, b),
        topology=[set(), {a}, {b}, {a, b}],
    )


def _indiscrete(a, b):
    return FiniteTopologicalSpace(carrier=(a, b), topology=[set(), {a, b}])


def _sierpinski():
    return FiniteTopologicalSpace(carrier=(1, 2), topology=[set(), {1}, {1, 2}])


def _symbolic():
    return InfiniteTopologicalSpace(carrier="X", metadata={"representation": "infinite_T2"})


# ---------------------------------------------------------------------------
# sequence_converges_to — symbolic space returns unknown (lines 35-36)
# ---------------------------------------------------------------------------

class TestSequenceConvergesToSymbolic:
    def test_symbolic_space_returns_unknown(self):
        r = sequence_converges_to(_symbolic(), [1, 2], 1)
        assert not r.is_true and not r.is_false

    def test_empty_sequence_returns_false(self):
        X = _discrete(1, 2)
        r = sequence_converges_to(X, [], 1)
        assert r.is_false

    def test_out_of_carrier_term_returns_false(self):
        X = _discrete(1, 2)
        r = sequence_converges_to(X, [1, 99], 1)
        assert r.is_false

    def test_point_not_in_carrier_returns_unknown(self):
        X = _discrete(1, 2)
        r = sequence_converges_to(X, [1, 2], 99)
        assert not r.is_true and not r.is_false

    def test_convergence_true_on_discrete(self):
        X = _discrete(1, 2)
        r = sequence_converges_to(X, [1, 1, 1], 1)
        assert r.is_true

    def test_convergence_false_on_discrete(self):
        # [1, 2, 2]: no tail consists solely of 1s → does not converge to 1
        X = _discrete(1, 2)
        r = sequence_converges_to(X, [1, 2, 2], 1)
        assert r.is_false


# ---------------------------------------------------------------------------
# sequence_cluster_point — symbolic and error paths (lines 131-132, 143)
# ---------------------------------------------------------------------------

class TestSequenceClusterPointEdgeCases:
    def test_symbolic_space_returns_unknown(self):
        r = sequence_cluster_point(_symbolic(), [1, 2], 1)
        assert not r.is_true and not r.is_false

    def test_out_of_carrier_term_returns_false(self):
        X = _discrete(1, 2)
        r = sequence_cluster_point(X, [1, 99], 1)
        assert r.is_false

    def test_cluster_true_on_indiscrete(self):
        X = _indiscrete(1, 2)
        r = sequence_cluster_point(X, [1], 2)
        assert r.is_true

    def test_cluster_false(self):
        X = _discrete(1, 2)
        r = sequence_cluster_point(X, [2, 2], 1)
        assert r.is_false


# ---------------------------------------------------------------------------
# sequential_closure — symbolic and error paths (lines 193-194, 205)
# ---------------------------------------------------------------------------

class TestSequentialClosureEdgeCases:
    def test_symbolic_space_returns_unknown(self):
        r = sequential_closure(_symbolic(), {1})
        assert not r.is_true and not r.is_false

    def test_subset_outside_carrier_returns_false(self):
        X = _discrete(1, 2)
        r = sequential_closure(X, {99})
        assert r.is_false

    def test_basic_closure_on_sierpinski(self):
        X = _sierpinski()
        r = sequential_closure(X, {2})
        assert r.is_true
        assert 2 in r.value


# ---------------------------------------------------------------------------
# Invalid topology — SequenceError caught (lines 298, 305, 307)
# ---------------------------------------------------------------------------

class TestInvalidTopologyHandling:
    def test_topology_missing_empty_set(self):
        bad = FiniteTopologicalSpace(carrier=(1, 2), topology=[{1, 2}])
        r = sequence_converges_to(bad, [1], 1)
        assert not r.is_true and not r.is_false

    def test_topology_missing_full_carrier(self):
        # SequenceError is caught by sequence_converges_to but not sequential_closure
        bad = FiniteTopologicalSpace(carrier=(1, 2), topology=[set()])
        r = sequence_converges_to(bad, [1], 1)
        assert not r.is_true and not r.is_false

    def test_open_set_outside_carrier(self):
        bad = FiniteTopologicalSpace(carrier=(1, 2), topology=[set(), {1, 2}, {1, 99}])
        r = sequence_converges_to(bad, [1], 1)
        assert not r.is_true and not r.is_false


# ---------------------------------------------------------------------------
# analyze_sequences — subset path (lines 272-283)
# ---------------------------------------------------------------------------

class TestAnalyzeSequencesSubsetPath:
    def test_subset_arg_returns_closure_result(self):
        X = _discrete(1, 2)
        r = analyze_sequences(X, subset={1})
        assert r.is_true
        assert 1 in r.value["sequential_closure"]

    def test_subset_with_outside_element_returns_closure_result(self):
        X = _discrete(1, 2)
        r = analyze_sequences(X, subset={99})
        assert r.is_false

    def test_no_args_returns_unknown(self):
        X = _discrete(1, 2)
        r = analyze_sequences(X)
        assert not r.is_true and not r.is_false

    def test_sequence_and_point_returns_dict_result(self):
        X = _discrete(1, 2)
        r = analyze_sequences(X, sequence=[1, 1], point=1)
        assert r.is_true
        assert "converges_to_point" in r.value

    def test_symbolic_closure_falls_through(self):
        s = _symbolic()
        r = analyze_sequences(s, subset={1})
        assert not r.is_true and not r.is_false
