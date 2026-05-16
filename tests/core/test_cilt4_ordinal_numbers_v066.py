"""
test_cilt4_ordinal_numbers_v066.py
=====================================
Test suite for src/pytop/ordinal_numbers.py (v0.1.66)

Covers:
- OrdinalNumberError exception
- ordinal_class: finite / omega / infinite_successor / infinite_limit / ordinal_space / unknown
- ordinal_profile: all keys present and correct for each type
- analyze_ordinal_numbers: Result shape, mode, metadata
- Public API accessible from pytop package
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
    mod.__package__ = "pytop"
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))
import pytop as _pytop_pkg  # noqa: E402

_om = _load("pytop.ordinal_numbers", "ordinal_numbers.py")
FiniteTopologicalSpace = sys.modules["pytop.finite_spaces"].FiniteTopologicalSpace

ordinal_class          = _om.ordinal_class
ordinal_profile        = _om.ordinal_profile
analyze_ordinal_numbers = _om.analyze_ordinal_numbers
OrdinalNumberError     = _om.OrdinalNumberError


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
        self.metadata = {}
        self.representation = representation


# ---------------------------------------------------------------------------
# OrdinalNumberError
# ---------------------------------------------------------------------------

def test_error_is_exception():
    assert issubclass(OrdinalNumberError, Exception)

def test_error_can_be_raised():
    with pytest.raises(OrdinalNumberError):
        raise OrdinalNumberError("test")

def test_error_message():
    try:
        raise OrdinalNumberError("bad ordinal")
    except OrdinalNumberError as e:
        assert "bad" in str(e)


# ---------------------------------------------------------------------------
# ordinal_class — finite
# ---------------------------------------------------------------------------

def test_finite_n0():
    assert ordinal_class(make_finite(0)) == "finite_ordinal"

def test_finite_n1():
    assert ordinal_class(make_finite(1)) == "finite_ordinal"

def test_finite_n4():
    assert ordinal_class(make_finite(4)) == "finite_ordinal"

def test_finite_rep():
    assert ordinal_class(_Tagged(representation="finite")) == "finite_ordinal"


# ---------------------------------------------------------------------------
# ordinal_class — omega
# ---------------------------------------------------------------------------

def test_omega_tag():
    assert ordinal_class(_Tagged(tags=["omega"])) == "omega"

def test_omega_tag_first_infinite():
    assert ordinal_class(_Tagged(tags=["first_infinite_ordinal"])) == "omega"

def test_omega_rep():
    assert ordinal_class(_Repped("omega_standard")) == "omega"


# ---------------------------------------------------------------------------
# ordinal_class — infinite_successor
# ---------------------------------------------------------------------------

def test_successor_tag():
    assert ordinal_class(_Tagged(tags=["successor_ordinal"])) == "infinite_successor"

def test_successor_omega_plus_1():
    assert ordinal_class(_Tagged(tags=["omega_plus_1"])) == "infinite_successor"

def test_successor_infinite():
    assert ordinal_class(_Tagged(tags=["infinite_successor"])) == "infinite_successor"


# ---------------------------------------------------------------------------
# ordinal_class — infinite_limit
# ---------------------------------------------------------------------------

def test_limit_tag():
    assert ordinal_class(_Tagged(tags=["limit_ordinal"])) == "infinite_limit"

def test_limit_omega_1():
    assert ordinal_class(_Tagged(tags=["omega_1"])) == "infinite_limit"

def test_limit_omega_squared():
    assert ordinal_class(_Tagged(tags=["omega_squared"])) == "infinite_limit"

def test_limit_first_uncountable():
    assert ordinal_class(_Tagged(tags=["first_uncountable_ordinal"])) == "infinite_limit"


# ---------------------------------------------------------------------------
# ordinal_class — ordinal_space
# ---------------------------------------------------------------------------

def test_ordinal_space_tag():
    assert ordinal_class(_Tagged(tags=["ordinal_space"])) == "ordinal_space"

def test_ordinal_space_long_line():
    assert ordinal_class(_Tagged(tags=["long_line"])) == "ordinal_space"

def test_ordinal_space_order_topology():
    assert ordinal_class(_Tagged(tags=["ordinal_topology"])) == "ordinal_space"

def test_ordinal_space_rep():
    assert ordinal_class(_Repped("ordinal_space_omega1")) == "ordinal_space"


# ---------------------------------------------------------------------------
# ordinal_class — unknown
# ---------------------------------------------------------------------------

def test_unknown_no_tags():
    assert ordinal_class(_Tagged()) == "unknown"

def test_unknown_generic():
    assert ordinal_class(_Tagged(representation="symbolic_general")) == "unknown"


# ---------------------------------------------------------------------------
# ordinal_profile — all keys present
# ---------------------------------------------------------------------------

REQUIRED_KEYS = [
    "ordinal_type", "order_type_label", "well_ordering_note",
    "successor_limit_class", "cardinal_vs_ordinal", "arithmetic_note",
    "transfinite_induction", "cofinality_preview", "topological_bridge",
    "key_theorems", "key_examples", "representation",
]

@pytest.mark.parametrize("space", [
    make_finite(3),
    _Tagged(tags=["omega"]),
    _Tagged(tags=["omega_plus_1"]),
    _Tagged(tags=["limit_ordinal"]),
    _Tagged(tags=["ordinal_space"]),
    _Tagged(),
])
def test_profile_has_all_keys(space):
    p = ordinal_profile(space)
    for key in REQUIRED_KEYS:
        assert key in p, f"Missing key: {key}"


# ---------------------------------------------------------------------------
# ordinal_profile — finite ordinal
# ---------------------------------------------------------------------------

def test_profile_finite_type():
    assert ordinal_profile(make_finite(3))["ordinal_type"] == "finite_ordinal"

def test_profile_finite_label_contains_n():
    assert "3" in ordinal_profile(make_finite(3))["order_type_label"]

def test_profile_finite_sl_class_successor():
    assert ordinal_profile(make_finite(3))["successor_limit_class"] == "successor"

def test_profile_finite_n0_sl_class_zero():
    assert ordinal_profile(make_finite(0))["successor_limit_class"] == "zero"

def test_profile_finite_arithmetic_commutes():
    p = ordinal_profile(make_finite(3))
    assert "commut" in p["arithmetic_note"].lower() or "finite" in p["arithmetic_note"].lower()

def test_profile_finite_induction_ordinary():
    p = ordinal_profile(make_finite(3))
    assert "induction" in p["transfinite_induction"].lower()

def test_profile_finite_key_theorems_nonempty():
    assert len(ordinal_profile(make_finite(3))["key_theorems"]) >= 5

def test_profile_finite_key_examples_nonempty():
    assert len(ordinal_profile(make_finite(3))["key_examples"]) >= 5

def test_profile_finite_representation():
    assert ordinal_profile(make_finite(3))["representation"] == "finite"


# ---------------------------------------------------------------------------
# ordinal_profile — omega
# ---------------------------------------------------------------------------

def test_profile_omega_type():
    assert ordinal_profile(_Tagged(tags=["omega"]))["ordinal_type"] == "omega"

def test_profile_omega_label():
    p = ordinal_profile(_Tagged(tags=["omega"]))
    assert "omega" in p["order_type_label"].lower()

def test_profile_omega_sl_limit():
    assert ordinal_profile(_Tagged(tags=["omega"]))["successor_limit_class"] == "limit"

def test_profile_omega_cardinal_note():
    p = ordinal_profile(_Tagged(tags=["omega"]))
    note = p["cardinal_vs_ordinal"].lower()
    assert "omega" in note and ("aleph" in note or "cardinality" in note)

def test_profile_omega_arithmetic_noncommut():
    p = ordinal_profile(_Tagged(tags=["omega"]))
    assert "commut" in p["arithmetic_note"].lower() or "1 + omega" in p["arithmetic_note"]

def test_profile_omega_cf_preview():
    p = ordinal_profile(_Tagged(tags=["omega"]))
    assert "cf" in p["cofinality_preview"].lower() or "cofinality" in p["cofinality_preview"].lower()

def test_profile_omega_topological_bridge():
    p = ordinal_profile(_Tagged(tags=["omega"]))
    assert "sequence" in p["topological_bridge"].lower() or "omega" in p["topological_bridge"].lower()


# ---------------------------------------------------------------------------
# ordinal_profile — infinite_successor
# ---------------------------------------------------------------------------

def test_profile_successor_type():
    p = ordinal_profile(_Tagged(tags=["omega_plus_1"]))
    assert p["ordinal_type"] == "infinite_successor"

def test_profile_successor_sl_class():
    assert ordinal_profile(_Tagged(tags=["omega_plus_1"]))["successor_limit_class"] == "successor"

def test_profile_successor_cf_preview():
    p = ordinal_profile(_Tagged(tags=["omega_plus_1"]))
    assert "1" in p["cofinality_preview"] or "successor" in p["cofinality_preview"].lower()

def test_profile_successor_cardinal_note():
    p = ordinal_profile(_Tagged(tags=["omega_plus_1"]))
    note = p["cardinal_vs_ordinal"].lower()
    assert "cardinality" in note or "ordinal" in note


# ---------------------------------------------------------------------------
# ordinal_profile — infinite_limit
# ---------------------------------------------------------------------------

def test_profile_limit_type():
    assert ordinal_profile(_Tagged(tags=["limit_ordinal"]))["ordinal_type"] == "infinite_limit"

def test_profile_limit_sl_class():
    assert ordinal_profile(_Tagged(tags=["limit_ordinal"]))["successor_limit_class"] == "limit"

def test_profile_limit_cf_preview():
    p = ordinal_profile(_Tagged(tags=["limit_ordinal"]))
    assert "cofinality" in p["cofinality_preview"].lower() or "cf" in p["cofinality_preview"].lower()

def test_profile_limit_top_bridge():
    p = ordinal_profile(_Tagged(tags=["omega_1"]))
    assert "compact" in p["topological_bridge"].lower() or "ordinal" in p["topological_bridge"].lower()


# ---------------------------------------------------------------------------
# ordinal_profile — ordinal_space
# ---------------------------------------------------------------------------

def test_profile_ordinal_space_type():
    assert ordinal_profile(_Tagged(tags=["ordinal_space"]))["ordinal_type"] == "ordinal_space"

def test_profile_ordinal_space_sl_class():
    assert ordinal_profile(_Tagged(tags=["ordinal_space"]))["successor_limit_class"] == "limit"

def test_profile_ordinal_space_topological_bridge():
    p = ordinal_profile(_Tagged(tags=["ordinal_space"]))
    assert "compact" in p["topological_bridge"].lower() or "counterexample" in p["topological_bridge"].lower()

def test_profile_ordinal_space_cf_preview():
    p = ordinal_profile(_Tagged(tags=["ordinal_space"]))
    assert "cofinality" in p["cofinality_preview"].lower() or "alpha" in p["cofinality_preview"].lower()


# ---------------------------------------------------------------------------
# ordinal_profile — unknown
# ---------------------------------------------------------------------------

def test_profile_unknown_type():
    assert ordinal_profile(_Tagged())["ordinal_type"] == "unknown"

def test_profile_unknown_sl_class():
    assert ordinal_profile(_Tagged())["successor_limit_class"] == "unknown"

def test_profile_unknown_label():
    assert "unknown" in ordinal_profile(_Tagged())["order_type_label"].lower()


# ---------------------------------------------------------------------------
# Key theorems content checks
# ---------------------------------------------------------------------------

def test_key_theorems_trichotomy():
    p = ordinal_profile(make_finite(3))
    joined = " ".join(p["key_theorems"]).lower()
    assert "trichotomy" in joined or "successor" in joined or "limit" in joined

def test_key_theorems_transfinite_induction():
    p = ordinal_profile(make_finite(3))
    joined = " ".join(p["key_theorems"]).lower()
    assert "transfinite" in joined or "induction" in joined

def test_key_theorems_arithmetic_noncommut():
    p = ordinal_profile(make_finite(3))
    joined = " ".join(p["key_theorems"]).lower()
    assert "commut" in joined or "1 + omega" in joined

def test_key_theorems_cardinal_ordinal_distinction():
    p = ordinal_profile(make_finite(3))
    joined = " ".join(p["key_theorems"]).lower()
    assert "cardinal" in joined or "cardinality" in joined

def test_key_theorems_cofinality_mentioned():
    p = ordinal_profile(make_finite(3))
    joined = " ".join(p["key_theorems"]).lower()
    assert "cofinality" in joined or "cf(" in joined


# ---------------------------------------------------------------------------
# Key examples content checks
# ---------------------------------------------------------------------------

def test_key_examples_omega():
    p = ordinal_profile(make_finite(3))
    joined = " ".join(p["key_examples"]).lower()
    assert "omega" in joined

def test_key_examples_omega_plus_1():
    p = ordinal_profile(make_finite(3))
    joined = " ".join(p["key_examples"])
    assert "omega+1" in joined or "omega + 1" in joined or "omega_1" in joined.lower()

def test_key_examples_long_line():
    p = ordinal_profile(make_finite(3))
    joined = " ".join(p["key_examples"]).lower()
    assert "long line" in joined or "long_line" in joined

def test_key_examples_von_neumann():
    p = ordinal_profile(make_finite(3))
    joined = " ".join(p["key_examples"]).lower()
    assert "von neumann" in joined or "{0" in joined


# ---------------------------------------------------------------------------
# analyze_ordinal_numbers — Result shape
# ---------------------------------------------------------------------------

def test_analyze_finite_status():
    assert analyze_ordinal_numbers(make_finite(3)).status == "true"

def test_analyze_finite_mode():
    assert analyze_ordinal_numbers(make_finite(3)).mode == "exact"

def test_analyze_finite_version():
    assert analyze_ordinal_numbers(make_finite(3)).metadata["version"] == "0.1.66"

def test_analyze_finite_carrier_size():
    assert analyze_ordinal_numbers(make_finite(4)).metadata["carrier_size"] == 4

def test_analyze_finite_ordinal_type():
    assert analyze_ordinal_numbers(make_finite(3)).metadata["ordinal_type"] == "finite_ordinal"

def test_analyze_finite_sl_metadata():
    r = analyze_ordinal_numbers(make_finite(3))
    assert r.metadata["successor_limit_class"] == "successor"

def test_analyze_omega_mode():
    assert analyze_ordinal_numbers(_Tagged(tags=["omega"])).mode == "theorem"

def test_analyze_omega_status():
    assert analyze_ordinal_numbers(_Tagged(tags=["omega"])).status == "true"

def test_analyze_omega_type_metadata():
    r = analyze_ordinal_numbers(_Tagged(tags=["omega"]))
    assert r.metadata["ordinal_type"] == "omega"

def test_analyze_successor_mode():
    r = analyze_ordinal_numbers(_Tagged(tags=["omega_plus_1"]))
    assert r.mode == "theorem"

def test_analyze_limit_mode():
    r = analyze_ordinal_numbers(_Tagged(tags=["limit_ordinal"]))
    assert r.mode == "theorem"

def test_analyze_ordinal_space_mode():
    r = analyze_ordinal_numbers(_Tagged(tags=["ordinal_space"]))
    assert r.mode == "theorem"

def test_analyze_unknown_mode():
    r = analyze_ordinal_numbers(_Tagged())
    assert r.mode == "symbolic"

def test_analyze_value_is_dict():
    assert isinstance(analyze_ordinal_numbers(make_finite(3)).value, dict)

def test_analyze_value_has_ordinal_type():
    assert "ordinal_type" in analyze_ordinal_numbers(make_finite(3)).value

def test_analyze_justification_nonempty():
    r = analyze_ordinal_numbers(make_finite(3))
    assert len(r.justification) >= 3

def test_analyze_justification_mentions_type():
    r = analyze_ordinal_numbers(make_finite(3))
    joined = " ".join(r.justification).lower()
    assert "ordinal" in joined or "finite" in joined

def test_analyze_domain_representation_metadata():
    r = analyze_ordinal_numbers(make_finite(3))
    assert r.metadata["domain_representation"] == "finite"

def test_analyze_label_metadata_finite():
    r = analyze_ordinal_numbers(make_finite(4))
    assert "4" in r.metadata["order_type_label"]

def test_analyze_label_metadata_omega():
    r = analyze_ordinal_numbers(_Tagged(tags=["omega"]))
    assert "omega" in r.metadata["order_type_label"].lower()


# ---------------------------------------------------------------------------
# Public API — accessible from pytop package
# ---------------------------------------------------------------------------

def test_public_ordinal_class():
    assert hasattr(_pytop_pkg, "ordinal_class")

def test_public_ordinal_profile():
    assert hasattr(_pytop_pkg, "ordinal_profile")

def test_public_analyze_ordinal_numbers():
    assert hasattr(_pytop_pkg, "analyze_ordinal_numbers")

def test_public_OrdinalNumberError():
    assert hasattr(_pytop_pkg, "OrdinalNumberError")

def test_public_ordinal_class_callable():
    assert callable(_pytop_pkg.ordinal_class)

def test_public_analyze_callable():
    assert callable(_pytop_pkg.analyze_ordinal_numbers)

def test_public_finite_via_package():
    assert _pytop_pkg.ordinal_class(make_finite(2)) == "finite_ordinal"

def test_public_analyze_via_package():
    r = _pytop_pkg.analyze_ordinal_numbers(make_finite(2))
    assert r.status == "true"

def test_public_omega_via_package():
    r = _pytop_pkg.analyze_ordinal_numbers(_Tagged(tags=["omega"]))
    assert r.metadata["ordinal_type"] == "omega"


# ---------------------------------------------------------------------------
# Representation recorded correctly
# ---------------------------------------------------------------------------

def test_representation_finite():
    assert ordinal_profile(make_finite(3))["representation"] == "finite"

def test_representation_symbolic():
    assert ordinal_profile(_Tagged(tags=["omega"]))["representation"] == "symbolic_general"

def test_representation_ordinal_space():
    p = ordinal_profile(_Tagged(tags=["ordinal_space"], representation="ordinal_space_omega1"))
    assert "ordinal" in p["representation"]
