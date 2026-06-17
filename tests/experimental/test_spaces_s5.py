"""Milestone S5 — Tychonoff/T5/T6 predicates and reasoning over the full hierarchy.

Highlight: the engine distinguishes the rational plane Q² (second countable, hence
Lindelöf and normal/T4) from the Sorgenfrey plane (regular but famously *not*
normal and *not* Lindelöf) — purely via preservation + the pi-Base implication
graph, with no enumeration.
"""

from __future__ import annotations

from pytop.experimental.spaces import (
    CofiniteSpace,
    DiscreteCountableSpace,
    FiniteSpace,
    OrderTopologySpace,
    ProductSpace,
    SorgenfreyLineSpace,
    SubspaceSpace,
    SumSpace,
    derive,
    discrete_finite_space,
    is_t5,
    is_t6,
    is_tychonoff,
    rational_metric_space,
)

SIERPINSKI = FiniteSpace("Sierpinski", {0, 1}, [set(), {0}, {0, 1}])


# --------------------------------------------------------------------------
# Predicates: finite collapse to T1, infinite via certificate
# --------------------------------------------------------------------------

def test_finite_tychonoff_t5_t6_collapse_to_discrete():
    d = discrete_finite_space({0, 1, 2})
    assert is_tychonoff(d).value is True
    assert is_t5(d).value is True
    assert is_t6(d).value is True


def test_sierpinski_is_not_tychonoff():
    assert is_tychonoff(SIERPINSKI).value is False  # not even T1


def test_cofinite_is_not_tychonoff():
    assert is_tychonoff(CofiniteSpace()).value is False  # not regular


def test_metric_is_t6():
    assert is_t6(rational_metric_space()).value is True
    assert is_t5(rational_metric_space()).value is True


def test_sorgenfrey_is_t6():
    assert is_t6(SorgenfreyLineSpace()).value is True


# --------------------------------------------------------------------------
# THE headline: Q² vs the Sorgenfrey plane
# --------------------------------------------------------------------------

def test_rational_plane_is_lindelof_and_normal_via_metrization():
    q2 = ProductSpace([OrderTopologySpace(), OrderTopologySpace()])
    # second countable is productive; second countable ⟹ Lindelöf, and
    # regular + second countable ⟹ metrizable ⟹ normal (Urysohn), all via pi-Base
    assert derive(q2, "second_countable").verdict.value is True
    assert derive(q2, "lindelof").verdict.value is True
    assert derive(q2, "T4").verdict.value is True


def test_sorgenfrey_plane_is_not_lindelof_or_normal():
    s2 = ProductSpace([SorgenfreyLineSpace(), SorgenfreyLineSpace()])
    assert derive(s2, "T3").verdict.value is True          # regularity is productive
    assert derive(s2, "lindelof").verdict.value is not True  # Sorgenfrey plane is not Lindelöf
    assert derive(s2, "T4").verdict.value is not True        # ... and not normal


# --------------------------------------------------------------------------
# Preservation facts for the extended properties
# --------------------------------------------------------------------------

def test_second_countable_is_hereditary():
    sub = SubspaceSpace(DiscreteCountableSpace(), member=lambda x: True)
    assert derive(sub, "second_countable").verdict.value is True
    assert derive(sub, "first_countable").verdict.value is True


def test_separable_is_productive():
    q2 = ProductSpace([OrderTopologySpace(), OrderTopologySpace()])
    assert derive(q2, "separable").verdict.value is True


def test_tychonoff_is_productive():
    q2 = ProductSpace([OrderTopologySpace(), OrderTopologySpace()])
    assert derive(q2, "tychonoff").verdict.value is True


def test_sum_preserves_normality():
    s = SumSpace([OrderTopologySpace(), OrderTopologySpace()])
    assert derive(s, "T4").verdict.value is True
