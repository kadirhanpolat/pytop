"""Extended tests for filters.py — covers all remaining branches."""

import pytest
from pytop import (
    analyze_filter,
    filter_cluster_points,
    filter_clusters_at,
    filter_converges_to,
    generated_filter,
    is_filter,
    is_filter_base,
    is_finer_filter,
    neighborhood_filter_base,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

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
# is_filter_base — error branches
# ===========================================================================

class TestIsFilterBaseExtended:
    def test_empty_family_rejected(self):
        r = is_filter_base({1, 2}, [])
        assert r.is_false
        assert 'non-empty' in r.justification[0].lower()

    def test_empty_set_in_family_rejected(self):
        r = is_filter_base({1, 2}, [set()])
        assert r.is_false
        assert 'empty set' in r.justification[0].lower()

    def test_elements_outside_carrier_rejected(self):
        r = is_filter_base({1, 2}, [{1, 3}])  # 3 not in carrier
        assert r.is_false
        assert 'outside the carrier' in r.justification[0].lower()

    def test_failed_intersection_pair_rejected(self):
        # {1} ∩ {2} = {} has no base element below it
        r = is_filter_base({1, 2}, [{1}, {2}])
        assert r.is_false
        assert r.metadata['failed_intersection_pairs'] > 0

    def test_valid_base(self):
        r = is_filter_base({1, 2, 3}, [{1, 2}])
        assert r.is_true


# ===========================================================================
# generated_filter — invalid base
# ===========================================================================

class TestGeneratedFilterExtended:
    def test_invalid_base_rejected(self):
        r = generated_filter({1, 2}, [])  # empty → not a valid filter base
        assert r.is_false

    def test_valid_base_generates_filter(self):
        r = generated_filter({1, 2}, [{1}])
        assert r.is_true
        assert frozenset({1}) in r.value
        assert frozenset({1, 2}) in r.value


# ===========================================================================
# is_filter — error branches
# ===========================================================================

class TestIsFilterExtended:
    def test_empty_family_rejected(self):
        r = is_filter({1, 2}, [])
        assert r.is_false
        assert 'non-empty' in r.justification[0].lower()

    def test_empty_set_in_family_rejected(self):
        r = is_filter({1, 2}, [set(), {1, 2}])
        assert r.is_false
        assert '(F1)' in r.justification[0]

    def test_f2_failure_rejected(self):
        # {1} ∩ {2} = {} ∉ family
        r = is_filter({1, 2}, [{1}, {2}, {1, 2}])
        assert r.is_false
        assert r.metadata['failed_f2_pairs'] > 0

    def test_f3_failure_rejected(self):
        # {1} in family but superset {1, 2} within carrier is not
        r = is_filter({1, 2, 3}, [{1}])
        assert r.is_false
        assert r.metadata['failed_f3_pairs'] > 0

    def test_valid_filter(self):
        r = is_filter({1, 2}, [{1}, {1, 2}])
        assert r.is_true


# ===========================================================================
# neighborhood_filter_base — error branches
# ===========================================================================

class TestNeighborhoodFilterBaseExtended:
    def test_symbolic_space_returns_unknown(self):
        r = neighborhood_filter_base(_SymbolicSpace(), 0)
        assert not r.is_true
        assert not r.is_false
        assert r.metadata['operator'] == 'neighborhood_filter_base'

    def test_point_not_in_carrier(self):
        sp = _discrete(2)
        r = neighborhood_filter_base(sp, 99)
        assert r.is_false
        assert r.metadata['point'] == 99

    def test_no_open_neighborhoods(self):
        # topology contains only the empty open set; no non-empty set contains the point
        sp = _FiniteSpace([0, 1], [frozenset()])
        r = neighborhood_filter_base(sp, 0)
        assert r.is_false


# ===========================================================================
# filter_converges_to — error branches
# ===========================================================================

class TestFilterConvergesToExtended:
    def test_symbolic_space_returns_unknown(self):
        r = filter_converges_to(_SymbolicSpace(), [{1, 2}], 1)
        assert not r.is_true
        assert not r.is_false

    def test_point_not_in_carrier(self):
        sp = _discrete(2)
        r = filter_converges_to(sp, [frozenset({0, 1})], 99)
        assert r.is_false
        assert r.metadata['point'] == 99

    def test_missing_open_neighborhood(self):
        # discrete space: {0} is an open nbhd of 0 but not in the filter
        sp = _discrete(2)
        r = filter_converges_to(sp, [frozenset({0, 1})], 0)
        assert r.is_false
        assert r.metadata['missing_open_neighborhoods'] > 0


# ===========================================================================
# is_finer_filter — error branches
# ===========================================================================

class TestIsFinerFilterExtended:
    def test_invalid_inputs_rejected(self):
        # empty families are not valid filters
        r = is_finer_filter({1, 2}, [], [])
        assert r.is_false

    def test_missing_coarser_members(self):
        carrier = {0, 1}
        # trivial filter {{0,1}} does not contain {0} from the principal filter
        finer = [frozenset({0, 1})]
        coarser = [frozenset({0}), frozenset({0, 1})]
        r = is_finer_filter(carrier, finer, coarser)
        assert r.is_false
        assert r.metadata['missing_coarser_members'] > 0

    def test_valid_refinement(self):
        carrier = {0, 1}
        finer = [frozenset({0}), frozenset({0, 1})]
        coarser = [frozenset({0, 1})]
        r = is_finer_filter(carrier, finer, coarser)
        assert r.is_true


# ===========================================================================
# filter_clusters_at — error branches
# ===========================================================================

class TestFilterClustersAtExtended:
    def test_symbolic_space_returns_unknown(self):
        r = filter_clusters_at(_SymbolicSpace(), [{1, 2}], 1)
        assert not r.is_true
        assert not r.is_false

    def test_point_not_in_carrier(self):
        sp = _discrete(2)
        r = filter_clusters_at(sp, [frozenset({0, 1})], 99)
        assert r.is_false
        assert r.metadata['point'] == 99

    def test_invalid_filter_rejected(self):
        sp = _discrete(2)
        # frozenset() (empty set) in family → fails F1
        r = filter_clusters_at(sp, [frozenset(), frozenset({0, 1})], 0)
        assert r.is_false
        assert 'valid filter' in r.justification[0].lower()

    def test_failed_neighborhood_member_pair(self):
        # discrete space: {0} is open nbhd of 0; filter member {1} is disjoint
        sp = _discrete(2)
        fam = [frozenset({1}), frozenset({0, 1})]
        r = filter_clusters_at(sp, fam, 0)
        assert r.is_false
        assert r.metadata['failed_neighborhood_member_pairs'] > 0

    def test_true_case(self):
        sp = _discrete(2)
        fam = [frozenset({0}), frozenset({0, 1})]
        r = filter_clusters_at(sp, fam, 0)
        assert r.is_true


# ===========================================================================
# filter_cluster_points — error branches
# ===========================================================================

class TestFilterClusterPointsExtended:
    def test_symbolic_space_returns_unknown(self):
        r = filter_cluster_points(_SymbolicSpace(), [{1, 2}])
        assert not r.is_true
        assert not r.is_false

    def test_invalid_filter_rejected(self):
        sp = _discrete(2)
        # empty set in family → invalid filter
        r = filter_cluster_points(sp, [frozenset()])
        assert r.is_false

    def test_valid_filter(self):
        sp = _discrete(2)
        fam = [frozenset({0}), frozenset({0, 1})]
        r = filter_cluster_points(sp, fam)
        assert r.is_true
        assert 0 in r.value


# ===========================================================================
# analyze_filter — error branches
# ===========================================================================

class TestAnalyzeFilterExtended:
    def test_symbolic_space_returns_unknown(self):
        r = analyze_filter(_SymbolicSpace(), [{1, 2}])
        assert not r.is_true
        assert not r.is_false

    def test_invalid_filter_returns_false(self):
        sp = _discrete(2)
        # empty set → F1 fails → not a valid filter
        r = analyze_filter(sp, [frozenset()])
        assert r.is_false
        assert 'not a valid filter' in r.justification[0].lower()

    def test_valid_with_point_and_coarser(self):
        sp = _discrete(2)
        fam = [frozenset({0}), frozenset({0, 1})]
        coarser = [frozenset({0, 1})]
        r = analyze_filter(sp, fam, point=0, coarser=coarser)
        assert r.is_true
        assert 'converges_to_point' in r.value
        assert 'is_finer_than_coarser' in r.value
        assert r.value['is_finer_than_coarser'].is_true
