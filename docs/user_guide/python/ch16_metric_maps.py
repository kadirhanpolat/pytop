# %% [markdown]
"""
# Bölüm 16 — Metrik Fonksiyonlar ve Sözleşmeler

Bu bölümde metrik uzaylar arasındaki fonksiyon türleri (izometri, Lipschitz, sürekli)
ve bunların sınıflandırılması incelenmektedir.
"""

# %% [markdown]
"""
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
"""

# %% [markdown]
"""
> **Neden bu konu?** Büzülme dönüşümleri (contraction) ve Lipschitz koşulları sabit nokta teoremlerinin temelidir.

> 🔍 **Kendin dene:** Banach sabit nokta teoremini küçük tam metrik uzayda verify edin.

> ⚠️ **Sık hata:** Uniform süreklilik süreklilikten güçlüdür; uniform `True` iken `continuous False` olamaz ama tersi mümkün.

> ↗️ **Bkz.:** Bölüm 10 (süreklilik), Bölüm 15 (tamlık — Banach için gerekli).

> 💭 **Öz-yansıtma:** Lipschitz sabiti neden < 1 olmalı Banach için?
"""

# %% [markdown]
"""
## 2. Teoremler

**Teorem 2.1.** İzometri ⟹ homeomorfizma. (Bijektif izometri bir homeomorfizma.)

**Teorem 2.2.** Benzerlik: c=1 ⟹ İzometri.

**Teorem 2.3.** Lipschitz ⟹ Üniform sürekli ⟹ Sürekli.
*(Kanıt: δ=ε/K alarak Lipschitz → ünif. süreklilik; her nokta için lokal olarak.)*

**Teorem 2.4.** Kompakt metrik uzaydan metrik uzaya her sürekli fonksiyon
üniform süreklidir.
"""

# %% [markdown]
"""
## 3. Algoritmalar

### classify_finite_metric_map — O(|X|²)

    ClassifyMap(X, d₁, Y, d₂, f):
        K ← 0
        isometry ← True
        similarity_ratio ← None

        for each pair (x1, x2) with x1 ≠ x2:
            ratio ← d₂(f(x1),f(x2)) / d₁(x1,x2)
            K ← max(K, ratio)
            if d₂(f(x1),f(x2)) ≠ d₁(x1,x2): isometry ← False
            if similarity_ratio is None: similarity_ratio ← ratio
            elif ratio ≠ similarity_ratio: similarity_ratio ← None  # sabit değil

        return MetricMapProfile(lipschitz_constant=K, isometry=isometry, ...)

Karmaşıklık: O(|X|²).
"""

# %% [markdown]
"""
## 4. pytop API
"""

# %%
from pytop.metric_spaces import FiniteMetricSpace
from pytop.metric_map_taxonomy import (
    classify_finite_metric_map,
    metric_map_profile,
    MetricMapProfile,
)

# %% [markdown]
"""
## 5. Örnekler

### Örnek 5.1 — Özdeşlik Fonksiyonu: İzometri ✓
"""

# %%
pts = [1, 2, 3, 4]
dist_disc = {(a, b): (0 if a == b else 1) for a in pts for b in pts}
fms = FiniteMetricSpace(carrier=tuple(pts), distance=dist_disc)

f_id = {1: 1, 2: 2, 3: 3, 4: 4}
prof_id = classify_finite_metric_map(fms, fms, f_id)

print("=== Ornek 5.1: Ozdeslik ===")
print("isometry:", prof_id.isometry)
print("lipschitz_constant:", prof_id.lipschitz_constant)
print("similarity:", prof_id.similarity)
print()

# %% [markdown]
"""
### Örnek 5.2 — 2× Ölçekleme: Benzerlik ✓, İzometri ✗
"""

# %%
pts2 = [2, 4, 6, 8]
dist_eucl1 = {(a, b): abs(a - b) for a in pts for b in pts}
dist_eucl2 = {(a, b): abs(a - b) for a in pts2 for b in pts2}
fms_line1 = FiniteMetricSpace(carrier=tuple(pts), distance=dist_eucl1)
fms_line2 = FiniteMetricSpace(carrier=tuple(pts2), distance=dist_eucl2)

f_scale = {1: 2, 2: 4, 3: 6, 4: 8}
prof_scale = classify_finite_metric_map(fms_line1, fms_line2, f_scale)

print("=== Ornek 5.2: 2x Olcekleme ===")
print("isometry:", prof_scale.isometry)
print("similarity:", prof_scale.similarity)
print("similarity_ratio:", prof_scale.similarity_ratio)
print("lipschitz_constant:", prof_scale.lipschitz_constant)
print()

# %% [markdown]
"""
### Örnek 5.3 — Sabit Fonksiyon: Lipschitz K=0, İzometri ✗
"""

# %%
f_const = {1: 1, 2: 1, 3: 1, 4: 1}
prof_const = classify_finite_metric_map(fms, fms, f_const)

print("=== Ornek 5.3: Sabit Fonksiyon f=1 ===")
print("isometry:", prof_const.isometry)
print("lipschitz_constant:", prof_const.lipschitz_constant)
print("non_expansive:", prof_const.non_expansive)
print("bijective:", prof_const.bijective)
print()
# Sabit fonksiyon: K=0 (en kucuk Lipschitz sabiti), genislemez, ama bijektif degil.

# %% [markdown]
"""
### Örnek 5.4 — MetricMapProfile Alanları
"""

# %%
print("=== Ornek 5.4: Profile Alanlari ===")
p = prof_id
print("name:", p.name)
print("certification:", p.certification)
print("non_expansive:", p.non_expansive)
print("lipschitz:", p.lipschitz)
print("uniformly_continuous:", p.uniformly_continuous)
print("continuous:", p.continuous)
print("isometry:", p.isometry)
print("homeomorphism:", p.homeomorphism)
print()

# %% [markdown]
"""
### Örnek 5.5 — Karşılaştırma: İzometri vs Benzerlik
"""

# %%
print("=== Ornek 5.5: Karsılastirma ===")
print("Ozdeslik lipschitz:", prof_id.lipschitz_constant,
      "| isometry:", prof_id.isometry,
      "| similarity_ratio:", prof_id.similarity_ratio)
print("2x scaling lipschitz:", prof_scale.lipschitz_constant,
      "| isometry:", prof_scale.isometry,
      "| similarity_ratio:", prof_scale.similarity_ratio)
print("Sabit lipschitz:", prof_const.lipschitz_constant,
      "| isometry:", prof_const.isometry)
print()
# Ozdeslik: K=1, izometri=True, ratio=1.0
# 2x scaling: K=2, izometri=False, similarity=True, ratio=2.0
# Sabit: K=0, izometri=False, bijective=False

# %% [markdown]
"""
## 6. Alıştırmalar

### Kodlama

K1. {1,2,3} üzerinde f(1)=2, f(2)=3, f(3)=1 (döngü) fonksiyonunu ayrık metrikte
    classify_finite_metric_map ile sınıflandırın.

K2. Öklid metrikli {0,1,2,3,4} uzayında f(x) = x+1 (modüler değil, 4'e kadar) gibi
    bir kaydırma fonksiyonu tanımlayın. Lipschitz sabitini hesaplayın.

K3. Bir ezme (contracting) fonksiyon tanımlayın: f(x) = 1 (sabit). Lipschitz sabitinin
    0 olduğunu doğrulayın.

### Teori

T1. İzometri ⟹ genişlemez ⟹ Lipschitz (K=1) zincirini ispatlayın.

T2. Lipschitz ⟹ üniform sürekli olduğunu δ=ε/K seçimi ile ispatlayın.
"""

if __name__ == "__main__":
    print("pytop Kullanim Kilavuzu — Bolum 9: Metrik Fonksiyonlar")
    print("=" * 55)
