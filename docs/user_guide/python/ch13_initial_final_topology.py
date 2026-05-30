# %% [markdown]
"""
# Bölüm 13 — Başlangıç ve Son Topoloji

**Başlangıç topolojisi** (initial topology): verilen haritaları sürekli kılan en kaba
(coarsest) topolojidir.
**Son topoloji** (final topology): verilen haritaları sürekli kılan en ince (finest)
topolojidir.
Altuzay ve çarpım topolojileri başlangıç topolojisinin; bölüm (quotient) topolojisi ise
son topolojisinin özel halleridir.
"""

# %%
from pytop.finite_map_analysis import FiniteMap
from pytop import (
    initial_topology_from_maps,
    discrete_topology, indiscrete_topology, make_topology, sierpinski_space,
    binary_product, finite_subspace,
    generic_quotient_space_from_map,
    is_t0, is_t1, is_t2,
)

# %% [markdown]
"""
## 1. Başlangıç Topolojisi

X kümesi ve haritalar ailesi {f_alpha : X -> (Y_alpha, tau_alpha)} verilsin.

**Tanım.** Başlangıç topolojisi tau_ini, her f_alpha'yı sürekli kılan
topolojilerin kesişimidir.

Alt-baz:
    S = {f_alpha^{-1}(U) | U in tau_alpha, alpha in A}
    tau_ini = S tarafindan uretilen topoloji (kesisim + birlesimlerin kapatmasi)

**Teorem 1.** tau_ini tekil ve vardır; her f_alpha'yı sürekli kılan tüm topolojilerin
en kaba (coarsest) olanıdır.

**Teorem 2.** Altuzay topolojisi = ekleme haritası i: A -> X'in başlangıç topolojisidir.

**Teorem 3.** Çarpım topolojisi = projeksiyon haritaları {pi_alpha}'nın başlangıç
topolojisidir.

**Teorem 4 (evrensel özellik).** Z -> (X, tau_ini) haritası f süreklidir ancak ve
ancak f_alpha o f her alpha için sürekli olduğunda.
"""

# %% [markdown]
"""
## 2. pytop API: initial_topology_from_maps

```python
initial_topology_from_maps(carrier, [FiniteMap(domain, codomain, name, mapping)])
```

Algoritma:
  1. Her haritanın kodomen uzayındaki açık kümelerin ön-görüntülerini hesapla.
  2. Bu ön-görüntülerden bir alt-baz oluştur.
  3. Alt-bazdan topolojiyi üret (kesişim ve birleşim kapatması).

Dikkat: `FiniteMap` doğrudan veri sınıfı olarak kullanılır; `make_function` değil.
Her haritanın domain carrier'ı, istenen başlangıç uzayının carrier'ıyla eşit olmalıdır.
"""

# %% [markdown]
"""
## 3. Tek Harita ile Başlangıç Topolojisi
"""

# %%
# X = {0,1,2,3}, Y = discrete({0,1}), f(0)=f(1)=0, f(2)=f(3)=1
X_carrier = [0, 1, 2, 3]
Y_d = discrete_topology(0, 1)
X_ph  = make_topology(X_carrier, set(), set(X_carrier))   # sadece carrier gerekli

f = FiniteMap(domain=X_ph, codomain=Y_d, name="f",
              mapping={0: 0, 1: 0, 2: 1, 3: 1})

tau_f = initial_topology_from_maps(X_carrier, [f])

print("f: {0,1} -> 0, {2,3} -> 1")
print("Y topolojisi (discrete):",
      sorted([sorted(u) for u in Y_d.topology], key=lambda x: (len(x), x)))
print("Baslangic topolojisi:")
for u in sorted([sorted(u) for u in tau_f.topology], key=lambda x: (len(x), x)):
    print("  ", u if u else "empty")
print("Eleman sayisi:", len(tau_f.topology))

# %% [markdown]
"""
```text
f: {0,1} -> 0, {2,3} -> 1
Y topolojisi (discrete): [[], [0], [1], [0, 1]]
Baslangic topolojisi:
   empty
   [0, 1]
   [2, 3]
   [0, 1, 2, 3]
Eleman sayisi: 4
```

Alt-baz hesabı:
  f^{-1}(empty) = empty         -> her zaman acik
  f^{-1}({0})   = {0,1}         -> alt-baz elemanı
  f^{-1}({1})   = {2,3}         -> alt-baz elemanı
  f^{-1}({0,1}) = {0,1,2,3}     -> birlesimle zaten var

Tau_ini = {empty, {0,1}, {2,3}, {0,1,2,3}} — 4 acik kume.
"""

# %% [markdown]
"""
## 4. İkinci Harita Topolojiyi İnceltir
"""

# %%
# g: {0,1,2,3} -> Sierpinski,  g(0)=0, g(1)=g(2)=g(3)=1
S_sier = sierpinski_space()   # carrier {0,1}, acik kumeler: empty, {1}, {0,1}
g = FiniteMap(domain=X_ph, codomain=S_sier, name="g",
              mapping={0: 0, 1: 1, 2: 1, 3: 1})

tau_fg = initial_topology_from_maps(X_carrier, [f, g])

print("g: {0} -> 0, {1,2,3} -> 1  (Sierpinski kodomen)")
print("Baslangic topolojisi (f ve g birlikte):")
for u in sorted([sorted(u) for u in tau_fg.topology], key=lambda x: (len(x), x)):
    print("  ", u if u else "empty")
print("f tek basina:", len(tau_f.topology), "eleman  |  f+g:", len(tau_fg.topology), "eleman")

# %% [markdown]
"""
```text
g: {0} -> 0, {1,2,3} -> 1  (Sierpinski kodomen)
Baslangic topolojisi (f ve g birlikte):
   empty
   [1]
   [0, 1]
   [2, 3]
   [1, 2, 3]
   [0, 1, 2, 3]
f tek basina: 4 eleman  |  f+g: 6 eleman
```

g'nin alt-baz katkisi: g^{-1}({1}) = {1,2,3}
Yeni kesisim: {0,1} ∩ {1,2,3} = {1}
Daha fazla harita = daha ince (ya da esit) topoloji.
"""

# %% [markdown]
"""
## 5. Özel Hal 1 — Altuzay = Başlangıç Topolojisi

i: A -> X ekleme haritasının başlangıç topolojisi, A üzerindeki altuzay topolojisiyle
örtüşür.
"""

# %%
fts_X = make_topology([0, 1, 2, 3], set(), {0, 1}, {2, 3}, {0, 1, 2, 3})

# Altuzay topolojisi
sub_A = finite_subspace(fts_X, [1, 2])

# Baslangic topolojisi: ekleme i: {1,2} -> X
A_dom = discrete_topology(1, 2)   # domain topology anlamsiz; sadece carrier secme
inc   = FiniteMap(domain=A_dom, codomain=fts_X, name="i", mapping={1: 1, 2: 2})
init_A = initial_topology_from_maps([1, 2], [inc])

sub_tau  = sorted([sorted(u) for u in sub_A.topology],  key=lambda x: (len(x), x))
init_tau = sorted([sorted(u) for u in init_A.topology], key=lambda x: (len(x), x))

print("X topolojisi:",
      sorted([sorted(u) for u in fts_X.topology], key=lambda x: (len(x), x)))
print()
print("A={1,2} altuzay topolojisi :", sub_tau)
print("A={1,2} baslangic topolojisi:", init_tau)
print("Esit mi:", sub_tau == init_tau)

# %% [markdown]
"""
```text
X topolojisi: [[], [0, 1], [2, 3], [0, 1, 2, 3]]

A={1,2} altuzay topolojisi : [[], [1], [2], [1, 2]]
A={1,2} baslangic topolojisi: [[], [1], [2], [1, 2]]
Esit mi: True
```

Hesap: i^{-1}({0,1}) = {1}, i^{-1}({2,3}) = {2} — alt-baz {1} ve {2}'yi verir.
Bu alt-baz discrete({1,2}) üretir; altuzay topolojisiyle ozdes.
"""

# %% [markdown]
"""
## 6. Özel Hal 2 — Çarpım = Başlangıç Topolojisi

d2 × d2 çarpım topolojisi, projeksiyon haritaları pi_X ve pi_Y'nin başlangıç
topolojisiyle özdeşleşir.
"""

# %%
d2   = discrete_topology(0, 1)
prod = binary_product(d2, d2)   # carrier: {(0,0),(0,1),(1,0),(1,1)}

pi_x = FiniteMap(domain=prod, codomain=d2, name="pi_x",
                 mapping={(0, 0): 0, (0, 1): 0, (1, 0): 1, (1, 1): 1})
pi_y = FiniteMap(domain=prod, codomain=d2, name="pi_y",
                 mapping={(0, 0): 0, (0, 1): 1, (1, 0): 0, (1, 1): 1})

init_prod = initial_topology_from_maps(list(prod.carrier), [pi_x, pi_y])

prod_fs = {frozenset(u) for u in prod.topology}
init_fs = {frozenset(u) for u in init_prod.topology}

print("Carpim uzayi tasiyicisi:", sorted(prod.carrier))
print("Carpim topolojisi eleman sayisi  :", len(prod.topology))
print("Baslangic topolojisi eleman sayisi:", len(init_prod.topology))
print("Esit mi:", prod_fs == init_fs)

# %% [markdown]
"""
```text
Carpim uzayi tasiyicisi: [(0, 0), (0, 1), (1, 0), (1, 1)]
Carpim topolojisi eleman sayisi  : 16
Baslangic topolojisi eleman sayisi: 16
Esit mi: True
```

pi_x ve pi_y'nin alt-baz katkıları:
  pi_x^{-1}({0}) = {(0,0),(0,1)},  pi_x^{-1}({1}) = {(1,0),(1,1)}
  pi_y^{-1}({0}) = {(0,0),(1,0)},  pi_y^{-1}({1}) = {(0,1),(1,1)}

Bu dört küme, kesişimleriyle tüm tektonları üretir; birleşimleri tam kuvvet
kümesini (discrete) verir.
"""

# %% [markdown]
"""
## 7. Son Topoloji

Haritalar ailesi {g_i : (X_i, sigma_i) -> Y} verilsin.

**Tanım.** Son topoloji (final topology) tau_fin, her g_i'yi sürekli kılan
topolojilerin birleşimidir; en ince topolojidir.

    V in tau_fin  <=>  g_i^{-1}(V) in sigma_i  (her i icin)

**Teorem 5.** tau_fin tekil ve vardır; en ince (finest) topolojidir.

**Teorem 6 (evrensel özellik).** h: (Y, tau_fin) -> Z haritası süreklidir ancak ve
ancak h o g_i her i için sürekli olduğunda.

**Teorem 7.** Bölüm topolojisi, tek surjektif haritanın (q: X -> X/~) son
topolojisidir.

Algoritma (sonlu durum):
  tau_fin = {V ⊆ Y : g_i^{-1}(V) in sigma_i tum i icin}

Bu alt kümeler Y'nin kuvvet kümesi üzerinde koşulla filtrelenir: O(2^|Y| × Σ |sigma_i|).
"""

# %% [markdown]
"""
## 8. Son Topoloji — Manuel Hesap
"""

# %%
# X1 = {0,1,2} ile tau_{X1} = {empty, {0,1}, {0,1,2}}
# g1: X1 -> Y={0,1}, g1(0)=g1(1)=0, g1(2)=1
X1       = make_topology([0, 1, 2], set(), {0, 1}, {0, 1, 2})
Y_car    = [0, 1]
g1_map   = {0: 0, 1: 0, 2: 1}
tau_X1   = {frozenset(u) for u in X1.topology}

open_Y = []
for mask in range(1 << len(Y_car)):
    V        = frozenset(Y_car[i] for i in range(len(Y_car)) if mask & (1 << i))
    preimage = frozenset(x for x in X1.carrier if g1_map[x] in V)
    if preimage in tau_X1:
        open_Y.append(set(V))

final_Y   = make_topology(Y_car, *open_Y)
final_tau = sorted([sorted(u) for u in final_Y.topology], key=lambda x: (len(x), x))

print("X1 topolojisi:",
      sorted([sorted(u) for u in X1.topology], key=lambda x: (len(x), x)))
print("g1: {0,1} -> 0, {2} -> 1")
print()
print("Son topoloji on Y={0,1}:", final_tau)
print("Eleman sayisi:", len(final_Y.topology))

# %% [markdown]
"""
```text
X1 topolojisi: [[], [0, 1], [0, 1, 2]]
g1: {0,1} -> 0, {2} -> 1

Son topoloji on Y={0,1}: [[], [0], [0, 1]]
Eleman sayisi: 3
```

Aciklama (her V ic Y icin g1^{-1}(V) kontrolu):
  V=empty    : preimage=empty   in tau_{X1}? Evet
  V={0}      : preimage={0,1}   in tau_{X1}? Evet ({0,1} acik)
  V={1}      : preimage={2}     in tau_{X1}? Hayir ({2} acik degil)
  V={0,1}    : preimage={0,1,2} in tau_{X1}? Evet

Son topoloji = {empty, {0}, {0,1}} — Sierpinski-benzeri, {0} acik tek tektondur.
"""

# %% [markdown]
"""
## 9. Bölüm Topolojisi = Son Topoloji
"""

# %%
# generic_quotient_space_from_map: sonlu haritalar icin on-topoloji duyarli
Y_ind = indiscrete_topology(0, 1)   # codomain carrier'i saglayan yer tutucu
q     = FiniteMap(domain=X1, codomain=Y_ind, name="q",
                  mapping={0: 0, 1: 0, 2: 1})

quot_Y   = generic_quotient_space_from_map(q)
quot_tau = sorted([sorted(u) for u in quot_Y.topology], key=lambda x: (len(x), x))

print("generic_quotient_space_from_map sonucu:", quot_tau)
print("Manuel son topoloji ile esit mi  :", quot_tau == final_tau)

print()
print("Son topoloji T0 mi:", is_t0(final_Y).status)
print("Son topoloji T2 mi:", is_t2(final_Y).status)

# %% [markdown]
"""
```text
generic_quotient_space_from_map sonucu: [[], [0], [0, 1]]
Manuel son topoloji ile esit mi  : True

Son topoloji T0 mi: true
Son topoloji T2 mi: false
```

Bölüm = son topoloji: q^{-1}(V) acik <=> V bolum topolojisinde acik.
Son topoloji T0'dir (0 ve 1 komshuluk sistemiyle ayrılır) ancak T2 degil.
"""

# %% [markdown]
"""
## Alıştırmalar

1. f: {a,b,c,d} -> discrete({0,1}),  f(a)=f(b)=0, f(c)=f(d)=1 haritasiyla
   `initial_topology_from_maps` kullanin. Sonucu altuzay `finite_subspace` ile
   karsilastirin: iki sonlu bölüm için eşitlik beklenebilir mi?

2. Iki projeksiyon pi_x, pi_y yerine yalnizca pi_x kullanildiginda carpim uzayinin
   baslangic topolojisi ne olur? Discrete mi yoksa daha kaba mi?

3. X = {0,1,2,3,4}, sigma_X = discrete, g: X -> Y={0,1,2} haritasi icin
   son topolojiyi manuel olarak hesaplayin. Hangi degisik sigma_X'ler farkli son
   topolojiler uretir?

4. (Teori) Z -> (X, tau_ini) surekli olmasi icin neden f_alpha o f'nin
   surekliligi yeterlidir? Evrensel ozelligi ispatayin.

5. (Teori) tau_fin'den daha ince hicbir topoloji her g_i'yi surekli kilamaz;
   bunu tanımdaki "en ince" kosulundan kalkarak gosterin.
"""

# %%
if __name__ == "__main__":
    pass
