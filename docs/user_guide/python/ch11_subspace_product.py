# %% [markdown]
"""
# Bölüm 11 — Alt Uzay ve Çarpım Topolojisi

Alt uzay topolojisi bir uzayın alt kümesine "miras kalan" topolojiyi tanımlar.
Çarpım topolojisi ise iki veya daha fazla uzayı birleştirerek yeni bir uzay kurar.
"""

# %% [markdown]
"""
## 1. Konu

### Alt Uzay Topolojisi

(X, τ) topolojik uzayı ve A ⊆ X alt kümesi verilsin.
**Alt uzay topolojisi** (göreceli topoloji):

    τ_A = {U ∩ A : U ∈ τ}

(A, τ_A) bir topolojik uzaydır; dahil etme fonksiyonu i: A → X süreklidir.

### Çarpım Topolojisi

(X, τ_X) ve (Y, τ_Y) verilsin. **Çarpım topolojisi** X × Y üzerinde
{U × V : U ∈ τ_X, V ∈ τ_Y} kümesinin oluşturduğu bazdan üretilen topolojidir.

- Çarpım uzayı: (X × Y, τ_{X×Y})
- Projeksiyon π_X: X × Y → X ve π_Y: X × Y → Y süreklidir.
- τ_{X×Y} her iki projektiyonu sürekli kılan en kaba topolojidir.

### Temel Özellikler

| Özellik | Alt uzay | Çarpım |
|---------|----------|--------|
| Hausdorff kalıtımı | ✓ | ✓ |
| Kompaktlık kalıtımı | Kapalı alt uzay | ✓ (Tychonoff) |
| Bağlantılılık kalıtımı | Genel olarak hayır | ✓ |
"""

# %% [markdown]
"""
> **Neden bu konu?** Yeni uzay inşa etmenin üç temel yöntemi; çarpım topolojisi Tychonoff teoreminin temelidir.

> 🔍 **Kendin dene:** `subspace_topology` ile `product_topology`'nin boyutunu karşılaştırın.

> ⚠️ **Sık hata:** Çarpım topolojisi ince topolojidir; {U×V} ailesi baz, topoloji değil.

> ↗️ **Bkz.:** Bölüm 7 (Tychonoff), Bölüm 12 (bölüm = eşdeğerlikten gelen topoloji).

> 💭 **Öz-yansıtma:** Alt-uzay topolojisi orijinal topolojiden neden daha az açık küme içerebilir?
"""

# %% [markdown]
"""
## 2. Teoremler

**Teorem 2.1.** Hausdorff uzayın her alt uzayı Hausdorff'tur.

**Teorem 2.2.** Kompakt uzayın kapalı alt uzayı kompakttır.

**Teorem 2.3.** X ve Y bağlantılı ⟹ X × Y bağlantılıdır.

**Teorem 2.4.** X ve Y kompakt ⟹ X × Y kompakt. (Tychonoff, n=2 durumu)

**Teorem 2.5.** X ve Y Hausdorff ⟹ X × Y Hausdorff.

**Teorem 2.6 (Evrensel Özellik — Çarpım).**
f: Z → X × Y sürekli ⟺ π_X∘f: Z → X ve π_Y∘f: Z → Y her ikisi süreklidir.
"""

# %% [markdown]
"""
## 3. Algoritmalar

### finite_subspace — O(|τ| · |A|)

    Subspace(X, tau, A):
        tau_A ← {}
        for each U in tau:
            tau_A.add(U ∩ A)
        return (A, tau_A)

### binary_product — O(|τ_X| · |τ_Y|)

    Product(X, tau_X, Y, tau_Y):
        basis ← {U x V : U ∈ tau_X, V ∈ tau_Y}
        return topology_from_basis(X x Y, basis)
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
    finite_subspace,
    binary_product,
    is_compact,
    is_connected,
    is_t2,
)

# %% [markdown]
"""
## 5. Örnekler

### Örnek 5.1 — Alt Uzay: Ayrık Topoloji
"""

# %%
d4 = discrete_topology(1, 2, 3, 4)
sub12 = finite_subspace(d4, [1, 2])

print("=== Ornek 5.1: Subspace {1,2} of Disc(1,2,3,4) ===")
print("carrier:", sub12.carrier)
print("topology:", sorted([sorted(list(u)) for u in sub12.topology], key=lambda x: (len(x), x)))
print()
# Ayrik topoloji: her alt kume acik.
# {1,2}'nin alt uzay topolojisi de ayrik: {bos, {1}, {2}, {1,2}}.

# %% [markdown]
"""
### Örnek 5.2 — Alt Uzay: Sierpiński
"""

# %%
s = sierpinski_space()
sub0 = finite_subspace(s, [0])
sub1 = finite_subspace(s, [1])

print("=== Ornek 5.2: Sierpinski Alt Uzaylari ===")
print("carrier {0}:", sub0.carrier, "| topology:", list(sub0.topology))
print("carrier {1}:", sub1.carrier, "| topology:", list(sub1.topology))
print()
# {0}: tau_A = {bos∩{0}, {0,1}∩{0}, {1}∩{0}} = {bos, {0}, bos} = {bos, {0}} -> indiscrete!
# {1}: tau_A = {bos, {1}} -> discrete (tek noktali).

# %% [markdown]
"""
### Örnek 5.3 — Alt Uzay: Özel Topoloji
"""

# %%
X = [1, 2, 3, 4, 5]
tau_X = [set(), {1, 2}, {3, 4}, {1, 2, 3, 4}, {1, 2, 3, 4, 5}]
fts = make_topology(X, *tau_X)
sub_A = finite_subspace(fts, [2, 3, 4])

print("=== Ornek 5.3: Alt Uzay A={2,3,4} ===")
print("carrier:", sub_A.carrier)
print("tau_A:", sorted([sorted(list(u)) for u in sub_A.topology], key=lambda x: (len(x), x)))
print()
# tau_A = {bos∩A, {1,2}∩A, {3,4}∩A, {1,2,3,4}∩A, X∩A}
#       = {bos, {2}, {3,4}, {2,3,4}, {2,3,4}} = {bos, {2}, {3,4}, {2,3,4}}

# %% [markdown]
"""
### Örnek 5.4 — Çarpım Topolojisi: D(0,1) × D(0,1)
"""

# %%
d2 = discrete_topology(0, 1)
prod_dd = binary_product(d2, d2)

print("=== Ornek 5.4: D(0,1) x D(0,1) ===")
print("carrier:", sorted(prod_dd.carrier))
print("topology size:", len(list(prod_dd.topology)))
print("compact:", is_compact(prod_dd).status)
print("connected:", is_connected(prod_dd).status)
print()
# D(0,1) x D(0,1): 4 nokta, 2^4 = 16 acik kume (ayrik carpim).

# %% [markdown]
"""
### Örnek 5.5 — Çarpım Topolojisi: Sierpiński × Sierpiński
"""

# %%
ss = binary_product(s, s)

print("=== Ornek 5.5: Sierpinski x Sierpinski ===")
print("carrier:", sorted(ss.carrier))
print("topology size:", len(list(ss.topology)))
print("compact:", is_compact(ss).status)
print("connected:", is_connected(ss).status)
print()
# Sierpinski x Sierpinski: 4 nokta, daha az acik kume (carpim bazindan).
# Sierpinski baglantilidır -> carpım da baglantilidır.

# %% [markdown]
"""
### Örnek 5.6 — Topolojik Özellik Kalıtımı
"""

# %%
d3 = discrete_topology(1, 2, 3)
ind3 = indiscrete_topology(1, 2, 3)

prod_di = binary_product(d3, ind3)

print("=== Ornek 5.6: D(3) x Ind(3) ===")
print("carrier size:", len(prod_di.carrier))
print("topology size:", len(list(prod_di.topology)))
print("compact:", is_compact(prod_di).status)
print("connected:", is_connected(prod_di).status)
print("T2:", is_t2(prod_di).status)
print()
# Indiscrete baglantilidır -> carpım baglantili.
# Discrete T2'dir ama Indiscrete T0 bile degil -> carpım T2 olmaz.

# %% [markdown]
"""
## 6. Alıştırmalar

### Kodlama

K1. `sierpinski_space()` uzayının {0} ve {1} alt uzaylarını oluşturun.
    Her birinin ayrık mı yoksa indiscrete mi topoloji taşıdığını belirleyin.

K2. `make_topology(1,2,3,4, open_sets=[...])` ile 4-noktalı bir uzay tanımlayın
    ve {2,3} alt uzayını bulun.

K3. `binary_product(sierpinski_space(), discrete_topology(0,1))` için
    `is_compact` ve `is_connected` kontrol edin.

### Teori

T1. Alt uzay topolojisinde dahil etme i: A → X fonksiyonunun sürekli
    olduğunu ispatlayın.

T2. X ve Y bağlantılı ⟹ X × Y bağlantılı olduğunu ispatlayın.
    (İpucu: {x₀} × Y ve X × {y₀} gibi bağlantılı dilimleri kullanın.)
"""

if __name__ == "__main__":
    print("pytop Kullanim Kilavuzu — Bolum 11: Alt Uzay ve Carpim Topolojisi")
    print("=" * 60)
