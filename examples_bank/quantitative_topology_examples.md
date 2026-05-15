# Quantitative topology examples

Bu dosya, Cilt II Bölüm 24 için örnek ailesini toplar. Amaç, kardinal fonksiyonları tam teknik ayrıntısıyla vermek değil; nitel özelliklerden nicel sorulara geçişte hangi örneklerin kullanılacağını görünür kılmaktır.

## Çekirdek örnek ailesi

### 1. Sayılabilir ayrık uzay
- her noktada tekil açık komşuluk vardır;
- yerel veri küçüktür;
- buna karşılık yoğun altküme tüm uzayı kapsamak zorundadır.

**Pedagojik işlev:** küçük karakter ile büyük yoğunluk / büyük taban davranışının aynı uzayda mümkün olduğunu erkenden sezdirir.

### 2. İndiscrete uzay
- topolojiyi belirlemek için çok az veri gerekir;
- buna karşılık ayırma davranışı son derece zayıftır.

**Pedagojik işlev:** “nicel küçüklük” ile “iyi topolojik davranış”ın aynı şey olmadığını gösterir.

### 3. Reel doğru
- rasyonel uçlu aralıklarla sayılabilir taban taşır;
- rasyoneller üzerinden sayılabilir yoğun altküme taşır.

**Pedagojik işlev:** nicel küçüklüğün klasik olumlu modeli olarak kullanılır.

### 4. Sonlu topolojik uzaylar
- taban, karakter ve yoğunluk nicelikleri doğrudan sayılabilir;
- `pytop.invariants` ile hesaplamalı köprü kurulabilir.

**Pedagojik işlev:** soyut tanımların gerçekten hesaplanabilir olduğu sınıfı verir.

## Bölüm 24 için önerilen kullanım sırası

1. İndiscrete uzay ile “çok az veri” fikrini başlat.
2. Reel doğru ile “zengin topoloji ama küçük denetim verisi” olgusunu göster.
3. Sonsuz ayrık uzayla farklı niceliklerin farklı yönlere gidebildiğini vurgula.
4. Sonlu uzaylarla hesaplamalı destek ver.

## Standard spaces bağlantısı

Bu dosya tek başına okunmamalıdır. Özellikle `standard_spaces.md` ile birlikte kullanıldığında, Bölüm 24'te seçilen örneklerin Bölüm 25, 30 ve 31'de nasıl geri döndüğü daha açık görünür.

## v0.6.18 notebook bridge

Bu dosya artık doğrudan `notebooks/exploration/13_quantitative_topology.ipynb` ile birlikte okunmalıdır. Özellikle nitel özellik / nicel veri ayrımı ve sonlu uzay laboratuvarı burada notebook tarafına taşınmıştır.

## v0.1.68 — Nicel Topoloji Örnekleri

### QT-01: Sonlu uzayda nicel profil (exact mod)
```python
from pytop import analyze_quantitative_topology
from pytop.spaces import FiniteTopologicalSpace

X = FiniteTopologicalSpace(
    carrier={1, 2, 3},
    topology=[set(), {1}, {1, 2}, {1, 2, 3}]
)
result = analyze_quantitative_topology(X)
assert result.mode == "exact"
profile = result.value
assert profile["weight"] == "finite: 4"
assert profile["density"] == "finite: <= 3"
assert profile["character"] == "finite: <= 4"
assert profile["lindelof_number"] == "finite: Lindelof (trivially)"
```

### QT-02: Sorgenfrey doğrusu (theorem mod, etiket tabanlı)
```python
from pytop import analyze_quantitative_topology

class SorgenfreyLine:
    metadata = {"tags": ["lindelof", "separable", "first_countable",
                         "not_second_countable"]}
    representation = "symbolic_general"

result = analyze_quantitative_topology(SorgenfreyLine())
assert result.mode == "theorem"
profile = result.value
assert "uncountable" in profile["weight"]
assert "countable" in profile["density"]
assert "countable" in profile["character"]
assert "lindelof" in profile["lindelof_number"].lower()
```

### QT-03: İkinci sayılabilir uzay (theorem mod)
```python
from pytop import quantitative_profile

class SecondCountableSpace:
    metadata = {"tags": ["second_countable", "separable", "lindelof"]}
    representation = "symbolic_general"

profile = quantitative_profile(SecondCountableSpace())
assert "countable" in profile["weight"]
assert "countable" in profile["density"]
assert "countable" in profile["character"]
assert len(profile["key_inequalities"]) >= 6
```

### QT-04: Sembolik (bilinmeyen) uzay — symbolic mod
```python
from pytop import analyze_quantitative_topology

class UnknownSpace:
    pass

result = analyze_quantitative_topology(UnknownSpace())
assert result.mode == "symbolic"
profile = result.value
assert "symbolic" in profile["weight"]
assert "symbolic" in profile["density"]
assert "set_theoretic_bridge" in profile
```

### QT-05: Arhangel'skii eşitsizliği profil çıktısında
```python
from pytop import quantitative_profile
from pytop.spaces import FiniteTopologicalSpace

X = FiniteTopologicalSpace(carrier={0, 1}, topology=[set(), {0}, {0, 1}])
profile = quantitative_profile(X)
inequalities = profile["key_inequalities"]
arhangelskii = [i for i in inequalities if "Arhangelskii" in i or "2^{chi" in i]
assert len(arhangelskii) >= 1
```

### QT-06: Result metadata ve versiyon damgası
```python
from pytop import analyze_quantitative_topology
from pytop.spaces import FiniteTopologicalSpace

X = FiniteTopologicalSpace(carrier={1}, topology=[set(), {1}])
result = analyze_quantitative_topology(X)
assert result.metadata["version"] == "0.1.68"
assert "weight" in result.metadata
assert "density" in result.metadata
assert "character" in result.metadata
assert "lindelof_number" in result.metadata
assert result.metadata["carrier_size"] >= 1
```

---

## v0.1.69 — Temel Topolojik Değişmezler Örnekleri

### BI-01: Sonlu uzayda sekiz değişmez (exact mod)
```python
from pytop import analyze_topological_invariants
from pytop.finite_spaces import FiniteTopologicalSpace

X = FiniteTopologicalSpace(
    carrier={1, 2, 3},
    topology=[set(), {1}, {1, 2}, {1, 2, 3}]
)
result = analyze_topological_invariants(X)
assert result.mode == "exact"
p = result.value
assert "finite" in p["weight"]
assert "finite" in p["cellularity"]
assert "finite" in p["tightness"]
assert "finite" in p["network_weight"]
```

### BI-02: İkinci sayılabilir uzayda değişmezler (theorem mod)
```python
from pytop import topological_invariants_profile

class SecondCountable:
    metadata = {"tags": ["second_countable", "separable", "lindelof", "first_countable"]}
    representation = "symbolic_general"

p = topological_invariants_profile(SecondCountable())
assert "countable" in p["weight"]
assert "countable" in p["cellularity"]
assert "countable" in p["tightness"]
assert "countable" in p["network_weight"]
```

### BI-03: Sorgenfrey doğrusu değişmez profili
```python
from pytop import topological_invariants_profile

class SorgenfreyLine:
    metadata = {"tags": ["lindelof", "separable", "first_countable", "not_second_countable"]}
    representation = "symbolic_general"

p = topological_invariants_profile(SorgenfreyLine())
assert "uncountable" in p["weight"]
assert "countable" in p["density"]
assert "countable" in p["tightness"]
```

### BI-04: Sembolik uzay (symbolic mod)
```python
from pytop import analyze_topological_invariants

class UnknownSpace:
    pass

result = analyze_topological_invariants(UnknownSpace())
assert result.mode == "symbolic"
assert "symbolic" in result.value["weight"]
```

### BI-05: 10 anahtar eşitsizlik ve Arhangel'skii
```python
from pytop import topological_invariants_profile
from pytop.finite_spaces import FiniteTopologicalSpace

X = FiniteTopologicalSpace(carrier={0, 1}, topology=[set(), {0}, {0, 1}])
p = topological_invariants_profile(X)
assert len(p["key_inequalities"]) >= 8
assert any("Arhan" in i for i in p["key_inequalities"])
```

### BI-06: metadata versiyon damgası ve 8 alan kontrolü
```python
from pytop import analyze_topological_invariants
from pytop.finite_spaces import FiniteTopologicalSpace

X = FiniteTopologicalSpace(carrier={1}, topology=[set(), {1}])
result = analyze_topological_invariants(X)
assert result.metadata["version"] == "0.1.69"
for field in ["weight", "density", "character", "lindelof_number",
              "cellularity", "spread", "network_weight", "tightness"]:
    assert field in result.metadata
```

---

## v0.1.70 — Kardinal Fonksiyon Çerçevesi Örnekleri

### CF2-01: Tanım katmanı — 8 fonksiyon tanım kaydı
```python
from pytop import cardinal_function_definition

for fname in ["weight","density","character","lindelof_number",
              "cellularity","spread","network_weight","tightness"]:
    d = cardinal_function_definition(fname)
    assert "symbol" in d
    assert "key_threshold" in d
    assert "finite_case" in d
```

### CF2-02: Alias çözümleme (w, chi, nw, t, lindelof)
```python
from pytop import cardinal_function_definition
assert cardinal_function_definition("w")["symbol"] == "w(X)"
assert cardinal_function_definition("chi")["symbol"] == "chi(X)"
assert cardinal_function_definition("nw")["symbol"] == "nw(X)"
assert cardinal_function_definition("t")["symbol"] == "t(X)"
```

### CF2-03: Karşılaştırma katmanı — d(X) <= w(X)
```python
from pytop import cardinal_function_comparison
cmp = cardinal_function_comparison("weight", "density")
assert cmp["inequality"] == "d(X) <= w(X)"
assert "proof_idea" in cmp
assert "examples" in cmp and len(cmp["examples"]) >= 1
```

### CF2-04: Sonlu uzay tam çerçeve profili (exact mod)
```python
from pytop import analyze_cardinal_functions_framework
from pytop.finite_spaces import FiniteTopologicalSpace
X = FiniteTopologicalSpace(carrier={1,2,3}, topology=[set(), {1}, {1,2}, {1,2,3}])
result = analyze_cardinal_functions_framework(X)
assert result.mode == "exact"
assert len(result.value["definition_layer"]) == 8
assert len(result.value["comparison_layer"]) >= 7
assert len(result.value["framework_principles"]) >= 4
```

### CF2-05: Etiket tabanlı uzay (theorem mod)
```python
from pytop import analyze_cardinal_functions_framework
class SC:
    metadata = {"tags": ["second_countable", "separable", "lindelof"]}
    representation = "symbolic_general"
result = analyze_cardinal_functions_framework(SC())
assert result.mode == "theorem"
assert "second_countable" in result.value["space_tags"]
```

### CF2-06: metadata versiyon damgası v0.1.70
```python
from pytop import analyze_cardinal_functions_framework
from pytop.finite_spaces import FiniteTopologicalSpace
X = FiniteTopologicalSpace(carrier={1}, topology=[set(), {1}])
result = analyze_cardinal_functions_framework(X)
assert result.metadata["version"] == "0.1.70"
assert result.metadata["functions_defined"] == 8
assert result.metadata["comparisons_recorded"] >= 7
```
