"""
test_cilt4_cofinality_v067.py
================================
Test suite for src/pytop/cofinality.py (v0.1.67)
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
import pytop as _pytop_pkg  # noqa: E402

_cm = _load("pytop.cofinality", "cofinality.py")
FiniteTopologicalSpace = sys.modules["pytop.finite_spaces"].FiniteTopologicalSpace

cofinality_class   = _cm.cofinality_class
cofinality_profile = _cm.cofinality_profile
analyze_cofinality = _cm.analyze_cofinality
CofinAlityError    = _cm.CofinAlityError


def make_finite(n):
    c = list(range(n))
    t = [frozenset(s) for r in range(n+1) for s in combinations(c,r)]
    return FiniteTopologicalSpace(carrier=frozenset(c), topology=frozenset(t))

class _Tagged:
    def __init__(self, tags=(), representation="symbolic_general"):
        self.metadata = {"tags": list(tags)}
        self.representation = representation

class _Repped:
    def __init__(self, representation):
        self.metadata = {}; self.representation = representation


# ---------------------------------------------------------------------------
# CofinAlityError
# ---------------------------------------------------------------------------

def test_error_is_exception():
    assert issubclass(CofinAlityError, Exception)

def test_error_can_be_raised():
    with pytest.raises(CofinAlityError):
        raise CofinAlityError("test")

def test_error_message():
    try:
        raise CofinAlityError("cf error")
    except CofinAlityError as e:
        assert "cf" in str(e)


# ---------------------------------------------------------------------------
# cofinality_class — finite
# ---------------------------------------------------------------------------

def test_finite_n0():    assert cofinality_class(make_finite(0)) == "finite"
def test_finite_n1():    assert cofinality_class(make_finite(1)) == "finite"
def test_finite_n4():    assert cofinality_class(make_finite(4)) == "finite"
def test_finite_rep():   assert cofinality_class(_Tagged(representation="finite")) == "finite"


# ---------------------------------------------------------------------------
# cofinality_class — omega_regular
# ---------------------------------------------------------------------------

def test_omega_tag():
    assert cofinality_class(_Tagged(tags=["omega"])) == "omega_regular"

def test_omega_countably_infinite():
    assert cofinality_class(_Tagged(tags=["countably_infinite"])) == "omega_regular"

def test_omega_regular_tag():
    assert cofinality_class(_Tagged(tags=["omega_regular"])) == "omega_regular"

def test_omega_rep():
    assert cofinality_class(_Repped("omega_discrete")) == "omega_regular"


# ---------------------------------------------------------------------------
# cofinality_class — successor_regular
# ---------------------------------------------------------------------------

def test_successor_aleph_1():
    assert cofinality_class(_Tagged(tags=["aleph_1"])) == "successor_regular"

def test_successor_aleph_2():
    assert cofinality_class(_Tagged(tags=["aleph_2"])) == "successor_regular"

def test_successor_cardinal_tag():
    assert cofinality_class(_Tagged(tags=["successor_cardinal"])) == "successor_regular"

def test_successor_regular_tag():
    assert cofinality_class(_Tagged(tags=["successor_regular"])) == "successor_regular"


# ---------------------------------------------------------------------------
# cofinality_class — uncountable_regular
# ---------------------------------------------------------------------------

def test_uncountable_reg_omega1():
    assert cofinality_class(_Tagged(tags=["omega_1"])) == "uncountable_regular"

def test_uncountable_reg_first_uncountable():
    assert cofinality_class(_Tagged(tags=["first_uncountable_ordinal"])) == "uncountable_regular"

def test_uncountable_reg_regular_cardinal():
    assert cofinality_class(_Tagged(tags=["regular_cardinal"])) == "uncountable_regular"

def test_uncountable_reg_rep():
    assert cofinality_class(_Repped("omega_1_order_topology")) == "uncountable_regular"


# ---------------------------------------------------------------------------
# cofinality_class — singular
# ---------------------------------------------------------------------------

def test_singular_tag():
    assert cofinality_class(_Tagged(tags=["singular"])) == "singular"

def test_singular_omega_omega():
    assert cofinality_class(_Tagged(tags=["omega_omega"])) == "singular"

def test_singular_aleph_omega():
    assert cofinality_class(_Tagged(tags=["aleph_omega"])) == "singular"

def test_singular_rep():
    assert cofinality_class(_Repped("singular_cardinal_omega_omega")) == "singular"


# ---------------------------------------------------------------------------
# cofinality_class — unknown
# ---------------------------------------------------------------------------

def test_unknown_no_tags():
    assert cofinality_class(_Tagged()) == "unknown"


# ---------------------------------------------------------------------------
# cofinality_profile — all keys present
# ---------------------------------------------------------------------------

REQUIRED_KEYS = [
    "cofinality_class", "cofinality_label", "regularity_status",
    "cofinal_subset_note", "successor_regularity", "singular_examples",
    "topological_bridge", "cardinal_function_bridge",
    "key_theorems", "key_examples", "representation",
]

@pytest.mark.parametrize("space", [
    make_finite(3),
    _Tagged(tags=["omega"]),
    _Tagged(tags=["omega_1"]),
    _Tagged(tags=["singular"]),
    _Tagged(tags=["aleph_1"]),
    _Tagged(),
])
def test_profile_has_all_keys(space):
    p = cofinality_profile(space)
    for key in REQUIRED_KEYS:
        assert key in p, f"Missing key: {key}"


# ---------------------------------------------------------------------------
# cofinality_profile — finite
# ---------------------------------------------------------------------------

def test_profile_finite_class():
    assert cofinality_profile(make_finite(3))["cofinality_class"] == "finite"

def test_profile_finite_regularity():
    assert cofinality_profile(make_finite(3))["regularity_status"] == "trivial"

def test_profile_finite_label_1():
    p = cofinality_profile(make_finite(3))
    assert "1" in p["cofinality_label"]

def test_profile_finite_n0_label():
    p = cofinality_profile(make_finite(0))
    assert "0" in p["cofinality_label"]

def test_profile_finite_key_theorems():
    assert len(cofinality_profile(make_finite(3))["key_theorems"]) >= 5

def test_profile_finite_key_examples():
    assert len(cofinality_profile(make_finite(3))["key_examples"]) >= 5

def test_profile_finite_representation():
    assert cofinality_profile(make_finite(3))["representation"] == "finite"


# ---------------------------------------------------------------------------
# cofinality_profile — omega_regular
# ---------------------------------------------------------------------------

def test_profile_omega_class():
    assert cofinality_profile(_Tagged(tags=["omega"]))["cofinality_class"] == "omega_regular"

def test_profile_omega_regularity():
    assert cofinality_profile(_Tagged(tags=["omega"]))["regularity_status"] == "regular"

def test_profile_omega_label():
    p = cofinality_profile(_Tagged(tags=["omega"]))
    assert "omega" in p["cofinality_label"].lower()

def test_profile_omega_cofinal_note():
    p = cofinality_profile(_Tagged(tags=["omega"]))
    assert "finite" in p["cofinal_subset_note"].lower() or "omega" in p["cofinal_subset_note"].lower()

def test_profile_omega_top_bridge():
    p = cofinality_profile(_Tagged(tags=["omega"]))
    assert "sequence" in p["topological_bridge"].lower() or "first-countable" in p["topological_bridge"].lower()


# ---------------------------------------------------------------------------
# cofinality_profile — successor_regular
# ---------------------------------------------------------------------------

def test_profile_succ_class():
    assert cofinality_profile(_Tagged(tags=["aleph_1"]))["cofinality_class"] == "successor_regular"

def test_profile_succ_regularity():
    assert cofinality_profile(_Tagged(tags=["aleph_1"]))["regularity_status"] == "regular"

def test_profile_succ_regularity_note():
    p = cofinality_profile(_Tagged(tags=["aleph_1"]))
    assert "successor" in p["successor_regularity"].lower()


# ---------------------------------------------------------------------------
# cofinality_profile — uncountable_regular
# ---------------------------------------------------------------------------

def test_profile_uncountable_reg_class():
    assert cofinality_profile(_Tagged(tags=["omega_1"]))["cofinality_class"] == "uncountable_regular"

def test_profile_uncountable_reg_regularity():
    assert cofinality_profile(_Tagged(tags=["omega_1"]))["regularity_status"] == "regular"

def test_profile_uncountable_reg_top_bridge():
    p = cofinality_profile(_Tagged(tags=["omega_1"]))
    assert "compact" in p["topological_bridge"].lower()

def test_profile_uncountable_reg_cofinal_note():
    p = cofinality_profile(_Tagged(tags=["omega_1"]))
    assert "countable" in p["cofinal_subset_note"].lower() or "omega_1" in p["cofinal_subset_note"].lower()


# ---------------------------------------------------------------------------
# cofinality_profile — singular
# ---------------------------------------------------------------------------

def test_profile_singular_class():
    assert cofinality_profile(_Tagged(tags=["singular"]))["cofinality_class"] == "singular"

def test_profile_singular_regularity():
    assert cofinality_profile(_Tagged(tags=["singular"]))["regularity_status"] == "singular"

def test_profile_singular_label():
    p = cofinality_profile(_Tagged(tags=["singular"]))
    assert "kappa" in p["cofinality_label"].lower() or "<" in p["cofinality_label"]

def test_profile_singular_cofinal_note():
    p = cofinality_profile(_Tagged(tags=["singular"]))
    assert "strictly" in p["cofinal_subset_note"].lower() or "less" in p["cofinal_subset_note"].lower()

def test_profile_singular_top_bridge():
    p = cofinality_profile(_Tagged(tags=["omega_omega"]))
    assert "compact" in p["topological_bridge"].lower() or "omega" in p["topological_bridge"].lower()


# ---------------------------------------------------------------------------
# cofinality_profile — unknown
# ---------------------------------------------------------------------------

def test_profile_unknown_class():
    assert cofinality_profile(_Tagged())["cofinality_class"] == "unknown"

def test_profile_unknown_regularity():
    assert cofinality_profile(_Tagged())["regularity_status"] == "unknown"


# ---------------------------------------------------------------------------
# Key theorems content checks
# ---------------------------------------------------------------------------

def test_key_theorems_regular():
    p = cofinality_profile(make_finite(3))
    joined = " ".join(p["key_theorems"]).lower()
    assert "regular" in joined

def test_key_theorems_idempotent():
    p = cofinality_profile(make_finite(3))
    joined = " ".join(p["key_theorems"]).lower()
    assert "idempotent" in joined or "cf(cf" in joined

def test_key_theorems_successor():
    p = cofinality_profile(make_finite(3))
    joined = " ".join(p["key_theorems"]).lower()
    assert "successor" in joined

def test_key_theorems_omega1():
    p = cofinality_profile(make_finite(3))
    joined = " ".join(p["key_theorems"]).lower()
    assert "omega_1" in joined or "uncountable" in joined

def test_key_theorems_countably_compact():
    p = cofinality_profile(make_finite(3))
    joined = " ".join(p["key_theorems"]).lower()
    assert "compact" in joined

def test_key_theorems_konig():
    p = cofinality_profile(make_finite(3))
    joined = " ".join(p["key_theorems"]).lower()
    assert "könig" in joined or "konig" in joined or "könig" in joined


# ---------------------------------------------------------------------------
# Key examples content checks
# ---------------------------------------------------------------------------

def test_key_examples_omega():
    p = cofinality_profile(make_finite(3))
    joined = " ".join(p["key_examples"]).lower()
    assert "omega" in joined

def test_key_examples_omega1_compact():
    p = cofinality_profile(make_finite(3))
    joined = " ".join(p["key_examples"]).lower()
    assert "omega_1" in joined or "countably compact" in joined

def test_key_examples_singular():
    p = cofinality_profile(make_finite(3))
    joined = " ".join(p["key_examples"])
    assert "omega_omega" in joined or "singular" in joined.lower()

def test_key_examples_konig():
    p = cofinality_profile(make_finite(3))
    joined = " ".join(p["key_examples"]).lower()
    assert "könig" in joined or "konig" in joined or "2^" in joined


# ---------------------------------------------------------------------------
# analyze_cofinality — Result shape
# ---------------------------------------------------------------------------

def test_analyze_finite_status():
    assert analyze_cofinality(make_finite(3)).status == "true"

def test_analyze_finite_mode():
    assert analyze_cofinality(make_finite(3)).mode == "exact"

def test_analyze_finite_version():
    assert analyze_cofinality(make_finite(3)).metadata["version"] == "0.1.67"

def test_analyze_finite_carrier_size():
    assert analyze_cofinality(make_finite(4)).metadata["carrier_size"] == 4

def test_analyze_finite_cf_class():
    assert analyze_cofinality(make_finite(3)).metadata["cofinality_class"] == "finite"

def test_analyze_finite_regularity_metadata():
    assert analyze_cofinality(make_finite(3)).metadata["regularity_status"] == "trivial"

def test_analyze_omega_mode():
    assert analyze_cofinality(_Tagged(tags=["omega"])).mode == "theorem"

def test_analyze_omega_status():
    assert analyze_cofinality(_Tagged(tags=["omega"])).status == "true"

def test_analyze_omega_cf_class():
    assert analyze_cofinality(_Tagged(tags=["omega"])).metadata["cofinality_class"] == "omega_regular"

def test_analyze_omega1_mode():
    assert analyze_cofinality(_Tagged(tags=["omega_1"])).mode == "theorem"

def test_analyze_singular_mode():
    assert analyze_cofinality(_Tagged(tags=["singular"])).mode == "theorem"

def test_analyze_singular_cf_class():
    assert analyze_cofinality(_Tagged(tags=["singular"])).metadata["cofinality_class"] == "singular"

def test_analyze_unknown_mode():
    assert analyze_cofinality(_Tagged()).mode == "symbolic"

def test_analyze_value_is_dict():
    assert isinstance(analyze_cofinality(make_finite(3)).value, dict)

def test_analyze_value_has_cf_class():
    assert "cofinality_class" in analyze_cofinality(make_finite(3)).value

def test_analyze_justification_nonempty():
    assert len(analyze_cofinality(make_finite(3)).justification) >= 3

def test_analyze_justification_mentions_cofinality():
    joined = " ".join(analyze_cofinality(make_finite(3)).justification).lower()
    assert "cofinality" in joined or "cf" in joined or "finite" in joined

def test_analyze_domain_rep_metadata():
    assert analyze_cofinality(make_finite(3)).metadata["domain_representation"] == "finite"

def test_analyze_label_metadata_finite():
    r = analyze_cofinality(make_finite(3))
    assert "1" in r.metadata["cofinality_label"] or "0" in r.metadata["cofinality_label"]

def test_analyze_label_metadata_omega():
    r = analyze_cofinality(_Tagged(tags=["omega"]))
    assert "omega" in r.metadata["cofinality_label"].lower()

def test_analyze_label_metadata_singular():
    r = analyze_cofinality(_Tagged(tags=["singular"]))
    assert "kappa" in r.metadata["cofinality_label"].lower() or "<" in r.metadata["cofinality_label"]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def test_public_cofinality_class():
    assert hasattr(_pytop_pkg, "cofinality_class")

def test_public_cofinality_profile():
    assert hasattr(_pytop_pkg, "cofinality_profile")

def test_public_analyze_cofinality():
    assert hasattr(_pytop_pkg, "analyze_cofinality")

def test_public_CofinAlityError():
    assert hasattr(_pytop_pkg, "CofinAlityError")

def test_public_callable():
    assert callable(_pytop_pkg.cofinality_class)
    assert callable(_pytop_pkg.analyze_cofinality)

def test_public_finite_via_package():
    assert _pytop_pkg.cofinality_class(make_finite(2)) == "finite"

def test_public_analyze_via_package():
    r = _pytop_pkg.analyze_cofinality(make_finite(2))
    assert r.status == "true"

def test_public_omega_via_package():
    r = _pytop_pkg.analyze_cofinality(_Tagged(tags=["omega"]))
    assert r.metadata["cofinality_class"] == "omega_regular"


# ---------------------------------------------------------------------------
# Singular examples and successor regularity notes always present
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("space", [
    make_finite(3), _Tagged(tags=["omega"]), _Tagged(tags=["omega_1"]),
    _Tagged(tags=["singular"]), _Tagged(),
])
def test_singular_examples_present(space):
    p = cofinality_profile(space)
    assert len(p["singular_examples"]) > 20

@pytest.mark.parametrize("space", [
    make_finite(3), _Tagged(tags=["omega"]), _Tagged(tags=["omega_1"]),
    _Tagged(tags=["singular"]), _Tagged(),
])
def test_successor_regularity_present(space):
    p = cofinality_profile(space)
    assert "successor" in p["successor_regularity"].lower()

@pytest.mark.parametrize("space", [
    make_finite(3), _Tagged(tags=["omega"]), _Tagged(tags=["omega_1"]),
    _Tagged(tags=["singular"]), _Tagged(),
])
def test_cardinal_function_bridge_present(space):
    p = cofinality_profile(space)
    assert "cardinal" in p["cardinal_function_bridge"].lower()


# ---------------------------------------------------------------------------
# Representation
# ---------------------------------------------------------------------------

def test_representation_finite():
    assert cofinality_profile(make_finite(3))["representation"] == "finite"

def test_representation_symbolic():
    assert cofinality_profile(_Tagged(tags=["omega"]))["representation"] == "symbolic_general"
