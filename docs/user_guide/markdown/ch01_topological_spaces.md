# Bölüm 1 — Topolojik Uzaylar

## 1. Konu

### 1.1 Sezgisel Giriş

Topoloji, bir kümedeki noktaların birbirine "yakın" olup olmadığını, aralarındaki sürekliliği
ve şekilsel özellikleri, mesafe kavramına gerek duymadan inceleyen matematiksel bir disiplindir.
Bunu mümkün kılan temel araç *açık küme* kavramıdır.

Düşünelim: gerçek doğruda $(a, b)$ aralığı "açık"tır; her noktasının çevresinde küçük bir açık
aralık daha bulunur. Bu sezgiyi soyutlayarak *herhangi* bir küme üzerinde topoloji tanımlamak
mümkündür.

### 1.2 Formal Tanım

Bir $X$ kümesi ve $\tau \subseteq \mathcal{P}(X)$ ailesi verilsin.
$(X, \tau)$ bir **topolojik uzay**, $\tau$ ise $X$ üzerinde bir **topoloji** olarak adlandırılır,
eğer aşağıdaki üç aksiyom sağlanıyorsa:

| Aksiyom | İfade |
|---------|-------|
| **(T1)** Trivial kümeler | $\emptyset \in \tau$ ve $X \in \tau$ |
| **(T2)** Sonlu kesişim | $U, V \in \tau \Rightarrow U \cap V \in \tau$ |
| **(T3)** Keyfi birleşim | $\{U_\alpha\}_{\alpha \in I} \subseteq \tau \Rightarrow \bigcup_\alpha U_\alpha \in \tau$ |

$\tau$'nun elemanları **açık küme** olarak adlandırılır.

### 1.3 Temel Örnekler

| Topoloji | Tanım | Açık kümeler |
|----------|-------|--------------|
| **Ayrık (discrete)** | Her alt küme açık | $\tau = \mathcal{P}(X)$ |
| **İndirgenmiş (indiscrete)** | Yalnızca $\emptyset$ ve $X$ açık | $\tau = \{\emptyset, X\}$ |
| **Kosonlu (cofinite)** | $U$ açık ⟺ $U = \emptyset$ veya $X \setminus U$ sonlu | — |
| **Sierpiński** | $X = \{0,1\}$, $\tau = \{\emptyset, \{1\}, X\}$ | 3 açık küme |

### 1.4 Baz ve Alt-Baz

**Baz:** $\mathcal{B} \subseteq \tau$ ailesi, her $U \in \tau$ ve her $x \in U$ için
$x \in B \subseteq U$ sağlayan bir $B \in \mathcal{B}$ varsa $\tau$'ya **baz** denir.

**Baz Koşulları (B1–B2):**
- **(B1)** $\bigcup \mathcal{B} = X$
- **(B2)** $B_1, B_2 \in \mathcal{B}$ ve $x \in B_1 \cap B_2$ ise bir $B_3 \in \mathcal{B}$ vardır:
  $x \in B_3 \subseteq B_1 \cap B_2$

**Alt-Baz:** $\mathcal{S} \subseteq \mathcal{P}(X)$ ailesi; sonlu kesişimleri baz, onların birleşimleri
ise $\tau$'yu oluşturur.

### 1.5 Sonlu ve Sonsuz Uzaylar

`pytop`'ta iki temel sınıf bulunur:

- **`FiniteTopologicalSpace`:** Taşıyıcı ($X$) sonlu; topoloji açıkça `frozenset`'ler koleksiyonu
  olarak saklanır. Tüm hesaplamalar tam ve kesindir.
- **`InfiniteTopologicalSpace` türevleri:** Taşıyıcı simgesel (örn. `'R'`, `'N'`); topoloji
  `topology=None` ile gösterilir ve etiket tabanlı sembolik çıkarım yapılır.

---

## 2. Teoremler

### Teorem 2.1 — Aksiyomların Yeterliliği

**Teorem:** $(X, \tau)$ bir topolojik uzay olsun. T1–T3 aksiyomları, açık kümelerin
herhangi bir ailesinin birleşiminin ve *sonlu* herhangi bir ailesinin kesişiminin
yeniden $\tau$'da olduğunu garanti eder. Özellikle,
$$\bigcap_{i=1}^{n} U_i \in \tau \quad (U_i \in \tau, n < \infty)$$
elde edilir.

**Not:** *Sonsuz* kesişim gerekmez. Gerçek doğruda $\bigcap_{n=1}^{\infty}(-\frac{1}{n}, \frac{1}{n}) = \{0\}$
açık değildir; bu sonsuz kesişimin topolojide yer almak zorunda olmadığını gösterir.

### Teorem 2.2 — Baz Teoremi

**Teorem:** $\mathcal{B} \subseteq \mathcal{P}(X)$ ailesi (B1)–(B2) koşullarını sağlıyorsa,
$$\tau_{\mathcal{B}} = \bigl\{U \subseteq X : \forall x \in U,\, \exists B \in \mathcal{B},\, x \in B \subseteq U\bigr\}$$
bir topoloji olur ve $\mathcal{B}$ bu topolojiye baz oluşturur.

**Kanıt İskeleti:** T1: $\emptyset \in \tau_{\mathcal{B}}$ (boş koşul); $X \in \tau_{\mathcal{B}}$ (B1 ile). T2: $U, V \in \tau_{\mathcal{B}}$ ve $x \in U \cap V$ ise $B_U, B_V$ bul; (B2) ile $B_3 \subseteq B_U \cap B_V$. T3: birleşim noktası için doğrudan baz elemanı al.

### Teorem 2.3 — Karşılaştırma

**Teorem:** $X$ üzerinde iki topoloji $\tau_1 \subseteq \tau_2$ ise $\tau_1$ **kaba (coarser)**,
$\tau_2$ **ince (finer)** topoloji olarak adlandırılır. Ayrık topoloji en ince, indirgenmiş
topoloji en kaba topolojidir.

---

## 3. Algoritmalar

### 3.1 Bazdan Topoloji Üretimi

**Problem:** $X$ ve $\mathcal{B} \subseteq \mathcal{P}(X)$ verilsin; $\tau_{\mathcal{B}}$'yi hesapla.

**Sözde Kod:**

```
BazdenTopoloji(X, B):
    tau ← {∅, X}
    for each alt_aile S ⊆ B (boş olmayan):
        tau.add(⋃ S)          # keyfi birleşim
    tau ← ClosureUnderIntersection(tau)  # sonlu kesişimi kapat
    return tau

ClosureUnderIntersection(tau):
    changed ← true
    while changed:
        changed ← false
        for each U, V ∈ tau:
            if U ∩ V ∉ tau:
                tau.add(U ∩ V)
                changed ← true
    return tau
```

**Karmaşıklık:**
- En kötü durum: $O(|\mathcal{B}| \cdot 2^{|\mathcal{B}|})$ (tüm alt-ailelerin birleşimi)
- Pratik (çakışmayan baz elemanları): $O(|\tau| \cdot |\mathcal{B}|)$
- Uzay: $O(|\tau|)$ açık küme saklar

`pytop`'ta bu işlem `topology_from_basis` / `generate_topology_from_basis` fonksiyonları
aracılığıyla `subbases.py` modülünde gerçekleştirilmektedir.

### 3.2 Alt-Bazdan Topoloji Üretimi

**Problem:** $\mathcal{S}$ verilsin; önce $\mathcal{S}$'nin sonlu kesişimlerinden baz oluştur,
ardından 3.1'i uygula.

**Karmaşıklık:** $O(|\mathcal{S}|^k \cdot 2^{|\mathcal{S}|^k})$ — $k$ kesişim derinliği.

---

## 4. pytop API

### 4.1 Sınıflar

```python
from pytop import TopologicalSpace, FiniteTopologicalSpace
```

| Sınıf | Taşıyıcı | Topoloji |
|-------|----------|----------|
| `TopologicalSpace` | `Any` (simgesel veya somut) | `Any` (None olabilir) |
| `FiniteTopologicalSpace` | sonlu `frozenset` | `frozenset[frozenset]` |

`TopologicalSpace` temel sınıftır; `FiniteTopologicalSpace` ondan türer ve otomatik olarak
`"finite"` etiketini taşır.

**Alanlar:**
- `carrier`: Altta yatan küme
- `topology`: Açık kümeler koleksiyonu (veya `None`)
- `tags`: Özellik etiketleri (`set[str]`)
- `metadata`: Ek bilgiler (`dict`)

### 4.2 Oluşturucular

```python
from pytop import (
    make_topology,
    discrete_topology,
    indiscrete_topology,
    cofinite_topology,
    sierpinski_space,
    topology_from_basis,
    topology_from_subbasis,
)
```

| Fonksiyon | İmza | Açıklama |
|-----------|------|----------|
| `make_topology` | `(carrier, *open_sets)` | Açık kümeleri listeleyerek topoloji inşa et |
| `discrete_topology` | `(*elements)` | Ayrık topoloji |
| `indiscrete_topology` | `(*elements)` | İndirgenmiş topoloji |
| `cofinite_topology` | `(*elements)` | Kosonlu topoloji (sonlu X'te ayrıkla çakışır) |
| `sierpinski_space` | `()` | $\{0,1\}$ üzerinde Sierpiński uzayı |
| `topology_from_basis` | `(carrier, basis)` | Bazdan topoloji üret |
| `topology_from_subbasis` | `(carrier, subbasis)` | Alt-bazdan topoloji üret |

### 4.3 Hazır Örnekler

```python
from pytop import finite_chain_space, naturals_cofinite, real_line_metric
```

| Fonksiyon | Döndürür | Açıklama |
|-----------|---------|----------|
| `finite_chain_space(n)` | `FiniteTopologicalSpace` | $n$ noktalı Alexandrov zinciri |
| `naturals_cofinite()` | `CofiniteSpace` | $\mathbb{N}$ kosonlu topoloji |
| `real_line_metric()` | `SymbolicMetricSpace` | $\mathbb{R}$ olağan metrik topoloji |

### 4.4 Tag Sistemi

`pytop` nesneleri `tags` kümesi aracılığıyla topolojik özellikler taşır. Örnek etiketler:
`"finite"`, `"discrete"`, `"t0"`, `"t1"`, `"hausdorff"`, `"compact"`, `"connected"`,
`"metric"`, `"separable"`, `"second_countable"`.

---

## 5. Örnekler

### Örnek 5.1 — Sierpiński Uzayı

```python
from pytop import sierpinski_space

s = sierpinski_space()
print("Taşıyıcı:", s.carrier)
print("Topoloji:", sorted(str(t) for t in s.topology))
print("Etiketler:", sorted(s.tags))
```

```text
Taşıyıcı: frozenset({0, 1})
Topoloji: ['frozenset()', 'frozenset({0, 1})', 'frozenset({1})']
Etiketler: ['compact', 'connected', 'finite', 't0']
```

**Çıktı Açıklaması:** Topoloji tam olarak üç açık küme içerir: $\emptyset$, $\{1\}$, $\{0,1\}$.
$\{0\}$ açık değildir — bu T0 fakat T1 değil özelliğinin kaynağıdır. Etiket `t0` bu durumu
özetler; `t1` etiketi bulunmaz.

### Örnek 5.2 — Ayrık Topoloji

```python
from pytop import discrete_topology

d = discrete_topology(1, 2, 3)
print("|τ| =", len(d.topology))      # 2^3 = 8
print("Etiketler:", sorted(d.tags))
```

```text
|τ| = 8
Etiketler: ['discrete', 'finite', 'hausdorff', 'metrizable', 'normal', 'regular']
```

**Çıktı Açıklaması:** $n = 3$ elemanlı bir kümenin ayrık topolojisi $2^3 = 8$ açık küme içerir.
Ayrık topoloji her topolojik özelliği sağlar: Hausdorff, regüler, normal, metriklenebilir.

### Örnek 5.3 — `make_topology` ile Manuel İnşa

```python
from pytop import make_topology

sp = make_topology({1, 2, 3}, {1}, {2, 3})
print("|τ| =", len(sp.topology))
print("Açık kümeler:", sorted(str(t) for t in sp.topology))
```

```text
|τ| = 4
Açık kümeler: ['frozenset()', 'frozenset({1})', 'frozenset({2, 3})', 'frozenset({1, 2, 3})']
```

**Çıktı Açıklaması:** $\{1\}$ ve $\{2,3\}$ açık olarak verilince, $\emptyset$ ve $X$ otomatik
eklenir. T2 ve T3 aksiyomları sağlanmış olur: $\{1\} \cup \{2,3\} = X$ ve
$\{1\} \cap \{2,3\} = \emptyset$ zaten $\tau$'dadır.

### Örnek 5.4 — Alexandrov Zincir Uzayı

```python
from pytop import finite_chain_space

c = finite_chain_space(3)
print("Taşıyıcı:", c.carrier)
print("Topoloji:", sorted(str(t) for t in c.topology))
```

```text
Taşıyıcı: (1, 2, 3)
Topoloji: ['set()', '{1, 2, 3}', '{1, 2}', '{1}']
```

**Çıktı Açıklaması:** $n = 3$ zincirinde topoloji $\{\emptyset, \{1\}, \{1,2\}, \{1,2,3\}\}$
şeklindedir. Her açık küme bir "önek"tir: noktalar soldan sağa "giderek az açık" hale gelir.
Bu Alexandrov topolojisinin sezgisel yorumudur.

### Örnek 5.5 — Bazdan Topoloji Üretimi

```python
from pytop import topology_from_basis

b = [{1}, {2, 3}, {4}]
ts = topology_from_basis({1, 2, 3, 4}, b)
print("Baz:", [set(x) for x in b])
print("|τ| =", len(ts.topology))
print("Topoloji:", sorted(str(t) for t in ts.topology))
```

```text
Baz: [{1}, {2, 3}, {4}]
|τ| = 8
Topoloji: ['set()', '{1, 2, 3, 4}', '{1, 2, 3}', '{1, 4}', '{1}', '{2, 3, 4}', '{2, 3}', '{4}']
```

**Çıktı Açıklaması:** Baz $\{\{1\}, \{2,3\}, \{4\}\}$ bir bölüntüden oluşur; her çift
kesişimi boştur (B2 trivially sağlanır). Oluşturulan 8 açık küme, baz elemanlarının
tüm olası birleşimlerinden elde edilir. Bu yapı bölüntü-topolojisinin özel bir örneğidir.

### Örnek 5.6 — Sonsuz Uzay: Gerçek Doğru

```python
from pytop import real_line_metric

rl = real_line_metric()
print("Taşıyıcı:", rl.carrier)
print("Etiketler:", sorted(rl.tags))
```

```text
Taşıyıcı: R
Etiketler: ['complete', 'connected', 'first_countable', 'hausdorff', 'infinite',
            'lindelof', 'metric', 'not_compact', 'path_connected', 'second_countable',
            'separable', 't0', 't1', 'uncountable']
```

**Çıktı Açıklaması:** Gerçek doğru simgesel olarak temsil edilir; `topology=None`.
Topolojik özellikler etiketlerde kodlanmıştır: ikinci-sayılabilir, ayrılabilir, Lindelöf,
tam metrik fakat kompakt değil.

---

## 6. Alıştırmalar

### Kodlama Alıştırmaları

**K1.** $X = \{a, b, c\}$ üzerinde `make_topology` kullanarak T1 ama T2 (Hausdorff) olmayan
bir topoloji inşa edin. (İpucu: kosonlu topolojiyi düşünün.)

**K2.** `topology_from_subbasis({1,2,3,4}, [{1,2},{3,4},{2,3}])` çağrısının ürettiği
topolojinin kaç açık küme içerdiğini bulun ve açık kümeleri listeleyin.

**K3.** `finite_chain_space(5)` ile bir Alexandrov-5 zinciri oluşturun; topolojinin kaç açık
küme içerdiğini ve hangi elemanların "en açık" (yani en küçük açık kümede yer alan) nokta
olduğunu bulun.

### Teori Alıştırmaları

**T1.** $X = \{1, 2, 3\}$ üzerinde kaç farklı topoloji tanımlanabilir? Bu sayıyı T1–T3
aksiyomlarını doğrudan kontrol ederek hesaplamak yerine neden baz teoremini kullanmak daha
pratiktir?

**T2.** Ayrık topolojinin her zaman diğer topolojilerden daha ince, indirgenmiş topolojinin
ise daha kaba olduğunu kanıtlayın. Bu kanıt için T1–T3 aksiyomlarından hangisini kullanmanız
gerekiyor?
