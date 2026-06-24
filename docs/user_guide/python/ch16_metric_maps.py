# %% [markdown]
"""
# Bölüm 16 — Metrik Fonksiyonlar ve Sözleşmeler

Bu bölümde metrik uzaylar arasındaki fonksiyon türleri (izometri, Lipschitz, sürekli)
ve bunların sınıflandırılması incelenmektedir.

---
"""

# %% [markdown]
"""
## 1. Konu
"""

# %% [markdown]
"""
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

![İzometri: f, x ile y arasındaki mesafeyi korur — d₂(f(x),f(y)) = d₁(x,y).](../assets/ch16/fig_ch16_izometri.png)

> 💡 **Sezgi:** Bir izometriyi, bir kâğıt parçasını **buruşturmadan ve germeden**
> başka bir yere taşıyan bir hareket gibi düşünün: döndürebilir, kaydırabilir,
> yansıtabilirsiniz, ama iki nokta arasındaki mesafe asla değişmez. Düzlemde
> öteleme, dönme ve yansıma izometridir. Benzerlik ise kâğıdı oranını koruyarak
> büyüten/küçülten bir fotokopi makinesidir (c=2 → her mesafe iki katına çıkar);
> c=1 alındığında benzerlik tekrar izometriye iner.
"""

# %% [markdown]
"""
### Lipschitz Sabiti

    K = sup_{x≠y} d₂(f(x),f(y)) / d₁(x,y)

İzometri: K=1 ve eşitlik; benzerlik: K=c sabit.

![Büzülme: K<1 olduğunda f, noktaları birbirine yaklaştırır — d₂(f(x),f(y)) ≤ k·d₁(x,y).](../assets/ch16/fig_ch16_buzulme.png)

> 💡 **Sezgi:** Lipschitz sabiti K, fonksiyonun "en dik eğimi" gibidir: hiçbir
> nokta çiftinde mesafeyi K katından fazla büyütemez. K<1 olduğunda her adımda
> mesafe **kesin** olarak küçülür — buna **büzülme (contraction)** denir. Büzülme
> bir haritayı tekrar tekrar uyguladığınızda, tüm noktalar tek bir noktaya
> (sabit noktaya) doğru hunilenir; Banach sabit-nokta teoreminin kalbi budur.

![Düzgün süreklilik: aynı δ tüm noktalarda iş görür (ε önceden verildiğinde).](../assets/ch16/fig_ch16_duzgun_sureklilik.png)

> ❌ **Karşı-örnek:** Her sürekli fonksiyon düzgün (üniform) sürekli **değildir**.
> ℝ⁺ üzerinde `f(x) = 1/x` süreklidir, ama düzgün sürekli değildir: x sıfıra
> yaklaştıkça eğim sınırsız diklenir, bu yüzden verilen bir ε için **tek** bir δ
> bütün noktalarda iş göremez (`x=0.001` civarında çok küçük bir δ gerekirken
> `x=10` civarında çok daha büyüğü yeterlidir). Aynı şekilde ℝ üzerinde
> `f(x) = x²` süreklidir ama düzgün sürekli değildir. Düzgün süreklilik δ'nın
> **noktadan bağımsız** seçilebilmesini ister; Lipschitz fonksiyonlar bunu
> δ=ε/K ile otomatik sağlar.

> **Neden bu konu?** Büzülme dönüşümleri (contraction) ve Lipschitz koşulları sabit nokta teoremlerinin temelidir.

> 🔍 **Kendin dene:** Banach sabit nokta teoremini küçük tam metrik uzayda verify edin.

> ⚠️ **Sık hata:** Uniform süreklilik süreklilikten güçlüdür; uniform `True` iken `continuous False` olamaz ama tersi mümkün.

> ↗️ **Bkz.:** Bölüm 10 (süreklilik), Bölüm 15 (tamlık — Banach için gerekli).

> 💭 **Öz-yansıtma:** Lipschitz sabiti neden < 1 olmalı Banach için?

---
"""

# %% [markdown]
"""
## 2. Teoremler

**Teorem 2.1.** İzometri ⟹ homeomorfizma. (Bijektif izometri bir homeomorfizma.)

> **İspat eskizi.** Önce **injektiflik**: f bir izometri ve f(x)=f(y) olsun. O
> zaman `d₁(x,y) = d₂(f(x),f(y)) = d₂(f(x),f(x)) = 0`, dolayısıyla metriğin
> ayırma aksiyomundan x=y. Demek ki izometri **daima injektiftir**. Bijektif
> kabul edersek f⁻¹ vardır ve o da bir izometridir (`d₁(f⁻¹u,f⁻¹v) = d₂(u,v)`).
> İzometri her mesafeyi koruduğu için ε-δ sürekliliğini δ=ε ile sağlar: hem f
> hem f⁻¹ süreklidir. Bijektif + sürekli + sürekli ters = homeomorfizma. ∎

**Teorem 2.2.** Benzerlik: c=1 ⟹ İzometri.

**Teorem 2.3.** Lipschitz ⟹ Üniform sürekli ⟹ Sürekli.

> **İspat eskizi.** f, sabiti K>0 olan bir Lipschitz fonksiyon olsun:
> `d₂(f(x),f(y)) ≤ K·d₁(x,y)`. Verilen herhangi bir ε>0 için **δ = ε/K** seçin.
> O zaman `d₁(x,y) < δ` olduğunda `d₂(f(x),f(y)) ≤ K·d₁(x,y) < K·(ε/K) = ε`.
> Seçilen δ yalnızca ε ve K'ye bağlıdır, x noktasına bağlı **değildir** —
> dolayısıyla f düzgün (üniform) süreklidir. Düzgün süreklilik özel olarak her
> noktada (lokal) sürekliliği de içerir, dolayısıyla f süreklidir. ∎

**Teorem 2.4.** Kompakt metrik uzaydan metrik uzaya her sürekli fonksiyon
üniform süreklidir.

---
"""

# %% [markdown]
"""
## 3. Algoritmalar
"""

# %% [markdown]
"""
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
`classify_finite_metric_map(fms1, fms2, f)` → `MetricMapProfile` döner (Result değil).

`MetricMapProfile` alanları: `isometry`, `similarity`, `similarity_ratio`,
`lipschitz_constant`, `non_expansive`, `bijective`, `lipschitz`, `continuous`,
`uniformly_continuous`, `homeomorphism`, `name`, `certification`.

---
"""

# %% [markdown]
"""
## 5. Örnekler
"""

# %% [markdown]
"""
### Örnek 5.1 — Özdeşlik Fonksiyonu: İzometri
"""

# %%
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

# %% [markdown]
"""
```text
isometry: True
lipschitz_constant: 1.0
similarity: True
```
"""

# %% [markdown]
"""
### Örnek 5.2 — 2× Ölçekleme: Benzerlik, İzometri ✗
"""

# %%
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

# %% [markdown]
"""
```text
isometry: False
similarity: True
similarity_ratio: 2.0
lipschitz_constant: 2.0
```
"""

# %% [markdown]
"""
### Örnek 5.3 — Sabit Fonksiyon: Lipschitz K=0
"""

# %%
f_const = {1: 1, 2: 1, 3: 1, 4: 1}
prof_const = classify_finite_metric_map(fms, fms, f_const)

print("isometry:", prof_const.isometry)
print("lipschitz_constant:", prof_const.lipschitz_constant)
print("non_expansive:", prof_const.non_expansive)
print("bijective:", prof_const.bijective)

# %% [markdown]
"""
```text
isometry: False
lipschitz_constant: 0.0
non_expansive: True
bijective: False
```

Sabit fonksiyon: K=0 (en küçük Lipschitz sabiti), genişlemez, ama bijektif değil.
"""

# %% [markdown]
"""
### Örnek 5.4 — MetricMapProfile Alanları
"""

# %%
p = prof_id
print("name:", p.name)
print("certification:", p.certification)
print("non_expansive:", p.non_expansive)
print("lipschitz:", p.lipschitz)
print("uniformly_continuous:", p.uniformly_continuous)
print("continuous:", p.continuous)
print("isometry:", p.isometry)
print("homeomorphism:", p.homeomorphism)

# %% [markdown]
"""
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
"""

# %% [markdown]
"""
### Örnek 5.5 — Karşılaştırma: İzometri vs Benzerlik
"""

# %%
print("Ozdeslik  K:", prof_id.lipschitz_constant,
      "| isometry:", prof_id.isometry,
      "| ratio:", prof_id.similarity_ratio)
print("2x scale  K:", prof_scale.lipschitz_constant,
      "| isometry:", prof_scale.isometry,
      "| ratio:", prof_scale.similarity_ratio)
print("Sabit     K:", prof_const.lipschitz_constant,
      "| isometry:", prof_const.isometry)

# %% [markdown]
"""
```text
Ozdeslik  K: 1.0 | isometry: True | ratio: 1.0
2x scale  K: 2.0 | isometry: False | ratio: 2.0
Sabit     K: 0.0 | isometry: False
```
"""

# %% [markdown]
"""
### Örnek 5.6 — Büzülme (Contraction): K = 1/2

Öklid doğrusu üzerinde her mesafeyi yarıya indiren `f(x) = x/2` türünden bir
eşleme tanımlayalım. Bu bir **büzülmedir** (K<1): Banach teoreminin gerektirdiği
sözleşme koşulunu sağlar.
"""

# %%
from pytop.metric_spaces import FiniteMetricSpace
from pytop.metric_map_taxonomy import classify_finite_metric_map

src = [0, 2, 4, 6]
img = [0, 1, 2, 3]
d_src = {(a, b): abs(a - b) for a in src for b in src}
d_img = {(a, b): abs(a - b) for a in img for b in img}
M_src = FiniteMetricSpace(carrier=tuple(src), distance=d_src)
M_img = FiniteMetricSpace(carrier=tuple(img), distance=d_img)

f_half = {0: 0, 2: 1, 4: 2, 6: 3}
prof_half = classify_finite_metric_map(M_src, M_img, f_half)

print("lipschitz_constant:", prof_half.lipschitz_constant)
print("non_expansive:", prof_half.non_expansive)
print("similarity:", prof_half.similarity)
print("similarity_ratio:", prof_half.similarity_ratio)
print("isometry:", prof_half.isometry)
print("uniformly_continuous:", prof_half.uniformly_continuous)

# %% [markdown]
"""
```text
lipschitz_constant: 0.5
non_expansive: True
similarity: True
similarity_ratio: 0.5
isometry: False
uniformly_continuous: True
```

K = 0.5 < 1: büzülme. Her mesafe tam yarıya indiği için aynı zamanda
oran c=0.5 olan bir benzerliktir. İzometri değildir (mesafeleri korumaz), ama
genişlemez ve (Lipschitz olduğundan) üniform süreklidir.
"""

# %% [markdown]
"""
### Örnek 5.7 — Ayrık Metrikte Döngü: İzometri ve Homeomorfizma

Ayrık metrikte (farklı noktalar arası mesafe daima 1) bir **permütasyon**
herhangi iki nokta arası mesafeyi değiştiremez: her bijeksiyon bir izometridir.
{1,2,3} üzerinde döngü f(1)=2, f(2)=3, f(3)=1'i sınıflandıralım.
"""

# %%
from pytop.metric_spaces import FiniteMetricSpace
from pytop.metric_map_taxonomy import classify_finite_metric_map

dp = [1, 2, 3]
d_disc = {(a, b): (0 if a == b else 1) for a in dp for b in dp}
M_disc = FiniteMetricSpace(carrier=tuple(dp), distance=d_disc)

f_cycle = {1: 2, 2: 3, 3: 1}
prof_cycle = classify_finite_metric_map(M_disc, M_disc, f_cycle)

print("isometry:", prof_cycle.isometry)
print("bijective:", prof_cycle.bijective)
print("homeomorphism:", prof_cycle.homeomorphism)
print("lipschitz_constant:", prof_cycle.lipschitz_constant)

# %% [markdown]
"""
```text
isometry: True
bijective: True
homeomorphism: True
lipschitz_constant: 1.0
```

Döngü bir bijeksiyon ve ayrık metrikte izometridir (K=1, mesafe korunur);
Teorem 2.1 gereği bijektif izometri olarak bir homeomorfizmadır.

---
"""

# %% [markdown]
"""
## 6. Alıştırmalar
"""

# %% [markdown]
"""
### Kodlama

K1. {1,2,3} üzerinde f(1)=2, f(2)=3, f(3)=1 (döngü) fonksiyonunu ayrık metrikte
    `classify_finite_metric_map` ile sınıflandırın.

K2. Öklid metrikli {0,1,2,3,4} uzayında f(x) = x+1 (4'e kadar) gibi bir kaydırma
    fonksiyonu tanımlayın. Lipschitz sabitini hesaplayın.

K3. Bir ezme (contracting) fonksiyon tanımlayın: f(x) = 1 (sabit). Lipschitz
    sabitinin 0 olduğunu doğrulayın.

K4. Öklid doğrusunda {0,2,4,6} → {0,1,2,3} büzülmesini (f(x)=x/2) kurun ve
    `lipschitz_constant`, `similarity_ratio`, `non_expansive` alanlarını yazdırın.
    Lipschitz sabitinin 1'den küçük olduğunu doğrulayın.

K5. {1,2,3} üzerinde **özdeşlik olmayan** bir döngü permütasyonunu hem ayrık
    metrikte hem de Öklid (mesafe = |a−b|) metrikte sınıflandırın. Hangi metrikte
    izometri olur, hangisinde olmaz? `isometry` alanlarını karşılaştırın.
"""

# %% [markdown]
"""
### Teori

T1. İzometri ⟹ genişlemez ⟹ Lipschitz (K=1) zincirini ispatlayın.

T2. Lipschitz ⟹ üniform sürekli olduğunu δ=ε/K seçimi ile ispatlayın.

T3. İzometrinin daima injektif olduğunu ispatlayın. (İpucu: f(x)=f(y) ise
    d₂(f(x),f(y))=0; izometri eşitliğini ve metriğin ayırma aksiyomunu kullanın.)
    Ardından düzlemde sabit (constant) bir fonksiyonun neden izometri olamadığını
    açıklayın.
```
"""
