# %% [markdown]
"""
# Bölüm 5 — Yüklemler ve Altküme Operatörleri
"""

# %% [markdown]
"""
## 1. Konu
"""

# %% [markdown]
"""
### 1.1 Altküme Yüklemleri

Bir $(X, \tau)$ topolojik uzayı ve $A \subseteq X$ alınalım:

| Yüklem | Tanım |
|--------|-------|
| **Açık (open)** | $A \in \tau$ |
| **Kapalı (closed)** | $X \setminus A \in \tau$ |
| **Clopen** | $A \in \tau$ ve $X \setminus A \in \tau$ |
| **Yoğun (dense)** | Her boş olmayan $U \in \tau$ için $U \cap A \neq \emptyset$; eşdeğer: $\overline{A} = X$ |
| **Hiçbiryerde-yoğun (nowhere dense)** | $\mathrm{int}(\overline{A}) = \emptyset$ |
"""

# %% [markdown]
"""
### 1.2 Altküme Operatörleri

| Operatör | Gösterim | Tanım |
|----------|----------|-------|
| Kapanış | $\overline{A} = \mathrm{cl}(A)$ | $A$'yı içeren en küçük kapalı küme |
| İç | $A^\circ = \mathrm{int}(A)$ | $A$'ya dahil en büyük açık küme |
| Sınır | $\partial A = \mathrm{bd}(A)$ | $\overline{A} \setminus A^\circ$ |
| Türev kümesi | $A' = d(A)$ | $A$'nın birikme noktaları kümesi |

**Birikme noktası:** $x \in A'$ ⟺ her $U \ni x$ açık için $U \cap (A \setminus \{x\}) \neq \emptyset$.

> 💡 **Sezgi:** Bir $A$ kümesini, $X$ üzerinde duran bir "boya lekesi" gibi düşünün.
> **İç** $A^\circ$, lekenin tamamen içine sığabildiğiniz açık bir komşuluğunuz olan
> noktalardır — "rahatça içerideyim" bölgesi. **Kapanış** $\mathrm{cl}(A)$, lekeye
> dokunan her noktayı ekler — leke artı onun "gölgesi". **Sınır** $\partial A$ ise
> tam kenardır: her açık komşuluğu hem $A$'dan hem $X \setminus A$'dan kesen noktalar.
> Bu üçlü, $X$'i ayrık üç parçaya böler: iç, sınır ve **dış** $\mathrm{ext}(A) =
> (X \setminus A)^\circ$ (bkz. Şekil aşağıda).

![A kümesinin içi (yeşil), sınırı (turuncu) ve dışı (mavi); kapanış kırmızı çerçeve](../assets/ch05/fig_ch05_ic_kapanis_sinir.png)
"""

# %% [markdown]
"""
### 1.3 Komşuluk Sistemi N(x)

$x \in X$ için:
$$N(x) = \{N \subseteq X : \exists U \in \tau,\, x \in U \subseteq N\}$$

**Komşuluk Aksiyomları (N1–N4):**
- **(N1)** $x \in N$, her $N \in N(x)$ için
- **(N2)** $X \in N(x)$
- **(N3)** $N_1, N_2 \in N(x) \Rightarrow N_1 \cap N_2 \in N(x)$
- **(N4)** $N \in N(x)$, $N \subseteq M \Rightarrow M \in N(x)$

> **Neden bu konu?** Kapanış, iç ve sınır işlemleri topolojik analizin temel araçları; pytop bunları sembolik ve sonlu uzaylarda hesaplar.

> 🔍 **Kendin dene:** `cl({0})` ile `cl({1})`'i Sierpiński uzayında hesaplayın; hangisi daha büyük?

> ⚠️ **Sık hata:** `closure_of_subset` bir nokta değil küme alır; `cl(0)` değil `cl({0})`.

> ↗️ **Bkz.:** Bölüm 4 (topoloji tanımı), Bölüm 6 (T1: nokta kapanışları kapalı).

> 💭 **Öz-yansıtma:** İç küme her zaman kapalı olur mu? Sınır boş olabilir mi?

---
"""

# %% [markdown]
"""
## 2. Teoremler

**Teorem 2.1 (Kuratowski Kapanış Aksiyomları).**
$\mathrm{cl}: \mathcal{P}(X) \to \mathcal{P}(X)$ operatörü şu dört özelliği sağlar
(ve yalnızca bunları sağlayan her operatör bir topoloji belirler):
- **(K1)** $\mathrm{cl}(\emptyset) = \emptyset$
- **(K2)** $A \subseteq \mathrm{cl}(A)$
- **(K3)** $\mathrm{cl}(\mathrm{cl}(A)) = \mathrm{cl}(A)$ (kuvvet-idemp.)
- **(K4)** $\mathrm{cl}(A \cup B) = \mathrm{cl}(A) \cup \mathrm{cl}(B)$

![Kuratowski aksiyomları K1–K4 ve bunların tek bir topoloji belirlemesi](../assets/ch05/fig_ch05_kuratowski.png)

> **İspat eskizi.** Kapanış, $A$'yı içeren tüm kapalı kümelerin kesişimidir:
> $\mathrm{cl}(A) = \bigcap \{C : C \text{ kapalı},\, A \subseteq C\}$. **(K1)** $\emptyset$
> zaten kapalı, en küçük kapalı üst-küme kendisidir. **(K2)** kesişimdeki her $C \supseteq A$
> içerdiğinden $A \subseteq \mathrm{cl}(A)$. **(K3)** $\mathrm{cl}(A)$ kapalı bir küme;
> kapalı bir kümenin kapanışı kendisidir, dolayısıyla idempotenttir. **(K4)** $\subseteq$ yönü
> monotonluktan; $\supseteq$ yönü $\mathrm{cl}(A) \cup \mathrm{cl}(B)$'nin $A \cup B$'yi içeren
> bir kapalı küme olmasından gelir. pytop'ta bu dört aksiyom `kuratowski_closure_check` ile
> sonlu bir uzayda doğrudan doğrulanır (Örnek 5.7).

**Teorem 2.2 (İç-Kapanış Dualitesi).**
Her $A \subseteq X$ için:
$$A^\circ = X \setminus \mathrm{cl}(X \setminus A), \qquad
  \mathrm{cl}(A) = X \setminus \mathrm{int}(X \setminus A).$$

> **İspat eskizi.** $A^\circ$ tanım gereği $A$'ya dahil **en büyük açık** kümedir;
> $\mathrm{cl}(B)$ ise $B$'yi içeren **en küçük kapalı** kümedir. Tümleme alma açık ↔ kapalı
> ve "en büyük" ↔ "en küçük" ile $\subseteq$ ilişkisini ters çevirir. $B = X \setminus A$
> alın: $X \setminus A$'yı içeren en küçük kapalı kümenin tümleyeni, $A$'ya dahil en büyük açık
> kümedir; yani $A^\circ = X \setminus \mathrm{cl}(X \setminus A)$. İkinci eşitlik $A \mapsto
> X \setminus A$ ikamesiyle simetrik olarak çıkar. **Sonuç:** iç ve kapanış, tümleme altında
> birbirinin ikizidir — birini hesaplamak diğerini bedavaya verir.

**Teorem 2.3 (Komşuluk Sistemi Round-Trip).**
Bir topolojiden türetilen komşuluk sistemi $\{N(x)\}_{x \in X}$, N1–N4'ü sağlar.
Tersine, N1–N4'ü sağlayan her aile $\tau = \{U : \forall x \in U, U \in N(x)\}$
şeklinde tek bir topolojiyi geri üretir.

> **İspat eskizi.** İleri yön: $\tau$'dan $N(x) = \{N : \exists U \in \tau,\, x \in U
> \subseteq N\}$ tanımlayın. (N1) $x \in U \subseteq N$ olduğundan $x \in N$. (N2) $X \in \tau$
> her noktayı içerir. (N3) $U_1 \cap U_2 \in \tau$ açık olduğundan kesişim de komşuluktur.
> (N4) üst-küme almak tanımı bozmaz. Geri yön: $\tau = \{U : \forall x \in U,\, U \in N(x)\}$
> ailesinin topoloji aksiyomlarını sağladığı (N1–N4'ten) ve başlangıç sistemini geri verdiği
> doğrulanır; tekliği bu eşleşmenin tersinir olmasından gelir.

---
"""

# %% [markdown]
"""
## 3. Algoritmalar
"""

# %% [markdown]
"""
### 3.1 Sonlu Kapanış Hesabı

```
Kapanis(A, X, τ):
    closed_sets ← {X ∖ U : U ∈ τ}
    result ← X
    for each C ∈ closed_sets:
        if A ⊆ C and |C| < |result|:
            result ← C
    return result
```

**Karmaşıklık:** $O(|\tau| \cdot |X|)$ — her kapalı kümede $\subseteq$ kontrolü.
"""

# %% [markdown]
"""
### 3.2 Sonlu İç Hesabı

```
Ic(A, X, τ):
    result ← ∅
    for each U ∈ τ:
        if U ⊆ A and |U| > |result|:
            result ← U
    return result
```

**Karmaşıklık:** $O(|\tau| \cdot |X|)$.
"""

# %% [markdown]
"""
### 3.3 Türev Kümesi

```
TurevKumesi(A, X, τ):
    acc ← ∅
    for each x ∈ X:
        if every open U ∋ x meets A ∖ {x}:
            acc.add(x)
    return acc
```

**Karmaşıklık:** $O(|X| \cdot |\tau|)$.

---
"""

# %% [markdown]
"""
## 4. pytop API
"""

# %%
from pytop import (
    analyze_predicate,
    closure_of_subset, interior_of_subset, boundary_of_subset,
    derived_set_of_subset,
    is_open_subset, is_closed_subset, is_dense_subset, is_nowhere_dense_subset,
    neighborhood_system, character_at_point, analyze_neighborhood_system,
)

# %% [markdown]
"""
| Fonksiyon | İmza | Döndürür |
|-----------|------|---------|
| `analyze_predicate` | `(space, predicate, subset)` | `Result` |
| `closure_of_subset` | `(space, subset)` | `Result` |
| `interior_of_subset` | `(space, subset)` | `Result` |
| `boundary_of_subset` | `(space, subset)` | `Result` |
| `derived_set_of_subset` | `(space, subset)` | `Result` |
| `is_open_subset` | `(space, subset)` | `Result` |
| `is_closed_subset` | `(space, subset)` | `Result` |
| `is_dense_subset` | `(space, subset)` | `Result` |
| `is_nowhere_dense_subset` | `(space, subset)` | `Result` |
| `neighborhood_system` | `(carrier, topology, point)` | `Result` |
| `character_at_point` | `(carrier, topology, point)` | `Result` |
| `analyze_neighborhood_system` | `(carrier, topology, point=None)` | `Result` |

**Not:** `neighborhood_system`, `character_at_point`, `analyze_neighborhood_system`
fonksiyonları doğrudan `carrier` (liste) ve `topology` (liste) alır; space nesnesi değil.
Space nesnesi için `list(space.carrier)` ve `list(space.topology)` kullanın.

**`Result` Yorumlama:** `.status` (`"true"`, `"false"`, `"unknown"`), `.value` (hesaplanan değer),
`.justification` (gerekçe listesi).

---
"""

# %% [markdown]
"""
## 5. Örnekler
"""

# %% [markdown]
"""
### Örnek 5.1 — Kapanış ve İç: Sierpiński Uzayında
"""

# %%
from pytop import sierpinski_space, closure_of_subset, interior_of_subset, boundary_of_subset

s = sierpinski_space()
print("cl({0})  =", closure_of_subset(s, {0}).value)
print("cl({1})  =", closure_of_subset(s, {1}).value)
print("int({0}) =", interior_of_subset(s, {0}).value)
print("int({1}) =", interior_of_subset(s, {1}).value)
print("bd({1})  =", boundary_of_subset(s, {1}).value)

# %% [markdown]
"""
```text
cl({0})  = frozenset({0})
cl({1})  = frozenset({0, 1})
int({0}) = frozenset()
int({1}) = frozenset({1})
bd({1})  = frozenset({0})
```

**Çıktı Açıklaması:** $\{0\}$'ın kapanışı kendisidir çünkü $\{0\} = X \setminus \{1\}$
zaten kapalıdır. $\{1\}$'in kapanışı $X$'tir — $\{1\}$ kapalı değildir ve onu içeren
en küçük kapalı küme $X$'tir. $\{0\}$'ın içi boştur: $\{0\}$'ı kapsayan açık küme yoktur.
$\partial\{1\} = \{0\}$ sınır noktasıdır.
"""

# %% [markdown]
"""
### Örnek 5.2 — Türev Kümesi ve Hiçbiryerde-Yoğunluk
"""

# %%
from pytop import sierpinski_space, derived_set_of_subset, is_nowhere_dense_subset

s = sierpinski_space()
print("d({0}) =", derived_set_of_subset(s, {0}).value)
print("d({1}) =", derived_set_of_subset(s, {1}).value)
print("{0} nowhere_dense?", is_nowhere_dense_subset(s, {0}).status)
print("{1} nowhere_dense?", is_nowhere_dense_subset(s, {1}).status)

# %% [markdown]
"""
```text
d({0}) = frozenset()
d({1}) = frozenset({0})
{0} nowhere_dense? true
{1} nowhere_dense? false
```

**Çıktı Açıklaması:** $d(\{0\}) = \emptyset$: $\{0\}$ için birikme noktası yok —
$0$'ı içeren her komşuluk $\{0,1\}$, $\{0\} \setminus \{0\} = \emptyset$ ile kesişmez.
$d(\{1\}) = \{0\}$: $0$'ı içeren $\{0,1\}$, $\{1\} \setminus \{0\} = \{1\} \neq \emptyset$
ile kesişir.
"""

# %% [markdown]
"""
### Örnek 5.3 — Yüklemler: Ayrık Topoloji
"""

# %%
from pytop import discrete_topology, analyze_predicate

d = discrete_topology('a', 'b', 'c')
print("{'a'} acik?          =", analyze_predicate(d, 'open', {'a'}).status)
print("{'a'} kapali?        =", analyze_predicate(d, 'closed', {'a'}).status)
print("{'a'} clopen?        =", analyze_predicate(d, 'clopen', {'a'}).status)
print("{'a','b','c'} yogun? =", analyze_predicate(d, 'dense', {'a','b','c'}).status)

# %% [markdown]
"""
```text
{'a'} acik?          = true
{'a'} kapali?        = true
{'a'} clopen?        = true
{'a','b','c'} yogun? = true
```

**Çıktı Açıklaması:** Ayrık topolojide her tekil küme hem açık hem kapalıdır (clopen).
$X$'in kendisi trivially yoğundur.
"""

# %% [markdown]
"""
### Örnek 5.4 — Sınır Hesabı
"""

# %%
from pytop import make_topology, boundary_of_subset

sp = make_topology({1, 2, 3}, {1}, {2, 3})
print("bd({1})   =", boundary_of_subset(sp, {1}).value)
print("bd({2,3}) =", boundary_of_subset(sp, {2, 3}).value)
print("bd({1,2}) =", boundary_of_subset(sp, {1, 2}).value)

# %% [markdown]
"""
```text
bd({1})   = frozenset()
bd({2,3}) = frozenset()
bd({1,2}) = frozenset({2, 3})
```

**Çıktı Açıklaması:** $\{1\}$ ve $\{2,3\}$ açık kümeler olduğundan sınırları boştur
($\partial U = \emptyset$ açık $U$ için). $\{1,2\}$ ne açık ne kapalı; sınırı
$\partial\{1,2\} = \{2,3\}$ sınır noktalarını içerir.
"""

# %% [markdown]
"""
### Örnek 5.5 — Komşuluk Sistemi
"""

# %%
from pytop import sierpinski_space, neighborhood_system, character_at_point

s = sierpinski_space()
carrier = list(s.carrier)
topology = list(s.topology)

print("N(0) =", neighborhood_system(carrier, topology, 0).value)
print("N(1) =", neighborhood_system(carrier, topology, 1).value)
print("chi(0) =", character_at_point(carrier, topology, 0).value)
print("chi(1) =", character_at_point(carrier, topology, 1).value)

# %% [markdown]
"""
```text
N(0) = [['0', '1']]
N(1) = [['1'], ['0', '1']]
chi(0) = 1
chi(1) = 2
```

**Çıktı Açıklaması:** $N(0) = \{X\}$ — $0$ yalnızca $X$'te yer aldığından bir tek komşuluğu
vardır. $N(1) = \{\{1\}, X\}$ — $1$ hem $\{1\}$ hem $X$'te yer alır. $\chi(0)=1$,
$\chi(1)=2$ yerel baz büyüklüklerini gösterir.
"""

# %% [markdown]
"""
### Örnek 5.6 — İç / Kapanış / Sınır / Dış Parçalanışı
"""

# %%
from pytop import (make_topology, interior_of_subset, closure_of_subset,
                   boundary_of_subset, exterior_of_subset)

sp = make_topology({1, 2, 3, 4, 5}, {1, 2}, {4, 5}, {1, 2, 4, 5})
A = {1, 2, 3}
print("int(A) =", interior_of_subset(sp, A).value)
print("cl(A)  =", closure_of_subset(sp, A).value)
print("bd(A)  =", boundary_of_subset(sp, A).value)
print("ext(A) =", exterior_of_subset(sp, A).value)

# %% [markdown]
"""
```text
int(A) = frozenset({1, 2})
cl(A)  = frozenset({1, 2, 3})
bd(A)  = frozenset({3})
ext(A) = frozenset({4, 5})
```

**Çıktı Açıklaması:** $A = \{1,2,3\}$ için $A^\circ = \{1,2\}$ (içine sığan en büyük açık küme
$\{1,2\}$), $\mathrm{cl}(A) = \{1,2,3\}$, $\partial A = \mathrm{cl}(A) \setminus A^\circ = \{3\}$.
Dış küme $\mathrm{ext}(A) = (X \setminus A)^\circ = \{4,5\}$ (yukarıdaki figürde mavi). İç
$\{1,2\}$, sınır $\{3\}$ ve dış $\{4,5\}$ birlikte $X = \{1,2,3,4,5\}$'i ayrık olarak kaplar:
$X = A^\circ \cup \partial A \cup \mathrm{ext}(A)$.
"""

# %% [markdown]
"""
### Örnek 5.7 — Kuratowski Aksiyomlarının Doğrulanması
"""

# %%
from pytop import finite_chain_space, kuratowski_closure_check

s = finite_chain_space(3)
report = kuratowski_closure_check(list(s.carrier), list(s.topology))
for k in sorted(report):
    print(f"{k:<13}= {report[k]}")

# %% [markdown]
"""
```text
all          = True
empty        = True
extensive    = True
finite_union = True
idempotent   = True
```

**Çıktı Açıklaması:** `kuratowski_closure_check`, sonlu uzayın kapanış operatörünü K1–K4'e karşı
test eder: `empty` $\to$ (K1), `extensive` $\to$ (K2), `idempotent` $\to$ (K3),
`finite_union` $\to$ (K4). `all` hepsinin sağlandığını özetler — `finite_chain_space(3)`
geçerli bir topolojidir.
"""

# %% [markdown]
"""
### Örnek 5.8 — Yoğun Nokta ve Birikme Kümesi (Zincir Uzayı)
"""

# %%
from pytop import finite_chain_space, closure_of_subset, is_dense_subset, derived_set_of_subset

c = finite_chain_space(4)
print("cl({1})    =", closure_of_subset(c, {1}).value)
print("{1} dense? =", is_dense_subset(c, {1}).status)
print("d({3})     =", derived_set_of_subset(c, {3}).value)
print("cl({4})    =", closure_of_subset(c, {4}).value)

# %% [markdown]
"""
```text
cl({1})    = frozenset({1, 2, 3, 4})
{1} dense? = true
d({3})     = frozenset({4})
cl({4})    = frozenset({4})
```

**Çıktı Açıklaması:** `finite_chain_space(4)` zincirinde açıklar
$\{1\} \subset \{1,2\} \subset \{1,2,3\} \subset X$'tir. $1$ noktası **jeneriktir**:
$\mathrm{cl}(\{1\}) = X$, yani $\{1\}$ yoğundur. Karşıt uçta $4$ **kapalı bir noktadır**:
$\mathrm{cl}(\{4\}) = \{4\}$. $d(\{3\}) = \{4\}$, çünkü $4$'ü içeren tek açık $X$'tir ve
$X \cap (\{3\} \setminus \{4\}) = \{3\} \neq \emptyset$.

![Zincir uzayında özelleşme oku; 1 yoğun (jenerik), 4 kapalı nokta](../assets/ch05/fig_ch05_yogunluk.png)

> ❌ **Karşı-örnek:** "İç küme her zaman kapalıdır" yanılgısı. Örnek 5.6'da
> $A^\circ = \{1,2\}$ açıktır ama **kapalı değildir** ($X \setminus \{1,2\} = \{3,4,5\}$ açık
> değil). İç ve dış daima açıktır; kapanış ve sınır daima kapalıdır — bu iki ailenin
> karıştırılması en sık yapılan hatadır. Ayrıca $\partial A = \emptyset$ ancak ve ancak $A$
> hem açık hem kapalı (clopen) ise olur; Örnek 5.4'te $\{1\}$ açık olduğundan
> $\partial\{1\} = \emptyset$, ama $\{1,2\}$ clopen olmadığından sınırı boş değildir.

---
"""

# %% [markdown]
"""
## 6. Alıştırmalar
"""

# %% [markdown]
"""
### Kodlama Alıştırmaları

**K1.** İndirgenmiş topoloji (iki nokta) üzerinde her iki noktanın komşuluk sistemini
hesaplayın. N1–N4 aksiyomları geçiyor mu?

**K2.** $X = \{1,2,3,4\}$ üzerinde `make_topology({1,2,3,4},{1,2},{3,4})` topolojisinde
$\mathrm{bd}(\{1,2,3\})$ ve $\mathrm{cl}(\{1,2,3\})$ hesaplayın.

**K3.** `finite_chain_space(4)` zincirinde $\{1,2\}$'nin iç, kapanış ve sınır kümelerini
bulun. Beklediğiniz değerler ile örtüşüyor mu?

**K4.** `make_topology({1,2,3,4,5}, {1,2}, {4,5}, {1,2,4,5})` uzayında $A = \{1,2,3\}$ için
`interior_of_subset`, `boundary_of_subset` ve `exterior_of_subset` çalıştırın. Üç kümenin
birleşiminin $X$'i ayrık olarak kapladığını ($X = A^\circ \cup \partial A \cup \mathrm{ext}(A)$)
doğrulayın. _İpucu:_ üç frozenset'i `set().union(...)` ile birleştirip $X$ ile karşılaştırın.

**K5.** `finite_chain_space(4)` zincirinde `kuratowski_closure_check(list(c.carrier),
list(c.topology))` çağırın ve `all` alanının `True` döndüğünü gösterin. Ardından `cl({1})`'i
hesaplayıp $\{1\}$'in yoğun olduğunu (`is_dense_subset` ile) teyit edin.
"""

# %% [markdown]
"""
### Teori Alıştırmaları

**T1.** $(X,\tau)$ uzayında $A^\circ = X \setminus \mathrm{cl}(X \setminus A)$ eşitliğini
Kuratowski aksiyomlarını kullanarak kanıtlayın.

**T2.** Bir $A \subseteq X$ kümesinin yoğun olması için gerek ve yeter koşulun
$\mathrm{cl}(A) = X$ olduğunu gösterin.

**T3.** Her $A \subseteq X$ için $X = A^\circ \cup \partial A \cup \mathrm{ext}(A)$ olduğunu
ve bu üç kümenin ikişer ikişer ayrık olduğunu ispatlayın. (İpucu: $\mathrm{ext}(A) =
(X \setminus A)^\circ$ ve $\partial A = \mathrm{cl}(A) \setminus A^\circ$ tanımlarını kullanın.)

**T4.** $A^\circ$ kümesinin daima açık olduğunu, fakat genel olarak kapalı **olmadığını**
gösteren bir karşı-örnek verin. (İpucu: Örnek 5.6'daki $\{1,2\}$ kümesi üzerinde düşünün.)
"""
