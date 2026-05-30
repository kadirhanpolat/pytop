# Bölüm 4 — Kompaktlık

Kompaktlık, sonsuz yapılarda "sınırlılık" fikrinin topolojik soyutlamasıdır.
Açık örtü tanımı temel alınarak incelenmekte; varyantlar ve lokal kompaktlık da ele alınmaktadır.

---

## 1. Konu

### Kompaktlık Tanımı

(X, τ) topolojik uzayı **kompakt** ise:
Her açık örtü `{U_α}` için sonlu alt-örtü vardır.

    X ⊆ ⋃_{α} U_α  ⟹  ∃ sonlu I: X ⊆ ⋃_{α∈I} U_α

### Kompaktlık Varyantları

| Varyant | Tanım |
|---------|-------|
| **Kompakt** | Her açık örtünün sonlu alt-örtüsü var |
| **Sayılabilir kompakt** | Her sayılabilir açık örtünün sonlu alt-örtüsü var |
| **Ardışımlı kompakt** | Her dizi bir yakınsak alt-dizi içerir |
| **Sözde kompakt (pseudocompact)** | Her sürekli f: X → ℝ sınırlıdır |
| **Lindelöf** | Her açık örtünün sayılabilir alt-örtüsü var |
| **σ-kompakt** | Sayılabilir kompakt kümelerin birleşimi |
| **Lokal kompakt** | Her noktanın kompakt komşuluğu var |
| **Metakompakt** | Her açık örtünün nokta-sonlu açık rafinmanı var |

**Sıralama:** Kompakt ⟹ Sayılabilir kompakt ⟹ Ardışımlı kompakt ⟹ Lindelöf.

### Lokal Kompaktlık

x ∈ X noktasında **lokal kompakt:** U komşuluğu kompakt kapanış içerir: `U ⊆ K kompakt`.

---

## 2. Teoremler

**Teorem 2.1 (Heine-Borel).** ℝⁿ'de kompakt ⟺ kapalı ve sınırlı.

**Teorem 2.2.** Kompakt + Hausdorff ⟹ Normal (T4).

**Teorem 2.3.** Kompakt uzaydan Hausdorff uzaya sürekli bijeksiyon ⟹ homeomorfizma.

**Teorem 2.4 (Tychonoff).** Keyfi kompakt uzayların kartezyen çarpımı kompakttır.

**Teorem 2.5 (Alexandroff Tek-Nokta Kompaktifikasyonu).** Her lokal kompakt Hausdorff uzay X için ∞ noktası eklenerek X* = X ∪ {∞} kompakt Hausdorff uzay oluşturulabilir.

---

## 3. Algoritmalar

### Sonlu Uzayda Kompaktlık

Sonlu uzay her zaman kompakttır: her örtü sonlu sayıda eleman içerir.
Algoritma: O(1).

### analyze_compactness_variants — Tag Tabanlı Çıkarım

```
AnalyzeVariants(X, τ):
    if X sonlu:
        tüm varyantlar ← True
        return VariantProfile(...)
    tags'e göre çıkarım yap:
        'compact' ∈ tags ⟹ countably_compact, sequentially_compact, lindelof
        'metric' ∧ 'compact' ⟹ sequentially_compact
        'pseudocompact' ∧ ~Tychonoff ⟹ sadece pseudocompact
```

---

## 4. pytop API

```python
from pytop import (
    is_compact,
    is_lindelof,
    is_locally_compact,
)
from pytop.compactness_variants import (
    is_countably_compact,
    is_sequentially_compact,
    analyze_compactness_variants,
)
```

`analyze_compactness_variants(space)` → `Result` döner; `.value` bir `dict` içerir.

---

## 5. Örnekler

### Örnek 5.1 — Sonlu Uzaylar: Otomatik Kompakt

```python
from pytop import sierpinski_space, discrete_topology, finite_chain_space, is_compact

s = sierpinski_space()
print("Sierpinski compact?", is_compact(s).status)     # true
d = discrete_topology(1, 2, 3)
print("Discrete(3) compact?", is_compact(d).status)    # true
c = finite_chain_space(3)
print("Chain(3) compact?", is_compact(c).status)       # true
```

```text
Sierpinski compact?      true
Chain(3) compact?        true
Discrete(3) compact?     true
```

Sonlu uzaylar trivially kompakttır: her örtü zaten sonlu.

### Örnek 5.2 — Gerçek Doğru ℝ: Kompakt Değil

```python
from pytop import real_line_metric, is_compact, is_lindelof, is_locally_compact

rl = real_line_metric()
print("compact?", is_compact(rl).status)           # false
print("lindelof?", is_lindelof(rl).status)         # true
print("locally_compact?", is_locally_compact(rl).status)  # conditional
```

```text
compact?          false
lindelof?         true
locally_compact?  conditional
```

ℝ kompakt değil (sınırsız), ama Lindelöf ve lokal kompakt.

### Örnek 5.3 — Kapalı [0,1]: Kompakt

```python
from pytop import closed_unit_interval_metric, is_compact
from pytop.compactness_variants import is_sequentially_compact, is_countably_compact

ui = closed_unit_interval_metric()
print("compact?", is_compact(ui).status)                      # true
print("sequentially?", is_sequentially_compact(ui).status)   # true
print("countably?", is_countably_compact(ui).status)         # true
```

```text
compact?          true
sequentially?     true
countably?        true
```

### Örnek 5.4 — analyze_compactness_variants: Gerçek Doğru

```python
from pytop import real_line_metric
from pytop.compactness_variants import analyze_compactness_variants

rl = real_line_metric()
r = analyze_compactness_variants(rl)
for key, val in r.value.items():
    if hasattr(val, 'status'):
        print(f"  {key:<25}: {val.status}")
    else:
        print(f"  {key:<25}: {val}")
```

```text
  representation           : infinite_metric
  countably_compact        : unknown
  sequentially_compact     : unknown
  pseudocompact            : false
  feebly_compact           : false
  metacompact              : true
  relatively_compact       : unknown
  sigma_compact            : unknown
  lindelof                 : true
```

### Örnek 5.5 — analyze_compactness_variants: Sierpiński

```python
s = sierpinski_space()
r = analyze_compactness_variants(s)
for key, val in r.value.items():
    if hasattr(val, 'status'):
        print(f"  {key:<25}: {val.status}")
    else:
        print(f"  {key:<25}: {val}")
```

```text
  representation           : finite
  countably_compact        : true
  sequentially_compact     : true
  pseudocompact            : true
  feebly_compact           : true
  metacompact              : true
  relatively_compact       : true
  sigma_compact            : true
  lindelof                 : true
```

---

## 6. Alıştırmalar

### Kodlama

K1. `finite_chain_space(5)` ve `discrete_topology(1,2,3,4,5)` için `is_compact` karşılaştırın.
    Her ikisi de kompakt mı?

K2. `naturals_cofinite()` için `is_compact`, `is_lindelof`, `is_countably_compact` hesaplayın.

K3. `closed_unit_interval_metric()` ile `real_line_metric()` için
    `analyze_compactness_variants` çalıştırıp çıktıları karşılaştırın.

### Teori

T1. Kompakt + sürekli ⟹ görüntü kompakt olduğunu ispatlayın.
    (İpucu: görüntüdeki bir açık örtüyü geri çek.)

T2. Heine-Borel teoreminin ℝ'deki neden geçerli olduğunu açıklayın:
    [0,1] neden kompakt, (0,1) neden kompakt değil?
