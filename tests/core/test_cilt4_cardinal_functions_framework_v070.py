"""test_cilt4_cardinal_functions_framework_v070.py

v0.1.70 — Cilt IV kardinal fonksiyon çerçevesi (3 katman: tanım/karşılaştırma/örnek)
Bağımsız doğrulama: python3 tests/core/test_cilt4_cardinal_functions_framework_v070.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from pytop import (
    CardinalFunctionFrameworkError,
    cardinal_function_definition,
    cardinal_function_comparison,
    cardinal_functions_framework_profile,
    analyze_cardinal_functions_framework,
)
from pytop.finite_spaces import FiniteTopologicalSpace


# ─── Test 1: TANIM katmanı — 8 fonksiyon ──────────────────────────────
for fname in ["weight", "density", "character", "lindelof_number",
              "cellularity", "spread", "network_weight", "tightness"]:
    d = cardinal_function_definition(fname)
    assert "symbol" in d, f"symbol missing for {fname}"
    assert "definition" in d
    assert "key_threshold" in d
    assert "computation" in d
    assert "finite_case" in d
print("✓ Test 1: 8 fonksiyon tanım katmanı OK")


# ─── Test 2: TANIM katmanı — alias çözümleme ──────────────────────────
assert cardinal_function_definition("w")["symbol"] == "w(X)"
assert cardinal_function_definition("chi")["symbol"] == "chi(X)"
assert cardinal_function_definition("nw")["symbol"] == "nw(X)"
assert cardinal_function_definition("t")["symbol"] == "t(X)"
assert cardinal_function_definition("lindelof")["symbol"] == "L(X)"
print("✓ Test 2: alias çözümleme OK")


# ─── Test 3: TANIM katmanı — hata fırlatma ────────────────────────────
try:
    cardinal_function_definition("unknown_invariant")
    assert False, "Should have raised"
except CardinalFunctionFrameworkError:
    pass
print("✓ Test 3: CardinalFunctionFrameworkError fırlatma OK")


# ─── Test 4: KARŞILAŞTIRMA katmanı — 7 çift ──────────────────────────
pairs = [
    ("weight", "density"),
    ("weight", "character"),
    ("weight", "network_weight"),
    ("density", "cellularity"),
    ("density", "spread"),
    ("character", "tightness"),
    ("character", "lindelof_number"),
]
for n1, n2 in pairs:
    cmp = cardinal_function_comparison(n1, n2)
    assert "inequality" in cmp
    assert "proof_idea" in cmp
    assert "equality_condition" in cmp
    assert "examples" in cmp
    assert len(cmp["examples"]) >= 1
print(f"✓ Test 4: {len(pairs)} karşılaştırma kaydı OK")


# ─── Test 5: Sonlu uzay — exact mod ───────────────────────────────────
X = FiniteTopologicalSpace(
    carrier={1, 2, 3},
    topology=[set(), {1}, {1, 2}, {1, 2, 3}]
)
result = analyze_cardinal_functions_framework(X)
assert result.mode == "exact", f"Expected exact, got {result.mode}"
p = result.value
assert "definition_layer" in p
assert "comparison_layer" in p
assert "example_layer" in p
assert "framework_principles" in p
assert len(p["definition_layer"]) == 8
assert len(p["comparison_layer"]) >= 7
assert len(p["example_layer"]) >= 8
assert len(p["framework_principles"]) >= 4
print("✓ Test 5: sonlu uzay exact mod, 4 katman OK")


# ─── Test 6: Etiket tabanlı uzay — theorem mod ────────────────────────
class SecondCountable:
    metadata = {"tags": ["second_countable", "separable", "lindelof"]}
    representation = "symbolic_general"

result6 = analyze_cardinal_functions_framework(SecondCountable())
assert result6.mode == "theorem"
p6 = result6.value
assert p6["space_tags"] == ["lindelof", "second_countable", "separable"]
print("✓ Test 6: theorem mod, space_tags OK")


# ─── Test 7: Sembolik uzay — symbolic mod ─────────────────────────────
class Unknown: pass
result7 = analyze_cardinal_functions_framework(Unknown())
assert result7.mode == "symbolic"
print("✓ Test 7: symbolic mod OK")


# ─── Test 8: metadata versiyon damgası ────────────────────────────────
assert result.metadata["version"] == "0.1.70"
assert result.metadata["functions_defined"] == 8
assert result.metadata["comparisons_recorded"] >= 7
assert result.metadata["examples_count"] >= 8
print("✓ Test 8: metadata versiyon damgası v0.1.70 OK")


# ─── Test 9: profil framework_principles içeriği ──────────────────────
X2 = FiniteTopologicalSpace(carrier={0, 1}, topology=[set(), {0}, {0, 1}])
p9 = cardinal_functions_framework_profile(X2)
principles = p9["framework_principles"]
has_tanim = any("TANIM" in pr for pr in principles)
has_karsilastirma = any("KARŞILAŞTIRMA" in pr for pr in principles)
has_esik = any("EŞİK" in pr for pr in principles)
assert has_tanim and has_karsilastirma and has_esik
print("✓ Test 9: framework_principles TANIM/KARŞILAŞTIRMA/EŞİK ilkeleri OK")


# ─── Test 10: cross-version tüm modüller hâlâ çalışıyor ──────────────
from pytop import (
    analyze_cardinal_numbers, analyze_ordinal_numbers,
    analyze_cofinality, analyze_quantitative_topology,
    analyze_topological_invariants,
)
print("✓ Test 10: v0.1.65–v0.1.70 cross-version imports OK")


print()
print("ALL v0.1.70 CHECKS PASSED")
