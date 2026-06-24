# %% [markdown]
"""
# Bölüm 6 — Ayrılma Aksiyomları
"""

# %% [markdown]
"""
## 1. Konu

Ayrılma aksiyomları, bir topolojik uzaydaki noktaların ve kapalı kümelerin birbirinden
açık kümeler aracılığıyla ne ölçüde "ayrılabildiğini" ölçer.

> **💡 Sezgi:** Ayrılma aksiyomlarını bir mikroskobun çözünürlük kademeleri gibi düşünün: T0'da iki noktayı *en az bir yönden* ayırt edebilirsiniz; T1'de her iki yönden; T2'de noktaları çakışmayan iki ayrı "görüş alanına" koyabilirsiniz; T3 ve T4'te artık nokta–kapalı küme ve kapalı–kapalı çiftleri bile ayrışır.
"""

# %% [markdown]
"""
### 1.1 Aksiyomlar Tablosu

| Aksiyom | İsim | Koşul |
|---------|------|-------|
| **T0** | Kolmogorov | $\forall x \neq y$: $\exists U \in \tau$, $x \in U, y \notin U$ veya tersi |
| **T1** | Fréchet | $\forall x \neq y$: $\exists U, V \in \tau$, $x \in U \setminus V$, $y \in V \setminus U$ |
| **T2** | Hausdorff | $\forall x \neq y$: $\exists U, V \in \tau$, $x \in U$, $y \in V$, $U \cap V = \emptyset$ |
| **T2.5** | Urysohn | $\forall x \neq y$: $\exists U, V \in \tau$, $x \in U$, $y \in V$, $\overline{U} \cap \overline{V} = \emptyset$ |
| **T3** | Regüler | T1 + $\forall x$, kapalı $C \not\ni x$: $\exists U, V \in \tau$, $x \in U$, $C \subseteq V$, $U \cap V = \emptyset$ |
| **T3.5** | Tychonoff | T1 + $\forall x$, kapalı $C \not\ni x$: $\exists f: X \to [0,1]$ sürekli, $f(x)=0$, $f|_C=1$ |
| **T4** | Normal | T1 + $\forall C, D$ kapalı, $C \cap D = \emptyset$: $\exists U, V \in \tau$, $C \subseteq U$, $D \subseteq V$, $U \cap V = \emptyset$ |
| **Tamamen normal** | Completely normal | Kalıtsal T4 |
| **Mükemmel normal** | Perfectly normal | T4 + kapalı kümeler $G_\delta$ |

**Sıralama:** T4 $\Rightarrow$ T3.5 $\Rightarrow$ T3 $\Rightarrow$ T2.5 $\Rightarrow$ T2 $\Rightarrow$ T1 $\Rightarrow$ T0

> **⚠️ Dikkat — sık hata:** T3 ve T4'ün tanımı kaynaktan kaynağa değişir. Bu kılavuzda ve `pytop`'ta: **T3 = T1 + regüler, T4 = T1 + normal**. Fark gerçektir: iki noktalı indirgenmiş uzay regüler *ve* normaldir, ama T1 olmadığından T3 de T4 de değildir.
"""

# %%
from pytop import two_point_indiscrete_space, is_regular, is_normal, is_t3, is_t4

tp = two_point_indiscrete_space()
print("regular:", is_regular(tp).status, "| normal:", is_normal(tp).status)
print("t3     :", is_t3(tp).status, "| t4    :", is_t4(tp).status)

# %% [markdown]
"""
```text
regular: true | normal: true
t3     : false | t4    : false
```

![Hausdorff: x ve y ayrık U, V açıklarıyla ayrılır](../assets/ch06/fig_ch06_t2_ayirma.png)

![Regülerlik: nokta ile kapalı küme ayrık açıklarla ayrılır](../assets/ch06/fig_ch06_t3_regulerlik.png)

> **🚫 Karşı-örnek:** Hiçbir ayrılma aksiyomunu sağlamayan uzay: iki noktalı indirgenmiş uzay. Açıklar yalnız $\emptyset$ ve $X$ olduğundan iki noktayı ayıran *hiçbir* açık yoktur — uzay T0 bile değildir.

> **Neden bu konu?** T0–T4 hiyerarşisi Hausdorff gibi güçlü özelliklerin tam anlaşılması için gerekli; kümeler arası ayrışma fikrinden doğar.

> 🔍 **Kendin dene:** Sierpiński'nin T0 ama T1 olmadığını `is_t0`/`is_t1` ile doğrulayın.

> ⚠️ **Sık hata:** `is_t2 True` iken `is_t1 False` olamaz; hiyerarşi sıkı içermedir.

> ↗️ **Bkz.:** Bölüm 4 (topoloji), Bölüm 7 (kompakt Hausdorff → normal).

> 💭 **Öz-yansıtma:** T2 (Hausdorff) neden önemli? Hangi ispatlarda özellikle kullanılır?

---
"""

# %% [markdown]
"""
## 2. Teoremler

**Teorem 2.1 (Ayrılma Zinciri).**
T4 $\Rightarrow$ T3.5 $\Rightarrow$ T3 $\Rightarrow$ T2.5 $\Rightarrow$ T2 $\Rightarrow$ T1 $\Rightarrow$ T0.
Tersi genel olarak doğru değildir.

**Rehberli Kanıt (model halka, T2 ⇒ T1):** $x\neq y$ için ayrık $U\ni x$, $V\ni y$ al; $U\cap V=\emptyset$ olduğundan $y\notin U$ ve $x\notin V$ — iki yönlü ayrım hazır. T1 ⇒ T0: iki yönlü ayrım tek yönlüyü içerir. Kalan halkalar Alıştırma T1'de.

![T4'ten T0'a implikasyon zinciri; terslerin geçmediği karşı-örnekler](../assets/ch06/fig_ch06_implikasyon.png)

**Teorem 2.2 (Urysohn Fonksiyon Teoremi).**
$X$ normal ise ve $C, D$ disjoint kapalı kümeler ise, $f: X \to [0,1]$ sürekli bir fonksiyon
vardır: $f|_C \equiv 0$, $f|_D \equiv 1$.

> **İspat eskizi.** Normallikle $C \subseteq U_{1/2}$, $\overline{U_{1/2}} \cap D = \emptyset$ olan açık $U_{1/2}$ seç. Aynı adımı tekrarlayıp her ikili kesir $q = k/2^n \in [0,1]$ için, $p < q \Rightarrow \overline{U_p} \subseteq U_q$ koşulunu sağlayan iç-içe açıklar $\{U_q\}$ ailesi kur (normallik her ekleme adımını mümkün kılar). Sonra $f(x) = \inf\{q : x \in U_q\}$ (hiç içermiyorsa $1$) tanımla; iç-içe geçme süreklilik verir, $C$ üzerinde $0$, $D$ üzerinde $1$ alınır. ∎

![Urysohn fonksiyonu: C üzerinde 0, D üzerinde 1 değerini alan sürekli f](../assets/ch06/fig_ch06_urysohn.png)

**Teorem 2.3 (Tietze Genişleme Teoremi).**
$X$ normal ise her kapalı $A \subseteq X$ üzerinde $f: A \to [a,b]$ süreklisi
tüm $X$'e sürekli genişletilebilir.

**Teorem 2.4 (Tychonoff Karakterizasyonu).**
$X$, T3.5'tir $\iff$ $X$, bir küp $[0,1]^I$'nın içine homeomorf gömülebilir.

> **İspat eskizi.** ($\Leftarrow$) $[0,1]^I$ bir kompakt Hausdorff çarpımdır, dolayısıyla T3.5'tir; T3.5 kalıtsaldır, alt-uzaya geçer. ($\Rightarrow$) $X$ tam regüler ise $I = C(X,[0,1])$ (tüm sürekli $[0,1]$-değerli fonksiyonlar) indeks kümesini al; değerlendirme gömmesi $e(x) = (f(x))_{f\in I}$ tanımla. Tam regülerlik $e$'nin birebir ve homeomorfik bir gömme olmasını sağlar — her nokta–kapalı çift bir $f$ ile ayrıldığından. ∎

**Teorem 2.5 (Sonlu T1 ⟺ Ayrık).**
Sonlu bir uzayda T1 $\iff$ ayrık topoloji.

**Rehberli Kanıt:**
1. (⇒) T1 gereği her $y\neq x$ için $y\in U_y$, $x\notin U_y$ olan açık $U_y$ vardır; $X\setminus\{x\}=\bigcup_{y\neq x}U_y$ açıktır, yani $\{x\}$ kapalıdır.
2. Herhangi $A\subseteq X$, *sonlu* sayıda tekilin birleşimi olarak kapalıdır.
3. Her $A$ kapalı ise her $X\setminus A$ açıktır; topoloji ayrıktır.
4. (⇐) Ayrık topolojide her $\{x\}$ açıktır; $x\neq y$ çifti $\{x\}$ ve $\{y\}$ ile iki yönlü ayrılır.

Sonsuzlukta 2. adım çöker: sonsuz birleşim kapalılığı korumaz — kosonlu $\mathbb{N}$ tam bu nedenle T1 olup ayrık değildir.

**Teorem 2.6 (Kompakt + Hausdorff $\Rightarrow$ T4).**
Her kompakt Hausdorff uzay normaldir (T4).

> **İspat eskizi.** Önce "kompakt Hausdorff $\Rightarrow$ regüler"i kur: $x \notin C$ (kapalı, dolayısıyla kompakt) ise, her $c \in C$ için Hausdorff ayrık $U_c \ni x$, $V_c \ni c$ verir; $\{V_c\}$ $C$'yi örter, kompaktlıkla sonlu alt-örtü $V_{c_1},\dots,V_{c_n}$ al. $U = \bigcap U_{c_i}$ ve $V = \bigcup V_{c_i}$ aradığın ayrık açıkları verir. Sonra aynı argümanı bir nokta yerine ikinci bir kapalı (kompakt) $D$ kümesine uygula: her $d \in D$ için yukarıdaki regülerlik ayrık $U_d \supseteq C$, $W_d \ni d$ verir; $D$ kompakt olduğundan sonlu alt-örtüyle $C$ ve $D$ ayrık açıklara konur — normallik tam budur. ∎

Bu, Bölüm 7'deki "kompakt + Hausdorff $\Rightarrow$ T4" teoreminin ayrılma-aksiyomu tarafıdır; kompaktlık, sonsuz Hausdorff ayrımlarını *sonlu* sayıya indirgeyerek normalliği mümkün kılar.

---
"""

# %% [markdown]
"""
## 3. Algoritmalar
"""

# %% [markdown]
"""
### 3.1 Sonlu T0 Karar Prosedürü

```
KontrolT0(X, τ):
    for each pair (x, y) with x ≠ y:
        if not (∃U∈τ: x∈U ∧ y∉U) and not (∃U∈τ: y∈U ∧ x∉U):
            return False
    return True
```

**Karmaşıklık:** $O(|X|^2 \cdot |\tau|)$.
"""

# %% [markdown]
"""
### 3.2 Sonlu T2 (Hausdorff) Karar Prosedürü

```
KontrolT2(X, τ):
    for each pair (x, y) with x ≠ y:
        if not ∃ U,V∈τ: x∈U ∧ y∈V ∧ U∩V=∅:
            return False
    return True
```

**Karmaşıklık:** $O(|X|^2 \cdot |\tau|^2)$.
"""

# %% [markdown]
"""
### 3.3 check_tychonoff — 5-Katmanlı Prosedür

1. T3'ü doğrula
2. `completely_regular` tanığı ara
3. T3.5 onaylama (T3 + completely_regular)
4. Etiket tabanlı geri çekilme
5. Sonuç döndür

**İz Sürme: T0 Prosedürü Sierpiński Üzerinde.** $X=\{0,1\}$, $\tau=\{\emptyset,\{1\},X\}$:

| Çift $(x,y)$ | Denenen $U$ | $x\in U \wedge y\notin U$? | $y\in U \wedge x\notin U$? | Karar |
|--------------|-------------|------------------------------|------------------------------|-------|
| $(0,1)$ | $\emptyset$ | hayır | hayır | devam |
| $(0,1)$ | $\{1\}$ | hayır | **evet** | çift ayrıldı |
| — | — | — | — | tüm çiftler bitti → **true** |

Tek çift tek açıkla ayrıldığından prosedür $O(1)$ adımda biter; genel sınır $O(|X|^2\cdot|\tau|)$'dur.

---
"""

# %% [markdown]
"""
## 4. pytop API
"""

# %%
from pytop import (
    is_t0, is_t1, is_t2, is_t2_5, is_t3, is_t4,
    is_hausdorff, is_regular, is_normal, is_perfectly_normal,
    separation_chain, analyze_separation,
)

# %% [markdown]
"""
| Fonksiyon | İmza | Döndürür |
|-----------|------|---------|
| `is_t0` … `is_t4` | `(space)` | `Result` |
| `is_hausdorff` | `(space)` | `Result` |
| `is_regular` | `(space)` | `Result` |
| `is_normal` | `(space)` | `Result` |
| `is_perfectly_normal` | `(space)` | `Result` |
| `separation_chain` | `(space)` | `dict[str, Result]` |
| `analyze_separation` | `(space, property='hausdorff')` | `Result` |

**`separation_chain` döndürür:** `{'t0': Result, 't1': Result, 'hausdorff': Result, ...}` — her aksiyom için ayrı `Result`.

**`analyze_separation(space, prop)` döndürür:** `Result` — `status='true'` ise uzay `prop`'u sağlar.

> **🎯 Neden önemli?** `is_*` yüklemleri ham `bool` değil, `.status` alanı `true` / `false` / `unknown` olabilen bir `Result` döndürür. Üçüncü değer dürüstlüktür: ör. T3.5 (Tychonoff) sürekli fonksiyonlarla tanımlanır ve sonlu açık-küme taramasıyla karar verilemez; `separation_chain` bu durumda `tychonoff: unknown` raporlar.

---
"""

# %% [markdown]
"""
## 5. Örnekler
"""

# %% [markdown]
"""
### Örnek 5.1 — Sierpiński: T0 ✓, T1 ✗
"""

# %%
from pytop import sierpinski_space, is_t0, is_t1, is_t2

s = sierpinski_space()
print("T0:", is_t0(s).status)
print("T1:", is_t1(s).status)
print("T2:", is_t2(s).status)

# %% [markdown]
"""
```text
T0: true
T1: false
T2: false
```

**Ne oldu?** `T0: true` — $(0,1)$ çifti için $\{1\}$ açığı $1$'i içerir, $0$'ı dışlar. `T1: false` — ters yön yok: $0$'ı içerip $1$'i dışlayan açık küme yoktur. Sierpiński, zincirin "T0'da takılan" kanonik örneğidir.
"""

# %% [markdown]
"""
### Örnek 5.2 — İndirgenmiş: Hiçbir T Aksiyomu Yok
"""

# %%
from pytop import indiscrete_topology, is_t0, is_t1

ind = indiscrete_topology('a', 'b')
print("T0:", is_t0(ind).status)
print("T1:", is_t1(ind).status)

# %% [markdown]
"""
```text
T0: false
T1: false
```

**Ne oldu?** $\tau = \{\emptyset, X\}$; $a$ ve $b$'yi birbirinden ayıran açık küme yoktur — T0 bile sağlanamaz.
"""

# %% [markdown]
"""
### Örnek 5.3 — Kosonlu $\mathbb{N}$: T1 ✓, T2 ✗
"""

# %%
from pytop import naturals_cofinite, is_t0, is_t1, is_t2

nc = naturals_cofinite()
print("T0:", is_t0(nc).status)
print("T1:", is_t1(nc).status)
print("T2:", is_t2(nc).status)

# %% [markdown]
"""
```text
T0: true
T1: true
T2: false
```

**Ne oldu?** `T1: true` — her $n$ için $\mathbb{N}\setminus\{n\}$ kosonludur, dolayısıyla açıktır. `T2: false` — boş olmayan iki kosonlu açık daima kesişir: $\mathbb{N}$ sonsuz olduğundan $U\cap V\neq\emptyset$. Bu örnek, Bölüm 4 K1'in "neden sonsuz taşıyıcı gerekir" sorusunun cevabıdır.
"""

# %% [markdown]
"""
### Örnek 5.4 — Ayrılma Zinciri: Ayrık Topoloji
"""

# %%
from pytop import discrete_topology, separation_chain

d = discrete_topology(1, 2, 3)
chain = separation_chain(d)
for prop, result in chain.items():
    print(f"  {prop:20s}: {result.status}")

# %% [markdown]
"""
```text
  t0                  : true
  t1                  : true
  hausdorff           : true
  urysohn             : true
  t3                  : true
  tychonoff           : true
  t4                  : true
  completely_normal   : true
  perfectly_normal    : true
```

**Ne oldu?** Ayrık uzayda her tekil açık olduğundan her ayırma görevi tekil komşuluklarla çözülür; dokuz yüklemin tümü `true` döner. `separation_chain`'in anahtar sırası zincirin mantıksal sırasıdır — bir uzayın "nerede takıldığını" yukarıdan aşağı okuyabilirsiniz.
"""

# %% [markdown]
"""
### Örnek 4.5 — Regüler Ama T3 Değil: Konvansiyon Testi
"""

# %%
from pytop import two_point_indiscrete_space, is_regular, is_normal, is_t3, is_t4

tp = two_point_indiscrete_space()
print("regular:", is_regular(tp).status, "| normal:", is_normal(tp).status)
print("t3     :", is_t3(tp).status, "| t4    :", is_t4(tp).status)

# %% [markdown]
"""
Çıktı:

```text
regular: true | normal: true
t3     : false | t4    : false
```

**Ne oldu?** İndirgenmiş iki noktalı uzayda kapalı kümeler yalnız $\emptyset$ ve $X$'tir; ayırma koşullarının öncülü hiç gerçekleşmez, koşullar boş yere sağlanır: `regular` ve `normal` `true`. Ama uzay T1 olmadığından `t3` ve `t4` `false` kalır.
"""

# %% [markdown]
"""
### Örnek 5.5 — Sierpiński Zinciri
"""

# %%
from pytop import sierpinski_space, separation_chain

s = sierpinski_space()
for prop, result in separation_chain(s).items():
    print(f"  {prop:20s}: {result.status}")

# %% [markdown]
"""
```text
  t0                  : true
  t1                  : false
  hausdorff           : false
  urysohn             : false
  t3                  : false
  tychonoff           : unknown
  t4                  : false
  completely_normal   : false
  perfectly_normal    : false
```

**Çıktı Açıklaması:** Sierpiński yalnızca T0'ı sağlar. `tychonoff: unknown` — tam regülerlik
sonlu uzayda kesin olarak belirlenemiyor (sembolik çıkarım sınırı); bu değerin anlamı için "Neden önemli?" kutusuna bakın.
"""

# %% [markdown]
"""
### Örnek 5.6 — analyze_separation
"""

# %%
from pytop import discrete_topology, sierpinski_space, real_line_metric, analyze_separation

d = discrete_topology(1, 2, 3)
s = sierpinski_space()
rl = real_line_metric()

print("Real line Hausdorff?:", analyze_separation(rl).status)
print("Discrete Hausdorff? :", analyze_separation(d).status)
print("Sierpinski Hausdorff?:", analyze_separation(s).status)
print("Sierpinski T0?       :", analyze_separation(s, 't0').status)

# %% [markdown]
"""
```text
Real line Hausdorff?: true
Discrete Hausdorff? : true
Sierpinski Hausdorff?: false
Sierpinski T0?       : true
```

**Çıktı Açıklaması:** `analyze_separation(space, property)` tek bir aksiyom için sorgu yapar.
Varsayılan `'hausdorff'`'tur. `status='true'` → uzay o aksiyomu sağlar; sonuçlar "Neden önemli?" kutusundaki `Result` türüyle döner.
"""

# %% [markdown]
"""
### Örnek 5.7 — Dışlanan-Nokta Topolojisi: İkinci Bir "T0'da Takılan"

Sierpiński, T0-olup-T1-olmayan tek örnek değildir. $X = \{0,1,2\}$ üzerinde
**dışlanan-nokta topolojisi** ($0$ dışlanır): bir küme, ya $0$'ı içermez ya da
$X$'in kendisidir.
"""

# %%
from pytop import excluded_point_topology, is_t0, is_t1, separation_chain

ep = excluded_point_topology(3, 0)   # X = {0,1,2}, dışlanan nokta 0
print("T0:", is_t0(ep).status, "| T1:", is_t1(ep).status)
for prop, result in separation_chain(ep).items():
    print(f"  {prop:20s}: {result.status}")

# %% [markdown]
"""
```text
T0: true | T1: false
  t0                  : true
  t1                  : false
  hausdorff           : false
  urysohn             : false
  t3                  : false
  tychonoff           : false
  t4                  : false
  completely_normal   : false
  perfectly_normal    : false
```

**Ne oldu?** `T0: true` — $1$ ve $2$, $\{1\}$ / $\{2\}$ gibi $0$-içermeyen açıklarla iki yönlü ayrılır; $0$ ile herhangi bir nokta arasında ise $0$'ı dışlayan açık tek yönlü ayrım verir. `T1: false` — $0$'ı içeren tek açık $X$'tir, dolayısıyla $0$'ı içerip başka noktayı dışlayan açık yoktur: $\{0\}$ kapalı değildir. Sierpiński'den farklı bir mekanizmayla yine zincir T0'da takılır.
"""

# %% [markdown]
"""
### Örnek 5.8 — Metrik Uzaylar: Zincirin Tepesine Kadar

Her metrik uzay normaldir (T4) ve dolayısıyla zincirin tüm üst basamaklarını
sağlar. Bunu $\mathbb{R}$ ve $[0,1]$ üzerinde gözlemleyelim.
"""

# %%
from pytop import real_line_metric, closed_unit_interval_metric
from pytop import is_t2, is_urysohn, is_t3, is_t4

rl = real_line_metric()
ui = closed_unit_interval_metric()
print("R         t2/urysohn/t3/t4:", is_t2(rl).status, is_urysohn(rl).status, is_t3(rl).status, is_t4(rl).status)
print("[0,1]     t2/urysohn/t3/t4:", is_t2(ui).status, is_urysohn(ui).status, is_t3(ui).status, is_t4(ui).status)

# %% [markdown]
"""
```text
R         t2/urysohn/t3/t4: true true true true
[0,1]     t2/urysohn/t3/t4: true true true true
```

**Ne oldu?** Metrik mesafenin kendisi bir ayırıcıdır: ayrık kapalı kümeler $C, D$ için $f(x) = d(x,C) / (d(x,C) + d(x,D))$ sürekli Urysohn fonksiyonunu doğrudan verir — yani metrik uzaylar yalnız T2 değil, T4'e kadar her aksiyomu sağlar (Teorem 2.2'nin metrik durumda elle yazılabilen tanığı). Bu, ayrılma zincirinin "sonlu/sembolik" örneklerle "metrik" örnekler arasındaki keskin farkını gösterir.

---
"""

# %% [markdown]
"""
## 6. Alıştırmalar
"""

# %% [markdown]
"""
### Kodlama Alıştırmaları

**K1.** `cofinite_topology('a','b','c')` ile üç noktalı kosonlu uzayı kurun; topolojisini ve etiketlerini yazdırın, `is_t1` ve `is_t2` ile test edin. Gözlem: sonlu bir kümede kosonlu topoloji ayrık topolojiyle çakışır. T1 olup Hausdorff olmayan bir örnek için taşıyıcının neden sonsuz olması gerektiğini açıklayın.
*İpucu: Önce açıkları listeleyin: $\emptyset,\{1\},\{2\},\{1,2\},X$.*
*(Çözüm: [solutions.md](solutions.md) → Bölüm 6 / K1)*

**K2.** `finite_chain_space(3)` üzerinde en yüksek sağlanan aksiyomu bulun.
*İpucu: Çıktıda `true` olan en güçlü anahtarı arayın; `unknown` değerlerini "Neden önemli?" kutusuna göre yorumlayın.*
*(Çözüm: [solutions.md](solutions.md) → Bölüm 6 / K2)*

**K3.** `two_point_indiscrete_space()` üzerinde T0, T1, T2 test edin.
*İpucu: Tek boş olmayan açık $X$ iken herhangi bir çift nasıl ayrılabilir?*
*(Çözüm: [solutions.md](solutions.md) → Bölüm 6 / K3)*

**K4.** `excluded_point_topology(4, 0)` (yani $X=\{0,1,2,3\}$, dışlanan nokta $0$) üzerinde `separation_chain` çalıştırın; sağlanan en yüksek aksiyomu belirleyin ve neden T1'in düştüğünü açıklayın.
*İpucu: $0$'ı içeren tek açık $X$'tir; $\{0\}$ kapalı mı?*
*(Çözüm: [_solutions_ch06.md](_solutions_ch06.md) → Bölüm 6 (ek) / K4)*
"""

# %% [markdown]
"""
### Teori Alıştırmaları

**T1.** T2 $\Rightarrow$ T1 $\Rightarrow$ T0 implikasyonlarını kanıtlayın.
*İpucu: T2 ⇒ T1: ayrık $U\ni x$, $V\ni y$ verildiğinde $U$, $y$'yi; $V$, $x$'i dışlar — iki yönlü ayrım hazır.*
*(Çözüm: [solutions.md](solutions.md) → Bölüm 6 / T1)*

**T2.** Sonlu uzayda T1 ⟺ ayrık topoloji olduğunu gösterin.
*İpucu: T1 ⇒ tekiller kapalı ⇒ (sonlu birleşim) her alt küme kapalı ⇒ her alt küme açık.*
*(Çözüm: [solutions.md](solutions.md) → Bölüm 6 / T2)*

**T3.** Her metrik uzayın normal (T4) olduğunu kanıtlayın.
*İpucu: Ayrık kapalı $C, D$ için $f(x) = d(x,C)/(d(x,C)+d(x,D))$ sürekli Urysohn fonksiyonunu yazın; $f^{-1}([0,\tfrac12))$ ve $f^{-1}((\tfrac12,1])$ aradığınız ayrık açıklardır.*
*(Çözüm: [_solutions_ch06.md](_solutions_ch06.md) → Bölüm 6 (ek) / T3)*
"""
