"""
test_cilt3_paracompactness_v062.py
====================================
Test suite for src/pytop/paracompactness.py (v0.1.62)
"""
import importlib.util
import os
import sys
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

_pm = _load("pytop.paracompactness", "paracompactness.py")
FiniteTopologicalSpace  = sys.modules["pytop.finite_spaces"].FiniteTopologicalSpace
is_paracompact          = _pm.is_paracompact
paracompact_profile     = _pm.paracompact_profile
analyze_paracompactness = _pm.analyze_paracompactness
ParacompactnessError    = _pm.ParacompactnessError

def make_finite(n):
    c = list(range(n))
    t = [frozenset(s) for r in range(n+1) for s in combinations(c,r)]
    return FiniteTopologicalSpace(carrier=frozenset(c), topology=frozenset(t))

class _Tagged:
    def __init__(self, tags=(), representation="symbolic_general"):
        self.metadata = {"tags": list(tags)}; self.representation = representation


# ---- ParacompactnessError ----
def test_error_is_exception():
    assert issubclass(ParacompactnessError, Exception)

def test_error_can_be_raised():
    with pytest.raises(ParacompactnessError):
        raise ParacompactnessError("test")


# ---- is_paracompact — finite ----
def test_finite_true():
    assert is_paracompact(make_finite(3)).status == "true"

def test_finite_exact():
    assert is_paracompact(make_finite(3)).mode == "exact"

def test_finite_n1():
    assert is_paracompact(make_finite(1)).status == "true"

def test_finite_criterion():
    assert is_paracompact(make_finite(3)).metadata["criterion"] == "finite"

def test_finite_carrier_size():
    assert is_paracompact(make_finite(4)).metadata["carrier_size"] == 4

def test_finite_version():
    assert is_paracompact(make_finite(3)).metadata["version"] == "0.5.3"


# ---- is_paracompact — Stone's theorem ----
def test_metrizable_true():
    assert is_paracompact(_Tagged(tags=["metrizable"])).status == "true"

def test_metric_true():
    assert is_paracompact(_Tagged(tags=["metric"])).status == "true"

def test_stone_criterion():
    assert is_paracompact(_Tagged(tags=["metrizable"])).metadata["criterion"] == "stone_theorem"


# ---- is_paracompact — compact ----
def test_compact_true():
    assert is_paracompact(_Tagged(tags=["compact"])).status == "true"

def test_compact_hausdorff_true():
    assert is_paracompact(_Tagged(tags=["compact_hausdorff"])).status == "true"

def test_compact_criterion():
    assert is_paracompact(_Tagged(tags=["compact"])).metadata["criterion"] == "compact"


# ---- is_paracompact — Michael's theorem ----
def test_michael_t3_lindelof():
    assert is_paracompact(_Tagged(tags=["t3","lindelof"])).status == "true"

def test_michael_hausdorff_second_countable():
    assert is_paracompact(_Tagged(tags=["hausdorff","second_countable"])).status == "true"

def test_michael_regular_second_countable():
    assert is_paracompact(_Tagged(tags=["regular","second_countable"])).status == "true"

def test_michael_tychonoff_lindelof():
    assert is_paracompact(_Tagged(tags=["tychonoff","lindelof"])).status == "true"

def test_michael_criterion():
    r = is_paracompact(_Tagged(tags=["t3","lindelof"]))
    assert r.metadata["criterion"] == "michael_theorem"


# ---- is_paracompact — explicit tag ----
def test_explicit_paracompact_tag():
    assert is_paracompact(_Tagged(tags=["paracompact"])).status == "true"


# ---- is_paracompact — negative ----
def test_not_paracompact_tag_false():
    assert is_paracompact(_Tagged(tags=["not_paracompact"])).status == "false"


# ---- is_paracompact — unknown ----
def test_unknown_generic():
    assert is_paracompact(_Tagged()).status == "unknown"

def test_lindelof_alone_unknown():
    # Lindelöf alone (without regular) should be unknown
    assert is_paracompact(_Tagged(tags=["lindelof"])).status == "unknown"


# ---- paracompact_profile ----
def test_profile_required_keys():
    prof = paracompact_profile(make_finite(3))
    for k in ["is_paracompact_result","is_fully_normal_result","partition_of_unity",
              "locally_finite_covers","key_theorems","counterexamples","representation"]:
        assert k in prof

def test_profile_finite_representation():
    assert paracompact_profile(make_finite(3))["representation"] == "finite"

def test_profile_symbolic_representation():
    assert paracompact_profile(_Tagged())["representation"] == "symbolic_general"

def test_profile_finite_full_normality():
    prof = paracompact_profile(make_finite(3))
    assert prof["is_fully_normal_result"].is_true

def test_profile_finite_partition_of_unity():
    prof = paracompact_profile(make_finite(3))
    assert "yes" in prof["partition_of_unity"].lower()

def test_profile_key_theorems_nonempty():
    prof = paracompact_profile(make_finite(3))
    assert len(prof["key_theorems"]) >= 3

def test_profile_key_theorems_mention_stone():
    prof = paracompact_profile(make_finite(3))
    combined = " ".join(prof["key_theorems"])
    assert "Stone" in combined or "metrizable" in combined.lower()

def test_profile_counterexamples_nonempty():
    prof = paracompact_profile(make_finite(3))
    assert len(prof["counterexamples"]) >= 2

def test_profile_counterexamples_mention_sorgenfrey():
    prof = paracompact_profile(_Tagged())
    combined = " ".join(prof["counterexamples"])
    assert "Sorgenfrey" in combined or "Moore" in combined or "Niemytzki" in combined

def test_profile_metrizable_pou():
    prof = paracompact_profile(_Tagged(tags=["metrizable","hausdorff"]))
    assert "yes" in prof["partition_of_unity"].lower() or "paracompact" in prof["partition_of_unity"].lower()

def test_profile_lf_covers_description():
    prof = paracompact_profile(_Tagged())
    assert "locally finite" in prof["locally_finite_covers"].lower()


# ---- analyze_paracompactness ----
def test_analyze_status_true():
    assert analyze_paracompactness(make_finite(3)).status == "true"

def test_analyze_mode_exact_finite():
    assert analyze_paracompactness(make_finite(3)).mode == "exact"

def test_analyze_mode_theorem_metrizable():
    r = analyze_paracompactness(_Tagged(tags=["metrizable"]))
    assert r.mode == "theorem"

def test_analyze_version():
    assert analyze_paracompactness(make_finite(3)).metadata["version"] == "0.5.3"

def test_analyze_carrier_size():
    assert analyze_paracompactness(make_finite(5)).metadata["carrier_size"] == 5

def test_analyze_paracompact_status():
    assert analyze_paracompactness(make_finite(3)).metadata["paracompact_status"] == "true"

def test_analyze_paracompact_criterion():
    assert analyze_paracompactness(make_finite(3)).metadata["paracompact_criterion"] == "finite"

def test_analyze_justification_nonempty():
    assert len(analyze_paracompactness(make_finite(3)).justification) > 0

def test_analyze_value_is_profile():
    r = analyze_paracompactness(make_finite(3))
    assert isinstance(r.value, dict) and "is_paracompact_result" in r.value

def test_analyze_compact_metrizable():
    r = analyze_paracompactness(_Tagged(tags=["metrizable","compact"]))
    assert r.metadata["paracompact_status"] == "true"
