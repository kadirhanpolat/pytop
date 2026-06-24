## Bölüm 5: Yüklemler ve Operatörler

Bu dosya Bölüm 5'in (Yüklemler ve Altküme Operatörleri) kodlama ve teori
alıştırmalarının çözümlerini içerir. Kodlama çözümleri çalıştırılabilir;
beklenen çıktılar `text` bloklarında verilmiştir.

### Kodlama Çözümleri

**K1.** İki noktalı indirgenmiş topolojide her noktanın komşuluk sistemi.

```python
from pytop import make_topology, neighborhood_system, analyze_neighborhood_system

ind = make_topology({0, 1})  # yalniz {} ve X acik: indirgenmis topoloji
carrier = list(ind.carrier)
topology = list(ind.topology)
print("N(0) =", neighborhood_system(carrier, topology, 0).value)
print("N(1) =", neighborhood_system(carrier, topology, 1).value)
print("N1-N4 ok? =", analyze_neighborhood_system(carrier, topology).status)
```

```text
N(0) = [['0', '1']]
N(1) = [['0', '1']]
N1-N4 ok? = true
```

İndirgenmiş topolojide her noktanın tek komşuluğu $X$'tir; N1–N4 aksiyomları sağlanır.

**K2.** $X=\{1,2,3,4\}$, $\tau=\{\emptyset,\{1,2\},\{3,4\},X\}$ üzerinde
$\mathrm{bd}(\{1,2,3\})$ ve $\mathrm{cl}(\{1,2,3\})$.

```python
from pytop import make_topology, boundary_of_subset, closure_of_subset

sp = make_topology({1, 2, 3, 4}, {1, 2}, {3, 4})
print("bd({1,2,3}) =", boundary_of_subset(sp, {1, 2, 3}).value)
print("cl({1,2,3}) =", closure_of_subset(sp, {1, 2, 3}).value)
```

```text
bd({1,2,3}) = frozenset({3, 4})
cl({1,2,3}) = frozenset({1, 2, 3, 4})
```

$\{3,4\}$ açık olduğundan $3$, $\{1,2,3\}$'ün sınır noktasıdır; $4$ de öyle. Kapanış $X$'tir.

**K3.** `finite_chain_space(4)` zincirinde $\{1,2\}$'nin iç, kapanış, sınır.

```python
from pytop import finite_chain_space, interior_of_subset, closure_of_subset, boundary_of_subset

c = finite_chain_space(4)
print("int({1,2}) =", interior_of_subset(c, {1, 2}).value)
print("cl({1,2})  =", closure_of_subset(c, {1, 2}).value)
print("bd({1,2})  =", boundary_of_subset(c, {1, 2}).value)
```

```text
int({1,2}) = frozenset({1, 2})
cl({1,2})  = frozenset({1, 2, 3, 4})
bd({1,2})  = frozenset({3, 4})
```

$\{1,2\}$ açıktır (içi kendisi). Kapanışı tüm zincirdir, çünkü $3$ ve $4$'ün her açık
komşuluğu $\{1,2\}$'yi keser. Sınır $\{3,4\}$ kalan noktalardır.

**K4.** $X = A^\circ \cup \partial A \cup \mathrm{ext}(A)$ ayrık parçalanışını doğrulayın.

```python
from pytop import make_topology, interior_of_subset, boundary_of_subset, exterior_of_subset

sp = make_topology({1, 2, 3, 4, 5}, {1, 2}, {4, 5}, {1, 2, 4, 5})
A = {1, 2, 3}
ic = set(interior_of_subset(sp, A).value)
sinir = set(boundary_of_subset(sp, A).value)
dis = set(exterior_of_subset(sp, A).value)
birlesim = ic | sinir | dis
print("ic    =", sorted(ic))
print("sinir =", sorted(sinir))
print("dis   =", sorted(dis))
print("birlesim == X? =", birlesim == {1, 2, 3, 4, 5})
print("ayrik? =", len(ic & sinir) == 0 and len(ic & dis) == 0 and len(sinir & dis) == 0)
```

```text
ic    = [1, 2]
sinir = [3]
dis   = [4, 5]
birlesim == X? = True
ayrik? = True
```

Üç küme örtüşmeden $X$'i kaplar — iç-sınır-dış ayrık parçalanışının somut doğrulaması.

**K5.** `finite_chain_space(4)` için Kuratowski kontrolü ve $\{1\}$'in yoğunluğu.

```python
from pytop import finite_chain_space, kuratowski_closure_check, closure_of_subset, is_dense_subset

c = finite_chain_space(4)
report = kuratowski_closure_check(list(c.carrier), list(c.topology))
print("kuratowski all =", report["all"])
print("cl({1})        =", closure_of_subset(c, {1}).value)
print("{1} dense?     =", is_dense_subset(c, {1}).status)
```

```text
kuratowski all = True
cl({1})        = frozenset({1, 2, 3, 4})
{1} dense?     = true
```

Kapanış operatörü K1–K4'ü sağlar (`all = True`) ve $\{1\}$ jenerik noktadır:
$\mathrm{cl}(\{1\}) = X$, yani yoğundur.

### Teori Çözümleri

**T1.** $A^\circ = X \setminus \mathrm{cl}(X \setminus A)$.

İç tanımı: $A^\circ$, $A$'ya dahil açık kümelerin birleşimidir (en büyük açık alt-küme).
Bir $x$ noktası $A^\circ$'da değildir ancak ve ancak $x$'in her açık komşuluğu $X\setminus A$'yı
kesiyorsa, yani $x \in \mathrm{cl}(X\setminus A)$. Bu mantıksal denkliğin tümleyeni alınırsa
$x \in A^\circ \iff x \notin \mathrm{cl}(X\setminus A)$, dolayısıyla
$A^\circ = X\setminus\mathrm{cl}(X\setminus A)$. Kuratowski (K2) ile $X\setminus A \subseteq
\mathrm{cl}(X\setminus A)$ olduğundan tümleyen gerçekten $A$'ya dahildir; (K3) idempotentlik
sağ tarafın açık (yani kapalı bir kümenin tümleyeni) olmasını garantiler.

**T2.** $A$ yoğun $\iff \mathrm{cl}(A) = X$.

($\Rightarrow$) $A$ yoğun olsun: her boş olmayan açık $U$ için $U \cap A \neq \emptyset$.
$\mathrm{cl}(A) \neq X$ varsayalım; o zaman $U = X\setminus\mathrm{cl}(A)$ boş olmayan bir
açık kümedir ve $U \cap A = \emptyset$ (çünkü $A \subseteq \mathrm{cl}(A)$). Bu yoğunlukla
çelişir; demek ki $\mathrm{cl}(A) = X$.
($\Leftarrow$) $\mathrm{cl}(A) = X$ olsun ve $U \neq \emptyset$ açık alın. $x \in U$ seçin.
$x \in X = \mathrm{cl}(A)$ olduğundan $x$'in her açık komşuluğu — özellikle $U$ — $A$'yı keser,
yani $U \cap A \neq \emptyset$. Demek ki $A$ yoğundur.

**T3.** $X = A^\circ \cup \partial A \cup \mathrm{ext}(A)$ ayrık parçalanışı.

Tanımlar: $\partial A = \mathrm{cl}(A)\setminus A^\circ$ ve $\mathrm{ext}(A) =
(X\setminus A)^\circ = X\setminus\mathrm{cl}(A)$ (dualite, T1). Birleşim:
$A^\circ \cup \partial A = \mathrm{cl}(A)$ (çünkü $A^\circ \subseteq \mathrm{cl}(A)$ ve
$\partial A$ farkı tamamlar); buna $\mathrm{ext}(A) = X\setminus\mathrm{cl}(A)$ eklenince
sonuç $X$ olur. Ayrıklık: $A^\circ \subseteq \mathrm{cl}(A)$ iken $\mathrm{ext}(A)$ onun
tümleyenidir (kesişim boş); $\partial A = \mathrm{cl}(A)\setminus A^\circ$ tanımı gereği
$A^\circ$ ile ayrıktır ve $\mathrm{cl}(A)$ içinde kaldığından $\mathrm{ext}(A)$ ile de
ayrıktır. Üç küme ikişer ikişer ayrık ve birleşimleri $X$ — bir parçalanış.
(Somut doğrulama: Örnek 5.6 ve K4.)

**T4.** $A^\circ$ açıktır ama genel olarak kapalı değildir.

$A^\circ$ açık kümelerin birleşimi olduğundan daima açıktır. Kapalı olmaması için bir
karşı-örnek: Örnek 5.6'daki `make_topology({1,2,3,4,5}, {1,2}, {4,5}, {1,2,4,5})` uzayında
$A=\{1,2,3\}$ için $A^\circ = \{1,2\}$. Bu küme açıktır, fakat tümleyeni
$X\setminus\{1,2\} = \{3,4,5\}$ bu topolojide açık **değildir** (açıklar yalnız $\emptyset,
\{1,2\}, \{4,5\}, \{1,2,4,5\}, X$), dolayısıyla $\{1,2\}$ kapalı değildir. Yani iç işlemi
açıklığı korur ama kapalılığı garanti etmez.
