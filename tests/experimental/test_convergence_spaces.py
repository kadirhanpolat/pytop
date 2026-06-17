"""Tests for finite convergence spaces (experimental)."""

from __future__ import annotations

from itertools import combinations

from pytop.experimental.convergence_spaces import (
    ConvergenceSpace,
    convergence_from_topology,
    grill_of_filter,
    is_continuous_convergence_map,
    is_convergence_space,
    is_pretopology,
    is_pseudotopology,
    is_topological,
    topology_from_convergence,
)


def _nonempty_subsets(elements):
    members = list(elements)
    for size in range(1, len(members) + 1):
        for combo in combinations(members, size):
            yield frozenset(combo)


def _pretopology_from_neighborhoods(neighborhoods):
    points = frozenset(neighborhoods)
    convergences = []
    for point, neighborhood in neighborhoods.items():
        for subset in _nonempty_subsets(neighborhood):
            convergences.append((subset, point))
    return ConvergenceSpace(points, convergences)


# --------------------------------------------------------------------------
# Topology -> convergence -> topology round trip
# --------------------------------------------------------------------------

SIERPINSKI_OPENS = [set(), {0}, {0, 1}]


def test_sierpinski_is_topological():
    space = convergence_from_topology({0, 1}, SIERPINSKI_OPENS)
    assert is_convergence_space(space)
    assert is_pretopology(space)
    assert is_pseudotopology(space)
    assert is_topological(space)


def test_topology_round_trip_sierpinski():
    space = convergence_from_topology({0, 1}, SIERPINSKI_OPENS)
    recovered = topology_from_convergence(space)
    assert recovered == frozenset(frozenset(o) for o in SIERPINSKI_OPENS)


def test_topology_round_trip_discrete():
    discrete_opens = [set(), {0}, {1}, {0, 1}]
    space = convergence_from_topology({0, 1}, discrete_opens)
    assert is_topological(space)
    assert topology_from_convergence(space) == frozenset(
        frozenset(o) for o in discrete_opens
    )


# --------------------------------------------------------------------------
# A pretopology that is not a topology
# --------------------------------------------------------------------------

def test_pretopology_not_topological():
    # U_0 = {0,1} but 1 in U_0 while U_1 = {1,2} is not contained in U_0.
    space = _pretopology_from_neighborhoods(
        {0: {0, 1}, 1: {1, 2}, 2: {2}}
    )
    assert is_convergence_space(space)
    assert is_pretopology(space)
    assert not is_topological(space)


def test_topology_from_non_topological_raises():
    space = _pretopology_from_neighborhoods({0: {0, 1}, 1: {1, 2}, 2: {2}})
    try:
        topology_from_convergence(space)
    except ValueError:
        return
    raise AssertionError("expected ValueError for a non-topological convergence space")


# --------------------------------------------------------------------------
# A convergence space that is not a pretopology
# --------------------------------------------------------------------------

def test_convergence_space_not_pretopology():
    # At 0 the convergent kernels have two maximal elements {0,1} and {0,2}
    # but {0,1,2} does not converge -> not a pretopology / pseudotopology.
    convergences = []
    for subset in _nonempty_subsets({0, 1}):
        convergences.append((subset, 0))
    for subset in _nonempty_subsets({0, 2}):
        convergences.append((subset, 0))
    convergences.append((frozenset({1}), 1))
    convergences.append((frozenset({2}), 2))
    space = ConvergenceSpace({0, 1, 2}, convergences)

    assert is_convergence_space(space)
    assert not is_pretopology(space)
    assert not is_pseudotopology(space)


# --------------------------------------------------------------------------
# Failure of the convergence-space axioms
# --------------------------------------------------------------------------

def test_missing_point_filter_fails_axiom():
    # {1} does not converge to 1 -> centered axiom fails.
    space = ConvergenceSpace({0, 1}, [(frozenset({0}), 0)])
    assert not is_convergence_space(space)


# --------------------------------------------------------------------------
# Continuity
# --------------------------------------------------------------------------

def test_identity_is_continuous():
    space = convergence_from_topology({0, 1}, SIERPINSKI_OPENS)
    assert is_continuous_convergence_map(space, space, {0: 0, 1: 1})


def test_sierpinski_swap_is_not_continuous():
    space = convergence_from_topology({0, 1}, SIERPINSKI_OPENS)
    # swapping the open and the generic point breaks continuity
    assert not is_continuous_convergence_map(space, space, {0: 1, 1: 0})


# --------------------------------------------------------------------------
# Grill (dual of a filter)
# --------------------------------------------------------------------------

def test_grill_of_principal_filter():
    grill = grill_of_filter({0}, {0, 1})
    # sets meeting {0}: {0} and {0,1}
    assert grill == frozenset({frozenset({0}), frozenset({0, 1})})
