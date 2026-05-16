"""Coverage-targeted tests for order_spaces.py (v0.5.1)."""
import pytest
from pytop.order_spaces import (
    FinitePosetSpace,
    FinitePreorderSpace,
    analyze_order_space,
    order_space_report,
    poset_space,
    preorder_space,
    specialization_poset,
)
from pytop.alexandroff import AlexandroffError


# ---------------------------------------------------------------------------
# FinitePosetSpace.__post_init__ — line 58 (non-antisymmetric relation raises)
# ---------------------------------------------------------------------------

def test_poset_space_non_antisymmetric_relation_raises():
    # (1,2) and (2,1) survive closure → violates antisymmetry → line 58
    with pytest.raises(AlexandroffError, match="antisymmetric"):
        poset_space([1, 2], [(1, 2), (2, 1)])


# ---------------------------------------------------------------------------
# specialization_poset — line 123 (missing carrier or topology raises)
# ---------------------------------------------------------------------------

def test_specialization_poset_no_carrier_raises():
    class _NullSpace:
        carrier = None
        topology = None
        metadata = {}

    with pytest.raises(AlexandroffError, match="explicit finite topology"):
        specialization_poset(_NullSpace())


# ---------------------------------------------------------------------------
# analyze_order_space — lines 158-164 (FinitePreorderSpace, non-poset)
# ---------------------------------------------------------------------------

def test_analyze_order_space_preorder_not_poset():
    # preorder_space returns FinitePreorderSpace (not FinitePosetSpace)
    # because the relation is not antisymmetric in the original direction
    space = preorder_space([1, 2], [(1, 2)])
    result = analyze_order_space(space)
    assert result.is_true
    assert result.value == "finite_preorder_space"
    assert result.is_exact


# ---------------------------------------------------------------------------
# analyze_order_space — line 165 (unknown fallback)
# ---------------------------------------------------------------------------

def test_analyze_order_space_unknown_for_non_order_object():
    result = analyze_order_space({"not": "an order space"})
    assert result.is_unknown


# ---------------------------------------------------------------------------
# order_space_report — line 172
# ---------------------------------------------------------------------------

def test_order_space_report_returns_expected_keys():
    space = preorder_space([1, 2], [(1, 2)])
    report = order_space_report(space)
    assert "carrier_size" in report
    assert "order_model" in report
    assert "relation" in report
    assert "neighborhoods" in report
    assert report["carrier_size"] == 2
