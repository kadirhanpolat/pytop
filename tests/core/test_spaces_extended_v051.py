"""Coverage-targeted tests for spaces.py (v0.5.1)."""
import pytest
from pytop.spaces import TopologicalSpace


# ---------------------------------------------------------------------------
# is_finite — try/except path (lines 28-32)
# ---------------------------------------------------------------------------

def test_is_finite_frozenset_carrier_true():
    space = TopologicalSpace(carrier=frozenset({1, 2, 3}))
    assert space.is_finite() is True


def test_is_finite_list_carrier_true():
    space = TopologicalSpace(carrier=[1, 2])
    assert space.is_finite() is True


def test_is_finite_empty_frozenset_true():
    space = TopologicalSpace(carrier=frozenset())
    assert space.is_finite() is True


def test_is_finite_exception_path_returns_false():
    class NoLen:
        pass
    space = TopologicalSpace(carrier=NoLen())
    assert space.is_finite() is False


def test_is_finite_none_carrier_false():
    space = TopologicalSpace.symbolic(description="test")
    assert space.carrier is None
    assert space.is_finite() is False


def test_is_finite_string_carrier_false():
    space = TopologicalSpace(carrier="omega")
    assert space.is_finite() is False


def test_is_finite_bytes_carrier_false():
    space = TopologicalSpace(carrier=b"bytes")
    assert space.is_finite() is False


# ---------------------------------------------------------------------------
# describe — line 45
# ---------------------------------------------------------------------------

def test_describe_with_description():
    space = TopologicalSpace.symbolic(description="my space")
    assert space.describe() == "my space"


def test_describe_default_when_no_description():
    space = TopologicalSpace(carrier=frozenset({1}))
    assert space.describe() == "topological space"


def test_describe_empty_metadata():
    space = TopologicalSpace(carrier=None)
    assert space.describe() == "topological space"


# ---------------------------------------------------------------------------
# add_tags and has_tag
# ---------------------------------------------------------------------------

def test_add_tags_updates_metadata():
    space = TopologicalSpace(carrier=None)
    space.add_tags("compact", "Hausdorff")
    assert space.has_tag("compact")
    assert space.has_tag("hausdorff")
    assert "compact" in space.metadata["tags"]


def test_has_tag_case_insensitive():
    space = TopologicalSpace.symbolic(description="test", tags=["METRIZABLE"])
    assert space.has_tag("metrizable")


def test_tags_normalized_at_init():
    space = TopologicalSpace(carrier=None, tags={"  Compact ", "T2"})
    assert "compact" in space.tags
    assert "t2" in space.tags


# ---------------------------------------------------------------------------
# symbolic constructor
# ---------------------------------------------------------------------------

def test_symbolic_sets_carrier_none():
    space = TopologicalSpace.symbolic(description="test")
    assert space.carrier is None
    assert space.topology is None


def test_symbolic_tags_merged():
    space = TopologicalSpace.symbolic(description="test", tags=["separable", "hausdorff"])
    assert "separable" in space.tags
    assert "hausdorff" in space.tags


def test_symbolic_representation_default():
    space = TopologicalSpace.symbolic(description="test")
    assert space.metadata.get("representation") == "symbolic_general"


def test_symbolic_custom_representation():
    space = TopologicalSpace.symbolic(description="test", representation="infinite_metric")
    assert space.metadata.get("representation") == "infinite_metric"
