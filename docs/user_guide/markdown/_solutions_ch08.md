## Bölüm 8: Bağlantılılık

### K1 — Clopen bölme: {1} | {2,3}

(ch08 K1 alıştırmasına dön)

```python
from pytop import make_topology, is_connected

t = make_topology({1, 2, 3}, {1}, {2, 3})
print("make_topology({1,2,3},{1},{2,3}) connected?", is_connected(t).status)
```

```
make_topology({1,2,3},{1},{2,3}) connected? false
```

Topoloji `{1}` ile `{2,3}`'ü taban açık küme yaptığından ikisi de birbirinin
tümleyenidir: hem açık hem kapalı (*clopen*). Demek ki `X = {1} ⊔ {2,3}` boş
olmayan, trivial olmayan bir clopen ayrılmadır ⟹ uzay **bağlantısız**dır.

### K2 — Sonlu zincir bağlantılıdır

(ch08 K2 alıştırmasına dön)

```python
from pytop import finite_chain_space, is_connected

print("chain(4) connected?", is_connected(finite_chain_space(4)).status)
```

```
chain(4) connected? true
```

`finite_chain_space(4)` iç içe (nested) açık kümelerden oluşur: `{0} ⊂ {0,1} ⊂
{0,1,2} ⊂ {0,1,2,3}`. Hiçbir açık kümenin tümleyeni açık değildir (en küçük açık
kümede `0` her zaman bulunur), dolayısıyla clopen bölme kurulamaz — zincir
**bağlantılı**dır.

### K3 — İki noktalı ayrık vs indiscrete

(ch08 K3 alıştırmasına dön)

```python
from pytop import (two_point_discrete_space, two_point_indiscrete_space,
                   is_connected, is_path_connected)

for name, sp in [("discrete2", two_point_discrete_space()),
                 ("indiscrete2", two_point_indiscrete_space())]:
    print(f"{name:12s} connected={is_connected(sp).status:6s} "
          f"path={is_path_connected(sp).status}")
```

```
discrete2    connected=false  path=unknown
indiscrete2  connected=true   path=unknown
```

İki noktalı **ayrık** uzayda her tekil küme clopen olduğundan `{a} ⊔ {b}` bir
bölme verir ⟹ bağlantısız. İki noktalı **indiscrete** uzayda yalnız `∅` ve `X`
açıktır; trivial olmayan clopen küme yok ⟹ bağlantılı. (Yol durumu için pytop
sonlu uzaylarda kesin tanık üretemediğinden `unknown` döner.)

### K4 — Ark / yol düzeyi farkı

(ch08 K4 alıştırmasına dön)

```python
from pytop import (indiscrete_topology, real_line_metric,
                   is_arc_connected, is_path_connected)

for name, sp in [("Indiscrete(2)", indiscrete_topology(1, 2)),
                 ("R", real_line_metric())]:
    print(f"{name:14s} arc={is_arc_connected(sp).status:8s} "
          f"path={is_path_connected(sp).status}")
```

```
Indiscrete(2)  arc=true     path=unknown
R              arc=unknown  path=true
```

İki uzayda da farklı düzeyler `unknown` döner: indiscrete sonlu uzayda pytop
**ark**-bağlantılığı yapısal olarak doğrular (`true`) ama yol için kesin tanık
üretmez; ℝ'de tam tersine **yol**-bağlantılılık `true`, ark düzeyi `unknown`'dır.
`unknown`, ilgili düzeyin `false` olduğu anlamına **gelmez** — yalnız pytop'un o
düzey için kesin karar verememesidir.

### K5 — `analyze_connectedness` tutarlılığı

(ch08 K5 alıştırmasına dön)

```python
from pytop import analyze_connectedness, discrete_topology

d = discrete_topology(1, 2, 3)
print("connected           :", analyze_connectedness(d, "connected").status)
print("totally_disconnected:", analyze_connectedness(d, "totally_disconnected").status)
```

```
connected            : false
totally_disconnected : true
```

İki sonuç birbiriyle tutarlıdır: ayrık uzay (birden çok noktayla) **bağlantısız**
(`connected: false`) ve aynı zamanda **tamamen bağlantısız**dır
(`totally_disconnected: true`) — her tekil küme clopen olduğundan tek-noktadan
büyük hiçbir bağlantılı alt küme yoktur. `analyze_connectedness` farklı
`property_name` değerleriyle aynı uzayı tek arayüzden sorgulamayı sağlar.

### T1 — Bağlantılı + sürekli ⟹ görüntü bağlantılı

(ch08 T1 alıştırmasına dön)

`f: X → Y` sürekli, `X` bağlantılı olsun. Tersine, `f(X)` bağlantısız olsaydı
`f(X) = U ⊔ V` biçiminde boş olmayan, ayrık, açık iki kümeye bölünürdü.
Süreklilikten `f⁻¹(U)` ve `f⁻¹(V)` açıktır; ayrıktır; birleşimleri `X`'tir ve
ikisi de boş değildir (çünkü `U, V ⊆ f(X)` boş değil, dolayısıyla ön görüntüleri
de boş olamaz). Bu, `X`'in trivial olmayan bir clopen ayrılmasıdır ve `X`'in
bağlantılılığıyla çelişir. O hâlde `f(X)` bağlantılıdır. ∎

### T2 — Yol-bağlantılı ⟹ bağlantılı

(ch08 T2 alıştırmasına dön)

`X` yol-bağlantılı ama bağlantısız olsaydı, `X = U ⊔ V` trivial olmayan bir clopen
ayrılma bulunurdu. `x ∈ U` ve `y ∈ V` seçip, yol-bağlantılılıktan `f:[0,1]→X`,
`f(0)=x`, `f(1)=y` sürekli yolunu alalım. `[0,1]` bağlantılıdır; o hâlde `f([0,1])`
de bağlantılıdır (T1). Ama `U ∩ f([0,1])` ve `V ∩ f([0,1])`, `f([0,1])`'in boş
olmayan (sırasıyla `x` ve `y`'yi içerir), ayrık, açık iki parçaya ayrılmasıdır —
yani `f([0,1])` bağlantısız olurdu. Çelişki. Demek ki `X` bağlantılıdır.

Tersi yanlıştır: topolojist sinüs eğrisi bağlantılıdır ama yol-bağlantılı
değildir (bkz. T3). ∎

### T3 — Topolojist sinüs eğrisi: bağlantılı ama yol-bağlantısız

(ch08 T3 alıştırmasına dön)

`S = {(x, sin(1/x)) : 0 < x ≤ 1} ∪ ({0}×[-1,1])` olsun. İki gözlem:

**Bağlantılı.** Sağdaki eğri parçası `G = {(x, sin(1/x)) : 0 < x ≤ 1}` sürekli bir
görüntü olduğundan bağlantılıdır. `x → 0⁺` giderken `sin(1/x)` tüm `[-1,1]`
değerlerini sonsuz kez alır; bu yüzden dikey segment `{0}×[-1,1]`'in her noktası
`G`'nin kapanışındadır: `S = cl(G)`. Bağlantılı bir kümenin kapanışı bağlantılıdır
⟹ `S` bağlantılıdır.

**Yol-bağlantısız.** Dikey segmentteki bir nokta `p = (0, 0)` ile eğri üzerindeki
bir nokta `q` arasında sürekli bir yol `γ:[0,1]→S`, `γ(0)=p`, `γ(1)=q` olduğunu
varsayalım. `t₀ = sup{t : γ(t) ∈ {0}×[-1,1]}` noktasını ele alın. `t₀`'a sağdan
yaklaşıldığında `γ`'nın birinci koordinatı `x(t) → 0⁺` olur; süreklilik gereği
ikinci koordinat `y(t) = sin(1/x(t))` bir limite yakınsamalı. Ama `x(t) → 0⁺`
iken `sin(1/x(t))` `-1` ile `+1` arasında salınmaya devam eder ve **yakınsamaz** —
süreklilikle çelişir. Demek ki böyle bir yol yoktur: `S` yol-bağlantılı değildir.

Sonuç: "tek parça olmak" (bağlantılı) ile "iki noktayı sürekli yolla
birleştirebilmek" (yol-bağlantılı) farklı kavramlardır. ∎
