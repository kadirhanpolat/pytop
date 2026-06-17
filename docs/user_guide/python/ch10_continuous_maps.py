# %% [markdown]
"""
# Bölüm 10 — Sürekli Fonksiyonlar ve Homeomorfizmalar

Topolojik uzaylar arasındaki fonksiyonlarda süreklilik, açık kümelerin
geri çekiminin (preimage) açık olması koşuluna dayanır. Homeomorfizma ise
topolojik yapıyı tam olarak koruyan bijektif sürekli fonksiyondur.
"""

# %% [markdown]
"""
## 1. Konu

### Süreklilik Tanımı

f: (X, τ_X) → (Y, τ_Y) fonksiyonu **sürekli** ise:
Her V ∈ τ_Y (açık küme) için f⁻¹(V) ∈ τ_X.

Eşdeğer koşullar:
- Her x ∈ X ve f(x)'in her komşuluğu W için f⁻¹(W) x'in komşuluğudur.
- Her kapalı F ⊆ Y için f⁻¹(F) kapalıdır.

### Süreklilik Hiyerarşisi

| Tür | Koşul |
|-----|-------|
| **Sabit fonksiyon** | f(x) = c; her zaman sürekli |
| **Özdeşlik** | f(x) = x; her zaman sürekli |
| **Bileşke** | f, g sürekli ⟹ g∘f sürekli |
| **Homeomorfizma** | Bijektif, f ve f⁻¹ sürekli |

### Görüntü ve Geri Çekim

- **Görüntü (image):** f(A) = {f(x) : x ∈ A}
- **Geri çekim (preimage):** f⁻¹(B) = {x ∈ X : f(x) ∈ B}

Süreklilik: açık kümenin geri çekimi açıktır.
Sürekli f: geri-çekim işlemi topoloji yapısını korur.
"""

# %% [markdown]
"""
> **Neden bu konu?** Süreklilik topolojinin temel kavramı; homeomorfizma yapı-koruma denkliğidir.

> 🔍 **Kendin dene:** Sierpiński → Sierpiński'ye kaç fonksiyon var, kaçı sürekli? `is_continuous_finite_map` ile tek tek test edin.

> ⚠️ **Sık hata:** `s_topo = list(s.topology)` kullanın; `[set(u) for u in s.topology]` gerekmez — `is_continuous_finite_map` `Iterable[Iterable]` kabul eder.

> ↗️ **Bkz.:** Bölüm 7 (kompakt görüntü kompakt), Bölüm 8 (bağlantılı görüntü bağlantılı).

> 💭 **Öz-yansıtma:** Homeomorfizma ile izomorfizma arasındaki fark ne? Hangi yapıyı korur?
"""

# %% [markdown]
"""
## 2. Teoremler

**Teorem 2.1.** Her sabit fonksiyon süreklidir.
*(Kanıt: f⁻¹(V) = X eğer c ∈ V, ∅ eğer c ∉ V; her ikisi de açık.)*

**Teorem 2.2.** f: X → Y ve g: Y → Z sürekli ⟹ g∘f sürekli.

**Teorem 2.3.** f: X → Y sürekli, X kompakt ⟹ f(X) kompakttır.

**Teorem 2.4.** f: X → Y sürekli, X bağlantılı ⟹ f(X) bağlantılıdır.

**Teorem 2.5.** f: X → Y homeomorfizma ⟺
bijektif, f sürekli, f⁻¹ sürekli.

**Teorem 2.6.** f: X → Y kompakt X'ten Hausdorff Y'ye sürekli bijeksiyon ⟹ homeomorfizma.
"""

# %% [markdown]
"""
## 3. Algoritmalar

### is_continuous_finite_map — O(|τ_Y| · |X|)

    IsContinuous(X, τ_X, Y, τ_Y, f):
        for each V in τ_Y:
            preimage ← {x ∈ X : f(x) ∈ V}
            if preimage not in τ_X: return False
        return True

Karmaşıklık: O(|τ_Y| · |X|) — her açık küme için geri çekim.

### finite_homeomorphism_result — O(|τ|²)

Önce bijektiflik, sonra her iki yönde süreklilik kontrol edilir.
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
    make_set,
    empty_set,
    real_line_metric,
    closed_unit_interval_metric,
    is_continuous_finite_map,
    finite_homeomorphism_result,
)

# %% [markdown]
"""
## 5. Örnekler

### Örnek 5.1 — Sabit Fonksiyon: Her Zaman Sürekli
"""

# %%
s = sierpinski_space()
s_pts = list(s.carrier)
s_topo = list(s.topology)

f_const = {0: 1, 1: 1}   # her seyi 1'e gonder
result = is_continuous_finite_map(s_pts, s_topo, s_pts, s_topo, f_const)
print("=== Ornek 5.1: Sabit f(x)=1 ===")
print("continuous:", result)
print()
# Sabit fonksiyon her zaman sureklidir:
# f^-1(V) ya X ya da bos kume -- ikisi de acik.

# %% [markdown]
"""
### Örnek 5.2 — Özdeşlik ve Swap: Ayrık Topoloji
"""

# %%
d = discrete_topology(0, 1)
d_pts = list(d.carrier)
d_topo = list(d.topology)

f_id   = {0: 0, 1: 1}
f_swap = {0: 1, 1: 0}

print("=== Ornek 5.2: Ayrik Topoloji ===")
print("ozdeslik continuous:", is_continuous_finite_map(d_pts, d_topo, d_pts, d_topo, f_id))
print("swap     continuous:", is_continuous_finite_map(d_pts, d_topo, d_pts, d_topo, f_swap))
print()
# Ayrik topolojide her fonksiyon sureklidir:
# geri cekim her zaman acik (ayrik topolojide her kume acik).

# %% [markdown]
"""
### Örnek 5.3 — Sierpiński → Ayrık: Sürekli Değil
"""

# %%
print("=== Ornek 5.3: Sierpinski -> Ayrik ===")
# Ozdeslik: Sierpinski -> Discrete
cont_sd = is_continuous_finite_map(s_pts, s_topo, d_pts, d_topo, f_id)
print("id: Sierpinski -> Disc continuous:", cont_sd)

# Ozdeslik: Discrete -> Sierpinski
cont_ds = is_continuous_finite_map(d_pts, d_topo, s_pts, s_topo, f_id)
print("id: Disc -> Sierpinski continuous:", cont_ds)
print()
# Sierpinski tau = {bos, {0,1}, {1}}
# id: Sier->Disc: f^-1({0}) = {0} -- Sierpinski'de acik degil! -> surekli degil.
# id: Disc->Sier: f^-1({1}) = {1} acik, f^-1({0,1}) = {0,1} acik -> surekli.

# %% [markdown]
"""
### Örnek 5.4 — Indiscrete → Herhangi: Her Zaman Sürekli
"""

# %%
ind = indiscrete_topology(0, 1)
ind_pts = list(ind.carrier)
ind_topo = list(ind.topology)

f_const0 = {0: 0, 1: 0}   # sabit 0 fonksiyonu
print("=== Ornek 5.4: Indiscrete -> Sierpinski ===")
cont_id   = is_continuous_finite_map(ind_pts, ind_topo, s_pts, s_topo, f_id)
cont_c0   = is_continuous_finite_map(ind_pts, ind_topo, s_pts, s_topo, f_const0)
print("id (0->0, 1->1) continuous:", cont_id)
print("const_0 (tum->0) continuous:", cont_c0)
print()
# Indiscrete'den sureklilik icin f^-1(V) in {bos, X} olmali.
# f_id: f^-1({1}) = {1} -- {1} ∉ {bos,{0,1}} -> surekli DEGIL.
# f_const0: f^-1({1}) = bos ∈ {bos,{0,1}} -> surekli.

# %% [markdown]
"""
### Örnek 5.5 — Homeomorfizma Kontrolü
"""

# %%
d2a = discrete_topology(1, 2)
d2b = discrete_topology('a', 'b')
ind2 = indiscrete_topology(1, 2)

print("=== Ornek 5.5: Homeomorfizma ===")
print("D(1,2) ~ D(a,b):", finite_homeomorphism_result(d2a, d2b).status)
print("D(1,2) ~ S(0,1):", finite_homeomorphism_result(d2a, s).status)
print("D(1,2) ~ Ind(1,2):", finite_homeomorphism_result(d2a, ind2).status)
print()
# D(1,2) ~ D(a,b): evet, ayni boyutta ayrik -> homeomorf.
# D(1,2) ~ Sierpinski: hayir, topolojik ozellikler farkli (T1 vs T0).
# D(1,2) ~ Ind(1,2): hayir, T2 vs T0.

# %% [markdown]
"""
### Örnek 5.6 — Özel Topolojili Süreklilik
"""

# %%
# {1,2,3} uzayi: tau = {bos, {1}, {2,3}, {1,2,3}}
X = [1, 2, 3]
tau_X = [empty_set(), make_set(1), make_set(2, 3), make_set(1, 2, 3)]
# Ayni uzay: f(1)=1, f(2)=3, f(3)=2 -- 2 ve 3'u degistiriyor
f_23swap = {1: 1, 2: 3, 3: 2}

print("=== Ornek 5.6: Ozel Topoloji ===")
cont_swap = is_continuous_finite_map(X, tau_X, X, tau_X, f_23swap)
print("2-3 swap surekli mi:", cont_swap)
# f^-1({2,3}) = {2,3} (acik); f^-1({1}) = {1} (acik) -> surekli.
print()

# %% [markdown]
"""
## 6. Alıştırmalar

### Kodlama

K1. `make_topology({0,1,2}, {0}, {0,1})` ile tanımlanan topolojide
    f(0)=0, f(1)=0, f(2)=1 fonksiyonunun sürekli olup olmadığını kontrol edin.

K2. Sierpiński uzayından kendisine giden dört farklı fonksiyonu test edin:
    hangileri sürekli, hangileri değil?

K3. `finite_homeomorphism_result` ile {1,2,3} ayrık ve {a,b,c} ayrık
    topolojilerinin homeomorf olduğunu doğrulayın.

### Teori

T1. Her sabit fonksiyonun sürekli olduğunu ispatlayın.

T2. f: X → Y ve g: Y → Z sürekli ⟹ g∘f sürekli olduğunu ispatlayın.
"""

if __name__ == "__main__":
    print("pytop Kullanim Kilavuzu — Bolum 10: Surekli Fonksiyonlar")
    print("=" * 55)
