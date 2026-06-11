# %% [markdown]
"""
# Bölüm 15 — Metrik Tamlık ve Kompaktlık

Metrik tamlık (completeness), bir metrik uzayda Cauchy dizilerinin yakınsayıp
yakınsamadığını araştıran temel bir kavramdır. Tamamen sınırlılık ise kompaktlık
için anahtar bileşendir.
"""

# %% [markdown]
"""
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

(M, d) tam ∧ tamamen sınırlı ⟺ (M, d) kompakttır. (Metrik uzaylarda.)

### Önemli Örnekler

| Uzay | Tam? | Tamamen sınırlı? | Kompakt? |
|------|------|-------------------|---------|
| ℝ (Öklid) | ✓ | ✗ | ✗ |
| [0,1] | ✓ | ✓ | ✓ |
| (0,1) | ✗ | ✓ | ✗ |
| ℚ (rasyoneller) | ✗ | ✗ | ✗ |
| Sonlu metrik | ✓ | ✓ | ✓ |
"""

# %% [markdown]
"""
> **Neden bu konu?** Cauchy dizileri tamlık için gerekli; tam olmayan uzaylarda yakınsama "dışarı kaçar".

> 🔍 **Kendin dene:** `closed_unit_interval_metric()` ve `real_line_metric()` için `is_complete` sonuçlarını karşılaştırın.

> ⚠️ **Sık hata:** Tamlık topolojik özellik değildir; (0,1) ~ ℝ homeomorf ama biri tam diğeri değil.

> ↗️ **Bkz.:** Bölüm 14 (metrik uzay tanımı), Bölüm 7 (kompakt metrik ⟹ tam).

> 💭 **Öz-yansıtma:** Baire kategorisi teoremi neden tam metrik uzaylar için geçerli?
"""

# %% [markdown]
"""
## 2. Teoremler

**Teorem 2.1 (Heine-Borel Metrik Genelleştirmesi).**
Metrik uzayda kompaktlık ⟺ tamlık ∧ tamamen sınırlılık.

**Teorem 2.2 (Banach Sabit-Nokta Teoremi).**
(M, d) tam metrik uzay; T: M → M büzülme (Lipschitz sabiti < 1) ⟹
T'nin eşsiz bir sabit noktası var: T(x*) = x*.

**Teorem 2.3 (Baire Kategorisi Teoremi).**
Tam metrik uzay 1. kategoriden değildir: hiçbir zaman sayılabilir "ince" kümelerin
(hiçbiryerde-yoğun) birleşimi olamaz.
"""

# %% [markdown]
"""
## 3. Algoritmalar

### Sonlu Metrikte is_complete

Sonlu metrik uzayda her Cauchy dizisi eninde sonunda sabit: trivially tam.
Algoritma: O(1).

### Sonlu Metrikte is_totally_bounded

Taşıyıcı kendisi ε-net oluşturur her ε>0 için: trivially tam sınırlı.
Algoritma: O(1).

### metric_compactness_check

    MetricCompactnessCheck(M, d):
        complete ← is_complete(M, d)
        totally_bounded ← is_totally_bounded(M, d)
        return complete ∧ totally_bounded

Sonlu uzayda: her ikisi trivially true → otomatik kompakt.
"""

# %% [markdown]
"""
## 4. pytop API
"""

# %%
from pytop.metric_spaces import FiniteMetricSpace
from pytop.metric_completeness import (
    is_complete,
    is_totally_bounded,
    metric_compactness_check,
    analyze_metric_completeness,
)
from pytop import real_line_metric, closed_unit_interval_metric

# %% [markdown]
"""
## 5. Örnekler

### Örnek 5.1 — Sonlu Metrik: Tam ve Kompakt
"""

# %%
points = ['A', 'B', 'C', 'D']
dist = {(a, b): (0 if a == b else 1) for a in points for b in points}
fms = FiniteMetricSpace(carrier=tuple(points), distance=dist)

print("=== Ornek 5.1: Sonlu Ayrik Metrik ===")
print("is_complete:", is_complete(fms).status)
print("is_totally_bounded:", is_totally_bounded(fms).status)
mc = metric_compactness_check(fms)
print("metric_compactness_check:", mc.status, mc.value)
print()

# %% [markdown]
"""
### Örnek 5.2 — Kapalı [0,1]: Tam ve Kompakt
"""

# %%
ui = closed_unit_interval_metric()
print("=== Ornek 5.2: [0,1] ===")
print("is_complete:", is_complete(ui).status)
print("is_totally_bounded:", is_totally_bounded(ui).status)
print("metric_compactness:", metric_compactness_check(ui).status)
print()

# %% [markdown]
"""
### Örnek 5.3 — Gerçek Doğru ℝ: Tam, Kompakt Değil
"""

# %%
rl = real_line_metric()
print("=== Ornek 5.3: Gercek Dogru R ===")
print("is_complete:", is_complete(rl).status)
print("is_totally_bounded:", is_totally_bounded(rl).status)
print("metric_compactness:", metric_compactness_check(rl).status)
print()
# R tam (her Cauchy dizisi yakınsar) ama tamamen sınırlı DEGIL
# (sınırsız; her ε-net sonsuz uzunlukta gerektirir).

# %% [markdown]
"""
### Örnek 5.4 — analyze_metric_completeness
"""

# %%
print("=== Ornek 5.4: analyze_metric_completeness ===")
r = analyze_metric_completeness(fms)
print("status:", r.status)
print("value:", r.value)
print()

# %% [markdown]
"""
### Örnek 5.5 — Öklid Metriki ile Karşılaştırma
"""

# %%
pts = list(range(5))
dist_eucl = {(a, b): abs(a - b) for a in pts for b in pts}
fms_e = FiniteMetricSpace(carrier=tuple(pts), distance=dist_eucl)

print("=== Ornek 5.5: Oklid {0,1,2,3,4} ===")
print("is_complete:", is_complete(fms_e).status)
print("is_totally_bounded:", is_totally_bounded(fms_e).status)
mc2 = metric_compactness_check(fms_e)
print("compactness:", mc2.status)
print()

# %% [markdown]
"""
## 6. Alıştırmalar

### Kodlama

K1. Rasyonel sayılar ℚ (sembolik) için is_complete sonucunu kontrol edin.
    (pytop.examples: rationals_metric())

K2. Kendi 4-noktalı metrik uzayınızı oluşturun ve metric_compactness_check
    uygulayın.

K3. analyze_metric_completeness(closed_unit_interval_metric()) çalıştırın ve
    justification'ı inceleyin.

### Teori

T1. Banach sabit-nokta teoremini sözlü olarak açıklayın ve bir uygulama örneği verin.

T2. Kapalı [0,1]'in tam olduğunu; açık (0,1)'in tam olmadığını gösterin.
    (Hint: 1/n dizisi Cauchy ama 0 ∉ (0,1).)
"""

if __name__ == "__main__":
    print("pytop Kullanim Kilavuzu — Bolum 8: Metrik Tamlik")
    print("=" * 50)
