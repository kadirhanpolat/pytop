# %% [markdown]
"""
# Bölüm 8 — Bağlantılılık

Bağlantılılık, bir topolojik uzayın iki ayrı açık parçaya bölünememesi özelliğidir.
Yol-bağlantılılık daha güçlü bir kavramdır ve sürekli yolların varlığına dayanır.

---
"""

# %% [markdown]
"""
## 1. Konu
"""

# %% [markdown]
"""
### 1.0 Sezgisel Giriş — "Tek Parça mı, Kopuk mu?"

Bağlantılılığı tek cümlede özetlemek gerekirse: **bir uzayın iki ayrı *açık*
parçaya kesilememesidir.** Bir kâğıt parçasını düşünün — onu hiçbir yeri
yırtmadan iki ayrı açık parçaya bölemiyorsanız o kâğıt bağlantılıdır. Baştan iki
ayrı kâğıdınız varsa uzay bağlantısızdır.

![Bağlantılı (tek parça) vs bağlantısız (X = U ⊔ V, iki ayrı clopen parça).](../assets/ch08/fig_ch08_clopen_ayrilma.png)

Bu "kesilememe" fikrinin teknik karşılığı **clopen ayrılma**dır: uzay
bağlantısızdır ancak ve ancak boş olmayan, uzayın tamamından farklı, hem açık hem
kapalı (*clopen*) bir küme varsa. Bağlantılı uzayda böyle bir bölme yoktur; tek
"trivial" clopen kümeler ∅ ve X'tir.

> 💡 **Sezgi:** "Bağlantılı" = uzay tek parça. "Yol-bağlantılı" = uzayda herhangi
> iki noktayı sürekli bir yol ile birleştirebilmek. İkinci kavram birincisinden
> *daha güçlü*: yol kurabiliyorsanız zaten tek parçasınızdır, ama tek parça olmak
> her zaman yol kurabildiğiniz anlamına gelmez (aşağıdaki sinüs eğrisi karşı-örneği).
"""

# %% [markdown]
"""
### Bağlantılılık Kavramları

| Kavram | Tanım |
|--------|-------|
| **Bağlantılı (connected)** | X = U ∪ V, U∩V = ∅, U,V açık ⟹ U=∅ veya V=∅ |
| **Yol-bağlantılı (path-connected)** | ∀ x,y ∈ X: ∃ sürekli f:[0,1]→X, f(0)=x, f(1)=y |
| **Ark-bağlantılı (arc-connected)** | Yol-bağlantılı; üstelik yollar enjektif |
| **Lokal bağlantılı** | Her noktanın bağlantılı komşulukları var |
| **Tamamen bağlantısız** | Her bağlantılı alt küme tek-noktadır |

**Sıralama:** Ark-bağlantılı ⟹ Yol-bağlantılı ⟹ Bağlantılı.
"""

# %% [markdown]
"""
### Clopen Ayrılma

X bağlantısız ⟺ boş olmayan trivial olmayan bir clopen A ⊆ X vardır.
"""

# %% [markdown]
"""
### Bağlantılı Bileşenler

Bir uzayı, içerme bakımından **en büyük** bağlantılı alt kümelerine ayırabiliriz;
bunlara *bağlantılı bileşenler* denir. Bileşenler X'i örten, ayrık parçalardır.
Uzay bağlantılıdır ⟺ tek bir bileşeni vardır (k = 1).

![Bağlantılı bileşenler: X = C₁ ⊔ C₂ ⊔ C₃; her parça en büyük bağlantılı alt küme.](../assets/ch08/fig_ch08_bilesenler.png)

> ❌ **Karşı-örnek (Topolojist sinüs eğrisi — bağlantılı ama yol-bağlantısız):**
> $S = \{(x, \sin\tfrac{1}{x}) : 0 < x \le 1\} \cup (\{0\}\times[-1,1])$ kümesini
> ele alın. Sağdaki eğri $x \to 0^+$ giderken sonsuz hızla salınır ve soldaki
> dikey segmente keyfi yakın olur; bu yüzden $S$ **bağlantılıdır**. Ama dikey
> segmentteki bir noktayı eğri üzerindeki bir noktaya bağlayan *sürekli* bir yol
> **yoktur** — yol $x=0$'a yaklaşırken sinüs salınımı yakınsamayı engeller. Demek
> ki $S$ bağlantılı, ama **yol-bağlantılı değil**. "Tek parça olmak" ile "yol
> kurulabilmek"in aynı şey olmadığının klasik kanıtıdır.

![Topolojist sinüs eğrisi: bağlantılı ama yol-bağlantılı değil.](../assets/ch08/fig_ch08_topolojist_sinus.png)

> **Neden bu konu?** Bağlantılılık ve yol-bağlantılılık aynı kavram değildir; pytop ikisini ayrı ayrı test eder.

> 🔍 **Kendin dene:** Sierpiński `is_connected` mı? Cevabınızı tahmin edin, sonra test edin.

> ⚠️ **Sık hata:** Yol-bağlantılı ⟹ Bağlantılı, ama tersi yanlış; `is_path_connected True` iken `is_connected False` olamaz.

> ↗️ **Bkz.:** Bölüm 10 (sürekli görüntü bağlantılıdır).

> 💭 **Öz-yansıtma:** Ayrık topoloji neden bağlantısızdır?

---
"""

# %% [markdown]
"""
## 2. Teoremler

**Teorem 2.1.** Bağlantılı küme süreklilik altında bağlantılıdır:
f: X → Y sürekli, X bağlantılı ⟹ f(X) bağlantılı.

> **İspat eskizi.** $f(X)$ bağlantısız olsaydı, $f(X) = U \sqcup V$ biçiminde boş
> olmayan, ayrık, açık iki kümeye ayrılırdı. Süreklilikten $f^{-1}(U)$ ve
> $f^{-1}(V)$ açıktır; ayrıktır; birleşimleri $X$'tir ve ikisi de boş değildir
> (çünkü $U, V \subseteq f(X)$ boş değil). Bu, $X$'in bir clopen ayrılmasıdır —
> $X$'in bağlantılılığıyla çelişir. Demek ki $f(X)$ bağlantılı. ∎

**Teorem 2.2.** Yol-bağlantılı ⟹ bağlantılı. Tersi genel olarak yanlış.
(Karşı örnek: Topolojist sinüs eğrisi — bağlantılı ama yol-bağlantısız.)

> **İspat eskizi.** $X$ yol-bağlantılı ama bağlantısız olsaydı, $X = U \sqcup V$
> clopen ayrılması olurdu. $x \in U$, $y \in V$ alıp $f:[0,1]\to X$, $f(0)=x$,
> $f(1)=y$ sürekli yolunu kuralım. $[0,1]$ bağlantılı olduğundan görüntü $f([0,1])$
> de bağlantılıdır (Teorem 2.1); ama bu görüntü $U$ ve $V$ tarafından gerçek bir
> clopen ayrılmaya uğrar (her ikisini de keser) — çelişki. Ters yön yanlıştır:
> topolojist sinüs eğrisi bağlantılı, ama yol-bağlantılı değildir. ∎

**Teorem 2.3 (Ara Değer Teoremi).** f: X → ℝ sürekli, X bağlantılı, a,b ∈ f(X) ise
her c ∈ [a,b] için f⁻¹(c) ≠ ∅.

> **İspat eskizi.** $f(X) \subseteq \mathbb{R}$ bağlantılıdır (Teorem 2.1).
> $\mathbb{R}$'de bağlantılı kümeler tam olarak aralıklardır (Teorem 2.4); demek
> ki $f(X)$ bir aralıktır. $a, b \in f(X)$ ise aralık özelliğinden tüm $[a,b]
> \subseteq f(X)$. O hâlde her $c \in [a,b]$ için $c \in f(X)$, yani $f^{-1}(c)
> \neq \emptyset$. ∎

**Teorem 2.4.** Gerçek doğru ℝ'de bağlantılı alt kümeler tam olarak aralıklardır.

> **İspat eskizi.** (Aralık ⟹ bağlantılı) Bir $I$ aralığı $U \sqcup V$ clopen
> ayrılmasına uğrasaydı, $a\in U$, $b\in V$ ($a<b$) alıp $c=\sup\{x\in U : x\le b\}$
> tanımlanır; $c$'nin hangi parçada olduğu hem açıklık hem kapalılıkla çelişir.
> (Bağlantılı ⟹ aralık) $S$ aralık değilse, $a<c<b$ olup $a,b\in S$, $c\notin S$
> olan bir $c$ vardır; o zaman $(-\infty,c)\cap S$ ve $(c,\infty)\cap S$ bir clopen
> ayrılma verir. ∎

---
"""

# %% [markdown]
"""
## 3. Algoritmalar
"""

# %% [markdown]
"""
### Sonlu Bağlantılılık — O(|τ|²)

```
BagliMi(X, tau):
    for each non-empty A ⊊ X:
        if A ∈ tau and X\A ∈ tau:
            return False   // A clopen bölme bulundu
    return True
```

Karmaşıklık: O(|τ|²) — clopen küme taraması.

---
"""

# %% [markdown]
"""
## 4. pytop API
"""

# %%
from pytop import (
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
Tüm fonksiyonlar `Result` döner: `.status` ('true'/'false'/'unknown').

---
"""

# %% [markdown]
"""
## 5. Örnekler
"""

# %% [markdown]
"""
### Örnek 5.1 — Sierpiński: Bağlantılı
"""

# %%
from pytop import sierpinski_space, is_connected, is_path_connected

s = sierpinski_space()
print("connected?", is_connected(s).status)
print("path_connected?", is_path_connected(s).status)

# %% [markdown]
"""
```text
connected?       true
path_connected?  unknown
```

Sierpiński {0,1} uzayı bağlantılıdır: {1} açık, {0} kapalı; clopen bölme yok.
"""

# %% [markdown]
"""
### Örnek 5.2 — Ayrık Topoloji: Tamamen Bağlantısız
"""

# %%
from pytop import discrete_topology, is_connected, is_totally_disconnected

d = discrete_topology(1, 2, 3)
print("connected?", is_connected(d).status)
print("totally_disconn?", is_totally_disconnected(d).status)

# %% [markdown]
"""
```text
connected?          false
totally_disconn?    true
```

Ayrık topolojide {1} hem açık hem kapalı — clopen bölme var.
"""

# %% [markdown]
"""
### Örnek 5.3 — İndiscrete: Bağlantılı
"""

# %%
from pytop import indiscrete_topology, is_connected

ind = indiscrete_topology('a', 'b')
print("connected?", is_connected(ind).status)

# %% [markdown]
"""
```text
connected?  true
```
"""

# %% [markdown]
"""
### Örnek 5.4 — Gerçek Doğru ve [0,1]
"""

# %%
from pytop import real_line_metric, closed_unit_interval_metric
from pytop import is_connected, is_path_connected

rl = real_line_metric()
ui = closed_unit_interval_metric()
print("R connected?", is_connected(rl).status)
print("R path_connected?", is_path_connected(rl).status)
print("[0,1] connected?", is_connected(ui).status)
print("[0,1] path_connected?", is_path_connected(ui).status)

# %% [markdown]
"""
```text
R connected?          true
R path_connected?     true
[0,1] connected?      true
[0,1] path_connected? true
```
"""

# %% [markdown]
"""
### Örnek 5.5 — Kosonlu Topoloji
"""

# %%
from pytop import naturals_cofinite, is_connected, is_path_connected

nc = naturals_cofinite()
print("connected?", is_connected(nc).status)
print("path_connected?", is_path_connected(nc).status)

# %% [markdown]
"""
```text
connected?       true
path_connected?  unknown
```
"""

# %% [markdown]
"""
### Örnek 5.6 — Lokal Bağlantılılık
"""

# %%
from pytop import is_locally_connected

print("Sierpinski locally_connected?", is_locally_connected(s).status)
print("Discrete locally_connected?", is_locally_connected(d).status)
print("R locally_connected?", is_locally_connected(rl).status)

# %% [markdown]
"""
```text
Sierpinski locally_connected?  unknown
Discrete locally_connected?    unknown
R locally_connected?           unknown
```
"""

# %% [markdown]
"""
### Örnek 5.7 — Ark / Yol / Bağlantı Hiyerarşisi

Hiyerarşi **Ark-bağlantılı ⟹ Yol-bağlantılı ⟹ Bağlantılı** idi. pytop bu üç
düzeyi `is_arc_connected`, `is_path_connected` ve `is_connected` ile ayrı ayrı
sorgular. Bazı uzaylarda bir düzey `true`, diğeri `unknown` döner — pytop
yalnızca *kanıtlayabildiğini* kesin bildirir.
"""

# %%
from pytop import (
    indiscrete_topology, real_line_metric, discrete_topology,
    is_arc_connected, is_path_connected, is_connected,
)

for name, sp in [("Indiscrete(2)", indiscrete_topology(1, 2)),
                 ("R", real_line_metric()),
                 ("Discrete(3)", discrete_topology(1, 2, 3))]:
    print(f"{name:14s} connected={is_connected(sp).status:6s} "
          f"path={is_path_connected(sp).status:8s} arc={is_arc_connected(sp).status}")

# %% [markdown]
"""
```text
Indiscrete(2)  connected=true   path=unknown  arc=true
R              connected=true   path=true     arc=unknown
Discrete(3)    connected=false  path=unknown  arc=false
```

Ayrık uzayda üç düzey de başarısız (`false`); birden çok nokta clopen bölme verir.
`unknown` çıktıları, ilgili düzey için pytop'un kesin bir tanık üretemediğini
gösterir — `false` değildir.
"""

# %% [markdown]
"""
### Örnek 5.8 — Tek Çağrıyla Çoklu Sorgu: `analyze_connectedness`

Her özelliği ayrı fonksiyonla çağırmak yerine `analyze_connectedness(space,
property_name)` tek bir dağıtıcı (dispatcher) sunar. Geçerli `property_name`
değerleri: `"connected"`, `"path_connected"`, `"locally_connected"`,
`"totally_disconnected"`, `"arc_connected"`.
"""

# %%
from pytop import analyze_connectedness, sierpinski_space

s = sierpinski_space()
for prop in ["connected", "path_connected", "locally_connected",
             "totally_disconnected", "arc_connected"]:
    r = analyze_connectedness(s, prop)
    print(f"  {prop:22s}: {r.status}")

# %% [markdown]
"""
```text
  connected             : true
  path_connected        : unknown
  locally_connected     : unknown
  totally_disconnected  : false
  arc_connected         : false
```

Sierpiński bağlantılıdır (`connected: true`) ve tamamen bağlantısız değildir
(`totally_disconnected: false`) — tutarlı, çünkü bağlantılı bir uzay (tek
noktadan büyükse) tamamen bağlantısız olamaz.
"""

# %% [markdown]
"""
### Örnek 5.9 — Clopen Ayrılmayı Elle Kurmak

Bir clopen bölmenin bağlantısızlığı nasıl ürettiğini doğrudan `make_topology` ile
kurarak görelim: $X=\{1,2,3,4\}$ üzerinde $U=\{1,2\}$ ve $V=\{3,4\}$ açık
kümelerini taban alırsak, ikisi de hem açık hem (birbirinin tümleyeni olduğundan)
kapalıdır — yani $X = U \sqcup V$ bir clopen ayrılmadır.
"""

# %%
from pytop import make_topology, is_connected, is_totally_disconnected

X = make_topology({1, 2, 3, 4}, {1, 2}, {3, 4})   # clopen bölme: {1,2} | {3,4}
print("split connected?", is_connected(X).status)
print("split totally_disconn?", is_totally_disconnected(X).status)

Y = make_topology({1, 2, 3}, {1}, {1, 2}, {1, 2, 3})  # ic ice (nested), bölme yok
print("nested connected?", is_connected(Y).status)

# %% [markdown]
"""
```text
split connected?           false
split totally_disconn?     false
nested connected?          true
```

İlk uzay bağlantısızdır (clopen bölme var) ama *tamamen* bağlantısız değildir —
$\{1,2\}$ alt kümesi içinde clopen bölme bulunmaz, dolayısıyla tek-noktadan büyük
bağlantılı bir parça vardır. İkinci uzay iç içe (nested) açık kümelerden oluşur;
hiçbir gerçek clopen bölme kurulamaz, bu yüzden bağlantılıdır.

---
"""

# %% [markdown]
"""
## 6. Alıştırmalar
"""

# %% [markdown]
"""
### Kodlama

K1. `make_topology({1,2,3}, {1}, {2,3})` topolojisi için `is_connected` hesaplayın.
    {1} ve {2,3} clopen bölme gösteriyor mu?

K2. `finite_chain_space(4)` zincirinin bağlantılı olup olmadığını kontrol edin.

K3. `two_point_discrete_space()` ve `two_point_indiscrete_space()` üzerinde
    `is_connected`, `is_path_connected` karşılaştırın.

K4. `indiscrete_topology(1,2)` ve `real_line_metric()` için `is_arc_connected` ve
    `is_path_connected` çıktılarını karşılaştırın. Hangi uzayda hangi düzey
    `unknown` döner? (İpucu: Örnek 5.7.)

K5. `discrete_topology(1,2,3)` için `analyze_connectedness(d, "connected")` ve
    `analyze_connectedness(d, "totally_disconnected")` çağırın. İki sonucun neden
    birbiriyle tutarlı olduğunu açıklayın. (İpucu: Örnek 5.8.)
"""

# %% [markdown]
"""
### Teori

T1. Bağlantılı + sürekli ⟹ görüntü bağlantılı teoremini ispatlayın.

T2. Yol-bağlantılı ⟹ bağlantılı implicasyonunu ispatlayın.

T3. Topolojist sinüs eğrisinin neden bağlantılı *ama* yol-bağlantılı olmadığını
    açıklayın. Dikey segmentten eğriye giden sürekli bir yolun varlığını varsayıp
    çelişkiye ulaşın. (İpucu: §1'deki karşı-örnek kutusu + sinüs eğrisi figürü.)
"""
