# %% [markdown]
"""
# Bölüm 0 — Küme Teorisi ve Fonksiyon Temelleri

pytop'un tüm modülleri küme teorisi ve fonksiyon kavramları üzerine kuruludur.
Bu bölüm, kılavuzun geri kalanında varsayılan ön koşulları pytop API'siyle
birlikte pekiştirir.
"""

# %% [markdown]
"""
## 1. Konu

### Küme ve Altküme

Küme: birbirinden ayrı nesnelerin koleksiyonu. Gösterim: A = {1, 2, 3}.
Altküme: A ⊆ B ⟺ her a ∈ A için a ∈ B.
Güç kümesi: P(A) = {S : S ⊆ A}. |P(A)| = 2^|A|.

### Küme İşlemleri

| İşlem | Gösterim | Tanım |
|-------|----------|-------|
| Birleşim | A ∪ B | a ∈ A veya a ∈ B |
| Kesişim | A ∩ B | a ∈ A ve a ∈ B |
| Fark | A \\ B | a ∈ A ve a ∉ B |
| Tümleyen | A^c | a ∉ A (evren X'te) |

### Bağıntılar

Kartezyen çarpım: A × B = {(a, b) : a ∈ A, b ∈ B}.
A üzerinde bir bağıntı R ⊆ A × A.

Bağıntı türleri:
- **Yansımalı:** ∀a, (a,a) ∈ R
- **Simetrik:** (a,b) ∈ R ⟹ (b,a) ∈ R
- **Geçişli:** (a,b),(b,c) ∈ R ⟹ (a,c) ∈ R
- **Denklik bağıntısı:** Yansımalı + Simetrik + Geçişli

### Fonksiyonlar

f: A → B bir fonksiyon: her a ∈ A için tek bir f(a) ∈ B.

| Tür | Koşul |
|-----|-------|
| Enjeksiyon (birebir) | f(a₁) = f(a₂) ⟹ a₁ = a₂ |
| Sürjeksiyon (örten) | ∀b ∈ B, ∃a ∈ A: f(a) = b |
| Bijeksiyon | Enjeksiyon + Sürjeksiyon |
"""

# %%
from pytop import (
    make_set, power_set,
    set_union, set_intersection, set_difference,
    is_subset, is_proper_subset, equal_sets,
    make_relation, is_equivalence_relation,
    identity_relation, inverse_relation, relation_profile,
    normalize_finite_map_data,
    is_injective_finite_map, is_surjective_finite_map, is_bijective_finite_map,
    image_of_subset_finite, preimage_of_subset_finite,
)

# %% [markdown]
"""
## 2. Teoremler
"""

# %% [markdown]
"""
**Teorem 2.1 (De Morgan).**
(A ∪ B)^c = A^c ∩ B^c    ve    (A ∩ B)^c = A^c ∪ B^c.

**Teorem 2.2 (Güç Kümesi Boyutu).**
|A| = n ⟹ |P(A)| = 2ⁿ.

**Teorem 2.3 (Denklik Sınıfları Bölüntü Oluşturur).**
~ denklik bağıntısı ise {[a] : a ∈ A} A'nın bir bölüntüsüdür;
yani sınıflar örtüşmez ve birleşimleri A'dır.

**Teorem 2.4 (Ön-Görüntü Özellikleri).**
f: A → B ve S ⊆ B için:
- f⁻¹(B \\ S) = A \\ f⁻¹(S)
- f⁻¹(S₁ ∪ S₂) = f⁻¹(S₁) ∪ f⁻¹(S₂)
- f⁻¹(S₁ ∩ S₂) = f⁻¹(S₁) ∩ f⁻¹(S₂)
"""

# %% [markdown]
"""
## 3. Algoritmalar

### Güç Kümesi — O(2^|A|)

```
PowerSet(A):
    result <- {∅}
    for each a in A:
        result <- result ∪ {S ∪ {a} : S ∈ result}
    return result
```

### Denklik Bağıntısı Doğrulama — O(|R|·|A|)

```
IsEquivalence(A, R):
    for each a in A:
        if (a, a) not in R: return False   // yansımalı
    for each (a, b) in R:
        if (b, a) not in R: return False   // simetrik
    for each (a, b) in R:
        for each (b, c) in R:
            if (a, c) not in R: return False  // geçişli
    return True
```
"""

# %% [markdown]
"""
## 4. pytop API

```python
from pytop import (
    make_set, power_set,
    set_union, set_intersection, set_difference,
    is_subset, is_proper_subset, equal_sets,
    make_relation, is_equivalence_relation,
    identity_relation, inverse_relation, relation_profile,
    normalize_finite_map_data,
    is_injective_finite_map, is_surjective_finite_map, is_bijective_finite_map,
    image_of_subset_finite, preimage_of_subset_finite,
)
```

`make_set(*elements)` → `frozenset`

`power_set(values)` → `set[frozenset]`

`make_relation(carrier, *pairs)` → `set[tuple]`

`relation_profile(carrier, relation)` → `dict` (is_reflexive, is_symmetric, is_transitive, ...)

`normalize_finite_map_data(domain, codomain, mapping)` → `FiniteMapData`
"""

# %% [markdown]
"""
## 5. Örnekler
"""

# %% [markdown]
"""
### Örnek 5.1 — Küme İşlemleri
"""

# %%
A = make_set(1, 2, 3)
B = make_set(2, 3, 4)

print("A:", sorted(A))
print("B:", sorted(B))
print("A union B:", sorted(set_union(A, B)))
print("A inter B:", sorted(set_intersection(A, B)))
print("A diff B:", sorted(set_difference(A, B)))
print("{2,3} subset A:", is_subset({2, 3}, A))
print("{1,4} subset A:", is_subset({1, 4}, A))
print("A = B:", equal_sets(A, B))

# %% [markdown]
"""
```text
A: [1, 2, 3]
B: [2, 3, 4]
A ∪ B: [1, 2, 3, 4]
A ∩ B: [2, 3]
A \\ B: [1]
{2,3} ⊆ A: True
{1,4} ⊆ A: False
A = B: False
```
"""

# %% [markdown]
"""
### Örnek 5.2 — Güç Kümesi
"""

# %%
P = power_set([1, 2, 3])
print("P({1,2,3}) boyutu:", len(P))
print("Elemanlar:")
for s in sorted([sorted(list(x)) for x in P], key=lambda x: (len(x), x)):
    print(" ", s if s else "empty")

# %% [markdown]
"""
```text
P({1,2,3}) boyutu: 8
Elemanlar:
  ∅
  [1]
  [2]
  [3]
  [1, 2]
  [1, 3]
  [2, 3]
  [1, 2, 3]
```

3 elemanlı A için |P(A)| = 2³ = 8.
"""

# %% [markdown]
"""
### Örnek 5.3 — Denklik Bağıntısı
"""

# %%
carrier = [1, 2, 3, 4]

# 1~3 ve 2~4: tam denklik bağıntısı
rel_eq = make_relation(carrier, (1,1),(2,2),(3,3),(4,4),(1,3),(3,1),(2,4),(4,2))
print("Denklik bağıntısı mı:", is_equivalence_relation(carrier, rel_eq))

# Bağıntı profili
prof = relation_profile(carrier, rel_eq)
print("Yansımalı:", prof['is_reflexive'])
print("Simetrik:", prof['is_symmetric'])
print("Geçişli:", prof['is_transitive'])
print("Denklik:", prof['is_equivalence_relation'])

# Simetrik+yansımalı ama geçişli değil: (1,2),(2,3) var ama (1,3) yok
rel_not_trans = make_relation(carrier,
    (1,1),(2,2),(3,3),(4,4),(1,2),(2,1),(2,3),(3,2))
print()
print("Geçişsiz bağıntı denklik mi:", is_equivalence_relation(carrier, rel_not_trans))

# %% [markdown]
"""
```text
Denklik bağıntısı mı: True
Yansımalı: True
Simetrik: True
Geçişli: True
Denklik: True

Yalnız simetrik bağıntı denklik mi: False
```

İkinci bağıntı geçişli değil: (1,2) ve (2,4) ∈ R ama (1,4) ∉ R.
"""

# %% [markdown]
"""
### Örnek 5.4 — Özdeşlik ve Ters Bağıntı
"""

# %%
carrier3 = [0, 1, 2]
id_rel = identity_relation(carrier3)
print("Özdeşlik bağıntısı:", sorted(id_rel))

# Simetrik olmayan bir bağıntı
r = make_relation(carrier3, (0,1),(1,2))
print("R:", sorted(r))
print("R^(-1) (ters):", sorted(inverse_relation(r)))

# %% [markdown]
"""
```text
Özdeşlik bağıntısı: [(0, 0), (1, 1), (2, 2)]
R: [(0, 1), (1, 2)]
R^(-1) (ters): [(1, 0), (2, 1)]
```
"""

# %% [markdown]
"""
### Örnek 5.5 — Fonksiyon Türleri
"""

# %%
domain   = [1, 2, 3]
codomain = ['a', 'b', 'c']

# Bijeksiyon
f_bij = normalize_finite_map_data(domain, codomain, {1:'a', 2:'b', 3:'c'})
print("f: {1,2,3} -> {a,b,c}")
print("  enjeksiyon:", is_injective_finite_map(f_bij))
print("  sürjeksiyon:", is_surjective_finite_map(f_bij))
print("  bijeksiyon:", is_bijective_finite_map(f_bij))

# Enjeksiyon ama sürjeksiyon değil
f_inj = normalize_finite_map_data([1,2], ['a','b','c'], {1:'a', 2:'b'})
print()
print("g: {1,2} -> {a,b,c} (eksik c)")
print("  enjeksiyon:", is_injective_finite_map(f_inj))
print("  sürjeksiyon:", is_surjective_finite_map(f_inj))

# Sürjeksiyon ama enjeksiyon değil
f_sur = normalize_finite_map_data([1,2,3], ['x','y'], {1:'x', 2:'x', 3:'y'})
print()
print("h: {1,2,3} -> {x,y} (1 ve 2 aynı yere)")
print("  enjeksiyon:", is_injective_finite_map(f_sur))
print("  sürjeksiyon:", is_surjective_finite_map(f_sur))

# %% [markdown]
"""
```text
f: {1,2,3} -> {a,b,c}
  enjeksiyon: True
  sürjeksiyon: True
  bijeksiyon: True

g: {1,2} -> {a,b,c} (eksik c)
  enjeksiyon: True
  sürjeksiyon: False

h: {1,2,3} -> {x,y} (1 ve 2 aynı yere)
  enjeksiyon: False
  sürjeksiyon: True
```
"""

# %% [markdown]
"""
### Örnek 5.6 — Görüntü ve Ön-Görüntü
"""

# %%
f = normalize_finite_map_data([1,2,3,4], ['a','b','c','d'],
                               {1:'a', 2:'b', 3:'c', 4:'d'})

img = image_of_subset_finite(f, [1, 2])
pre = preimage_of_subset_finite(f, ['b', 'c'])
print("f({1,2}) =", sorted(img))
print("f^(-1)({b,c}) =", sorted(pre))

# Sabit fonksiyon: tüm görüntü tek eleman
g = normalize_finite_map_data([1,2,3], ['z'], {1:'z', 2:'z', 3:'z'})
print()
print("sabit g({1,2,3}) =", sorted(image_of_subset_finite(g, [1,2,3])))
print("g^(-1)({z}) =", sorted(preimage_of_subset_finite(g, ['z'])))

# %% [markdown]
"""
```text
f({1,2}) = ['a', 'b']
f^(-1)({b,c}) = [2, 3]

sabit g({1,2,3}) = ['z']
g^(-1)({z}) = [1, 2, 3]
```

Sabit fonksiyonun bütün etki alanı tek elemanlı görüntüye gönderilir;
ön-görüntüsü de tam etki alanıdır.
"""

# %% [markdown]
"""
## 6. Alıştırmalar

### Kodlama

K1. A = {1,2,3,4,5}, B = {3,4,5,6,7} için A∪B, A∩B ve A\\B'yi `set_union`,
    `set_intersection`, `set_difference` ile hesaplayın.

K2. {1,2,3,4} için güç kümesini üretin; |P| = 16 olduğunu doğrulayın.

K3. Bağıntı R = {(0,0),(1,1),(2,2),(0,1),(1,0),(1,2),(2,1),(0,2),(2,0)} üzerinde
    `relation_profile` çalıştırın; denklik olup olmadığını kontrol edin.

### Teori

T1. A ⊆ B ⟺ A ∩ B = A olduğunu ispatlayın.

T2. f: A → B ve g: B → C fonksiyonlarının her ikisi de enjeksiyon ise
    g ∘ f'nin de enjeksiyon olduğunu ispatlayın.
"""

# %%
if __name__ == "__main__":
    pass
