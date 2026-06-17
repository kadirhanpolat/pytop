"""Tests for the pi-Base deductive inference engine (experimental)."""

from __future__ import annotations

import pytest

from pytop.experimental.pi_base import (
    InconsistentTraitsError,
    PI_BASE_ATTRIBUTION,
    asserted_traits,
    compare_traits,
    consequences,
    dataset_counts,
    deduce,
    is_consistent,
    properties,
    property_name,
    property_uid,
    spaces,
    theorems,
)

COMPACT = "P000016"
COUNTABLY_COMPACT = "P000019"
DISCRETE = "P000052"


# --------------------------------------------------------------------------
# Dataset loads with the expected shape
# --------------------------------------------------------------------------

def test_dataset_counts():
    assert dataset_counts() == {
        "properties": 243,
        "theorems": 902,
        "spaces": 222,
        "traits": 2099,
    }
    assert len(properties()) == 243
    assert len(theorems()) == 902


def test_attribution_is_cc_by():
    assert "pi-Base" in PI_BASE_ATTRIBUTION
    assert "CC BY 4.0" in PI_BASE_ATTRIBUTION


# --------------------------------------------------------------------------
# Name resolution
# --------------------------------------------------------------------------

def test_property_lookup_by_name_alias_uid():
    assert property_uid("Compact") == COMPACT
    assert property_uid("quasi-compact") == COMPACT  # alias
    assert property_uid(COMPACT) == COMPACT          # uid passthrough
    assert property_name(COMPACT) == "Compact"


def test_unknown_property_raises():
    from pytop.experimental.pi_base import UnknownPropertyError

    with pytest.raises(UnknownPropertyError):
        property_uid("definitely not a property")


# --------------------------------------------------------------------------
# Forward chaining and contrapositive
# --------------------------------------------------------------------------

def test_forward_compact_implies_countably_compact():
    # T000001: Compact -> Countably compact
    assert consequences("Compact")[COUNTABLY_COMPACT] is True


def test_contrapositive_not_countably_compact_implies_not_compact():
    closure = deduce({COUNTABLY_COMPACT: False})
    assert closure[COMPACT] is False


def test_discrete_closure_is_rich_and_consistent():
    closure = deduce({DISCRETE: True})
    # discreteness implies many separation/metric properties; closure must grow
    assert len(closure) > 5
    assert is_consistent({DISCRETE: True})


# --------------------------------------------------------------------------
# Inconsistency detection
# --------------------------------------------------------------------------

def test_contradiction_is_detected():
    # Compact forces countably compact; claiming the negation is inconsistent.
    assert not is_consistent({COMPACT: True, COUNTABLY_COMPACT: False})
    with pytest.raises(InconsistentTraitsError):
        deduce({COMPACT: True, COUNTABLY_COMPACT: False})


# --------------------------------------------------------------------------
# Every pi-Base space is internally consistent under the engine
# --------------------------------------------------------------------------

def test_all_pi_base_spaces_are_consistent():
    for space_uid in spaces():
        traits = asserted_traits(space_uid)
        assert is_consistent(traits), f"{space_uid} deduced a contradiction"


def test_asserted_traits_of_discrete_two_point_space():
    traits = asserted_traits("S000001")  # discrete topology on {0,1}
    assert traits.get(DISCRETE) is True


# --------------------------------------------------------------------------
# Cross-validation helper
# --------------------------------------------------------------------------

def test_compare_traits_flags_disagreement():
    conflicts = compare_traits({"P000016": True}, {COUNTABLY_COMPACT: False})
    assert len(conflicts) == 1
    assert conflicts[0].property_uid == COUNTABLY_COMPACT
    assert conflicts[0].deduced is True
    assert conflicts[0].expected is False
