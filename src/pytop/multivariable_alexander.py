"""Multivariable Alexander polynomial via Wirtinger presentation + Fox calculus.

For an oriented link diagram ``L`` with ``n`` components, the multivariable
Alexander polynomial ``Δ_L(t₁, …, tₙ)`` is the order of the Alexander module of
the complement, computed here from a planar-diagram (PD) code through:

1. **Wirtinger arcs.**  An arc is a maximal piece of the diagram running between
   two consecutive *under*-crossings (it passes freely over any number of
   over-crossings).  A link diagram with ``c`` crossings has exactly ``c`` arcs.
   Arcs are recovered by union-find: the two *over*-strand edges ``b, d`` of
   every crossing are merged (the over-strand is unbroken); the *under*-strand
   edges ``a, c`` are not.
2. **Colouring.**  Each arc carries the variable ``t_γ`` of the component it
   belongs to.  Components are the orbits of the strands (union ``a–c`` and
   ``b–d`` at every crossing).
3. **Wirtinger relators.**  Each crossing gives the relator
   ``x_out = x_over^{±1} · x_in · x_over^{∓1}`` (``+`` for a positive crossing).
4. **Fox calculus.**  The Alexander matrix is ``A[r][j] = φ(∂rᵣ/∂xⱼ)`` where
   ``φ`` abelianises ``x_j ↦ t_{colour(j)}``.  Deleting one column (colour ``γ₀``)
   and one redundant row leaves a ``(c−1)×(c−1)`` minor with determinant ``D``.
   The Alexander polynomial is, up to units ``±t₁^{a₁}…tₙ^{aₙ}``,

       Δ_L = D                       for a knot (n = 1),
       Δ_L = D / (t_{γ₀} − 1)        for a link (n ≥ 2).

Everything is exact integer arithmetic over the ``n``-variable Laurent ring
``ℤ[t₁^{±1}, …, tₙ^{±1}]`` (polynomials stored as ``{exponent_tuple: coeff}``);
no dependencies.  The determinant is a memoised Laplace expansion — intended
for the small diagrams of the knot/link tables, not large-scale computation.

Conventions
-----------
The result is normalised to a canonical representative of its unit class: every
variable is shifted so its minimum exponent is ``0``, and the sign is fixed so
the lexicographically-smallest monomial has a positive coefficient.  The split
link (and the multi-component unlink) gives ``Δ = 0`` (the empty dict).
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

# A polynomial in ℤ[t₁^±,…,tₙ^±] is a dict {exponent_tuple: int_coeff}; the
# zero polynomial is the empty dict.
Poly = dict


__all__ = ["multivariable_alexander"]


# ---------------------------------------------------------------------------
# n-variable Laurent polynomial arithmetic (sparse dicts)
# ---------------------------------------------------------------------------


def _p_add(left: Poly, right: Poly) -> Poly:
    result = dict(left)
    for exp, coeff in right.items():
        total = result.get(exp, 0) + coeff
        if total:
            result[exp] = total
        else:
            result.pop(exp, None)
    return result


def _p_sub(left: Poly, right: Poly) -> Poly:
    result = dict(left)
    for exp, coeff in right.items():
        total = result.get(exp, 0) - coeff
        if total:
            result[exp] = total
        else:
            result.pop(exp, None)
    return result


def _p_mul(left: Poly, right: Poly) -> Poly:
    result: Poly = {}
    for exp_l, coeff_l in left.items():
        for exp_r, coeff_r in right.items():
            exp = tuple(a + b for a, b in zip(exp_l, exp_r))
            total = result.get(exp, 0) + coeff_l * coeff_r
            if total:
                result[exp] = total
            else:
                result.pop(exp, None)
    return result


def _p_one(n_vars: int) -> Poly:
    return {(0,) * n_vars: 1}


# ---------------------------------------------------------------------------
# Union-find
# ---------------------------------------------------------------------------


def _find(parent: dict, x: Any) -> Any:
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def _union(parent: dict, x: Any, y: Any) -> None:
    root_x, root_y = _find(parent, x), _find(parent, y)
    if root_x != root_y:
        parent[root_x] = root_y


# ---------------------------------------------------------------------------
# Wirtinger data from a PD code
# ---------------------------------------------------------------------------


def _over_strand_directions(
    crossings: list[tuple[Any, Any, Any, Any]],
) -> list[int]:
    """Return, per crossing, ``+1`` if the over-strand is oriented ``b → d`` and
    ``-1`` if ``d → b``.

    The orientation is intrinsic to the diagram (recovered by tracing each
    component forward from an under-strand) — it does **not** rely on a supplied
    crossing-sign array, which may be chosen only for the writhe.  At a crossing
    ``(a, b, c, d)`` the understrand runs ``a → c`` (edge ``a`` enters, edge
    ``c`` exits), and the over-strand passes straight through ``b ↔ d``.  Tracing
    forward (exit each crossing opposite the entry) orients every edge.
    """

    occurrences: dict = defaultdict(list)
    for index, (a, b, c, d) in enumerate(crossings):
        for position, label in enumerate((a, b, c, d)):
            occurrences[label].append((index, position))

    # edge_into[label] = crossing the edge points into (its head).
    edge_into: dict[Any, int] = {}
    visited_exits: set[tuple[int, int]] = set()
    n = len(crossings)
    for seed in range(n):
        # Position 2 (edge c) is the outgoing under-edge → the forward direction.
        index, position = seed, 2
        while (index, position) not in visited_exits:
            visited_exits.add((index, position))
            label = crossings[index][position]
            first, second = occurrences[label]
            other = second if first == (index, position) else first
            next_index, entry = other
            edge_into[label] = next_index  # oriented (index) → (next_index)
            index, position = next_index, (entry + 2) % 4

    directions: list[int] = []
    for index, (a, b, c, d) in enumerate(crossings):
        # over-strand is b → d iff edge b enters this crossing (head == index).
        directions.append(1 if edge_into.get(b) == index else -1)
    return directions


def _wirtinger_data(
    crossings: list[tuple[Any, Any, Any, Any]],
) -> tuple[int, int, list[int], list[list[tuple[int, int]]]]:
    """Return ``(n_arcs, n_vars, colour_of_arc, relators)``.

    ``relators[k]`` is a list of ``(arc_index, ±1)`` signed letters for the
    Wirtinger relator of crossing ``k``.
    """

    labels = sorted({label for crossing in crossings for label in crossing}, key=repr)

    component_parent = {label: label for label in labels}
    arc_parent = {label: label for label in labels}
    for (a, b, c, d) in crossings:
        _union(component_parent, a, c)  # under-strand continues a → c
        _union(component_parent, b, d)  # over-strand continues b → d
        _union(arc_parent, b, d)        # over-strand is one unbroken arc

    arc_members: dict = defaultdict(list)
    component_members: dict = defaultdict(list)
    for label in labels:
        arc_members[_find(arc_parent, label)].append(label)
        component_members[_find(component_parent, label)].append(label)

    arc_roots = sorted(arc_members, key=lambda root: min(map(repr, arc_members[root])))
    component_roots = sorted(
        component_members, key=lambda root: min(map(repr, component_members[root]))
    )
    arc_index = {root: i for i, root in enumerate(arc_roots)}
    colour_index = {root: i for i, root in enumerate(component_roots)}

    n_arcs = len(arc_roots)
    n_vars = len(component_roots)

    def arc_of(label: Any) -> int:
        return arc_index[_find(arc_parent, label)]

    def colour_of(label: Any) -> int:
        return colour_index[_find(component_parent, label)]

    colour_of_arc = [0] * n_arcs
    for root, idx in arc_index.items():
        colour_of_arc[idx] = colour_of(arc_members[root][0])

    over_directions = _over_strand_directions(crossings)
    relators: list[list[tuple[int, int]]] = []
    for (a, b, c, d), over_dir in zip(crossings, over_directions):
        under_in = arc_of(a)
        under_out = arc_of(c)
        over = arc_of(b)  # == arc_of(d)
        # x_out = x_over^{ε} x_in x_over^{-ε}, ε = +1 for an over-strand b → d
        # (right-to-left across the under-strand), −1 for d → b.
        if over_dir > 0:
            relator = [(under_out, -1), (over, 1), (under_in, 1), (over, -1)]
        else:
            relator = [(under_out, -1), (over, -1), (under_in, 1), (over, 1)]
        relators.append(relator)

    return n_arcs, n_vars, colour_of_arc, relators


# ---------------------------------------------------------------------------
# Fox-derivative Alexander matrix
# ---------------------------------------------------------------------------


def _fox_matrix(
    relators: list[list[tuple[int, int]]],
    colour_of_arc: list[int],
    n_arcs: int,
    n_vars: int,
) -> list[list[Poly]]:
    """Return the abelianised Fox-derivative matrix ``A[r][j] = φ(∂rᵣ/∂xⱼ)``."""

    matrix: list[list[Poly]] = [[{} for _ in range(n_arcs)] for _ in relators]
    for r, relator in enumerate(relators):
        prefix = [0] * n_vars  # exponent vector of the abelianised prefix
        row = matrix[r]
        for arc, sign in relator:
            colour = colour_of_arc[arc]
            if sign == 1:
                exponent = tuple(prefix)
                row[arc][exponent] = row[arc].get(exponent, 0) + 1
            else:
                shifted = list(prefix)
                shifted[colour] -= 1
                exponent = tuple(shifted)
                row[arc][exponent] = row[arc].get(exponent, 0) - 1
            prefix[colour] += sign
        for arc in range(n_arcs):
            row[arc] = {exp: c for exp, c in row[arc].items() if c != 0}
    return matrix


# ---------------------------------------------------------------------------
# Determinant (memoised Laplace expansion over the Laurent ring)
# ---------------------------------------------------------------------------


def _determinant(matrix: list[list[Poly]], n_vars: int) -> Poly:
    size = len(matrix)
    if size == 0:
        return _p_one(n_vars)

    memo: dict[tuple[int, ...], Poly] = {}

    def expand(row: int, columns: tuple[int, ...]) -> Poly:
        if not columns:
            return _p_one(n_vars)
        cached = memo.get(columns)
        if cached is not None:
            return cached
        total: Poly = {}
        for position, column in enumerate(columns):
            entry = matrix[row][column]
            if not entry:
                continue
            remaining = columns[:position] + columns[position + 1 :]
            term = _p_mul(entry, expand(row + 1, remaining))
            total = _p_add(total, term) if position % 2 == 0 else _p_sub(total, term)
        memo[columns] = total
        return total

    return expand(0, tuple(range(size)))


def _minor(
    matrix: list[list[Poly]],
    deleted_row: int,
    deleted_column: int,
    n_vars: int,
) -> Poly:
    rows = [i for i in range(len(matrix)) if i != deleted_row]
    columns = [j for j in range(len(matrix[0])) if j != deleted_column]
    submatrix = [[matrix[i][j] for j in columns] for i in rows]
    return _determinant(submatrix, n_vars)


# ---------------------------------------------------------------------------
# Exact division by (t_k − 1) and unit normalisation
# ---------------------------------------------------------------------------


def _divide_univariate_by_t_minus_one(uni: dict[int, int]) -> dict[int, int]:
    """Exactly divide a single-variable Laurent polynomial by ``(t − 1)``."""

    uni = {exp: c for exp, c in uni.items() if c != 0}
    if not uni:
        return {}
    low, high = min(uni), max(uni)
    degree = high - low
    if degree == 0:
        return {}  # a nonzero constant is not divisible — caller guarantees it won't occur
    a = [uni.get(low + i, 0) for i in range(degree + 1)]
    b = [0] * degree
    b[degree - 1] = a[degree]
    for i in range(degree - 1, 0, -1):
        b[i - 1] = a[i] + b[i]
    return {i + low: b[i] for i in range(degree) if b[i] != 0}


def _divide_by_variable_minus_one(poly: Poly, k: int, n_vars: int) -> Poly:
    """Exactly divide ``poly`` by ``(t_k − 1)`` in ``ℤ[t₁^±,…,tₙ^±]``.

    Since ``(t_k − 1)`` involves only variable ``k``, the quotient splits over
    the other variables: group by the other exponents and divide each
    single-variable slice by ``(t − 1)``.
    """

    groups: dict[tuple[int, ...], dict[int, int]] = defaultdict(dict)
    for exp, coeff in poly.items():
        rest = exp[:k] + exp[k + 1 :]
        groups[rest][exp[k]] = groups[rest].get(exp[k], 0) + coeff

    result: Poly = {}
    for rest, slice_poly in groups.items():
        quotient = _divide_univariate_by_t_minus_one(slice_poly)
        for power, coeff in quotient.items():
            full = rest[:k] + (power,) + rest[k:]
            result[full] = result.get(full, 0) + coeff
    return {exp: c for exp, c in result.items() if c != 0}


def _normalise(poly: Poly, n_vars: int) -> Poly:
    """Return the canonical representative of ``poly``'s unit class.

    Shift each variable so its minimum exponent is ``0``, then fix the sign so
    the lexicographically-smallest monomial has a positive coefficient.
    """

    poly = {exp: c for exp, c in poly.items() if c != 0}
    if not poly:
        return {}
    minima = [min(exp[i] for exp in poly) for i in range(n_vars)]
    shifted = {
        tuple(exp[i] - minima[i] for i in range(n_vars)): c for exp, c in poly.items()
    }
    smallest = min(shifted)
    if shifted[smallest] < 0:
        shifted = {exp: -c for exp, c in shifted.items()}
    return shifted


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def multivariable_alexander(link: Any) -> dict[tuple[int, ...], int]:
    """Return the multivariable Alexander polynomial of a link diagram.

    Parameters
    ----------
    link:
        A :class:`~pytop.knot_invariants.LinkDiagram` (or any object exposing
        ``crossings``, ``signs`` and ``n_components``).

    Returns
    -------
    dict[tuple[int, ...], int]
        Coefficients of ``Δ_L(t₁, …, tₙ)`` keyed by exponent tuples of length
        ``n`` (the number of components), normalised up to units.  A knot gives
        length-1 tuples; the unknot gives ``{(0,): 1}``; a split link / unlink
        gives the empty dict (``Δ = 0``).

    Notes
    -----
    Exact, dependency-free, and pure Python.  The determinant is exponential in
    the crossing number in the worst case; intended for small tabulated
    diagrams.
    """

    crossings = [tuple(crossing) for crossing in link.crossings]
    n_components = int(getattr(link, "n_components", 1))

    if not crossings:
        # No crossings: an n-component unlink. Unknot → 1, split link → 0.
        return {(0,): 1} if n_components <= 1 else {}

    n_arcs, n_vars, colour_of_arc, relators = _wirtinger_data(crossings)
    if n_arcs != len(relators):
        raise ValueError(
            "non-standard diagram: number of Wirtinger arcs "
            f"({n_arcs}) ≠ number of crossings ({len(relators)}); "
            "every component must pass under at least one crossing."
        )

    matrix = _fox_matrix(relators, colour_of_arc, n_arcs, n_vars)

    # Delete column 0 (colour γ₀) and one redundant row; the minors are equal up
    # to units, so take the first non-vanishing one.
    gamma0 = colour_of_arc[0]
    determinant: Poly = {}
    for deleted_row in range(len(matrix)):
        determinant = _minor(matrix, deleted_row, 0, n_vars)
        if determinant:
            break

    if not determinant:
        return {}  # Δ = 0 (split link)

    if n_vars == 1:
        result = determinant
    else:
        result = _divide_by_variable_minus_one(determinant, gamma0, n_vars)

    return _normalise(result, n_vars)
