"""Coverage-targeted tests for basic_invariants.py (v0.5.1)."""
import pytest
from pytop.basic_invariants import (
    BasicInvariantError,
    topological_invariants_profile,
    analyze_topological_invariants,
    _representation_of,
    _carrier_size,
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
            self.tags = set()


def _finite_space():
    carrier = frozenset({1, 2})
    topology = frozenset([frozenset(), frozenset({1}), frozenset({1, 2})])
    return FiniteTopologicalSpace(carrier=carrier, topology=topology)


def _tagged(**tags_list):
    obj = _Obj()
    obj.tags = set(tags_list)
    return obj


# ---------------------------------------------------------------------------
# _representation_of — finite path via carrier+topology (line 50)
# ---------------------------------------------------------------------------

def test_representation_of_finite_space_via_metadata():
    space = _finite_space()
    # FiniteTopologicalSpace has metadata["representation"]="finite" → early return
    assert _representation_of(space) == "finite"


def test_representation_of_carrier_topology_no_metadata_rep():
    # Has carrier+topology but no metadata["representation"] → returns "finite"
    class FiniteLike:
        metadata = {}
        carrier = frozenset({1})
        topology = frozenset([frozenset(), frozenset({1})])
    assert _representation_of(FiniteLike()) == "finite"


def test_representation_of_metadata_path():
    obj = _Obj()
    obj.metadata = {"representation": "symbolic_general"}
    assert _representation_of(obj) == "symbolic_general"


def test_representation_of_fallback():
    obj = _Obj()
    assert _representation_of(obj) == "symbolic_general"


# ---------------------------------------------------------------------------
# _carrier_size — TypeError path (lines 69-70)
# ---------------------------------------------------------------------------

def test_carrier_size_finite():
    space = _finite_space()
    assert _carrier_size(space) == 2


def test_carrier_size_none():
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


# ---------------------------------------------------------------------------
# _topology_size — TypeError path (lines 79-81)
# ---------------------------------------------------------------------------

def test_topology_size_finite():
    space = _finite_space()
    assert _topology_size(space) == 3


def test_topology_size_none():
    obj = _Obj()
    obj.topology = None
    assert _topology_size(obj) is None


def test_topology_size_type_error():
    class BadTopology:
        def __len__(self):
            raise TypeError("unsized")
    obj = _Obj()
    obj.topology = BadTopology()
    assert _topology_size(obj) is None


# ---------------------------------------------------------------------------
# _density_value — not_separable tag (line 106)
# ---------------------------------------------------------------------------

def test_density_not_separable_tag():
    obj = _Obj()
    obj.tags = {"not_separable"}
    p = topological_invariants_profile(obj)
    assert "uncountable" in p["density"]


# ---------------------------------------------------------------------------
# _character_value — not_first_countable tag (line 117)
# ---------------------------------------------------------------------------

def test_character_not_first_countable_tag():
    obj = _Obj()
    obj.tags = {"not_first_countable"}
    p = topological_invariants_profile(obj)
    assert "uncountable" in p["character"]


# ---------------------------------------------------------------------------
# _lindelof_value — compact (129), second_countable (131), not_lindelof (133)
# ---------------------------------------------------------------------------

def test_lindelof_compact_tag():
    obj = _Obj()
    obj.tags = {"compact"}
    p = topological_invariants_profile(obj)
    assert "Lindelof" in p["lindelof_number"]


def test_lindelof_second_countable_tag():
    obj = _Obj()
    obj.tags = {"second_countable"}
    p = topological_invariants_profile(obj)
    assert "Lindelof" in p["lindelof_number"]


def test_lindelof_not_lindelof_tag():
    obj = _Obj()
    obj.tags = {"not_lindelof"}
    p = topological_invariants_profile(obj)
    assert "non-Lindelof" in p["lindelof_number"]


# ---------------------------------------------------------------------------
# _cellularity_value — second_countable (line 144)
# ---------------------------------------------------------------------------

def test_cellularity_second_countable_tag():
    obj = _Obj()
    obj.tags = {"second_countable"}
    p = topological_invariants_profile(obj)
    assert "countable" in p["cellularity"]


# ---------------------------------------------------------------------------
# _spread_value — hereditarily_separable (line 155)
# ---------------------------------------------------------------------------

def test_spread_hereditarily_separable_tag():
    obj = _Obj()
    obj.tags = {"hereditarily_separable"}
    p = topological_invariants_profile(obj)
    assert "countable" in p["spread"]


# ---------------------------------------------------------------------------
# _tightness_value — fallback (line 176)
# ---------------------------------------------------------------------------

def test_tightness_sequential_tag():
    obj = _Obj()
    obj.tags = {"sequential"}
    p = topological_invariants_profile(obj)
    assert "countable" in p["tightness"]


def test_tightness_unknown_fallback():
    obj = _Obj()
    obj.tags = {"hausdorff"}
    p = topological_invariants_profile(obj)
    assert "symbolic" in p["tightness"]


# ---------------------------------------------------------------------------
# analyze_topological_invariants — modes
# ---------------------------------------------------------------------------

def test_analyze_invariants_finite():
    r = analyze_topological_invariants(_finite_space())
    assert r.is_true
    assert r.mode == "exact"


def test_analyze_invariants_symbolic():
    obj = _Obj()
    obj.tags = {"metrizable"}
    r = analyze_topological_invariants(obj)
    assert r.is_true
    assert r.mode in ("theorem", "symbolic")


def test_profile_has_all_keys():
    obj = _Obj()
    p = topological_invariants_profile(obj)
    for key in ("weight", "density", "character", "lindelof_number",
                "cellularity", "spread", "network_weight", "tightness",
                "key_inequalities", "key_examples"):
        assert key in p
