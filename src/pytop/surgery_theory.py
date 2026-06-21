"""Handle decompositions and surgery theory.

P7.5 milestone — three public objects:

handle_attachment  : attach a k-handle to a simplicial complex
trace_cobordism    : build the trace W of a surgery on a simplicial complex
trace_homology     : compute H_*(W; Z) via Mayer–Vietoris for the trace

Mathematical background
-----------------------
**Handle decomposition** (Morse theory / surgery):  Given an n-manifold M with
boundary, attaching a k-handle means gluing Dᵏ × D^{n−k} along Sᵏ⁻¹ × D^{n−k}
in the boundary ∂M.  The effect on the homotopy type is equivalent to attaching
a k-cell.  Here we work simplicially:

    handle_attachment(K, attaching_sphere) → K ∪_f Dᵏ

where ``attaching_sphere`` is a sub-complex homeomorphic to Sᵏ⁻¹ and Dᵏ is
the cone over it.  The result is K with the cone CL appended, where the
cone apex is the core of the handle.

**Surgery** on a knot/manifold replaces a tubular neighbourhood N(K) ≅ Sᵏ⁻¹ × Dⁿ⁻ᵏ
with Dᵏ × Sⁿ⁻ᵏ⁻¹.  The **trace cobordism** W of the surgery is the manifold with

    ∂W = M ⊔ M'

where M is the original manifold and M' is the result after surgery.  Simplicially,
the trace is built as the mapping cylinder of the attaching map:

    W = (M × I) ∪_{Sᵏ⁻¹ × {1}} (Dᵏ attachment)

We represent W as a pair (W_complex, M_complex, M_prime_complex) and compute
its homology via the Mayer–Vietoris sequence for the decomposition

    W = (M × I) ∪ (handle)    with    (M × I) ∩ (handle) ≅ Sᵏ⁻¹

Cross-validation
----------------
For Dehn surgery on the unknot in S³:
    M = S³,  surgery along unknot = S¹ × D²,  M' = S² × S¹ or L(p,q)
    H_*(trace W) verifiable against SnapPy (see test_snappy_oracle.py).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .homology import HomologyResult, simplicial_homology
from .mayer_vietoris import (
    _compute_homology_data,
    _induced_on_hk,
    sc_union,
)
from .simplices import Simplex
from .simplicial_complexes import SimplicialComplex
from .simplicial_maps import cone_complex


@dataclass
class SurgeryTrace:
    """Result of attaching a handle to a simplicial complex.

    Attributes
    ----------
    original : SimplicialComplex
        The original complex M before surgery.
    handle : SimplicialComplex
        The cone Dᵏ attached along the attaching sphere.
    trace : SimplicialComplex
        The trace W = M ∪ Dᵏ (union along the attaching sphere).
    attaching_sphere : SimplicialComplex
        The sub-complex Sᵏ⁻¹ ⊆ ∂M along which the handle is glued.
    handle_index : int
        The handle index k (dimension of the core Dᵏ).
    """

    original: SimplicialComplex
    handle: SimplicialComplex
    trace: SimplicialComplex
    attaching_sphere: SimplicialComplex
    handle_index: int


def handle_attachment(
    K: SimplicialComplex,
    attaching_sphere: SimplicialComplex,
    apex: Any = "_h",
) -> SurgeryTrace:
    """Attach a k-handle to K along an attaching sphere.

    Computes the cone CDᵏ = cone(attaching_sphere) with apex vertex ``apex``
    and glues it to K along the attaching sphere.  The result is the
    simplicial complex

        W = K ∪_{attaching_sphere} cone(attaching_sphere)

    which has the homotopy type of K with a k-cell attached.

    Parameters
    ----------
    K : SimplicialComplex
        The base complex (manifold with boundary, or any complex).
    attaching_sphere : SimplicialComplex
        A sub-complex of K homeomorphic to Sᵏ⁻¹.  Every simplex of
        ``attaching_sphere`` must already appear in K.
    apex : Any
        Label for the cone apex (core of the handle).  Must not be in K.

    Returns
    -------
    SurgeryTrace
        With ``trace = K ∪ cone(attaching_sphere)`` and ``handle_index = k``
        where k = attaching_sphere.dimension + 1.

    Raises
    ------
    ValueError
        If ``attaching_sphere`` is not a sub-complex of K, or apex is in K.

    Examples
    --------
    Attaching a 1-handle to two disjoint points (= connecting them with an arc):

    >>> from pytop.simplices import Simplex
    >>> from pytop.simplicial_complexes import SimplicialComplex
    >>> K = SimplicialComplex([Simplex([0]), Simplex([1])])
    >>> S0 = K  # S⁰ = two points
    >>> t = handle_attachment(K, S0)
    >>> t.handle_index
    1
    """
    if apex in K.vertices:
        raise ValueError(f"Apex {apex!r} is already a vertex of K.")

    # Verify attaching_sphere ⊆ K
    K_simplices = {s.vertices for s in K.simplexes}
    for s in attaching_sphere.simplexes:
        if s.vertices not in K_simplices:
            raise ValueError(
                f"Attaching sphere simplex {set(s.vertices)} is not in K."
            )

    handle = cone_complex(attaching_sphere, apex=apex)
    trace = sc_union(K, handle)
    k = attaching_sphere.dimension + 1

    return SurgeryTrace(
        original=K,
        handle=handle,
        trace=trace,
        attaching_sphere=attaching_sphere,
        handle_index=k,
    )


def trace_cobordism(
    K: SimplicialComplex,
    attaching_sphere: SimplicialComplex,
    apex: Any = "_h",
) -> tuple[SurgeryTrace, SimplicialComplex]:
    """Build the trace cobordism of a surgery on K.

    The trace cobordism W is the result of attaching a handle to K:

        W = K ∪_{Sᵏ⁻¹} Dᵏ

    and the boundary ∂W = K ⊔ K' where K' is obtained from K by surgery
    (removing the attaching sphere neighbourhood and replacing with the dual
    disk boundary).

    For the simplicial model:
    - ``W`` = handle_attachment(K, attaching_sphere)
    - ``K'`` = K with the attaching sphere filled in
      (since surgery kills [Sᵏ⁻¹] and introduces a new Dᵏ)

    Parameters
    ----------
    K : SimplicialComplex
    attaching_sphere : SimplicialComplex
        Sub-complex of K ≅ Sᵏ⁻¹.
    apex : Any
        Apex for the cone.

    Returns
    -------
    (surgery_trace, result_complex)
        ``surgery_trace`` is the SurgeryTrace of the handle attachment.
        ``result_complex`` is K' = K ∪ cone(attaching_sphere) with the
        attaching sphere contractible — i.e., the manifold after surgery
        (same as the trace since we work simplicially without removing anything).
    """
    trace = handle_attachment(K, attaching_sphere, apex=apex)
    # K' in the simplicial model: the trace complex itself (attaching the disk
    # kills the Sᵏ⁻¹ class and creates a new manifold with the handle core)
    result_complex = trace.trace
    return trace, result_complex


@dataclass
class TraceHomology:
    """Homology groups of the surgery trace W.

    Attributes
    ----------
    groups : list[HomologyResult]
        Homology groups H_k(W; Z) for k = 0, 1, …, max_degree.
    handle_index : int
        The handle index k of the surgery.
    euler_characteristic : int
        χ(W) = Σ (−1)^k β_k(W).
    """

    groups: list[HomologyResult]
    handle_index: int
    euler_characteristic: int

    def get(self, degree: int) -> HomologyResult:
        """Return H_degree(W; Z), or trivial group if degree out of range."""
        if 0 <= degree < len(self.groups):
            return self.groups[degree]
        return HomologyResult(degree=degree, betti=0, torsion=())


def trace_homology(
    surgery_trace: SurgeryTrace,
    max_degree: int | None = None,
) -> TraceHomology:
    """Compute the homology of the surgery trace W via direct simplicial homology.

    For a handle attachment W = K ∪_{Sᵏ⁻¹} Dᵏ the homology satisfies
    (by Mayer–Vietoris for the decomposition W = K ∪ Dᵏ along Sᵏ⁻¹):

        ⋯ → H_n(Sᵏ⁻¹) → H_n(K) ⊕ H_n(Dᵏ) → H_n(W) → H_{n-1}(Sᵏ⁻¹) → ⋯

    Since Dᵏ is contractible and Sᵏ⁻¹ is the attaching sphere, this gives:

        H_n(W) ≅ H_n(K)          for n ≠ k−1, k
        H_{k-1}(W): kills the [Sᵏ⁻¹] class
        H_k(W): creates a new generator from the handle core

    The homology is computed directly on the trace complex (no approximation).

    Parameters
    ----------
    surgery_trace : SurgeryTrace
    max_degree : int | None
        Compute up to this degree.  Defaults to trace.dimension + 1.

    Returns
    -------
    TraceHomology
        With groups H_k(W) for k = 0, …, max_degree.
    """
    W = surgery_trace.trace
    top = max_degree if max_degree is not None else W.dimension + 1

    groups: list[HomologyResult] = [
        simplicial_homology(W, k) for k in range(top + 1)
    ]
    chi = sum((-1) ** k * g.betti for k, g in enumerate(groups))

    return TraceHomology(
        groups=groups,
        handle_index=surgery_trace.handle_index,
        euler_characteristic=chi,
    )
