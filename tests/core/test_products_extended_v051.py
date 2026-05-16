"""Coverage-targeted tests for products.py (v0.5.1)."""
import pytest
from pytop.products import product, binary_product, _space_is_finite, _is_open_from_basis
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


def _single():
    return _space([1], [set(), {1}])


def _compact_connected():
    # Indiscrete on {1} — trivially compact and "connected"
    space = _space([1], [set(), {1}])
    space.tags.add("compact")
    space.tags.add("connected")
    return space


# ---------------------------------------------------------------------------
# _space_is_finite — exception path (lines 81-82)
# ---------------------------------------------------------------------------

def test_space_is_finite_exception_returns_false():
    class Bad:
        def is_finite(self):
            raise RuntimeError("broken")
    assert _space_is_finite(Bad()) is False


def test_space_is_finite_no_is_finite_method():
    class Bare:
        pass
    assert _space_is_finite(Bare()) is False


def test_space_is_finite_finite_space():
    assert _space_is_finite(_discrete2()) is True


# ---------------------------------------------------------------------------
# product — infinite fallback (line 21)
# ---------------------------------------------------------------------------

def test_product_non_finite_returns_symbolic():
    from pytop.spaces import TopologicalSpace
    sym = TopologicalSpace.symbolic(description="test")
    result = product(sym, _discrete2())
    # Falls through to infinite_product
    assert result is not None


def test_product_symbolic_only():
    from pytop.spaces import TopologicalSpace
    s1 = TopologicalSpace.symbolic(description="a")
    s2 = TopologicalSpace.symbolic(description="b")
    result = product(s1, s2)
    assert result is not None


# ---------------------------------------------------------------------------
# product — finite exact computation
# ---------------------------------------------------------------------------

def test_product_two_finite_spaces():
    result = product(_single(), _single())
    assert isinstance(result, FiniteTopologicalSpace)
    # |{1}| × |{1}| = 1 point
    assert len(result.carrier) == 1


def test_product_two_discrete_spaces():
    result = product(_discrete2(), _single())
    assert isinstance(result, FiniteTopologicalSpace)
    # {1,2} × {1} = 2 points
    assert len(result.carrier) == 2


def test_binary_product_same_as_product():
    r1 = product(_single(), _single())
    r2 = binary_product(_single(), _single())
    assert len(r1.carrier) == len(r2.carrier)


# ---------------------------------------------------------------------------
# tag propagation — connected (line 43) and compact (line 45)
# ---------------------------------------------------------------------------

def test_product_connected_tag_propagated():
    s1 = _compact_connected()
    s2 = _compact_connected()
    result = product(s1, s2)
    assert isinstance(result, FiniteTopologicalSpace)
    assert "connected" in result.tags


def test_product_compact_tag_propagated():
    s1 = _compact_connected()
    s2 = _compact_connected()
    result = product(s1, s2)
    assert "compact" in result.tags


def test_product_no_compact_tag_when_one_missing():
    s1 = _compact_connected()  # has compact
    s2 = _discrete2()          # no compact tag
    result = product(s1, s2)
    assert "compact" not in result.tags


# ---------------------------------------------------------------------------
# _is_open_from_basis — True return path (line 74)
# ---------------------------------------------------------------------------

def test_product_discrete_product_topology_complete():
    # Discrete × Discrete: every subset should be open
    result = product(_discrete2(), _discrete2())
    assert isinstance(result, FiniteTopologicalSpace)
    # Discrete product of two discrete spaces is discrete — all 16 subsets open
    carrier_size = len(result.carrier)
    assert carrier_size == 4  # 2×2


def test_product_single_single_has_full_open():
    result = product(_single(), _single())
    # {(1,1)} should be open in discrete product
    assert isinstance(result, FiniteTopologicalSpace)
    topo_sets = {frozenset(u) for u in result.topology}
    full = frozenset(result.carrier)
    assert full in topo_sets


# ---------------------------------------------------------------------------
# _is_open_from_basis — True return path (line 74) — direct call
# ---------------------------------------------------------------------------

def test_is_open_from_basis_nonempty_open_returns_true():
    # Non-empty subset where every point has a covering basis element
    basis = [set(), {(1, 1)}, {(1, 2)}, {(1, 1), (1, 2)}]
    subset = {(1, 1), (1, 2)}
    assert _is_open_from_basis(subset, basis) is True


def test_is_open_from_basis_empty_returns_true():
    assert _is_open_from_basis(set(), []) is True


def test_is_open_from_basis_not_open_returns_false():
    basis = [{(1,)}]
    # (2,) is in subset but no basis element covers (2,)
    assert _is_open_from_basis({(1,), (2,)}, basis) is False


# ---------------------------------------------------------------------------
# product with metadata
# ---------------------------------------------------------------------------

def test_product_with_metadata():
    result = product(_single(), _single(), metadata={"description": "test product"})
    assert isinstance(result, FiniteTopologicalSpace)
    assert result.metadata.get("description") == "test product"
