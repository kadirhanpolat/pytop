"""Structured random function generators.

Provides:
- ``random_injective_function``   — one-to-one function (requires |codomain| >= |domain|)
- ``random_surjective_function``  — onto function (requires |domain| >= |codomain|)
- ``random_bijection``            — bijection (requires equal sizes)
- ``random_continuous_function``  — continuous map between topological spaces
- ``random_open_map``             — open map between topological spaces
- ``random_closed_map``           — closed map between topological spaces
- ``random_homeomorphism``        — homeomorphism (bijective + continuous + open)

All functions return a plain ``dict``.  Pass the result to
:func:`pytop.maps.make_function` to obtain a :class:`~pytop.maps.FiniteMap`.
Topological generators accept both :class:`~pytop.finite_spaces.FiniteTopologicalSpace`
and :class:`~pytop.random_generators.LazyTopology` as space arguments.
"""

from __future__ import annotations

from random import Random
from typing import Any

from .random_generators import LazyTopology, RandomGeneratorError

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _is_open_in(space: Any, subset: frozenset[Any]) -> bool:
    """Return True iff *subset* is open in *space*."""
    if isinstance(space, LazyTopology):
        return space.is_open(subset)
    # FiniteTopologicalSpace: topology is a collection of open sets
    return subset in frozenset(frozenset(u) for u in space.topology)


def _basis_of(space: Any) -> list[frozenset[Any]]:
    """Return a basis (list of open sets) for *space*.

    For LazyTopology the cached intersection-closed basis is returned.
    For FiniteTopologicalSpace the full topology is returned (every open
    set is trivially a union of itself, so it acts as its own basis).
    The empty set is always excluded; the carrier (X) is included only if
    it appears in the basis/topology.
    """
    if isinstance(space, LazyTopology):
        return [b for b in space._basis_cache if b]
    return [frozenset(u) for u in space.topology]


def _check_continuous(
    f_dict: dict[Any, Any],
    domain_space: Any,
    codomain_space: Any,
) -> bool:
    """Return True iff *f_dict* is continuous from domain to codomain.

    Uses the basis criterion: f is continuous iff the preimage of every
    basis element of the codomain is open in the domain.
    """
    for B in _basis_of(codomain_space):
        preimage = frozenset(x for x in domain_space.carrier if f_dict[x] in B)
        if not _is_open_in(domain_space, preimage):
            return False
    return True


def _check_open_map(
    f_dict: dict[Any, Any],
    domain_space: Any,
    codomain_space: Any,
) -> bool:
    """Return True iff *f_dict* is an open map."""
    for B in _basis_of(domain_space):
        if not B:
            continue
        image = frozenset(f_dict[x] for x in B)
        if not _is_open_in(codomain_space, image):
            return False
    return True


def _check_closed_map(
    f_dict: dict[Any, Any],
    domain_space: Any,
    codomain_space: Any,
) -> bool:
    """Return True iff *f_dict* is a closed map.

    Closed sets in the domain are complements of open sets.
    Their images must be closed (complement open) in the codomain.
    """
    carrier_domain = frozenset(domain_space.carrier)
    carrier_codomain = frozenset(codomain_space.carrier)
    for U in _basis_of(domain_space):
        closed = carrier_domain - U
        image_closed = frozenset(f_dict[x] for x in closed)
        complement = carrier_codomain - image_closed
        if not _is_open_in(codomain_space, complement):
            return False
    return True


def _uniform_random_dict(
    domain_list: list[Any],
    codomain_list: list[Any],
    rng: Random,
) -> dict[Any, Any]:
    return {x: rng.choice(codomain_list) for x in domain_list}


# ---------------------------------------------------------------------------
# Set-level (topology-agnostic) generators
# ---------------------------------------------------------------------------

def random_injective_function(
    domain: Any,
    codomain: Any,
    seed: int | None = None,
) -> dict[Any, Any]:
    """Return a random injective (one-to-one) function as a dict.

    Each domain element is assigned a distinct codomain element.

    Parameters
    ----------
    domain:
        Elements of the domain set.
    codomain:
        Elements of the codomain set (must have at least as many elements
        as the domain).
    seed:
        Random seed for reproducibility.

    Raises
    ------
    RandomGeneratorError
        If ``|codomain| < |domain|``.
    """
    rng = Random(seed)
    domain_list = list(domain)
    codomain_list = list(codomain)
    if len(codomain_list) < len(domain_list):
        raise RandomGeneratorError(
            f"Injective function requires |codomain| >= |domain|, "
            f"got {len(codomain_list)} < {len(domain_list)}."
        )
    values = rng.sample(codomain_list, len(domain_list))
    return dict(zip(domain_list, values))


def random_surjective_function(
    domain: Any,
    codomain: Any,
    seed: int | None = None,
) -> dict[Any, Any]:
    """Return a random surjective (onto) function as a dict.

    Every codomain element is the image of at least one domain element.

    Parameters
    ----------
    domain:
        Elements of the domain set (must have at least as many elements
        as the codomain).
    codomain:
        Elements of the codomain set (must be non-empty).
    seed:
        Random seed for reproducibility.

    Raises
    ------
    RandomGeneratorError
        If ``|domain| < |codomain|`` or codomain is empty.
    """
    rng = Random(seed)
    domain_list = list(domain)
    codomain_list = list(codomain)
    if not codomain_list:
        raise RandomGeneratorError("Codomain must be non-empty.")
    if len(domain_list) < len(codomain_list):
        raise RandomGeneratorError(
            f"Surjective function requires |domain| >= |codomain|, "
            f"got {len(domain_list)} < {len(codomain_list)}."
        )
    # Shuffle both lists to remove ordering bias
    shuffled_domain = list(domain_list)
    rng.shuffle(shuffled_domain)
    shuffled_codomain = list(codomain_list)
    rng.shuffle(shuffled_codomain)
    result: dict[Any, Any] = {}
    # Guarantee each codomain element is hit
    for i, cod_elem in enumerate(shuffled_codomain):
        result[shuffled_domain[i]] = cod_elem
    # Assign remaining domain elements freely
    for i in range(len(shuffled_codomain), len(shuffled_domain)):
        result[shuffled_domain[i]] = rng.choice(shuffled_codomain)
    return result


def random_bijection(
    domain: Any,
    codomain: Any,
    seed: int | None = None,
) -> dict[Any, Any]:
    """Return a random bijection as a dict.

    Parameters
    ----------
    domain:
        Elements of the domain set.
    codomain:
        Elements of the codomain set (must have the same cardinality as
        the domain).
    seed:
        Random seed for reproducibility.

    Raises
    ------
    RandomGeneratorError
        If ``|domain| != |codomain|``.
    """
    rng = Random(seed)
    domain_list = list(domain)
    codomain_list = list(codomain)
    if len(domain_list) != len(codomain_list):
        raise RandomGeneratorError(
            f"Bijection requires |domain| == |codomain|, "
            f"got {len(domain_list)} != {len(codomain_list)}."
        )
    values = rng.sample(codomain_list, len(codomain_list))
    return dict(zip(domain_list, values))


# ---------------------------------------------------------------------------
# Topological function generators
# ---------------------------------------------------------------------------

def random_continuous_function(
    domain_space: Any,
    codomain_space: Any,
    seed: int | None = None,
    max_attempts: int = 500,
) -> dict[Any, Any]:
    """Return a random continuous function between two topological spaces.

    Uses rejection sampling: uniform random functions are generated until
    a continuous one is found (verified via the basis preimage criterion).
    Works with both :class:`~pytop.finite_spaces.FiniteTopologicalSpace`
    and :class:`~pytop.random_generators.LazyTopology`.

    Parameters
    ----------
    domain_space:
        Source topological space.
    codomain_space:
        Target topological space.
    seed:
        Random seed for reproducibility.
    max_attempts:
        Maximum number of random functions to try.

    Raises
    ------
    RandomGeneratorError
        If no continuous function is found within *max_attempts* tries,
        or if the codomain carrier is empty.
    """
    rng = Random(seed)
    domain_list = list(domain_space.carrier)
    codomain_list = list(codomain_space.carrier)
    if not codomain_list:
        raise RandomGeneratorError("Codomain carrier must be non-empty.")
    for _ in range(max_attempts):
        f = _uniform_random_dict(domain_list, codomain_list, rng)
        if _check_continuous(f, domain_space, codomain_space):
            return f
    raise RandomGeneratorError(
        f"No continuous function found after {max_attempts} attempts. "
        "The spaces may have very few continuous maps."
    )


def random_open_map(
    domain_space: Any,
    codomain_space: Any,
    seed: int | None = None,
    max_attempts: int = 500,
) -> dict[Any, Any]:
    """Return a random open map between two topological spaces.

    An open map sends every open set of the domain to an open set of the
    codomain.  Uses rejection sampling with the basis image criterion.

    Parameters
    ----------
    domain_space:
        Source topological space.
    codomain_space:
        Target topological space.
    seed:
        Random seed for reproducibility.
    max_attempts:
        Maximum number of random functions to try.

    Raises
    ------
    RandomGeneratorError
        If no open map is found within *max_attempts* tries.
    """
    rng = Random(seed)
    domain_list = list(domain_space.carrier)
    codomain_list = list(codomain_space.carrier)
    if not codomain_list:
        raise RandomGeneratorError("Codomain carrier must be non-empty.")
    for _ in range(max_attempts):
        f = _uniform_random_dict(domain_list, codomain_list, rng)
        if _check_open_map(f, domain_space, codomain_space):
            return f
    raise RandomGeneratorError(
        f"No open map found after {max_attempts} attempts."
    )


def random_closed_map(
    domain_space: Any,
    codomain_space: Any,
    seed: int | None = None,
    max_attempts: int = 500,
) -> dict[Any, Any]:
    """Return a random closed map between two topological spaces.

    A closed map sends every closed set of the domain to a closed set of
    the codomain.  Uses rejection sampling.

    Parameters
    ----------
    domain_space:
        Source topological space.
    codomain_space:
        Target topological space.
    seed:
        Random seed for reproducibility.
    max_attempts:
        Maximum number of random functions to try.

    Raises
    ------
    RandomGeneratorError
        If no closed map is found within *max_attempts* tries.
    """
    rng = Random(seed)
    domain_list = list(domain_space.carrier)
    codomain_list = list(codomain_space.carrier)
    if not codomain_list:
        raise RandomGeneratorError("Codomain carrier must be non-empty.")
    for _ in range(max_attempts):
        f = _uniform_random_dict(domain_list, codomain_list, rng)
        if _check_closed_map(f, domain_space, codomain_space):
            return f
    raise RandomGeneratorError(
        f"No closed map found after {max_attempts} attempts."
    )


def random_homeomorphism(
    domain_space: Any,
    codomain_space: Any,
    seed: int | None = None,
    max_attempts: int = 500,
) -> dict[Any, Any]:
    """Return a random homeomorphism between two topological spaces.

    A homeomorphism is a bijective continuous open map.  Only bijections
    (random permutations of the codomain) are tried, so each candidate is
    automatically bijective.

    Parameters
    ----------
    domain_space:
        Source topological space.
    codomain_space:
        Target topological space (must have the same cardinality as domain).
    seed:
        Random seed for reproducibility.
    max_attempts:
        Maximum number of random bijections to try.

    Raises
    ------
    RandomGeneratorError
        If the carrier sizes differ, or if no homeomorphism is found within
        *max_attempts* tries (the spaces may not be homeomorphic).
    """
    rng = Random(seed)
    domain_list = list(domain_space.carrier)
    codomain_list = list(codomain_space.carrier)
    if len(domain_list) != len(codomain_list):
        raise RandomGeneratorError(
            f"Homeomorphism requires equal carrier sizes, "
            f"got {len(domain_list)} != {len(codomain_list)}."
        )
    for _ in range(max_attempts):
        values = rng.sample(codomain_list, len(codomain_list))
        f = dict(zip(domain_list, values))
        if _check_continuous(f, domain_space, codomain_space) and \
                _check_open_map(f, domain_space, codomain_space):
            return f
    raise RandomGeneratorError(
        f"No homeomorphism found after {max_attempts} attempts. "
        "The spaces may not be homeomorphic."
    )


__all__ = [
    "random_injective_function",
    "random_surjective_function",
    "random_bijection",
    "random_continuous_function",
    "random_open_map",
    "random_closed_map",
    "random_homeomorphism",
]
