"""Finite convergence spaces: the "royal road" generalization of topology.

A convergence space specifies which filters converge to which points, with no
requirement that the convergence come from a topology. This is the framework of
Dolecki's *A Royal Road to Topology* (2024) and the classical convergence-space
school (Choquet, Kowalsky, Kent).

On a **finite** carrier every filter is principal, so a filter is determined by
its kernel (the intersection of its members), a nonempty subset ``S`` of the
carrier. We therefore model a convergence structure as a relation between
kernels ``S`` and points ``x`` -- "the principal filter at ``S`` converges to
``x``". This makes the whole hierarchy computable:

* **convergence space** -- the principal filter at ``x`` converges to ``x``
  (centered) and finer filters keep converging (isotone);
* **pretopology** -- the coarsest filter converging to ``x`` (its neighborhood
  filter) also converges to ``x``;
* **pseudotopology** -- a filter converges to ``x`` whenever every finer
  ultrafilter does (on a finite carrier ultrafilters are the point filters, so
  this coincides with the pretopology condition);
* **topology** -- a pretopology whose minimal neighborhoods are open, i.e. the
  neighborhood assignment is transitive.

Bridges between finite topologies and convergence structures are provided, and
they are mutually inverse on topological convergences.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from itertools import combinations
from typing import Any

Kernel = frozenset


def _nonempty_subsets(elements: frozenset[Any]) -> list[frozenset[Any]]:
    members = list(elements)
    subsets: list[frozenset[Any]] = []
    for size in range(1, len(members) + 1):
        for combo in combinations(members, size):
            subsets.append(frozenset(combo))
    return subsets


@dataclass(frozen=True)
class ConvergenceSpace:
    """A finite convergence space.

    ``points`` is the carrier; ``convergences`` is the set of ``(kernel, point)``
    pairs meaning "the principal filter with kernel ``kernel`` converges to
    ``point``". Kernels are nonempty subsets of ``points``.
    """

    points: frozenset[Any]
    convergences: frozenset[tuple[frozenset[Any], Any]]

    def __init__(
        self,
        points: Iterable[Any],
        convergences: Iterable[tuple[Iterable[Any], Any]],
    ) -> None:
        carrier = frozenset(points)
        normalized: set[tuple[frozenset[Any], Any]] = set()
        for kernel, limit in convergences:
            kernel_set = frozenset(kernel)
            if not kernel_set:
                raise ValueError("A filter kernel must be nonempty.")
            if not kernel_set <= carrier:
                raise ValueError("Filter kernels must be subsets of the carrier.")
            if limit not in carrier:
                raise ValueError("Limit points must belong to the carrier.")
            normalized.add((kernel_set, limit))
        object.__setattr__(self, "points", carrier)
        object.__setattr__(self, "convergences", frozenset(normalized))

    def converges(self, kernel: Iterable[Any], limit: Any) -> bool:
        return (frozenset(kernel), limit) in self.convergences

    def kernels_converging_to(self, limit: Any) -> set[frozenset[Any]]:
        return {kernel for kernel, point in self.convergences if point == limit}

    def neighborhood_kernel(self, limit: Any) -> frozenset[Any]:
        """Return the kernel of the neighborhood filter at ``limit``.

        This is the union of all kernels converging to ``limit`` (the kernel of
        the coarsest such filter). Empty if nothing converges to ``limit``.
        """

        kernels = self.kernels_converging_to(limit)
        return frozenset().union(*kernels) if kernels else frozenset()


def is_convergence_space(space: ConvergenceSpace) -> bool:
    """Check the centered and isotone axioms.

    * centered: the point filter ``{x}`` converges to ``x`` for every ``x``;
    * isotone: if a filter converges to ``x`` then every finer filter (smaller
      kernel) also converges to ``x``.
    """

    for point in space.points:
        if not space.converges({point}, point):
            return False
    for kernel, limit in space.convergences:
        for finer in _nonempty_subsets(kernel):
            if (finer, limit) not in space.convergences:
                return False
    return True


def is_pretopology(space: ConvergenceSpace) -> bool:
    """A convergence space is a pretopology iff each neighborhood filter converges."""

    if not is_convergence_space(space):
        return False
    for point in space.points:
        neighborhood = space.neighborhood_kernel(point)
        if (neighborhood, point) not in space.convergences:
            return False
    return True


def is_pseudotopology(space: ConvergenceSpace) -> bool:
    """A convergence space is a pseudotopology iff filters whose every finer
    ultrafilter converges to ``x`` themselves converge to ``x``.

    On a finite carrier the ultrafilters are the point filters, so this is the
    condition that every nonempty subset of ``{p : {p} -> x}`` converges to
    ``x`` -- equivalent to the pretopology condition.
    """

    if not is_convergence_space(space):
        return False
    for point in space.points:
        point_limits = frozenset(
            p for p in space.points if space.converges({p}, point)
        )
        for subset in _nonempty_subsets(point_limits):
            if (subset, point) not in space.convergences:
                return False
    return True


def is_topological(space: ConvergenceSpace) -> bool:
    """A pretopology is topological iff its minimal neighborhoods are transitive.

    Concretely: for every point ``x`` and every ``y`` in its neighborhood kernel
    ``U_x``, the neighborhood kernel ``U_y`` is contained in ``U_x`` (so ``U_x``
    is open). This is the finite/Alexandrov topology condition.
    """

    if not is_pretopology(space):
        return False
    for point in space.points:
        u_x = space.neighborhood_kernel(point)
        for y in u_x:
            if not space.neighborhood_kernel(y) <= u_x:
                return False
    return True


def convergence_from_topology(
    points: Iterable[Any],
    opens: Iterable[Iterable[Any]],
) -> ConvergenceSpace:
    """Build the convergence space of a finite topology.

    ``opens`` is the family of open sets. The minimal neighborhood of ``x`` is
    ``U_x = intersection of all opens containing x``; a filter with kernel ``S``
    converges to ``x`` iff ``S`` is contained in ``U_x``.
    """

    carrier = frozenset(points)
    open_sets = [frozenset(o) for o in opens]
    convergences: set[tuple[frozenset[Any], Any]] = set()
    for x in carrier:
        containing = [o for o in open_sets if x in o]
        minimal = frozenset(carrier).intersection(*containing) if containing else carrier
        for subset in _nonempty_subsets(minimal):
            convergences.add((subset, x))
    return ConvergenceSpace(carrier, convergences)


def topology_from_convergence(space: ConvergenceSpace) -> frozenset[frozenset[Any]]:
    """Recover the open sets of a topological convergence space.

    A set ``O`` is open iff it is a neighborhood of each of its points, i.e.
    ``U_x`` is contained in ``O`` for every ``x`` in ``O``. Raises if ``space``
    is not topological.
    """

    if not is_topological(space):
        raise ValueError("Only topological convergence spaces induce a topology.")
    opens: set[frozenset[Any]] = {frozenset()}
    for subset in _nonempty_subsets(space.points):
        if all(space.neighborhood_kernel(x) <= subset for x in subset):
            opens.add(subset)
    return frozenset(opens)


def is_continuous_convergence_map(
    domain: ConvergenceSpace,
    codomain: ConvergenceSpace,
    mapping: dict[Any, Any],
) -> bool:
    """Check continuity: convergent filters map to convergent filters.

    ``f`` is continuous iff for every ``(S, x)`` converging in the domain, the
    pushed-forward filter (principal at ``f(S)``) converges to ``f(x)`` in the
    codomain.
    """

    if set(mapping) != set(domain.points):
        raise ValueError("The mapping must be defined on every domain point.")
    if not set(mapping.values()) <= set(codomain.points):
        raise ValueError("The mapping must land in the codomain carrier.")
    for kernel, limit in domain.convergences:
        image_kernel = frozenset(mapping[p] for p in kernel)
        if (image_kernel, mapping[limit]) not in codomain.convergences:
            return False
    return True


def grill_of_filter(kernel: Iterable[Any], carrier: Iterable[Any]) -> frozenset[frozenset[Any]]:
    """Return the grill of the principal filter with the given ``kernel``.

    The grill of a filter ``F`` is ``{A : A meets every member of F}``. For a
    principal filter the smallest member is the kernel, so the grill is exactly
    the sets that intersect the kernel. The grill is the order-dual notion to a
    filter and underlies the convergence-theoretic treatment of closure.
    """

    kernel_set = frozenset(kernel)
    universe = frozenset(carrier)
    return frozenset(
        subset
        for subset in _nonempty_subsets(universe)
        if subset & kernel_set
    )


__all__ = [
    "ConvergenceSpace",
    "is_convergence_space",
    "is_pretopology",
    "is_pseudotopology",
    "is_topological",
    "convergence_from_topology",
    "topology_from_convergence",
    "is_continuous_convergence_map",
    "grill_of_filter",
]
