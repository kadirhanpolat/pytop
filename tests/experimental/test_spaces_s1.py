"""Milestone S1 — the computable-space protocol, end to end via is_hausdorff."""

from __future__ import annotations

from fractions import Fraction

from pytop.experimental.spaces import (
    CofiniteSpace,
    Decidability,
    FiniteSpace,
    OpaqueInfiniteSpace,
    OrderTopologySpace,
    Verdict,
    discrete_finite_space,
    is_hausdorff,
    rational_metric_space,
)


# --------------------------------------------------------------------------
# Verdict semantics
# --------------------------------------------------------------------------

def test_verdict_bool_and_decidability():
    assert bool(Verdict.true("ok")) is True
    assert bool(Verdict.false("no")) is False
    assert bool(Verdict.undecidable("dunno")) is False  # undecided is not truthy
    assert Verdict.true().is_decided is True
    assert Verdict.undecidable().is_decided is False


# --------------------------------------------------------------------------
# Finite spaces — decided by computation, with witness / counterexample
# --------------------------------------------------------------------------

def test_finite_sierpinski_not_hausdorff():
    sierpinski = FiniteSpace("Sierpinski", {0, 1}, [set(), {0}, {0, 1}])
    v = is_hausdorff(sierpinski)
    assert v.value is False
    assert v.decidability is Decidability.DECIDED
    assert v.counterexample == (0, 1)


def test_finite_discrete_is_hausdorff():
    v = is_hausdorff(discrete_finite_space({0, 1, 2}))
    assert v.value is True
    assert v.decidability is Decidability.DECIDED
    assert v.witness["pairs_separated"] == 3


def test_finite_indiscrete_not_hausdorff():
    indiscrete = FiniteSpace("indiscrete", {0, 1}, [set(), {0, 1}])
    v = is_hausdorff(indiscrete)
    assert v.value is False and v.decidability is Decidability.DECIDED


# --------------------------------------------------------------------------
# Infinite spaces — decided via construction certificates
# --------------------------------------------------------------------------

def test_cofinite_infinite_not_hausdorff():
    v = is_hausdorff(CofiniteSpace())
    assert v.value is False
    assert v.decidability is Decidability.DECIDED
    assert "cofinite" in v.reason.lower()


def test_cofinite_is_t1_certificate():
    v = CofiniteSpace().separation_certificate("T1")
    assert v.value is True
    assert CofiniteSpace().separation_certificate("T2").value is False


def test_order_topology_is_hausdorff():
    v = is_hausdorff(OrderTopologySpace())
    assert v.value is True and v.decidability is Decidability.DECIDED


def test_metric_space_is_hausdorff():
    v = is_hausdorff(rational_metric_space())
    assert v.value is True and v.decidability is Decidability.DECIDED


# --------------------------------------------------------------------------
# Honest undecidability for an opaque infinite space
# --------------------------------------------------------------------------

def test_opaque_infinite_is_undecidable():
    opaque = OpaqueInfiniteSpace("opaque", member=lambda p: isinstance(p, int))
    v = is_hausdorff(opaque)
    assert v.value is None
    assert v.decidability is Decidability.UNDECIDABLE


# --------------------------------------------------------------------------
# Representations produce real separation witnesses
# --------------------------------------------------------------------------

def test_metric_point_separation_witness():
    v = rational_metric_space().point_separation(Fraction(0), Fraction(1))
    assert v.value is True
    (cx, r1), (cy, r2) = v.witness
    assert r1 == r2 == Fraction(1, 2)  # balls of radius d/2


def test_order_point_separation_splits_at_midpoint():
    v = OrderTopologySpace().point_separation(Fraction(0), Fraction(2))
    assert v.value is True
    assert v.witness == (("ray_below", Fraction(1)), ("ray_above", Fraction(1)))


def test_finite_point_separation_returns_disjoint_opens():
    space = discrete_finite_space({0, 1})
    v = space.point_separation(0, 1)
    assert v.value is True
    u, w = v.witness
    assert 0 in u and 1 in w and not (u & w)
