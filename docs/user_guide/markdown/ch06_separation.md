# Bölüm 6 — Ayrılma Aksiyomları

## 1. Konu

Ayrılma aksiyomları, bir topolojik uzaydaki noktaların ve kapalı kümelerin birbirinden
açık kümeler aracılığıyla ne ölçüde "ayrılabildiğini" ölçer.

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

---

## 2. Teoremler

**Teorem 2.1 (Ayrılma Zinciri).**
T4 $\Rightarrow$ T3.5 $\Rightarrow$ T3 $\Rightarrow$ T2.5 $\Rightarrow$ T2 $\Rightarrow$ T1 $\Rightarrow$ T0.
Tersi genel olarak doğru değildir.

**Teorem 2.2 (Urysohn Fonksiyon Teoremi).**
$X$ normal ise ve $C, D$ disjoint kapalı kümeler ise, $f: X \to [0,1]$ sürekli bir fonksiyon
vardır: $f|_C \equiv 0$, $f|_D \equiv 1$.

**Teorem 2.3 (Tietze Genişleme Teoremi).**
$X$ normal ise her kapalı $A \subseteq X$ üzerinde $f: A \to [a,b]$ süreklisi
tüm $X$'e sürekli genişletilebilir.

**Teorem 2.4 (Tychonoff Karakterizasyonu).**
$X$, T3.5'tir $\iff$ $X$, bir küp $[0,1]^I$'nın içine homeomorf gömülebilir.

**Teorem 2.5 (Sonlu T1 ⟺ Ayrık).**
Sonlu bir uzayda T1 $\iff$ ayrık topoloji.
*(Kanıt: T1 $\Rightarrow$ her tekil küme kapalı $\Rightarrow$ her küme kapalı $\Rightarrow$ her küme açık.)*

---

## 3. Algoritmalar

### 3.1 Sonlu T0 Karar Prosedürü

```
KontrolT0(X, τ):
    for each pair (x, y) with x ≠ y:
        if not (∃U∈τ: x∈U ∧ y∉U) and not (∃U∈τ: y∈U ∧ x∉U):
            return False
    return True
```

**Karmaşıklık:** $O(|X|^2 \cdot |\tau|)$.

### 3.2 Sonlu T2 (Hausdorff) Karar Prosedürü

```
KontrolT2(X, τ):
    for each pair (x, y) with x ≠ y:
        if not ∃ U,V∈τ: x∈U ∧ y∈V ∧ U∩V=∅:
            return False
    return True
```

**Karmaşıklık:** $O(|X|^2 \cdot |\tau|^2)$.

### 3.3 check_tychonoff — 5-Katmanlı Prosedür

1. T3'ü doğrula
2. `completely_regular` tanığı ara
3. T3.5 onaylama (T3 + completely_regular)
4. Etiket tabanlı geri çekilme
5. Sonuç döndür

---

## 4. pytop API

```python
from pytop import (
    is_t0, is_t1, is_t2, is_t2_5, is_t3, is_t4,
    is_hausdorff, is_regular, is_normal, is_perfectly_normal,
    separation_chain, analyze_separation,
)
```

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

---

## 5. Örnekler

### Örnek 5.1 — Sierpiński: T0 ✓, T1 ✗

```python
from pytop import sierpinski_space, is_t0, is_t1, is_t2

s = sierpinski_space()
print("T0:", is_t0(s).status)
print("T1:", is_t1(s).status)
print("T2:", is_t2(s).status)
```

```text
T0: true
T1: false
T2: false
```

**Çıktı Açıklaması:** $\{0\}$ açık olmadığından T1 sağlanamaz — $1$'i $0$'dan ayıran açık küme
var ($\{1\}$) ama $0$'ı $1$'den ayıran yok. T0 sağlanır: $\{1\}$ ile $0 \in \{0,1\} \setminus \{1\}$.

### Örnek 5.2 — İndirgenmiş: Hiçbir T Aksiyomu Yok

```python
from pytop import indiscrete_topology, is_t0, is_t1

ind = indiscrete_topology('a', 'b')
print("T0:", is_t0(ind).status)
print("T1:", is_t1(ind).status)
```

```text
T0: false
T1: false
```

**Çıktı Açıklaması:** $\tau = \{\emptyset, X\}$; $a$ ve $b$'yi birbirinden ayıran açık küme
yoktur.

### Örnek 5.3 — Kosonlu $\mathbb{N}$: T1 ✓, T2 ✗

```python
from pytop import naturals_cofinite, is_t0, is_t1, is_t2

nc = naturals_cofinite()
print("T0:", is_t0(nc).status)
print("T1:", is_t1(nc).status)
print("T2:", is_t2(nc).status)
```

```text
T0: true
T1: true
T2: false
```

**Çıktı Açıklaması:** Kosonlu topolojide her tekil kümenin tamamlayıcısı sonlu, dolayısıyla
açıktır — $\{n\} = \mathbb{N} \setminus (\mathbb{N} \setminus \{n\})$ kapalıdır, T1 sağlanır.
Ancak herhangi iki boş olmayan açık küme kesişir, T2 başarısız.

### Örnek 5.4 — Ayrılma Zinciri: Ayrık Topoloji

```python
from pytop import discrete_topology, separation_chain

d = discrete_topology(1, 2, 3)
chain = separation_chain(d)
for prop, result in chain.items():
    print(f"  {prop:20s}: {result.status}")
```

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

**Çıktı Açıklaması:** Ayrık topoloji tüm aksiyomları sağlar — her iki nokta arasında
disjoint tekil kümeler mevcuttur; Urysohn, T3, T4 otomatik.

### Örnek 5.5 — Sierpiński Zinciri

```python
from pytop import sierpinski_space, separation_chain

s = sierpinski_space()
for prop, result in separation_chain(s).items():
    print(f"  {prop:20s}: {result.status}")
```

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
sonlu uzayda kesin olarak belirlenemiyor (sembolik çıkarım sınırı).

### Örnek 5.6 — analyze_separation

```python
from pytop import discrete_topology, sierpinski_space, real_line_metric, analyze_separation

d = discrete_topology(1, 2, 3)
s = sierpinski_space()
rl = real_line_metric()

print("Real line Hausdorff?:", analyze_separation(rl).status)
print("Discrete Hausdorff? :", analyze_separation(d).status)
print("Sierpinski Hausdorff?:", analyze_separation(s).status)
print("Sierpinski T0?       :", analyze_separation(s, 't0').status)
```

```text
Real line Hausdorff?: true
Discrete Hausdorff? : true
Sierpinski Hausdorff?: false
Sierpinski T0?       : true
```

**Çıktı Açıklaması:** `analyze_separation(space, property)` tek bir aksiyom için sorgu yapar.
Varsayılan `'hausdorff'`'tur. `status='true'` → uzay o aksiyomu sağlar.

---

## 6. Alıştırmalar

### Kodlama Alıştırmaları

**K1.** `make_topology({1,2,3},{1},{2},{1,2})` topolojisi için `separation_chain` çalıştırın.
Hangi aksiyomlar sağlanıyor?

**K2.** `two_point_indiscrete_space()` (`pytop.examples`) üzerinde `is_t0`, `is_t1`, `is_t2`
sonuçlarını inceleyin.

**K3.** `finite_chain_space(3)` üzerinde ayrılma zincirini çalıştırın; en yüksek sağlanan
aksiyom hangisidir?

### Teori Alıştırmaları

**T1.** T2 $\Rightarrow$ T1 $\Rightarrow$ T0 implicasyonlarını formal olarak kanıtlayın.

**T2.** Sonlu bir uzayda T1 $\iff$ ayrık topoloji olduğunu gösterin.
*(İpucu: T1 → her tekil küme kapalı → her küme kapalı → her küme açık.)*
