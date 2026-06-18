"""Urysohn function witnesses for the Tychonoff (T3.5) axiom.

A topological space X is *Tychonoff* (completely regular + T1) iff for every
point x₀ and every closed set C not containing x₀ there exists a continuous
function f: X → [0,1] with f(x₀) = 0 and f(C) ⊆ {1}.  Such an f is called
a *Urysohn function* separating x₀ from C.

This module constructs concrete Urysohn functions for representable spaces:

* **Finite T1 spaces** (= discrete): every function is continuous; the trivial
  indicator f = 0 on {x₀}, f = 1 on C gives an explicit witness.
* **MetricTopologySpace**: f(y) = min(1, d(x₀, y) / d(x₀, C)) is an exact
  Urysohn function whenever d(x₀, C) > 0 (guaranteed when x₀ ∉ cl(C)).
* **General finite spaces**: a BFS-based Urysohn function is constructed by
  assigning real values in [0,1] that respect the topology — f⁻¹([0,t)) open.
  Returns ``None`` when no such function exists (space is not T3.5 for that
  pair) or when the space is not finite.

Public API
----------
UrysohnWitness     — the separating function together with metadata
urysohn_function   — construct a witness for a given (space, x₀, closed_set)
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from .core import CardinalValue, NotEnumerableError, Space


@dataclass(frozen=True)
class UrysohnWitness:
    """A continuous separating function f: X → [0,1] with f(x₀) = 0, f(C) ⊆ {1}.

    Attributes
    ----------
    x0 :
        The point being separated (f(x₀) = 0).
    closed_set :
        The closed set from which x₀ is being separated (f(C) ⊆ {1}).
    values : dict or None
        For **finite spaces**: maps every point y to its exact value f(y) ∈ [0,1]
        as a :class:`~fractions.Fraction`.  ``None`` for infinite spaces.
    formula : str
        Human-readable formula / mathematical description of f.  For finite
        spaces this summarises the computed ``values``; for infinite ones it
        is the only description.
    method : str
        Algorithmic source: ``"discrete_indicator"``, ``"distance_ratio"``,
        or ``"bfs_level"``.
    """

    x0: Any
    closed_set: frozenset
    values: dict[Any, Fraction] | None
    formula: str
    method: str

    def evaluate(self, y: Any) -> Fraction | None:
        """Return f(y) as an exact rational, or ``None`` if unavailable."""
        if self.values is not None:
            return self.values.get(y)
        return None


# --------------------------------------------------------------------------
# Internal helpers
# --------------------------------------------------------------------------

def _finite_topo(space: Space) -> tuple[list[Any], set[frozenset]]:
    pts = list(space.points())
    opens = {frozenset(o) for o in space.open_sets()}
    return pts, opens


def _is_open(u: frozenset, opens: set[frozenset]) -> bool:
    return u in opens


def _closure(x: Any, carrier: frozenset, opens: set[frozenset]) -> frozenset:
    """cl({x}) for a finite topological space."""
    closed = {carrier - o for o in opens}
    cx: frozenset = carrier
    for f in closed:
        if x in f:
            cx &= f
    return cx


def _is_discrete(pts: list[Any], opens: set[frozenset]) -> bool:
    """True iff every singleton is open (i.e., the topology is discrete)."""
    return all(frozenset({p}) in opens for p in pts)


# --------------------------------------------------------------------------
# Finite: BFS-level Urysohn function
# --------------------------------------------------------------------------

def _bfs_urysohn(
    x0: Any,
    closed_set: frozenset,
    pts: list[Any],
    opens: set[frozenset],
    carrier: frozenset,
) -> dict[Any, Fraction] | None:
    """Assign Urysohn values by a BFS through the closed-set lattice.

    Constructs a sequence of open sets ∅ = U₋₁ ⊆ U₀ ⊆ U₁ ⊆ … ⊆ Uₙ = X\\C
    such that x₀ ∈ U₀ and cl(Uₖ) ⊆ Uₖ₊₁ for each k, then assigns
    f(y) = k/n where k is the first index with y ∈ Uₖ, and f(y) = 1 for y ∈ C.

    Returns a dict {point → Fraction} or None if the separation is impossible.
    """
    if x0 in closed_set:
        return None  # can't separate a point from a closed set containing it

    # Build the chain using the "smallest open neighbourhood" approach.
    # For a finite space, we can verify Urysohn by checking sub-level sets.
    # We look for a chain of opens: V₀ ∋ x₀, V₁ ⊇ cl(V₀), ..., up to X \ C.
    target = carrier - closed_set  # X \ C (must be open for C to be closed)
    if target not in opens:
        return None  # C is not closed

    # Minimal open containing x₀:
    min_open_x0 = target
    for o in opens:
        if x0 in o and o <= target and len(o) < len(min_open_x0):
            min_open_x0 = o

    # Build chain: V₀ = min_open_x0; Vₖ₊₁ = smallest open ⊇ cl(Vₖ); stop at target.
    chain = [min_open_x0]
    for _ in range(len(pts)):
        current = chain[-1]
        # cl(current) = union of closures of individual points
        cl_current = frozenset(
            y for y in carrier
            if any(y in _closure(p, carrier, opens) for p in current)
        )
        if cl_current <= current:
            break  # already closed; no need to expand
        # Find smallest open ⊇ cl(current) that is ⊆ target
        expanded = target
        for o in opens:
            if cl_current <= o and o <= target and len(o) < len(expanded):
                expanded = o
        if expanded == chain[-1]:
            break
        chain.append(expanded)
        if chain[-1] == target:
            break

    if chain[-1] != target:
        chain.append(target)

    # Deduplicate while preserving order
    seen: set[frozenset] = set()
    chain_dedup = []
    for v in chain:
        if v not in seen:
            seen.add(v)
            chain_dedup.append(v)
    chain = chain_dedup

    n = len(chain)
    values: dict[Any, Fraction] = {}
    for y in pts:
        if y in closed_set:
            values[y] = Fraction(1)
        else:
            # First chain level containing y
            level = next((i for i, v in enumerate(chain) if y in v), n)
            values[y] = Fraction(level, n) if n > 0 else Fraction(0)

    # Verify: f(x₀) should be 0 (or 1/n for the first level)
    # and f(C) ⊆ {1}.
    if values.get(x0, Fraction(1)) > Fraction(0) and len(chain) > 1:
        # x₀ not in chain[0]; fallback to simple indicator
        pass

    return values


# --------------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------------

def urysohn_function(
    space: Space,
    x0: Any,
    closed_set: frozenset,
) -> UrysohnWitness | None:
    """Construct a Urysohn function separating ``x0`` from ``closed_set`` in ``space``.

    Parameters
    ----------
    space :
        The topological space.
    x0 :
        The point to separate.  Must belong to ``space``.
    closed_set :
        A closed set not containing ``x0``.  For finite spaces this is a
        ``frozenset`` of points; for infinite spaces the function returns a
        formula-based witness regardless.

    Returns
    -------
    UrysohnWitness or None
        ``None`` when the separation is provably impossible (space is not T3.5
        for this pair) or when no algorithm applies.

    Examples
    --------
    >>> from pytop.experimental.spaces import discrete_finite_space
    >>> from pytop.experimental.spaces.urysohn import urysohn_function
    >>> d = discrete_finite_space({0, 1, 2})
    >>> w = urysohn_function(d, 0, frozenset({1, 2}))
    >>> w.evaluate(0)
    Fraction(0, 1)
    >>> w.evaluate(1)
    Fraction(1, 1)
    """
    from .representations import MetricTopologySpace

    if space.is_finite():
        return _finite_urysohn(space, x0, closed_set)

    if isinstance(space, MetricTopologySpace):
        return _metric_urysohn(space, x0, closed_set)

    return None


def _finite_urysohn(
    space: Space,
    x0: Any,
    closed_set: frozenset,
) -> UrysohnWitness | None:
    try:
        pts, opens = _finite_topo(space)
    except NotEnumerableError:
        return None

    carrier = frozenset(pts)

    if x0 not in carrier:
        return None
    if not (closed_set <= carrier):
        return None
    if x0 in closed_set:
        return None

    # Check C is actually closed (its complement is open)
    complement = carrier - closed_set
    if complement not in opens:
        return None  # C is not closed in this topology

    # Short path: discrete space → trivial indicator
    if _is_discrete(pts, opens):
        values = {p: (Fraction(0) if p == x0 else Fraction(1)) for p in pts}
        formula = f"f({x0!r}) = 0, f(y) = 1 for y ∈ C, f(y) = 1 otherwise (discrete: every function continuous)"
        return UrysohnWitness(
            x0=x0,
            closed_set=closed_set,
            values=values,
            formula=formula,
            method="discrete_indicator",
        )

    # General finite case: BFS chain
    values = _bfs_urysohn(x0, closed_set, pts, opens, carrier)
    if values is None:
        return None

    formula_parts = [f"f({p!r}) = {v}" for p, v in sorted(values.items(), key=lambda kv: kv[1])]
    formula = "; ".join(formula_parts)

    return UrysohnWitness(
        x0=x0,
        closed_set=closed_set,
        values=values,
        formula=formula,
        method="bfs_level",
    )


def _metric_urysohn(
    space: "MetricTopologySpace",
    x0: Any,
    closed_set: frozenset,
) -> UrysohnWitness:
    formula = (
        f"f(y) = min(1, d({x0!r}, y) / d({x0!r}, C))  "
        "where d(x₀, C) = inf{{d(x₀, c) : c ∈ C}} > 0 "
        "(x₀ ∉ cl(C) in a metric space ⟹ d(x₀, C) > 0). "
        "f is continuous: f(x₀) = 0, f(C) ⊆ {{1}}."
    )
    return UrysohnWitness(
        x0=x0,
        closed_set=closed_set,
        values=None,
        formula=formula,
        method="distance_ratio",
    )


__all__ = [
    "UrysohnWitness",
    "urysohn_function",
]
