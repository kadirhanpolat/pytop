"""Structured random relation generators.

Provides:
- ``random_reflexive_relation``   — reflexive + Bernoulli off-diagonal
- ``random_symmetric_relation``   — symmetric via pair-mirroring
- ``random_transitive_relation``  — Bernoulli start + transitive closure
- ``random_partial_order``        — DAG-based partial order
- ``random_total_order``          — linear order from random permutation
- ``random_equivalence_relation`` — equivalence via random partition
"""

from __future__ import annotations

from collections import defaultdict
from random import Random
from typing import Any

from .random_generators import RandomGeneratorError
from .relations import equivalence_from_classes

# ---------------------------------------------------------------------------
# Internal helper
# ---------------------------------------------------------------------------

def _transitive_closure(
    carrier_list: list[Any],
    relation: set[tuple[Any, Any]],
) -> set[tuple[Any, Any]]:
    """Compute the transitive closure via Warshall's algorithm."""
    n = len(carrier_list)
    idx: dict[Any, int] = {x: i for i, x in enumerate(carrier_list)}
    mat: list[list[bool]] = [[False] * n for _ in range(n)]
    for (x, y) in relation:
        mat[idx[x]][idx[y]] = True
    for k in range(n):
        for i in range(n):
            if mat[i][k]:
                for j in range(n):
                    if mat[k][j]:
                        mat[i][j] = True
    result: set[tuple[Any, Any]] = set()
    for i in range(n):
        for j in range(n):
            if mat[i][j]:
                result.add((carrier_list[i], carrier_list[j]))
    return result


def _validate_density(density: float) -> None:
    if not (0.0 <= density <= 1.0):
        raise RandomGeneratorError(f"density must be in [0.0, 1.0], got {density}.")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def random_reflexive_relation(
    carrier: Any,
    density: float = 0.5,
    seed: int | None = None,
) -> set[tuple[Any, Any]]:
    """Return a random reflexive binary relation on *carrier*.

    The diagonal ``(x, x)`` is always included.  Each off-diagonal pair
    ``(x, y)`` with ``x != y`` is included independently with probability
    *density*.

    Parameters
    ----------
    carrier:
        Elements of the underlying set.
    density:
        Inclusion probability for off-diagonal pairs, in [0.0, 1.0].
    seed:
        Random seed for reproducibility.
    """
    _validate_density(density)
    rng = Random(seed)
    carrier_list = list(carrier)
    relation: set[tuple[Any, Any]] = set()
    for x in carrier_list:
        relation.add((x, x))
        for y in carrier_list:
            if y != x and rng.random() < density:
                relation.add((x, y))
    return relation


def random_symmetric_relation(
    carrier: Any,
    density: float = 0.5,
    seed: int | None = None,
) -> set[tuple[Any, Any]]:
    """Return a random symmetric binary relation on *carrier*.

    For each unordered pair ``{x, y}`` with ``x != y``, both ``(x, y)`` and
    ``(y, x)`` are included with probability *density*.  Each diagonal pair
    ``(x, x)`` is included independently with probability *density*.

    Parameters
    ----------
    carrier:
        Elements of the underlying set.
    density:
        Inclusion probability per unordered pair and per diagonal element.
    seed:
        Random seed for reproducibility.
    """
    _validate_density(density)
    rng = Random(seed)
    carrier_list = list(carrier)
    relation: set[tuple[Any, Any]] = set()
    for i, x in enumerate(carrier_list):
        if rng.random() < density:
            relation.add((x, x))
        for y in carrier_list[i + 1:]:
            if rng.random() < density:
                relation.add((x, y))
                relation.add((y, x))
    return relation


def random_transitive_relation(
    carrier: Any,
    density: float = 0.5,
    seed: int | None = None,
) -> set[tuple[Any, Any]]:
    """Return a random transitive binary relation on *carrier*.

    Pairs are initially sampled via Bernoulli(*density*), then the transitive
    closure is applied.  The final density may exceed *density* because
    closure adds implied pairs.

    Parameters
    ----------
    carrier:
        Elements of the underlying set.
    density:
        Initial inclusion probability per pair before closure.
    seed:
        Random seed for reproducibility.
    """
    _validate_density(density)
    rng = Random(seed)
    carrier_list = list(carrier)
    initial: set[tuple[Any, Any]] = set()
    for x in carrier_list:
        for y in carrier_list:
            if rng.random() < density:
                initial.add((x, y))
    return _transitive_closure(carrier_list, initial)


def random_partial_order(
    carrier: Any,
    density: float = 0.5,
    seed: int | None = None,
) -> set[tuple[Any, Any]]:
    """Return a random partial order (reflexive, antisymmetric, transitive).

    Algorithm:

    1. Pick a random permutation of *carrier*.
    2. For each pair ``(i, j)`` with ``i < j`` in the permutation, include
       the edge ``(perm[i], perm[j])`` with probability *density*.
       This produces a DAG — no cycles possible.
    3. Apply transitive closure (antisymmetry preserved by the DAG structure).
    4. Add the diagonal to make the relation reflexive.

    Parameters
    ----------
    carrier:
        Elements of the underlying set.
    density:
        Probability that each forward DAG edge is included.
    seed:
        Random seed for reproducibility.
    """
    _validate_density(density)
    rng = Random(seed)
    carrier_list = list(carrier)
    perm = list(carrier_list)
    rng.shuffle(perm)
    dag: set[tuple[Any, Any]] = set()
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            if rng.random() < density:
                dag.add((perm[i], perm[j]))
    result = _transitive_closure(carrier_list, dag)
    for x in carrier_list:
        result.add((x, x))
    return result


def random_total_order(
    carrier: Any,
    seed: int | None = None,
) -> set[tuple[Any, Any]]:
    """Return a random total (linear) order on *carrier*.

    A random permutation of *carrier* determines a strict linear order;
    the result includes all pairs ``(perm[i], perm[j])`` with ``i <= j``
    (i.e. the reflexive total order).

    Parameters
    ----------
    carrier:
        Elements of the underlying set.
    seed:
        Random seed for reproducibility.
    """
    rng = Random(seed)
    perm = list(carrier)
    rng.shuffle(perm)
    result: set[tuple[Any, Any]] = set()
    for i in range(len(perm)):
        for j in range(i, len(perm)):
            result.add((perm[i], perm[j]))
    return result


def random_equivalence_relation(
    carrier: Any,
    seed: int | None = None,
) -> set[tuple[Any, Any]]:
    """Return a random equivalence relation (reflexive, symmetric, transitive).

    The carrier is randomly partitioned into ``k`` equivalence classes
    (``k`` is chosen uniformly from ``1`` to ``|carrier|``).  Each element
    is independently assigned to a class.  The resulting relation contains
    all pairs ``(a, b)`` where ``a`` and ``b`` belong to the same class.

    Parameters
    ----------
    carrier:
        Elements of the underlying set.
    seed:
        Random seed for reproducibility.
    """
    rng = Random(seed)
    carrier_list = list(carrier)
    n = len(carrier_list)
    if n == 0:
        return set()
    num_classes = rng.randint(1, n)
    buckets: dict[int, list[Any]] = defaultdict(list)
    for x in carrier_list:
        buckets[rng.randint(0, num_classes - 1)].append(x)
    non_empty = [members for members in buckets.values() if members]
    return equivalence_from_classes(*non_empty)


__all__ = [
    "random_reflexive_relation",
    "random_symmetric_relation",
    "random_transitive_relation",
    "random_partial_order",
    "random_total_order",
    "random_equivalence_relation",
]
