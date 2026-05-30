# %% [markdown]
"""
# Bölüm 3 — Ayrılma Aksiyomları

Ayrılma aksiyomları (T0–T4 ve ötesi), bir topolojik uzaydaki noktaların ve kapalı
kümelerin birbirinden açık kümeler aracılığıyla ne ölçüde "ayrılabildiğini" ölçer.
Her aksiyom bir öncekinden daha güçlüdür.
"""

# %% [markdown]
"""
## 1. Konu

### Ayrılma Aksiyomları Sıralaması

| Aksiyom | İsim | Koşul |
|---------|------|-------|
| T0 | Kolmogorov | ∀ x≠y: ∃ U∈τ, (x∈U, y∉U) veya (y∈U, x∉U) |
| T1 | Fréchet | ∀ x≠y: ∃ U,V∈τ, x∈U∧y∉U, y∈V∧x∉V |
| T2 | Hausdorff | ∀ x≠y: ∃ U,V∈τ, x∈U, y∈V, U∩V=∅ |
| T2.5 | Urysohn | ∀ x≠y: ∃ U,V∈τ, x∈U, y∈V, cl(U)∩cl(V)=∅ |
| T3 | Regüler | T1 + ∀ x, kapalı C ∌ x: ∃ U,V∈τ, x∈U, C⊆V, U∩V=∅ |
| T3.5 | Tychonoff/Tam regüler | T1 + ∀ x, kapalı C ∌ x: ∃f:X→[0,1] sürekli, f(x)=0, f|C=1 |
| T4 | Normal | T1 + ∀ C,D kapalı, C∩D=∅: ∃ U,V∈τ, C⊆U, D⊆V, U∩V=∅ |
| Perfectly normal | — | T4 + kapalı kümeler Gδ |

**Sıralama:** T4 ⟹ T3.5 ⟹ T3 ⟹ T2.5 ⟹ T2 ⟹ T1 ⟹ T0
"""

# %% [markdown]
"""
## 2. Teoremler

**Teorem 2.1 (Ayrılma Zinciri).**
T4 ⟹ T3.5 ⟹ T3 ⟹ T2.5 ⟹ T2 ⟹ T1 ⟹ T0.
Tersi genel olarak doğru değildir.

**Teorem 2.2 (Urysohn Fonksiyon Teoremi).**
X normal (T4) ise ve C, D disjoint kapalı kümeler ise, f: X → [0,1] sürekli bir
fonksiyon vardır: f|C ≡ 0, f|D ≡ 1.

**Teorem 2.3 (Tietze Genişleme Teoremi).**
X normal ise her kapalı A ⊆ X üzerinde tanımlı sürekli f: A → [a,b] fonksiyonu
tüm X'e sürekli olarak genişletilebilir.

**Teorem 2.4 (Tychonoff Karakterizasyonu).**
X, T3.5'tir ⟺ X, [0,1]^I ile homeomorf bir alt uzayı olacak biçimde sürekli
fonksiyonlar X'i ayrıştırır.
"""

# %% [markdown]
"""
## 3. Algoritmalar

### Sonlu Ayrılma Karar Prosedürü

T0 (ve analog olarak T1, T2) için sonlu uzayda:

    KontrolT0(X, τ):
        for each pair (x, y) with x ≠ y:
            if not (∃U∈τ: x∈U∧y∉U or y∈U∧x∉U):
                return False
        return True

Karmaşıklık: O(|X|²·|τ|)

T3 için (regülerlik):

    KontrolT3(X, τ):
        closed ← {X ∖ U : U ∈ τ}
        for each x ∈ X, each C ∈ closed with x ∉ C:
            if not ∃ U,V∈τ: x∈U ∧ C⊆V ∧ U∩V=∅:
                return False
        return True

Karmaşıklık: O(|X|·|τ|²)
"""

# %% [markdown]
"""
## 4. pytop API
"""

# %%
from pytop import (
    sierpinski_space,
    discrete_topology,
    indiscrete_topology,
    naturals_cofinite,
    real_line_metric,
    is_t0, is_t1, is_t2, is_t2_5, is_t3, is_t4,
    is_hausdorff, is_regular, is_normal,
    is_perfectly_normal,
    separation_chain,
    analyze_separation,
)

# %% [markdown]
"""
## 5. Örnekler

### Örnek 5.1 — Sierpiński: T0 ✓, T1 ✗
"""

# %%
s = sierpinski_space()
print("=== Ornek 5.1: Sierpinski ===")
print("T0:", is_t0(s).status)
print("T1:", is_t1(s).status)
print("T2:", is_t2(s).status)
print()
# Sierpinski: T1 degil cunku {0} acik degildir — 0'i yalnizca X ayirir, sadece 1 degil.

# %% [markdown]
"""
### Örnek 5.2 — İndirgenmiş Topoloji: Hiçbir T Aksiyomu Yok
"""

# %%
ind = indiscrete_topology('a', 'b')
print("=== Ornek 5.2: Indiscrete ===")
print("T0:", is_t0(ind).status)
print("T1:", is_t1(ind).status)
print()
# Indiscrete: T0 degil — a ve b'yi ayiran acik kume yok.

# %% [markdown]
"""
### Örnek 5.3 — Kosonlu Doğal Sayılar: T1 ✓, T2 ✗
"""

# %%
nc = naturals_cofinite()
print("=== Ornek 5.3: Naturals Cofinite ===")
print("T0:", is_t0(nc).status)
print("T1:", is_t1(nc).status)
print("T2:", is_t2(nc).status)
print()
# Kosonlu: T1 ama Hausdorff degil — herhangi iki acik kume kesisir.

# %% [markdown]
"""
### Örnek 5.4 — Ayrık Topoloji: Tüm Aksiyomlar ✓
"""

# %%
d = discrete_topology(1, 2, 3)
print("=== Ornek 5.4: Discrete {1,2,3} ===")
chain = separation_chain(d)
for prop, result in chain.items():
    print(f"  {prop:20s}: {result.status}")
print()

# %% [markdown]
"""
### Örnek 5.5 — separation_chain Özet
"""

# %%
print("=== Ornek 5.5: separation_chain ozeti ===")
print("Sierpinski chain:")
for prop, result in separation_chain(s).items():
    print(f"  {prop:20s}: {result.status}")
print()

# %% [markdown]
"""
### Örnek 5.6 — analyze_separation
"""

# %%
print("=== Ornek 5.6: analyze_separation ===")
rl = real_line_metric()
# analyze_separation(space) varsayilan olarak 'hausdorff' ozelligini test eder.
print("Real line Hausdorff mi?:", analyze_separation(rl).status)
print("Discrete Hausdorff mi?:", analyze_separation(d).status)
print("Sierpinski Hausdorff mi?:", analyze_separation(s).status)
print("Sierpinski T0 mu?:", analyze_separation(s, 't0').status)
print()
# status='true'  => uzay bu aksiyomu saglar
# status='false' => uzay bu aksiyomu saglamaz

# %% [markdown]
"""
## 6. Alıştırmalar

### Kodlama

K1. make_topology({1,2,3},{1},{2},{1,2}) üzerinde separation_chain hesaplayın.
    Bu topoloji T0, T1, T2 aksiyomlarından hangilerini sağlıyor?

K2. two_point_indiscrete_space() (examples modülü) üzerinde is_t0, is_t1, is_t2
    sonuçlarını inceleyin. Beklediğinizle uyuşuyor mu?

K3. finite_chain_space(3) üzerinde ayrılma zincirini çalıştırın; hangi aksiyomların
    geçtiğini not edin.

### Teori

T1. T2 ⟹ T1 ⟹ T0 implicasyonlarını formal olarak kanıtlayın.

T2. Bir sonlu uzayda T1 ⟺ ayrık topoloji olduğunu gösterin.
    (İpucu: T1 → her tekil küme kapalı → her küme kapalı → her küme açık.)
"""

if __name__ == "__main__":
    print("pytop Kullanim Kilavuzu — Bolum 3: Ayrilma Aksiyomlari")
    print("=" * 60)
