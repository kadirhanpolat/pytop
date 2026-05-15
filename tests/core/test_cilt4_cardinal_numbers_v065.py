"""
test_cilt4_cardinal_numbers_v065.py
=====================================
Test suite for src/pytop/cardinal_numbers.py (v0.1.65)

Covers:
- CardinalNumberError exception
- cardinality_class: finite / countably_infinite / continuum / uncountable / unknown
- cardinal_number_profile: all keys present and correct for each tier
- analyze_cardinal_numbers: Result shape, mode, metadata
- Public API accessible from pytop package
"""
import importlib.util
import sys
import os
from itertools import combinations

import pytest

# ---------------------------------------------------------------------------
# Module loading helpers
# ---------------------------------------------------------------------------
_BASE = os.path.join(os.path.dirname(__file__), "..", "..", "src", "pytop")


def _load(name, rel):
    path = os.path.normpath(os.path.join(_BASE, rel))
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    mod.__package__ = "pytop"
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


sys.path.insert(
    0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
)
import pytop as _pytop_pkg

_cm = _load("pytop.cardinal_numbers", "cardinal_numbers.py")

FiniteTopologicalSpace = sys.modules["pytop.finite_spaces"].FiniteTopologicalSpace

cardinality_class       = _cm.cardinality_class
cardinal_number_profile = _cm.cardinal_number_profile
analyze_cardinal_numbers = _cm.analyze_cardinal_numbers
CardinalNumberError     = _cm.CardinalNumberError


# ---------------------------------------------------------------------------
# Space factories
# ---------------------------------------------------------------------------

def make_finite(n):
    """Concrete FiniteTopologicalSpace with n points (discrete topology)."""
    c = list(range(n))
    t = [frozenset(s) for r in range(n + 1) for s in combinations(c, r)]
    return FiniteTopologicalSpace(carrier=frozenset(c), topology=frozenset(t))


class _Tagged:
    """Minimal symbolic space with metadata tags."""
    def __init__(self, tags=(), representation="symbolic_general"):
        self.metadata = {"tags": list(tags)}
        self.representation = representation


class _Repped:
    """Symbolic space with explicit representation string."""
    def __init__(self, representation):
        self.metadata = {}
        self.representation = representation


# ---------------------------------------------------------------------------
# CardinalNumberError
# ---------------------------------------------------------------------------

def test_error_is_exception():
    assert issubclass(CardinalNumberError, Exception)


def test_error_can_be_raised():
    with pytest.raises(CardinalNumberError):
        raise CardinalNumberError("test")


def test_error_message():
    try:
        raise CardinalNumberError("bad input")
    except CardinalNumberError as e:
        assert "bad" in str(e)


# ---------------------------------------------------------------------------
# cardinality_class — finite
# ---------------------------------------------------------------------------

def test_finite_space_tier():
    assert cardinality_class(make_finite(3)) == "finite"


def test_finite_n0():
    assert cardinality_class(make_finite(0)) == "finite"


def test_finite_n1():
    assert cardinality_class(make_finite(1)) == "finite"


def test_finite_n5():
    assert cardinality_class(make_finite(5)) == "finite"


def test_finite_rep_tag():
    assert cardinality_class(_Tagged(representation="finite")) == "finite"


# ---------------------------------------------------------------------------
# cardinality_class — countably infinite
# ---------------------------------------------------------------------------

def test_countable_tag_omega():
    assert cardinality_class(_Tagged(tags=["omega"])) == "countably_infinite"


def test_countable_tag_discrete_countable():
    assert cardinality_class(_Tagged(tags=["discrete_countable"])) == "countably_infinite"


def test_countable_tag_rationals():
    assert cardinality_class(_Tagged(tags=["rationals"])) == "countably_infinite"


def test_countable_tag_countably_infinite():
    assert cardinality_class(_Tagged(tags=["countably_infinite"])) == "countably_infinite"


def test_countable_rep_string():
    assert cardinality_class(_Repped("countable_discrete")) == "countably_infinite"


# ---------------------------------------------------------------------------
# cardinality_class — continuum
# ---------------------------------------------------------------------------

def test_continuum_tag_real_line():
    assert cardinality_class(_Tagged(tags=["real_line"])) == "continuum"


def test_continuum_tag_reals():
    assert cardinality_class(_Tagged(tags=["reals"])) == "continuum"


def test_continuum_tag_continuum():
    assert cardinality_class(_Tagged(tags=["continuum"])) == "continuum"


def test_continuum_tag_cantor_set():
    assert cardinality_class(_Tagged(tags=["cantor_set"])) == "continuum"


def test_continuum_tag_hilbert_cube():
    assert cardinality_class(_Tagged(tags=["hilbert_cube"])) == "continuum"


def test_continuum_rep_real():
    assert cardinality_class(_Repped("real_line_standard")) == "continuum"


# ---------------------------------------------------------------------------
# cardinality_class — uncountable
# ---------------------------------------------------------------------------

def test_uncountable_tag():
    assert cardinality_class(_Tagged(tags=["uncountable"])) == "uncountable"


def test_uncountable_tag_variant():
    assert cardinality_class(_Tagged(tags=["uncountably_infinite"])) == "uncountable"


# ---------------------------------------------------------------------------
# cardinality_class — unknown
# ---------------------------------------------------------------------------

def test_unknown_no_tags():
    assert cardinality_class(_Tagged()) == "unknown"


def test_unknown_generic_symbolic():
    assert cardinality_class(_Tagged(representation="symbolic_general")) == "unknown"


# ---------------------------------------------------------------------------
# cardinal_number_profile — keys present
# ---------------------------------------------------------------------------

_REQUIRED_KEYS = [
    "cardinality_tier",
    "cardinality_label",
    "equinumerosity_note",
    "countability_threshold",
    "power_set_tier",
    "schroeder_bernstein_note",
    "continuum_note",
    "topological_bridge",
    "key_theorems",
    "key_examples",
    "representation",
]


@pytest.mark.parametrize("space", [
    make_finite(3),
    _Tagged(tags=["omega"]),
    _Tagged(tags=["real_line"]),
    _Tagged(tags=["uncountable"]),
    _Tagged(),
])
def test_profile_has_all_keys(space):
    profile = cardinal_number_profile(space)
    for key in _REQUIRED_KEYS:
        assert key in profile, f"Missing key: {key}"


# ---------------------------------------------------------------------------
# cardinal_number_profile — finite tier
# ---------------------------------------------------------------------------

def test_profile_finite_tier():
    p = cardinal_number_profile(make_finite(4))
    assert p["cardinality_tier"] == "finite"


def test_profile_finite_label_contains_n():
    p = cardinal_number_profile(make_finite(4))
    assert "4" in p["cardinality_label"]


def test_profile_finite_threshold_keyword():
    p = cardinal_number_profile(make_finite(4))
    assert "finite" in p["countability_threshold"].lower()


def test_profile_finite_power_set_note():
    p = cardinal_number_profile(make_finite(4))
    assert "2^" in p["power_set_tier"] or "P(X)" in p["power_set_tier"]


def test_profile_finite_topological_bridge():
    p = cardinal_number_profile(make_finite(4))
    assert "cardinal" in p["topological_bridge"].lower()


def test_profile_finite_key_theorems_nonempty():
    p = cardinal_number_profile(make_finite(4))
    assert len(p["key_theorems"]) >= 5


def test_profile_finite_key_examples_nonempty():
    p = cardinal_number_profile(make_finite(4))
    assert len(p["key_examples"]) >= 5


def test_profile_finite_sb_note():
    p = cardinal_number_profile(make_finite(4))
    assert "Schroeder" in p["schroeder_bernstein_note"] or "Bernstein" in p["schroeder_bernstein_note"]


def test_profile_finite_representation():
    p = cardinal_number_profile(make_finite(4))
    assert p["representation"] == "finite"


# ---------------------------------------------------------------------------
# cardinal_number_profile — countably infinite tier
# ---------------------------------------------------------------------------

def test_profile_countable_tier():
    p = cardinal_number_profile(_Tagged(tags=["omega"]))
    assert p["cardinality_tier"] == "countably_infinite"


def test_profile_countable_label_aleph():
    p = cardinal_number_profile(_Tagged(tags=["omega"]))
    assert "aleph" in p["cardinality_label"].lower() or "0" in p["cardinality_label"]


def test_profile_countable_threshold():
    p = cardinal_number_profile(_Tagged(tags=["omega"]))
    assert "aleph" in p["countability_threshold"].lower() or "countably" in p["countability_threshold"].lower()


def test_profile_countable_power_set_continuum():
    p = cardinal_number_profile(_Tagged(tags=["omega"]))
    assert "continuum" in p["power_set_tier"].lower() or "c" in p["power_set_tier"].lower()


def test_profile_countable_continuum_note():
    p = cardinal_number_profile(_Tagged(tags=["omega"]))
    assert "aleph" in p["continuum_note"].lower() or "countably" in p["continuum_note"].lower()


def test_profile_countable_topological_bridge():
    p = cardinal_number_profile(_Tagged(tags=["omega"]))
    assert "aleph" in p["topological_bridge"].lower() or "second" in p["topological_bridge"].lower()


# ---------------------------------------------------------------------------
# cardinal_number_profile — continuum tier
# ---------------------------------------------------------------------------

def test_profile_continuum_tier():
    p = cardinal_number_profile(_Tagged(tags=["real_line"]))
    assert p["cardinality_tier"] == "continuum"


def test_profile_continuum_label():
    p = cardinal_number_profile(_Tagged(tags=["real_line"]))
    assert "c" in p["cardinality_label"].lower() or "continuum" in p["cardinality_label"].lower()


def test_profile_continuum_threshold_uncountable():
    p = cardinal_number_profile(_Tagged(tags=["real_line"]))
    assert "uncountable" in p["countability_threshold"].lower()


def test_profile_continuum_power_set_note():
    p = cardinal_number_profile(_Tagged(tags=["real_line"]))
    assert "2^c" in p["power_set_tier"] or "strictly larger" in p["power_set_tier"]


def test_profile_continuum_note_ch():
    p = cardinal_number_profile(_Tagged(tags=["real_line"]))
    # continuum note should mention continuum hypothesis or Cohen/Goedel
    note = p["continuum_note"].lower()
    assert "continuum" in note or "hypothesis" in note or "cohen" in note


def test_profile_continuum_topological_bridge():
    p = cardinal_number_profile(_Tagged(tags=["real_line"]))
    assert "cardinal" in p["topological_bridge"].lower()


# ---------------------------------------------------------------------------
# cardinal_number_profile — uncountable tier
# ---------------------------------------------------------------------------

def test_profile_uncountable_tier():
    p = cardinal_number_profile(_Tagged(tags=["uncountable"]))
    assert p["cardinality_tier"] == "uncountable"


def test_profile_uncountable_label():
    p = cardinal_number_profile(_Tagged(tags=["uncountable"]))
    assert "aleph" in p["cardinality_label"].lower() or "unknown" in p["cardinality_label"].lower()


def test_profile_uncountable_threshold():
    p = cardinal_number_profile(_Tagged(tags=["uncountable"]))
    assert "uncountable" in p["countability_threshold"].lower() or "aleph" in p["countability_threshold"].lower()


# ---------------------------------------------------------------------------
# cardinal_number_profile — unknown tier
# ---------------------------------------------------------------------------

def test_profile_unknown_tier():
    p = cardinal_number_profile(_Tagged())
    assert p["cardinality_tier"] == "unknown"


def test_profile_unknown_label():
    p = cardinal_number_profile(_Tagged())
    assert "unknown" in p["cardinality_label"].lower()


# ---------------------------------------------------------------------------
# analyze_cardinal_numbers — Result shape
# ---------------------------------------------------------------------------

def test_analyze_finite_status():
    r = analyze_cardinal_numbers(make_finite(3))
    assert r.status == "true"


def test_analyze_finite_mode():
    r = analyze_cardinal_numbers(make_finite(3))
    assert r.mode == "exact"


def test_analyze_finite_version():
    r = analyze_cardinal_numbers(make_finite(3))
    assert r.metadata["version"] == "0.1.65"


def test_analyze_finite_carrier_size():
    r = analyze_cardinal_numbers(make_finite(5))
    assert r.metadata["carrier_size"] == 5


def test_analyze_finite_tier_metadata():
    r = analyze_cardinal_numbers(make_finite(3))
    assert r.metadata["cardinality_tier"] == "finite"


def test_analyze_countable_mode():
    r = analyze_cardinal_numbers(_Tagged(tags=["omega"]))
    assert r.mode == "theorem"


def test_analyze_countable_status():
    r = analyze_cardinal_numbers(_Tagged(tags=["omega"]))
    assert r.status == "true"


def test_analyze_countable_tier_metadata():
    r = analyze_cardinal_numbers(_Tagged(tags=["omega"]))
    assert r.metadata["cardinality_tier"] == "countably_infinite"


def test_analyze_continuum_mode():
    r = analyze_cardinal_numbers(_Tagged(tags=["real_line"]))
    assert r.mode == "theorem"


def test_analyze_continuum_tier_metadata():
    r = analyze_cardinal_numbers(_Tagged(tags=["real_line"]))
    assert r.metadata["cardinality_tier"] == "continuum"


def test_analyze_uncountable_mode():
    r = analyze_cardinal_numbers(_Tagged(tags=["uncountable"]))
    assert r.mode == "theorem"


def test_analyze_unknown_mode():
    r = analyze_cardinal_numbers(_Tagged())
    assert r.mode == "symbolic"


def test_analyze_value_is_dict():
    r = analyze_cardinal_numbers(make_finite(3))
    assert isinstance(r.value, dict)


def test_analyze_value_has_cardinality_tier():
    r = analyze_cardinal_numbers(make_finite(3))
    assert "cardinality_tier" in r.value


def test_analyze_justification_nonempty():
    r = analyze_cardinal_numbers(make_finite(3))
    assert len(r.justification) >= 3


def test_analyze_justification_mentions_tier():
    r = analyze_cardinal_numbers(make_finite(3))
    joined = " ".join(r.justification).lower()
    assert "tier" in joined or "finite" in joined


def test_analyze_domain_representation_metadata():
    r = analyze_cardinal_numbers(make_finite(3))
    assert r.metadata["domain_representation"] == "finite"


def test_analyze_label_metadata_finite():
    r = analyze_cardinal_numbers(make_finite(4))
    assert "4" in r.metadata["cardinality_label"]


def test_analyze_label_metadata_countable():
    r = analyze_cardinal_numbers(_Tagged(tags=["omega"]))
    assert "aleph" in r.metadata["cardinality_label"].lower() or "0" in r.metadata["cardinality_label"]


def test_analyze_label_metadata_continuum():
    r = analyze_cardinal_numbers(_Tagged(tags=["real_line"]))
    label = r.metadata["cardinality_label"].lower()
    assert "c" in label or "continuum" in label


# ---------------------------------------------------------------------------
# Public API — accessible from pytop package
# ---------------------------------------------------------------------------

def test_public_cardinality_class():
    assert hasattr(_pytop_pkg, "cardinality_class")


def test_public_cardinal_number_profile():
    assert hasattr(_pytop_pkg, "cardinal_number_profile")


def test_public_analyze_cardinal_numbers():
    assert hasattr(_pytop_pkg, "analyze_cardinal_numbers")


def test_public_CardinalNumberError():
    assert hasattr(_pytop_pkg, "CardinalNumberError")


def test_public_cardinality_class_callable():
    assert callable(_pytop_pkg.cardinality_class)


def test_public_analyze_callable():
    assert callable(_pytop_pkg.analyze_cardinal_numbers)


def test_public_finite_via_package():
    result = _pytop_pkg.cardinality_class(make_finite(2))
    assert result == "finite"


def test_public_analyze_via_package():
    r = _pytop_pkg.analyze_cardinal_numbers(make_finite(2))
    assert r.status == "true"


# ---------------------------------------------------------------------------
# Key theorems content checks
# ---------------------------------------------------------------------------

def test_key_theorems_equinumerosity():
    p = cardinal_number_profile(make_finite(3))
    joined = " ".join(p["key_theorems"]).lower()
    assert "equivalence" in joined or "equinumer" in joined


def test_key_theorems_cantor():
    p = cardinal_number_profile(make_finite(3))
    joined = " ".join(p["key_theorems"]).lower()
    assert "cantor" in joined


def test_key_theorems_schroeder_bernstein():
    p = cardinal_number_profile(make_finite(3))
    joined = " ".join(p["key_theorems"]).lower()
    assert "schroeder" in joined or "bernstein" in joined


def test_key_theorems_diagonal():
    p = cardinal_number_profile(make_finite(3))
    joined = " ".join(p["key_theorems"]).lower()
    assert "diagonal" in joined


def test_key_theorems_power_set():
    p = cardinal_number_profile(make_finite(3))
    joined = " ".join(p["key_theorems"]).lower()
    assert "power" in joined or "p(a)" in joined


# ---------------------------------------------------------------------------
# Key examples content checks
# ---------------------------------------------------------------------------

def test_key_examples_naturals():
    p = cardinal_number_profile(make_finite(3))
    joined = " ".join(p["key_examples"]).lower()
    assert "n" in joined or "natural" in joined


def test_key_examples_rationals():
    p = cardinal_number_profile(make_finite(3))
    joined = " ".join(p["key_examples"]).lower()
    assert "q" in joined or "rational" in joined


def test_key_examples_reals():
    p = cardinal_number_profile(make_finite(3))
    joined = " ".join(p["key_examples"]).lower()
    assert "r" in joined or "real" in joined or "uncountable" in joined


def test_key_examples_continuum():
    p = cardinal_number_profile(make_finite(3))
    joined = " ".join(p["key_examples"]).lower()
    assert "continuum" in joined or "c" in joined or "interval" in joined


# ---------------------------------------------------------------------------
# Schroeder-Bernstein note universality
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("space", [
    make_finite(3),
    _Tagged(tags=["omega"]),
    _Tagged(tags=["real_line"]),
    _Tagged(tags=["uncountable"]),
    _Tagged(),
])
def test_sb_note_always_present(space):
    p = cardinal_number_profile(space)
    assert len(p["schroeder_bernstein_note"]) > 20


# ---------------------------------------------------------------------------
# Representation recorded correctly
# ---------------------------------------------------------------------------

def test_representation_finite():
    p = cardinal_number_profile(make_finite(3))
    assert p["representation"] == "finite"


def test_representation_symbolic():
    p = cardinal_number_profile(_Tagged(tags=["omega"]))
    assert p["representation"] == "symbolic_general"


def test_representation_real_line():
    p = cardinal_number_profile(_Tagged(tags=["real_line"], representation="real_line_standard"))
    assert "real" in p["representation"]
