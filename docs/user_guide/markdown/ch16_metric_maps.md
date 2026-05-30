# Bölüm 16 — Metrik Fonksiyonlar ve Sözleşmeler

Bu bölümde metrik uzaylar arasındaki fonksiyon türleri (izometri, Lipschitz, sürekli)
ve bunların sınıflandırılması incelenmektedir.

---

## 1. Konu

### Metrik Fonksiyon Sınıfları

f: (M₁,d₁) → (M₂,d₂) fonksiyonu:

| Sınıf | Koşul |
|-------|-------|
| **Genişlemez (non-expansive)** | d₂(f(x),f(y)) ≤ d₁(x,y) |
| **Lipschitz** | ∃K>0: d₂(f(x),f(y)) ≤ K·d₁(x,y) |
| **Üniform sürekli** | ∀ε>0, ∃δ>0: d₁(x,y)<δ ⟹ d₂(f(x),f(y))<ε |
| **Sürekli** | Her noktada ε-δ sürekliliği |
| **İzometri** | d₂(f(x),f(y)) = d₁(x,y) (mesafeyi korur) |
| **Benzerlik (similarity)** | ∃c>0: d₂(f(x),f(y)) = c·d₁(x,y) |
| **Homeomorfizma** | Bijektif sürekli; ters de sürekli |

**Sıralama:** İzometri ⟹ Genişlemez ⟹ Lipschitz ⟹ Üniform sürekli ⟹ Sürekli

### Lipschitz Sabiti

    K = sup_{x≠y} d₂(f(x),f(y)) / d₁(x,y)

İzometri: K=1 ve eşitlik; benzerlik: K=c sabit.

---

## 2. Teoremler

**Teorem 2.1.** İzometri ⟹ homeomorfizma. (Bijektif izometri bir homeomorfizma.)

**Teorem 2.2.** Benzerlik: c=1 ⟹ İzometri.

**Teorem 2.3.** Lipschitz ⟹ Üniform sürekli ⟹ Sürekli.
*(Kanıt: δ=ε/K alarak Lipschitz → ünif. süreklilik; her nokta için lokal olarak.)*

**Teorem 2.4.** Kompakt metrik uzaydan metrik uzaya her sürekli fonksiyon
üniform süreklidir.

---

## 3. Algoritmalar

### classify_finite_metric_map — O(|X|²)

```
ClassifyMap(X, d1, Y, d2, f):
    K <- 0
    isometry <- True
    similarity_ratio <- None

    for each pair (x1, x2) with x1 != x2:
        ratio <- d2(f(x1),f(x2)) / d1(x1,x2)
        K <- max(K, ratio)
        if d2(f(x1),f(x2)) != d1(x1,x2): isometry <- False
        if similarity_ratio is None: similarity_ratio <- ratio
        elif ratio != similarity_ratio: similarity_ratio <- None  // sabit degil

    return MetricMapProfile(lipschitz_constant=K, isometry=isometry, ...)
```

Karmaşıklık: O(|X|²).

---

## 4. pytop API

```python
from pytop.metric_spaces import FiniteMetricSpace
from pytop.metric_map_taxonomy import (
    classify_finite_metric_map,
    metric_map_profile,
    MetricMapProfile,
)
```

`classify_finite_metric_map(fms1, fms2, f)` → `MetricMapProfile` döner (Result değil).

`MetricMapProfile` alanları: `isometry`, `similarity`, `similarity_ratio`,
`lipschitz_constant`, `non_expansive`, `bijective`, `lipschitz`, `continuous`,
`uniformly_continuous`, `homeomorphism`, `name`, `certification`.

---

## 5. Örnekler

### Örnek 5.1 — Özdeşlik Fonksiyonu: İzometri

```python
from pytop.metric_spaces import FiniteMetricSpace
from pytop.metric_map_taxonomy import classify_finite_metric_map

pts = [1, 2, 3, 4]
dist_disc = {(a, b): (0 if a == b else 1) for a in pts for b in pts}
fms = FiniteMetricSpace(carrier=tuple(pts), distance=dist_disc)

f_id = {1: 1, 2: 2, 3: 3, 4: 4}
prof_id = classify_finite_metric_map(fms, fms, f_id)

print("isometry:", prof_id.isometry)
print("lipschitz_constant:", prof_id.lipschitz_constant)
print("similarity:", prof_id.similarity)
```

```text
isometry: True
lipschitz_constant: 1.0
similarity: True
```

### Örnek 5.2 — 2× Ölçekleme: Benzerlik, İzometri ✗

```python
pts2 = [2, 4, 6, 8]
dist_eucl1 = {(a, b): abs(a - b) for a in pts for b in pts}
dist_eucl2 = {(a, b): abs(a - b) for a in pts2 for b in pts2}
fms_line1 = FiniteMetricSpace(carrier=tuple(pts), distance=dist_eucl1)
fms_line2 = FiniteMetricSpace(carrier=tuple(pts2), distance=dist_eucl2)

f_scale = {1: 2, 2: 4, 3: 6, 4: 8}
prof_scale = classify_finite_metric_map(fms_line1, fms_line2, f_scale)

print("isometry:", prof_scale.isometry)
print("similarity:", prof_scale.similarity)
print("similarity_ratio:", prof_scale.similarity_ratio)
print("lipschitz_constant:", prof_scale.lipschitz_constant)
```

```text
isometry: False
similarity: True
similarity_ratio: 2.0
lipschitz_constant: 2.0
```

### Örnek 5.3 — Sabit Fonksiyon: Lipschitz K=0

```python
f_const = {1: 1, 2: 1, 3: 1, 4: 1}
prof_const = classify_finite_metric_map(fms, fms, f_const)

print("isometry:", prof_const.isometry)
print("lipschitz_constant:", prof_const.lipschitz_constant)
print("non_expansive:", prof_const.non_expansive)
print("bijective:", prof_const.bijective)
```

```text
isometry: False
lipschitz_constant: 0.0
non_expansive: True
bijective: False
```

Sabit fonksiyon: K=0 (en küçük Lipschitz sabiti), genişlemez, ama bijektif değil.

### Örnek 5.4 — MetricMapProfile Alanları

```python
p = prof_id
print("name:", p.name)
print("certification:", p.certification)
print("non_expansive:", p.non_expansive)
print("lipschitz:", p.lipschitz)
print("uniformly_continuous:", p.uniformly_continuous)
print("continuous:", p.continuous)
print("isometry:", p.isometry)
print("homeomorphism:", p.homeomorphism)
```

```text
name: f
certification: exact-finite
non_expansive: True
lipschitz: True
uniformly_continuous: True
continuous: True
isometry: True
homeomorphism: True
```

### Örnek 5.5 — Karşılaştırma: İzometri vs Benzerlik

```python
print("Ozdeslik  K:", prof_id.lipschitz_constant,
      "| isometry:", prof_id.isometry,
      "| ratio:", prof_id.similarity_ratio)
print("2x scale  K:", prof_scale.lipschitz_constant,
      "| isometry:", prof_scale.isometry,
      "| ratio:", prof_scale.similarity_ratio)
print("Sabit     K:", prof_const.lipschitz_constant,
      "| isometry:", prof_const.isometry)
```

```text
Ozdeslik  K: 1.0 | isometry: True | ratio: 1.0
2x scale  K: 2.0 | isometry: False | ratio: 2.0
Sabit     K: 0.0 | isometry: False
```

---

## 6. Alıştırmalar

### Kodlama

K1. {1,2,3} üzerinde f(1)=2, f(2)=3, f(3)=1 (döngü) fonksiyonunu ayrık metrikte
    `classify_finite_metric_map` ile sınıflandırın.

K2. Öklid metrikli {0,1,2,3,4} uzayında f(x) = x+1 (4'e kadar) gibi bir kaydırma
    fonksiyonu tanımlayın. Lipschitz sabitini hesaplayın.

K3. Bir ezme (contracting) fonksiyon tanımlayın: f(x) = 1 (sabit). Lipschitz
    sabitinin 0 olduğunu doğrulayın.

### Teori

T1. İzometri ⟹ genişlemez ⟹ Lipschitz (K=1) zincirini ispatlayın.

T2. Lipschitz ⟹ üniform sürekli olduğunu δ=ε/K seçimi ile ispatlayın.
