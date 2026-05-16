"""Coverage-targeted tests for compactness_variants.py (v0.5.1)."""
import pytest
from pytop.compactness_variants import (
    is_countably_compact,
    is_sequentially_compact,
    is_pseudocompact,
    is_lindelof,
    is_feebly_compact,
    is_metacompact,
    is_relatively_compact,
    is_sigma_compact,
    _representation_of,
    _carrier_size,
    _tags_of,
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
# _representation_of — metadata path (lines 53-54) and attr path (55-57)
# ---------------------------------------------------------------------------

def test_representation_of_finite():
    space = _finite_space()
    assert _representation_of(space) == "finite"


def test_representation_of_metadata_path():
    obj = _Obj()
    obj.metadata = {"representation": "meta_rep"}
    assert _representation_of(obj) == "meta_rep"


def test_representation_of_attr_path():
    obj = _Obj(representation="attr_rep")
    assert _representation_of(obj) == "attr_rep"


def test_representation_of_fallback():
    obj = _Obj()
    assert _representation_of(obj) == "symbolic_general"


# ---------------------------------------------------------------------------
# _carrier_size — TypeError path  (lines 74-77)
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
# is_countably_compact — lindelof_not_compact (line 109), metrizable+seq_compact (144-145)
# ---------------------------------------------------------------------------

def test_countably_compact_not_tag():
    obj = _Obj(tags=["not_countably_compact"])
    r = is_countably_compact(obj)
    assert r.is_false


def test_countably_compact_lindelof_not_compact_tag():
    obj = _Obj(tags=["lindelof_not_compact"])
    r = is_countably_compact(obj)
    assert r.is_false


def test_countably_compact_sigma_compact_not_compact_tag():
    obj = _Obj(tags=["sigma_compact_not_compact"])
    r = is_countably_compact(obj)
    assert r.is_false


def test_countably_compact_finite():
    space = _finite_space()
    r = is_countably_compact(space)
    assert r.is_true
    assert r.mode == "exact"


def test_countably_compact_compact_tag():
    obj = _Obj(tags=["compact"])
    r = is_countably_compact(obj)
    assert r.is_true


def test_countably_compact_metrizable_seq_compact():
    obj = _Obj(tags=["metrizable", "sequentially_compact"])
    r = is_countably_compact(obj)
    assert r.is_true
    assert "metrizable" in str(r.metadata).lower() or r.is_true


def test_countably_compact_unknown():
    obj = _Obj(tags=["hausdorff"])
    r = is_countably_compact(obj)
    assert r.is_unknown


# ---------------------------------------------------------------------------
# is_sequentially_compact
# ---------------------------------------------------------------------------

def test_sequentially_compact_finite():
    space = _finite_space()
    r = is_sequentially_compact(space)
    assert r.is_true
    assert r.mode == "exact"


def test_sequentially_compact_not_tag():
    obj = _Obj(tags=["not_sequentially_compact"])
    r = is_sequentially_compact(obj)
    assert r.is_false


def test_sequentially_compact_metrizable_compact():
    obj = _Obj(tags=["metrizable", "compact"])
    r = is_sequentially_compact(obj)
    assert r.is_true


def test_sequentially_compact_compact_only_unknown():
    obj = _Obj(tags=["compact"])
    r = is_sequentially_compact(obj)
    assert r.is_unknown


# ---------------------------------------------------------------------------
# is_pseudocompact
# ---------------------------------------------------------------------------

def test_pseudocompact_finite():
    space = _finite_space()
    r = is_pseudocompact(space)
    assert r.is_true


def test_pseudocompact_not_tag():
    obj = _Obj(tags=["not_pseudocompact"])
    r = is_pseudocompact(space=obj)
    assert r.is_false


def test_pseudocompact_metrizable_lindelof_non_compact():
    obj = _Obj(tags=["metrizable", "lindelof"])
    r = is_pseudocompact(obj)
    assert r.is_false


def test_pseudocompact_countably_compact():
    obj = _Obj(tags=["countably_compact"])
    r = is_pseudocompact(obj)
    assert r.is_true


# ---------------------------------------------------------------------------
# is_feebly_compact — not_feebly_compact tag (line 412), metrizable noncompact (444-445)
# ---------------------------------------------------------------------------

def test_feebly_compact_finite():
    space = _finite_space()
    r = is_feebly_compact(space)
    assert r.is_true
    assert r.mode == "exact"


def test_feebly_compact_not_tag():
    obj = _Obj(tags=["not_feebly_compact"])
    r = is_feebly_compact(obj)
    assert r.is_false
    assert r.mode == "theorem"


def test_feebly_compact_compact_tag():
    obj = _Obj(tags=["compact"])
    r = is_feebly_compact(obj)
    assert r.is_true


def test_feebly_compact_metrizable_noncompact():
    obj = _Obj(tags=["metrizable"])
    r = is_feebly_compact(obj)
    assert r.is_false


def test_feebly_compact_unknown():
    obj = _Obj(tags=["hausdorff"])
    r = is_feebly_compact(obj)
    assert r.is_unknown


# ---------------------------------------------------------------------------
# is_metacompact — not_metacompact tag (line 479), metrizable (508-509)
# ---------------------------------------------------------------------------

def test_metacompact_finite():
    space = _finite_space()
    r = is_metacompact(space)
    assert r.is_true
    assert r.mode == "exact"


def test_metacompact_not_tag():
    obj = _Obj(tags=["not_metacompact"])
    r = is_metacompact(obj)
    assert r.is_false
    assert r.mode == "theorem"


def test_metacompact_paracompact_tag():
    obj = _Obj(tags=["paracompact"])
    r = is_metacompact(obj)
    assert r.is_true


def test_metacompact_metrizable():
    obj = _Obj(tags=["metrizable"])
    r = is_metacompact(obj)
    assert r.is_true


def test_metacompact_metric():
    obj = _Obj(tags=["metric"])
    r = is_metacompact(obj)
    assert r.is_true


def test_metacompact_unknown():
    obj = _Obj(tags=["hausdorff"])
    r = is_metacompact(obj)
    assert r.is_unknown


# ---------------------------------------------------------------------------
# is_relatively_compact — not tag (line 544), totally_bounded_metrizable (571-572), unknown
# ---------------------------------------------------------------------------

def test_relatively_compact_finite():
    space = _finite_space()
    r = is_relatively_compact(space)
    assert r.is_true
    assert r.mode == "exact"


def test_relatively_compact_not_tag():
    obj = _Obj(tags=["not_relatively_compact"])
    r = is_relatively_compact(obj)
    assert r.is_false
    assert r.mode == "theorem"


def test_relatively_compact_compact_tag():
    obj = _Obj(tags=["compact"])
    r = is_relatively_compact(obj)
    assert r.is_true


def test_relatively_compact_totally_bounded_metrizable():
    obj = _Obj(tags=["metrizable", "totally_bounded"])
    r = is_relatively_compact(obj)
    assert r.is_true


def test_relatively_compact_unknown():
    obj = _Obj(tags=["hausdorff"])
    r = is_relatively_compact(obj)
    assert r.is_unknown


# ---------------------------------------------------------------------------
# is_sigma_compact — not tag (line 606), locally_compact+second_countable (633-644),
#                    lc_metrizable_lindelof (646-647), unknown (656)
# ---------------------------------------------------------------------------

def test_sigma_compact_finite():
    space = _finite_space()
    r = is_sigma_compact(space)
    assert r.is_true
    assert r.mode == "exact"


def test_sigma_compact_not_tag():
    obj = _Obj(tags=["not_sigma_compact"])
    r = is_sigma_compact(obj)
    assert r.is_false
    assert r.mode == "theorem"


def test_sigma_compact_compact_tag():
    obj = _Obj(tags=["compact"])
    r = is_sigma_compact(obj)
    assert r.is_true


def test_sigma_compact_locally_compact_second_countable():
    obj = _Obj(tags=["locally_compact", "second_countable"])
    r = is_sigma_compact(obj)
    assert r.is_true


def test_sigma_compact_locally_compact_separable_metrizable():
    obj = _Obj(tags=["locally_compact", "separable_metrizable"])
    r = is_sigma_compact(obj)
    assert r.is_true


def test_sigma_compact_lc_metrizable_lindelof():
    obj = _Obj(tags=["locally_compact", "metrizable", "lindelof"])
    r = is_sigma_compact(obj)
    assert r.is_true


def test_sigma_compact_unknown():
    obj = _Obj(tags=["hausdorff"])
    r = is_sigma_compact(obj)
    assert r.is_unknown
