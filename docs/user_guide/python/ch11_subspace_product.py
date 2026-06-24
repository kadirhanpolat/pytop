# %% [markdown]
"""
# Bölüm 11 — Alt Uzay ve Çarpım Topolojisi

Alt uzay topolojisi bir uzayın alt kümesine "miras kalan" topolojiyi tanımlar.
Çarpım topolojisi ise iki veya daha fazla uzayı birleştirerek yeni bir uzay kurar.

---
"""

# %% [markdown]
"""
## 1. Konu
"""

# %% [markdown]
"""
### Alt Uzay Topolojisi

(X, τ) topolojik uzayı ve A ⊆ X verilsin. **Alt uzay topolojisi:**

    τ_A = {U ∩ A : U ∈ τ}

(A, τ_A) bir topolojik uzaydır; dahil etme i: A → X süreklidir.

> 💡 **Sezgi:** A'yı X'ten kesilen bir "pencere" gibi düşünün. A üzerindeki
> açıkları sıfırdan tanımlamayız; X'in hazır açıklarını A ile keser, "ne kadarı
> A'ya düşüyorsa" onu açık sayarız. Bu yüzden τ_A, τ'dan **miras** alınır.

![A ⊆ X alt uzayında açık kümeler U ∩ A biçimindedir](../assets/ch11/fig_ch11_altuzay.png)
"""

# %% [markdown]
"""
### Çarpım Topolojisi

(X, τ_X) ve (Y, τ_Y) verilsin. **Çarpım topolojisi** X × Y üzerinde
{U × V : U ∈ τ_X, V ∈ τ_Y} bazından üretilen topolojidir.

Projeksiyon π_X: X × Y → X ve π_Y: X × Y → Y süreklidir.
τ_{X×Y} her iki projektiyonu sürekli kılan **en kaba** topolojidir.

> 💡 **Sezgi:** Çarpım topolojisinin bazı, düzlemdeki açık dikdörtgenlere benzer:
> bir "yatay" açık U ile bir "dikey" açık V'yi çarparak U × V kutusunu kurarız.
> Bu kutular tüm açıkların *bazıdır* — açıklar bu kutuların birleşimleridir.

![Çarpım topolojisinin baz elemanı: U × V dikdörtgen kutusu](../assets/ch11/fig_ch11_carpim_baz.png)

İki projeksiyon, çarpımdaki bir noktayı bileşenlerine "düşürür":

![π_X ve π_Y projeksiyonları (x,y) noktasını x ve y'ye gönderir](../assets/ch11/fig_ch11_izdusum.png)

> ❌ **Karşı-örnek:** "U × V biçiminde olmayan açık yok" demek yanlıştır. Açık
> birim disk D(0,1) × D(0,1) içinde bir dairesel bölge, hiçbir tek U × V
> kutusuna eşit olmasa da açıktır — çünkü açıklar kutuların *birleşimidir*,
> kendileri değil. {U × V} yalnızca **baz**'dır, topolojinin tamamı değil.
"""

# %% [markdown]
"""
### Topolojik Özelliklerin Kalıtımı

| Özellik | Alt uzay | Çarpım |
|---------|----------|--------|
| Hausdorff | ✓ (kalıtır) | ✓ |
| Kompaktlık | Yalnız kapalı alt uzay | ✓ (Tychonoff) |
| Bağlantılılık | Genel olarak hayır | ✓ |
| T0/T1/T2 | ✓ | ✓ |

> **Neden bu konu?** Yeni uzay inşa etmenin üç temel yöntemi; çarpım topolojisi Tychonoff teoreminin temelidir.

> 🔍 **Kendin dene:** `subspace_topology` ile `product_topology`'nin boyutunu karşılaştırın.

> ⚠️ **Sık hata:** Çarpım topolojisi ince topolojidir; {U×V} ailesi baz, topoloji değil.

> ↗️ **Bkz.:** Bölüm 7 (Tychonoff), Bölüm 12 (bölüm = eşdeğerlikten gelen topoloji).

> 💭 **Öz-yansıtma:** Alt-uzay topolojisi orijinal topolojiden neden daha az açık küme içerebilir?

---
"""

# %% [markdown]
"""
## 2. Teoremler

**Teorem 2.1.** Hausdorff uzayın her alt uzayı Hausdorff'tur.

> **İspat eskizi.** x ≠ y noktaları A ⊆ X içinde olsun. X Hausdorff olduğundan
> X'te ayrık açıklar U ∋ x, V ∋ y vardır. O hâlde U ∩ A ve V ∩ A, A'da açık,
> x ile y'yi ayıran ve kesişmeyen komşuluklardır: (U ∩ A) ∩ (V ∩ A) = (U ∩ V) ∩ A = ∅.

**Teorem 2.2.** Kompakt uzayın kapalı alt uzayı kompakttır.

> **İspat eskizi.** A ⊆ X kapalı, X kompakt olsun. A'nın bir açık örtüsü
> {U_α ∩ A} verilsin. Her U_α'yı, açık olan X∖A ile birlikte alırsak X'in bir
> açık örtüsünü elde ederiz. X kompakt olduğundan sonlu alt-örtü vardır; bundan
> X∖A'yı atınca A'yı örten sonlu sayıda U_α ∩ A kalır.

**Teorem 2.3.** X ve Y bağlantılı ⟹ X × Y bağlantılıdır.

> **İspat eskizi.** Sabit y₀ için X × {y₀} ≅ X bağlantılıdır; her x için {x} × Y ≅ Y
> bağlantılıdır. Her {x} × Y dilimi, ortak nokta (x, y₀) üzerinden X × {y₀}
> ile kesişir. Ortak noktalı bağlantılı kümelerin birleşimi bağlantılıdır;
> bu birleşim tüm X × Y'yi kapsar.

**Teorem 2.4.** X ve Y kompakt ⟹ X × Y kompakt. (Tychonoff, n=2)

**Teorem 2.5.** X ve Y Hausdorff ⟹ X × Y Hausdorff.

> **İspat eskizi.** (x₁,y₁) ≠ (x₂,y₂) ise ya x₁ ≠ x₂ ya da y₁ ≠ y₂. Diyelim
> x₁ ≠ x₂; X'te ayrık U₁ ∋ x₁, U₂ ∋ x₂ seçilir. O zaman U₁ × Y ve U₂ × Y çarpımda
> açık, ayrık ve iki noktayı ayırır. Bunlar baz elemanı (U × V) biçimindedir.

**Teorem 2.6 (Evrensel Özellik — Çarpım).**
f: Z → X × Y sürekli ⟺ π_X∘f ve π_Y∘f süreklidir.

> **İspat eskizi.** (⟹) Projeksiyonlar sürekli, sürekli fonksiyonların bileşkesi
> süreklidir. (⟸) Bir baz elemanı U × V'nin ön-görüntüsü
> f⁻¹(U × V) = (π_X∘f)⁻¹(U) ∩ (π_Y∘f)⁻¹(V) olup, iki açık ön-görüntünün
> kesişimi olarak Z'de açıktır; baz üzerinde süreklilik tüm topolojide sürekliliği verir.

---
"""

# %% [markdown]
"""
## 3. Algoritmalar
"""

# %% [markdown]
"""
### finite_subspace — O(|τ| · |A|)

```
Subspace(X, tau, A):
    tau_A <- {}
    for each U in tau:
        tau_A.add(U ∩ A)
    return (A, tau_A)
```
"""

# %% [markdown]
"""
### binary_product — O(|τ_X| · |τ_Y|)

```
Product(X, tau_X, Y, tau_Y):
    basis <- {U x V : U in tau_X, V in tau_Y}
    return topology_from_basis(X x Y, basis)
```

---
"""

# %% [markdown]
"""
## 4. pytop API
"""

# %%
from pytop import (
    finite_subspace,
    binary_product,
    sierpinski_space,
    discrete_topology,
    indiscrete_topology,
    make_topology,
    make_set,
    empty_set,
    is_compact,
    is_connected,
    is_t2,
    separation_inherited_by_subspace,
)

# %% [markdown]
"""
`finite_subspace(space, subset)` → `FiniteTopologicalSpace`

`binary_product(left, right)` → `FiniteTopologicalSpace` (carrier: tuple çiftleri)

`separation_inherited_by_subspace(subspace_obj, feature="hausdorff")` → `Result`
(alt uzayın bir ayırma özelliğini miras alıp almadığını bildirir)

---
"""

# %% [markdown]
"""
## 5. Örnekler
"""

# %% [markdown]
"""
### Örnek 5.1 — Alt Uzay: Ayrık Topoloji
"""

# %%
d4 = discrete_topology(1, 2, 3, 4)
sub12 = finite_subspace(d4, [1, 2])
print("carrier:", sub12.carrier)
print("topology:", sorted([sorted(list(u)) for u in sub12.topology], key=lambda x: (len(x), x)))

# %% [markdown]
"""
```text
carrier: (1, 2)
topology: [[], [1], [2], [1, 2]]
```

Ayrık topolojinin alt uzayı da ayrıktır: U ∩ A her A ⊆ X için açıktır.
"""

# %% [markdown]
"""
### Örnek 5.2 — Alt Uzay: Sierpiński
"""

# %%
s = sierpinski_space()
sub0 = finite_subspace(s, [0])
sub1 = finite_subspace(s, [1])
print("carrier {0}:", sub0.carrier, "| topology:", list(sub0.topology))
print("carrier {1}:", sub1.carrier, "| topology:", list(sub1.topology))

# %% [markdown]
"""
```text
carrier {0}: (0,) | topology: [set(), {0}]
carrier {1}: (1,) | topology: [set(), {1}]
```
"""

# %% [markdown]
"""
### Örnek 5.3 — Alt Uzay: Özel Topoloji
"""

# %%
X = [1, 2, 3, 4, 5]
fts = make_topology(
    X,
    empty_set(),
    make_set(1, 2),
    make_set(3, 4),
    make_set(1, 2, 3, 4),
    make_set(1, 2, 3, 4, 5),
)
sub_A = finite_subspace(fts, [2, 3, 4])
print("carrier:", sub_A.carrier)
print("tau_A:", sorted([sorted(list(u)) for u in sub_A.topology], key=lambda x: (len(x),x)))

# %% [markdown]
"""
```text
carrier: (2, 3, 4)
tau_A: [[], [2], [3, 4], [2, 3, 4]]
```

τ_A = {∅∩A, {1,2}∩A, {3,4}∩A, {1,2,3,4}∩A, X∩A} = {∅, {2}, {3,4}, {2,3,4}}.
"""

# %% [markdown]
"""
### Örnek 5.4 — Çarpım: D(0,1) × D(0,1)
"""

# %%
d2 = discrete_topology(0, 1)
prod_dd = binary_product(d2, d2)
print("carrier:", sorted(prod_dd.carrier))
print("topology size:", len(list(prod_dd.topology)))
print("compact:", is_compact(prod_dd).status)
print("connected:", is_connected(prod_dd).status)

# %% [markdown]
"""
```text
carrier: [(0, 0), (0, 1), (1, 0), (1, 1)]
topology size: 16
compact: true
connected: false
```

D(0,1) × D(0,1): 4 nokta, 2⁴ = 16 açık küme. Ayrık → bağlantısız.
"""

# %% [markdown]
"""
### Örnek 5.5 — Çarpım: Sierpiński × Sierpiński
"""

# %%
ss = binary_product(s, s)
print("carrier:", sorted(ss.carrier))
print("topology size:", len(list(ss.topology)))
print("compact:", is_compact(ss).status)
print("connected:", is_connected(ss).status)

# %% [markdown]
"""
```text
carrier: [(0, 0), (0, 1), (1, 0), (1, 1)]
topology size: 6
compact: true
connected: true
```

Sierpiński bağlantılı → çarpım da bağlantılı.
"""

# %% [markdown]
"""
### Örnek 5.6 — Topolojik Özellik Kalıtımı
"""

# %%
d3 = discrete_topology(1, 2, 3)
ind3 = indiscrete_topology(1, 2, 3)
prod_di = binary_product(d3, ind3)
print("topology size:", len(list(prod_di.topology)))
print("compact:", is_compact(prod_di).status)
print("connected:", is_connected(prod_di).status)
print("T2:", is_t2(prod_di).status)

# %% [markdown]
"""
```text
topology size: 8
compact: true
connected: false
T2: false
```

İndiscrete bağlantılı ama D ayrık → çarpım bağlantısız. D T2 ama Ind değil → çarpım T2 değil.
"""

# %% [markdown]
"""
### Örnek 5.7 — Alt Uzay: İndiscrete'in Alt Uzayı İndiscrete'tir
"""

# %%
ind4 = indiscrete_topology(1, 2, 3, 4)
sub_ind = finite_subspace(ind4, [1, 2])
print("carrier:", sub_ind.carrier)
print("topology:", sorted([sorted(list(u)) for u in sub_ind.topology], key=lambda x: (len(x), x)))
print("connected:", is_connected(sub_ind).status)

# %% [markdown]
"""
```text
carrier: (1, 2)
topology: [[], [1, 2]]
connected: true
```

İndiscrete uzayın yalnızca ∅ ve X açıkları vardır; bunları A ile kesince
∅ ∩ A = ∅ ve X ∩ A = A elde edilir. Yani alt uzay yine yalnız {∅, A} taşır:
indiscrete topoloji alt uzaya **miras kalır** ve bağlantılı kalır.
"""

# %% [markdown]
"""
### Örnek 5.8 — Hausdorff Kalıtımı ve Çarpıma Etkisi
"""

# %%
d4 = discrete_topology(1, 2, 3, 4)
sub_d = finite_subspace(d4, [1, 2])
inh = separation_inherited_by_subspace(sub_d, "hausdorff")
print("subspace Hausdorff inherited:", inh.status)

prod_T2 = binary_product(d2, d2)
print("D(0,1) x D(0,1) T2:", is_t2(prod_T2).status)
prod_notT2 = binary_product(d2, indiscrete_topology(0, 1))
print("D(0,1) x Ind(0,1) T2:", is_t2(prod_notT2).status)

# %% [markdown]
"""
```text
subspace Hausdorff inherited: true
D(0,1) x D(0,1) T2: true
D(0,1) x Ind(0,1) T2: false
```

Hausdorff'luk alt uzaya kalıtır (Teorem 2.1). Çarpımda ise ancak **her iki**
çarpan Hausdorff ise sonuç Hausdorff'tur (Teorem 2.5): bir çarpan indiscrete
olunca T2 bozulur.

---
"""

# %% [markdown]
"""
## 6. Alıştırmalar
"""

# %% [markdown]
"""
### Kodlama

K1. `sierpinski_space()` uzayının {0} ve {1} alt uzaylarını oluşturun.
    Her birinin hangi topolojiyi taşıdığını belirleyin.

K2. `make_topology([1,2,3,4], set(), {1,2}, {3,4}, {1,2,3,4})` ile bir uzay
    tanımlayın ve {2,3} alt uzayını bulun.

K3. `binary_product(sierpinski_space(), discrete_topology(0,1))` için
    `is_compact` ve `is_connected` kontrol edin.

K4. `indiscrete_topology(1,2,3,4)` uzayının `[1,2]` alt uzayını oluşturun.
    Taşıdığı açık küme sayısını ve `is_connected` çıktısını bulun; sonucu
    Örnek 5.7 ile karşılaştırın.

K5. `separation_inherited_by_subspace` ile `discrete_topology(1,2,3)`'ten
    alınan `[1,2]` alt uzayının Hausdorff özelliğini miras alıp almadığını
    kontrol edin.
"""

# %% [markdown]
"""
### Teori

T1. Alt uzay topolojisinde i: A → X dahil etme fonksiyonunun sürekli
    olduğunu ispatlayın.

T2. X ve Y bağlantılı ⟹ X × Y bağlantılı olduğunu ispatlayın.
    (İpucu: {x₀} × Y ve X × {y₀} gibi bağlantılı dilimleri kullanın.)

T3. Çarpımın evrensel özelliğini ispatlayın: f: Z → X × Y sürekli ⟺
    π_X∘f ve π_Y∘f süreklidir. (İpucu: bir baz elemanı U × V'nin ön-görüntüsünü
    iki projeksiyonun ön-görüntülerinin kesişimi olarak yazın.)
"""
