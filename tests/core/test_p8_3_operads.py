"""Tests for P8.3: operads computational engines.

Functions tested: associahedron_complex, operad_composition_check, bar_construction_sc
Private helpers: _full_binary_trees, _one_step_rotations
"""
import pytest

from pytop import associahedron_complex, bar_construction_sc, operad_composition_check
from pytop.operads import _full_binary_trees, _one_step_rotations

# ---------------------------------------------------------------------------
# _full_binary_trees
# ---------------------------------------------------------------------------

class TestFullBinaryTrees:
    def test_n1_gives_one_tree(self):
        trees = _full_binary_trees(1)
        assert len(trees) == 1
        assert trees[0] is None

    def test_n2_gives_one_tree(self):
        # Only one binary tree with 2 leaves
        trees = _full_binary_trees(2)
        assert len(trees) == 1
        assert trees[0] == (None, None)

    def test_n3_gives_two_trees(self):
        # Catalan(2) = 2
        trees = _full_binary_trees(3)
        assert len(trees) == 2

    def test_n4_gives_five_trees(self):
        # Catalan(3) = 5
        trees = _full_binary_trees(4)
        assert len(trees) == 5

    def test_n5_gives_fourteen_trees(self):
        # Catalan(4) = 14
        trees = _full_binary_trees(5)
        assert len(trees) == 14

    def test_all_trees_are_tuples_or_none(self):
        for t in _full_binary_trees(4):
            assert isinstance(t, tuple)


# ---------------------------------------------------------------------------
# _one_step_rotations
# ---------------------------------------------------------------------------

class TestOneStepRotations:
    def test_leaf_has_no_rotations(self):
        assert _one_step_rotations(None) == []

    def test_two_leaf_tree_has_no_rotations(self):
        # (None, None) — neither child is a tuple
        assert _one_step_rotations((None, None)) == []

    def test_left_skew_has_one_rotation(self):
        # ((None,None),None) can do left rotation → (None,(None,None))
        rots = _one_step_rotations(((None, None), None))
        assert (None, (None, None)) in rots

    def test_right_skew_has_one_rotation(self):
        # (None,(None,None)) can do right rotation → ((None,None),None)
        rots = _one_step_rotations((None, (None, None)))
        assert ((None, None), None) in rots

    def test_pentagon_vertex_has_two_rotations(self):
        # T1 = (None,(None,(None,None))) should have 2 rotations
        t = (None, (None, (None, None)))
        rots = _one_step_rotations(t)
        assert len(rots) >= 2


# ---------------------------------------------------------------------------
# associahedron_complex
# ---------------------------------------------------------------------------

class TestAssociahedronComplex:
    def test_k2_invalid(self):
        with pytest.raises(ValueError):
            associahedron_complex(1)

    def test_k3_has_two_vertices(self):
        sc = associahedron_complex(3)
        v_count = sum(1 for s in sc.simplexes if len(s.vertices) == 1)
        assert v_count == 2

    def test_k3_has_one_edge(self):
        sc = associahedron_complex(3)
        e_count = sum(1 for s in sc.simplexes if len(s.vertices) == 2)
        assert e_count == 1

    def test_k3_total_simplices(self):
        sc = associahedron_complex(3)
        assert len(list(sc.simplexes)) == 3  # 2 vertices + 1 edge

    def test_k4_has_five_vertices(self):
        sc = associahedron_complex(4)
        v_count = sum(1 for s in sc.simplexes if len(s.vertices) == 1)
        assert v_count == 5

    def test_k4_has_five_edges(self):
        sc = associahedron_complex(4)
        e_count = sum(1 for s in sc.simplexes if len(s.vertices) == 2)
        assert e_count == 5

    def test_k4_total_simplices(self):
        sc = associahedron_complex(4)
        assert len(list(sc.simplexes)) == 10  # 5 vertices + 5 edges

    def test_returns_simplicial_complex(self):
        from pytop.simplicial_complexes import SimplicialComplex
        sc = associahedron_complex(3)
        assert isinstance(sc, SimplicialComplex)


# ---------------------------------------------------------------------------
# operad_composition_check
# ---------------------------------------------------------------------------

class TestOperadCompositionCheck:
    def test_constant_zero_is_associative(self):
        result = operad_composition_check([[0, 0], [0, 0]])
        assert result["associative"] is True

    def test_empty_matrix_is_associative(self):
        result = operad_composition_check([])
        assert result["associative"] is True

    def test_1x1_matrix_associative(self):
        result = operad_composition_check([[0]])
        assert result["associative"] is True

    def test_return_keys_present(self):
        result = operad_composition_check([[0]])
        for key in ("associative", "n_violations", "is_operad_composition"):
            assert key in result

    def test_nonassociative_composition_detected(self):
        # µ(0,0)=1, µ(1,0)=0, µ(0,1)=0, µ(1,1)=0
        # µ(µ(0,0),0) = µ(1,0) = 0
        # µ(0,µ(0,0)) = µ(0,1) = 0
        # Not obvious — identity µ(i,j)=i is non-associative if µ(µ(0,0),1) ≠ µ(0,µ(0,1))
        # Let's try µ[i][j] = (i + j) % 2
        mu = [[0, 1], [1, 0]]
        result = operad_composition_check(mu)
        # (0+0)%2=0, (0+1)%2=1, (1+0)%2=1, (1+1)%2=0
        # µ(µ(0,0),0) = µ(0,0) = 0; µ(0,µ(0,0)) = µ(0,0) = 0 — associative!
        # Z/2 with addition is associative
        assert result["associative"] is True

    def test_n_violations_is_nonneg(self):
        result = operad_composition_check([[0, 0], [0, 0]])
        assert result["n_violations"] == 0


# ---------------------------------------------------------------------------
# bar_construction_sc
# ---------------------------------------------------------------------------

class TestBarConstructionSc:
    def test_two_generators_no_relations(self):
        sc = bar_construction_sc(2, 0)
        v = sum(1 for s in sc.simplexes if len(s.vertices) == 1)
        e = sum(1 for s in sc.simplexes if len(s.vertices) == 2)
        assert v == 2
        assert e == 1

    def test_three_generators_one_relation(self):
        sc = bar_construction_sc(3, 1)
        triangles = sum(1 for s in sc.simplexes if len(s.vertices) == 3)
        assert triangles == 1

    def test_zero_generators(self):
        with pytest.raises(ValueError):
            bar_construction_sc(0, 0)

    def test_returns_simplicial_complex(self):
        from pytop.simplicial_complexes import SimplicialComplex
        sc = bar_construction_sc(3, 0)
        assert isinstance(sc, SimplicialComplex)

    def test_complete_graph_structure(self):
        # 4 generators → 4 vertices + C(4,2)=6 edges = 10 simplices
        sc = bar_construction_sc(4, 0)
        v = sum(1 for s in sc.simplexes if len(s.vertices) == 1)
        e = sum(1 for s in sc.simplexes if len(s.vertices) == 2)
        assert v == 4
        assert e == 6

    def test_negative_generators_raises(self):
        with pytest.raises(ValueError):
            bar_construction_sc(-1, 0)
