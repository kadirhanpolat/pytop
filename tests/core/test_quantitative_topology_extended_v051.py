"""Coverage-targeted tests for quantitative_topology.py (v0.5.1)."""
import pytest
from pytop.quantitative_topology import (
    QuantitativeTopologyError,
    quantitative_profile,
    analyze_quantitative_topology,
    _representation_of,
    _carrier_size,
    _tags_of,
    _topology_size,
)
from pytop.finite_spaces import FiniteTopologicalSpace


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class _Obj:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        if not hasattr(self, "metadata"):
            self.metadata = {}
        if not hasattr(self, "tags"):
            self.tags = []


def _finite_space():
    carrier = frozenset({1, 2})
    topology = frozenset([frozenset(), frozenset({1}), frozenset({1, 2})])
    return FiniteTopologicalSpace(carrier=carrier, topology=topology)


# ---------------------------------------------------------------------------
# _representation_of — metadata path (line 61), attr path (63-64), fallback (65)
# ---------------------------------------------------------------------------

def test_representation_of_finite_space():
    space = _finite_space()
    assert _representation_of(space) == "finite"


def test_representation_of_metadata_path():
    obj = _Obj()
    obj.metadata = {"representation": "compact_hausdorff_type"}
    assert _representation_of(obj) == "compact_hausdorff_type"


def test_representation_of_attr_path():
    obj = _Obj(representation="custom_rep")
    assert _representation_of(obj) == "custom_rep"


def test_representation_of_fallback():
    obj = _Obj()
    assert _representation_of(obj) == "symbolic_general"


# ---------------------------------------------------------------------------
# _carrier_size — TypeError path  (lines 81-84)
# ---------------------------------------------------------------------------

def test_carrier_size_finite_space():
    space = _finite_space()
    assert _carrier_size(space) == 2


def test_carrier_size_none_carrier():
    obj = _Obj()
    obj.carrier = None
    assert _carrier_size(obj) is None


def test_carrier_size_type_error():
    class BadCarrier:
        def __len__(self):
            raise TypeError("unsized")
    obj = _Obj()
    obj.carrier = BadCarrier()
    assert _carrier_size(obj) is None


def test_carrier_size_no_carrier():
    obj = _Obj()
    assert _carrier_size(obj) is None


# ---------------------------------------------------------------------------
# _tags_of paths
# ---------------------------------------------------------------------------

def test_tags_of_from_metadata():
    obj = _Obj()
    obj.metadata = {"tags": ["separable", "hausdorff"]}
    tags = _tags_of(obj)
    assert "separable" in tags
    assert "hausdorff" in tags


def test_tags_of_from_attr():
    obj = _Obj()
    obj.tags = ["metrizable", "compact"]
    tags = _tags_of(obj)
    assert "metrizable" in tags


# ---------------------------------------------------------------------------
# quantitative_profile — weight/density/character estimate edge cases
# ---------------------------------------------------------------------------

def test_quantitative_profile_finite():
    space = _finite_space()
    p = quantitative_profile(space)
    assert "weight" in p
    assert "density" in p
    assert "character" in p
    assert "finite" in p["weight"]


def test_quantitative_profile_second_countable():
    obj = _Obj(tags=["second_countable"])
    p = quantitative_profile(obj)
    assert "aleph_0" in p["weight"]


def test_quantitative_profile_discrete_uncountable():
    obj = _Obj(tags=["discrete_uncountable"])
    p = quantitative_profile(obj)
    assert "|X|" in p["weight"]


def test_quantitative_profile_indiscrete_weight():
    obj = _Obj(tags=["indiscrete"])
    p = quantitative_profile(obj)
    assert "1" in p["weight"]


def test_quantitative_profile_indiscrete_density():
    obj = _Obj(tags=["indiscrete"])
    p = quantitative_profile(obj)
    assert "1" in p["density"]


def test_quantitative_profile_indiscrete_character():
    obj = _Obj(tags=["indiscrete"])
    p = quantitative_profile(obj)
    assert "1" in p["character"]


def test_quantitative_profile_omega_weight():
    obj = _Obj(tags=["omega"])
    p = quantitative_profile(obj)
    assert "aleph_0" in p["weight"]


def test_quantitative_profile_omega_density():
    obj = _Obj(tags=["countably_infinite"])
    p = quantitative_profile(obj)
    assert "aleph_0" in p["density"]


def test_quantitative_profile_omega_1_character():
    obj = _Obj(tags=["omega_1"])
    p = quantitative_profile(obj)
    assert "aleph_1" in p["character"]


def test_quantitative_profile_separable_density():
    obj = _Obj(tags=["separable"])
    p = quantitative_profile(obj)
    assert "aleph_0" in p["density"]


def test_quantitative_profile_compact_lindelof():
    obj = _Obj(tags=["compact"])
    p = quantitative_profile(obj)
    assert "1" in p["lindelof_number"]


def test_quantitative_profile_unknown_weight():
    obj = _Obj(tags=["hausdorff"])
    p = quantitative_profile(obj)
    assert "unknown" in p["weight"]


def test_quantitative_profile_lindelof_tag():
    obj = _Obj(tags=["lindelof"])
    p = quantitative_profile(obj)
    assert "aleph_0" in p["lindelof_number"]


def test_quantitative_profile_uncountable_discrete_lindelof():
    obj = _Obj(tags=["discrete_uncountable", "uncountable"])
    p = quantitative_profile(obj)
    assert "|X|" in p["lindelof_number"]


# ---------------------------------------------------------------------------
# _topology_size — direct call  (lines 90-92)
# ---------------------------------------------------------------------------

def test_topology_size_finite_space():
    space = _finite_space()
    assert _topology_size(space) == 3  # {∅, {1}, {1,2}}


def test_topology_size_non_finite():
    obj = _Obj()
    assert _topology_size(obj) is None


# ---------------------------------------------------------------------------
# Empty finite space — weight/density n==0 paths  (lines 103, 126)
# ---------------------------------------------------------------------------

def test_quantitative_profile_empty_space():
    carrier = frozenset()
    topology = frozenset([frozenset()])
    space = FiniteTopologicalSpace(carrier=carrier, topology=topology)
    p = quantitative_profile(space)
    assert "0" in p["weight"]
    assert "0" in p["density"]


# ---------------------------------------------------------------------------
# analyze_quantitative_topology — smoke test
# ---------------------------------------------------------------------------

def test_analyze_quantitative_topology_finite():
    space = _finite_space()
    r = analyze_quantitative_topology(space)
    assert r.is_true
    assert r.mode == "exact"


def test_analyze_quantitative_topology_symbolic():
    obj = _Obj(tags=["metrizable"])
    r = analyze_quantitative_topology(obj)
    assert r.is_true


# ---------------------------------------------------------------------------
# _weight_estimate / _density_estimate — line 106, 129 (finite rep, n is None)
# ---------------------------------------------------------------------------

def test_quantitative_profile_finite_rep_no_carrier():
    # metadata["representation"]="finite" but no carrier -> n=None -> lines 106, 129 fire
    obj = _Obj()
    obj.metadata = {"representation": "finite"}
    p = quantitative_profile(obj)
    assert p["weight"] == "finite"
    assert p["density"] == "finite"
