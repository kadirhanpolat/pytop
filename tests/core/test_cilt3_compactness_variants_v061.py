"""
test_cilt3_compactness_variants_v061.py
========================================
Test suite for src/pytop/compactness_variants.py (v0.1.61)
"""
import importlib.util, sys, os
from itertools import combinations
import pytest

_BASE = os.path.join(os.path.dirname(__file__), "..", "..", "src", "pytop")
def _load(name, rel):
    path = os.path.normpath(os.path.join(_BASE, rel))
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    mod.__package__ = "pytop"; sys.modules[name] = mod
    spec.loader.exec_module(mod); return mod

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))
import pytop as _pytop_pkg

_cv = _load("pytop.compactness_variants", "compactness_variants.py")
FiniteTopologicalSpace         = sys.modules["pytop.finite_spaces"].FiniteTopologicalSpace
is_countably_compact           = _cv.is_countably_compact
is_sequentially_compact        = _cv.is_sequentially_compact
is_pseudocompact               = _cv.is_pseudocompact
is_lindelof                    = _cv.is_lindelof
compactness_variant_profile    = _cv.compactness_variant_profile
analyze_compactness_variants   = _cv.analyze_compactness_variants
CompactnessVariantError        = _cv.CompactnessVariantError

def make_finite(n):
    c = list(range(n))
    t = [frozenset(s) for r in range(n+1) for s in combinations(c,r)]
    return FiniteTopologicalSpace(carrier=frozenset(c), topology=frozenset(t))

class _Tagged:
    def __init__(self, tags=(), representation="symbolic_general"):
        self.metadata = {"tags": list(tags)}; self.representation = representation


# ---- CompactnessVariantError ----
def test_error_is_exception():
    assert issubclass(CompactnessVariantError, Exception)

def test_error_can_be_raised():
    with pytest.raises(CompactnessVariantError):
        raise CompactnessVariantError("test")


# ---- is_countably_compact ----
def test_cc_finite_true():
    assert is_countably_compact(make_finite(3)).status == "true"

def test_cc_finite_exact():
    assert is_countably_compact(make_finite(3)).mode == "exact"

def test_cc_finite_n1():
    assert is_countably_compact(make_finite(1)).status == "true"

def test_cc_compact_tag():
    assert is_countably_compact(_Tagged(tags=["compact"])).status == "true"

def test_cc_sequentially_compact_tag():
    assert is_countably_compact(_Tagged(tags=["sequentially_compact"])).status == "true"

def test_cc_countably_compact_tag():
    assert is_countably_compact(_Tagged(tags=["countably_compact"])).status == "true"

def test_cc_neg_tag_false():
    assert is_countably_compact(_Tagged(tags=["not_countably_compact"])).status == "false"

def test_cc_unknown():
    assert is_countably_compact(_Tagged()).status == "unknown"

def test_cc_metrizable_seq_compact():
    r = is_countably_compact(_Tagged(tags=["metrizable","sequentially_compact"]))
    assert r.status == "true"

def test_cc_metadata_version():
    r = is_countably_compact(make_finite(3))
    assert r.metadata.get("version") == "0.1.61"


# ---- is_sequentially_compact ----
def test_sc_finite_true():
    assert is_sequentially_compact(make_finite(3)).status == "true"

def test_sc_finite_exact():
    assert is_sequentially_compact(make_finite(2)).mode == "exact"

def test_sc_metrizable_compact():
    r = is_sequentially_compact(_Tagged(tags=["metrizable","compact"]))
    assert r.status == "true"

def test_sc_compact_only_unknown():
    r = is_sequentially_compact(_Tagged(tags=["compact"]))
    assert r.status == "unknown"

def test_sc_neg_tag_false():
    assert is_sequentially_compact(_Tagged(tags=["not_sequentially_compact"])).status == "false"

def test_sc_explicit_tag():
    assert is_sequentially_compact(_Tagged(tags=["sequentially_compact"])).status == "true"

def test_sc_unknown_generic():
    assert is_sequentially_compact(_Tagged()).status == "unknown"

def test_sc_metadata_version():
    r = is_sequentially_compact(make_finite(3))
    assert r.metadata.get("version") == "0.1.61"


# ---- is_pseudocompact ----
def test_pc_finite_true():
    assert is_pseudocompact(make_finite(3)).status == "true"

def test_pc_finite_exact():
    assert is_pseudocompact(make_finite(4)).mode == "exact"

def test_pc_countably_compact_tag():
    assert is_pseudocompact(_Tagged(tags=["countably_compact"])).status == "true"

def test_pc_compact_tag():
    assert is_pseudocompact(_Tagged(tags=["compact"])).status == "true"

def test_pc_metrizable_lindelof_false():
    r = is_pseudocompact(_Tagged(tags=["metrizable","lindelof"]))
    assert r.status == "false"

def test_pc_second_countable_metrizable_false():
    r = is_pseudocompact(_Tagged(tags=["metrizable","second_countable"]))
    assert r.status == "false"

def test_pc_neg_tag_false():
    assert is_pseudocompact(_Tagged(tags=["not_pseudocompact"])).status == "false"

def test_pc_explicit_tag():
    assert is_pseudocompact(_Tagged(tags=["pseudocompact"])).status == "true"

def test_pc_unknown_generic():
    assert is_pseudocompact(_Tagged()).status == "unknown"

def test_pc_metadata_version():
    r = is_pseudocompact(make_finite(3))
    assert r.metadata.get("version") == "0.1.61"


# ---- is_lindelof ----
def test_lf_finite_true():
    assert is_lindelof(make_finite(3)).status == "true"

def test_lf_finite_exact():
    assert is_lindelof(make_finite(2)).mode == "exact"

def test_lf_second_countable():
    assert is_lindelof(_Tagged(tags=["second_countable"])).status == "true"

def test_lf_compact():
    assert is_lindelof(_Tagged(tags=["compact"])).status == "true"

def test_lf_separable_metrizable():
    assert is_lindelof(_Tagged(tags=["separable_metrizable"])).status == "true"

def test_lf_uncountable_discrete_false():
    r = is_lindelof(_Tagged(tags=["uncountable","discrete"]))
    assert r.status == "false"

def test_lf_neg_tag_false():
    assert is_lindelof(_Tagged(tags=["not_lindelof"])).status == "false"

def test_lf_explicit_tag():
    assert is_lindelof(_Tagged(tags=["lindelof"])).status == "true"

def test_lf_unknown_generic():
    assert is_lindelof(_Tagged()).status == "unknown"

def test_lf_metadata_version():
    r = is_lindelof(make_finite(3))
    assert r.metadata.get("version") == "0.1.61"


# ---- compactness_variant_profile ----
def test_profile_keys():
    prof = compactness_variant_profile(make_finite(3))
    assert set(prof.keys()) == {
        "representation", "countably_compact", "sequentially_compact",
        "pseudocompact", "feebly_compact", "metacompact",
        "relatively_compact", "sigma_compact", "lindelof",
    }

def test_profile_finite_representation():
    assert compactness_variant_profile(make_finite(2))["representation"] == "finite"

def test_profile_symbolic_representation():
    assert compactness_variant_profile(_Tagged())["representation"] == "symbolic_general"

def test_profile_values_are_results():
    prof = compactness_variant_profile(make_finite(3))
    for key in ["countably_compact","sequentially_compact","pseudocompact","lindelof"]:
        assert hasattr(prof[key], "status")


# ---- analyze_compactness_variants ----
def test_analyze_status_true():
    assert analyze_compactness_variants(make_finite(3)).status == "true"

def test_analyze_mode_exact_finite():
    assert analyze_compactness_variants(make_finite(3)).mode == "exact"

def test_analyze_mode_theorem_symbolic():
    r = analyze_compactness_variants(_Tagged(tags=["compact"]))
    assert r.mode == "theorem"

def test_analyze_metadata_version():
    r = analyze_compactness_variants(make_finite(3))
    assert r.metadata.get("version") == "0.1.61"

def test_analyze_carrier_size():
    r = analyze_compactness_variants(make_finite(4))
    assert r.metadata.get("carrier_size") == 4

def test_analyze_justification_nonempty():
    r = analyze_compactness_variants(make_finite(3))
    assert len(r.justification) > 0

def test_analyze_justification_mentions_n():
    r = analyze_compactness_variants(make_finite(3))
    j = " ".join(r.justification)
    assert "3" in j or "finite" in j.lower()

def test_analyze_value_is_profile():
    r = analyze_compactness_variants(make_finite(3))
    assert isinstance(r.value, dict)
    assert "countably_compact" in r.value
