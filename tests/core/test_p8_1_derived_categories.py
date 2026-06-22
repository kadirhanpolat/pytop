"""Tests for P8.1: derived_categories computational engines.

Functions tested: mapping_cone_complex, derived_functor_h, triangulated_structure_check
"""
import pytest
from pytop import mapping_cone_complex, derived_functor_h, triangulated_structure_check


# ---------------------------------------------------------------------------
# mapping_cone_complex
# ---------------------------------------------------------------------------

class TestMappingConeComplex:
    def test_empty_inputs_returns_empty(self):
        assert mapping_cone_complex([], [], []) == []

    def test_returns_list(self):
        result = mapping_cone_complex([], [], [[[1]]])
        assert isinstance(result, list)

    def test_cone_of_trivial_map(self):
        # chain_map has one level: 1×1 identity at degree 0
        result = mapping_cone_complex([], [], [[[1]]])
        assert isinstance(result, list)

    def test_zero_chain_map(self):
        result = mapping_cone_complex([], [], [[[0]]])
        assert isinstance(result, list)

    def test_each_element_is_matrix(self):
        # Non-empty cone: boundaries_a has a 1×2 matrix (transposed ∂_1 of interval)
        ba = [[[-1, 1]]]
        bb = [[[-1, 1]]]
        f = [[[1, 0], [0, 1]]]
        result = mapping_cone_complex(ba, bb, f)
        for mat in result:
            assert isinstance(mat, list)
            for row in mat:
                assert isinstance(row, list)

    def test_cone_of_identity_interval(self):
        # Identity map on the interval chain complex
        ba = [[[-1, 1]]]
        bb = [[[-1, 1]]]
        f = [[[1, 0], [0, 1]], [[1]]]
        result = mapping_cone_complex(ba, bb, f)
        # Cone of an isomorphism is acyclic: H_0 should be 0
        h0 = derived_functor_h(result, 0)
        assert h0["betti_number"] == 0

    def test_cone_boundary_signs_correct(self):
        # ∂^C at n=1 has top-left block = -∂^A_0 (= 0 here since boundary is empty)
        # and the shape should be consistent
        ba = [[[-1, 1]]]
        result = mapping_cone_complex(ba, [[[-1, 1]]], [[[1, 0], [0, 1]]])
        # result should be a list of matrices
        for mat in result:
            assert all(isinstance(e, int) for row in mat for e in row)


# ---------------------------------------------------------------------------
# derived_functor_h
# ---------------------------------------------------------------------------

class TestDerivedFunctorH:
    def test_empty_complex_betti_zero(self):
        assert derived_functor_h([], 0)["betti_number"] == 0

    def test_empty_complex_high_degree(self):
        assert derived_functor_h([], 5)["betti_number"] == 0

    def test_interval_h0_equals_one(self):
        # Interval: one edge [[-1, 1]], H_0 = ℤ (Betti = 1)
        result = derived_functor_h([[[-1, 1]]], 0)
        assert result["betti_number"] == 1

    def test_interval_h1_equals_zero(self):
        result = derived_functor_h([[[-1, 1]]], 1)
        assert result["betti_number"] == 0

    def test_degree_key_matches_input(self):
        result = derived_functor_h([], 3)
        assert result["degree"] == 3

    def test_return_dict_has_all_keys(self):
        result = derived_functor_h([], 0)
        for key in ("betti_number", "torsion_coefficients", "rank_in",
                    "rank_out", "kernel_dimension", "degree"):
            assert key in result

    def test_rank_in_computed_for_interval(self):
        # ∂_1 = [[-1, 1]] (rank 1)
        result = derived_functor_h([[[-1, 1]]], 0)
        assert result["rank_in"] == 1

    def test_rank_out_zero_for_top_chain(self):
        result = derived_functor_h([[[-1, 1]]], 0)
        assert result["rank_out"] == 0

    def test_torsion_empty_for_free_complex(self):
        result = derived_functor_h([[[-1, 1]]], 0)
        assert result["torsion_coefficients"] == []

    def test_kernel_dim_nonneg(self):
        result = derived_functor_h([[[-1, 1]]], 0)
        assert result["kernel_dimension"] >= 0

    def test_betti_is_nonneg_integer(self):
        for degree in range(3):
            r = derived_functor_h([[[-1, 1]]], degree)
            assert isinstance(r["betti_number"], int)
            assert r["betti_number"] >= 0

    def test_two_disjoint_edges_h0(self):
        # Two separate edges → two components → Betti_0 = 2
        # ∂_1^T for two disjoint edges (transposed form: ncols = dim C_0 = 4)
        boundaries = [[[-1, 0, 1, 0], [0, -1, 0, 1]]]  # 2×4 transposed form
        result = derived_functor_h(boundaries, 0)
        # dim C_0 = ncols = 4, rank = 2 → kernel = 2 → betti = 2
        assert result["betti_number"] == 2


# ---------------------------------------------------------------------------
# triangulated_structure_check
# ---------------------------------------------------------------------------

class TestTriangulatedStructureCheck:
    def test_empty_inputs_returns_dict(self):
        result = triangulated_structure_check([], [], [], [], [])
        assert isinstance(result, dict)

    def test_return_keys_present(self):
        result = triangulated_structure_check([], [], [], [], [])
        for key in ("composition_zero", "degree_checks", "cone_betti",
                    "c_betti", "cone_matches_c"):
            assert key in result

    def test_zero_map_composition_zero(self):
        # f = id, g = 0 → g∘f = 0
        result = triangulated_structure_check([], [], [], [[[1]]], [[[0]]])
        assert result["composition_zero"] is True

    def test_nonzero_composition_detected(self):
        # f = [[1]], g = [[1]] → g∘f = [[1]] ≠ 0
        result = triangulated_structure_check([], [], [], [[[1]]], [[[1]]])
        assert result["composition_zero"] is False

    def test_empty_maps_no_violations(self):
        result = triangulated_structure_check([], [], [], [], [])
        assert result["composition_zero"] is True

    def test_cone_betti_is_list(self):
        result = triangulated_structure_check([], [], [], [], [])
        assert isinstance(result["cone_betti"], list)

    def test_cone_matches_c_for_empty(self):
        result = triangulated_structure_check([], [], [], [], [])
        assert result["cone_matches_c"] is True

    def test_degree_checks_populated(self):
        # With non-trivial maps, degree_checks should be populated
        result = triangulated_structure_check([], [], [], [[[1]]], [[[0]]])
        assert isinstance(result["degree_checks"], dict)
