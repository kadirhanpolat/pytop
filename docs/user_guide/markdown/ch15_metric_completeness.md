# Bölüm 8 — Metrik Tamlık ve Kompaktlık

Metrik tamlık (completeness), bir metrik uzayda Cauchy dizilerinin yakınsayıp
yakınsamadığını araştıran temel bir kavramdır. Tamamen sınırlılık ise kompaktlık
için anahtar bileşendir.

---

## 1. Konu

### Cauchy Dizisi ve Tamlık

Bir (M, d) metrik uzayında {x_n} dizisi **Cauchy** ise:

    ∀ε>0, ∃N∈ℕ: m,n≥N ⟹ d(x_m, x_n) < ε

(M, d) **tam (complete)** ise: Her Cauchy dizisi M'de bir limite yakınsır.

### Tamamen Sınırlılık

A ⊆ M **tamamen sınırlı (totally bounded)** ise: her ε>0 için A'nın sonlu bir
ε-net (ε-kapsama) kümesi vardır.

    ε-net: S = {s_1,...,s_n} ⊆ M, her x∈A için ∃i: d(x,s_i) < ε

### Metrik Kompaktlık Karakterizasyonu

**(M, d) tam ∧ tamamen sınırlı ⟺ (M, d) kompakttır.** (Metrik uzaylarda.)

### Önemli Örnekler

| Uzay | Tam? | Tamamen sınırlı? | Kompakt? |
|------|------|-------------------|---------|
| ℝ (Öklid) | ✓ | ✗ | ✗ |
| [0,1] | ✓ | ✓ | ✓ |
| (0,1) | ✗ | ✓ | ✗ |
| ℚ (rasyoneller) | ✗ | ✗ | ✗ |
| Sonlu metrik | ✓ | ✓ | ✓ |

---

## 2. Teoremler

**Teorem 2.1 (Heine-Borel Metrik Genelleştirmesi).**
Metrik uzayda kompaktlık ⟺ tamlık ∧ tamamen sınırlılık.

**Teorem 2.2 (Banach Sabit-Nokta Teoremi).**
(M, d) tam metrik uzay; T: M → M büzülme (Lipschitz sabiti < 1) ⟹
T'nin eşsiz bir sabit noktası var: T(x*) = x*.

**Teorem 2.3 (Baire Kategorisi Teoremi).**
Tam metrik uzay 1. kategoriden değildir: hiçbir zaman sayılabilir "ince" kümelerin
(hiçbiryerde-yoğun) birleşimi olamaz.

---

## 3. Algoritmalar

### Sonlu Metrikte is_complete

Sonlu metrik uzayda her Cauchy dizisi eninde sonunda sabit: trivially tam.
Algoritma: O(1).

### Sonlu Metrikte is_totally_bounded

Taşıyıcı kendisi ε-net oluşturur her ε>0 için: trivially tamamen sınırlı.
Algoritma: O(1).

### metric_compactness_check

```
MetricCompactnessCheck(M, d):
    complete <- is_complete(M, d)
    totally_bounded <- is_totally_bounded(M, d)
    return complete AND totally_bounded
```

Sonlu uzayda: her ikisi trivially true → otomatik kompakt.

---

## 4. pytop API

```python
from pytop.metric_spaces import FiniteMetricSpace
from pytop.metric_completeness import (
    is_complete,
    is_totally_bounded,
    metric_compactness_check,
    analyze_metric_completeness,
)
from pytop import real_line_metric, closed_unit_interval_metric
```

Tüm fonksiyonlar `Result` döner: `.status`, `.value`, `.justification`.

---

## 5. Örnekler

### Örnek 5.1 — Sonlu Metrik: Tam ve Kompakt

```python
from pytop.metric_spaces import FiniteMetricSpace
from pytop.metric_completeness import is_complete, is_totally_bounded, metric_compactness_check

points = ['A', 'B', 'C', 'D']
dist = {(a, b): (0 if a == b else 1) for a in points for b in points}
fms = FiniteMetricSpace(carrier=tuple(points), distance=dist)

print("is_complete:", is_complete(fms).status)
print("is_totally_bounded:", is_totally_bounded(fms).status)
mc = metric_compactness_check(fms)
print("metric_compactness_check:", mc.status, mc.value)
```

```text
is_complete: true
is_totally_bounded: true
metric_compactness_check: true True
```

### Örnek 5.2 — Kapalı [0,1]: Tam ve Kompakt

```python
from pytop import closed_unit_interval_metric

ui = closed_unit_interval_metric()
print("is_complete:", is_complete(ui).status)
print("is_totally_bounded:", is_totally_bounded(ui).status)
print("metric_compactness:", metric_compactness_check(ui).status)
```

```text
is_complete: unknown
is_totally_bounded: unknown
metric_compactness: unknown
```

Sembolik uzaylar için sonuç tag bilgisine göre `unknown` dönebilir.

### Örnek 5.3 — Gerçek Doğru ℝ: Tam, Kompakt Değil

```python
from pytop import real_line_metric

rl = real_line_metric()
print("is_complete:", is_complete(rl).status)
print("is_totally_bounded:", is_totally_bounded(rl).status)
print("metric_compactness:", metric_compactness_check(rl).status)
```

```text
is_complete: unknown
is_totally_bounded: unknown
metric_compactness: unknown
```

### Örnek 5.4 — analyze_metric_completeness

```python
from pytop.metric_completeness import analyze_metric_completeness

r = analyze_metric_completeness(fms)
print("status:", r.status)
print("value:", r.value)
```

```text
status: true
value: {'is_complete': True, 'is_totally_bounded': True, 'metric_compact': True}
```

### Örnek 5.5 — Öklid Metriki ile Karşılaştırma

```python
pts = list(range(5))
dist_eucl = {(a, b): abs(a - b) for a in pts for b in pts}
fms_e = FiniteMetricSpace(carrier=tuple(pts), distance=dist_eucl)

print("is_complete:", is_complete(fms_e).status)
print("is_totally_bounded:", is_totally_bounded(fms_e).status)
mc2 = metric_compactness_check(fms_e)
print("compactness:", mc2.status)
```

```text
is_complete: true
is_totally_bounded: true
compactness: true
```

---

## 6. Alıştırmalar

### Kodlama

K1. Rasyonel sayılar ℚ (sembolik) için `is_complete` sonucunu kontrol edin.

K2. Kendi 4-noktalı metrik uzayınızı oluşturun ve `metric_compactness_check`
    uygulayın.

K3. `analyze_metric_completeness(fms)` çalıştırın ve `value` sözlüğünü inceleyin.

### Teori

T1. Banach sabit-nokta teoremini sözlü olarak açıklayın ve bir uygulama örneği verin.

T2. Kapalı [0,1]'in tam olduğunu; açık (0,1)'in tam olmadığını gösterin.
    (Hint: 1/n dizisi Cauchy ama 0 ∉ (0,1).)
