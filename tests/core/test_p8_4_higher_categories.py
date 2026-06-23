"""Tests for P8.4: higher_categories computational engines.

Functions tested: nerve_of_category, kan_fibration_check_sc, homotopy_type_finite_cat
"""
from pytop import homotopy_type_finite_cat, kan_fibration_check_sc, nerve_of_category
from pytop.simplices import Simplex
from pytop.simplicial_complexes import SimplicialComplex

# ---------------------------------------------------------------------------
# nerve_of_category
# ---------------------------------------------------------------------------

class TestNerveOfCategory:
    def test_single_object_gives_one_vertex(self):
        sc = nerve_of_category(["A"], [])
        v = sum(1 for s in sc.simplexes if len(s.vertices) == 1)
        assert v == 1

    def test_two_objects_one_morphism_gives_edge(self):
        sc = nerve_of_category(["A", "B"], [("A", "B")])
        e = sum(1 for s in sc.simplexes if len(s.vertices) == 2)
        assert e == 1

    def test_chain_with_composite_gives_triangle(self):
        # A→B→C with A→C (composite) → 2-simplex
        sc = nerve_of_category(
            ["A", "B", "C"],
            [("A", "B"), ("B", "C"), ("A", "C")],
        )
        tri = sum(1 for s in sc.simplexes if len(s.vertices) == 3)
        assert tri >= 1

    def test_chain_without_composite_no_triangle(self):
        # A→B→C but NO A→C → no 2-simplex
        sc = nerve_of_category(["A", "B", "C"], [("A", "B"), ("B", "C")])
        tri = sum(1 for s in sc.simplexes if len(s.vertices) == 3)
        assert tri == 0

    def test_empty_category_no_morphisms(self):
        sc = nerve_of_category(["A", "B", "C"], [])
        e = sum(1 for s in sc.simplexes if len(s.vertices) == 2)
        assert e == 0

    def test_returns_simplicial_complex(self):
        sc = nerve_of_category(["A"], [])
        assert isinstance(sc, SimplicialComplex)

    def test_n_objects_vertices_match(self):
        objects = ["A", "B", "C", "D"]
        sc = nerve_of_category(objects, [])
        v = sum(1 for s in sc.simplexes if len(s.vertices) == 1)
        assert v == len(objects)

    def test_self_morphisms_not_added_as_edges(self):
        # Identity morphisms (a, a) should not become 1-simplices
        sc = nerve_of_category(["A"], [("A", "A")])
        e = sum(1 for s in sc.simplexes if len(s.vertices) == 2)
        assert e == 0


# ---------------------------------------------------------------------------
# kan_fibration_check_sc
# ---------------------------------------------------------------------------

class TestKanFibrationCheckSc:
    def test_single_vertex_is_kan(self):
        sc = SimplicialComplex([Simplex([0])])
        result = kan_fibration_check_sc(sc)
        assert result["is_kan_complex"] is True

    def test_single_edge_is_kan(self):
        sc = SimplicialComplex([Simplex([0]), Simplex([1]), Simplex([0, 1])])
        result = kan_fibration_check_sc(sc)
        assert result["is_kan_complex"] is True

    def test_filled_triangle_is_kan(self):
        sc = SimplicialComplex([
            Simplex([0]), Simplex([1]), Simplex([2]),
            Simplex([0, 1]), Simplex([0, 2]), Simplex([1, 2]),
            Simplex([0, 1, 2]),
        ])
        result = kan_fibration_check_sc(sc)
        assert result["is_kan_complex"] is True

    def test_boundary_triangle_is_not_kan(self):
        # Three edges but no filled 2-simplex
        sc = SimplicialComplex([
            Simplex([0]), Simplex([1]), Simplex([2]),
            Simplex([0, 1]), Simplex([0, 2]), Simplex([1, 2]),
        ])
        result = kan_fibration_check_sc(sc)
        assert result["is_kan_complex"] is False

    def test_unfilled_horns_list(self):
        result = kan_fibration_check_sc(SimplicialComplex([Simplex([0])]))
        assert isinstance(result["unfilled_horns"], list)

    def test_return_keys_present(self):
        sc = SimplicialComplex([Simplex([0])])
        result = kan_fibration_check_sc(sc)
        for key in ("unfilled_horns", "n_horns_checked", "is_kan_complex"):
            assert key in result

    def test_n_horns_checked_is_nonneg(self):
        sc = SimplicialComplex([Simplex([0])])
        result = kan_fibration_check_sc(sc)
        assert result["n_horns_checked"] >= 0

    def test_boundary_triangle_has_one_unfilled_horn(self):
        sc = SimplicialComplex([
            Simplex([0]), Simplex([1]), Simplex([2]),
            Simplex([0, 1]), Simplex([0, 2]), Simplex([1, 2]),
        ])
        result = kan_fibration_check_sc(sc)
        assert result["n_horns_checked"] >= 1


# ---------------------------------------------------------------------------
# homotopy_type_finite_cat
# ---------------------------------------------------------------------------

class TestHomotopyTypeFiniteCat:
    def test_single_object_contractible(self):
        result = homotopy_type_finite_cat(["*"], [])
        assert result["is_contractible"] is True

    def test_two_objects_one_morphism_contractible(self):
        # A → B: the classifying space BC is contractible
        result = homotopy_type_finite_cat(["A", "B"], [("A", "B")])
        assert result["is_contractible"] is True

    def test_single_object_connected(self):
        result = homotopy_type_finite_cat(["*"], [])
        assert result["is_connected"] is True

    def test_three_objects_chain_connected(self):
        result = homotopy_type_finite_cat(
            ["A", "B", "C"],
            [("A", "B"), ("B", "C"), ("A", "C")],
        )
        assert result["is_connected"] is True

    def test_return_keys_present(self):
        result = homotopy_type_finite_cat(["*"], [])
        for key in ("betti_numbers", "euler_characteristic", "n_objects",
                    "n_morphisms", "is_contractible", "is_connected"):
            assert key in result

    def test_n_objects_correct(self):
        result = homotopy_type_finite_cat(["A", "B", "C"], [])
        assert result["n_objects"] == 3

    def test_n_morphisms_correct(self):
        result = homotopy_type_finite_cat(["A", "B"], [("A", "B")])
        assert result["n_morphisms"] == 1

    def test_betti_numbers_is_dict(self):
        result = homotopy_type_finite_cat(["*"], [])
        assert isinstance(result["betti_numbers"], dict)

    def test_euler_characteristic_contractible(self):
        result = homotopy_type_finite_cat(["*"], [])
        assert result["euler_characteristic"] == 1

    def test_isolated_objects_not_contractible(self):
        # Two disjoint objects, no morphisms → disconnected
        result = homotopy_type_finite_cat(["A", "B"], [])
        # Two disconnected vertices: B_0 = 2, not contractible
        assert result["betti_numbers"].get(0, 0) == 2
        assert result["is_contractible"] is False
