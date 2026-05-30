# %% [markdown]
"""
# Bölüm 5 — Bağlantılılık

Bağlantılılık, bir topolojik uzayın iki ayrı açık parçaya bölünememesi özelliğidir.
Yol-bağlantılılık daha güçlü bir kavramdır ve sürekli yolların varlığına dayanır.
"""

# %% [markdown]
"""
## 1. Konu

### Bağlantılılık Kavramları

| Kavram | Tanım |
|--------|-------|
| **Bağlantılı (connected)** | X = U ∪ V, U∩V = ∅, U,V açık ⟹ U=∅ veya V=∅ |
| **Yol-bağlantılı (path-connected)** | ∀ x,y ∈ X: ∃ sürekli f:[0,1]→X, f(0)=x, f(1)=y |
| **Ark-bağlantılı (arc-connected)** | Yol-bağlantılı, üstelik yollar enjektif |
| **Lokal bağlantılı** | Her noktanın bağlantılı komşulukları var |
| **Tamamen bağlantısız** | Her bağlantılı alt küme tek-noktadır |

**Sıralama:** Ark-bağlantılı ⟹ Yol-bağlantılı ⟹ Bağlantılı.
Tersi genel olarak doğru değildir.

### Clopen Ayrılma

X bağlantısız ⟺ boş olmayan trivial olmayan bir clopen A ⊆ X vardır.
"""

# %% [markdown]
"""
## 2. Teoremler

**Teorem 2.1.** Bağlantılı küme süreklilik altında bağlantılıdır:
f: X → Y sürekli, X bağlantılı ⟹ f(X) bağlantılı.

**Teorem 2.2.** Yol-bağlantılı ⟹ bağlantılı. Tersi genel olarak yanlış.
(Karşı örnek: Topolojist sinüs eğrisi — bağlantılı ama yol-bağlantısız.)

**Teorem 2.3 (Ara Değer Teoremi).** f: X → ℝ sürekli, X bağlantılı, a,b ∈ f(X) ise
her c ∈ [a,b] için f⁻¹(c) ≠ ∅.

**Teorem 2.4.** Gerçek doğru ℝ'de bağlantılı alt kümeler tam olarak aralıklardır.
"""

# %% [markdown]
"""
## 3. Algoritmalar

### Sonlu Bağlantılılık (Clopen Arama)

    BağlıMı(X, τ):
        for each non-empty A ⊊ X:
            if A açık (A ∈ τ) and X∖A açık (X∖A ∈ τ):
                return False   # A clopen bölme bulundu
        return True

Karmaşıklık: O(|τ|²) — clopen küme taraması.

### Yol-Bağlantılılık → Ark-Bağlantılılık Redüksiyonu

Yerel yol-bağlantılı Hausdorff uzaylarda yol-bağlantılı ⟺ ark-bağlantılı.
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
    make_topology,
    real_line_metric,
    closed_unit_interval_metric,
    naturals_cofinite,
    is_connected,
    is_path_connected,
    is_locally_connected,
    is_totally_disconnected,
)
try:
    from pytop import is_arc_connected
except ImportError:
    is_arc_connected = None

# %% [markdown]
"""
## 5. Örnekler

### Örnek 5.1 — Sierpiński: Bağlantılı ✓
"""

# %%
s = sierpinski_space()
print("=== Ornek 5.1: Sierpinski ===")
print("connected?      ", is_connected(s).status)
print("path_connected? ", is_path_connected(s).status)
print()
# Sierpinski baglantilidır: {0,1} iki open parcaya bolunmez
# (sadece {1} acik; {0} ise kapali ancak acik degil).

# %% [markdown]
"""
### Örnek 5.2 — Ayrık Topoloji: Bağlantısız
"""

# %%
d = discrete_topology(1, 2, 3)
print("=== Ornek 5.2: Discrete{1,2,3} ===")
print("connected?         ", is_connected(d).status)
print("totally_disconn?   ", is_totally_disconnected(d).status)
print()
# Ayrik: her tekil kume hem acik hem kapali — {1} clopen bolme gosteriyor.
# Tamamen baglantisiz: her baglantili alt kume tek noktalidir.

# %% [markdown]
"""
### Örnek 5.3 — İndirgenmiş: Her Zaman Bağlantılı
"""

# %%
ind = indiscrete_topology('a', 'b')
print("=== Ornek 5.3: Indiscrete{a,b} ===")
print("connected? ", is_connected(ind).status)
print()
# Indiscrete: sadece bos kume ve X acik; clopen bolme yok.

# %% [markdown]
"""
### Örnek 5.4 — Gerçek Doğru ve [0,1]
"""

# %%
rl = real_line_metric()
ui = closed_unit_interval_metric()
print("=== Ornek 5.4: Gercek Dogru ve [0,1] ===")
print("R connected?         ", is_connected(rl).status)
print("R path_connected?    ", is_path_connected(rl).status)
print("[0,1] connected?     ", is_connected(ui).status)
print("[0,1] path_connected?", is_path_connected(ui).status)
print()

# %% [markdown]
"""
### Örnek 5.5 — Bağlantılı Ama Yol-Bağlantısız Değil: Kosonlu Topoloji
"""

# %%
nc = naturals_cofinite()
print("=== Ornek 5.5: Naturals Cofinite ===")
print("connected?      ", is_connected(nc).status)
print("path_connected? ", is_path_connected(nc).status)
print()

# %% [markdown]
"""
### Örnek 5.6 — Lokal Bağlantılılık
"""

# %%
print("=== Ornek 5.6: Lokal Baglantililik ===")
print("Sierpinski locally_connected? ", is_locally_connected(s).status)
print("Discrete locally_connected?   ", is_locally_connected(d).status)
print("R locally_connected?          ", is_locally_connected(rl).status)
print()

# %% [markdown]
"""
## 6. Alıştırmalar

### Kodlama

K1. make_topology({1,2,3},{1},{2,3}) topolojisi için is_connected hesaplayın.
    {1} ve {2,3} clopen bölme gösteriyor mu?

K2. finite_chain_space(4) zincirinin bağlantılı olup olmadığını kontrol edin.

K3. two_point_discrete_space() ve two_point_indiscrete_space() üzerinde is_connected,
    is_path_connected karşılaştırın.

### Teori

T1. Bağlantılı + sürekli ⟹ görüntü bağlantılı teoremini ispatlayın.

T2. Yol-bağlantılı ⟹ bağlantılı implicasyonunu ispatlayın.
"""

if __name__ == "__main__":
    print("pytop Kullanim Kilavuzu — Bolum 5: Baglantililik")
    print("=" * 50)
