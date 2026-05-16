"""Extended tests for nets.py — covers all remaining branches."""

import pytest
from pytop import (
    analyze_net,
    is_directed_set,
    is_eventually_in,
    is_frequently_in,
    net_cluster_points,
    net_converges_to,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_IDX = (0, 1, 2)
_PRE = {(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)}  # linear 0≤1≤2
_VAL = {0: 'a', 1: 'b', 2: 'c'}


class _FiniteSpace:
    def __init__(self, carrier, topology):
        self.carrier = carrier
        self.topology = topology


class _SymbolicSpace:
    @property
    def carrier(self):
        raise AttributeError("symbolic")


def _discrete(n):
    pts = list(range(n))
    topo = (
        [frozenset()]
        + [frozenset({p}) for p in pts]
        + [frozenset(pts)]
    )
    return _FiniteSpace(pts, topo)


# ===========================================================================
# is_directed_set — error branches
# ===========================================================================

class TestIsDirectedSetExtended:
    def test_empty_index_set(self):
        r = is_directed_set([], [])
        assert r.is_false
        assert r.metadata['index_count'] == 0

    def test_outside_pairs_rejected(self):
        # pair (0, 9) references 9 which is not in {0, 1, 2}
        pairs = list(_PRE) + [(0, 9)]
        r = is_directed_set(_IDX, pairs)
        assert r.is_false
        assert (0, 9) in r.metadata['outside_pairs']

    def test_missing_reflexive_rejected(self):
        # (1, 1) omitted
        pairs = {(0, 0), (2, 2), (0, 1), (0, 2), (1, 2)}
        r = is_directed_set(_IDX, pairs)
        assert r.is_false
        assert 1 in r.metadata['missing_reflexive_indices']

    def test_non_transitive_rejected(self):
        # 0≤1 and 1≤2 but (0, 2) missing → not transitive
        pairs = {(0, 0), (1, 1), (2, 2), (0, 1), (1, 2)}
        r = is_directed_set(_IDX, pairs)
        assert r.is_false
        assert r.metadata['failed_transitive_triples']

    def test_valid_directed_set(self):
        r = is_directed_set(_IDX, _PRE)
        assert r.is_true and r.is_exact


# ===========================================================================
# is_eventually_in — error branches
# ===========================================================================

class TestIsEventuallyInExtended:
    def test_invalid_directed_set_rejected(self):
        r = is_eventually_in([], [], _VAL, {'a'})
        assert r.is_false
        assert r.metadata['directed_metadata']['index_count'] == 0

    def test_missing_index_in_dict(self):
        # dict covers only 0 and 1 — index 2 missing
        r = is_eventually_in(_IDX, _PRE, {0: 'a', 1: 'b'}, {'a'})
        assert r.is_false
        assert 2 in r.metadata['missing_indices']

    def test_callable_net_values_true(self):
        r = is_eventually_in(_IDX, _PRE, lambda i: 'a', {'a'})
        assert r.is_true

    def test_callable_net_values_false(self):
        r = is_eventually_in(_IDX, _PRE, lambda i: 'x', {'a'})
        assert r.is_false

    def test_invalid_net_values_type(self):
        # int is neither Mapping nor callable
        r = is_eventually_in(_IDX, _PRE, 42, {'a'})  # type: ignore[arg-type]
        assert r.is_false


# ===========================================================================
# is_frequently_in — error branches
# ===========================================================================

class TestIsFrequentlyInExtended:
    def test_invalid_directed_set_rejected(self):
        r = is_frequently_in([], [], _VAL, {'a'})
        assert r.is_false
        assert r.metadata['directed_metadata']['index_count'] == 0

    def test_missing_index_in_dict(self):
        r = is_frequently_in(_IDX, _PRE, {0: 'a', 1: 'b'}, {'a'})
        assert r.is_false
        assert 2 in r.metadata['missing_indices']

    def test_callable_values_true(self):
        r = is_frequently_in(_IDX, _PRE, lambda i: 'a', {'a'})
        assert r.is_true

    def test_invalid_net_values_type(self):
        r = is_frequently_in(_IDX, _PRE, 99, {'a'})  # type: ignore[arg-type]
        assert r.is_false


# ===========================================================================
# net_converges_to — error branches
# ===========================================================================

class TestNetConvergesToExtended:
    def test_invalid_directed_rejected(self):
        sp = _discrete(2)
        r = net_converges_to(sp, [], [], {}, 0)
        assert r.is_false
        assert r.metadata['directed_metadata']['index_count'] == 0

    def test_symbolic_space_returns_unknown(self):
        r = net_converges_to(_SymbolicSpace(), _IDX, _PRE, _VAL, 'x')
        assert not r.is_true
        assert not r.is_false
        assert r.metadata['representation'] == 'symbolic_general'

    def test_point_not_in_carrier(self):
        sp = _discrete(2)
        r = net_converges_to(sp, _IDX, _PRE, {0: 0, 1: 0, 2: 0}, 99)
        assert r.is_false
        assert r.metadata['point'] == 99

    def test_missing_net_values(self):
        sp = _discrete(2)
        r = net_converges_to(sp, _IDX, _PRE, {0: 0, 1: 0}, 0)
        assert r.is_false
        assert 2 in r.metadata['missing_indices']

    def test_values_outside_carrier(self):
        sp = _discrete(2)  # carrier = [0, 1]
        r = net_converges_to(sp, _IDX, _PRE, {0: 99, 1: 99, 2: 99}, 0)
        assert r.is_false
        assert 'values_outside_carrier' in r.metadata


# ===========================================================================
# net_cluster_points — error branches
# ===========================================================================

class TestNetClusterPointsExtended:
    def test_invalid_directed_rejected(self):
        sp = _discrete(2)
        r = net_cluster_points(sp, [], [], {})
        assert r.is_false
        assert r.metadata['directed_metadata']['index_count'] == 0

    def test_symbolic_space_returns_unknown(self):
        r = net_cluster_points(_SymbolicSpace(), _IDX, _PRE, _VAL)
        assert not r.is_true
        assert not r.is_false
        assert r.metadata['representation'] == 'symbolic_general'

    def test_missing_values_rejected(self):
        sp = _discrete(2)
        r = net_cluster_points(sp, _IDX, _PRE, {0: 0, 1: 0})
        assert r.is_false
        assert 2 in r.metadata['missing_indices']

    def test_values_outside_carrier(self):
        sp = _discrete(2)  # carrier = [0, 1]
        r = net_cluster_points(sp, _IDX, _PRE, {0: 99, 1: 99, 2: 99})
        assert r.is_false
        assert 'values_outside_carrier' in r.metadata

    def test_finite_space_cluster_points(self):
        sp = _discrete(2)
        # constant net at 0 → 0 is a cluster point
        r = net_cluster_points(sp, _IDX, _PRE, {0: 0, 1: 0, 2: 0})
        assert r.is_true
        assert 0 in r.value


# ===========================================================================
# analyze_net — all four dispatch paths
# ===========================================================================

class TestAnalyzeNetExtended:
    def test_none_args_returns_unknown(self):
        # index_set / preorder / net_values all None → unknown
        r = analyze_net()
        assert not r.is_true
        assert not r.is_false
        assert r.metadata['operator'] == 'analyze_net'

    def test_subset_only(self):
        # subset provided, no space → eventual + frequent containment
        r = analyze_net(index_set=_IDX, preorder=_PRE, net_values=_VAL, subset={'a'})
        assert r.is_true
        assert 'eventually_in_subset' in r.value
        assert 'frequently_in_subset' in r.value

    def test_space_and_point_without_subset(self):
        # space + point, no subset → cluster + convergence
        sp = _discrete(2)
        vals = {0: 0, 1: 0, 2: 0}
        r = analyze_net(sp, _IDX, _PRE, vals, point=0)
        assert r.is_true
        assert 'cluster_points' in r.value
        assert 'converges_to_point' in r.value
        assert r.value['point_is_cluster_point'] is True

    def test_directed_only_no_subset_no_space(self):
        # neither subset nor space → falls through to directed-only check
        r = analyze_net(index_set=_IDX, preorder=_PRE, net_values=_VAL)
        assert r.is_true
        assert 'directed_set' in r.value
        assert r.value['directed_set'] is True
