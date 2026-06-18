"""Incremental Phase 1/2 improvements — round 2:
  - AlexandroffSpace.certificate (T0 antisymmetry, connectedness)
  - AlexandroffSpace.cardinal_certificate (weight, character)
  - Urysohn witnesses for SorgenfreyLine and OrderTopology
  - _decide certificate-first dispatch
"""

from __future__ import annotations

import pytest

from pytop.experimental.spaces import (
    AlexandroffSpace,
    CofiniteSpace,
    OrderTopologySpace,
    SorgenfreyLineSpace,
    discrete_finite_space,
    is_connected,
    is_t0,
)
from pytop.experimental.spaces.cardinal_invariants import character, weight
from pytop.experimental.spaces.urysohn import UrysohnWitness, urysohn_function


# ==========================================================================
# AlexandroffSpace.certificate — T0
# ==========================================================================

class TestAlexandroffT0Certificate:
    def test_partial_order_is_t0(self):
        # Diamond: strict partial order → T0
        diamond = AlexandroffSpace("S^1", {0, 1, 2, 3}, [(0, 2), (0, 3), (1, 2), (1, 3)])
        v = is_t0(diamond)
        assert v.value is True
        # Certificate should mention antisymmetry (structural reason, not enumeration)
        assert "antisymmetric" in v.reason.lower() or "AlexandroffSpace" in v.reason

    def test_t0_certificate_has_witness(self):
        chain = AlexandroffSpace("chain3", {0, 1, 2}, [(0, 1), (1, 2)])
        v = is_t0(chain)
        assert v.value is True
        assert v.witness is not None

    def test_non_t0_detected_via_antisymmetry(self):
        # Preorder with x≤y AND y≤x for x≠y: not a partial order → not T0
        # Give both (0,1) and (1,0) as cover relations
        non_t0 = AlexandroffSpace("non_t0", {0, 1, 2}, [(0, 1), (1, 0)])
        v = is_t0(non_t0)
        assert v.value is False
        # Counterexample should be the two equivalent points
        assert v.counterexample is not None

    def test_indiscrete_non_t0(self):
        # Only reflexive pairs → no strict comparisons → antisymmetric trivially
        # BUT the indiscrete topology on {0,1} has open sets {∅,{0,1}} → not T0
        # An AlexandroffSpace with empty order (besides reflexive): topology = {∅, X}
        # The order is trivially antisymmetric (only reflexive pairs), so this should
        # RETURN T0=True... but the indiscrete topology is NOT T0.
        # This is because the test is: does AlexandroffSpace with empty order give T0?
        # Answer: empty order ≠ indiscrete. With empty strict order, every set is trivially
        # an upset only if the condition "a in sub → b in sub for all (a,b) in order" is
        # vacuously satisfied (no non-reflexive pairs). So EVERY subset is an upset.
        # That gives the discrete topology, which IS T0.
        # Wait: the AlexandroffSpace with no strict order relations:
        #   - Only reflexive pairs (x,x) in the preorder
        #   - Upper sets: sets U where (x∈U and x≤y) → y∈U
        #   - Only reflexive pairs, so x≤y iff x=y
        #   - U is an upset iff (x∈U and x=y) → y∈U, trivially satisfied
        #   - ALL subsets are upsets → discrete topology
        # So AlexandroffSpace with empty order = discrete → T0 ✓
        empty_order = AlexandroffSpace("discrete_2", {0, 1}, [])
        v = is_t0(empty_order)
        assert v.value is True

    def test_direct_certificate_call(self):
        chain = AlexandroffSpace("chain2", {0, 1}, [(0, 1)])
        cert = chain.certificate("T0")
        assert cert is not None
        assert cert.value is True

    def test_non_t0_direct_certificate(self):
        # Cyclic preorder: 0≤1 and 1≤0
        cyclic = AlexandroffSpace("cyclic", {0, 1}, [(0, 1), (1, 0)])
        cert = cyclic.certificate("T0")
        assert cert is not None
        assert cert.value is False
        assert cert.counterexample is not None


# ==========================================================================
# AlexandroffSpace.certificate — connected
# ==========================================================================

class TestAlexandroffConnectedCertificate:
    def test_chain_is_connected(self):
        chain = AlexandroffSpace("chain3", {0, 1, 2}, [(0, 1), (1, 2)])
        v = is_connected(chain)
        assert v.value is True
        assert "AlexandroffSpace" in v.reason or "connected" in v.reason.lower()

    def test_diamond_is_connected(self):
        diamond = AlexandroffSpace("S^1", {0, 1, 2, 3}, [(0, 2), (0, 3), (1, 2), (1, 3)])
        v = is_connected(diamond)
        assert v.value is True

    def test_discrete_two_points_disconnected(self):
        # No order relations → each point is isolated
        discrete = AlexandroffSpace("disc", {0, 1}, [])
        v = is_connected(discrete)
        # Discrete 2-point space is disconnected
        assert v.value is False

    def test_single_point_connected(self):
        pt = AlexandroffSpace("pt", {0}, [])
        v = is_connected(pt)
        assert v.value is True

    def test_direct_certificate_connected(self):
        chain = AlexandroffSpace("chain2", {0, 1}, [(0, 1)])
        cert = chain.certificate("connected")
        assert cert is not None
        assert cert.value is True

    def test_direct_certificate_disconnected(self):
        discrete = AlexandroffSpace("disc", {0, 1}, [])
        cert = discrete.certificate("connected")
        assert cert is not None
        assert cert.value is False


# ==========================================================================
# AlexandroffSpace.cardinal_certificate
# ==========================================================================

class TestAlexandroffCardinalCertificate:
    def test_character_is_1(self):
        # Principal upset ↑x is the minimal open neighborhood → character = 1
        diamond = AlexandroffSpace("S^1", {0, 1, 2, 3}, [(0, 2), (0, 3), (1, 2), (1, 3)])
        cert = diamond.cardinal_certificate("character")
        assert cert is not None
        assert cert.finite == 1

    def test_character_via_cardinal_function(self):
        chain = AlexandroffSpace("chain3", {0, 1, 2}, [(0, 1), (1, 2)])
        cv = character(chain)
        assert cv.finite == 1

    def test_weight_t0_space(self):
        # T0 AlexandroffSpace (partial order) → weight = |X|
        chain = AlexandroffSpace("chain4", {0, 1, 2, 3}, [(0, 1), (1, 2), (2, 3)])
        cert = chain.cardinal_certificate("weight")
        assert cert is not None
        assert cert.finite == 4

    def test_weight_via_cardinal_function(self):
        chain = AlexandroffSpace("chain3", {0, 1, 2}, [(0, 1), (1, 2)])
        cv = weight(chain)
        # character=1, so weight via minimal base should be 3 (or computed from opens)
        assert cv.finite is not None

    def test_non_t0_weight_not_certified(self):
        # Non-T0 space: weight certificate returns None (module computes it)
        non_t0 = AlexandroffSpace("non_t0", {0, 1}, [(0, 1), (1, 0)])
        cert = non_t0.cardinal_certificate("weight")
        assert cert is None  # honest: let the module enumerate

    def test_certificate_unknown_invariant(self):
        s = AlexandroffSpace("S^1", {0, 1, 2, 3}, [(0, 2), (0, 3), (1, 2), (1, 3)])
        assert s.cardinal_certificate("cellularity") is None
        assert s.cardinal_certificate("density") is None


# ==========================================================================
# Urysohn for SorgenfreyLineSpace
# ==========================================================================

class TestUrysohnSorgenfrey:
    def test_returns_witness(self):
        s = SorgenfreyLineSpace()
        w = urysohn_function(s, 0, frozenset())
        assert w is not None
        assert isinstance(w, UrysohnWitness)

    def test_method_is_sorgenfrey(self):
        s = SorgenfreyLineSpace()
        w = urysohn_function(s, 0, frozenset())
        assert w is not None
        assert "sorgenfrey" in w.method.lower()

    def test_formula_references_euclidean(self):
        s = SorgenfreyLineSpace()
        w = urysohn_function(s, 1, frozenset())
        assert w is not None
        assert "d" in w.formula.lower() or "distance" in w.formula.lower() or "min" in w.formula.lower()

    def test_values_none_infinite_space(self):
        s = SorgenfreyLineSpace()
        w = urysohn_function(s, 0, frozenset())
        assert w is not None
        assert w.values is None

    def test_evaluate_returns_none(self):
        s = SorgenfreyLineSpace()
        w = urysohn_function(s, 0, frozenset())
        assert w is not None
        assert w.evaluate(42) is None  # infinite space has no explicit values


# ==========================================================================
# Urysohn for OrderTopologySpace
# ==========================================================================

class TestUrysohnOrderTopology:
    def test_returns_witness(self):
        o = OrderTopologySpace()
        w = urysohn_function(o, 0, frozenset())
        assert w is not None
        assert isinstance(w, UrysohnWitness)

    def test_method_is_order_metric(self):
        o = OrderTopologySpace()
        w = urysohn_function(o, 0, frozenset())
        assert w is not None
        assert "order" in w.method.lower() or "metric" in w.method.lower()

    def test_formula_mentions_distance(self):
        o = OrderTopologySpace()
        w = urysohn_function(o, 0, frozenset())
        assert w is not None
        assert "d" in w.formula or "distance" in w.formula.lower()

    def test_values_none(self):
        o = OrderTopologySpace()
        w = urysohn_function(o, 0, frozenset())
        assert w is not None
        assert w.values is None


# ==========================================================================
# _decide certificate-first dispatch
# ==========================================================================

class TestDecideCertificateFirst:
    def test_alexandroff_t0_uses_certificate_reason(self):
        # The reason should come from the certificate (mentions antisymmetry)
        # not from the generic finite-topology enumeration
        chain = AlexandroffSpace("chain2", {0, 1}, [(0, 1)])
        v = is_t0(chain)
        assert v.value is True
        assert "antisymmetric" in v.reason.lower() or "AlexandroffSpace" in v.reason

    def test_alexandroff_connected_uses_certificate_reason(self):
        chain = AlexandroffSpace("chain3", {0, 1, 2}, [(0, 1), (1, 2)])
        v = is_connected(chain)
        assert v.value is True
        assert "AlexandroffSpace" in v.reason or "connected" in v.reason.lower()

    def test_regular_finite_space_still_works(self):
        # Non-AlexandroffSpace finite spaces still go through finite_rule
        from pytop.experimental.spaces import FiniteSpace, is_t0
        s = FiniteSpace("sierpinski", {0, 1}, [set(), {0}, {0, 1}])
        v = is_t0(s)
        # Sierpinski IS T0 (0 and 1 are distinguishable: 0 is in {0} but 1 is not)
        assert v.value is True

    def test_non_t0_space_counterexample_via_certificate(self):
        # AlexandroffSpace with cyclic order → not T0, certificate provides counterexample
        cyclic = AlexandroffSpace("cyclic", {0, 1, 2}, [(0, 1), (1, 2), (2, 0)])
        v = is_t0(cyclic)
        assert v.value is False
        assert v.counterexample is not None

    def test_certificate_returned_for_cofinite_infinite(self):
        # CofiniteSpace has a certificate for T0 → used by _decide via infinite path
        c = CofiniteSpace()
        v = is_t0(c)
        assert v.value is True
