"""Coverage-targeted tests for experimental/maturity_registry.py (v0.5.1)."""
import pytest
from pytop.experimental.maturity_registry import (
    lookup_experimental_maturity,
    get_experimental_maturity_profiles,
)


# ---------------------------------------------------------------------------
# lookup_experimental_maturity — line 185 (module not found → raises KeyError)
# ---------------------------------------------------------------------------

def test_lookup_experimental_maturity_not_found_raises():
    with pytest.raises(KeyError):
        lookup_experimental_maturity("nonexistent_module_xyz")


def test_lookup_experimental_maturity_found():
    profiles = get_experimental_maturity_profiles()
    if profiles:
        first = profiles[0]
        result = lookup_experimental_maturity(first.module_name)
        assert result.module_name == first.module_name
