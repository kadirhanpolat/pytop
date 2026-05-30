# Bölüm 7 — Metrik Uzaylar

Metrik uzaylar, mesafe fonksiyonuna dayanan topolojik yapılardır. Her metrik uzay
doğal olarak bir topolojik uzay oluşturur; bu yapı "indüklenen topoloji" olarak adlandırılır.

---

## 1. Konu

### Metrik Aksiyomları

Bir M kümesi ve d: M×M → [0,∞) fonksiyonu verilsin. (M, d) bir **metrik uzay**,
d ise bir **metrik** olarak adlandırılır, eğer:

- **(M1) Özdeşlik:** d(x,y) = 0 ⟺ x = y
- **(M2) Simetri:** d(x,y) = d(y,x)
- **(M3) Üçgen eşitsizliği:** d(x,z) ≤ d(x,y) + d(y,z)

(M3'ten M1 ile birlikte **pozitif tanımlılık** türer: d(x,y) ≥ 0.)

### Temel Kavramlar

- **Açık top:** B(x, r) = {y ∈ M : d(x,y) < r}
- **Kapalı top:** B̄(x, r) = {y ∈ M : d(x,y) ≤ r}
- **İndüklenen topoloji:** τ_d = {U : ∀x∈U, ∃ε>0, B(x,ε)⊆U}
- **Çap:** diam(A) = sup{d(x,y) : x,y ∈ A}

### Standart Metrikler

| Metrik | Tanım | Uzay |
|--------|-------|------|
| Öklid | d(x,y) = \|x-y\| | ℝ |
| Ayrık | d(x,y) = 0 veya 1 | Herhangi X |
| l∞ (max) | max_i d_i(x_i,y_i) | Çarpım uzayı |
| Sınırlı (capped) | d'(x,y) = min(d(x,y), 1) | Eşdeğer topoloji |

---

## 2. Teoremler

**Teorem 2.1.** Her metrik uzay Hausdorff (T2) ve 1. sayılabilirdir.
*(Kanıt: B(x, d(x,y)/2) ve B(y, d(x,y)/2) disjoint; {B(x,1/n)} yerel baz.)*

**Teorem 2.2 (Sınırlı Metrik Eşdeğerliği).**
d'(x,y) = min(d(x,y),1) ile d aynı topolojiyi indükler.

**Teorem 2.3.** ℝⁿ üzerindeki max, sum ve Öklid metrikleri topolojik olarak eşdeğerdir.

---

## 3. Algoritmalar

### validate_metric — O(|X|³)

```
ValidateMetric(X, d):
    // M1: özdeşlik
    for each x in X:
        if d(x,x) != 0: return False
        for each y != x:
            if d(x,y) == 0: return False
    // M2: simetri
    for each x,y in X:
        if d(x,y) != d(y,x): return False
    // M3: üçgen
    for each x,y,z in X:
        if d(x,z) > d(x,y) + d(y,z): return False
    return True
```

Karmaşıklık: O(|X|³) — üçgen eşitsizliği dominates.

### open_ball — O(|X|)

```
OpenBall(x, r, X, d):
    return {y in X : d(x,y) < r}
```

---

## 4. pytop API

```python
from pytop.metric_spaces import (
    FiniteMetricSpace,
    SymbolicMetricSpace,
    validate_metric,
)
from pytop import (
    open_ball,
    closed_ball,
    distance_to_subset,
    diameter_of_subset,
    is_bounded_subset,
    capped_metric,
    normalized_metric,
)
```

`FiniteMetricSpace(carrier=tuple, distance=dict)` — mesafe sözlüğü `(a,b): float` şeklinde.

`open_ball(fms, point, radius)` → `set` döner (Result değil).

`capped_metric(distance_fn, cap=1.0)` → `Callable` döner; yeni `FiniteMetricSpace` değil.

---

## 5. Örnekler

### Örnek 5.1 — Ayrık Metrik Uzay Oluşturma

```python
from pytop.metric_spaces import FiniteMetricSpace

points = [1, 2, 3, 4]
dist_discrete = {(a, b): (0 if a == b else 1) for a in points for b in points}
fms = FiniteMetricSpace(carrier=tuple(points), distance=dist_discrete)

print("carrier:", fms.carrier)
print("d(1,2):", fms.distance[(1,2)])
print("d(1,1):", fms.distance[(1,1)])
```

```text
carrier: (1, 2, 3, 4)
d(1,2): 1
d(1,1): 0
```

### Örnek 5.2 — validate_metric

```python
from pytop.metric_spaces import validate_metric

r = validate_metric(fms)
print("status:", r.status)
print("justification:", r.justification[0] if r.justification else "")
```

```text
status: true
justification: All metric axioms hold on the explicit finite carrier.
```

### Örnek 5.3 — open_ball ve closed_ball

```python
from pytop import open_ball, closed_ball

print("B(1, 0.5) =", open_ball(fms, 1, 0.5))    # yalnizca {1}
print("B(1, 1.5) =", open_ball(fms, 1, 1.5))    # tum uzay
print("Bclosed(1, 1.0) =", closed_ball(fms, 1, 1.0))  # tum uzay
```

```text
B(1, 0.5) = {1}
B(1, 1.5) = {1, 2, 3, 4}
Bclosed(1, 1.0) = {1, 2, 3, 4}
```

Ayrık metrikte B(1, r): r < 1 ise yalnız {1}, r ≥ 1 ise tüm uzay.

### Örnek 5.4 — diameter ve distance_to_subset

```python
from pytop import diameter_of_subset, distance_to_subset, is_bounded_subset

print("diam({1,2,3}):", diameter_of_subset(fms, {1, 2, 3}))
print("d(1, {2,3}):", distance_to_subset(fms, 1, {2, 3}))
print("is_bounded({1,2}):", is_bounded_subset(fms, {1, 2}))
```

```text
diam({1,2,3}): 1.0
d(1, {2,3}): 1.0
is_bounded({1,2}): True
```

### Örnek 5.5 — Öklid Metriki

```python
points_line = [0, 1, 2, 3]
dist_eucl = {(a, b): abs(a - b) for a in points_line for b in points_line}
fms_line = FiniteMetricSpace(carrier=tuple(points_line), distance=dist_eucl)

print("d(0,3):", fms_line.distance[(0,3)])
print("B(1, 1.5) =", open_ball(fms_line, 1, 1.5))
print("diam({0,1,2,3}):", diameter_of_subset(fms_line, {0,1,2,3}))
```

```text
d(0,3): 3
B(1, 1.5) = {0, 1, 2}
diam({0,1,2,3}): 3.0
```

### Örnek 5.6 — capped_metric

```python
from pytop import capped_metric

cap_fn = capped_metric(fms_line.distance, cap=1.0)
print("d(0,3) capped:", cap_fn(0, 3))  # min(3, 1.0) = 1.0
print("d(0,1) capped:", cap_fn(0, 1))  # min(1, 1.0) = 1.0
```

```text
d(0,3) capped: 1.0
d(0,1) capped: 1.0
```

`capped_metric` eşit topoloji üretir ama değerler [0, cap] aralığındadır.

---

## 6. Alıştırmalar

### Kodlama

K1. {A, B, C, D} noktaları üzerinde bir metrik tanımlayın ve `validate_metric` ile
    doğrulayın. Üçgen eşitsizliğini ihlal eden bir örnek de deneyin.

K2. Öklid metrikli {0,1,...,9} üzerinde `open_ball(fms, 5, 3.0)` ve
    `closed_ball(fms, 5, 3.0)` hesaplayın.

K3. `normalized_metric` kullanarak bir metriği [0,1]'e normalleştirin.

### Teori

T1. Her metrik uzayın Hausdorff olduğunu ispatlayın.
    (İpucu: d(x,y)>0 için B(x, ε) ∩ B(y, ε) = ∅ seçin.)

T2. d' = min(d, 1) ve d aynı topolojiyi indüklediğini gösterin.
