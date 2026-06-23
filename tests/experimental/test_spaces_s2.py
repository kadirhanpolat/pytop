"""Milestone S2 — extended witness predicates and finite construction closure."""

from __future__ import annotations

from pytop.experimental.spaces import (
    CofiniteSpace,
    Decidability,
    FiniteSpace,
    OpaqueInfiniteSpace,
    OrderTopologySpace,
    binary_product,
    discrete_finite_space,
    disjoint_sum,
    is_compact,
    is_connected,
    is_hausdorff,
    is_normal,
    is_regular,
    is_t0,
    is_t1,
    quotient,
    rational_metric_space,
    subspace,
)

SIERPINSKI = FiniteSpace("Sierpinski", {0, 1}, [set(), {0}, {0, 1}])
INDISCRETE2 = FiniteSpace("indiscrete2", {0, 1}, [set(), {0, 1}])


# --------------------------------------------------------------------------
# Extended predicates on finite spaces (computed)
# --------------------------------------------------------------------------

def test_discrete_separation_axioms():
    d = discrete_finite_space({0, 1, 2})
    assert is_t0(d).value is True
    assert is_t1(d).value is True
    assert is_hausdorff(d).value is True
    assert is_regular(d).value is True
    assert is_normal(d).value is True
    assert is_compact(d).value is True
    assert is_connected(d).value is False  # discrete with >1 point is disconnected


def test_sierpinski_axioms():
    assert is_t0(SIERPINSKI).value is True
    assert is_t1(SIERPINSKI).value is False   # {0} is not closed
    assert is_hausdorff(SIERPINSKI).value is False
    assert is_connected(SIERPINSKI).value is True   # only trivial clopen sets
    assert is_compact(SIERPINSKI).value is True


def test_indiscrete_is_not_t0():
    v = is_t0(INDISCRETE2)
    assert v.value is False and v.counterexample == (0, 1)


def test_t1_counterexample_is_a_point():
    v = is_t1(SIERPINSKI)
    assert v.value is False and v.counterexample == 0


# --------------------------------------------------------------------------
# Extended predicates on infinite spaces (certificates) — honest decidability
# --------------------------------------------------------------------------

def test_cofinite_axioms():
    c = CofiniteSpace()
    assert is_t1(c).value is True
    assert is_hausdorff(c).value is False
    assert is_compact(c).value is True
    assert is_connected(c).value is True
    assert is_regular(c).value is False
    assert is_normal(c).value is False


def test_order_topology_axioms():
    q = OrderTopologySpace()
    assert is_hausdorff(q).value is True
    assert is_regular(q).value is True
    assert is_normal(q).value is True
    assert is_compact(q).value is False     # Q is not compact
    assert is_connected(q).value is False   # Q is totally disconnected


def test_metric_compactness_is_undecidable_generically():
    # "being metric" does not determine compactness/connectedness -> honest undecidable
    m = rational_metric_space()
    assert is_normal(m).value is True
    assert is_compact(m).decidability is Decidability.UNDECIDABLE
    assert is_connected(m).decidability is Decidability.UNDECIDABLE


def test_opaque_space_all_undecidable():
    o = OpaqueInfiniteSpace("opaque", member=lambda p: True)
    for predicate in (is_t0, is_t1, is_regular, is_normal, is_compact, is_connected):
        assert predicate(o).decidability is Decidability.UNDECIDABLE


# --------------------------------------------------------------------------
# Construction closure — predicates compose on constructed spaces
# --------------------------------------------------------------------------

def test_subspace_of_discrete_is_discrete():
    s = subspace(discrete_finite_space({0, 1, 2}), {0, 1})
    assert len(list(s.points())) == 2
    assert is_hausdorff(s).value is True


def test_product_of_hausdorff_is_hausdorff():
    p = binary_product(discrete_finite_space({0, 1}), discrete_finite_space({0, 1}))
    assert len(list(p.points())) == 4
    assert is_hausdorff(p).value is True
    assert is_compact(p).value is True


def test_product_of_non_hausdorff_is_non_hausdorff():
    p = binary_product(SIERPINSKI, SIERPINSKI)
    assert is_hausdorff(p).value is False
    assert is_t0(p).value is True   # T0 is productive and Sierpinski is T0


def test_disjoint_sum_is_disconnected():
    s = disjoint_sum(discrete_finite_space({0}), discrete_finite_space({0}))
    assert len(list(s.points())) == 2
    assert is_connected(s).value is False


def test_quotient_to_single_point():
    q = quotient(discrete_finite_space({0, 1}), [{0, 1}])
    assert len(list(q.points())) == 1
    assert is_connected(q).value is True
    assert is_compact(q).value is True


def test_quotient_validates_partition():
    import pytest

    with pytest.raises(ValueError):
        quotient(discrete_finite_space({0, 1, 2}), [{0, 1}])  # does not cover 2
