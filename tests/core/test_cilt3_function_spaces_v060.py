"""
test_cilt3_function_spaces_v060.py
====================================
Test suite for v0.1.60 — compare_function_space_topologies
"""
import importlib.util
import os
import sys
from itertools import combinations

_BASE = os.path.join(os.path.dirname(__file__), "..", "..", "src", "pytop")
def _load(name, rel):
    path = os.path.normpath(os.path.join(_BASE, rel))
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    mod.__package__ = "pytop"; sys.modules[name] = mod
    spec.loader.exec_module(mod); return mod

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))

_fs_mod = _load("pytop.function_spaces", "function_spaces.py")
FiniteTopologicalSpace          = sys.modules["pytop.finite_spaces"].FiniteTopologicalSpace
compare_function_space_topologies = _fs_mod.compare_function_space_topologies

def make_finite(n):
    c = list(range(n))
    t = [frozenset(s) for r in range(n+1) for s in combinations(c,r)]
    return FiniteTopologicalSpace(carrier=frozenset(c), topology=frozenset(t))

class _Tagged:
    def __init__(self, tags=(), representation="symbolic_general"):
        self.metadata = {"tags": list(tags)}; self.representation = representation

class _CompactTagged(_Tagged):
    def __init__(self): super().__init__(tags=["compact","hausdorff"])
class _LocallyCompactTagged(_Tagged):
    def __init__(self): super().__init__(tags=["locally_compact","locally_compact_hausdorff"])


# ---- required keys ----
def test_required_keys():
    r = compare_function_space_topologies(make_finite(3))
    for k in ["fineness_order","coincidence_conditions","comparison_table","counterexamples","summary","representation"]:
        assert k in r

def test_comparison_table_has_three_rows():
    r = compare_function_space_topologies(make_finite(3))
    assert len(r["comparison_table"]) == 3

def test_comparison_table_row_keys():
    r = compare_function_space_topologies(make_finite(3))
    for row in r["comparison_table"]:
        for k in ["topology_1","topology_2","finer","equal_when","example_where_differ"]:
            assert k in row

# ---- finite space ----
def test_finite_all_coincide_in_fineness():
    r = compare_function_space_topologies(make_finite(3))
    assert "pt = co = u" in r["fineness_order"] or "all three coincide" in r["fineness_order"]

def test_finite_representation():
    r = compare_function_space_topologies(make_finite(2))
    assert r["representation"] == "finite"

def test_finite_summary_mentions_n():
    r = compare_function_space_topologies(make_finite(4))
    assert "4" in r["summary"]

def test_finite_no_counterexamples():
    r = compare_function_space_topologies(make_finite(3))
    assert "No counterexamples" in r["counterexamples"][0]

def test_finite_coincidence_pt_eq_u():
    r = compare_function_space_topologies(make_finite(3))
    cc = r["coincidence_conditions"]
    assert cc.get("pt_eq_u","").startswith("yes") or cc.get("all_three","").startswith("yes")

def test_finite_n1_edge_case():
    r = compare_function_space_topologies(make_finite(1))
    assert "1" in r["summary"] or "finite" in r["fineness_order"].lower()

# ---- compact ----
def test_compact_fineness_mentions_compact():
    r = compare_function_space_topologies(_CompactTagged())
    assert "compact" in r["fineness_order"].lower()

def test_compact_co_eq_u_coincidence():
    r = compare_function_space_topologies(_CompactTagged())
    cc = r["coincidence_conditions"]
    assert cc.get("co_eq_u","").startswith("yes") or "compact" in cc.get("co_eq_u","").lower()

def test_compact_summary_uniform():
    r = compare_function_space_topologies(_CompactTagged())
    assert "uniform" in r["summary"].lower()

def test_compact_representation_symbolic():
    r = compare_function_space_topologies(_CompactTagged())
    assert r["representation"] == "symbolic_general"

# ---- locally compact ----
def test_lc_strict_chain():
    r = compare_function_space_topologies(_LocallyCompactTagged())
    assert "pt ≤ co ≤ u" in r["fineness_order"]

def test_lc_summary_exponential_or_homotopy():
    r = compare_function_space_topologies(_LocallyCompactTagged())
    assert "exponential" in r["summary"].lower() or "homotopy" in r["summary"].lower()

# ---- generic ----
def test_generic_fineness_order():
    r = compare_function_space_topologies(_Tagged())
    assert "pt ≤ co ≤ u" in r["fineness_order"]

def test_generic_counterexamples_multiple():
    r = compare_function_space_topologies(_Tagged())
    assert len(r["counterexamples"]) > 1

def test_generic_counterexample_mentions_real_line():
    r = compare_function_space_topologies(_Tagged())
    combined = " ".join(r["counterexamples"])
    assert "ℝ" in combined or "R" in combined

def test_generic_summary_compact_open():
    r = compare_function_space_topologies(_Tagged())
    assert "compact-open" in r["summary"].lower() or "exponential" in r["summary"].lower()

def test_generic_coincidence_pt_co_not_always():
    r = compare_function_space_topologies(_Tagged())
    cc = r["coincidence_conditions"]
    assert "compact" in cc.get("pt_eq_co","").lower()

def test_generic_coincidence_co_u_not_always():
    r = compare_function_space_topologies(_Tagged())
    cc = r["coincidence_conditions"]
    assert "compact" in cc.get("co_eq_u","").lower()

# ---- table finer relation ----
def test_table_pt_le_co_row():
    r = compare_function_space_topologies(_Tagged())
    pt_co = next((row for row in r["comparison_table"] if "pointwise" in row["topology_1"] and "compact-open" in row["topology_2"]), None)
    assert pt_co is not None
    assert "pt ≤ co" in pt_co["finer"]

def test_table_co_le_u_row():
    r = compare_function_space_topologies(_Tagged())
    co_u = next((row for row in r["comparison_table"] if "compact-open" in row["topology_1"] and "uniform" in row["topology_2"]), None)
    assert co_u is not None
    assert "co ≤ u" in co_u["finer"]

def test_table_pt_le_u_row():
    r = compare_function_space_topologies(_Tagged())
    pt_u = next((row for row in r["comparison_table"] if "pointwise" in row["topology_1"] and "uniform" in row["topology_2"]), None)
    assert pt_u is not None
    assert "pt ≤ u" in pt_u["finer"]
