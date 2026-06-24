## Bölüm 10: Sürekli Fonksiyonlar

### K1 — Özel topolojide süreklilik kontrolü

(ch10 K1 alıştırmasına dön)

`{0,1,2}` üzerinde zincir topolojisi `{∅, {0}, {0,1}, {0,1,2}}` kurup
`f(0)=0, f(1)=0, f(2)=1` fonksiyonunun sürekli olup olmadığına bakıyoruz.

```python
from pytop import make_topology, make_set, is_continuous_finite_map

Tk = make_topology(make_set(0, 1, 2), make_set(0), make_set(0, 1))
pts, topo = list(Tk.carrier), list(Tk.topology)
f = {0: 0, 1: 0, 2: 1}
print("K1 cont:", is_continuous_finite_map(pts, topo, pts, topo, f))
```

```
K1 cont: True
```

Her açık kümenin geri çekimini kontrol edelim: `f⁻¹({0}) = {0,1}` (açık),
`f⁻¹({0,1}) = {0,1,2} = X` (açık), `f⁻¹(∅) = ∅`, `f⁻¹(X) = X`. Tüm geri
çekimler açık olduğundan `f` süreklidir.

---

### K2 — Sierpiński'den kendisine dört fonksiyon

(ch10 K2 alıştırmasına dön)

Sierpiński τ = {∅, {1}, {0,1}}. Dört fonksiyonu test ediyoruz.

```python
from pytop import sierpinski_space, is_continuous_finite_map

s = sierpinski_space()
pts, topo = list(s.carrier), list(s.topology)
maps = {
    "const0": {0: 0, 1: 0},
    "const1": {0: 1, 1: 1},
    "id":     {0: 0, 1: 1},
    "swap":   {0: 1, 1: 0},
}
for name, m in maps.items():
    print(f"  {name:7s}:", is_continuous_finite_map(pts, topo, pts, topo, m))
```

```
  const0 : True
  const1 : True
  id     : True
  swap   : False
```

Sabit fonksiyonlar her zaman süreklidir. Özdeşlik de süreklidir (her açığın
geri çekimi kendisidir). `swap` ise süreklilik kaybeder: tek özel açık `{1}`'in
geri çekimi `swap⁻¹({1}) = {0}`'dır, bu Sierpiński'de açık değildir. Yani dört
fonksiyondan üçü sürekli, yalnız `swap` sürekli değildir.

---

### K3 — Ayrık uzayların homeomorfizması

(ch10 K3 alıştırmasına dön)

İki üç-noktalı ayrık uzayın homeomorf olup olmadığını doğruluyoruz.

```python
from pytop import discrete_topology, finite_homeomorphism_result

da = discrete_topology(1, 2, 3)
db = discrete_topology('a', 'b', 'c')
print("D3 ~ D3:", finite_homeomorphism_result(da, db).status)
```

```
D3 ~ D3: true
```

Etiketler farklı (sayılar ve harfler) ama topolojik yapı aynı: her iki uzayda da
her alt küme açıktır. Eşit kardinaliteli iki ayrık uzay her zaman homeomorftur;
bir bijeksiyon ve onun tersi otomatik olarak süreklidir.

---

### K4 — Bileşke süreklilik: f, g, g∘f

(ch10 K4 alıştırmasına dön)

Üç zincir topolojisi `{∅, {α}, {α,β}, X}` kuralım; zinciri koruyan iki
fonksiyonun bileşkesinin de sürekli olduğunu doğrulayalım (Teorem 2.2).

```python
from pytop import make_topology, make_set, is_continuous_finite_map

TX = make_topology(make_set(1, 2, 3), make_set(1), make_set(1, 2))
TY = make_topology(make_set('a', 'b', 'c'), make_set('a'), make_set('a', 'b'))
TZ = make_topology(make_set('p', 'q', 'r'), make_set('p'), make_set('p', 'q'))
X_pts, X_topo = list(TX.carrier), list(TX.topology)
Y_pts, Y_topo = list(TY.carrier), list(TY.topology)
Z_pts, Z_topo = list(TZ.carrier), list(TZ.topology)

f = {1: 'a', 2: 'b', 3: 'c'}
g = {'a': 'p', 'b': 'q', 'c': 'r'}
gof = {x: g[f[x]] for x in X_pts}

print("f continuous:    ", is_continuous_finite_map(X_pts, X_topo, Y_pts, Y_topo, f))
print("g continuous:    ", is_continuous_finite_map(Y_pts, Y_topo, Z_pts, Z_topo, g))
print("g of f continuous:", is_continuous_finite_map(X_pts, X_topo, Z_pts, Z_topo, gof))
```

```
f continuous:     True
g continuous:     True
g of f continuous: True
```

`f` zinciri `1→a, 2→b, 3→c` koruyarak taşır, dolayısıyla her açık zincir
elemanının geri çekimi yine açıktır; aynısı `g` için de geçerlidir. Bileşkenin
geri çekimi `(g∘f)⁻¹(W) = f⁻¹(g⁻¹(W))` olduğundan iki sürekli adımın geri
çekimi zincirlenir ve açıklık korunur — `g∘f` süreklidir.

---

### T1 — Her sabit fonksiyon süreklidir

(ch10 T1 alıştırmasına dön)

`f: X → Y`, `f(x) = c` sabit olsun. Herhangi açık `V ⊆ Y` alalım. İki durum var:

1. `c ∈ V` ise her `x ∈ X` için `f(x) = c ∈ V`, yani `f⁻¹(V) = X`.
2. `c ∉ V` ise hiçbir `x` için `f(x) ∈ V` değildir, yani `f⁻¹(V) = ∅`.

Her iki durumda da `f⁻¹(V) ∈ {∅, X}` çıkar; `∅` ve `X` her topolojide açıktır.
Demek ki her açık `V`'nin geri çekimi açıktır — `f` süreklidir. ∎

---

### T2 — Bileşkenin sürekliliği

(ch10 T2 alıştırmasına dön)

`f: X → Y` ve `g: Y → Z` sürekli olsun; `g∘f: X → Z` sürekliliğini gösterelim.

Herhangi açık `W ⊆ Z` alalım.

1. `g` sürekli olduğundan `g⁻¹(W) ⊆ Y` açıktır.
2. `f` sürekli olduğundan `f⁻¹(g⁻¹(W)) ⊆ X` açıktır.
3. Küme özdeşliği: `(g∘f)⁻¹(W) = f⁻¹(g⁻¹(W))`.

Dolayısıyla `(g∘f)⁻¹(W)` açıktır. `W` keyfi açık olduğundan `g∘f` süreklidir. ∎

Bu, K4 alıştırmasında zincir topolojileriyle sayısal olarak da doğrulanır.

---

### T3 — Kompaktın sürekli görüntüsü kompakttır

(ch10 T3 alıştırmasına dön)

`f: X → Y` sürekli ve `X` kompakt olsun; `f(X)`'in kompakt olduğunu gösterelim.

`f(X)`'in (alt-uzay topolojisinde) bir açık örtüsü `{V_α}` verilsin; her `V_α`,
`Y`'nin bir açığının `f(X)` ile kesişimidir. Genellik kaybetmeden `V_α`'ları
`Y`'nin açıkları olarak alalım, öyle ki `f(X) ⊆ ⋃_α V_α`.

1. **Geri çekim.** `f` sürekli olduğundan her `f⁻¹(V_α)` `X`'te açıktır. Her
   `x ∈ X` için `f(x) ∈ f(X) ⊆ ⋃ V_α` olduğundan `x` bir `f⁻¹(V_α)` içindedir;
   yani `{f⁻¹(V_α)}` `X`'i örter.
2. **Sonlu alt-örtü.** `X` kompakt olduğundan sonlu indeksler `α₁, …, αₙ` vardır
   ki `X = f⁻¹(V_{α₁}) ∪ ⋯ ∪ f⁻¹(V_{αₙ})`.
3. **Görüntüye it.** O zaman `f(X) ⊆ V_{α₁} ∪ ⋯ ∪ V_{αₙ}`: çünkü herhangi
   `y = f(x) ∈ f(X)` için `x` bir `f⁻¹(V_{αᵢ})` içindedir, dolayısıyla
   `y = f(x) ∈ V_{αᵢ}`.

Demek ki keyfi `{V_α}` örtüsünün sonlu bir alt-örtüsü `{V_{α₁}, …, V_{αₙ}}`
bulundu. `f(X)` kompakttır. ∎

Sezgi: *süreklilik* açık örtüyü kaynağa geri çeker, *kompaktlık* orada sonlu
alt-örtü verir, sonra bu sonlu seçim görüntüye geri itilir. Bu, Bölüm 7'deki
``kompakt görüntü kompakttır'' teoreminin tam ispatıdır.
