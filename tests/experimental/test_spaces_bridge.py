"""Bridge tests — pi-Base atlas spaces analyzed through the reasoning engine."""

from __future__ import annotations

import pytest

from pytop.experimental.pi_base import deduced_space_traits, property_uid
from pytop.experimental.pi_base_atlas import space_uid
from pytop.experimental.spaces import (
    ProductSpace,
    analyze_pi_base_space,
    derive,
    is_compact,
    is_connected,
    is_hausdorff,
    pi_base_space,
)


# --------------------------------------------------------------------------
# Famous spaces, analyzed by the engine
# --------------------------------------------------------------------------

def test_cantor_set():
    cantor = pi_base_space("Cantor set")
    assert is_hausdorff(cantor).value is True
    assert is_compact(cantor).value is True
    assert is_connected(cantor).value is False


def test_long_line():
    long_line = pi_base_space("Long line")
    assert is_compact(long_line).value is False
    assert is_connected(long_line).value is True


def test_lookup_by_uid():
    assert pi_base_space("S000025").name  # the real line


# --------------------------------------------------------------------------
# The bridge is faithful to pi-Base's deduced traits
# --------------------------------------------------------------------------

@pytest.mark.parametrize("uid", ["S000025", "S000026", "S000038", "S000001"])
def test_bridge_agrees_with_pi_base_traits(uid):
    space = pi_base_space(uid)
    traits = deduced_space_traits(uid)
    for prop, pi_name in [("T2", "Hausdorff"), ("compact", "Compact"), ("connected", "Connected")]:
        expected = traits.get(property_uid(pi_name))
        if expected is None:
            continue
        assert derive(space, prop).verdict.value is expected


# --------------------------------------------------------------------------
# Famous spaces feed into the construction/reasoning machinery
# --------------------------------------------------------------------------

def test_product_of_cantor_sets_is_compact():
    # Tychonoff: a product of compact spaces is compact
    cantor_squared = ProductSpace([pi_base_space("Cantor set"), pi_base_space("Cantor set")])
    assert derive(cantor_squared, "compact").verdict.value is True


def test_product_of_connected_is_connected():
    line_squared = ProductSpace([pi_base_space("Long line"), pi_base_space("Long line")])
    assert derive(line_squared, "connected").verdict.value is True


# --------------------------------------------------------------------------
# analyze convenience
# --------------------------------------------------------------------------

def test_analyze_returns_all_properties():
    report = analyze_pi_base_space("Cantor set")
    assert report["compact"].value is True
    assert report["connected"].value is False
    assert "T2" in report and "lindelof" in report
