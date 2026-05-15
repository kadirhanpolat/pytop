"""Tests for finite_operator_engine.py."""

import pytest
from pytop.finite_operator_engine import (
    FiniteOperatorEngineError,
    FiniteOperatorTable,
    TopologyValidation,
    boundary,
    closed_sets_from_topology,
    closure,
    derived_set,
    exterior,
    interior,
    is_topology,
    kuratowski_closure_check,
    neighborhood_system,
    operator_table,
    relative_topology,
    validate_topology_candidate,
)

# ---------------------------------------------------------------------------
# Test fixtures
# ---------------------------------------------------------------------------

X3 = [1, 2, 3]

# Discrete topology on {1,2,3}
DISCRETE = [set(), {1}, {2}, {3}, {1,2}, {1,3}, {2,3}, {1,2,3}]

# Indiscrete topology on {1,2,3}
INDISCRETE = [set(), {1,2,3}]

# Sierpinski-like: {∅, {1}, {1,2}, X}
SIER = [set(), {1}, {1,2}, {1,2,3}]

# Not a topology — missing {1,2} from union {1}∪{2}
NOT_TOP = [set(), {1}, {2}, {1,2,3}]


# ---------------------------------------------------------------------------
# validate_topology_candidate
# ---------------------------------------------------------------------------

class TestValidateTopologyCandidate:
    def test_discrete_is_topology(self):
        v = validate_topology_candidate(X3, DISCRETE)
        assert v.is_topology

    def test_indiscrete_is_topology(self):
        v = validate_topology_candidate(X3, INDISCRETE)
        assert v.is_topology

    def test_sierpinski_like_is_topology(self):
        v = validate_topology_candidate(X3, SIER)
        assert v.is_topology

    def test_missing_union_detected(self):
        v = validate_topology_candidate(X3, NOT_TOP)
        assert not v.is_topology
        assert v.failure_count > 0

    def test_missing_empty_set_detected(self):
        v = validate_topology_candidate(X3, [{1,2,3}])
        assert not v.is_topology
        assert frozenset() in v.missing_required

    def test_missing_whole_set_detected(self):
        v = validate_topology_candidate(X3, [set()])
        assert not v.is_topology
        assert frozenset({1,2,3}) in v.missing_required

    def test_non_subset_member_detected(self):
        v = validate_topology_candidate([1, 2], [set(), {1,2}, {1,2,3}])
        assert not v.is_topology
        assert len(v.non_subset_members) > 0

    def test_as_dict_keys(self):
        v = validate_topology_candidate(X3, DISCRETE)
        d = v.as_dict()
        for key in ("carrier","opens","is_topology","missing_required",
                    "non_subset_members","union_failures","intersection_failures","failure_count"):
            assert key in d

    def test_carrier_is_frozenset(self):
        v = validate_topology_candidate(X3, DISCRETE)
        assert isinstance(v.carrier, frozenset)


# ---------------------------------------------------------------------------
# is_topology
# ---------------------------------------------------------------------------

class TestIsTopology:
    def test_discrete_true(self):
        assert is_topology(X3, DISCRETE)

    def test_indiscrete_true(self):
        assert is_topology(X3, INDISCRETE)

    def test_not_topology_false(self):
        assert not is_topology(X3, NOT_TOP)


# ---------------------------------------------------------------------------
# closed_sets_from_topology
# ---------------------------------------------------------------------------

class TestClosedSets:
    def test_discrete_has_eight_closed_sets(self):
        closed = closed_sets_from_topology(X3, DISCRETE)
        assert len(closed) == 8

    def test_indiscrete_closed_sets(self):
        closed = closed_sets_from_topology(X3, INDISCRETE)
        assert frozenset() in closed
        assert frozenset(X3) in closed

    def test_sierpinski_closed_sets(self):
        closed = closed_sets_from_topology(X3, SIER)
        assert frozenset() in closed
        assert frozenset(X3) in closed


# ---------------------------------------------------------------------------
# closure
# ---------------------------------------------------------------------------

class TestClosure:
    def test_closure_of_empty_is_empty_in_discrete(self):
        assert closure(X3, DISCRETE, []) == frozenset()

    def test_closure_of_singleton_in_discrete(self):
        assert closure(X3, DISCRETE, [1]) == frozenset({1})

    def test_closure_of_whole_space(self):
        assert closure(X3, DISCRETE, X3) == frozenset(X3)

    def test_closure_in_indiscrete(self):
        # Any non-empty subset has closure = whole space
        assert closure(X3, INDISCRETE, [1]) == frozenset(X3)

    def test_closure_contains_subset(self):
        sub = [1, 2]
        cl = closure(X3, SIER, sub)
        assert frozenset(sub).issubset(cl)

    def test_invalid_topology_raises(self):
        with pytest.raises(FiniteOperatorEngineError):
            closure(X3, NOT_TOP, [1])


# ---------------------------------------------------------------------------
# interior
# ---------------------------------------------------------------------------

class TestInterior:
    def test_interior_of_open_set_is_itself(self):
        assert interior(X3, SIER, [1]) == frozenset({1})

    def test_interior_of_closed_non_open(self):
        # {2,3} is closed in SIER (complement of {1}) but not open
        assert interior(X3, SIER, [2, 3]) == frozenset()

    def test_interior_of_whole_space(self):
        assert interior(X3, SIER, X3) == frozenset(X3)

    def test_interior_of_empty(self):
        assert interior(X3, SIER, []) == frozenset()


# ---------------------------------------------------------------------------
# exterior / boundary
# ---------------------------------------------------------------------------

class TestExteriorBoundary:
    def test_exterior_of_open_set(self):
        # exterior of {1} in SIER = interior of {2,3} = ∅
        assert exterior(X3, SIER, [1]) == frozenset()

    def test_boundary_of_open_set(self):
        # SIER closed sets: X, {2,3}, {3}, ∅ — closure of {1} is X, interior is {1} → boundary = {2,3}
        assert boundary(X3, SIER, [1]) == frozenset({2, 3})

    def test_boundary_of_non_open_set(self):
        # {2} in SIER: cl(X3)=X3, int(∅)=∅ → boundary = X3
        b = boundary(X3, SIER, [2])
        assert frozenset({2}).issubset(b)

    def test_exterior_complement_of_closure(self):
        # exterior(A) = interior(X - A)
        a = [1]
        ext = exterior(X3, SIER, a)
        complement = frozenset(X3) - frozenset(a)
        int_c = interior(X3, SIER, complement)
        assert ext == int_c


# ---------------------------------------------------------------------------
# derived_set
# ---------------------------------------------------------------------------

class TestDerivedSet:
    def test_derived_set_of_empty(self):
        d = derived_set(X3, DISCRETE, [])
        assert d == frozenset()

    def test_derived_set_discrete_singleton(self):
        # In discrete topology every point is isolated → derived set = ∅
        d = derived_set(X3, DISCRETE, [1])
        assert d == frozenset()

    def test_derived_set_indiscrete(self):
        # In indiscrete: every point of X3 is a limit point of any nonempty set
        d = derived_set(X3, INDISCRETE, [1])
        assert frozenset({2, 3}).issubset(d)


# ---------------------------------------------------------------------------
# neighborhood_system
# ---------------------------------------------------------------------------

class TestNeighborhoodSystem:
    def test_discrete_point_neighborhoods(self):
        nbhds = neighborhood_system(X3, DISCRETE, 1)
        # Every superset of {1} is a neighborhood
        assert frozenset({1}) in nbhds
        assert frozenset(X3) in nbhds

    def test_indiscrete_point_neighborhoods(self):
        nbhds = neighborhood_system(X3, INDISCRETE, 1)
        # Only whole space is a neighbourhood (only open set containing 1)
        assert frozenset(X3) in nbhds

    def test_point_not_in_carrier_raises(self):
        with pytest.raises(FiniteOperatorEngineError):
            neighborhood_system(X3, DISCRETE, 99)


# ---------------------------------------------------------------------------
# relative_topology
# ---------------------------------------------------------------------------

class TestRelativeTopology:
    def test_relative_topology_on_subspace(self):
        # subspace {1,2} with SIER restricted
        rel = relative_topology(X3, SIER, [1, 2])
        # SIER = {∅,{1},{1,2},{1,2,3}} → intersect with {1,2}: ∅,{1},{1,2},{1,2}
        assert frozenset({1}) in rel
        assert frozenset({1,2}) in rel

    def test_relative_discrete_on_whole_space(self):
        rel = relative_topology(X3, DISCRETE, X3)
        assert len(rel) == len(set(frozenset(s) for s in DISCRETE))


# ---------------------------------------------------------------------------
# kuratowski_closure_check
# ---------------------------------------------------------------------------

class TestKuratowskiClosureCheck:
    def test_discrete_satisfies_all_axioms(self):
        result = kuratowski_closure_check(X3, DISCRETE)
        assert result["all"] is True
        assert result["empty"] is True
        assert result["extensive"] is True
        assert result["idempotent"] is True
        assert result["finite_union"] is True

    def test_indiscrete_satisfies_all_axioms(self):
        result = kuratowski_closure_check(X3, INDISCRETE)
        assert result["all"] is True


# ---------------------------------------------------------------------------
# operator_table
# ---------------------------------------------------------------------------

class TestOperatorTable:
    def test_table_is_finite_operator_table(self):
        t = operator_table(X3, SIER, [1])
        assert isinstance(t, FiniteOperatorTable)

    def test_table_closure_contains_subset(self):
        t = operator_table(X3, SIER, [1])
        assert frozenset({1}).issubset(t.closure)

    def test_table_interior_subset_of_closure(self):
        t = operator_table(X3, SIER, [1, 2])
        assert t.interior.issubset(t.closure)

    def test_table_as_dict_keys(self):
        t = operator_table(X3, SIER, [1])
        d = t.as_dict()
        for key in ("carrier","subset","closure","interior","exterior",
                    "boundary","derived_set","closed_sets"):
            assert key in d

    def test_table_boundary_eq_closure_minus_interior(self):
        t = operator_table(X3, SIER, [1, 2])
        assert t.boundary == t.closure - t.interior


# ---------------------------------------------------------------------------
# Error paths
# ---------------------------------------------------------------------------

class TestErrorPaths:
    def test_string_carrier_raises(self):
        with pytest.raises(FiniteOperatorEngineError):
            validate_topology_candidate("abc", [])

    def test_none_carrier_raises(self):
        with pytest.raises(FiniteOperatorEngineError):
            validate_topology_candidate(None, [])
