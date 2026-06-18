"""Known-answer tests for exact graph planarity and genus."""

from __future__ import annotations

from itertools import combinations

from pytop import graph_genus, is_planar
from pytop.graph_planarity import satisfies_planar_edge_bound


def _complete(n):
    return list(combinations(range(n), 2))


def _complete_bipartite(m, n):
    return [(i, m + j) for i in range(m) for j in range(n)]


def _cycle(n):
    return [(i, (i + 1) % n) for i in range(n)]


def _wheel(n):
    """Hub vertex ``n`` joined to an ``n``-cycle ``0..n-1`` — always planar."""
    return _cycle(n) + [(n, i) for i in range(n)]


PETERSEN = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 0),        # outer 5-cycle
    (5, 7), (7, 9), (9, 6), (6, 8), (8, 5),        # inner pentagram
    (0, 5), (1, 6), (2, 7), (3, 8), (4, 9),        # spokes
]


# --------------------------------------------------------------------------
# Planar graphs
# --------------------------------------------------------------------------

def test_k4_is_planar():
    assert is_planar(_complete(4)) is True
    assert graph_genus(_complete(4)) == 0


def test_cycle_is_planar():
    assert is_planar(_cycle(5)) is True


def test_tree_is_planar():
    assert is_planar([(0, 1), (1, 2), (1, 3), (3, 4)]) is True


def test_wheel_is_planar():
    spokes = [(5, i) for i in range(5)]
    assert is_planar(_cycle(5) + spokes) is True


def test_single_vertex_and_empty_are_planar():
    assert is_planar([], vertices=[0]) is True
    assert is_planar([]) is True


# --------------------------------------------------------------------------
# Non-planar graphs
# --------------------------------------------------------------------------

def test_k5_is_non_planar():
    assert is_planar(_complete(5)) is False
    assert graph_genus(_complete(5)) == 1


def test_k33_is_non_planar():
    assert is_planar(_complete_bipartite(3, 3)) is False
    assert graph_genus(_complete_bipartite(3, 3)) == 1


def test_petersen_is_non_planar():
    assert is_planar(PETERSEN) is False
    assert graph_genus(PETERSEN) == 1


# --------------------------------------------------------------------------
# Disconnected graphs: genus is additive over components
# --------------------------------------------------------------------------

def test_disconnected_two_triangles_planar():
    edges = _cycle(3) + [(3, 4), (4, 5), (5, 3)]
    assert is_planar(edges) is True


def test_disconnected_two_k5_has_genus_two():
    edges = _complete(5) + [(a + 5, b + 5) for a, b in _complete(5)]
    assert graph_genus(edges) == 2
    assert is_planar(edges) is False


# --------------------------------------------------------------------------
# Necessary edge bound (Euler)
# --------------------------------------------------------------------------

def test_planar_edge_bound():
    assert satisfies_planar_edge_bound(5, 10) is False           # K5: 10 > 3*5-6=9
    assert satisfies_planar_edge_bound(6, 9, bipartite=True) is False  # K3,3: 9 > 2*6-4=8
    assert satisfies_planar_edge_bound(4, 6) is True             # K4: 6 <= 3*4-6=6


# --------------------------------------------------------------------------
# Regression: cases whose full rotation-system space exceeds the cap, but which
# is_planar now decides cheaply (edge bound / early termination) instead of
# raising GraphPlanarityError. Locks in the v0.9.x performance pass.
# --------------------------------------------------------------------------

def test_dense_complete_graphs_decided_by_edge_bound():
    # K6 (search space 24^6 ~ 1.9e8) and K7 used to raise; the Euler edge bound
    # E > 3V-6 now rejects them with no search at all.
    assert is_planar(_complete(6)) is False
    assert is_planar(_complete(7)) is False
    assert is_planar(_complete(8)) is False


def test_dense_bipartite_decided_by_bipartite_bound():
    # K4,4: E=16 > 2*8-4=12 (bipartite bound) -> non-planar without any search.
    assert is_planar(_complete_bipartite(4, 4)) is False
    assert is_planar(_complete_bipartite(4, 5)) is False


def test_octahedron_is_planar():
    # K_{2,2,2}: 4-regular, planar, passes the edge bound (E = 3V-6 exactly), so
    # it exercises the rotation-system search path (with genus-0 early termination)
    # rather than the edge-bound shortcut.
    octa = [(i, j) for i, j in combinations(range(6), 2)
            if {i, j} not in ({0, 1}, {2, 3}, {4, 5})]
    assert is_planar(octa) is True
    assert graph_genus(octa) == 0


def test_small_wheel_is_planar():
    # A wheel is always planar; W6 (hub degree 6) is small enough to decide
    # regardless of enumeration order.
    assert is_planar(_wheel(6)) is True
    assert graph_genus(_wheel(6)) == 0
