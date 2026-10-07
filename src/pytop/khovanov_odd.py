"""Odd Khovanov homology (Ozsváth–Rasmussen–Szabó 2013).

Odd Khovanov homology ``Kh'(L)`` is a bigraded link invariant built on the same
cube of resolutions as Khovanov homology, with the symmetric algebra replaced by
the exterior algebra.  Its graded Euler characteristic is the unnormalised Jones
polynomial and its mod-2 reduction is that of even Khovanov homology, yet over ℤ
(and over ℚ) the two differ: the trefoil has rank 6 here and rank 4 in the even
theory, and for the torus knot ``8_19`` the reduced theories have rational rank 3
and 5 (ORS §5).

Construction (ORS §1)
---------------------
1. **Exterior algebra.**  A resolution with circles ``a_1, …, a_k`` gets
   ``Λ*V`` where ``V`` is free on the circles; the monomial
   ``a_{i_1} ∧ … ∧ a_{i_e}`` has quantum degree ``k − 2e``.
2. **Arrows.**  Each crossing carries an arrow joining the two arcs of its
   0-resolution; pytop draws it from arc ``(a, b)`` to arc ``(c, d)`` of the PD
   tuple ``(a, b, c, d)``.  In the 1-resolution the arrow is rotated 90°
   counterclockwise and so runs from arc ``(b, c)`` to arc ``(d, a)``.
3. **Edge maps.**  A merge of ``a_1, a_2`` is the projection induced by
   ``V → V/(a_1 − a_2)``.  A split into ``a_1, a_2``, with the rotated arrow
   pointing from ``a_1`` to ``a_2``, is ``ω ↦ (a_1 − a_2) ∧ ω̃`` for any lift ``ω̃``.
4. **Faces.**  Around each square of the cube the two composites commute
   (type C), anticommute (type A), or both vanish — the ladybug configuration of
   two interleaved arrows on one circle, typed X or Y by the arrows (ORS Fig. 2).
5. **Signs.**  A type-X edge assignment ``ε`` makes every A and X face even and
   every C and Y face odd (ORS Def. 1.1); it exists by ORS Lemma 1.2 and is
   computed here on a spanning-tree gauge, then checked on every face.

Homology is computed per quantum grading by Smith normal form, so torsion is
exact.  Pure Python with no dependencies; the cube has ``2ⁿ`` vertices, so this
is meant for knot-table diagrams, not large ones.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .homology import _smith_normal_form
from .khovanov import KhovanovHomology
from .knot_invariants import KnotDiagram

__all__ = [
    "OddKhovanovHomology",
    "khovanov_homology_odd",
    "compare_khovanov_parities",
]

Position = tuple[int, int]  # (crossing index, slot 0..3 counterclockwise)
Edge = tuple[int, int]  # (vertex bitmask, crossing flipped 0 → 1)
Face = tuple[int, int, int]  # (vertex bitmask, j, k) with j < k, both 0 at the vertex

# Smoothing arcs per state: 0 joins slots (0,1),(2,3); 1 joins (0,3),(1,2).
_SMOOTHING = ({0: 1, 1: 0, 2: 3, 3: 2}, {0: 3, 3: 0, 1: 2, 2: 1})
# A type-X edge assignment needs these faces odd and the rest (A, X) even.
_ODD_FACES = frozenset({"C", "Y"})


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OddKhovanovHomology:
    """Bigraded odd Khovanov homology of a link.

    Attributes
    ----------
    groups : dict[(int,int), tuple[int, tuple[int,...]]]
        Maps (homological_degree, quantum_degree) → (free_rank, torsion).
    writhe : int
    n_plus, n_minus : int
    jones_graded_euler : dict[int, int]
        Graded Euler characteristic per quantum degree.
    """

    groups: dict[tuple[int, int], tuple[int, tuple[int, ...]]]
    writhe: int
    n_plus: int
    n_minus: int
    jones_graded_euler: dict[int, int]

    def betti(self, i: int, j: int) -> int:
        return self.groups.get((i, j), (0, ()))[0]

    def torsion(self, i: int, j: int) -> tuple[int, ...]:
        return self.groups.get((i, j), (0, ()))[1]

    def nonzero_groups(self) -> list[tuple[int, int, int, tuple[int, ...]]]:
        return [
            (i, j, b, t)
            for (i, j), (b, t) in sorted(self.groups.items())
            if b > 0 or t
        ]

    def total_rank(self) -> int:
        return sum(b for b, _ in self.groups.values())

    def euler_characteristic(self, j: int) -> int:
        return sum(
            (-1) ** i * b
            for (i, jj), (b, _) in self.groups.items()
            if jj == j
        )


# ---------------------------------------------------------------------------
# Planar resolutions
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _Resolution:
    """The circles of one resolution, each a cyclic tuple of arc passages
    ``(crossing, from_slot, to_slot)``, and the circle through every slot."""

    passages: tuple[tuple[tuple[int, int, int], ...], ...]
    circle_of: dict[Position, int]


def _edge_partners(pd: tuple[tuple[Any, Any, Any, Any], ...]) -> dict[Position, Position]:
    where: dict[Any, list[Position]] = {}
    for k, crossing in enumerate(pd):
        for slot, label in enumerate(crossing):
            where.setdefault(label, []).append((k, slot))
    partner: dict[Position, Position] = {}
    for label, slots in where.items():
        if len(slots) != 2:
            raise ValueError(
                f"Edge label {label!r} appears {len(slots)} time(s) in the PD code, but an "
                "edge joins exactly two crossing slots, so every label must appear exactly "
                "twice. Check the PD code; the right-handed trefoil, for example, is "
                "[(1, 5, 2, 4), (3, 1, 4, 6), (5, 3, 6, 2)]."
            )
        p, q = slots
        partner[p], partner[q] = q, p
    return partner


def _check_planar(n: int, partner: dict[Position, Position]) -> None:
    """Reject PD codes that do not describe a diagram in the plane.

    Tracing faces (along an edge, then one slot counterclockwise) gives
    ``V − E + F = 2c`` for a planar diagram with ``c`` connected pieces.
    """

    root = list(range(n))

    def find(x: int) -> int:
        while root[x] != x:
            root[x] = root[root[x]]
            x = root[x]
        return x

    for (k, _), (other, _) in partner.items():
        root[find(k)] = find(other)
    pieces = len({find(k) for k in range(n)})

    seen: set[Position] = set()
    faces = 0
    for start in partner:
        if start in seen:
            continue
        faces += 1
        position = start
        while position not in seen:
            seen.add(position)
            crossing, slot = partner[position]
            position = (crossing, (slot + 1) % 4)
    euler = n - 2 * n + faces
    if euler != 2 * pieces:
        raise ValueError(
            f"The PD code is not planar: its faces give V - E + F = {euler}, where a "
            f"diagram drawn in the plane with {pieces} connected piece(s) gives "
            f"{2 * pieces}. Odd Khovanov homology needs the planar picture, because "
            "its ladybug faces are typed by which side of a circle each crossing's "
            "arrow lies on. Check that every crossing lists its four edges "
            "counterclockwise; the right-handed trefoil, for example, is "
            "[(1, 5, 2, 4), (3, 1, 4, 6), (5, 3, 6, 2)]."
        )


def _resolve(n: int, partner: dict[Position, Position], state: int) -> _Resolution:
    circle_of: dict[Position, int] = {}
    circles: list[tuple[tuple[int, int, int], ...]] = []
    for k in range(n):
        for slot in range(4):
            if (k, slot) in circle_of:
                continue
            index, passages, position = len(circles), [], (k, slot)
            while position not in circle_of:
                crossing, here = position
                there = _SMOOTHING[state >> crossing & 1][here]
                circle_of[(crossing, here)] = circle_of[(crossing, there)] = index
                passages.append((crossing, here, there))
                position = partner[(crossing, there)]
            circles.append(tuple(passages))
    return _Resolution(tuple(circles), circle_of)


# ---------------------------------------------------------------------------
# Exterior algebra (monomials are bitmasks over circle indices)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _EdgeMap:
    """``image`` sends each circle to its circle after the surgery (a split circle
    to one of its halves — any lift will do); ``tail``/``head`` mark a split."""

    image: tuple[int, ...]
    tail: int = -1
    head: int = -1


def _wedge(i: int, monomial: int) -> tuple[int, int]:
    """``a_i ∧ monomial`` as ``(sign, monomial)``; sign 0 if ``a_i`` already occurs."""

    if monomial >> i & 1:
        return 0, 0
    sign = -1 if bin(monomial & ((1 << i) - 1)).count("1") % 2 else 1
    return sign, monomial | 1 << i


def _push_forward(monomial: int, image: tuple[int, ...]) -> tuple[int, int]:
    """Apply ``a_i ↦ a_image[i]`` factor by factor; sign 0 if two factors collide."""

    sign, out, i = 1, 0, 0
    while monomial:
        if monomial & 1:
            target = image[i]
            if out >> target & 1:
                return 0, 0
            if bin(out >> (target + 1)).count("1") % 2:
                sign = -sign
            out |= 1 << target
        monomial >>= 1
        i += 1
    return sign, out


def _apply(edge: _EdgeMap, monomial: int) -> list[tuple[int, int]]:
    sign, lifted = _push_forward(monomial, edge.image)
    if not sign:
        return []
    if edge.tail < 0:
        return [(sign, lifted)]
    terms = []
    for factor, circle in ((1, edge.tail), (-1, edge.head)):
        wedge_sign, out = _wedge(circle, lifted)
        if wedge_sign:
            terms.append((factor * sign * wedge_sign, out))
    return terms


def _apply_vector(edge: _EdgeMap, vector: dict[int, int]) -> dict[int, int]:
    result: dict[int, int] = {}
    for monomial, coefficient in vector.items():
        for sign, out in _apply(edge, monomial):
            result[out] = result.get(out, 0) + sign * coefficient
    return {m: c for m, c in result.items() if c}


# ---------------------------------------------------------------------------
# The cube: edge maps, face types, edge assignment
# ---------------------------------------------------------------------------


def _build_cube(diagram: KnotDiagram) -> tuple[list[_Resolution], dict[Edge, _EdgeMap]]:
    n = len(diagram.pd)
    partner = _edge_partners(diagram.pd)
    _check_planar(n, partner)
    resolutions = [_resolve(n, partner, state) for state in range(1 << n)]
    edges: dict[Edge, _EdgeMap] = {}
    for v, source in enumerate(resolutions):
        for k in range(n):
            if v >> k & 1:
                continue
            target = resolutions[v | 1 << k]
            image = tuple(target.circle_of[p[0][:2]] for p in source.passages)
            if source.circle_of[(k, 0)] != source.circle_of[(k, 2)]:
                edges[(v, k)] = _EdgeMap(image)
            else:  # rotated arrow: from arc (b, c) to arc (d, a)
                edges[(v, k)] = _EdgeMap(image, target.circle_of[(k, 1)], target.circle_of[(k, 3)])
    return resolutions, edges


def _ladybug_type(resolution: _Resolution, j: int, k: int) -> str:
    """X or Y for two interleaved arrows on one circle (ORS Fig. 2).

    Walk the circle with arrow ``j`` on the left; the type is X when the end met
    right after ``j``'s tail is ``k``'s tail, and Y when it is ``k``'s head.
    """

    passages = resolution.passages[resolution.circle_of[(j, 0)]]
    ends = [(c, here, there) for c, here, there in passages if c in (j, k)]
    if len(ends) != 4 or len({there == (here + 1) % 4 for c, here, there in ends if c == j}) != 1:
        raise RuntimeError(f"crossings {j} and {k} do not form a ladybug configuration")
    if next(there != (here + 1) % 4 for c, here, there in ends if c == j):
        ends.reverse()  # arrow j was on the right; walk the other way
    roles = [(c, "tail" if here in (0, 1) else "head") for c, here, _ in ends]
    following = roles[(roles.index((j, "tail")) + 1) % 4]
    if following == (k, "tail"):
        return "X"
    if following == (k, "head"):
        return "Y"
    raise RuntimeError(f"arrows at crossings {j} and {k} are not interleaved")


def _face_types(
    n: int, resolutions: list[_Resolution], edges: dict[Edge, _EdgeMap]
) -> dict[Face, str]:
    unit = {0: 1}
    first_step = {edge: _apply_vector(edge_map, unit) for edge, edge_map in edges.items()}
    types: dict[Face, str] = {}
    for (u, j), step in first_step.items():
        for k in range(j + 1, n):
            if u >> k & 1:
                continue
            via_j = _apply_vector(edges[(u | 1 << j, k)], step)
            via_k = _apply_vector(edges[(u | 1 << k, j)], first_step[(u, k)])
            if not via_j and not via_k:
                types[(u, j, k)] = _ladybug_type(resolutions[u], j, k)
            elif via_j == via_k:
                types[(u, j, k)] = "C"
            elif via_j == {m: -c for m, c in via_k.items()}:
                types[(u, j, k)] = "A"
            else:
                raise RuntimeError(f"face {(u, j, k)} neither commutes nor anticommutes")
    return types


def _cube_face_types(diagram: KnotDiagram) -> dict[Face, str]:
    """Type A, C, X or Y of every square face of the cube of resolutions."""

    resolutions, edges = _build_cube(diagram)
    return _face_types(len(diagram.pd), resolutions, edges)


def _edge_assignment(n: int, types: dict[Face, str]) -> dict[Edge, int]:
    """A type-X edge assignment, fixed to +1 on a spanning tree of the cube."""

    odd: dict[Edge, int] = {}
    for k in range(n):
        for v in range(1 << n):
            if v >> k & 1:
                continue
            below = v & ((1 << k) - 1)
            if not below:
                odd[(v, k)] = 0
                continue
            j = below.bit_length() - 1
            u = v ^ 1 << j
            forced = types[(u, j, k)] in _ODD_FACES
            odd[(v, k)] = forced ^ odd[(u, j)] ^ odd[(u, k)] ^ odd[(u | 1 << k, j)]
    for (u, j, k), kind in types.items():
        parity = odd[(u, j)] ^ odd[(u | 1 << j, k)] ^ odd[(u, k)] ^ odd[(u | 1 << k, j)]
        if parity != (kind in _ODD_FACES):
            raise RuntimeError(
                "No type-X edge assignment fits the face types, which contradicts "
                "ORS Lemma 1.2 — this is a bug in pytop, please report it with the PD code."
            )
    return {edge: -1 if flag else 1 for edge, flag in odd.items()}


# ---------------------------------------------------------------------------
# Complex and homology
# ---------------------------------------------------------------------------


def _odd_khovanov_complex(
    diagram: KnotDiagram,
) -> tuple[dict[tuple[int, int], list[tuple[int, int]]], dict[tuple[int, int], list[list[int]]]]:
    """The odd Khovanov cochain complex of a diagram with ``n ≥ 1`` crossings.

    ``elements[(i, j)]`` lists the basis ``(vertex bitmask, monomial bitmask)`` of
    bidegree ``(i, j)``; ``differentials[(i, j)]`` is the integer matrix of
    ``d : C^{i}_j → C^{i+1}_j`` (rows index ``C^{i+1}_j``).
    """

    n = len(diagram.pd)
    if n == 0:
        raise ValueError(
            "The cube of resolutions needs at least one crossing; a crossingless "
            "diagram is the unknot, which khovanov_homology_odd handles directly."
        )
    n_minus = sum(1 for s in diagram.signs if s < 0)
    shift = n - n_minus - 2 * n_minus  # n₊ − 2n₋
    resolutions, edges = _build_cube(diagram)
    signs = _edge_assignment(n, _face_types(n, resolutions, edges))

    elements: dict[tuple[int, int], list[tuple[int, int]]] = {}
    index: dict[tuple[int, int], dict[tuple[int, int], int]] = {}
    for v, resolution in enumerate(resolutions):
        r, circles = bin(v).count("1"), len(resolution.passages)
        for monomial in range(1 << circles):
            key = (r - n_minus, circles - 2 * bin(monomial).count("1") + r + shift)
            table = index.setdefault(key, {})
            table[(v, monomial)] = len(table)
            elements.setdefault(key, []).append((v, monomial))

    differentials: dict[tuple[int, int], list[list[int]]] = {}
    for (i, j), basis in elements.items():
        rows = index.get((i + 1, j))
        if not rows:
            continue
        matrix = [[0] * len(basis) for _ in range(len(rows))]
        for col, (v, monomial) in enumerate(basis):
            for k in range(n):
                if v >> k & 1:
                    continue
                for sign, out in _apply(edges[(v, k)], monomial):
                    matrix[rows[(v | 1 << k, out)]][col] += signs[(v, k)] * sign
        differentials[(i, j)] = matrix
    return elements, differentials


def _bigraded_homology(
    elements: dict[tuple[int, int], list[tuple[int, int]]],
    differentials: dict[tuple[int, int], list[list[int]]],
) -> dict[tuple[int, int], tuple[int, tuple[int, ...]]]:
    factors = {key: _smith_normal_form(matrix) for key, matrix in differentials.items()}
    groups: dict[tuple[int, int], tuple[int, tuple[int, ...]]] = {}
    for (i, j), basis in elements.items():
        incoming = factors.get((i - 1, j), [])
        free = len(basis) - len(factors.get((i, j), [])) - len(incoming)
        torsion = tuple(d for d in incoming if d > 1)
        if free or torsion:
            groups[(i, j)] = (free, torsion)
    return groups


def khovanov_homology_odd(diagram: KnotDiagram) -> OddKhovanovHomology:
    """Compute the odd Khovanov homology of a knot/link diagram.

    Parameters
    ----------
    diagram : KnotDiagram
        Planar diagram with crossing signs.  Use the same `KnotDiagram`
        objects as for standard `khovanov_homology`.

    Returns
    -------
    OddKhovanovHomology
    """
    n_minus = sum(1 for s in diagram.signs if s < 0)
    n_plus = len(diagram.pd) - n_minus

    if len(diagram.pd) == 0:  # the crossingless unknot: one circle, Λ*ℤ = ℤ ⊕ ℤ
        return OddKhovanovHomology(
            groups={(0, 1): (1, ()), (0, -1): (1, ())},
            writhe=0, n_plus=0, n_minus=0,
            jones_graded_euler={1: 1, -1: 1},
        )

    groups = _bigraded_homology(*_odd_khovanov_complex(diagram))
    jones: dict[int, int] = {}
    for (i, j), (free, _) in groups.items():
        jones[j] = jones.get(j, 0) + (-1) ** i * free
    return OddKhovanovHomology(
        groups=groups,
        writhe=n_plus - n_minus,
        n_plus=n_plus,
        n_minus=n_minus,
        jones_graded_euler={j: c for j, c in jones.items() if c},
    )


def _mod_2_dimensions(
    groups: dict[tuple[int, int], tuple[int, tuple[int, ...]]],
) -> dict[tuple[int, int], int]:
    """``dim H^{i,j}(C ⊗ 𝔽₂)`` by universal coefficients:
    ``H^i ⊗ 𝔽₂ ⊕ Tor(H^{i+1}, 𝔽₂)``."""

    dims: dict[tuple[int, int], int] = {}
    for (i, j), (free, torsion) in groups.items():
        even = sum(1 for d in torsion if d % 2 == 0)
        dims[(i, j)] = dims.get((i, j), 0) + free + even
        if even:
            dims[(i - 1, j)] = dims.get((i - 1, j), 0) + even
    return {key: dim for key, dim in dims.items() if dim}


def compare_khovanov_parities(
    kh_even: KhovanovHomology,
    kh_odd: OddKhovanovHomology,
) -> dict[str, Any]:
    """Compare even and odd Khovanov homology of the same diagram.

    ``agree_at`` / ``differ_at`` / ``n_differences`` compare the integral groups
    bidegree by bidegree; they differ in general (the trefoil already does).
    ``agree_mod_2`` compares ``dim H(·; 𝔽₂)``, which must agree by ORS
    Proposition 1.6 — ``mod_2_differences`` lists any bidegree where it does not.

    Parameters
    ----------
    kh_even : KhovanovHomology
    kh_odd : OddKhovanovHomology
    """
    all_gradings: set[tuple[int, int]] = (
        set(kh_even.groups.keys()) | set(kh_odd.groups.keys())
    )
    agreements: list[tuple[int, int]] = []
    differences: list[dict[str, Any]] = []

    for (i, j) in sorted(all_gradings):
        even_g = kh_even.groups.get((i, j), (0, ()))
        odd_g = kh_odd.groups.get((i, j), (0, ()))
        if even_g == odd_g:
            agreements.append((i, j))
        else:
            differences.append({
                "grading": (i, j),
                "even": even_g,
                "odd": odd_g,
            })

    even_mod_2 = _mod_2_dimensions(kh_even.groups)
    odd_mod_2 = _mod_2_dimensions(kh_odd.groups)
    mod_2_differences = sorted(
        key for key in set(even_mod_2) | set(odd_mod_2)
        if even_mod_2.get(key, 0) != odd_mod_2.get(key, 0)
    )
    return {
        "agree_at": agreements,
        "differ_at": differences,
        "n_differences": len(differences),
        "agree_mod_2": not mod_2_differences,
        "mod_2_differences": mod_2_differences,
    }
