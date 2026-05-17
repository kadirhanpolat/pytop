"""Tests for paracompactness.py (v0.5.3)."""
from pytop.finite_spaces import FiniteTopologicalSpace
from pytop.paracompactness import (
    _carrier_size,
    _representation_of,
    analyze_paracompactness,
    is_fully_normal,
    is_locally_finite_refinement,
    is_metacompact,
    is_paracompact,
    is_star_refinement,
    paracompact_profile,
    paracompactness_inheritance_profile,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _finite_space():
    carrier = frozenset({1, 2})
    topology = frozenset([frozenset(), frozenset({1}), frozenset({1, 2})])
    return FiniteTopologicalSpace(carrier=carrier, topology=topology)


class _Obj:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        if not hasattr(self, "metadata"):
            self.metadata = {}
        if not hasattr(self, "tags"):
            self.tags = set()


# ---------------------------------------------------------------------------
# _representation_of
# ---------------------------------------------------------------------------

def test_representation_of_metadata_path():
    obj = _Obj()
    obj.metadata = {"representation": "infinite_metric"}
    assert _representation_of(obj) == "infinite_metric"


def test_representation_of_finite_space():
    assert _representation_of(_finite_space()) == "finite"


def test_representation_of_fallback():
    obj = _Obj()
    obj.metadata = {}
    assert _representation_of(obj) == "symbolic_general"


# ---------------------------------------------------------------------------
# _carrier_size
# ---------------------------------------------------------------------------

def test_carrier_size_finite_space():
    assert _carrier_size(_finite_space()) == 2


def test_carrier_size_list_carrier():
    obj = _Obj()
    obj.carrier = [1, 2, 3]
    assert _carrier_size(obj) == 3


def test_carrier_size_none_carrier():
    obj = _Obj()
    obj.carrier = None
    assert _carrier_size(obj) is None


def test_carrier_size_type_error():
    class BadLen:
        def __len__(self):
            raise TypeError("no len")

    obj = _Obj()
    obj.carrier = BadLen()
    assert _carrier_size(obj) is None


# ---------------------------------------------------------------------------
# is_paracompact
# ---------------------------------------------------------------------------

def test_is_paracompact_not_paracompact_tag():
    obj = _Obj()
    obj.tags = {"not_paracompact"}
    assert is_paracompact(obj).is_false


def test_is_paracompact_finite_space():
    assert is_paracompact(_finite_space()).is_true


def test_is_paracompact_metrizable():
    obj = _Obj()
    obj.tags = {"metrizable"}
    assert is_paracompact(obj).is_true


def test_is_paracompact_metric_tag():
    obj = _Obj()
    obj.tags = {"metric"}
    assert is_paracompact(obj).is_true


def test_is_paracompact_compact():
    obj = _Obj()
    obj.tags = {"compact"}
    assert is_paracompact(obj).is_true


def test_is_paracompact_compact_hausdorff():
    obj = _Obj()
    obj.tags = {"compact_hausdorff"}
    assert is_paracompact(obj).is_true


def test_is_paracompact_regular_lindelof():
    obj = _Obj()
    obj.tags = {"regular", "lindelof"}
    assert is_paracompact(obj).is_true


def test_is_paracompact_second_countable_hausdorff():
    obj = _Obj()
    obj.tags = {"hausdorff", "second_countable"}
    assert is_paracompact(obj).is_true


def test_is_paracompact_cw_complex():
    obj = _Obj()
    obj.tags = {"cw_complex"}
    result = is_paracompact(obj)
    assert result.is_true
    assert result.metadata["criterion"] == "milnor_cw"


def test_is_paracompact_closed_subspace_paracompact():
    obj = _Obj()
    obj.tags = {"closed_subspace_paracompact"}
    result = is_paracompact(obj)
    assert result.is_true
    assert result.metadata["criterion"] == "hereditary_closed"


def test_is_paracompact_closed_in_paracompact():
    obj = _Obj()
    obj.tags = {"closed_in_paracompact"}
    assert is_paracompact(obj).is_true


def test_is_paracompact_explicit_tag():
    obj = _Obj()
    obj.tags = {"paracompact"}
    assert is_paracompact(obj).is_true


def test_is_paracompact_unknown():
    obj = _Obj()
    obj.tags = {"connected"}
    assert is_paracompact(obj).is_unknown


# ---------------------------------------------------------------------------
# is_fully_normal
# ---------------------------------------------------------------------------

def test_is_fully_normal_not_fully_normal_tag():
    obj = _Obj()
    obj.tags = {"not_fully_normal"}
    assert is_fully_normal(obj).is_false


def test_is_fully_normal_metrizable():
    obj = _Obj()
    obj.tags = {"metrizable"}
    result = is_fully_normal(obj)
    assert result.is_true
    assert result.metadata["criterion"] == "metrizable"


def test_is_fully_normal_paracompact_hausdorff():
    obj = _Obj()
    obj.tags = {"paracompact", "hausdorff"}
    result = is_fully_normal(obj)
    assert result.is_true
    assert result.metadata["criterion"] == "dieudonne"


def test_is_fully_normal_finite():
    result = is_fully_normal(_finite_space())
    assert result.is_true


def test_is_fully_normal_paracompact_no_hausdorff():
    obj = _Obj()
    obj.tags = {"paracompact"}
    result = is_fully_normal(obj)
    assert result.is_unknown


def test_is_fully_normal_explicit_tag():
    obj = _Obj()
    obj.tags = {"fully_normal"}
    assert is_fully_normal(obj).is_true


def test_is_fully_normal_unknown():
    obj = _Obj()
    obj.tags = {"connected"}
    assert is_fully_normal(obj).is_unknown


# ---------------------------------------------------------------------------
# is_metacompact
# ---------------------------------------------------------------------------

def test_is_metacompact_not_metacompact_tag():
    obj = _Obj()
    obj.tags = {"not_metacompact"}
    assert is_metacompact(obj).is_false


def test_is_metacompact_finite():
    result = is_metacompact(_finite_space())
    assert result.is_true
    assert result.metadata["criterion"] == "finite"


def test_is_metacompact_paracompact():
    obj = _Obj()
    obj.tags = {"metrizable"}
    result = is_metacompact(obj)
    assert result.is_true
    assert result.metadata["criterion"] == "paracompact_implies_metacompact"


def test_is_metacompact_compact():
    obj = _Obj()
    obj.tags = {"compact"}
    result = is_metacompact(obj)
    assert result.is_true
    assert result.metadata["criterion"] == "paracompact_implies_metacompact"


def test_is_metacompact_explicit_tag():
    obj = _Obj()
    obj.tags = {"metacompact"}
    assert is_metacompact(obj).is_true


def test_is_metacompact_unknown():
    obj = _Obj()
    obj.tags = {"connected"}
    assert is_metacompact(obj).is_unknown


# ---------------------------------------------------------------------------
# is_locally_finite_refinement
# ---------------------------------------------------------------------------

def test_is_locally_finite_refinement_empty():
    assert is_locally_finite_refinement([], []) is True


def test_is_locally_finite_refinement_finite_collection():
    cover = [{1, 2}, {2, 3}]
    refinement = [{1}, {2}, {3}]
    assert is_locally_finite_refinement(cover, refinement) is True


def test_is_locally_finite_refinement_non_iterable():
    assert is_locally_finite_refinement([], 42) is False


# ---------------------------------------------------------------------------
# is_star_refinement
# ---------------------------------------------------------------------------

def test_is_star_refinement_empty():
    assert is_star_refinement([], []) is True


def test_is_star_refinement_trivial():
    # Single-set refinement: St({1,2}, [{1,2}]) = {1,2} ⊆ {1,2,3}
    cover = [{1, 2, 3}]
    refinement = [{1, 2}]
    assert is_star_refinement(cover, refinement) is True


def test_is_star_refinement_fails():
    # St({1,2}, [{1,2},{2,3}]) = {1,2,3} which is not ⊆ {1,2} nor ⊆ {2,3}
    cover = [{1, 2}, {2, 3}]
    refinement = [{1, 2}, {2, 3}]
    assert is_star_refinement(cover, refinement) is False


def test_is_star_refinement_non_iterable_cover():
    assert is_star_refinement(42, []) is False


def test_is_star_refinement_non_iterable_refinement():
    assert is_star_refinement([], 42) is False


# ---------------------------------------------------------------------------
# paracompact_profile
# ---------------------------------------------------------------------------

def test_paracompact_profile_paracompact_no_hausdorff():
    obj = _Obj()
    obj.tags = {"paracompact"}
    profile = paracompact_profile(obj)
    assert "Hausdorff not confirmed" in profile["partition_of_unity"]


def test_paracompact_profile_metrizable_has_fully_normal():
    obj = _Obj()
    obj.tags = {"metrizable"}
    profile = paracompact_profile(obj)
    assert profile["is_fully_normal_result"].is_true


def test_paracompact_profile_includes_metacompact():
    obj = _Obj()
    obj.tags = {"metrizable"}
    profile = paracompact_profile(obj)
    assert profile["is_metacompact_result"].is_true


def test_paracompact_profile_finite():
    profile = paracompact_profile(_finite_space())
    assert "finite" in profile["locally_finite_covers"]
    assert len(profile["key_theorems"]) >= 5
    assert len(profile["counterexamples"]) >= 4


def test_paracompact_profile_not_para_unknown():
    obj = _Obj()
    obj.tags = {"connected"}
    profile = paracompact_profile(obj)
    assert profile["is_paracompact_result"].is_unknown


# ---------------------------------------------------------------------------
# paracompactness_inheritance_profile
# ---------------------------------------------------------------------------

def test_inheritance_profile_metrizable():
    obj = _Obj()
    obj.tags = {"metrizable"}
    p = paracompactness_inheritance_profile(obj)
    assert p["paracompact"] is True
    assert p["inherited_by_closed"] is True
    assert p["implies_metrizable"] is True


def test_inheritance_profile_paracompact_hausdorff():
    obj = _Obj()
    obj.tags = {"paracompact", "hausdorff"}
    p = paracompactness_inheritance_profile(obj)
    assert p["paracompact"] is True
    assert p["implies_normal"] is True
    assert p["implies_metrizable"] is None


def test_inheritance_profile_paracompact_no_hausdorff():
    obj = _Obj()
    obj.tags = {"paracompact"}
    p = paracompactness_inheritance_profile(obj)
    assert p["paracompact"] is True
    assert p["implies_normal"] is False


def test_inheritance_profile_not_paracompact():
    obj = _Obj()
    obj.tags = {"not_paracompact"}
    p = paracompactness_inheritance_profile(obj)
    assert p["paracompact"] is False
    assert p["implies_normal"] is None


def test_inheritance_profile_unknown():
    obj = _Obj()
    obj.tags = {"connected"}
    p = paracompactness_inheritance_profile(obj)
    assert p["paracompact"] is None
    assert "Sorgenfrey" in p["preserved_products"]


# ---------------------------------------------------------------------------
# analyze_paracompactness (facade)
# ---------------------------------------------------------------------------

def test_analyze_paracompactness_finite():
    result = analyze_paracompactness(_finite_space())
    assert result.is_true
    assert result.metadata["paracompact_status"] == "true"


def test_analyze_paracompactness_symbolic():
    obj = _Obj()
    obj.tags = {"metrizable"}
    result = analyze_paracompactness(obj)
    assert result.is_true
    profile = result.value
    assert profile["is_metacompact_result"].is_true
