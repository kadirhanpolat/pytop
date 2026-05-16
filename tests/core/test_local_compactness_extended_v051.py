"""Coverage-targeted tests for local_compactness.py (v0.5.1)."""
import pytest
from pytop.local_compactness import (
    LocalCompactnessError,
    is_locally_compact,
    one_point_compactification,
    alexandroff_point_check,
    local_compactness_profile,
    analyze_local_compactness,
    _representation_of,
    _finite_is_hausdorff,
    _finite_is_compact,
)
from pytop.finite_spaces import FiniteTopologicalSpace


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _space(carrier_list, opens_list):
    carrier = frozenset(carrier_list)
    topology = frozenset(frozenset(u) for u in opens_list)
    return FiniteTopologicalSpace(carrier=carrier, topology=topology)


def _discrete2():
    return _space([1, 2], [set(), {1}, {2}, {1, 2}])


def _indiscrete2():
    return _space([1, 2], [set(), {1, 2}])


class _TaggedObj:
    def __init__(self, tags=None, representation=None, metadata=None):
        self.tags = set(tags or [])
        if representation is not None:
            self.representation = representation
        self.metadata = metadata or {}


# ---------------------------------------------------------------------------
# _representation_of — metadata path (line 86) and fallback (line 90)
# ---------------------------------------------------------------------------

def test_representation_of_finite():
    space = _discrete2()
    assert _representation_of(space) == "finite"


def test_representation_of_metadata_path():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(description="test", tags=["compact"])
    # TopologicalSpace.symbolic sets metadata["representation"] = "symbolic_general"
    assert _representation_of(space) == "symbolic_general"


def test_representation_of_attr_path():
    obj = _TaggedObj(representation="custom_rep")
    assert _representation_of(obj) == "custom_rep"


def test_representation_of_fallback():
    # No metadata["representation"] and no .representation attr
    class Bare:
        tags = set()
        metadata = {"description": "bare"}
    assert _representation_of(Bare()) == "symbolic_general"


# ---------------------------------------------------------------------------
# _finite_is_hausdorff — discrete (true) and indiscrete (false)  (lines 121-136)
# ---------------------------------------------------------------------------

def test_finite_is_hausdorff_discrete_true():
    space = _discrete2()
    assert _finite_is_hausdorff(space) is True


def test_finite_is_hausdorff_indiscrete_false():
    space = _indiscrete2()
    assert _finite_is_hausdorff(space) is False


def test_finite_is_hausdorff_single_point():
    space = _space([1], [set(), {1}])
    assert _finite_is_hausdorff(space) is True


def test_finite_is_hausdorff_t0_not_hausdorff():
    # {1,2} with opens {∅, {1}, {1,2}} — T0 but not T2
    space = _space([1, 2], [set(), {1}, {1, 2}])
    assert _finite_is_hausdorff(space) is False


def test_finite_is_hausdorff_three_point_discrete():
    space = _space([1, 2, 3], [set(), {1}, {2}, {3}, {1,2}, {1,3}, {2,3}, {1,2,3}])
    assert _finite_is_hausdorff(space) is True


# ---------------------------------------------------------------------------
# _finite_is_compact — always True  (line 141)
# ---------------------------------------------------------------------------

def test_finite_is_compact_always_true():
    assert _finite_is_compact(_discrete2()) is True
    assert _finite_is_compact(_indiscrete2()) is True
    assert _finite_is_compact(_space([1], [set(), {1}])) is True


# ---------------------------------------------------------------------------
# is_locally_compact — symbolic paths (lines 86, 90)
# ---------------------------------------------------------------------------

def test_is_locally_compact_symbolic_true_tag():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(description="test", tags=["locally_compact"])
    r = is_locally_compact(space)
    assert r.is_true
    assert r.mode == "theorem"


def test_is_locally_compact_symbolic_compact_tag():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(description="test", tags=["compact"])
    r = is_locally_compact(space)
    assert r.is_true


def test_is_locally_compact_symbolic_false_tag():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(description="test", tags=["not_locally_compact"])
    r = is_locally_compact(space)
    assert r.is_false


def test_is_locally_compact_symbolic_metric_conditional():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(description="test", tags=["metrizable"])
    r = is_locally_compact(space)
    assert r.status == "conditional"


def test_is_locally_compact_symbolic_unknown():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(description="test", tags=["hausdorff"])
    r = is_locally_compact(space)
    assert r.is_unknown


def test_is_locally_compact_bare_object_fallback():
    class Bare:
        tags = set()
        metadata = {}
    r = is_locally_compact(Bare())
    assert r.is_unknown


# ---------------------------------------------------------------------------
# is_locally_compact — finite path
# ---------------------------------------------------------------------------

def test_is_locally_compact_finite():
    space = _discrete2()
    r = is_locally_compact(space)
    assert r.is_true
    assert r.mode == "exact"


# ---------------------------------------------------------------------------
# one_point_compactification — errors
# ---------------------------------------------------------------------------

def test_one_point_compactification_non_finite_raises():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(description="test")
    with pytest.raises(LocalCompactnessError, match="FiniteTopologicalSpace"):
        one_point_compactification(space)


def test_one_point_compactification_point_already_exists():
    space = _discrete2()
    with pytest.raises(LocalCompactnessError, match="already exists"):
        one_point_compactification(space, point_label=1)


def test_one_point_compactification_basic():
    space = _discrete2()
    ext = one_point_compactification(space)
    assert len(ext.carrier) == 3  # 2 original + infinity point


# ---------------------------------------------------------------------------
# alexandroff_point_check
# ---------------------------------------------------------------------------

def test_alexandroff_point_check_finite_always_false():
    space = _discrete2()
    r = alexandroff_point_check(space)
    assert r.is_false
    assert r.mode == "exact"


def test_alexandroff_point_check_symbolic_not_lc():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(description="test", tags=["not_locally_compact"])
    r = alexandroff_point_check(space)
    assert r.is_false


# ---------------------------------------------------------------------------
# local_compactness_profile / analyze_local_compactness
# ---------------------------------------------------------------------------

def test_local_compactness_profile_keys():
    space = _discrete2()
    p = local_compactness_profile(space)
    for key in ("is_locally_compact", "is_hausdorff", "is_compact", "alexandroff_eligible"):
        assert key in p


def test_analyze_local_compactness_finite():
    space = _discrete2()
    r = analyze_local_compactness(space)
    assert r.is_true
    assert r.mode == "exact"


def test_analyze_local_compactness_metadata_keys():
    space = _discrete2()
    r = analyze_local_compactness(space)
    for key in ("is_locally_compact", "is_hausdorff", "is_compact", "alexandroff_eligible"):
        assert key in r.metadata
