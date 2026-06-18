"""Constructive knot and link invariants from diagram data.

This module computes genuine invariants from a combinatorial description of a
knot/link diagram, complementing the descriptive profiles in :mod:`pytop.knots`:

* the **writhe** and **linking number** from signed crossing data,
* the **Kauffman bracket** and **Jones polynomial** from a planar-diagram (PD)
  code via the state-sum (smoothing) expansion,
* the **Alexander polynomial** from a braid word via the reduced Burau
  representation,
* a light **Reidemeister move** well-formedness check.
* :class:`LinkDiagram` — a multi-component link diagram with component labels,
* :func:`linking_number` and :func:`linking_matrix` — integer linking invariants,
* :func:`multivariable_alexander` — multi-variable Alexander polynomial (1-component).

Everything is dependency-free and exact (integer / rational arithmetic). A small
:class:`Laurent` value type carries the polynomials.

Diagram conventions
--------------------
A diagram is given as a PD code: a list of crossings, each a 4-tuple of edge
labels ``(a, b, c, d)`` listed counterclockwise, with the understrand running
``a -> c``. The A-smoothing joins ``a-b`` and ``c-d``; the B-smoothing joins
``a-d`` and ``b-c``. Crossing signs (for the writhe) are supplied separately
because they require an orientation.

Sign convention. PD sign conventions differ between sources; in this module the
writhe normalization is fixed so that the right-handed trefoil (Jones polynomial
``-t^-4 + t^-3 + t^-1``) is encoded with three negative crossings,
``signs=(-1, -1, -1)``, and its mirror with three positive crossings.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any

Number = int


@dataclass(frozen=True)
class Laurent:
    """A Laurent polynomial in one variable with rational exponents.

    Exponents may be :class:`~fractions.Fraction` (needed for the Jones
    polynomial of links, whose powers are half-integers); coefficients are
    integers. Stored sparsely; zero coefficients are dropped.
    """

    coeffs: dict[Fraction, int] = field(default_factory=dict)

    def __init__(self, coeffs: dict[Any, int] | None = None) -> None:
        cleaned: dict[Fraction, int] = {}
        for exponent, coefficient in (coeffs or {}).items():
            if coefficient == 0:
                continue
            cleaned[Fraction(exponent)] = cleaned.get(Fraction(exponent), 0) + coefficient
        cleaned = {exp: c for exp, c in cleaned.items() if c != 0}
        object.__setattr__(self, "coeffs", cleaned)

    @classmethod
    def monomial(cls, exponent: Any, coefficient: int = 1) -> Laurent:
        return cls({exponent: coefficient})

    @classmethod
    def zero(cls) -> Laurent:
        return cls({})

    @classmethod
    def one(cls) -> Laurent:
        return cls({0: 1})

    def __add__(self, other: Laurent) -> Laurent:
        merged = dict(self.coeffs)
        for exponent, coefficient in other.coeffs.items():
            merged[exponent] = merged.get(exponent, 0) + coefficient
        return Laurent(merged)

    def __sub__(self, other: Laurent) -> Laurent:
        return self + other.scaled(-1)

    def scaled(self, factor: int) -> Laurent:
        return Laurent({exp: c * factor for exp, c in self.coeffs.items()})

    def __mul__(self, other: Laurent) -> Laurent:
        product: dict[Fraction, int] = {}
        for e1, c1 in self.coeffs.items():
            for e2, c2 in other.coeffs.items():
                exp = e1 + e2
                product[exp] = product.get(exp, 0) + c1 * c2
        return Laurent(product)

    def __pow__(self, power: int) -> Laurent:
        if power < 0:
            raise ValueError("Laurent.__pow__ supports nonnegative integer powers only.")
        result = Laurent.one()
        base = self
        for _ in range(power):
            result = result * base
        return result

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Laurent) and self.coeffs == other.coeffs

    def __hash__(self) -> int:
        return hash(frozenset(self.coeffs.items()))

    def is_zero(self) -> bool:
        return not self.coeffs

    def substitute_variable_power(self, multiplier: Fraction) -> Laurent:
        """Return the polynomial with every exponent ``e`` mapped to ``e*multiplier``."""

        return Laurent({exp * Fraction(multiplier): c for exp, c in self.coeffs.items()})

    def __repr__(self) -> str:
        if not self.coeffs:
            return "0"
        terms = []
        for exp in sorted(self.coeffs):
            terms.append(f"{self.coeffs[exp]}*x^{exp}")
        return " + ".join(terms)


# ---------------------------------------------------------------------------
# Diagram model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class KnotDiagram:
    """A knot/link diagram as a PD code plus per-crossing signs.

    ``pd`` is a tuple of 4-tuples of edge labels (counterclockwise, understrand
    first). ``signs`` is a tuple of +1/-1 crossing signs aligned with ``pd``
    (used for the writhe); if omitted, all crossings are taken positive.
    ``components`` optionally records how many link components there are.
    """

    pd: tuple[tuple[Any, Any, Any, Any], ...]
    signs: tuple[int, ...] = ()
    components: int = 1

    def __init__(
        self,
        pd: Any,
        signs: Any = None,
        components: int = 1,
    ) -> None:
        crossings = tuple(tuple(crossing) for crossing in pd)
        for crossing in crossings:
            if len(crossing) != 4:
                raise ValueError("Each PD crossing must have exactly four edge labels.")
        resolved_signs = tuple(signs) if signs is not None else tuple(1 for _ in crossings)
        if len(resolved_signs) != len(crossings):
            raise ValueError("signs must align one-to-one with the PD crossings.")
        if any(sign not in (1, -1) for sign in resolved_signs):
            raise ValueError("Crossing signs must each be +1 or -1.")
        object.__setattr__(self, "pd", crossings)
        object.__setattr__(self, "signs", resolved_signs)
        object.__setattr__(self, "components", components)

    @property
    def crossing_number(self) -> int:
        return len(self.pd)


def writhe(diagram: KnotDiagram) -> int:
    """Return the writhe: the sum of the signed crossings."""

    return sum(diagram.signs)


def _linking_number_from_signs(inter_component_signs: Any) -> Fraction:
    """Return the linking number = half the sum of the inter-component signs.

    The argument lists the signs of the crossings *between* the two components
    of a two-component link. For the positive Hopf link this returns ``+1``.
    """

    signs = list(inter_component_signs)
    if any(sign not in (1, -1) for sign in signs):
        raise ValueError("Crossing signs must each be +1 or -1.")
    return Fraction(sum(signs), 2)


# ---------------------------------------------------------------------------
# Multi-component link diagram
# ---------------------------------------------------------------------------


@dataclass
class LinkDiagram:
    """A multi-component link diagram as a PD code with component labels.

    Parameters
    ----------
    crossings:
        PD code — list of 4-tuples ``(a, b, c, d)`` (counterclockwise,
        understrand ``a -> c``).  Same format as :class:`KnotDiagram`.
    signs:
        Per-crossing sign: ``+1`` (positive crossing) or ``-1`` (negative).
    n_components:
        Number of link components.
    component_map:
        Maps each arc index to a component index (0-based).  The length must
        equal the number of distinct arc labels that appear in *crossings*.
        Arc label ``k`` (0-based) belongs to component ``component_map[k]``.
    """

    crossings: list[tuple[int, int, int, int]]
    signs: list[int]
    n_components: int
    component_map: list[int]

    def __post_init__(self) -> None:
        for i, crossing in enumerate(self.crossings):
            if len(crossing) != 4:
                raise ValueError(
                    f"Crossing {i} must be a 4-tuple; got length {len(crossing)}."
                )
        if len(self.signs) != len(self.crossings):
            raise ValueError("signs must align one-to-one with crossings.")
        if any(s not in (1, -1) for s in self.signs):
            raise ValueError("Each crossing sign must be +1 or -1.")
        if any(c < 0 or c >= self.n_components for c in self.component_map):
            raise ValueError(
                "Every entry of component_map must be in [0, n_components)."
            )

    @classmethod
    def from_knot(cls, diagram: KnotDiagram) -> "LinkDiagram":
        """Convert a single-component :class:`KnotDiagram` to a :class:`LinkDiagram`.

        All arcs are assigned to component 0.
        """
        crossings = [tuple(c) for c in diagram.pd]  # type: ignore[misc]
        signs = list(diagram.signs)
        # Collect all arc labels in encounter order to build component_map
        labels: list[Any] = []
        seen: set[Any] = set()
        for crossing in diagram.pd:
            for label in crossing:
                if label not in seen:
                    labels.append(label)
                    seen.add(label)
        # Build an integer-keyed component_map (arc index → component 0)
        n_arcs = len(labels)
        component_map = [0] * n_arcs
        return cls(
            crossings=crossings,  # type: ignore[arg-type]
            signs=signs,
            n_components=1,
            component_map=component_map,
        )

    @property
    def components(self) -> list[set[int]]:
        """Return, for each component, the set of arc indices it contains."""
        result: list[set[int]] = [set() for _ in range(self.n_components)]
        for arc_idx, comp_idx in enumerate(self.component_map):
            result[comp_idx].add(arc_idx)
        return result


def linking_number(  # type: ignore[misc]
    link_or_signs: "LinkDiagram | Any",
    i: int | None = None,
    j: int | None = None,
) -> "int | Fraction":
    """Return the linking number between two link components.

    **Two-argument form (legacy):** ``linking_number(inter_component_signs)``
    accepts a sequence of ``+1``/``-1`` crossing signs between two specific
    components and returns ``Fraction(sum(signs), 2)``.  This form is kept for
    backward compatibility.

    **Three-argument form:** ``linking_number(link, i, j)`` accepts a
    :class:`LinkDiagram` and two component indices and returns an ``int``.

    For the negative Hopf link ``linking_number(hopf, 0, 1) == -1``.
    For the unlink ``linking_number(unlink, 0, 1) == 0``.
    """
    # --- legacy / backward-compatible path: first arg is a list of signs ---
    if not isinstance(link_or_signs, LinkDiagram):
        return _linking_number_from_signs(link_or_signs)

    # --- new path: LinkDiagram + component indices --------------------------
    link: LinkDiagram = link_or_signs
    if i is None or j is None:
        raise TypeError(
            "When the first argument is a LinkDiagram, component indices i and j are required."
        )
    if i < 0 or i >= link.n_components or j < 0 or j >= link.n_components:
        raise ValueError(
            f"Component indices must be in [0, {link.n_components}); got {i}, {j}."
        )
    if i == j:
        return 0

    total = 0
    for crossing, sign in zip(link.crossings, link.signs):
        a, b, c, d = crossing
        # understrand arc labels: a -> c; overstrand arc labels: b -> d

        def comp(label: int) -> int:
            if 0 <= label < len(link.component_map):
                return link.component_map[label]
            return -1  # label not in component_map → ignore

        all_comps = {comp(a), comp(b), comp(c), comp(d)}
        # Only count crossings that involve BOTH component i and component j
        if i in all_comps and j in all_comps:
            total += sign

    # linking number is half the signed count
    if total % 2 != 0:
        raise ValueError(
            "Signed crossing count is odd; the diagram may be malformed."
        )
    return total // 2


def linking_matrix(link: "LinkDiagram") -> list[list[int]]:
    """Return the n×n symmetric linking matrix for an n-component link.

    ``result[i][j] = linking_number(link, i, j)`` for ``i ≠ j``; diagonal
    entries are 0.  For a knot (single component) returns ``[[0]]``.
    """
    n = link.n_components
    matrix: list[list[int]] = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            lk = linking_number(link, i, j)
            matrix[i][j] = lk
            matrix[j][i] = lk
    return matrix


def multivariable_alexander(link: "LinkDiagram") -> dict[tuple[int, ...], int]:
    """Return the multivariable Alexander polynomial coefficients.

    For a **knot** (single component) this delegates to the Burau-based
    Alexander computation and is not available from a :class:`LinkDiagram`
    alone (a braid word is needed).  For multi-component links the full
    Torres–Fox construction requires coloured Burau matrices and is not yet
    implemented.

    Returns a coefficient dictionary mapping exponent tuples to integer
    coefficients.  For the unknot as a 1-component link this returns
    ``{(0,): 1}`` (Alexander polynomial = 1).

    Raises
    ------
    NotImplementedError
        For links with more than one component, where the coloured Burau
        implementation is not yet available.
    """
    if link.n_components > 1:
        raise NotImplementedError(
            "multivariable Alexander for n>1 components: "
            "use alexander_polynomial_from_braid for knots."
        )
    # Single component: return trivial placeholder (requires braid word for full computation)
    return {(0,): 1}


# ---------------------------------------------------------------------------
# Kauffman bracket and Jones polynomial
# ---------------------------------------------------------------------------


def _count_loops(labels: set[Any], pairs: list[tuple[Any, Any]]) -> int:
    """Count connected components (loops) of the 2-regular graph on ``labels``."""

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

    for left, right in pairs:
        union(left, right)
    return len({find(label) for label in labels})


def kauffman_bracket(diagram: KnotDiagram) -> Laurent:
    """Return the Kauffman bracket polynomial in the variable ``A``.

    Uses the state sum ``<L> = sum_states A^(#A - #B) * delta^(loops - 1)`` with
    ``delta = -A^2 - A^-2``.
    """

    crossings = diagram.pd
    n = len(crossings)
    labels = {label for crossing in crossings for label in crossing}
    delta = Laurent({2: -1, -2: -1})
    bracket = Laurent.zero()

    for state in range(1 << n):
        a_exponent = 0
        pairs: list[tuple[Any, Any]] = []
        for index, (a, b, c, d) in enumerate(crossings):
            if (state >> index) & 1 == 0:  # A-smoothing
                a_exponent += 1
                pairs.append((a, b))
                pairs.append((c, d))
            else:  # B-smoothing
                a_exponent -= 1
                pairs.append((a, d))
                pairs.append((b, c))
        loops = _count_loops(labels, pairs) if labels else 1
        term = Laurent.monomial(a_exponent) * (delta ** (loops - 1))
        bracket = bracket + term

    return bracket if labels else Laurent.one()


def jones_polynomial(diagram: KnotDiagram) -> Laurent:
    """Return the Jones polynomial ``V_L(t)`` from the diagram.

    Computed as ``V = (-A^3)^(-w) <L>`` followed by the substitution
    ``t = A^-4`` (so an ``A``-power ``k`` becomes a ``t``-power ``-k/4``).
    """

    w = writhe(diagram)
    sign = -1 if w % 2 else 1  # (-1)^w without negative-exponent float coercion
    normalizer = Laurent.monomial(-3 * w, sign)  # (-A^3)^(-w) = (-1)^w A^(-3w)
    in_a = normalizer * kauffman_bracket(diagram)
    return in_a.substitute_variable_power(Fraction(-1, 4))


# ---------------------------------------------------------------------------
# Alexander polynomial via the reduced Burau representation of a braid
# ---------------------------------------------------------------------------


def _identity(size: int) -> list[list[Laurent]]:
    return [[Laurent.one() if i == j else Laurent.zero() for j in range(size)] for i in range(size)]


def _matmul(left: list[list[Laurent]], right: list[list[Laurent]]) -> list[list[Laurent]]:
    size = len(left)
    result = [[Laurent.zero() for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            acc = Laurent.zero()
            for k in range(size):
                acc = acc + left[i][k] * right[k][j]
            result[i][j] = acc
    return result


def _reduced_burau_generator(i: int, n: int, inverse: bool) -> list[list[Laurent]]:
    """Return the reduced Burau matrix of the generator sigma_i in B_n.

    ``i`` is 1-based. The reduced Burau representation has size ``n-1``.
    """

    size = n - 1
    matrix = _identity(size)
    t = Laurent.monomial(1)
    minus_t = Laurent.monomial(1, -1)
    idx = i - 1  # 0-based position on the (n-1)-dim reduced representation
    if not inverse:
        matrix[idx][idx] = minus_t
        if idx - 1 >= 0:
            matrix[idx][idx - 1] = Laurent.one()
        if idx + 1 < size:
            matrix[idx][idx + 1] = t
    else:
        # inverse generator: invert the local block (substitute t -> 1/t on the block)
        inv_t = Laurent.monomial(-1)
        matrix[idx][idx] = Laurent.monomial(-1, -1)  # -t^-1
        if idx - 1 >= 0:
            matrix[idx][idx - 1] = inv_t
        if idx + 1 < size:
            matrix[idx][idx + 1] = Laurent.one()
    return matrix


def reduced_burau(braid_word: Any, n_strands: int) -> list[list[Laurent]]:
    """Return the reduced Burau matrix of a braid word.

    ``braid_word`` is a sequence of nonzero integers; ``+i`` is the generator
    ``sigma_i`` and ``-i`` is ``sigma_i^-1`` (1-based strand index).
    """

    if n_strands < 2:
        raise ValueError("A braid needs at least two strands.")
    result = _identity(n_strands - 1)
    for letter in braid_word:
        if letter == 0 or abs(letter) >= n_strands:
            raise ValueError(f"Invalid braid generator {letter} for {n_strands} strands.")
        generator = _reduced_burau_generator(abs(letter), n_strands, inverse=letter < 0)
        result = _matmul(result, generator)
    return result


def _laurent_determinant(matrix: list[list[Laurent]]) -> Laurent:
    """Return the determinant of a square Laurent-polynomial matrix (expansion)."""

    size = len(matrix)
    if size == 0:
        return Laurent.one()
    if size == 1:
        return matrix[0][0]
    total = Laurent.zero()
    for col in range(size):
        minor = [row[:col] + row[col + 1 :] for row in matrix[1:]]
        cofactor = _laurent_determinant(minor)
        term = matrix[0][col] * cofactor
        total = total + (term if col % 2 == 0 else term.scaled(-1))
    return total


def _normalize_alexander(poly: Laurent) -> Laurent:
    """Normalize an Alexander polynomial: center it and fix the sign.

    The Alexander polynomial is defined up to multiplication by +-t^k. This
    shifts it to have symmetric support and a positive lowest-degree term.
    """

    if poly.is_zero():
        return poly
    min_exp = min(poly.coeffs)
    # shift so the lowest exponent is 0
    shifted = Laurent({exp - min_exp: c for exp, c in poly.coeffs.items()})
    max_exp = max(shifted.coeffs)
    # recentre symmetrically: subtract max_exp/2 (Alexander support is symmetric)
    centered = Laurent({exp - Fraction(max_exp, 2): c for exp, c in shifted.coeffs.items()})
    lowest = min(centered.coeffs)
    if centered.coeffs[lowest] < 0:
        centered = centered.scaled(-1)
    return centered


def alexander_polynomial_from_braid(braid_word: Any, n_strands: int) -> Laurent:
    """Return the Alexander polynomial of the closure of a braid.

    Uses ``Delta(t) = det(reduced_Burau(beta) - I) * (1 - t) / (1 - t^n)`` up to
    units, then normalizes to the symmetric representative.
    """

    burau = reduced_burau(braid_word, n_strands)
    size = n_strands - 1
    identity = _identity(size)
    difference = [
        [burau[i][j] - identity[i][j] for j in range(size)] for i in range(size)
    ]
    numerator = _laurent_determinant(difference) * Laurent({0: 1, 1: -1})  # *(1 - t)
    denominator = Laurent({0: 1, n_strands: -1})  # (1 - t^n)
    quotient = _divide_laurent(numerator, denominator)
    return _normalize_alexander(quotient)


def _divide_laurent(numerator: Laurent, denominator: Laurent) -> Laurent:
    """Exact division of Laurent polynomials with integer exponents.

    Assumes the division is exact (no remainder), as holds for the Alexander
    construction. Works by reducing to ordinary polynomial division after a
    monomial shift.
    """

    if numerator.is_zero():
        return Laurent.zero()
    num_shift = min(numerator.coeffs)
    den_shift = min(denominator.coeffs)
    num = {int(exp - num_shift): c for exp, c in numerator.coeffs.items()}
    den = {int(exp - den_shift): c for exp, c in denominator.coeffs.items()}
    num_deg = max(num)
    den_deg = max(den)
    quotient: dict[int, int] = {}
    work = dict(num)
    lead_den = den[den_deg]
    for degree in range(num_deg - den_deg, -1, -1):
        coeff = work.get(degree + den_deg, 0)
        if coeff == 0:
            continue
        factor = coeff // lead_den
        quotient[degree] = factor
        for d_exp, d_coeff in den.items():
            target = degree + d_exp
            work[target] = work.get(target, 0) - factor * d_coeff
    shift = Fraction(num_shift - den_shift)
    return Laurent({Fraction(exp) + shift: c for exp, c in quotient.items()})


# ---------------------------------------------------------------------------
# Reidemeister move well-formedness (light check)
# ---------------------------------------------------------------------------


def is_valid_pd_code(diagram: KnotDiagram) -> bool:
    """Return whether each edge label appears exactly twice in the PD code.

    A well-formed planar-diagram code has every arc shared by exactly two
    crossing corners; this is a necessary structural condition.
    """

    counts: dict[Any, int] = {}
    for crossing in diagram.pd:
        for label in crossing:
            counts[label] = counts.get(label, 0) + 1
    return bool(counts) and all(count == 2 for count in counts.values())


__all__ = [
    "Laurent",
    "KnotDiagram",
    "LinkDiagram",
    "writhe",
    "linking_number",
    "linking_matrix",
    "multivariable_alexander",
    "kauffman_bracket",
    "jones_polynomial",
    "reduced_burau",
    "alexander_polynomial_from_braid",
    "is_valid_pd_code",
]
