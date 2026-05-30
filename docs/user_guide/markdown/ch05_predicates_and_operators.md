# Bölüm 2 — Yüklemler ve Altküme Operatörleri

## 1. Konu

### 1.1 Altküme Yüklemleri

Bir $(X, \tau)$ topolojik uzayı ve $A \subseteq X$ alınalım:

| Yüklem | Tanım |
|--------|-------|
| **Açık (open)** | $A \in \tau$ |
| **Kapalı (closed)** | $X \setminus A \in \tau$ |
| **Clopen** | $A \in \tau$ ve $X \setminus A \in \tau$ |
| **Yoğun (dense)** | Her boş olmayan $U \in \tau$ için $U \cap A \neq \emptyset$; eşdeğer: $\overline{A} = X$ |
| **Hiçbiryerde-yoğun (nowhere dense)** | $\mathrm{int}(\overline{A}) = \emptyset$ |

### 1.2 Altküme Operatörleri

| Operatör | Gösterim | Tanım |
|----------|----------|-------|
| Kapanış | $\overline{A} = \mathrm{cl}(A)$ | $A$'yı içeren en küçük kapalı küme |
| İç | $A^\circ = \mathrm{int}(A)$ | $A$'ya dahil en büyük açık küme |
| Sınır | $\partial A = \mathrm{bd}(A)$ | $\overline{A} \setminus A^\circ$ |
| Türev kümesi | $A' = d(A)$ | $A$'nın birikme noktaları kümesi |

**Birikme noktası:** $x \in A'$ ⟺ her $U \ni x$ açık için $U \cap (A \setminus \{x\}) \neq \emptyset$.

### 1.3 Komşuluk Sistemi N(x)

$x \in X$ için:
$$N(x) = \{N \subseteq X : \exists U \in \tau,\, x \in U \subseteq N\}$$

**Komşuluk Aksiyomları (N1–N4):**
- **(N1)** $x \in N$, her $N \in N(x)$ için
- **(N2)** $X \in N(x)$
- **(N3)** $N_1, N_2 \in N(x) \Rightarrow N_1 \cap N_2 \in N(x)$
- **(N4)** $N \in N(x)$, $N \subseteq M \Rightarrow M \in N(x)$

---

## 2. Teoremler

**Teorem 2.1 (Kuratowski Kapanış Aksiyomları).**
$\mathrm{cl}: \mathcal{P}(X) \to \mathcal{P}(X)$ operatörü şu dört özelliği sağlar
(ve yalnızca bunları sağlayan her operatör bir topoloji belirler):
- **(K1)** $\mathrm{cl}(\emptyset) = \emptyset$
- **(K2)** $A \subseteq \mathrm{cl}(A)$
- **(K3)** $\mathrm{cl}(\mathrm{cl}(A)) = \mathrm{cl}(A)$ (kuvvet-idemp.)
- **(K4)** $\mathrm{cl}(A \cup B) = \mathrm{cl}(A) \cup \mathrm{cl}(B)$

**Teorem 2.2 (İç-Kapanış Dualitesi).**
Her $A \subseteq X$ için:
$$A^\circ = X \setminus \mathrm{cl}(X \setminus A), \qquad
  \mathrm{cl}(A) = X \setminus \mathrm{int}(X \setminus A).$$

**Teorem 2.3 (Komşuluk Sistemi Round-Trip).**
Bir topolojiden türetilen komşuluk sistemi $\{N(x)\}_{x \in X}$, N1–N4'ü sağlar.
Tersine, N1–N4'ü sağlayan her aile $\tau = \{U : \forall x \in U, U \in N(x)\}$
şeklinde tek bir topolojiyi geri üretir.

---

## 3. Algoritmalar

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

## 4. pytop API

```python
from pytop import (
    analyze_predicate,
    closure_of_subset, interior_of_subset, boundary_of_subset,
    derived_set_of_subset,
    is_open_subset, is_closed_subset, is_dense_subset, is_nowhere_dense_subset,
    neighborhood_system, character_at_point, analyze_neighborhood_system,
)
```

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

## 5. Örnekler

### Örnek 5.1 — Kapanış ve İç: Sierpiński Uzayında

```python
from pytop import sierpinski_space, closure_of_subset, interior_of_subset, boundary_of_subset

s = sierpinski_space()
print("cl({0})  =", closure_of_subset(s, {0}).value)
print("cl({1})  =", closure_of_subset(s, {1}).value)
print("int({0}) =", interior_of_subset(s, {0}).value)
print("int({1}) =", interior_of_subset(s, {1}).value)
print("bd({1})  =", boundary_of_subset(s, {1}).value)
```

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

### Örnek 5.2 — Türev Kümesi ve Hiçbiryerde-Yoğunluk

```python
from pytop import sierpinski_space, derived_set_of_subset, is_nowhere_dense_subset

s = sierpinski_space()
print("d({0}) =", derived_set_of_subset(s, {0}).value)
print("d({1}) =", derived_set_of_subset(s, {1}).value)
print("{0} nowhere_dense?", is_nowhere_dense_subset(s, {0}).status)
print("{1} nowhere_dense?", is_nowhere_dense_subset(s, {1}).status)
```

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

### Örnek 5.3 — Yüklemler: Ayrık Topoloji

```python
from pytop import discrete_topology, analyze_predicate

d = discrete_topology('a', 'b', 'c')
print("{'a'} acik?          =", analyze_predicate(d, 'open', {'a'}).status)
print("{'a'} kapali?        =", analyze_predicate(d, 'closed', {'a'}).status)
print("{'a'} clopen?        =", analyze_predicate(d, 'clopen', {'a'}).status)
print("{'a','b','c'} yogun? =", analyze_predicate(d, 'dense', {'a','b','c'}).status)
```

```text
{'a'} acik?          = true
{'a'} kapali?        = true
{'a'} clopen?        = true
{'a','b','c'} yogun? = true
```

**Çıktı Açıklaması:** Ayrık topolojide her tekil küme hem açık hem kapalıdır (clopen).
$X$'in kendisi trivially yoğundur.

### Örnek 5.4 — Sınır Hesabı

```python
from pytop import make_topology, boundary_of_subset

sp = make_topology({1, 2, 3}, {1}, {2, 3})
print("bd({1})   =", boundary_of_subset(sp, {1}).value)
print("bd({2,3}) =", boundary_of_subset(sp, {2, 3}).value)
print("bd({1,2}) =", boundary_of_subset(sp, {1, 2}).value)
```

```text
bd({1})   = frozenset()
bd({2,3}) = frozenset()
bd({1,2}) = frozenset({2, 3})
```

**Çıktı Açıklaması:** $\{1\}$ ve $\{2,3\}$ açık kümeler olduğundan sınırları boştur
($\partial U = \emptyset$ açık $U$ için). $\{1,2\}$ ne açık ne kapalı; sınırı
$\partial\{1,2\} = \{2,3\}$ sınır noktalarını içerir.

### Örnek 5.5 — Komşuluk Sistemi

```python
from pytop import sierpinski_space, neighborhood_system, character_at_point

s = sierpinski_space()
carrier = list(s.carrier)
topology = list(s.topology)

print("N(0) =", neighborhood_system(carrier, topology, 0).value)
print("N(1) =", neighborhood_system(carrier, topology, 1).value)
print("chi(0) =", character_at_point(carrier, topology, 0).value)
print("chi(1) =", character_at_point(carrier, topology, 1).value)
```

```text
N(0) = [['0', '1']]
N(1) = [['1'], ['0', '1']]
chi(0) = 1
chi(1) = 2
```

**Çıktı Açıklaması:** $N(0) = \{X\}$ — $0$ yalnızca $X$'te yer aldığından bir tek komşuluğu
vardır. $N(1) = \{\{1\}, X\}$ — $1$ hem $\{1\}$ hem $X$'te yer alır. $\chi(0)=1$,
$\chi(1)=2$ yerel baz büyüklüklerini gösterir.

---

## 6. Alıştırmalar

### Kodlama Alıştırmaları

**K1.** İndirgenmiş topoloji (iki nokta) üzerinde her iki noktanın komşuluk sistemini
hesaplayın. N1–N4 aksiyomları geçiyor mu?

**K2.** $X = \{1,2,3,4\}$ üzerinde `make_topology({1,2,3,4},{1,2},{3,4})` topolojisinde
$\mathrm{bd}(\{1,2,3\})$ ve $\mathrm{cl}(\{1,2,3\})$ hesaplayın.

**K3.** `finite_chain_space(4)` zincirinde $\{1,2\}$'nin iç, kapanış ve sınır kümelerini
bulun. Beklediğiniz değerler ile örtüşüyor mu?

### Teori Alıştırmaları

**T1.** $(X,\tau)$ uzayında $A^\circ = X \setminus \mathrm{cl}(X \setminus A)$ eşitliğini
Kuratowski aksiyomlarını kullanarak kanıtlayın.

**T2.** Bir $A \subseteq X$ kümesinin yoğun olması için gerek ve yeter koşulun
$\mathrm{cl}(A) = X$ olduğunu gösterin.
