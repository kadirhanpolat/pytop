"""Coverage-targeted tests for neighborhood_systems.py (v0.5.1)."""
import pytest
from pytop.neighborhood_systems import (
    neighborhood_system_axioms,
    neighborhood_system,
    local_base_check,
    _open_sets_of,
    _neighborhood_system_from_topology,
    _axiom_finite_intersection,
    _axiom_superset_closed,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_DISCRETE_CARRIER = [1, 2]
_DISCRETE_TOPO = [frozenset(), frozenset({1}), frozenset({2}), frozenset({1, 2})]

_INDISCRETE_CARRIER = [1, 2]
_INDISCRETE_TOPO = [frozenset(), frozenset({1, 2})]


# ---------------------------------------------------------------------------
# _open_sets_of — direct call (line 31)
# ---------------------------------------------------------------------------

def test_open_sets_of_discrete():
    opens = _open_sets_of(_DISCRETE_CARRIER, _DISCRETE_TOPO)
    assert frozenset({1}) in opens
    assert frozenset({2}) in opens
    assert frozenset() in opens


def test_open_sets_of_indiscrete():
    opens = _open_sets_of(_INDISCRETE_CARRIER, _INDISCRETE_TOPO)
    assert len(opens) == 2


# ---------------------------------------------------------------------------
# _neighborhood_system_from_topology — direct call (lines 38-43)
# ---------------------------------------------------------------------------

def test_neighborhood_system_from_topology_discrete():
    nbhd = _neighborhood_system_from_topology(_DISCRETE_CARRIER, _DISCRETE_TOPO)
    assert 1 in nbhd
    assert 2 in nbhd
    # In discrete topology every non-empty set containing x is a neighborhood
    assert frozenset({1}) in nbhd[1]


def test_neighborhood_system_from_topology_indiscrete():
    nbhd = _neighborhood_system_from_topology(_INDISCRETE_CARRIER, _INDISCRETE_TOPO)
    # Only the whole space is open, so N(1) = {whole space} (only {1,2})
    assert frozenset({1, 2}) in nbhd[1]


# ---------------------------------------------------------------------------
# _axiom_finite_intersection — returns False (line 75)
# ---------------------------------------------------------------------------

def test_axiom_finite_intersection_fails():
    # {1,2} ∩ {2,3} = {2} not in the list → line 75
    nbhd = [frozenset({1, 2}), frozenset({2, 3})]
    assert _axiom_finite_intersection(nbhd) is False


def test_axiom_finite_intersection_passes():
    # Discrete at 1: neighborhoods are all supersets of {1}
    nbhd = [frozenset({1}), frozenset({1, 2})]
    # {1}∩{1,2}={1} ∈ nbhd → True
    assert _axiom_finite_intersection(nbhd) is True


# ---------------------------------------------------------------------------
# _axiom_superset_closed — returns False (line 85)
# ---------------------------------------------------------------------------

def test_axiom_superset_closed_fails():
    # nbhd = [{1}] on carrier [1,2,3]; {1,2} is a superset of {1} but not in nbhd
    carrier = [1, 2, 3]
    nbhd = [frozenset({1})]
    assert _axiom_superset_closed(carrier, nbhd) is False


def test_axiom_superset_closed_passes():
    # nbhd = [{1}, {1,2}] on carrier [1,2]; every superset of {1} that's a subset of {1,2} is in nbhd
    carrier = [1, 2]
    nbhd = [frozenset({1}), frozenset({1, 2})]
    assert _axiom_superset_closed(carrier, nbhd) is True


# ---------------------------------------------------------------------------
# local_base_check — point not in carrier (line 228)
# ---------------------------------------------------------------------------

def test_local_base_check_point_not_in_carrier():
    result = local_base_check(
        _DISCRETE_CARRIER,
        _DISCRETE_TOPO,
        point=99,  # not in carrier
        candidate_base=_DISCRETE_TOPO,
    )
    assert result.is_unknown


# ---------------------------------------------------------------------------
# neighborhood_system_axioms — normal paths
# ---------------------------------------------------------------------------

def test_neighborhood_system_axioms_discrete():
    result = neighborhood_system_axioms([1, 2], _DISCRETE_TOPO, 1)
    assert result.is_true
    assert result.value["all_axioms"] is True


def test_neighborhood_system_axioms_point_not_in_carrier():
    result = neighborhood_system_axioms([1, 2], _DISCRETE_TOPO, 99)
    assert result.is_unknown


# ---------------------------------------------------------------------------
# neighborhood_system — point not in carrier
# ---------------------------------------------------------------------------

def test_neighborhood_system_point_not_in_carrier():
    result = neighborhood_system([1, 2], _DISCRETE_TOPO, 99)
    assert result.is_unknown


def test_neighborhood_system_discrete():
    result = neighborhood_system([1, 2], _DISCRETE_TOPO, 1)
    assert result.is_true
