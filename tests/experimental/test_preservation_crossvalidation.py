"""Cross-validate the S3 preservation table against pi-Base meta-properties.

The reasoning engine's ``PRESERVATION`` table encodes preservation theorems by
hand. pi-Base independently records heredity/productivity/disjoint-union
meta-properties (sparsely). This test pins the two together in the
no-contradiction direction: wherever pi-Base *states* a meta-property for one of
our core properties, the hand-curated table must agree. (pi-Base silence is not a
negative claim, so we only check the positive direction.)
"""

from __future__ import annotations

import pytest

from pytop.experimental.pi_base import property_meta
from pytop.experimental.spaces.reasoning import _PI_NAME as PI_NAME
from pytop.experimental.spaces.reasoning import PRESERVATION, PROPERTY_KEYS

PRODUCT_FLAGS = {"products_arbitrary", "products_finite", "products_countable"}
SUM_FLAGS = {"sums_arbitrary", "sums_finite", "sums_countable"}


@pytest.mark.parametrize("key", PROPERTY_KEYS)
def test_subspace_table_agrees_with_pi_base_heredity(key):
    meta = set(property_meta(PI_NAME[key]))
    if "hereditary" in meta:
        assert key in PRESERVATION["subspace"], (
            f"pi-Base marks {key} hereditary, but the subspace table omits it"
        )


@pytest.mark.parametrize("key", PROPERTY_KEYS)
def test_product_table_agrees_with_pi_base_productivity(key):
    meta = set(property_meta(PI_NAME[key]))
    if meta & PRODUCT_FLAGS:
        assert key in PRESERVATION["product"], (
            f"pi-Base marks {key} product-preserved, but the product table omits it"
        )


@pytest.mark.parametrize("key", PROPERTY_KEYS)
def test_sum_table_agrees_with_pi_base_disjoint_unions(key):
    meta = set(property_meta(PI_NAME[key]))
    if meta & SUM_FLAGS:
        assert key in PRESERVATION["sum"], (
            f"pi-Base marks {key} disjoint-union-preserved, but the sum table omits it"
        )


def test_crossvalidation_has_teeth():
    # The data really does assert these, so the checks above are not vacuous.
    assert "hereditary" in property_meta("T0")
    assert "hereditary" in property_meta("Hausdorff")
    assert "hereditary" in property_meta("Regular")
    assert PRODUCT_FLAGS & set(property_meta("Compact"))   # Tychonoff
    assert SUM_FLAGS & set(property_meta("Compact"))        # finite disjoint unions
    assert SUM_FLAGS & set(property_meta("T0"))


def test_compact_is_not_arbitrarily_hereditary():
    # pi-Base records compact as closed-hereditary only (not plain hereditary);
    # the subspace table must therefore exclude compact.
    meta = set(property_meta("Compact"))
    assert "hereditary" not in meta
    assert "compact" not in PRESERVATION["subspace"]
