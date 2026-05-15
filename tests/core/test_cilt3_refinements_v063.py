"""
test_cilt3_refinements_v063.py
================================
Test suite for src/pytop/refinements.py (v0.1.63)
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

_rm = _load("pytop.refinements", "refinements.py")
FiniteTopologicalSpace   = sys.modules["pytop.finite_spaces"].FiniteTopologicalSpace
is_locally_finite_cover  = _rm.is_locally_finite_cover
refinement_profile       = _rm.refinement_profile
analyze_cover_refinement = _rm.analyze_cover_refinement
RefinementError          = _rm.RefinementError

def make_finite(n):
    c = list(range(n))
    t = [frozenset(s) for r in range(n+1) for s in combinations(c,r)]
    return FiniteTopologicalSpace(carrier=frozenset(c), topology=frozenset(t))

class _Tagged:
    def __init__(self, tags=(), representation="symbolic_general"):
        self.metadata = {"tags": list(tags)}; self.representation = representation


# ---- RefinementError ----
def test_error_is_exception():
    assert issubclass(RefinementError, Exception)

def test_error_can_be_raised():
    with pytest.raises(RefinementError):
        raise RefinementError("test")


# ---- is_locally_finite_cover — finite ----
def test_finite_true():
    assert is_locally_finite_cover(make_finite(3)).status == "true"

def test_finite_exact():
    assert is_locally_finite_cover(make_finite(3)).mode == "exact"

def test_finite_n1():
    assert is_locally_finite_cover(make_finite(1)).status == "true"

def test_finite_criterion():
    assert is_locally_finite_cover(make_finite(3)).metadata["criterion"] == "finite"

def test_finite_carrier_size():
    assert is_locally_finite_cover(make_finite(4)).metadata["carrier_size"] == 4

def test_finite_version():
    assert is_locally_finite_cover(make_finite(3)).metadata["version"] == "0.1.63"


# ---- is_locally_finite_cover — Stone's theorem ----
def test_metrizable_true():
    assert is_locally_finite_cover(_Tagged(tags=["metrizable"])).status == "true"

def test_metric_true():
    assert is_locally_finite_cover(_Tagged(tags=["metric"])).status == "true"

def test_stone_criterion():
    r = is_locally_finite_cover(_Tagged(tags=["metrizable"]))
    assert r.metadata["criterion"] == "stone_theorem"


# ---- is_locally_finite_cover — compact ----
def test_compact_true():
    assert is_locally_finite_cover(_Tagged(tags=["compact"])).status == "true"

def test_compact_hausdorff_true():
    assert is_locally_finite_cover(_Tagged(tags=["compact_hausdorff"])).status == "true"

def test_compact_criterion():
    assert is_locally_finite_cover(_Tagged(tags=["compact"])).metadata["criterion"] == "compact"


# ---- is_locally_finite_cover — Michael ----
def test_michael_t3_lindelof():
    assert is_locally_finite_cover(_Tagged(tags=["t3","lindelof"])).status == "true"

def test_michael_hausdorff_second_countable():
    assert is_locally_finite_cover(_Tagged(tags=["hausdorff","second_countable"])).status == "true"

def test_michael_criterion():
    r = is_locally_finite_cover(_Tagged(tags=["t3","lindelof"]))
    assert r.metadata["criterion"] == "michael_theorem"


# ---- is_locally_finite_cover — tag / negative ----
def test_paracompact_tag_true():
    assert is_locally_finite_cover(_Tagged(tags=["paracompact"])).status == "true"

def test_not_paracompact_false():
    assert is_locally_finite_cover(_Tagged(tags=["not_paracompact"])).status == "false"

def test_unknown_generic():
    assert is_locally_finite_cover(_Tagged()).status == "unknown"

def test_lindelof_alone_unknown():
    assert is_locally_finite_cover(_Tagged(tags=["lindelof"])).status == "unknown"


# ---- refinement_profile — required keys ----
def test_profile_required_keys():
    prof = refinement_profile(make_finite(3))
    for k in ["locally_finite_result","star_refinement","barycentric_refinement",
              "shrinking","sigma_locally_finite","definitions","key_theorems","representation"]:
        assert k in prof

def test_profile_finite_representation():
    assert refinement_profile(make_finite(3))["representation"] == "finite"

def test_profile_symbolic_representation():
    assert refinement_profile(_Tagged())["representation"] == "symbolic_general"


# ---- refinement_profile — definitions ----
def test_profile_definitions_keys():
    defs = refinement_profile(make_finite(3))["definitions"]
    for k in ["locally_finite_family","refinement","star_of_point",
              "star_refinement","sigma_locally_finite"]:
        assert k in defs

def test_profile_lf_family_definition():
    d = refinement_profile(_Tagged())["definitions"]["locally_finite_family"]
    assert "locally finite" in d.lower() or "neighbourhood" in d.lower()

def test_profile_refinement_definition():
    d = refinement_profile(_Tagged())["definitions"]["refinement"]
    assert "refine" in d.lower() or "contained" in d.lower()

def test_profile_star_definition():
    d = refinement_profile(_Tagged())["definitions"]["star_of_point"]
    assert "St(" in d or "star" in d.lower()

def test_profile_star_refinement_definition():
    d = refinement_profile(_Tagged())["definitions"]["star_refinement"]
    assert "star" in d.lower()

def test_profile_sigma_lf_definition():
    d = refinement_profile(_Tagged())["definitions"]["sigma_locally_finite"]
    assert "σ" in d or "sigma" in d.lower() or "countable union" in d.lower()


# ---- refinement_profile — content ----
def test_profile_finite_star_refinement_yes():
    prof = refinement_profile(make_finite(3))
    assert "yes" in prof["star_refinement"].lower()

def test_profile_finite_shrinking_yes():
    prof = refinement_profile(make_finite(3))
    assert "yes" in prof["shrinking"].lower()

def test_profile_finite_sigma_lf_yes():
    prof = refinement_profile(make_finite(3))
    assert "yes" in prof["sigma_locally_finite"].lower()

def test_profile_barycentric_mentions_barycentric():
    prof = refinement_profile(make_finite(3))
    assert "barycentric" in prof["barycentric_refinement"].lower()

def test_profile_key_theorems_count():
    prof = refinement_profile(make_finite(3))
    assert len(prof["key_theorems"]) >= 4

def test_profile_nagata_smirnov_in_theorems():
    prof = refinement_profile(make_finite(3))
    combined = " ".join(prof["key_theorems"])
    assert "Nagata" in combined or "nagata" in combined.lower()

def test_profile_metrizable_sigma_lf():
    prof = refinement_profile(_Tagged(tags=["metrizable"]))
    assert "yes" in prof["sigma_locally_finite"].lower()

def test_profile_metrizable_hausdorff_star():
    prof = refinement_profile(_Tagged(tags=["metrizable","hausdorff"]))
    s = prof["star_refinement"].lower()
    assert "yes" in s or "paracompact" in s

def test_profile_second_countable_sigma_lf():
    prof = refinement_profile(_Tagged(tags=["second_countable"]))
    assert "yes" in prof["sigma_locally_finite"].lower()


# ---- analyze_cover_refinement ----
def test_analyze_status_true():
    assert analyze_cover_refinement(make_finite(3)).status == "true"

def test_analyze_mode_exact_finite():
    assert analyze_cover_refinement(make_finite(3)).mode == "exact"

def test_analyze_mode_theorem_metrizable():
    r = analyze_cover_refinement(_Tagged(tags=["metrizable"]))
    assert r.mode == "theorem"

def test_analyze_version():
    assert analyze_cover_refinement(make_finite(3)).metadata["version"] == "0.1.63"

def test_analyze_carrier_size():
    assert analyze_cover_refinement(make_finite(4)).metadata["carrier_size"] == 4

def test_analyze_lf_status_true():
    assert analyze_cover_refinement(make_finite(3)).metadata["locally_finite_status"] == "true"

def test_analyze_lf_criterion_finite():
    assert analyze_cover_refinement(make_finite(3)).metadata["locally_finite_criterion"] == "finite"

def test_analyze_justification_nonempty():
    assert len(analyze_cover_refinement(make_finite(3)).justification) > 0

def test_analyze_value_is_profile():
    r = analyze_cover_refinement(make_finite(3))
    assert isinstance(r.value, dict) and "locally_finite_result" in r.value

def test_analyze_stone_lf_status():
    r = analyze_cover_refinement(_Tagged(tags=["metrizable"]))
    assert r.metadata["locally_finite_status"] == "true"
    assert r.metadata["locally_finite_criterion"] == "stone_theorem"
