"""Khovanov homology — the categorification of the Jones polynomial.

For a link diagram with ``n`` crossings, Khovanov homology ``Kh^{i,j}(L)`` is a
bigraded abelian group whose *graded Euler characteristic* is the unnormalised
Jones polynomial ``Ĵ_L(q)`` (with ``Ĵ_unknot = q + q⁻¹``):

    Σ_{i,j} (−1)^i · q^j · rank Kh^{i,j}(L) = Ĵ_L(q).

In pytop's crossing-sign convention this cross-checks against
:func:`pytop.knot_invariants.jones_polynomial` as
``Ĵ_L(q) = (−1)^{c−1} (q + q⁻¹) · V_L(t = q²)`` for a ``c``-component link.

Construction (Khovanov 2000, Bar-Natan 2002)
--------------------------------------------
1. **Cube of resolutions.**  Each crossing is given a ``0``-smoothing
   (Kauffman A) or a ``1``-smoothing (Kauffman B); the ``2ⁿ`` vertices of
   ``{0,1}ⁿ`` are complete resolutions, each a disjoint union of circles.
2. **Frobenius algebra.**  To a resolution with ``k`` circles assign
   ``V^{⊗k}`` where ``V = ℤ⟨1, X⟩``, ``deg 1 = +1``, ``deg X = −1``, with
   multiplication ``m`` (``1·1=1, 1·X=X·1=X, X·X=0``) and comultiplication
   ``Δ`` (``Δ1 = 1⊗X + X⊗1, ΔX = X⊗X``).
3. **Differential.**  An edge of the cube (one ``0 → 1``) merges two circles
   (apply ``m``) or splits one (apply ``Δ``), with the Khovanov sign
   ``(−1)^{#1's before the flipped crossing}``.  This makes ``d² = 0``.
4. **Gradings.**  With ``n₊``/``n₋`` positive/negative crossings, a generator
   in a vertex of weight ``r = Σ`` (number of 1-smoothings) has homological
   degree ``i = r − n₋`` and quantum degree
   ``j = (#1 − #X) + r + n₊ − 2n₋``.
5. **Homology.**  ``d`` preserves ``j``; for each quantum grading the complex is
   reduced over ℤ by Smith normal form, giving free ranks *and torsion*
   (e.g. the right-handed trefoil's ``ℤ/2`` at ``(i,j) = (3,7)``).

Pure Python, exact integer arithmetic, no dependencies.  The total dimension is
exponential in the crossing number; this is intended for the small diagrams of
the knot tables, not large-scale computation.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Any

from .homology import _smith_normal_form
from .knot_invariants import KnotDiagram

__all__ = [
    "KhovanovHomology",
    "khovanov_homology",
]


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class KhovanovHomology:
    """Bigraded Khovanov homology.

    ``groups`` maps each ``(i, j)`` with nonzero homology to a pair
    ``(free_rank, torsion)``, where ``torsion`` lists invariant factors
    ``d > 1`` (``d₁ | d₂ | …``).
    """

    groups: dict[tuple[int, int], tuple[int, tuple[int, ...]]]

    def free_rank(self, i: int, j: int) -> int:
        return self.groups.get((i, j), (0, ()))[0]

    def torsion(self, i: int, j: int) -> tuple[int, ...]:
        return self.groups.get((i, j), (0, ()))[1]

    def total_rank(self) -> int:
        """Total free rank over all bidegrees (the unreduced Betti number)."""
        return sum(free for free, _ in self.groups.values())

    def graded_euler_characteristic(self) -> dict[int, int]:
        """Return ``{j: Σ_i (−1)^i rank Kh^{i,j}}`` — the unnormalised Jones
        polynomial as a Laurent polynomial in ``q`` (keyed by ``q``-power)."""
        chi: dict[int, int] = {}
        for (i, j), (free, _torsion) in self.groups.items():
            if free:
                chi[j] = chi.get(j, 0) + ((-1) ** i) * free
        return {j: c for j, c in chi.items() if c != 0}

    def __str__(self) -> str:
        lines = []
        for (i, j) in sorted(self.groups):
            free, torsion = self.groups[(i, j)]
            pieces = []
            if free == 1:
                pieces.append("Z")
            elif free > 1:
                pieces.append(f"Z^{free}")
            pieces.extend(f"Z/{d}" for d in torsion)
            lines.append(f"Kh^{{{i},{j}}} = " + " + ".join(pieces))
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Cube of resolutions
# ---------------------------------------------------------------------------


def _resolve_circles(
    crossings: tuple[tuple[Any, Any, Any, Any], ...],
    state: tuple[int, ...],
) -> list[frozenset]:
    """Return the circles of the resolution ``state`` (0 = A, 1 = B), as a list
    of ``frozenset``s of edge labels ordered canonically by least label."""

    labels = {label for crossing in crossings for label in crossing}
    parent = {label: label for label in labels}

    def find(x: Any) -> Any:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: Any, y: Any) -> None:
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    for k, (a, b, c, d) in enumerate(crossings):
        if state[k] == 0:  # A-smoothing
            union(a, b)
            union(c, d)
        else:  # B-smoothing
            union(a, d)
            union(b, c)

    components: dict[Any, set] = {}
    for label in labels:
        components.setdefault(find(label), set()).add(label)
    return sorted(
        (frozenset(s) for s in components.values()),
        key=lambda s: min(map(repr, s)),
    )


# ---------------------------------------------------------------------------
# Khovanov complex
# ---------------------------------------------------------------------------


def _edge_image(
    circles: list[frozenset],
    circles_next: list[frozenset],
    generator: tuple[int, ...],
    touched: set,
) -> list[tuple[int, ...]]:
    """Apply the merge (``m``) or split (``Δ``) map across one cube edge.

    ``touched`` is the set of edge labels at the flipped crossing.  Returns the
    list of output generators over ``circles_next`` (0, 1, or 2 of them; labels
    are ``0 = 1`` and ``1 = X``).
    """

    affected = [idx for idx, circle in enumerate(circles) if circle & touched]
    affected_next = [idx for idx, circle in enumerate(circles_next) if circle & touched]
    label_of = {circle: generator[idx] for idx, circle in enumerate(circles)}

    def assemble(new_labels: dict[int, int]) -> tuple[int, ...]:
        out = []
        for idx, circle in enumerate(circles_next):
            out.append(new_labels[idx] if idx in new_labels else label_of[circle])
        return tuple(out)

    if len(affected) == 2:  # merge: m(x1 ⊗ x2)
        x1 = generator[affected[0]]
        x2 = generator[affected[1]]
        total = x1 + x2
        if total >= 2:  # X·X = 0
            return []
        return [assemble({affected_next[0]: total})]

    # split: Δ(x)
    x = generator[affected[0]]
    c1, c2 = affected_next
    if x == 1:  # ΔX = X ⊗ X
        return [assemble({c1: 1, c2: 1})]
    # Δ1 = 1 ⊗ X + X ⊗ 1
    return [assemble({c1: 0, c2: 1}), assemble({c1: 1, c2: 0})]


def _khovanov_complex(
    diagram: KnotDiagram,
) -> tuple[dict[tuple[int, int], list[tuple]], dict[tuple[int, int], list[list[int]]]]:
    """Build the Khovanov cochain complex of a diagram with ``n ≥ 1`` crossings.

    Returns ``(elements, differentials)`` where ``elements[(i, j)]`` lists the
    basis of the bidegree-``(i, j)`` group and ``differentials[(i, j)]`` is the
    integer matrix of ``d : C^{i}_j → C^{i+1}_j`` (rows index ``C^{i+1}_j``).
    """

    crossings = diagram.pd
    n = len(crossings)
    n_minus = sum(1 for s in diagram.signs if s < 0)
    n_plus = n - n_minus

    circle_cache: dict[tuple[int, ...], list[frozenset]] = {}

    def circles_of(state: tuple[int, ...]) -> list[frozenset]:
        cached = circle_cache.get(state)
        if cached is None:
            cached = _resolve_circles(crossings, state)
            circle_cache[state] = cached
        return cached

    # Enumerate the basis, grouped by bidegree (i, j), with a local index.
    basis_index: dict[tuple[int, int], dict[tuple, int]] = {}
    elements: dict[tuple[int, int], list[tuple]] = {}

    def grading(state: tuple[int, ...], generator: tuple[int, ...], n_circles: int):
        r = sum(state)
        i = r - n_minus
        deg = n_circles - 2 * sum(generator)  # (#1) − (#X)
        j = deg + r + n_plus - 2 * n_minus
        return i, j

    for state in product((0, 1), repeat=n):
        circles = circles_of(state)
        m = len(circles)
        for generator in product((0, 1), repeat=m):
            i, j = grading(state, generator, m)
            key = (i, j)
            table = basis_index.setdefault(key, {})
            table[(state, generator)] = len(table)
            elements.setdefault(key, []).append((state, generator))

    # Differential matrices: d[(i, j)] : C^{i}_j → C^{i+1}_j.
    differentials: dict[tuple[int, int], list[list[int]]] = {}

    for (i, j), basis in elements.items():
        target_key = (i + 1, j)
        target_index = basis_index.get(target_key, {})
        if not target_index:
            continue
        matrix = [[0] * len(basis) for _ in range(len(target_index))]
        for col, (state, generator) in enumerate(basis):
            circles = circles_of(state)
            for k in range(n):
                if state[k] == 1:
                    continue
                next_state = state[:k] + (1,) + state[k + 1 :]
                next_circles = circles_of(next_state)
                touched = set(crossings[k])
                sign = -1 if (sum(state[:k]) % 2) else 1
                for image in _edge_image(circles, next_circles, generator, touched):
                    row = target_index[(next_state, image)]
                    matrix[row][col] += sign
        differentials[(i, j)] = matrix

    return elements, differentials


def khovanov_homology(diagram: KnotDiagram) -> KhovanovHomology:
    """Return the Khovanov homology ``Kh^{i,j}`` of a knot/link diagram.

    Parameters
    ----------
    diagram:
        A :class:`~pytop.knot_invariants.KnotDiagram` (PD code with crossing
        signs).  The signs fix only the ``(n₊, n₋)`` grading shift.

    Returns
    -------
    KhovanovHomology
    """

    # Special case: a crossingless diagram is the unknot — one circle, V.
    if len(diagram.pd) == 0:
        return KhovanovHomology({(0, 1): (1, ()), (0, -1): (1, ())})

    elements, differentials = _khovanov_complex(diagram)

    # Smith normal form of each differential, computed once and reused. The ranks
    # and torsion below each reference d^{i}_j up to three times (as the outgoing
    # rank of C^i_j, the incoming rank of C^{i+1}_j, and the incoming torsion of
    # C^{i+1}_j), and SNF is the dominant cost — so memoising it per bidegree cuts
    # the homology step's SNF work ~3x with an identical result.
    snf_cache: dict[tuple[int, int], list[int]] = {}

    def snf(key: tuple[int, int]) -> list[int]:
        cached = snf_cache.get(key)
        if cached is None:
            matrix = differentials.get(key)
            cached = _smith_normal_form(matrix) if matrix else []
            snf_cache[key] = cached
        return cached

    def rank(key: tuple[int, int]) -> int:
        return len(snf(key))

    def torsion_of(key: tuple[int, int]) -> tuple[int, ...]:
        return tuple(d for d in snf(key) if d > 1)

    groups: dict[tuple[int, int], tuple[int, tuple[int, ...]]] = {}
    for (i, j), basis in elements.items():
        dim = len(basis)
        rank_out = rank((i, j))            # d^{i}_j
        rank_in = rank((i - 1, j))         # d^{i−1}_j
        free_rank = dim - rank_out - rank_in
        torsion = torsion_of((i - 1, j))   # cokernel torsion of the incoming map
        if free_rank or torsion:
            groups[(i, j)] = (free_rank, torsion)

    return KhovanovHomology(groups)
