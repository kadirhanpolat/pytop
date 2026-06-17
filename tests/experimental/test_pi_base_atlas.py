"""Tests for the pi-Base atlas and counterexample search (experimental)."""

from __future__ import annotations

import pytest

from pytop.experimental.pi_base import property_uid
from pytop.experimental.pi_base_atlas import (
    UnknownSpaceError,
    find_counterexamples,
    property_matrix,
    search_spaces,
    space_name,
    space_record,
    space_uid,
    steen_seebach_index,
)

COMPACT = "P000016"


# --------------------------------------------------------------------------
# Space lookup
# --------------------------------------------------------------------------

def test_space_lookup_and_round_trip():
    assert space_uid("S000001") == "S000001"
    assert "Discrete" in space_name("S000001")
    # name -> uid round trip
    assert space_uid(space_name("S000001")) == "S000001"


def test_unknown_space_raises():
    with pytest.raises(UnknownSpaceError):
        space_uid("no such space")


def test_space_record_has_name():
    record = space_record("S000001")
    assert "Discrete" in record["name"]
    assert record.get("counterexamples_id") == 1


# --------------------------------------------------------------------------
# Property matrix (deductive closure)
# --------------------------------------------------------------------------

def test_property_matrix_includes_asserted_and_derived():
    matrix = property_matrix("S000001")
    assert matrix.get("P000052") is True  # discrete (asserted)
    assert len(matrix) > 3                # closure adds derived properties

    named = property_matrix("S000001", names=True)
    assert named.get("Discrete") is True


# --------------------------------------------------------------------------
# Search and counterexample discovery
# --------------------------------------------------------------------------

def test_search_compact_spaces():
    compact = search_spaces({"Compact": True})
    assert len(compact) == 80
    # every match really is compact in its deduced matrix
    for uid in compact:
        assert property_matrix(uid).get(COMPACT) is True


def test_find_compact_non_hausdorff_counterexamples():
    examples = find_counterexamples(has=["Compact"], lacks=["Hausdorff"])
    assert len(examples) >= 1
    hausdorff_uid = property_uid("Hausdorff")
    for uid in examples:
        matrix = property_matrix(uid)
        assert matrix.get(COMPACT) is True
        assert matrix.get(hausdorff_uid) is False


def test_find_connected_not_path_connected():
    examples = find_counterexamples(has=["Connected"], lacks=["Path connected"])
    assert len(examples) >= 1


# --------------------------------------------------------------------------
# Steen-Seebach index
# --------------------------------------------------------------------------

def test_steen_seebach_index():
    index = steen_seebach_index()
    assert len(index) == 123
    assert index[1] == "S000001"  # Counterexample #1: finite discrete topology
