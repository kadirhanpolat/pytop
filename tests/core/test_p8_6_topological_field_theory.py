"""Tests for P8.6: topological_field_theory computational engines.

Functions tested: cobordism_from_handles, tqft_dimension_2d, handle_signature_tft
"""
import pytest

from pytop import cobordism_from_handles, handle_signature_tft, tqft_dimension_2d

# ---------------------------------------------------------------------------
# cobordism_from_handles
# ---------------------------------------------------------------------------

class TestCobordismFromHandles:
    def test_sphere_euler_characteristic(self):
        # S²: one 0-handle + one 2-handle → χ = 2
        result = cobordism_from_handles(1, 0, 1)
        assert result["euler_characteristic"] == 2

    def test_sphere_genus(self):
        result = cobordism_from_handles(1, 0, 1)
        assert result["genus"] == 0

    def test_torus_euler_characteristic(self):
        # T²: one 0-handle + two 1-handles + one 2-handle → χ = 0
        result = cobordism_from_handles(1, 2, 1)
        assert result["euler_characteristic"] == 0

    def test_torus_genus(self):
        result = cobordism_from_handles(1, 2, 1)
        assert result["genus"] == 1

    def test_genus2_surface(self):
        # Σ₂: χ = -2, genus = 2 → n₀-n₁+n₂ = 1-4+1 = -2
        result = cobordism_from_handles(1, 4, 1)
        assert result["euler_characteristic"] == -2
        assert result["genus"] == 2

    def test_handle_counts_in_result(self):
        result = cobordism_from_handles(1, 1, 1)
        assert result["handle_counts"]["zero_handles"] == 1
        assert result["handle_counts"]["one_handles"] == 1
        assert result["handle_counts"]["two_handles"] == 1

    def test_is_connected_with_zero_handle(self):
        result = cobordism_from_handles(1, 0, 1)
        assert result["is_connected"] is True

    def test_not_connected_without_zero_handle(self):
        result = cobordism_from_handles(0, 1, 1)
        assert result["is_connected"] is False

    def test_return_keys_present(self):
        result = cobordism_from_handles(1, 0, 1)
        for key in ("euler_characteristic", "genus", "handle_counts",
                    "is_closed", "is_connected"):
            assert key in result

    def test_odd_euler_char_genus_is_none(self):
        # χ = 1 (odd) → no oriented genus → genus = None
        result = cobordism_from_handles(1, 0, 0)
        # χ = 1, 2 - 1 = 1, odd → genus = None
        assert result["genus"] is None

    def test_disk_euler_char(self):
        # Disk D²: one 0-handle, no others → χ = 1
        result = cobordism_from_handles(1, 0, 0)
        assert result["euler_characteristic"] == 1


# ---------------------------------------------------------------------------
# tqft_dimension_2d
# ---------------------------------------------------------------------------

class TestTqftDimension2d:
    def test_sphere_bool_tft(self):
        result = tqft_dimension_2d(0)
        assert result["dim_boolean_tft"] == 1

    def test_sphere_a2_tft(self):
        result = tqft_dimension_2d(0)
        assert result["dim_A2_tft"] == 2

    def test_torus_bool_tft(self):
        result = tqft_dimension_2d(1)
        assert result["dim_boolean_tft"] == 1

    def test_torus_a2_tft(self):
        result = tqft_dimension_2d(1)
        assert result["dim_A2_tft"] == 1

    def test_genus2_a2_tft_zero(self):
        result = tqft_dimension_2d(2)
        assert result["dim_A2_tft"] == 0

    def test_genus_in_result(self):
        result = tqft_dimension_2d(3)
        assert result["genus"] == 3

    def test_euler_characteristic_sphere(self):
        result = tqft_dimension_2d(0)
        assert result["euler_characteristic"] == 2

    def test_euler_characteristic_torus(self):
        result = tqft_dimension_2d(1)
        assert result["euler_characteristic"] == 0

    def test_negative_genus_raises(self):
        with pytest.raises(ValueError):
            tqft_dimension_2d(-1)

    def test_boundary_components_reduce_euler_char(self):
        # S¹ (genus=0, 1 boundary): χ = 2 - 0 - 1 = 1
        result = tqft_dimension_2d(0, n_boundary_components=1)
        assert result["euler_characteristic"] == 1

    def test_return_keys_present(self):
        result = tqft_dimension_2d(0)
        for key in ("genus", "n_boundary_components", "euler_characteristic",
                    "dim_boolean_tft", "dim_A2_tft"):
            assert key in result


# ---------------------------------------------------------------------------
# handle_signature_tft
# ---------------------------------------------------------------------------

class TestHandleSignatureTft:
    def test_cp2_euler_char(self):
        # CP²: n₀=n₂=n₄=1, rest 0 → χ = 1 - 0 + 1 - 0 + 1 = 3
        result = handle_signature_tft(1, 0, 1, 0, 1)
        assert result["euler_characteristic"] == 3

    def test_s4_euler_char(self):
        # S⁴: one 0-handle + one 4-handle → χ = 2
        result = handle_signature_tft(1, 0, 0, 0, 1)
        assert result["euler_characteristic"] == 2

    def test_b2_count_correct(self):
        result = handle_signature_tft(1, 0, 3, 0, 1)
        assert result["betti_numbers"]["b2"] == 3

    def test_simply_connected_when_no_1handles(self):
        result = handle_signature_tft(1, 0, 2, 0, 1)
        assert result["is_simply_connected"] is True

    def test_not_simply_connected_with_1handles(self):
        result = handle_signature_tft(1, 1, 2, 1, 1)
        assert result["is_simply_connected"] is False

    def test_all_betti_keys_present(self):
        result = handle_signature_tft(1, 0, 1, 0, 1)
        for k in ("b0", "b1", "b2", "b3", "b4"):
            assert k in result["betti_numbers"]

    def test_handle_counts_in_result(self):
        result = handle_signature_tft(1, 2, 3, 2, 1)
        hc = result["handle_counts"]
        assert hc["zero"] == 1
        assert hc["two"] == 3
        assert hc["four"] == 1

    def test_signature_description_is_string(self):
        result = handle_signature_tft(1, 0, 1, 0, 1)
        assert isinstance(result["signature_description"], str)

    def test_return_keys_present(self):
        result = handle_signature_tft(1, 0, 0, 0, 1)
        for key in ("euler_characteristic", "betti_numbers",
                    "signature_description", "is_simply_connected", "handle_counts"):
            assert key in result

    def test_k3_surface_handles(self):
        # K3 surface: χ=24, one 0-handle, no 1-handles, 22 2-handles, one 4-handle
        result = handle_signature_tft(1, 0, 22, 0, 1)
        assert result["euler_characteristic"] == 24
        assert result["is_simply_connected"] is True
