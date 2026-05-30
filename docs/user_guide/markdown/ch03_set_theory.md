# Bölüm 3 — Küme Teorisi ve Fonksiyon Temelleri

pytop'un tüm modülleri küme teorisi ve fonksiyon kavramları üzerine kuruludur.
Bu bölüm, kılavuzun geri kalanında varsayılan ön koşulları pytop API'siyle birlikte pekiştirir.

---

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
| Fark | A \ B | a ∈ A ve a ∉ B |
| Tümleyen | A^c | a ∉ A (evren X'te) |

### Bağıntılar

Kartezyen çarpım: A × B = {(a, b) : a ∈ A, b ∈ B}.
A üzerinde bir bağıntı R ⊆ A × A.

| Özellik | Koşul |
|---------|-------|
| Yansımalı | ∀a, (a,a) ∈ R |
| Simetrik | (a,b) ∈ R ⟹ (b,a) ∈ R |
| Geçişli | (a,b),(b,c) ∈ R ⟹ (a,c) ∈ R |
| **Denklik** | Yansımalı + Simetrik + Geçişli |

### Fonksiyonlar

f: A → B, her a ∈ A için tek bir f(a) ∈ B.

| Tür | Koşul |
|-----|-------|
| Enjeksiyon | f(a₁) = f(a₂) ⟹ a₁ = a₂ |
| Sürjeksiyon | ∀b ∈ B, ∃a: f(a) = b |
| Bijeksiyon | Enjeksiyon + Sürjeksiyon |

---

## 2. Teoremler

**Teorem 2.1 (De Morgan).**
(A ∪ B)^c = A^c ∩ B^c  ve  (A ∩ B)^c = A^c ∪ B^c.

**Teorem 2.2 (Güç Kümesi Boyutu).**
|A| = n ⟹ |P(A)| = 2ⁿ.

**Teorem 2.3 (Denklik Sınıfları Bölüntü Oluşturur).**
~ denklik bağıntısı ise {[a] : a ∈ A} A'nın bir bölüntüsüdür.

**Teorem 2.4 (Ön-Görüntü Özellikleri).**
f⁻¹(S₁ ∪ S₂) = f⁻¹(S₁) ∪ f⁻¹(S₂)  ve  f⁻¹(S₁ ∩ S₂) = f⁻¹(S₁) ∩ f⁻¹(S₂).

---

## 3. Algoritmalar

### Güç Kümesi — O(2^|A|)

```
PowerSet(A):
    result <- {∅}
    for each a in A:
        result <- result ∪ {S ∪ {a} : S ∈ result}
    return result
```

### Denklik Bağıntısı Doğrulama — O(|R| · |A|)

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

---

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

---

## 5. Örnekler

### Örnek 5.1 — Küme İşlemleri

```python
A = make_set(1, 2, 3)
B = make_set(2, 3, 4)
print("A union B:", sorted(set_union(A, B)))
print("A inter B:", sorted(set_intersection(A, B)))
print("A diff B:", sorted(set_difference(A, B)))
print("{2,3} subset A:", is_subset({2, 3}, A))
print("{1,4} subset A:", is_subset({1, 4}, A))
```

```text
A union B: [1, 2, 3, 4]
A inter B: [2, 3]
A diff B: [1]
{2,3} subset A: True
{1,4} subset A: False
```

### Örnek 5.2 — Güç Kümesi

```python
P = power_set([1, 2, 3])
print("P({1,2,3}) boyutu:", len(P))
for s in sorted([sorted(list(x)) for x in P], key=lambda x: (len(x), x)):
    print(" ", s if s else "empty")
```

```text
P({1,2,3}) boyutu: 8
  empty
  [1]
  [2]
  [3]
  [1, 2]
  [1, 3]
  [2, 3]
  [1, 2, 3]
```

3 elemanlı A için |P(A)| = 2³ = 8.

### Örnek 5.3 — Denklik Bağıntısı

```python
carrier = [1, 2, 3, 4]
rel_eq = make_relation(carrier, (1,1),(2,2),(3,3),(4,4),(1,3),(3,1),(2,4),(4,2))
print("Denklik bağıntısı mı:", is_equivalence_relation(carrier, rel_eq))
prof = relation_profile(carrier, rel_eq)
print("Yansımalı:", prof['is_reflexive'])
print("Simetrik:", prof['is_symmetric'])
print("Geçişli:", prof['is_transitive'])

rel_not_trans = make_relation(carrier,
    (1,1),(2,2),(3,3),(4,4),(1,2),(2,1),(2,3),(3,2))
print("Geçişsiz bağıntı denklik mi:", is_equivalence_relation(carrier, rel_not_trans))
```

```text
Denklik bağıntısı mı: True
Yansımalı: True
Simetrik: True
Geçişli: True
Geçişsiz bağıntı denklik mi: False
```

İkinci bağıntı geçişli değil: (1,2) ve (2,3) ∈ R ama (1,3) ∉ R.

### Örnek 5.4 — Özdeşlik ve Ters Bağıntı

```python
id_rel = identity_relation([0, 1, 2])
print("Özdeşlik:", sorted(id_rel))

r = make_relation([0,1,2], (0,1),(1,2))
print("R:", sorted(r))
print("R^(-1):", sorted(inverse_relation(r)))
```

```text
Özdeşlik: [(0, 0), (1, 1), (2, 2)]
R: [(0, 1), (1, 2)]
R^(-1): [(1, 0), (2, 1)]
```

### Örnek 5.5 — Fonksiyon Türleri

```python
f_bij = normalize_finite_map_data([1,2,3], ['a','b','c'], {1:'a', 2:'b', 3:'c'})
print("bijeksiyon:", is_bijective_finite_map(f_bij))

f_inj = normalize_finite_map_data([1,2], ['a','b','c'], {1:'a', 2:'b'})
print("enjeksiyon (eksik c):", is_injective_finite_map(f_inj),
      "| sürjeksiyon:", is_surjective_finite_map(f_inj))

f_sur = normalize_finite_map_data([1,2,3], ['x','y'], {1:'x', 2:'x', 3:'y'})
print("sürjeksiyon (çakışan):", is_surjective_finite_map(f_sur),
      "| enjeksiyon:", is_injective_finite_map(f_sur))
```

```text
bijeksiyon: True
enjeksiyon (eksik c): True | sürjeksiyon: False
sürjeksiyon (çakışan): True | enjeksiyon: False
```

### Örnek 5.6 — Görüntü ve Ön-Görüntü

```python
f = normalize_finite_map_data([1,2,3,4], ['a','b','c','d'],
                               {1:'a', 2:'b', 3:'c', 4:'d'})
print("f({1,2}) =", sorted(image_of_subset_finite(f, [1, 2])))
print("f^(-1)({b,c}) =", sorted(preimage_of_subset_finite(f, ['b', 'c'])))
```

```text
f({1,2}) = ['a', 'b']
f^(-1)({b,c}) = [2, 3]
```

---

## 6. Alıştırmalar

### Kodlama

K1. A = {1,2,3,4,5}, B = {3,4,5,6,7} için A∪B, A∩B ve A\B hesaplayın.

K2. {1,2,3,4} için güç kümesini üretin; |P| = 16 olduğunu doğrulayın.

K3. R = {(0,0),(1,1),(2,2),(0,1),(1,0),(1,2),(2,1),(0,2),(2,0)} üzerinde
    `relation_profile` çalıştırın; denklik olup olmadığını kontrol edin.

### Teori

T1. A ⊆ B ⟺ A ∩ B = A olduğunu ispatlayın.

T2. f: A → B ve g: B → C her ikisi de enjeksiyon ise g ∘ f de enjeksiyondur.
