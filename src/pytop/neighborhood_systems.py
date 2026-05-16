"""Neighborhood systems module — v0.1.51 Cilt III corridor.

This module provides finite exact helpers for the axiomatic neighborhood-system
layer of Chapter 18 (Volume 2).  It consolidates the master's-level corridor:

  • neighborhood system verification (four axioms)
  • local base verification and character (χ) computation
  • neighborhood-system ↔ topology equivalence (round-trip consistency check)
  • open-neighborhood profile extraction
  • master's-level corridor entry-point: analyze_neighborhood_system

Finite-exact semantics: all helpers give exact Results for explicit finite spaces.

Roadmap reference:
  v0.1.51 — Restore full neighborhood systems as a master's-level chapter
             (Cilt III, Chapter 18)
"""

from __future__ import annotations

from typing import Any

from .result import Result

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _open_sets_of(carrier: list, topology: list[frozenset]) -> list[frozenset]:
    """Return the topology as a list of frozensets."""
    return [frozenset(u) for u in topology]


def _neighborhood_system_from_topology(
    carrier: list, topology: list[frozenset]
) -> dict[Any, list[frozenset]]:
    """Compute N(x) for every x from an explicit topology."""
    open_sets = _open_sets_of(carrier, topology)
    nbhd: dict[Any, list[frozenset]] = {}
    for x in carrier:
        nbhd[x] = [n for n in _power_subsets(carrier)
                   if any(x in u and u <= n for u in open_sets)]
    return nbhd


def _power_subsets(carrier: list) -> list[frozenset]:
    """Return all subsets of carrier as frozensets."""
    result = []
    n = len(carrier)
    for i in range(1 << n):
        result.append(frozenset(carrier[j] for j in range(n) if i & (1 << j)))
    return result


# ---------------------------------------------------------------------------
# Axiom checkers
# ---------------------------------------------------------------------------

def _axiom_x_in_every_N(x: Any, nbhd_x: list[frozenset]) -> bool:
    """N1: Every N ∈ N(x) satisfies x ∈ N."""
    return all(x in n for n in nbhd_x)


def _axiom_X_in_nbhd(carrier: list, nbhd_x: list[frozenset]) -> bool:
    """N2: The whole space X ∈ N(x)."""
    return frozenset(carrier) in [frozenset(n) for n in nbhd_x]


def _axiom_finite_intersection(nbhd_x: list[frozenset]) -> bool:
    """N3: N(x) is closed under finite intersections (for all pairs)."""
    nbhd_set = list(nbhd_x)
    for i, a in enumerate(nbhd_set):
        for b in nbhd_set[i:]:
            if (a & b) not in nbhd_x and (a & b) != frozenset():
                return False
    return True


def _axiom_superset_closed(carrier: list, nbhd_x: list[frozenset]) -> bool:
    """N4: N(x) is closed under supersets (upward-closed in the power set)."""
    all_subsets = _power_subsets(carrier)
    for n in nbhd_x:
        for s in all_subsets:
            if n <= s and s not in nbhd_x:
                return False
    return True


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def neighborhood_system_axioms(
    carrier: list,
    topology: list[frozenset],
    point: Any,
) -> Result:
    """Verify the four neighborhood-system axioms for a given point.

    The four axioms are:
      N1: x ∈ N for every N ∈ N(x).
      N2: X ∈ N(x).
      N3: N(x) is closed under finite intersections.
      N4: N(x) is upward-closed (superset-closed).

    Parameters
    ----------
    carrier:
        The finite set of points, e.g. ['a', 'b', 'c'].
    topology:
        The topology as a list of open sets (iterables of points).
    point:
        The point x at which to check the axioms.
    """
    if point not in carrier:
        return Result.unknown(
            mode="symbolic",
            value="neighborhood_system_axioms",
            justification=[f"Point {point!r} not in carrier {carrier}."],
            metadata={"operator": "neighborhood_system_axioms", "point": point},
        )

    open_sets = [frozenset(u) for u in topology]
    all_subsets = _power_subsets(carrier)
    nbhd_x = [s for s in all_subsets
               if any(point in u and u <= s for u in open_sets)]

    n1 = _axiom_x_in_every_N(point, nbhd_x)
    n2 = _axiom_X_in_nbhd(carrier, nbhd_x)
    n3 = _axiom_finite_intersection(nbhd_x)
    n4 = _axiom_superset_closed(carrier, nbhd_x)

    all_pass = n1 and n2 and n3 and n4

    return Result.true(
        mode="exact",
        value={
            "N1_x_in_N": n1,
            "N2_X_in_Nx": n2,
            "N3_finite_intersection": n3,
            "N4_superset_closed": n4,
            "all_axioms": all_pass,
        },
        justification=[
            f"Neighborhood system axioms at {point!r}: "
            f"N1={n1}, N2={n2}, N3={n3}, N4={n4}. "
            f"|N({point!r})|={len(nbhd_x)}."
        ],
        metadata={
            "operator": "neighborhood_system_axioms",
            "point": point,
            "neighborhood_count": len(nbhd_x),
            "carrier_size": len(carrier),
            "cilt_iii_corridor": "neighborhood-systems",
            "v0_1_51_corridor_record": True,
        },
    )


def neighborhood_system(
    carrier: list,
    topology: list[frozenset],
    point: Any,
) -> Result:
    """Return the neighborhood system N(x) for a given point.

    Parameters
    ----------
    carrier:
        Finite set of points.
    topology:
        List of open sets.
    point:
        The point x.
    """
    if point not in carrier:
        return Result.unknown(
            mode="symbolic",
            value="neighborhood_system",
            justification=[f"Point {point!r} not in carrier."],
            metadata={"operator": "neighborhood_system", "point": point},
        )

    open_sets = [frozenset(u) for u in topology]
    all_subsets = _power_subsets(carrier)
    nbhd_x = sorted(
        [s for s in all_subsets if any(point in u and u <= s for u in open_sets)],
        key=lambda s: (len(s), sorted(repr(e) for e in s)),
    )

    return Result.true(
        mode="exact",
        value=[sorted(repr(e) for e in n) for n in nbhd_x],
        justification=[
            f"N({point!r}) has {len(nbhd_x)} member(s). "
            f"Smallest: {sorted(repr(e) for e in nbhd_x[0]) if nbhd_x else 'none'}."
        ],
        metadata={
            "operator": "neighborhood_system",
            "point": point,
            "neighborhood_count": len(nbhd_x),
            "cilt_iii_corridor": "neighborhood-systems",
            "v0_1_51_corridor_record": True,
        },
    )


def local_base_check(
    carrier: list,
    topology: list[frozenset],
    point: Any,
    candidate_base: list[frozenset],
) -> Result:
    """Check whether a given family is a local base at point x.

    A family B_x is a local base at x iff:
      1. Every B ∈ B_x is a neighborhood of x.
      2. For every N ∈ N(x) there exists B ∈ B_x with B ⊆ N.

    Parameters
    ----------
    carrier, topology, point:
        As above.
    candidate_base:
        The proposed local base family (list of sets).
    """
    if point not in carrier:
        return Result.unknown(
            mode="symbolic",
            value="local_base_check",
            justification=[f"Point {point!r} not in carrier."],
            metadata={"operator": "local_base_check", "point": point},
        )

    open_sets = [frozenset(u) for u in topology]
    all_subsets = _power_subsets(carrier)
    nbhd_x = [s for s in all_subsets if any(point in u and u <= s for u in open_sets)]
    cand = [frozenset(b) for b in candidate_base]

    # Condition 1: every candidate is a neighborhood
    cond1 = all(b in nbhd_x for b in cand)
    failing_1 = [sorted(repr(e) for e in b) for b in cand if b not in nbhd_x]

    # Condition 2: every neighborhood contains some candidate
    cond2_failures = [n for n in nbhd_x if not any(b <= n for b in cand)]
    cond2 = len(cond2_failures) == 0

    is_local_base = cond1 and cond2

    return Result.true(
        mode="exact",
        value=is_local_base,
        justification=[
            f"Candidate family {'IS' if is_local_base else 'is NOT'} a local base at {point!r}. "
            f"Cond1 (all in N(x))={cond1}, Cond2 (cofinal in N(x))={cond2}."
        ],
        metadata={
            "operator": "local_base_check",
            "point": point,
            "is_local_base": is_local_base,
            "cond1_all_neighborhoods": cond1,
            "cond1_failing_sets": failing_1,
            "cond2_cofinal": cond2,
            "cond2_uncovered_count": len(cond2_failures),
            "candidate_size": len(cand),
            "neighborhood_count": len(nbhd_x),
            "cilt_iii_corridor": "neighborhood-systems",
            "v0_1_51_corridor_record": True,
        },
    )


def character_at_point(
    carrier: list,
    topology: list[frozenset],
    point: Any,
) -> Result:
    """Compute the character χ(x, X) — the minimum local base cardinality at x.

    For finite spaces this equals the size of the smallest local base at x,
    which is the set of open neighborhoods of x (the minimal local base).

    Parameters
    ----------
    carrier, topology, point:
        As above.
    """
    if point not in carrier:
        return Result.unknown(
            mode="symbolic",
            value="character_at_point",
            justification=[f"Point {point!r} not in carrier."],
            metadata={"operator": "character_at_point", "point": point},
        )

    open_sets = [frozenset(u) for u in topology]
    # Minimal local base = open neighborhoods of x
    open_nbhd = sorted(
        [u for u in open_sets if point in u],
        key=lambda s: (len(s), sorted(repr(e) for e in s)),
    )
    chi = len(open_nbhd)

    return Result.true(
        mode="exact",
        value=chi,
        justification=[
            f"χ({point!r}, X) = {chi}: the minimal local base at {point!r} "
            f"consists of {chi} open neighborhood(s)."
        ],
        metadata={
            "operator": "character_at_point",
            "point": point,
            "character": chi,
            "open_neighborhoods": [sorted(repr(e) for e in u) for u in open_nbhd],
            "cilt_iii_corridor": "neighborhood-systems",
            "v0_1_51_corridor_record": True,
        },
    )


def topology_from_neighborhood_system(
    carrier: list,
    nbhd_system: dict[Any, list[frozenset]],
) -> Result:
    """Recover the topology from an explicit neighborhood system.

    A set U is open iff U ∈ N(x) for every x ∈ U.

    Parameters
    ----------
    carrier:
        Finite point set.
    nbhd_system:
        A dict mapping each point to its list of neighborhoods.
    """
    all_subsets = _power_subsets(carrier)
    open_sets = []
    for s in all_subsets:
        if len(s) == 0:
            open_sets.append(s)  # empty set is always open
            continue
        if all(s in [frozenset(n) for n in nbhd_system.get(x, [])] for x in s):
            open_sets.append(s)

    return Result.true(
        mode="exact",
        value=[sorted(repr(e) for e in u) for u in sorted(open_sets, key=len)],
        justification=[
            f"Recovered topology has {len(open_sets)} open set(s) from the neighborhood system."
        ],
        metadata={
            "operator": "topology_from_neighborhood_system",
            "open_set_count": len(open_sets),
            "carrier_size": len(carrier),
            "cilt_iii_corridor": "neighborhood-systems",
            "v0_1_51_corridor_record": True,
        },
    )


def analyze_neighborhood_system(
    carrier: list,
    topology: list[frozenset],
    point: Any | None = None,
) -> Result:
    """Master's-level corridor entry-point for v0.1.51.

    - With point: full axiom check + neighborhood system + character at that point.
    - Without point: character profile for all points in the carrier.

    Parameters
    ----------
    carrier:
        Finite point set.
    topology:
        List of open sets.
    point:
        Optional point for focused analysis.
    """
    open_sets = [frozenset(u) for u in topology]

    if point is not None:
        axioms = neighborhood_system_axioms(carrier, open_sets, point)
        nbhd = neighborhood_system(carrier, open_sets, point)
        chi = character_at_point(carrier, open_sets, point)
        return Result.true(
            mode="exact",
            value={
                "point": point,
                "axioms": axioms.value,
                "neighborhood_count": nbhd.metadata["neighborhood_count"],
                "character": chi.value,
            },
            justification=[
                f"Full neighborhood-system analysis at {point!r}: "
                f"axioms all pass={axioms.value['all_axioms']}, "
                f"|N({point!r})|={nbhd.metadata['neighborhood_count']}, "
                f"χ={chi.value}."
            ],
            metadata={
                "operator": "analyze_neighborhood_system",
                "point": point,
                "axioms_all_pass": axioms.value["all_axioms"],
                "neighborhood_count": nbhd.metadata["neighborhood_count"],
                "character": chi.value,
                "carrier_size": len(carrier),
                "cilt_iii_corridor": "neighborhood-systems",
                "v0_1_51_corridor_record": True,
            },
        )

    # Full profile: character at every point
    profile = {}
    for x in carrier:
        chi = character_at_point(carrier, open_sets, x)
        profile[repr(x)] = chi.value

    return Result.true(
        mode="exact",
        value=profile,
        justification=[
            f"Character profile for all {len(carrier)} points. "
            f"Max χ = {max(profile.values()) if profile else 0}."
        ],
        metadata={
            "operator": "analyze_neighborhood_system",
            "carrier_size": len(carrier),
            "max_character": max(profile.values()) if profile else 0,
            "min_character": min(profile.values()) if profile else 0,
            "cilt_iii_corridor": "neighborhood-systems",
            "v0_1_51_corridor_record": True,
        },
    )


__all__ = [
    "neighborhood_system_axioms",
    "neighborhood_system",
    "local_base_check",
    "character_at_point",
    "topology_from_neighborhood_system",
    "analyze_neighborhood_system",
]
