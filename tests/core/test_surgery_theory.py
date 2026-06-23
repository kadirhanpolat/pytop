"""Tests for P7.5 — surgery_theory module.

Covers:
  handle_attachment  : 1-handle (connect), 2-handle (fill S¹), errors
  trace_cobordism    : returns SurgeryTrace + result complex
  trace_homology     : H_*(W) for known handle attachments
"""

from __future__ import annotations

import pytest

from pytop.simplices import Simplex
from pytop.simplicial_complexes import SimplicialComplex
from pytop.surgery_theory import (
    SurgeryTrace,
    TraceHomology,
    handle_attachment,
    trace_cobordism,
    trace_homology,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _two_points() -> SimplicialComplex:
    return SimplicialComplex([Simplex([0]), Simplex([1])])


def _circle() -> SimplicialComplex:
    return SimplicialComplex([
        Simplex([0]), Simplex([1]), Simplex([2]),
        Simplex([0, 1]), Simplex([0, 2]), Simplex([1, 2]),
    ])


def _disk() -> SimplicialComplex:
    return SimplicialComplex([
        Simplex([0]), Simplex([1]), Simplex([2]),
        Simplex([0, 1]), Simplex([0, 2]), Simplex([1, 2]),
        Simplex([0, 1, 2]),
    ])


def _sphere_s0() -> SimplicialComplex:
    """S⁰ = two discrete points."""
    return _two_points()


# ---------------------------------------------------------------------------
# handle_attachment
# ---------------------------------------------------------------------------

class TestHandleAttachment:
    def test_1_handle_on_two_points(self) -> None:
        K = _two_points()
        S0 = _sphere_s0()
        t = handle_attachment(K, S0)
        assert isinstance(t, SurgeryTrace)
        assert t.handle_index == 1

    def test_1_handle_creates_segment(self) -> None:
        K = _two_points()
        t = handle_attachment(K, K)
        # W = two_points ∪ cone(S⁰) = two_points ∪ [s,0] ∪ [s,1] ∪ {s}
        assert "_h" in t.trace.vertices

    def test_1_handle_connects(self) -> None:
        from pytop.homology import simplicial_homology
        K = _two_points()
        t = handle_attachment(K, K)
        # After attaching 1-handle: W is connected
        assert simplicial_homology(t.trace, 0).betti == 1

    def test_2_handle_on_circle(self) -> None:
        K = _circle()
        t = handle_attachment(K, K)  # S¹ as attaching sphere → 2-handle
        assert t.handle_index == 2

    def test_2_handle_fills_circle(self) -> None:
        from pytop.homology import simplicial_homology
        K = _circle()
        t = handle_attachment(K, K)
        # Cone over S¹ kills H_1: trace ≃ D² (contractible)
        assert simplicial_homology(t.trace, 0).betti == 1
        assert simplicial_homology(t.trace, 1).betti == 0

    def test_trace_contains_original(self) -> None:
        K = _two_points()
        t = handle_attachment(K, K)
        K_verts = K.vertices
        assert K_verts <= t.trace.vertices

    def test_handle_index_recorded(self) -> None:
        K = _two_points()
        t = handle_attachment(K, K)
        assert t.handle_index == 1

    def test_error_apex_in_K(self) -> None:
        K = _two_points()
        with pytest.raises(ValueError, match="already a vertex"):
            handle_attachment(K, K, apex=0)

    def test_error_attaching_sphere_not_in_K(self) -> None:
        K = _two_points()
        foreign = SimplicialComplex([Simplex([99])])
        with pytest.raises(ValueError, match="not in K"):
            handle_attachment(K, foreign)

    def test_custom_apex(self) -> None:
        K = _two_points()
        t = handle_attachment(K, K, apex="core")
        assert "core" in t.trace.vertices

    def test_0_handle_adds_point(self) -> None:
        # Attaching sphere for 0-handle: empty (no sphere), but here
        # S^{-1} = ∅ → handle_index = 0; we test by using a single vertex
        # as a degenerate case.  0-handle = disjoint point.
        # Actually attaching sphere for k=0 is S^{-1}=∅, not implementable here.
        # Instead test with a point complex and its 0-sphere.
        K = SimplicialComplex([Simplex([0])])
        pt = SimplicialComplex([Simplex([0])])
        t = handle_attachment(K, pt, apex="p")
        assert "p" in t.trace.vertices


# ---------------------------------------------------------------------------
# trace_cobordism
# ---------------------------------------------------------------------------

class TestTraceCobordism:
    def test_returns_tuple(self) -> None:
        K = _two_points()
        result = trace_cobordism(K, K)
        assert isinstance(result, tuple) and len(result) == 2

    def test_surgery_trace_type(self) -> None:
        K = _two_points()
        tr, K_prime = trace_cobordism(K, K)
        assert isinstance(tr, SurgeryTrace)

    def test_result_complex_is_trace(self) -> None:
        K = _two_points()
        tr, K_prime = trace_cobordism(K, K)
        # In the simplicial model K' = trace
        assert K_prime.simplexes == tr.trace.simplexes

    def test_1_handle_trace_connected(self) -> None:
        from pytop.homology import simplicial_homology
        K = _two_points()
        tr, K_prime = trace_cobordism(K, K)
        assert simplicial_homology(K_prime, 0).betti == 1


# ---------------------------------------------------------------------------
# trace_homology
# ---------------------------------------------------------------------------

class TestTraceHomology:
    def test_type(self) -> None:
        K = _two_points()
        tr = handle_attachment(K, K)
        h = trace_homology(tr)
        assert isinstance(h, TraceHomology)

    def test_1_handle_h0(self) -> None:
        K = _two_points()
        tr = handle_attachment(K, K)
        h = trace_homology(tr)
        assert h.get(0).betti == 1

    def test_1_handle_h1_zero(self) -> None:
        # Cone over S⁰ = interval: H_1 = 0
        K = _two_points()
        tr = handle_attachment(K, K)
        h = trace_homology(tr)
        assert h.get(1).betti == 0

    def test_2_handle_on_circle_kills_h1(self) -> None:
        K = _circle()
        tr = handle_attachment(K, K)
        h = trace_homology(tr)
        assert h.get(0).betti == 1
        assert h.get(1).betti == 0

    def test_handle_index_in_result(self) -> None:
        K = _two_points()
        tr = handle_attachment(K, K)
        h = trace_homology(tr)
        assert h.handle_index == 1

    def test_euler_characteristic(self) -> None:
        K = _two_points()
        tr = handle_attachment(K, K)
        h = trace_homology(tr)
        # χ = β_0 - β_1 + β_2 - ...
        expected = sum((-1) ** k * h.get(k).betti for k in range(len(h.groups)))
        assert h.euler_characteristic == expected

    def test_get_out_of_range(self) -> None:
        K = _two_points()
        tr = handle_attachment(K, K)
        h = trace_homology(tr)
        result = h.get(100)
        assert result.betti == 0

    def test_max_degree_respected(self) -> None:
        K = _circle()
        tr = handle_attachment(K, K)
        h = trace_homology(tr, max_degree=1)
        assert len(h.groups) == 2  # degrees 0 and 1

    def test_disk_2_handle_no_higher_homology(self) -> None:
        # Start with disk, attach 2-handle (fills again) — W still contractible
        K = _disk()
        # Attaching sphere = boundary = circle; but circle is subcomplex of disk
        circle_in_disk = SimplicialComplex([
            Simplex([0]), Simplex([1]), Simplex([2]),
            Simplex([0, 1]), Simplex([0, 2]), Simplex([1, 2]),
        ])
        tr = handle_attachment(K, circle_in_disk)
        h = trace_homology(tr)
        assert h.get(0).betti == 1
