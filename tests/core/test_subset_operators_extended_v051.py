"""Coverage-targeted tests for subset_operators.py (v0.5.1)."""
import pytest
from pytop.subset_operators import (
    SubsetOperatorError,
    UnknownFiniteSubsetError,
    UnknownFinitePointError,
    closure_of_subset,
    interior_of_subset,
    boundary_of_subset,
    derived_set_of_subset,
    exterior_of_subset,
    neighborhood_system_of_point,
    is_neighborhood_of_point,
    is_nowhere_dense_subset,
    _space_is_finite,
    _as_finite_subset,
    _as_finite_point,
    _representation_of,
    _exact_subset_operator_result,
)
from pytop.finite_spaces import FiniteTopologicalSpace


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _space(carrier_list, opens_list):
    carrier = frozenset(carrier_list)
    topology = frozenset(frozenset(u) for u in opens_list)
    return FiniteTopologicalSpace(carrier=carrier, topology=topology)


def _discrete2():
    return _space([1, 2], [set(), {1}, {2}, {1, 2}])


def _indiscrete2():
    return _space([1, 2], [set(), {1, 2}])


def _t0_space():
    return _space([1, 2], [set(), {1}, {1, 2}])


# ---------------------------------------------------------------------------
# _space_is_finite — exception branch  (lines 271-272)
# ---------------------------------------------------------------------------

def test_space_is_finite_raises_exception():
    class BadSpace:
        def is_finite(self):
            raise RuntimeError("broken")
    assert _space_is_finite(BadSpace()) is False


def test_space_is_finite_returns_true():
    space = _discrete2()
    assert _space_is_finite(space) is True


def test_space_is_finite_no_method():
    class NoMethod:
        pass
    assert _space_is_finite(NoMethod()) is False


# ---------------------------------------------------------------------------
# _as_finite_subset errors  (lines 279-284)
# ---------------------------------------------------------------------------

def test_as_finite_subset_symbolic_label():
    space = _discrete2()

    class Symbolic:
        label = "A"

    with pytest.raises(UnknownFiniteSubsetError, match="Symbolic"):
        _as_finite_subset(space, Symbolic())


def test_as_finite_subset_unsupported_type():
    space = _discrete2()
    with pytest.raises(UnknownFiniteSubsetError, match="Unsupported"):
        _as_finite_subset(space, 42)  # int is not a set/frozenset/list/tuple


def test_as_finite_subset_outside_carrier():
    space = _discrete2()
    with pytest.raises(UnknownFiniteSubsetError, match="outside the carrier"):
        _as_finite_subset(space, {99})


def test_as_finite_subset_valid():
    space = _discrete2()
    result = _as_finite_subset(space, {1})
    assert result == {1}


# ---------------------------------------------------------------------------
# _as_finite_point error  (line 291)
# ---------------------------------------------------------------------------

def test_as_finite_point_outside_carrier():
    space = _discrete2()
    with pytest.raises(UnknownFinitePointError, match="outside"):
        _as_finite_point(space, 99)


def test_as_finite_point_valid():
    space = _discrete2()
    assert _as_finite_point(space, 1) == 1


# ---------------------------------------------------------------------------
# _representation_of — finite path  (lines 356-358)
# ---------------------------------------------------------------------------

def test_representation_of_finite_space_via_metadata():
    # FiniteTopologicalSpace has metadata["representation"] = "finite" → early return
    space = _discrete2()
    assert _representation_of(space) == "finite"


def test_representation_of_symbolic():
    class Bare:
        pass
    assert _representation_of(Bare()) == "symbolic_general"


def test_representation_of_metadata_path():
    class WithMeta:
        metadata = {"representation": "meta_rep"}
    assert _representation_of(WithMeta()) == "meta_rep"


def test_representation_of_finite_via_topology_attr():
    # No metadata, but has .topology and is_finite() → line 357
    class FiniteLike:
        topology = frozenset([frozenset(), frozenset({1})])
        carrier = frozenset({1})
        def is_finite(self):
            return True
    assert _representation_of(FiniteLike()) == "finite"


# ---------------------------------------------------------------------------
# except clause (lines 95-96): finite space + bad subset → unknown fallthrough
# ---------------------------------------------------------------------------

def test_finite_space_bad_subset_falls_to_unknown():
    # FiniteTopologicalSpace is finite, but subset has points outside carrier
    # → UnknownFiniteSubsetError caught, falls to symbolic unknown
    space = _discrete2()
    r = closure_of_subset(space, frozenset({99, 100}))
    assert r.is_unknown


def test_finite_space_bad_point_falls_to_unknown():
    # point outside carrier → UnknownFinitePointError caught, falls to symbolic unknown
    space = _discrete2()
    r = neighborhood_system_of_point(space, 99)
    assert r.is_unknown


# ---------------------------------------------------------------------------
# Unsupported operator error  (line 167)
# ---------------------------------------------------------------------------

def test_exact_subset_operator_unsupported():
    space = _discrete2()
    finite_data = {
        "carrier": {1, 2},
        "points": (1, 2),
        "opens": [set(), {1}, {2}, {1, 2}],
    }
    with pytest.raises(SubsetOperatorError, match="Unsupported"):
        _exact_subset_operator_result(finite_data, "nonexistent_operator", {1})


# ---------------------------------------------------------------------------
# Symbolic/infinite → unknown result  (lines 95-116)
# Trigger by passing a non-finite space (no topology attr → _space_is_finite=False)
# ---------------------------------------------------------------------------

def test_symbolic_space_returns_unknown_closure():
    class Symbolic:
        def is_finite(self):
            return False
    r = closure_of_subset(Symbolic(), {1})
    assert r.is_unknown


def test_symbolic_space_returns_unknown_neighborhood():
    class Symbolic:
        def is_finite(self):
            return False
    r = neighborhood_system_of_point(Symbolic(), 1)
    assert r.is_unknown


def test_symbolic_space_returns_unknown_interior():
    class Symbolic:
        def is_finite(self):
            return False
    r = interior_of_subset(Symbolic(), {1})
    assert r.is_unknown


def test_symbolic_with_subset_metadata():
    class Symbolic:
        def is_finite(self):
            return False
    r = closure_of_subset(Symbolic(), frozenset({1}))
    assert r.is_unknown
    assert "subset_repr" in r.metadata


def test_symbolic_with_point_metadata():
    class Symbolic:
        def is_finite(self):
            return False
    r = neighborhood_system_of_point(Symbolic(), "p")
    assert r.is_unknown
    assert "point_repr" in r.metadata


# ---------------------------------------------------------------------------
# Exact computations — verify correctness
# ---------------------------------------------------------------------------

def test_closure_indiscrete():
    space = _indiscrete2()
    r = closure_of_subset(space, {1})
    assert r.is_true
    # closure of {1} in indiscrete = {1, 2}
    assert frozenset({1, 2}) == r.value


def test_interior_t0():
    space = _t0_space()
    r = interior_of_subset(space, {1, 2})
    assert r.is_true
    assert frozenset({1, 2}) == r.value


def test_boundary_discrete():
    space = _discrete2()
    r = boundary_of_subset(space, {1})
    assert r.is_true
    # discrete: interior({1})={1}, closure({1})={1} → boundary=∅
    assert frozenset() == r.value


def test_derived_set_discrete():
    space = _discrete2()
    r = derived_set_of_subset(space, {1, 2})
    assert r.is_true
    # discrete: no point is a limit point → derived set = ∅
    assert frozenset() == r.value


def test_exterior_indiscrete():
    space = _indiscrete2()
    r = exterior_of_subset(space, {1})
    assert r.is_true
    # exterior = interior(complement) = interior({2}) = ∅ in indiscrete
    assert frozenset() == r.value


def test_is_nowhere_dense_singleton_discrete():
    space = _discrete2()
    r = is_nowhere_dense_subset(space, {1})
    assert r.is_false  # in discrete, closure({1})={1}, interior({1})={1} ≠ ∅


def test_is_neighborhood_true():
    space = _t0_space()
    r = is_neighborhood_of_point(space, 1, {1})
    assert r.is_true


def test_is_neighborhood_false():
    space = _t0_space()
    # {2} cannot be a neighborhood of 1 (no open set containing 1 is a subset of {2})
    r = is_neighborhood_of_point(space, 1, {2})
    assert r.is_false
