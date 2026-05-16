"""
test_cilt4_quantitative_topology_v068.py
==========================================
Test suite for src/pytop/quantitative_topology.py (v0.1.68)
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
    mod = importlib.util.module_from_spec(spec); mod.__package__ = "pytop"
    sys.modules[name] = mod; spec.loader.exec_module(mod); return mod

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))
import pytop as _pytop_pkg  # noqa: E402

_qm = _load("pytop.quantitative_topology", "quantitative_topology.py")
FiniteTopologicalSpace = sys.modules["pytop.finite_spaces"].FiniteTopologicalSpace

quantitative_profile         = _qm.quantitative_profile
analyze_quantitative_topology = _qm.analyze_quantitative_topology
QuantitativeTopologyError    = _qm.QuantitativeTopologyError


def make_finite(n):
    c = list(range(n)); t = [frozenset(s) for r in range(n+1) for s in combinations(c,r)]
    return FiniteTopologicalSpace(carrier=frozenset(c), topology=frozenset(t))

class _Tagged:
    def __init__(self, tags=(), representation="symbolic_general"):
        self.metadata = {"tags": list(tags)}; self.representation = representation


# ---------------------------------------------------------------------------
# QuantitativeTopologyError
# ---------------------------------------------------------------------------
def test_error_is_exception():
    assert issubclass(QuantitativeTopologyError, Exception)

def test_error_can_be_raised():
    with pytest.raises(QuantitativeTopologyError):
        raise QuantitativeTopologyError("qt error")


# ---------------------------------------------------------------------------
# quantitative_profile -- all keys
# ---------------------------------------------------------------------------
REQUIRED_KEYS = [
    "weight", "density", "character", "lindelof_number",
    "qualitative_quantitative_bridge", "set_theoretic_bridge",
    "threshold_instances", "pedagogical_positioning",
    "key_inequalities", "key_examples", "representation",
]

@pytest.mark.parametrize("space", [
    make_finite(3),
    _Tagged(tags=["second_countable"]),
    _Tagged(tags=["real_line"]),
    _Tagged(tags=["discrete_uncountable"]),
    _Tagged(tags=["indiscrete"]),
    _Tagged(),
])
def test_profile_has_all_keys(space):
    p = quantitative_profile(space)
    for key in REQUIRED_KEYS:
        assert key in p, f"Missing key: {key}"


# ---------------------------------------------------------------------------
# Finite space
# ---------------------------------------------------------------------------
def test_finite_weight():   assert "finite" in quantitative_profile(make_finite(3))["weight"].lower()
def test_finite_density():  assert "finite" in quantitative_profile(make_finite(3))["density"].lower()
def test_finite_char():     assert "finite" in quantitative_profile(make_finite(3))["character"].lower()
def test_finite_lindelof(): assert "finite" in quantitative_profile(make_finite(3))["lindelof_number"].lower()
def test_finite_n4_weight(): assert "4" in quantitative_profile(make_finite(4))["weight"] or "finite" in quantitative_profile(make_finite(4))["weight"].lower()
def test_finite_key_ineqs(): assert len(quantitative_profile(make_finite(3))["key_inequalities"]) >= 5
def test_finite_key_examples(): assert len(quantitative_profile(make_finite(3))["key_examples"]) >= 5
def test_finite_representation(): assert quantitative_profile(make_finite(3))["representation"] == "finite"


# ---------------------------------------------------------------------------
# Second-countable space
# ---------------------------------------------------------------------------
def test_second_countable_weight():
    assert "aleph_0" in quantitative_profile(_Tagged(tags=["second_countable"]))["weight"]

def test_second_countable_density():
    assert "aleph_0" in quantitative_profile(_Tagged(tags=["second_countable"]))["density"]


# ---------------------------------------------------------------------------
# Real line
# ---------------------------------------------------------------------------
def test_real_line_weight():    assert "aleph_0" in quantitative_profile(_Tagged(tags=["real_line"]))["weight"]
def test_real_line_density():   assert "aleph_0" in quantitative_profile(_Tagged(tags=["real_line"]))["density"]
def test_real_line_character(): assert "aleph_0" in quantitative_profile(_Tagged(tags=["real_line"]))["character"]
def test_real_line_lindelof():  assert "aleph_0" in quantitative_profile(_Tagged(tags=["real_line"]))["lindelof_number"]


# ---------------------------------------------------------------------------
# Indiscrete space
# ---------------------------------------------------------------------------
def test_indiscrete_weight():   assert "1" in quantitative_profile(_Tagged(tags=["indiscrete"]))["weight"]
def test_indiscrete_density():  assert "1" in quantitative_profile(_Tagged(tags=["indiscrete"]))["density"]
def test_indiscrete_character(): assert "1" in quantitative_profile(_Tagged(tags=["indiscrete"]))["character"]


# ---------------------------------------------------------------------------
# Discrete uncountable space
# ---------------------------------------------------------------------------
def test_discrete_uncountable_weight():
    p = quantitative_profile(_Tagged(tags=["discrete_uncountable"]))
    assert "|X|" in p["weight"] or "uncountable" in p["weight"].lower()

def test_discrete_uncountable_density():
    p = quantitative_profile(_Tagged(tags=["discrete_uncountable"]))
    assert "|X|" in p["density"] or "uncountable" in p["density"].lower()


# ---------------------------------------------------------------------------
# Compact space (Lindelof)
# ---------------------------------------------------------------------------
def test_compact_lindelof():
    p = quantitative_profile(_Tagged(tags=["compact"]))
    assert "1" in p["lindelof_number"] or "finite" in p["lindelof_number"].lower()


# ---------------------------------------------------------------------------
# Bridges -- always present
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("space", [
    make_finite(3), _Tagged(tags=["real_line"]), _Tagged(tags=["second_countable"]),
    _Tagged(tags=["discrete_uncountable"]), _Tagged(),
])
def test_qq_bridge_present(space):
    p = quantitative_profile(space)
    assert len(p["qualitative_quantitative_bridge"]) > 30
    assert "qualitative" in p["qualitative_quantitative_bridge"].lower() or "w(X)" in p["qualitative_quantitative_bridge"]

@pytest.mark.parametrize("space", [
    make_finite(3), _Tagged(tags=["real_line"]), _Tagged(),
])
def test_set_theoretic_bridge_present(space):
    p = quantitative_profile(space)
    assert "cardinal" in p["set_theoretic_bridge"].lower()

@pytest.mark.parametrize("space", [
    make_finite(3), _Tagged(tags=["real_line"]), _Tagged(),
])
def test_threshold_instances_aleph0(space):
    p = quantitative_profile(space)
    assert "aleph_0" in p["threshold_instances"]

@pytest.mark.parametrize("space", [
    make_finite(3), _Tagged(tags=["real_line"]), _Tagged(),
])
def test_pedagogical_positioning_present(space):
    p = quantitative_profile(space)
    assert len(p["pedagogical_positioning"]) > 30


# ---------------------------------------------------------------------------
# Key inequalities content
# ---------------------------------------------------------------------------
def test_ineq_density_weight():
    joined = " ".join(quantitative_profile(make_finite(3))["key_inequalities"]).lower()
    assert "d(x)" in joined or "density" in joined

def test_ineq_character_weight():
    joined = " ".join(quantitative_profile(make_finite(3))["key_inequalities"]).lower()
    assert "chi" in joined or "character" in joined

def test_ineq_weight():
    joined = " ".join(quantitative_profile(make_finite(3))["key_inequalities"]).lower()
    assert "w(x)" in joined or "weight" in joined

def test_ineq_lindelof():
    joined = " ".join(quantitative_profile(make_finite(3))["key_inequalities"]).lower()
    assert "lindelof" in joined or "l(x)" in joined

def test_ineq_arhangelskii():
    joined = " ".join(quantitative_profile(make_finite(3))["key_inequalities"]).lower()
    assert "arhangelskii" in joined or "arhangel" in joined or "2^{chi" in joined


# ---------------------------------------------------------------------------
# Key examples content
# ---------------------------------------------------------------------------
def test_examples_real_line():
    joined = " ".join(quantitative_profile(make_finite(3))["key_examples"]).lower()
    assert "r " in joined or "real" in joined

def test_examples_indiscrete():
    joined = " ".join(quantitative_profile(make_finite(3))["key_examples"]).lower()
    assert "indiscrete" in joined

def test_examples_sorgenfrey():
    joined = " ".join(quantitative_profile(make_finite(3))["key_examples"]).lower()
    assert "sorgenfrey" in joined

def test_examples_ordinal_space():
    joined = " ".join(quantitative_profile(make_finite(3))["key_examples"]).lower()
    assert "omega_1" in joined or "ordinal" in joined


# ---------------------------------------------------------------------------
# analyze_quantitative_topology -- Result shape
# ---------------------------------------------------------------------------
def test_analyze_finite_status():   assert analyze_quantitative_topology(make_finite(3)).status == "true"
def test_analyze_finite_mode():     assert analyze_quantitative_topology(make_finite(3)).mode == "exact"
def test_analyze_finite_version():  assert analyze_quantitative_topology(make_finite(3)).metadata["version"] == "0.1.68"
def test_analyze_finite_carrier():  assert analyze_quantitative_topology(make_finite(4)).metadata["carrier_size"] == 4

def test_analyze_finite_weight_meta():
    r = analyze_quantitative_topology(make_finite(3))
    assert "finite" in r.metadata["weight"].lower()

def test_analyze_real_mode():
    assert analyze_quantitative_topology(_Tagged(tags=["real_line"])).mode == "theorem"

def test_analyze_real_weight_meta():
    r = analyze_quantitative_topology(_Tagged(tags=["real_line"]))
    assert "aleph_0" in r.metadata["weight"]

def test_analyze_real_density_meta():
    r = analyze_quantitative_topology(_Tagged(tags=["real_line"]))
    assert "aleph_0" in r.metadata["density"]

def test_analyze_unknown_mode():
    assert analyze_quantitative_topology(_Tagged()).mode == "symbolic"

def test_analyze_value_is_dict():
    assert isinstance(analyze_quantitative_topology(make_finite(3)).value, dict)

def test_analyze_justification_nonempty():
    assert len(analyze_quantitative_topology(make_finite(3)).justification) >= 4

def test_analyze_justification_mentions_weight():
    joined = " ".join(analyze_quantitative_topology(make_finite(3)).justification).lower()
    assert "weight" in joined or "w(x)" in joined

def test_analyze_domain_rep():
    assert analyze_quantitative_topology(make_finite(3)).metadata["domain_representation"] == "finite"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def test_public_quantitative_profile():      assert hasattr(_pytop_pkg, "quantitative_profile")
def test_public_analyze():                   assert hasattr(_pytop_pkg, "analyze_quantitative_topology")
def test_public_error():                     assert hasattr(_pytop_pkg, "QuantitativeTopologyError")
def test_public_callable():                  assert callable(_pytop_pkg.quantitative_profile)
def test_public_finite_via_package():
    assert _pytop_pkg.quantitative_profile(make_finite(2))["representation"] == "finite"
def test_public_analyze_via_package():
    assert _pytop_pkg.analyze_quantitative_topology(make_finite(2)).status == "true"
def test_public_real_via_package():
    r = _pytop_pkg.analyze_quantitative_topology(_Tagged(tags=["real_line"]))
    assert "aleph_0" in r.metadata["weight"]
