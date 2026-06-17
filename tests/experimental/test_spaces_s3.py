"""Milestone S3 — the property-reasoning engine over constructed spaces."""

from __future__ import annotations

from pytop.experimental.spaces import (
    CarrierKind,
    CofiniteSpace,
    Decidability,
    FiniteSpace,
    OrderTopologySpace,
    ProductSpace,
    QuotientSpace,
    Space,
    SubspaceSpace,
    SumSpace,
    Verdict,
    derive,
    discrete_finite_space,
    explain,
    rational_metric_space,
    synthesize,
)
from pytop.experimental.spaces.reasoning import _pi_base_closure

DISCRETE2 = discrete_finite_space({0, 1}, name="discrete2")
DISCRETE3 = discrete_finite_space({0, 1, 2}, name="discrete3")
SIERPINSKI = FiniteSpace("Sierpinski", {0, 1}, [set(), {0}, {0, 1}])


# --------------------------------------------------------------------------
# Infinite construction closure via preservation (no enumeration)
# --------------------------------------------------------------------------

def test_infinite_product_is_t1_via_productivity():
    space = ProductSpace([CofiniteSpace(), OrderTopologySpace()])
    d = derive(space, "T1")
    assert d.verdict.value is True
    assert "preserved by product" in d.rule


def test_infinite_product_is_compact_via_tychonoff():
    space = ProductSpace([CofiniteSpace(), CofiniteSpace()])
    assert derive(space, "compact").verdict.value is True


def test_subspace_of_infinite_metric_is_regular_hereditarily():
    space = SubspaceSpace(rational_metric_space(), member=lambda p: True)
    d = derive(space, "regular")
    assert d.verdict.value is True
    assert "subspace" in d.rule


# --------------------------------------------------------------------------
# Structural and undecidable verdicts
# --------------------------------------------------------------------------

def test_sum_is_structurally_disconnected():
    space = SumSpace([DISCRETE2, DISCRETE2])
    d = derive(space, "connected")
    assert d.verdict.value is False
    assert "disconnected" in d.rule


def test_quotient_preserves_compact_but_not_hausdorff():
    space = QuotientSpace(DISCRETE3)
    assert derive(space, "compact").verdict.value is True       # continuous image of compact
    assert derive(space, "T2").verdict.decidability is Decidability.UNDECIDABLE


# --------------------------------------------------------------------------
# pi-Base implication closure inside the engine
# --------------------------------------------------------------------------

def test_pi_base_closure_function():
    closed = _pi_base_closure({"T2"})
    assert {"T0", "T1", "T2"} <= closed


def test_implication_path_from_only_t2_certificate():
    class OnlyT2(Space):
        name = "onlyT2"
        carrier_kind = CarrierKind.COUNTABLE

        def contains(self, point):
            return True

        def certificate(self, prop):
            return Verdict.true(reason="declared T2") if prop == "T2" else None

    space = OnlyT2()
    # T1 and T0 are not certified directly, but follow from T2 via pi-Base
    assert derive(space, "T1").verdict.value is True
    assert derive(space, "T0").verdict.value is True
    assert "pi-Base" in derive(space, "T1").rule


# --------------------------------------------------------------------------
# Explanations
# --------------------------------------------------------------------------

def test_explain_returns_a_derivation_tree():
    text = explain(ProductSpace([DISCRETE2, DISCRETE2]), "T2")
    assert "preserved by product" in text
    assert text.count("\n") >= 2  # root + per-factor sub-derivations


# --------------------------------------------------------------------------
# Counterexample synthesis
# --------------------------------------------------------------------------

def test_synthesize_connected_non_hausdorff():
    space = synthesize(has=["connected"], lacks=["T2"])
    assert space is not None
    assert derive(space, "connected").verdict.value is True
    assert derive(space, "T2").verdict.value is False


def test_synthesize_hausdorff_disconnected():
    space = synthesize(has=["T2"], lacks=["connected"])
    assert space is not None
    assert derive(space, "T2").verdict.value is True
    assert derive(space, "connected").verdict.value is False
