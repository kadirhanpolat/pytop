"""test_cilt4_basic_invariants_v069.py

v0.1.69 — Cilt IV temel topolojik değişmezler koridoru
Bağımsız doğrulama: python3 -c "exec(open(...).read())"
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from pytop import (
    BasicInvariantError,
    topological_invariants_profile,
    analyze_topological_invariants,
)
from pytop.finite_spaces import FiniteTopologicalSpace


# ─── Test 1: Sonlu uzay — exact mod ───────────────────────────────────
X = FiniteTopologicalSpace(
    carrier={1, 2, 3},
    topology=[set(), {1}, {1, 2}, {1, 2, 3}]
)
result = analyze_topological_invariants(X)
assert result.mode == "exact", f"Expected exact, got {result.mode}"
p = result.value
assert "finite" in p["weight"]
assert "finite" in p["density"]
assert "finite" in p["character"]
assert "finite" in p["lindelof_number"]
assert "finite" in p["cellularity"]
assert "finite" in p["spread"]
assert "finite" in p["network_weight"]
assert "finite" in p["tightness"]
print("✓ Test 1: sonlu uzay exact mod OK")


# ─── Test 2: İkinci sayılabilir uzay — theorem mod ────────────────────
class SecondCountableSpace:
    metadata = {"tags": ["second_countable", "separable", "lindelof", "first_countable"]}
    representation = "symbolic_general"

result2 = analyze_topological_invariants(SecondCountableSpace())
assert result2.mode == "theorem", f"Expected theorem, got {result2.mode}"
p2 = result2.value
assert "countable" in p2["weight"]
assert "countable" in p2["density"]
assert "countable" in p2["character"]
assert "lindelof" in p2["lindelof_number"].lower() or "countable" in p2["lindelof_number"]
assert "countable" in p2["cellularity"]
print("✓ Test 2: ikinci sayılabilir uzay theorem mod OK")


# ─── Test 3: Sorgenfrey doğrusu — theorem mod ─────────────────────────
class SorgenfreyLine:
    metadata = {"tags": ["lindelof", "separable", "first_countable", "not_second_countable"]}
    representation = "symbolic_general"

result3 = analyze_topological_invariants(SorgenfreyLine())
assert result3.mode == "theorem"
p3 = result3.value
assert "uncountable" in p3["weight"]
assert "countable" in p3["density"]
assert "countable" in p3["character"]
assert "lindelof" in p3["lindelof_number"].lower() or "countable" in p3["lindelof_number"]
print("✓ Test 3: Sorgenfrey doğrusu theorem mod OK")


# ─── Test 4: Sembolik uzay — symbolic mod ─────────────────────────────
class UnknownSpace:
    pass

result4 = analyze_topological_invariants(UnknownSpace())
assert result4.mode == "symbolic", f"Expected symbolic, got {result4.mode}"
p4 = result4.value
assert "symbolic" in p4["weight"]
assert "symbolic" in p4["density"]
print("✓ Test 4: sembolik uzay symbolic mod OK")


# ─── Test 5: key_inequalities — 10 eşitsizlik ─────────────────────────
X2 = FiniteTopologicalSpace(carrier={0, 1}, topology=[set(), {0}, {0, 1}])
p5 = topological_invariants_profile(X2)
assert len(p5["key_inequalities"]) >= 8
arh = [i for i in p5["key_inequalities"] if "Arhan" in i or "chi" in i.lower()]
assert len(arh) >= 1, "Arhangel'skii eşitsizliği bulunamadı"
print(f"✓ Test 5: key_inequalities ({len(p5['key_inequalities'])} adet), Arhangel'skii mevcut")


# ─── Test 6: 8 değişmez tamamı profilde mevcut ────────────────────────
expected_keys = [
    "weight", "density", "character", "lindelof_number",
    "cellularity", "spread", "network_weight", "tightness",
    "key_inequalities", "key_examples",
    "quantitative_bridge", "cardinal_function_bridge", "representation"
]
for k in expected_keys:
    assert k in p5, f"Profilde eksik anahtar: {k}"
print(f"✓ Test 6: tüm {len(expected_keys)} profil anahtarı mevcut")


# ─── Test 7: metadata versiyon damgası ────────────────────────────────
X3 = FiniteTopologicalSpace(carrier={1}, topology=[set(), {1}])
result7 = analyze_topological_invariants(X3)
assert result7.metadata["version"] == "0.1.69"
assert result7.metadata["carrier_size"] == 1
for field in ["weight", "density", "character", "lindelof_number",
              "cellularity", "spread", "network_weight", "tightness"]:
    assert field in result7.metadata, f"metadata'da eksik: {field}"
print("✓ Test 7: metadata versiyon damgası ve alan kontrolü OK")


# ─── Test 8: metrizable + separable => second countable zincirleme ────
class SepMetrizable:
    metadata = {"tags": ["metrizable", "separable"]}
    representation = "symbolic_general"

p8 = topological_invariants_profile(SepMetrizable())
assert "countable" in p8["weight"], f"Got: {p8['weight']}"
assert "countable" in p8["character"], f"Got: {p8['character']}"
print("✓ Test 8: metrizable+separable => w=chi=aleph_0 zincirleme OK")


print()
print("ALL v0.1.69 CHECKS PASSED")
