# %% [markdown]
"""
# Bölüm 12 — Bölüm Topolojisi (Quotient Topology)

Bölüm topolojisi, bir topolojik uzayın noktalarını denklik sınıflarına göre
"yapıştırarak" yeni bir uzay kurar.
Alt uzay ve çarpım topolojisiyle birlikte temel üç inşaat yönteminden birini oluşturur.
"""

# %% [markdown]
"""
## 1. Konu

### Denklik Bağıntısı ve Bölüm Kümesi

X kümesi ve X üzerinde bir denklik bağıntısı ~ verilsin.
Her x için denklik sınıfı [x] = {y ∈ X : y ~ x} şeklindedir.
Bölüm kümesi X/~ = {[x] : x ∈ X}.

### Bölüm Topolojisi

(X, τ) topolojik uzayı ve ~ denklik bağıntısı verilsin.
Bölüm haritası q: X → X/~ tanımı: q(x) = [x].

Bölüm topolojisi τ_{X/~} üzerinde:
    U ⊆ X/~ açıktır  ⟺  q⁻¹(U) ∈ τ

Bu, q'yu sürekli kılan en ince (en fazla açık küme içeren) topolojidir.

### Temel Özellikler

| Özellik            | Bölüm uzayı için durum                      |
|--------------------|----------------------------------------------|
| Kompaktlık         | X kompakt ⟹ X/~ kompakt                   |
| Bağlantılılık      | X bağlantılı ⟹ X/~ bağlantılı            |
| Hausdorff          | Genel olarak korunmaz                        |
| T1                 | ~ kapalı bağıntı ise korunur                |
"""

# %%
from pytop import (
    quotient_set,
    finite_quotient_contract,
    finite_quotient_summary,
    make_quotient_map,
    is_quotient_map,
    discrete_topology,
    indiscrete_topology,
    sierpinski_space,
    make_topology,
    is_compact,
    is_connected,
    is_t2,
    is_t0,
)

# %% [markdown]
"""
> **Neden bu konu?** Eşdeğerlik bağıntısından yeni uzay üretmek; daire S¹ ve torus bu şekilde inşa edilir.

> 🔍 **Kendin dene:** `quotient_set` ile `equivalence_class` çıktılarını karşılaştırın: hangisi hangi bilgiyi taşır?

> ⚠️ **Sık hata:** `quotient_set` denklik bağıntısı gerektirir; rastgele bağıntı `RelationError` fırlatır.

> ↗️ **Bkz.:** Bölüm 3 (`partition_from_equivalence`), Bölüm 11 (bölüm topolojisi inşası).

> 💭 **Öz-yansıtma:** S¹ = [0,1] / {0~1} yapısını küçük bir taşıyıcı üzerinde modelleyebilir misiniz?
"""

# %% [markdown]
"""
## 2. Teoremler
"""

# %% [markdown]
"""
**Teorem 2.1 (Bölüm haritası sürekliliği).**
q: X → X/~ her zaman süreklidir.

**Teorem 2.2 (Evrensel özellik).**
g: X/~ → Z olsun. g süreklidir ⟺ g ∘ q: X → Z süreklidir.

**Teorem 2.3 (Kompaktlık korunumu).**
X kompakt ⟹ X/~ kompakttır.

**Teorem 2.4 (Bağlantılılık korunumu).**
X bağlantılı ⟹ X/~ bağlantılıdır.

**Teorem 2.5.**
X/~ Hausdorff ⟺ ~ grafiği (denklik sınıflarının grafiği) X × X'te kapalıdır.
"""

# %% [markdown]
"""
## 3. Algoritmalar

### quotient_set — O(|X|² · α(|X|))

```
QuotientSet(X, ~):
    Initialize: her x için {x} sınıfı
    For each (x, y) in ~:
        Union(x, y)           # union-find
    Return sınıfları tuple olarak
```

Sonuç: X/~'nin elemanları olan dondurulmuş kümeler (frozenset) demeti.

### finite_quotient_contract — O(|X| + |bloklar|)

```
FiniteQuotientContract(X, P):
    // P = X'in bir bölüntüsü (her x tam bir blokta)
    Validate(P covers X, blocks are disjoint)
    Return FiniteConstructionContract(
        status='true', carrier_size=|X|, block_count=|P|
    )
```
"""

# %% [markdown]
"""
## 4. pytop API

```python
from pytop import (
    quotient_set,               # denklik bağıntısından bölüm kümesi
    finite_quotient_contract,   # bölüntüden inşaat sözleşmesi
    finite_quotient_summary,    # kısa özet dizesi
    make_quotient_map,          # QuotientMap nesnesi
    is_quotient_map,            # Result: harita bölüm haritası mı?
)
```

`quotient_set(carrier, relation)` → `tuple[frozenset, ...]`
- `relation`: tam denklik bağıntısı (yansımalı + simetrik + geçişli çiftler)

`finite_quotient_contract(carrier, partition)` → `FiniteConstructionContract`
- `partition`: örtüşmeyen liste-listesi; `.status`, `.block_count`, `.carrier_size`, `.to_result()`

`finite_quotient_summary(carrier, partition)` → `str`

`make_quotient_map(domain, codomain)` → `QuotientMap`

`is_quotient_map(map_obj)` → `Result`
"""

# %% [markdown]
"""
## 5. Örnekler
"""

# %% [markdown]
"""
### Örnek 5.1 — İki Noktayı Özdeşleştirme
"""

# %%
d4 = discrete_topology(0, 1, 2, 3)

# partition: {0,1} tek blok, 2 ve 3 ayrı
partition_1 = [[0, 1], [2], [3]]
qs1 = quotient_set(
    [0, 1, 2, 3],
    [(0,0),(1,1),(2,2),(3,3),(0,1),(1,0)]
)
print("Bölüm kümesi:", qs1)
contract1 = finite_quotient_contract([0, 1, 2, 3], partition_1)
print("Blok sayısı:", contract1.block_count)
print("Durum:", contract1.status)

# %% [markdown]
"""
```text
Bölüm kümesi: (frozenset({2}), frozenset({3}), frozenset({0, 1}))
Blok sayısı: 3
Durum: true
```

4 noktalı ayrık uzayda 0 ve 1 özdeşleştirildi; bölüm uzayı 3 elemanlıdır.
"""

# %% [markdown]
"""
### Örnek 5.2 — Tüm Noktaları Tek Noktaya Çökertme
"""

# %%
carrier = [0, 1, 2, 3]
# Hepsi aynı denklik sınıfında
qs2 = quotient_set(
    carrier,
    [(i, j) for i in carrier for j in carrier]   # tam çarpım = tüm çiftler
)
print("Tek blok:", qs2)

contract2 = finite_quotient_contract(carrier, [carrier])
print("Blok sayısı:", contract2.block_count)
r2 = contract2.to_result()
print("Metadata blok boyutları:", r2.metadata['block_sizes'])

# %% [markdown]
"""
```text
Tek blok: (frozenset({0, 1, 2, 3}),)
Blok sayısı: 1
Metadata blok boyutları: [4]
```

Tüm noktalar tek sınıfta toplandığında bölüm uzayı tek noktalıdır (terminale indirgenir).
"""

# %% [markdown]
"""
### Örnek 5.3 — Sierpiński Uzayında Bölüm
"""

# %%
s = sierpinski_space()
print("Sierpinski carrier:", sorted(s.carrier))
print("Sierpinski topology:", sorted([sorted(list(u)) for u in s.topology],
                                     key=lambda x: (len(x), x)))

# İki noktayı özdeşleştir -> tek noktalı uzay
summary_s = finite_quotient_summary(list(s.carrier), [[0, 1]])
print("Sierpinski / {{0,1}}:", summary_s)

# %% [markdown]
"""
```text
Sierpinski carrier: [0, 1]
Sierpinski topology: [[], [1], [0, 1]]
Sierpinski / {0,1}: quotient: status=true, carrier=2, blocks=1
```

Sierpiński uzayında her iki nokta özdeşleştirildiğinde bir blok kalır.
"""

# %% [markdown]
"""
### Örnek 5.4 — Özel Topolojide Bölüm Sözleşmesi
"""

# %%
X5 = [1, 2, 3, 4, 5]
tau5 = [set(), {1,2}, {3,4}, {1,2,3,4}, {1,2,3,4,5}]
fts5 = make_topology(X5, *tau5)
print("Uzay:", sorted([sorted(list(u)) for u in fts5.topology],
                      key=lambda x: (len(x), x)))

# {1,2} tek blok, {3,4} tek blok, {5} kendi başına
partition5 = [[1, 2], [3, 4], [5]]
contract5 = finite_quotient_contract(X5, partition5)
r5 = contract5.to_result()
print("Status:", r5.status)
print("Bloklar:", r5.metadata['block_count'])
print("Blok boyutları:", r5.metadata['block_sizes'])

# %% [markdown]
"""
```text
Uzay: [[], [1, 2], [3, 4], [1, 2, 3, 4], [1, 2, 3, 4, 5]]
Status: true
Bloklar: 3
Blok boyutları: [2, 2, 1]
```

5 → 3 noktalı bölüm. τ'daki açık kümelerin tam olarak bloklar üzerinden tanımlı olması
bu bölüntünün uzayın "doğal" bölümtüsü olduğunu gösterir.
"""

# %% [markdown]
"""
### Örnek 5.5 — Bölüm Haritası Nesnesi
"""

# %%
d3 = discrete_topology(0, 1, 2)
d2 = discrete_topology('a', 'b')

qmap = make_quotient_map(d3, d2)
print("QuotientMap türü:", type(qmap).__name__)
print("Etiketler:", sorted(qmap.tags))

r_qmap = is_quotient_map(qmap)
print("is_quotient_map status:", r_qmap.status)
print("Justification:", r_qmap.justification[0])

# %% [markdown]
"""
```text
QuotientMap türü: QuotientMap
Etiketler: ['continuous', 'quotient', 'surjective']
is_quotient_map status: true
Justification: Map tag 'quotient' is explicitly present.
```

`make_quotient_map` bir QuotientMap nesnesi üretir; `is_quotient_map` bu nesne üzerinde
`Result` döner.
"""

# %% [markdown]
"""
### Örnek 5.6 — Bölüm Özetleri Karşılaştırması
"""

# %%
carrier6 = list(range(6))   # [0, 1, 2, 3, 4, 5]

configs = [
    ("6->6 (trivial)", [[x] for x in carrier6]),
    ("6->3 (çiftler)", [[0,1],[2,3],[4,5]]),
    ("6->2 (üçlüler)", [[0,1,2],[3,4,5]]),
    ("6->1 (tek nokta)",  [carrier6]),
]
for label, part in configs:
    s = finite_quotient_summary(carrier6, part)
    print(f"{label:20s}: {s}")

# %% [markdown]
"""
```text
6->6 (trivial)      : quotient: status=true, carrier=6, blocks=6
6->3 (çiftler)      : quotient: status=true, carrier=6, blocks=3
6->2 (üçlüler)      : quotient: status=true, carrier=6, blocks=2
6->1 (tek nokta)    : quotient: status=true, carrier=6, blocks=1
```

Aynı taşıyıcı üzerinde farklı bölüntüler farklı boyutlarda bölüm uzayları üretir.
"""

# %% [markdown]
"""
## 6. Alıştırmalar

### Kodlama

K1. `discrete_topology(0, 1, 2, 3, 4)` üzerinde `[[0,4],[1,3],[2]]` bölüntüsünü
    kullanarak `finite_quotient_contract` çağırın; blok sayısını ve boyutlarını yazdırın.

K2. `sierpinski_space()` üzerinde her noktanın kendi sınıfı olduğu (trivial) bölüntü ile
    `finite_quotient_summary` çağırın; çıktıyı yorumlayın.

K3. `make_topology([1,2,3,4], set(), {1,2}, {3,4}, {1,2,3,4})` üzerinde
    `[[1,2],[3,4]]` ve `[[1],[2],[3],[4]]` bölüntülerini karşılaştırın.

### Teori

T1. q: X → X/~ bölüm haritasının τ_{X/~} tanımı gereği her zaman sürekli olduğunu
    ispatlayın.

T2. X bağlantılı ise X/~ bağlantılıdır; q sürekli ve X = q⁻¹(X/~) bağlantılı olduğundan
    q(X) = X/~ bağlantılı olmalıdır. Bu argümanı formalize edin.
"""

# %%
if __name__ == "__main__":
    pass
