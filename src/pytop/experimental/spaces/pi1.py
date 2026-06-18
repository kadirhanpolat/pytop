"""π₁ computation for experimental.spaces Space objects.

Bridges the :class:`~pytop.experimental.spaces.core.Space` protocol to the
``van_kampen`` engine via the **McCord theorem**: for a finite T0 topological
space X, the geometric realization of the *order complex* of the specialization
partial order is weakly homotopy equivalent to X, so

    π₁(X) ≅ π₁(|K(X)|)

where |K(X)| is the geometric realization of K(X). The order complex has:

* **Vertices** — points of X.
* **Edges** — pairs (x, y) with x <_spec y (strict specialization).
* **2-cells** — triples (x, y, z) with x <_spec y <_spec z (triangles fill in
  the homotopy so composed paths through y are contractible).

The fundamental group is then computed by the CW spanning-tree algorithm
(:func:`~pytop.van_kampen.cw_complex_pi1`).

For **non-T0** spaces the T0 quotient (identifying points with the same
topological closure) is taken first — it shares the same weak homotopy type.

For **constructed spaces** structural theorems are applied:

* **ProductSpace**: π₁(A × B) ≅ π₁(A) × π₁(B) (for path-connected factors).
* **SumSpace**: π₁(A ⊔ B, a₀) ≅ π₁(A, a₀)  (basepoint in A; the two
  components cannot be connected by a path).

Public API
----------
Pi1Result         — fundamental group result with group type and notes
pi1_space         — compute π₁ for any Space object
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pytop.van_kampen import (
    CW1Complex,
    DirectedEdge,
    Face2,
    GroupPresentation,
    _abelianize,
    _identify_group,
    _tietze_simplify,
    cw_complex_pi1,
    trivial_group,
)

from .core import NotEnumerableError, Space
from .constructed import ProductSpace, SumSpace


# --------------------------------------------------------------------------
# Pi1Result
# --------------------------------------------------------------------------

@dataclass
class Pi1Result:
    """Fundamental group of a topological space.

    Attributes
    ----------
    presentation :
        Tietze-simplified group presentation ⟨S | R⟩.
    group_type :
        Named identification: ``"trivial"``, ``"infinite_cyclic"``,
        ``"free_rank_n"``, ``"cyclic_n"``, etc., or ``"unknown"``.
    abelianization_betti :
        Rank of the free part of H₁ = π₁^{ab}.
    abelianization_torsion :
        Torsion part of H₁ as a tuple of integers.
    method :
        Algorithmic source: ``"order_complex"``, ``"product_theorem"``,
        ``"sum_theorem"``, ``"trivial_finite"``, or ``"certificate"``.
    space_name :
        Name of the space.
    notes :
        Human-readable derivation notes.
    """

    presentation: GroupPresentation
    group_type: str
    abelianization_betti: int
    abelianization_torsion: tuple[int, ...]
    method: str
    space_name: str
    notes: tuple[str, ...]

    def presentation_string(self) -> str:
        return self.presentation.presentation_string()

    def is_trivial(self) -> bool:
        return self.group_type == "trivial"

    def is_free(self) -> bool:
        return self.presentation.is_free


# --------------------------------------------------------------------------
# Specialization order helpers
# --------------------------------------------------------------------------

def _compute_spec_order(pts: list[Any], opens: set[frozenset]) -> set[tuple[Any, Any]]:
    """Strict specialization order: {(x, y) : y ∈ cl({x}), x ≠ y}."""
    carrier = frozenset(pts)
    closed = {carrier - o for o in opens}
    order: set[tuple[Any, Any]] = set()
    for x in pts:
        # cl({x}) = intersection of all closed sets containing x
        cx: frozenset = carrier
        for f in closed:
            if x in f:
                cx &= f
        for y in pts:
            if y != x and y in cx:
                order.add((x, y))
    return order


def _t0_quotient(pts: list[Any], spec: set[tuple[Any, Any]]) -> dict[Any, Any]:
    """Map each point to its T0 equivalence class representative.

    x ~ y iff (x, y) ∈ spec and (y, x) ∈ spec (i.e., cl({x}) = cl({y})).
    Uses path-compression union-find.
    """
    parent: dict[Any, Any] = {p: p for p in pts}

    def find(p: Any) -> Any:
        while parent[p] != p:
            parent[p] = parent[parent[p]]
            p = parent[p]
        return p

    def union(p: Any, q: Any) -> None:
        rp, rq = find(p), find(q)
        if rp != rq:
            parent[rp] = rq

    for (x, y) in spec:
        if (y, x) in spec:
            union(x, y)

    return {p: find(p) for p in pts}


def _quotient_spec_order(
    pts: list[Any],
    spec: set[tuple[Any, Any]],
    reprs: dict[Any, Any],
) -> tuple[list[Any], set[tuple[Any, Any]]]:
    """Project the spec order onto the T0 quotient representatives."""
    q_pts_set: set[Any] = set(reprs.values())
    q_pts = [p for p in pts if reprs[p] == p]  # keep only canonical reps, in original order

    q_spec: set[tuple[Any, Any]] = set()
    for (x, y) in spec:
        rx, ry = reprs[x], reprs[y]
        if rx != ry:
            q_spec.add((rx, ry))

    return q_pts, q_spec


# --------------------------------------------------------------------------
# Order complex → CW1Complex
# --------------------------------------------------------------------------

def _order_complex_cw(pts: list[Any], spec: set[tuple[Any, Any]]) -> CW1Complex:
    """Build the CW1Complex for the order complex of a finite strict partial order.

    Vertices: one per point in pts.
    Edges: one directed edge e_{i}_{j} for each (pts[i], pts[j]) ∈ spec.
    2-cells: one face per 3-chain (x, y, z) with x <_spec y <_spec z.
    """
    idx = {p: i for i, p in enumerate(pts)}
    v_name = {p: f"v{idx[p]}" for p in pts}

    vertices = frozenset(v_name.values())

    edges: list[DirectedEdge] = []
    edge_name: dict[tuple[Any, Any], str] = {}
    for (x, y) in sorted(spec, key=lambda e: (idx[e[0]], idx[e[1]])):
        name = f"e{idx[x]}_{idx[y]}"
        edges.append(DirectedEdge(name, v_name[x], v_name[y]))
        edge_name[(x, y)] = name

    faces: list[Face2] = []
    face_count = 0
    for x in pts:
        for y in pts:
            if (x, y) not in spec:
                continue
            for z in pts:
                if (y, z) not in spec:
                    continue
                # x <_spec y <_spec z; by transitivity (x, z) ∈ spec
                if (x, z) not in edge_name:
                    continue
                e_xy = edge_name[(x, y)]
                e_yz = edge_name[(y, z)]
                e_xz = edge_name[(x, z)]
                faces.append(Face2(
                    f"f{face_count}",
                    ((e_xy, +1), (e_yz, +1), (e_xz, -1)),
                ))
                face_count += 1

    basepoint = v_name[pts[0]] if pts else None

    return CW1Complex(
        vertices=vertices,
        edges=tuple(edges),
        faces=tuple(faces),
        basepoint=basepoint,
    )


# --------------------------------------------------------------------------
# Result construction helper
# --------------------------------------------------------------------------

def _make_result(
    pres: GroupPresentation,
    method: str,
    space_name: str,
    notes: list[str],
) -> Pi1Result:
    simp_gens, simp_rels = _tietze_simplify(
        list(pres.generators), list(pres.relators)
    )
    simplified = GroupPresentation(
        generators=tuple(simp_gens),
        relators=tuple(simp_rels),
    )
    ab = _abelianize(simp_gens, simp_rels)
    group_type = _identify_group(simp_gens, simp_rels)
    return Pi1Result(
        presentation=simplified,
        group_type=group_type,
        abelianization_betti=ab.betti,
        abelianization_torsion=ab.torsion,
        method=method,
        space_name=space_name,
        notes=tuple(notes),
    )


# --------------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------------

def pi1_space(space: Space) -> Pi1Result:
    """Compute π₁ of a topological space in the experimental.spaces protocol.

    Parameters
    ----------
    space :
        Any finite :class:`~pytop.experimental.spaces.core.Space`, or a
        :class:`~pytop.experimental.spaces.constructed.ProductSpace` /
        :class:`~pytop.experimental.spaces.constructed.SumSpace` of finite
        spaces.

    Returns
    -------
    Pi1Result
        The fundamental group presentation together with its group type,
        abelianization, and derivation notes.

    Raises
    ------
    NotImplementedError
        When ``space`` is infinite and has no certificate-based route, or
        when the construction kind is not supported.

    Examples
    --------
    Contractible space (chain 0 < 1 < 2) has trivial π₁::

        from pytop.experimental.spaces import AlexandroffSpace
        from pytop.experimental.spaces.pi1 import pi1_space
        chain = AlexandroffSpace("chain3", {0,1,2}, [(0,1),(1,2)])
        result = pi1_space(chain)
        assert result.group_type == "trivial"

    Minimal finite T0 model of S¹ (diamond poset) has π₁ = ℤ::

        diamond = AlexandroffSpace("S1_4pt", {0,1,2,3},
                                   [(0,2),(0,3),(1,2),(1,3)])
        result = pi1_space(diamond)
        assert result.group_type == "infinite_cyclic"
    """
    # ---------- Constructed spaces ----------
    if isinstance(space, ProductSpace):
        return _product_pi1(space)
    if isinstance(space, SumSpace):
        return _sum_pi1(space)

    # ---------- Finite spaces via order complex ----------
    if space.is_finite():
        return _finite_pi1(space)

    raise NotImplementedError(
        f"π₁ not implemented for infinite space {space.name!r}. "
        "Only finite spaces and finite constructions are supported."
    )


def _finite_pi1(space: Space) -> Pi1Result:
    try:
        pts = list(space.points())
        opens = {frozenset(o) for o in space.open_sets()}
    except NotEnumerableError:
        raise NotImplementedError(f"π₁: {space.name!r} does not expose an enumerable topology.")

    notes = [f"Space: {space.name!r} ({len(pts)} points, {len(opens)} open sets)"]

    # Trivial cases
    if len(pts) == 0:
        return _make_result(trivial_group(), "trivial_finite", space.name,
                            notes + ["Empty space: π₁ = trivial."])
    if len(pts) == 1:
        return _make_result(trivial_group(), "trivial_finite", space.name,
                            notes + ["Single point: π₁ = trivial."])

    # Compute strict specialization order
    spec = _compute_spec_order(pts, opens)
    notes.append(f"Specialization order: {len(spec)} strict comparable pair(s).")

    # T0 quotient (if non-T0 space, identify equivalent points)
    reprs = _t0_quotient(pts, spec)
    n_classes = len(set(reprs.values()))
    if n_classes < len(pts):
        q_pts, q_spec = _quotient_spec_order(pts, spec, reprs)
        notes.append(
            f"Non-T0 space: T0 quotient collapses {len(pts)} → {n_classes} points "
            f"(same weak homotopy type by McCord)."
        )
        pts, spec = q_pts, q_spec
    else:
        notes.append("Space is T0 (no collapsing needed).")

    # Build order complex CW structure
    cw = _order_complex_cw(pts, spec)
    notes.append(
        f"Order complex: {len(cw.vertices)} vertices, {len(cw.edges)} edges, "
        f"{len(cw.faces)} 2-cells."
    )

    # π₁ via spanning-tree algorithm
    pres = cw_complex_pi1(cw)
    notes.append(f"CW spanning-tree: {len(pres.generators)} generator(s), "
                 f"{len(pres.relators)} relator(s).")

    return _make_result(pres, "order_complex", space.name, notes)


def _product_pi1(space: ProductSpace) -> Pi1Result:
    """π₁(A × B × …) ≅ π₁(A) × π₁(B) × … for path-connected factors.

    Implemented as the direct product: combine all generators and relators,
    then add commutativity relations [a, b] = aba⁻¹b⁻¹ = 1 between generators
    from different factors.
    """
    factor_results = [pi1_space(op) for op in space.construction.operands]
    notes = [f"Product: {space.name!r}"]

    # Rename generators to avoid collisions: factor_i_gen_j → fⁱgⱼ
    all_gens: list[str] = []
    all_rels: list = []
    factor_gens: list[list[str]] = []

    for i, res in enumerate(factor_results):
        renamed = [f"f{i}g{j}" for j, _ in enumerate(res.presentation.generators)]
        old_to_new = dict(zip(res.presentation.generators, renamed))
        all_gens.extend(renamed)
        factor_gens.append(renamed)

        for rel in res.presentation.relators:
            new_rel = tuple(
                (old_to_new.get(g, g), e) for g, e in rel
            )
            all_rels.append(new_rel)

        notes.append(f"  Factor {i} ('{res.space_name}'): {res.presentation_string()}")

    # Add commutativity between factors
    comm_count = 0
    for i in range(len(factor_gens)):
        for j in range(i + 1, len(factor_gens)):
            for a in factor_gens[i]:
                for b in factor_gens[j]:
                    comm = ((a, 1), (b, 1), (a, -1), (b, -1))
                    all_rels.append(comm)
                    comm_count += 1
    notes.append(f"Added {comm_count} commutativity relator(s) between factors.")

    try:
        pres = GroupPresentation(generators=tuple(all_gens), relators=tuple(all_rels))
    except Exception:
        pres = trivial_group()

    return _make_result(pres, "product_theorem", space.name, notes)


def _sum_pi1(space: SumSpace) -> Pi1Result:
    """π₁(A ⊔ B, a₀) ≅ π₁(A, a₀) when the basepoint lies in A.

    A topological sum (disjoint union) is disconnected; paths cannot cross
    from one summand to another.  The basepoint determines which component
    matters.  By convention we use the first summand as the basepoint component.
    """
    operands = space.construction.operands
    notes = [
        f"Sum: {space.name!r} ({len(operands)} summand(s)).",
        "Basepoint convention: first summand.",
        "π₁(A ⊔ B, a₀) = π₁(A, a₀) since paths cannot cross components.",
    ]
    if not operands:
        return _make_result(trivial_group(), "sum_theorem", space.name, notes)

    first = pi1_space(operands[0])
    notes.append(f"First summand ('{first.space_name}'): {first.presentation_string()}")

    return Pi1Result(
        presentation=first.presentation,
        group_type=first.group_type,
        abelianization_betti=first.abelianization_betti,
        abelianization_torsion=first.abelianization_torsion,
        method="sum_theorem",
        space_name=space.name,
        notes=tuple(notes),
    )


__all__ = [
    "Pi1Result",
    "pi1_space",
]
