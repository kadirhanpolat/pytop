"""Dimension theory benchmark helpers.

This v0.1.103 surface replaces the old placeholder constants with a
conservative benchmark/theorem layer for:

- small inductive dimension ``ind``
- large inductive dimension ``Ind``
- covering dimension ``dim``
- zero-dimensionality and related clopen/disconnectedness checks

The module is intentionally modest: it reads explicit tags/metadata and a few
stable benchmark corridors rather than pretending to solve general dimension
theory for arbitrary spaces.
"""

from __future__ import annotations

from typing import Any

VERSION = "0.1.103"

ZERO_DIMENSION_TAGS: frozenset[str] = frozenset({
    "zero_dimensional",
    "zero-dimensional",
    "clopen_base",
    "cantor_set",
    "stone_space",
})
TOTALLY_DISCONNECTED_TAGS: frozenset[str] = frozenset({
    "totally_disconnected",
    "totally-disconnected",
    "cantor_set",
})
NEGATIVE_ZERO_DIMENSION_TAGS: frozenset[str] = frozenset({
    "not_zero_dimensional",
    "not_zero-dimensional",
})


def _metadata_of(obj: Any) -> dict[str, Any]:
    if isinstance(obj, dict):
        raw = obj.get("metadata", {})
        return raw if isinstance(raw, dict) else {}
    raw = getattr(obj, "metadata", {}) or {}
    return raw if isinstance(raw, dict) else {}


def _extract_tags(obj: Any) -> set[str]:
    tags: set[str] = set()
    if isinstance(obj, dict):
        raw_tags = obj.get("tags", [])
        if isinstance(raw_tags, (set, list, tuple, frozenset)):
            tags.update(str(tag).strip().lower() for tag in raw_tags)
    metadata = _metadata_of(obj)
    raw_meta_tags = metadata.get("tags", [])
    if isinstance(raw_meta_tags, (set, list, tuple, frozenset)):
        tags.update(str(tag).strip().lower() for tag in raw_meta_tags)
    for attr in ("tags", "_tags"):
        raw = getattr(obj, attr, None)
        if isinstance(raw, (set, list, tuple, frozenset)):
            tags.update(str(tag).strip().lower() for tag in raw)
    return tags


def _representation_of(obj: Any) -> str:
    if isinstance(obj, dict) and "representation" in obj:
        return str(obj["representation"]).strip().lower()
    metadata = _metadata_of(obj)
    if "representation" in metadata:
        return str(metadata["representation"]).strip().lower()
    rep = getattr(obj, "representation", None)
    if rep:
        return str(rep).strip().lower()
    return "symbolic_general"


def _maybe_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    return None


def _dimension_field(obj: Any, key: str) -> int | None:
    if isinstance(obj, dict):
        value = _maybe_int(obj.get(key))
        if value is not None:
            return value
    metadata = _metadata_of(obj)
    value = _maybe_int(metadata.get(key))
    if value is not None:
        return value
    return _maybe_int(getattr(obj, key, None))


def _benchmark_dimension_from_name(obj: Any) -> int | None:
    name = ""
    if isinstance(obj, dict):
        name = str(obj.get("space_type") or obj.get("name") or "")
    if not name:
        metadata = _metadata_of(obj)
        name = str(metadata.get("space_type") or metadata.get("name") or getattr(obj, "name", ""))
    normalized = name.strip().lower()
    if normalized == "cantor set":
        return 0
    if normalized.startswith("r^"):
        tail = normalized[2:]
        if tail.isdigit():
            return int(tail)
    if normalized.startswith("euclidean_") and normalized[10:].isdigit():
        return int(normalized[10:])
    return None


def _dimension_value(obj: Any, key: str) -> int | None:
    explicit = _dimension_field(obj, key)
    if explicit is not None:
        return explicit
    benchmark = _benchmark_dimension_from_name(obj)
    if benchmark is not None:
        return benchmark
    tags = _extract_tags(obj)
    if tags & ZERO_DIMENSION_TAGS:
        return 0
    return None


def ind(space):
    """Small inductive dimension on the conservative benchmark corridor."""
    return _dimension_value(space, "ind")


def Ind(space):
    """Large inductive dimension on the conservative benchmark corridor."""
    return _dimension_value(space, "Ind")


def dim(space):
    """Covering dimension on the conservative benchmark corridor."""
    return _dimension_value(space, "dim")


def has_clopen_base(space):
    """Return whether the space is tagged/recognized as having a clopen base."""
    tags = _extract_tags(space)
    if tags & NEGATIVE_ZERO_DIMENSION_TAGS:
        return False
    if tags & ZERO_DIMENSION_TAGS:
        return True
    if _dimension_value(space, "dim") == 0 and (_representation_of(space) != "symbolic_general" or tags):
        return True
    if isinstance(space, dict):
        explicit = space.get("has_clopen_base")
        if isinstance(explicit, bool):
            return explicit
    metadata = _metadata_of(space)
    explicit = metadata.get("has_clopen_base")
    if isinstance(explicit, bool):
        return explicit
    explicit = getattr(space, "has_clopen_base", None)
    if isinstance(explicit, bool):
        return explicit
    return False


def is_zero_dimensional(space):
    """Return whether the space lies in the benchmark zero-dimensional corridor."""
    tags = _extract_tags(space)
    if tags & NEGATIVE_ZERO_DIMENSION_TAGS:
        return False
    if has_clopen_base(space):
        return True
    value = _dimension_value(space, "ind")
    if value == 0:
        return True
    return False


def is_totally_disconnected(space):
    """Return whether the space lies in the benchmark totally disconnected corridor."""
    tags = _extract_tags(space)
    if tags & TOTALLY_DISCONNECTED_TAGS:
        return True
    if is_zero_dimensional(space):
        return True
    if isinstance(space, dict):
        explicit = space.get("is_totally_disconnected")
        if isinstance(explicit, bool):
            return explicit
    metadata = _metadata_of(space)
    explicit = metadata.get("is_totally_disconnected")
    if isinstance(explicit, bool):
        return explicit
    explicit = getattr(space, "is_totally_disconnected", None)
    if isinstance(explicit, bool):
        return explicit
    return False


# ---------------------------------------------------------------------------
# Computational engines (from raw simplicial / topology data)
# ---------------------------------------------------------------------------

def covering_dimension_simplicial(simplices: list[list[Any]]) -> int:
    """Return the covering dimension of a finite simplicial complex.

    For a simplicial complex K, dim(|K|) = max{n : σ ∈ K, dim σ = n},
    i.e., the maximum simplex dimension.  This equals the geometric
    (and covering) dimension of the polyhedron |K|.

    Parameters
    ----------
    simplices:
        List of simplices as vertex lists.

    Returns
    -------
    int
        Covering dimension (≥ 0), or -1 for the empty complex.

    Examples
    --------
    A filled triangle has dimension 2:

    >>> covering_dimension_simplicial([[0,1,2],[0,1],[0,2],[1,2],[0],[1],[2]])
    2

    A circle S¹ (boundary of triangle) has dimension 1:

    >>> covering_dimension_simplicial([[0,1],[1,2],[2,0],[0],[1],[2]])
    1
    """
    if not simplices:
        return -1
    return max(len(s) - 1 for s in simplices if s)


def _specialization_order(open_sets: list[frozenset[Any]]) -> dict[Any, set[Any]]:
    universe: set[Any] = set()
    for u in open_sets:
        universe.update(u)
    leq: dict[Any, set[Any]] = {x: set() for x in universe}
    for x in universe:
        opens_x = [frozenset(u) for u in open_sets if x in frozenset(u)]
        for y in universe:
            if all(y in u for u in opens_x):
                leq[x].add(y)
    return leq


def ind_finite_space(open_sets: list[frozenset[Any]]) -> int:
    """Compute the small inductive dimension of a finite topological space.

    For a finite T₀ space X with specialization poset P_X:
    ind(X) = dim(Δ(P_X)), where Δ(P_X) is the order complex of P_X and
    dim = length of the longest chain in P_X.

    A chain x₀ <_P x₁ <_P ... <_P x_k has length k.
    ind(∅) = -1; ind(single point) = 0; ind(Sierpiński space) = 1.

    Parameters
    ----------
    open_sets:
        List of open sets as frozensets defining the topology.

    Returns
    -------
    int
        The small inductive dimension (≥ -1).

    Examples
    --------
    A single point has ind = 0:

    >>> ind_finite_space([frozenset(), frozenset({0})])
    0

    The Sierpiński space {0,1} with τ = {∅, {1}, {0,1}} has ind = 1:

    >>> ind_finite_space([frozenset(), frozenset({1}), frozenset({0,1})])
    1
    """
    leq = _specialization_order(open_sets)
    universe = set(leq)
    if not universe:
        return -1

    def longest_chain_from(x: Any, visited: frozenset[Any]) -> int:
        best = 0
        for y in universe:
            # strict specialization: x ≤ y but NOT y ≤ x
            if (y not in visited and y in leq.get(x, set())
                    and x != y and x not in leq.get(y, set())):
                best = max(best, 1 + longest_chain_from(y, visited | {y}))
        return best

    return max(longest_chain_from(x, frozenset({x})) for x in universe)


__all__ = [
    "ind",
    "Ind",
    "dim",
    "has_clopen_base",
    "is_zero_dimensional",
    "is_totally_disconnected",
    "covering_dimension_simplicial",
    "ind_finite_space",
]
