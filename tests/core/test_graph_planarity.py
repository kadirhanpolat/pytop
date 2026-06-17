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
