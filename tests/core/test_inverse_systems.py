"""Tests for inverse_systems.py."""

import pytest
from pytop.inverse_systems import inverse_limit, inverse_system


SPACES = ["X_0", "X_1", "X_2"]
MAPS = ["f_01", "f_12"]


# ---------------------------------------------------------------------------
# inverse_system
# ---------------------------------------------------------------------------

class TestInverseSystem:
    def test_basic_chain(self):
        s = inverse_system(SPACES, MAPS)
        assert s is not None
        assert s["system_type"] == "inverse_system"

    def test_space_count(self):
        s = inverse_system(SPACES, MAPS)
        assert s["space_count"] == 3

    def test_bonding_map_count(self):
        s = inverse_system(SPACES, MAPS)
        assert s["bonding_map_count"] == 2

    def test_chain_like_true_for_n_minus_one_maps(self):
        s = inverse_system(SPACES, MAPS)
        assert s["is_chain_like"] is True

    def test_chain_like_false_for_wrong_map_count(self):
        s = inverse_system(SPACES, ["f_01"])
        assert s["is_chain_like"] is False

    def test_empty_system(self):
        s = inverse_system([], [])
        assert s["space_count"] == 0

    def test_invalid_spaces_returns_none(self):
        assert inverse_system("not_a_list", MAPS) is None

    def test_invalid_maps_returns_none(self):
        assert inverse_system(SPACES, "not_a_list") is None

    def test_spaces_normalized_to_strings(self):
        s = inverse_system([1, 2, 3], ["f", "g"])
        assert all(isinstance(x, str) for x in s["spaces"])

    def test_version_present(self):
        s = inverse_system(SPACES, MAPS)
        assert "version" in s


# ---------------------------------------------------------------------------
# inverse_limit
# ---------------------------------------------------------------------------

class TestInverseLimit:
    def setup_method(self):
        self.sys = inverse_system(SPACES, MAPS)

    def test_basic_limit(self):
        lim = inverse_limit(self.sys)
        assert lim is not None
        assert lim["limit_type"] == "inverse_limit"

    def test_space_count_forwarded(self):
        lim = inverse_limit(self.sys)
        assert lim["space_count"] == 3

    def test_bonding_map_count_forwarded(self):
        lim = inverse_limit(self.sys)
        assert lim["bonding_map_count"] == 2

    def test_has_compatibility_rule(self):
        lim = inverse_limit(self.sys)
        assert "compatibility_rule" in lim

    def test_has_carrier_hint(self):
        lim = inverse_limit(self.sys)
        assert "carrier_hint" in lim

    def test_non_dict_returns_none(self):
        assert inverse_limit("not_a_dict") is None
        assert inverse_limit(None) is None

    def test_wrong_system_type_returns_none(self):
        assert inverse_limit({"system_type": "direct_system"}) is None

    def test_version_present(self):
        lim = inverse_limit(self.sys)
        assert "version" in lim
