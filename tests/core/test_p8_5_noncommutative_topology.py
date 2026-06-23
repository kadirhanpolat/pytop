"""Tests for P8.5: noncommutative_topology computational engines.

Functions tested: k0_group_matrix_algebra, spectral_dimension_finite,
k1_group_matrix_algebra
"""
import math

import pytest

from pytop import k0_group_matrix_algebra, k1_group_matrix_algebra, spectral_dimension_finite

# ---------------------------------------------------------------------------
# k0_group_matrix_algebra
# ---------------------------------------------------------------------------

class TestK0GroupMatrixAlgebra:
    def test_n1_identity_class(self):
        result = k0_group_matrix_algebra(1)
        assert result["identity_class"] == 1

    def test_n3_identity_class(self):
        result = k0_group_matrix_algebra(3)
        assert result["identity_class"] == 3

    def test_n10_identity_class(self):
        result = k0_group_matrix_algebra(10)
        assert result["identity_class"] == 10

    def test_k0_rank_always_one(self):
        for n in [1, 2, 5, 100]:
            assert k0_group_matrix_algebra(n)["K0_rank"] == 1

    def test_generator_class_always_one(self):
        for n in [1, 3, 7]:
            assert k0_group_matrix_algebra(n)["generator_class"] == 1

    def test_morita_equivalent_to_q(self):
        for n in [1, 2, 4]:
            assert k0_group_matrix_algebra(n)["morita_equivalent_to_Q"] is True

    def test_description_is_string(self):
        result = k0_group_matrix_algebra(5)
        assert isinstance(result["description"], str)

    def test_invalid_n_raises(self):
        with pytest.raises(ValueError):
            k0_group_matrix_algebra(0)

    def test_negative_n_raises(self):
        with pytest.raises(ValueError):
            k0_group_matrix_algebra(-1)

    def test_return_keys_present(self):
        result = k0_group_matrix_algebra(2)
        for key in ("K0_rank", "generator_class", "identity_class",
                    "morita_equivalent_to_Q", "description"):
            assert key in result


# ---------------------------------------------------------------------------
# spectral_dimension_finite
# ---------------------------------------------------------------------------

class TestSpectralDimensionFinite:
    def test_empty_eigenvalues_returns_zero(self):
        result = spectral_dimension_finite([])
        assert result["spectral_dimension"] == 0.0

    def test_single_eigenvalue_insufficient(self):
        result = spectral_dimension_finite([1.0])
        assert result["spectral_dimension"] == 0.0

    def test_linear_growth_gives_dim_two(self):
        # N(λ) ~ λ ↔ d_s = 2 (Weyl law for 2D)
        evs = list(range(1, 60))
        result = spectral_dimension_finite(evs)
        assert abs(result["spectral_dimension"] - 2.0) < 0.5

    def test_square_root_growth_gives_dim_one(self):
        # Eigenvalues k² (1D Laplacian on circle): N(λ) ~ √λ → d_s ≈ 1
        evs = sorted([k ** 2 for k in range(1, 30)])
        result = spectral_dimension_finite(evs)
        assert abs(result["spectral_dimension"] - 1.0) < 0.5

    def test_return_keys_present(self):
        result = spectral_dimension_finite([1.0, 2.0, 3.0])
        for key in ("spectral_dimension", "n_positive_eigenvalues", "slope"):
            assert key in result

    def test_n_positive_eigenvalues_count(self):
        result = spectral_dimension_finite([0.0, 0.0, 1.0, 2.0, 3.0])
        assert result["n_positive_eigenvalues"] == 3

    def test_threshold_filters_near_zero(self):
        evs = [1e-12, 1e-11, 1.0, 2.0, 3.0]
        result = spectral_dimension_finite(evs, threshold=1e-10)
        assert result["n_positive_eigenvalues"] == 3

    def test_spectral_dim_nonneg(self):
        result = spectral_dimension_finite([1.0, 2.0, 4.0, 8.0])
        assert result["spectral_dimension"] >= 0.0

    def test_slope_finite(self):
        result = spectral_dimension_finite([1.0, 2.0, 3.0])
        assert math.isfinite(result["slope"])


# ---------------------------------------------------------------------------
# k1_group_matrix_algebra
# ---------------------------------------------------------------------------

class TestK1GroupMatrixAlgebra:
    def test_torsion_part_is_z2(self):
        for n in [1, 2, 3, 10]:
            assert k1_group_matrix_algebra(n)["torsion_part"] == "ℤ/2"

    def test_k1_description_is_string(self):
        result = k1_group_matrix_algebra(2)
        assert isinstance(result["K1_description"], str)

    def test_morita_invariant_true(self):
        for n in [1, 2, 5]:
            assert k1_group_matrix_algebra(n)["morita_invariant"] is True

    def test_free_part_description_is_string(self):
        result = k1_group_matrix_algebra(3)
        assert isinstance(result["free_part_description"], str)

    def test_determinant_isomorphism_key_present(self):
        result = k1_group_matrix_algebra(4)
        assert "determinant_isomorphism" in result

    def test_invalid_n_raises(self):
        with pytest.raises(ValueError):
            k1_group_matrix_algebra(0)

    def test_return_keys_present(self):
        result = k1_group_matrix_algebra(2)
        for key in ("K1_description", "torsion_part", "free_part_description",
                    "determinant_isomorphism", "morita_invariant", "description"):
            assert key in result

    def test_description_mentions_morita(self):
        result = k1_group_matrix_algebra(2)
        assert "Morita" in result["description"]
