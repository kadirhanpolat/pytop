# %% [markdown]
"""
# Bölüm 4 — Kompaktlık

Kompaktlık, sonsuz topolojik uzaylarda "sonluluk" gibi davranan temel bir özelliğin
soyutlamasıdır. Her açık örtüyü sonlu bir alt-örtüye indirgemek mümkündür.
"""

# %% [markdown]
"""
## 1. Konu

### Kompaktlık Tanımı

(X, τ) bir topolojik uzay olsun. X **kompakt** ise: X'in her açık örtüsünün sonlu
bir alt-örtüsü vardır.

Yani: {U_α}_α ⊆ τ ve ⋃_α U_α = X ise, sonlu bir {α_1,...,α_n} ⊆ indeks kümesi
vardır: U_{α_1} ∪ ... ∪ U_{α_n} = X.

### Kompaktlık Varyantları

| Kavram | Tanım |
|--------|-------|
| Sayılabilir kompakt | Her sayılabilir açık örtünün sonlu alt-örtüsü var |
| Sıralı kompakt | Her dizi bir yakınsak alt-dizi içerir |
| Lindelöf | Her açık örtünün sayılabilir alt-örtüsü var |
| Lokal kompakt | Her noktanın kompakt bir komşuluğu var |
| σ-kompakt | Sayılabilir kompakt kümelerin birleşimi |
| Metakompakt | Her açık örtünün nokta-sonlu açık inceltmesi var |
| Feebly kompakt | Her sonsuz yerel sonlu açık aile sınırlı |

### Önemli Örnekler

- **Kapalı [a,b] aralığı:** kompakt (Heine-Borel)
- **Açık (a,b) aralığı:** kompakt değil
- **Gerçek doğru ℝ:** kompakt değil ama lokal kompakt
- **Herhangi sonlu uzay:** otomatik kompakt
"""

# %% [markdown]
"""
## 2. Teoremler

**Teorem 2.1 (Heine-Borel).** ℝⁿ'de bir alt küme kompakttır ⟺ kapalı ve sınırlıdır.

**Teorem 2.2 (Bolzano-Weierstrass).** Sınırlı her gerçek sayı dizisinin yakınsak bir
alt-dizisi vardır; metrik kompaktlık ile eşdeğerdir.

**Teorem 2.3.** Kompakt + Hausdorff ⟹ Normal (T4).

**Teorem 2.4 (Tychonoff Çarpım Teoremi).** Herhangi bir ailenin çarpım uzayı
kompakttır ⟺ her bileşen kompakttır.

**Teorem 2.5 (Alexandroff Tek-Nokta Kompaktifikasyonu).**
X lokally kompakt Hausdorff ise, X ∪ {∞} (uygun topolojiyle) kompakt Hausdorff.
"""

# %% [markdown]
"""
## 3. Algoritmalar

### Sonlu Uzayda Kompaktlık

Sonlu uzayda her açık örtü zaten sonludur → otomatik kompakt. Trivial algoritma.

### Alexandroff Tek-Nokta Kompaktifikasyonu

    OnePointCompact(X, τ):
        ∞ ← yeni nokta
        X* ← X ∪ {∞}
        τ* ← τ ∪ {(X* ∖ K) ∪ {∞} : K ⊆ X kapalı kompakt}
        return (X*, τ*)

Karmaşıklık: O(|τ|·|X|) — kompakt kapalı kümeler listelenir.

### is_pseudocompact

Her sürekli gerçel değerli fonksiyonun sınırlı olup olmadığını kontrol eder.
Sonsuz uzayda: metrizable + Lindelöf + non-compact ⟹ pseudocompact değil (teoremle).
"""

# %% [markdown]
"""
## 4. pytop API
"""

# %%
from pytop import (
    sierpinski_space,
    discrete_topology,
    finite_chain_space,
    real_line_metric,
    closed_unit_interval_metric,
    is_compact,
    is_lindelof,
    is_locally_compact,
)
from pytop.compactness_variants import (
    is_countably_compact,
    is_sequentially_compact,
    analyze_compactness_variants,
)

# %% [markdown]
"""
## 5. Örnekler

### Örnek 5.1 — Sonlu Uzay: Her Zaman Kompakt
"""

# %%
s = sierpinski_space()
c = finite_chain_space(3)
d = discrete_topology(1, 2, 3)
print("=== Ornek 5.1: Sonlu Uzaylar ===")
print("Sierpinski compact?     ", is_compact(s).status)
print("Chain(3) compact?       ", is_compact(c).status)
print("Discrete(3) compact?    ", is_compact(d).status)
print()
# Sonlu uzayda her acik ortu sonludur → otomatik kompakt.

# %% [markdown]
"""
### Örnek 5.2 — Gerçek Doğru: Kompakt Değil, Lokal Kompakt ✓
"""

# %%
rl = real_line_metric()
print("=== Ornek 5.2: Gercek Dogru ===")
print("compact?         ", is_compact(rl).status)
print("lindelof?        ", is_lindelof(rl).status)
print("locally_compact? ", is_locally_compact(rl).status)
print()
# R kompakt degil (Z+ ortusu alt-ortuye indirgenmez), ama lokal kompakt
# (her x∈R'in, [x-1,x+1] gibi kompakt bir komşuluğu var).

# %% [markdown]
"""
### Örnek 5.3 — Kapalı Birim Aralığı [0,1]
"""

# %%
ui = closed_unit_interval_metric()
print("=== Ornek 5.3: [0,1] ===")
print("compact?         ", is_compact(ui).status)
print("sequentially?    ", is_sequentially_compact(ui).status)
print("countably?       ", is_countably_compact(ui).status)
print()
# [0,1] kompakt (Heine-Borel), sırali kompakt, sayilabilir kompakt.

# %% [markdown]
"""
### Örnek 5.4 — analyze_compactness_variants: Gerçek Doğru
"""

# %%
print("=== Ornek 5.4: analyze_compactness_variants(R) ===")
r = analyze_compactness_variants(rl)
for key, val in r.value.items():
    if hasattr(val, 'status'):
        print(f"  {key:25s}: {val.status}")
    else:
        print(f"  {key:25s}: {val}")
print()
# Lindelof: true; pseudocompact: false; metacompact: true (metrik => paracompact).

# %% [markdown]
"""
### Örnek 5.5 — Sonlu Uzayda Varyant Analizi
"""

# %%
print("=== Ornek 5.5: analyze_compactness_variants(Sierpinski) ===")
rs = analyze_compactness_variants(s)
for key, val in rs.value.items():
    if hasattr(val, 'status'):
        print(f"  {key:25s}: {val.status}")
    else:
        print(f"  {key:25s}: {val}")
print()

# %% [markdown]
"""
## 6. Alıştırmalar

### Kodlama

K1. naturals_cofinite() uzayının kompaktlık ve Lindelöf özelliklerini test edin.

K2. make_topology({1,2,3,4},{1},{2,3},{4}) topolojisini oluşturun ve is_compact,
    is_locally_compact sonuçlarını inceleyin.

K3. analyze_compactness_variants(closed_unit_interval_metric()) çalıştırın ve
    her varyantın durumunu not edin.

### Teori

T1. Her sonlu uzayın kompakt olduğunu ispatın (T1–T3 aksiyomlarından yola çıkarak).

T2. Heine-Borel teoreminin gerçek doğru ℝ'de uygulamasını açıklayın: [0,1]'in
    kompakt, (0,1)'in kompakt olmadığını gösterin.
"""

if __name__ == "__main__":
    print("pytop Kullanim Kilavuzu — Bolum 4: Kompaktlik")
    print("=" * 50)
