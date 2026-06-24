# Alıştırma Çözümleri

Bu ek, Bölüm 4 ve Bölüm 6 alıştırmalarının tam çözümlerini içerir. Kodlama
çözümlerindeki tüm çıktılar gerçek çalıştırmadan alınmıştır; teori çözümleri tam
argüman verir.

---

---

## Bölüm 1: Hızlı Başlangıç

### K1 — İçi dolu üçgen vs boş üçgen

(ch01 K1 alıştırmasına dön)

```python
from pytop import simplicial_complex, betti_numbers

filled = simplicial_complex([[0], [1], [2], [0, 1], [1, 2], [0, 2], [0, 1, 2]])
empty = simplicial_complex([[0], [1], [2], [0, 1], [1, 2], [0, 2]])
print("dolu ucgen:", betti_numbers(filled))
print("bos ucgen :", betti_numbers(empty))
```

```text
dolu ucgen: (1, 0, 0)
bos ucgen : (1, 1)
```

İki kompleks de aynı köşelere ve kenarlara sahiptir; tek fark dolu komplekste
`[0,1,2]` 2-simpleksinin (üçgenin içinin) bulunmasıdır. Boş üçgende kenar
döngüsü `0→1→2→0` sınırlanmamış bir 1-çevrimdir, dolayısıyla `H_1 = Z` (bir
delik). Dolu üçgende bu döngü artık 2-simpleksin sınırıdır — yani sınırlanmış
bir çevrim olur ve homolojide sıfıra iner: `H_1 = 0`. "Deliği kapatmak" tam
olarak içini doldurmak demektir.

### K2 — Daha seyrek örnekleme: 4 nokta

(ch01 K2 alıştırmasına dön)

```python
import math
from pytop import (FiniteMetricSpace, persistent_homology,
                   persistence_betti_numbers)

pts = tuple(
    (round(math.cos(2 * math.pi * k / 4), 4),
     round(math.sin(2 * math.pi * k / 4), 4))
    for k in range(4)
)
space = FiniteMetricSpace(carrier=pts, distance=math.dist)
pairs = persistent_homology(space, max_dimension=1, max_scale=1.5)
essential = [p for p in pairs if p.is_essential]
print("kalici H1:", sum(1 for p in essential if p.dimension == 1))
print("betti    :", persistence_betti_numbers(pairs))
```

```text
kalici H1: 1
betti    : {0: 1, 1: 1}
```

Çemberi yalnızca 4 noktayla örneklesek bile (bir kare), kalıcı homoloji hâlâ
tek bir kalıcı `H_1` döngüsü bulur: `(1, 1)`. Sebebi, dört noktanın kenarları
filtrasyonda kare çerçeveyi oluşturup içi henüz dolmadan bir döngü yaratmasıdır.
Örnekleme yoğunluğu azaldıkça döngünün doğduğu/öldüğü ölçek değişir, ama topoloji
(tek delik) yeterli ölçek aralığında korunur — kalıcı homolojinin "gürültüye
karşı sağlamlık" özelliği budur. Çok az noktada veya yanlış `max_scale` seçiminde
döngü kaybolabilir; burada `max_scale=1.5` köşegeni (`√2 ≈ 1.41`) kapsayıp
döngüyü hayatta tutacak kadar geniştir.

### T1 — Sonlu uzay neden çemberle aynı π₁'e sahip?

(ch01 T1 alıştırmasına dön)

`finite_circle()` 4 noktalı bir T0 sonlu uzaydır. Sonlu T0 uzaylar ile sonlu
sıralı kümeler (preorder) birebir karşılık gelir; bu sıralamanın **düzen
kompleksi** (order complex / McCord kompleksi) bir simpliksel komplekstir.

**McCord teoremi (1966)** şunu söyler: her sonlu T0 uzay `X` ile onun düzen
kompleksi `|K(X)|` arasında **zayıf homotopi denkliği** veren sürekli bir
gönderim vardır. Zayıf homotopi denkliği tüm homotopi gruplarını (özellikle
`π_1`'i) ve homolojiyi korur.

`finite_circle()`'ın düzen kompleksi tam da bir çember triangülasyonudur (4
köşe, 4 kenar, 0 üçgen — kapanmış bir poligon), dolayısıyla `|K(X)| ≃ S^1` ve
`π_1(X) ≅ π_1(S^1) = Z` olur. Tek cümleyle: **sonlu uzayın "topolojik özü"
düzen kompleksinde yaşar; o kompleks bir çember olduğundan temel grup ℤ'dir.** ∎

---

## Bölüm 2: Önermeler Mantığı

### Alıştırma 6 — Dağılma Yasası (∧ üzerinden ∨)

(ch02 6. alıştırmasına dön)

İki değişkenli `check_tautology` deseni üç değişkene genişletilir: artık sekiz
`(p, q, r)` atamasının tümünü gezeriz. `iff` her atamada `True` dönerse ifade
bir tautolojidir.

```python
from pytop import Proposition, conjunction, disjunction, iff

triples = [(a, b, c) for a in (True, False)
                     for b in (True, False)
                     for c in (True, False)]

def check_tautology3(name, func):
    ok = all(
        func(Proposition("p", tp), Proposition("q", tq), Proposition("r", tr)).truth_value
        for tp, tq, tr in triples
    )
    print(f"{name}: {'tautoloji' if ok else 'DEGIL'}")

check_tautology3("p&(q|r) <-> (p&q)|(p&r)",
    lambda p, q, r: iff(conjunction(p, disjunction(q, r)),
                        disjunction(conjunction(p, q), conjunction(p, r))))
```

```text
p&(q|r) <-> (p&q)|(p&r): tautoloji
```

Sekiz satırın tamamında sol taraf `p & (q | r)` ile sağ taraf
`(p & q) | (p & r)` aynı doğruluk değerini alır. Sezgisel olarak: `p` yanlışsa
iki taraf da yanlıştır; `p` doğruysa her iki taraf da `q | r`'ye indirgenir.
Dolayısıyla `∧`, `∨` üzerinde dağılır. (Simetrik biçimde `∨`, `∧` üzerinde de
dağılır — `q` ile `r`'yi `∨`/`∧` rollerini değiştirerek aynı yöntemle
doğrulayabilirsiniz.)

### Alıştırma 7 — Kontrapozitif ≠ Tersi (Teori)

(ch02 7. alıştırmasına dön)

İddia yanlıştır: `p → q` doğru olduğunda `q → p` (tersi / converse) doğru olmak
**zorunda değildir**. `p → q`'nin gerçekten denk olduğu ifade kontrapozitif
`¬q → ¬p`'dir, tersi değil.

**Somut karşı-örnek.** `p` = "tam sayı 4'e bölünür", `q` = "tam sayı çifttir"
olsun.

- `p → q` **doğrudur**: 4'e bölünen her sayı çifttir (ör. 4, 8, 12).
- Tersi `q → p` **yanlıştır**: çift olan her sayı 4'e bölünmez — `6` çifttir
  ama 4'e bölünmez, yani `q` doğru iken `p` yanlıştır. Bu tek karşı-örnek
  `q → p`'yi çürütür.
- Kontrapozitif `¬q → ¬p` **doğrudur**: "çift değilse (tek ise) 4'e de bölünmez"
  — bu, `p → q` ile mantıksal olarak aynı içeriği taşır.

Genel kural: bir içerme her zaman kontrapozitifine denktir
(`(p → q) ↔ (¬q → ¬p)`, Bölüm 4'teki doğruluk tablosu kanıtı), ama tersine veya
 inverse'üne (`¬p → ¬q`) denk değildir. Öncül ile sonucu yer değiştirmek mantığın
yönünü tersine çevirir; yalnızca her ikisini birden olumsuzlayıp yer değiştirmek
(yani kontrapozitif) anlamı korur.

---

## Bölüm 3: Küme Teorisi

### K1 — A∪B, A∩B, A\B

(ch03 K1 alıştırmasına dön)

```python
from pytop import (
    make_set, power_set, set_union, set_intersection, set_difference,
    complement, cartesian_product, equal_sets,
    make_relation, relation_profile, is_equivalence_relation,
    equivalence_class, compose_relations, inverse_relation,
)

A = make_set(1, 2, 3, 4, 5)
B = make_set(3, 4, 5, 6, 7)
print("A u B:", sorted(set_union(A, B)))
print("A n B:", sorted(set_intersection(A, B)))
print("A \\ B:", sorted(set_difference(A, B)))
```

```text
A u B: [1, 2, 3, 4, 5, 6, 7]
A n B: [3, 4, 5]
A \ B: [1, 2]
```

A ∩ B = {3,4,5} ortak elemanlar; A \ B = {1,2} yalnız A'da olanlar.

---

### K2 — {1,2,3,4} güç kümesi

(ch03 K2 alıştırmasına dön)

```python
P = power_set([1, 2, 3, 4])
print("|P({1,2,3,4})| =", len(P))
```

```text
|P({1,2,3,4})| = 16
```

Teorem 2.2 gereği |P(A)| = 2⁴ = 16.

---

### K3 — Tam çarpım bağıntısı denkliktir

(ch03 K3 alıştırmasına dön)

```python
carrier = [0, 1, 2]
R = make_relation(carrier, *[(i, j) for i in carrier for j in carrier])
prof = relation_profile(carrier, R)
print("yansimalı:", prof['is_reflexive'])
print("simetrik :", prof['is_symmetric'])
print("gecisli  :", prof['is_transitive'])
print("denklik  :", is_equivalence_relation(carrier, R))
```

```text
yansimalı: True
simetrik : True
gecisli  : True
denklik  : True
```

Tam çarpım R = A × A her zaman denkliktir: her ikili mevcut olduğundan üç aksiyom
trivially sağlanır. Tek denklik sınıfı tüm taşıyıcıdır.

---

### K5 — Mod-2 denkliği

(ch03 K5 alıştırmasına dön)

```python
c5 = [0, 1, 2, 3, 4]
mod2 = make_relation(c5, *[(i, j) for i in c5 for j in c5 if (i - j) % 2 == 0])
print("[0] =", sorted(equivalence_class(c5, mod2, 0)))
print("[1] =", sorted(equivalence_class(c5, mod2, 1)))
```

```text
[0] = [0, 2, 4]
[1] = [1, 3]
```

İki sınıf: çiftler {0,2,4} ve tekler {1,3}. Bunlar {0,..,4}'ün bir bölüntüsüdür.

---

### K6 — De Morgan (X = {1,…,8})

(ch03 K6 alıştırmasına dön)

```python
X = make_set(1, 2, 3, 4, 5, 6, 7, 8)
A = make_set(1, 2, 3, 4)
B = make_set(3, 4, 5, 6)
dm1_l = complement(set_union(A, B), X)
dm1_r = set_intersection(complement(A, X), complement(B, X))
dm2_l = complement(set_intersection(A, B), X)
dm2_r = set_union(complement(A, X), complement(B, X))
print("(A u B)^c:", sorted(dm1_l), "==", sorted(dm1_r), "->", sorted(dm1_l) == sorted(dm1_r))
print("(A n B)^c:", sorted(dm2_l), "==", sorted(dm2_r), "->", sorted(dm2_l) == sorted(dm2_r))
```

```text
(A u B)^c: [7, 8] == [7, 8] -> True
(A n B)^c: [1, 2, 5, 6, 7, 8] == [1, 2, 5, 6, 7, 8] -> True
```

A ∪ B = {1,…,6} olduğundan tümleyeni {7,8}; A ∩ B = {3,4} olduğundan tümleyeni
{1,2,5,6,7,8}. Her iki De Morgan eşitliği de doğrulanır.

---

### K7 — Kartezyen çarpım değişmeli değildir

(ch03 K7 alıştırmasına dön)

```python
Pp = make_set('x', 'y', 'z')
Qq = make_set(0, 1)
pq = cartesian_product(Pp, Qq)
qp = cartesian_product(Qq, Pp)
print("|PxQ| =", len(pq), "| |QxP| =", len(qp))
print("PxQ == QxP :", equal_sets(pq, qp))
```

```text
|PxQ| = 6 | |QxP| = 6
PxQ == QxP : False
```

Boyutlar eşittir (|P|·|Q| = 3·2 = 6 = |Q|·|P|), ama kümeler farklıdır:
P × Q'nun ikilileri (x,0) biçiminde, Q × P'ninkiler (0,x) biçimindedir.

---

### T1 — A ⊆ B ⟺ A ∩ B = A

(ch03 T1 alıştırmasına dön)

**(⟹)** A ⊆ B varsayalım. A ∩ B ⊆ A her zaman doğrudur. Ters kapsama için
a ∈ A alalım; A ⊆ B olduğundan a ∈ B, dolayısıyla a ∈ A ∩ B. Böylece A ⊆ A ∩ B,
yani A ∩ B = A.

**(⟸)** A ∩ B = A varsayalım. a ∈ A alalım; o halde a ∈ A ∩ B = A, özellikle
a ∈ B. Demek ki A ⊆ B. ∎

---

### T2 — Enjeksiyonların bileşimi enjeksiyondur

(ch03 T2 alıştırmasına dön)

f: A → B ve g: B → C enjeksiyon olsun. (g ∘ f)(a₁) = (g ∘ f)(a₂) varsayalım, yani
g(f(a₁)) = g(f(a₂)). g enjeksiyon olduğundan f(a₁) = f(a₂). f enjeksiyon
olduğundan a₁ = a₂. Dolayısıyla g ∘ f enjeksiyondur. ∎

---

### T3 — (R∘S)⁻¹ = S⁻¹∘R⁻¹ (sonlu doğrulama)

(ch03 T3 alıştırmasına dön)

```python
R = make_relation([1, 2, 3], (1, 2), (2, 3))
S = make_relation([1, 2, 3], (1, 3), (2, 1))
# pytop konvansiyonu: compose_relations(first, second) = second o first
RoS = compose_relations(S, R)          # R o S
lhs = inverse_relation(RoS)            # (R o S)^-1
rhs = compose_relations(inverse_relation(R), inverse_relation(S))  # S^-1 o R^-1
print("(R o S)^-1 :", sorted(lhs))
print("S^-1 o R^-1:", sorted(rhs))
print("esit mi    :", sorted(lhs) == sorted(rhs))
```

```text
(R o S)^-1 : [(2, 2)]
S^-1 o R^-1: [(2, 2)]
esit mi    : True
```

`compose_relations(S, R)` pytop konvansiyonunda R ∘ S'tir (önce S, sonra R). Bu
örnekte R ∘ S = {(2,2)}: S ile 2→1, ardından R ile 1→2. Tersini almak çiftleri
ters çevirir ve sağ taraf S⁻¹ ∘ R⁻¹ ile aynı kümeyi verir — soyut özdeşlik sonlu
örnekte doğrulanır. ∎

---

## Bölüm 4: Topolojik Uzaylar

### K1 — cofinite_topology keşfi

(ch04 K1 alıştırmasına dön)

```python
from pytop import cofinite_topology, is_t1, is_t2

c = cofinite_topology('a', 'b', 'c')
print("|tau| =", len(c.topology))
print("Etiketler:", sorted(c.tags))
print("T1:", is_t1(c).status, "| T2:", is_t2(c).status)
```

```
|tau| = 8
Etiketler: ['cofinite', 'compact', 'finite', 't1']
T1: true | T2: true
```

Üç elemanlı kümede tüm alt kümeler kosonlu koşulunu sağlar; `|tau| = 2^3 = 8`:
topoloji ayrıktır. Sonlu kümede T1 => tekiller kapalı => her alt küme kapalı =>
her alt küme açık; T1 olan sonlu uzay zorunlu olarak ayrık, dolayısıyla
Hausdorff'tur. T1 olup T2 olmayan örnek için taşıyıcı sonsuz olmalıdır: kosonlu
N'de boş olmayan iki açık daima kesişir.

---

### K2 — topology_from_subbasis keşfi

(ch04 K2 alıştırmasına dön)

```python
from pytop import topology_from_subbasis

s = topology_from_subbasis({1, 2, 3, 4}, [{1, 2}, {3, 4}, {2, 3}])
print("|tau| =", len(s.topology))
print("Acik kumeler:", sorted(sorted(t) for t in s.topology))
```

```
|tau| = 9
Acik kumeler: [[], [1, 2], [1, 2, 3], [1, 2, 3, 4], [2], [2, 3], [2, 3, 4], [3], [3, 4]]
```

Alt-baz çiftlerinin kesişimleri `{2}`, `{3}`, `∅` yeni baz elemanları üretir;
birleşimler `{1,2,3}`, `{2,3,4}` ve `X`'i ekler. Toplam 9 açık küme. Alt-baz bir
topoloji üretmek için yeterlidir: önce sonlu kesişimler altında kapatılır, sonra
keyfi birleşimler altında kapatılır.

---

### K3 — finite_chain_space(5) keşfi

(ch04 K3 alıştırmasına dön)

```python
from pytop import finite_chain_space

c5 = finite_chain_space(5)
print("|tau| =", len(c5.topology))
print("Acik kumeler:", sorted(sorted(t) for t in c5.topology))
```

```
|tau| = 6
Acik kumeler: [[], [1], [1, 2], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 5]]
```

Açıklar 6 önektir. "En açık" nokta 1'dir: tek elemanlı `{1}` açığında ve
dolayısıyla her boş olmayan açıkta yer alır; 5 ise yalnızca `X`'tedir.

---

### T1 — {1,2,3} üzerinde kaç topoloji?

(ch04 T1 alıştırmasına dön)

`X = {1,2,3}` üzerinde tam olarak **29** farklı topoloji vardır (homeomorfizma
sınıfı olarak 9). Doğrudan yöntem `P(P(X))`'in `2^8 = 256` elemanlı aday
ailesinin her birinde üç aksiyomu denetlemeyi gerektirir. Baz teoremi işi tersine
çevirir: (B1)–(B2)'yi sağlayan küçük aileler seçilir, her biri otomatik olarak
geçerli bir topoloji üretir; yalnız üretilen topolojilerin tekrarları ayıklanır.
Aksiyom denetimi aday başına yapılmaz — üretim doğruluğu Baz Teoremi'nce
garantilidir.

---

### T2 — Ayrık en ince, indirgenmiş en kabadır

(ch04 T2 alıştırmasına dön)

**Ayrık en incedir:** Herhangi bir `tau` topolojisi tanım gereği
`tau ⊆ P(X) = tau_disc` sağlar; hiçbir aksiyoma gerek yoktur, "topoloji X'in alt
kümelerinden oluşur" tanımı yeter. **İndirgenmiş en kabadır:** (T1) aksiyomu her
topolojinin `∅` ve `X`'i içermesini zorunlu kılar;
`tau_ind = {∅, X} ⊆ tau`. Kullanılan tek aksiyom (T1)'dir. ∎

---

---

## Bölüm 4 (ek): Topolojik Uzaylar

Bu dosya, Bölüm 4'e eklenen yeni alıştırmaların (K4, T3) çözümlerini içerir;
mevcut `solutions.md` içindeki Bölüm 4 çözümleri (K1–K3, T1–T2) olduğu gibi kalır.

### K4 — count_topologies_on_n_points doğrulaması

(ch04 K4 alıştırmasına dön)

```python
from pytop import count_topologies_on_n_points

for n in range(0, 5):
    print(f"n={n}: {count_topologies_on_n_points(n)}")
```

```
n=0: 1
n=1: 1
n=2: 4
n=3: 29
n=4: 355
```

`n=3` satırı T1 alıştırmasındaki "29 topoloji" iddiasını birebir doğrular. `n=4`
için sonuç `355`'tir; oysa $\{1,2,3,4\}$'ün açık küme ailesi olarak seçilebilecek
aday sayısı $2^{2^4}=65536$'dır. Aradaki uçurum, üç aksiyomun (T1–T3) bu
adayların ezici çoğunluğunu elemesinden gelir: rastgele bir alt-küme ailesi
neredeyse hiçbir zaman birleşim/kesişim altında kapalı değildir. Dizi OEIS
A000798'dir (sonlu topolojilerin sayısı) ve etiketsiz uzaylar üzerinde tanımlıdır.

### T3 — excluded_point_topology(3, 0): T0 ama T1 değil

(ch04 T3 alıştırmasına dön)

```python
from pytop import excluded_point_topology, is_t0, is_t1, is_t2

ep = excluded_point_topology(3, 0)   # X = {0,1,2}, 0 dislanir
print("Acik:", sorted(sorted(t) for t in ep.topology))
print("T0:", is_t0(ep).status, "| T1:", is_t1(ep).status, "| T2:", is_t2(ep).status)
```

```
Acik: [[], [0, 1, 2], [1], [1, 2], [2]]
T0: true | T1: false | T2: false
```

**Kanıt.** Dışlanan-nokta topolojisinde bir küme açıktır ancak ve ancak ya
dışlanan nokta $0$'ı içermez ya da tüm uzaydır. Dolayısıyla $0$'ı içeren *tek*
açık küme $X=\{0,1,2\}$'dir.

- **T0 (sağlanır):** İki farklı nokta alalım. Eğer çift `{0, y}` ise (`y` farklı),
  `{y}` açıktır, `y`'yi içerir, `0`'ı içermez — bir yön ayırır. Eğer çift
  `{x, y}` ve ikisi de `0` değilse, `{x}` açıktır ve `x`'i `y`'den ayırır. Her
  durumda en az bir yön ayrıldığından uzay T0'dır.
- **T1 (sağlanmaz):** T1 için *her iki yönün de* ayrılması gerekir. `0` ile
  `1` çiftine bakalım: `1`'i içerip `0`'ı dışlayan açık vardır (`{1}`), ama
  `0`'ı içerip `1`'i dışlayan açık **yoktur** — çünkü `0`'ı içeren tek açık
  küme bütün uzaydır ve o da `1`'i içerir. Bu yüzden `(0, 1)` çifti `0→1`
  yönünde ayrılamaz ve uzay T1 değildir.

**Sierpiński ile karşılaştırma.** Sierpiński uzayı $X=\{0,1\}$, $\tau=\{\emptyset,\{1\},X\}$
tam olarak `excluded_point_topology(2, 0)`'a denktir: dışlanan nokta `0`, açık olan
yegâne öz alt-küme `{1}`'dir. `excluded_point_topology(3, 0)` ise bu aynı T0-ama-T1-değil
asimetrisini üç noktaya genişletir; "dışlanan nokta" daima en küçük açık komşuluğu tüm
uzay olan, topolojik olarak "yapışkan" noktadır.

---

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

---

## Bölüm 6: Ayrılma Aksiyomları

### K1 — make_topology ayrılma zinciri

(ch06 K1 alıştırmasına dön)

```python
from pytop import make_topology, separation_chain

k = make_topology({1, 2, 3}, {1}, {2}, {1, 2})
print("Acik kumeler:", sorted(sorted(t) for t in k.topology))
for prop, r in separation_chain(k).items():
    print(f"  {prop:20s}: {r.status}")
```

```
Acik kumeler: [[], [1], [1, 2], [1, 2, 3], [2]]
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

T0 sağlanır: `(1,2)` çiftini `{1}`, `(1,3)` çiftini `{1}`, `(2,3)` çiftini `{2}`
ayırır. T1 düşer: 3'ü içerip 1'i dışlayan açık yoktur (3 yalnız `X`'te).
`tychonoff: unknown` — sürekli fonksiyon ayırması açık-küme taramasıyla karara
bağlanmaz; kütüphane dürüstçe "bilinmiyor" der.

---

### K2 — finite_chain_space(3) en yüksek aksiyom

(ch06 K2 alıştırmasına dön)

```python
from pytop import finite_chain_space, separation_chain

for prop, r in separation_chain(finite_chain_space(3)).items():
    print(f"  {prop:20s}: {r.status}")
```

```
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

En yüksek sağlanan aksiyom **T0**'dır. Önek yapısı her çifti "daha solda olan"
lehine ayırır: `(1,2)` için `{1}`, `(2,3)` için `{1,2}`. T1 imkânsızdır: 2'yi
içerip 1'i dışlayan önek yoktur.

---

### K3 — two_point_indiscrete_space T0/T1/T2

(ch06 K3 alıştırmasına dön)

```python
from pytop import two_point_indiscrete_space, is_t0, is_t1, is_t2

tp = two_point_indiscrete_space()
print("T0:", is_t0(tp).status, "| T1:", is_t1(tp).status, "| T2:", is_t2(tp).status)
```

```
T0: false | T1: false | T2: false
```

Boş olmayan tek açık `X`'tir ve her iki noktayı da içerir; hiçbir çift hiçbir
yönden ayrılamaz. Zincirin tamamı en alt basamakta düşer.

---

### T1 — T2 => T1 => T0

(ch06 T1 alıştırmasına dön)

**T2 => T1:** `x ≠ y` verilsin. T2 ile ayrık `U ∋ x`, `V ∋ y` açıkları vardır.
`U ∩ V = ∅` olduğundan `y ∉ U` ve `x ∉ V`: hem "x'i içerip y'yi dışlayan" hem
"y'yi içerip x'i dışlayan" açık bulundu — T1'in iki yönlü koşulu sağlandı.
**T1 => T0:** T0 yalnız en az bir yönlü ayrım ister; T1'in verdiği iki yönlü
ayrımın herhangi biri yeter. ∎

---

### T2 — Sonlu T1 ⟺ Ayrık

(ch06 T2 alıştırmasına dön)

**(=>)** `X` sonlu ve T1 olsun. T1 gereği her `x` için ve her `y ≠ x` için
`y ∈ U_y`, `x ∉ U_y` olan açık `U_y` vardır; `X \ {x} = ⋃_{y≠x} U_y` açıktır,
yani `{x}` kapalıdır. Herhangi `A ⊆ X`, sonlu sayıda tekilin birleşimi olarak
kapalıdır; o halde tümleyeni `X \ A` açıktır. `A` keyfi olduğundan her alt küme
açıktır: topoloji ayrıktır.

**(<=)** Ayrık topolojide her `{x}` açıktır; `x ≠ y` için `{x}` ve `{y}` iki
yönlü ayrımı doğrudan verir, T1 (hatta T2) sağlanır. ∎

---

---

## Bölüm 6 (ek): Ayrılma Aksiyomları

### K4 — excluded_point_topology(4, 0) en yüksek aksiyom

(ch06 K4 alıştırmasına dön)

```python
from pytop import excluded_point_topology, separation_chain

ep = excluded_point_topology(4, 0)   # X = {0,1,2,3}, dışlanan nokta 0
for prop, r in separation_chain(ep).items():
    print(f"  {prop:20s}: {r.status}")
```

```text
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

Sağlanan en yüksek aksiyom **T0**'dır. Dışlanan-nokta topolojisinde bir küme ya
$0$'ı içermez ya da $X$'in kendisidir. Bu yüzden $1,2,3$ noktaları $\{1\},\{2\},
\{3\}$ gibi açıklarla iki yönlü; her $\{i, 0\}$ çifti ise $i$'yi içerip $0$'ı
dışlayan bir açıkla tek yönlü ayrılır — T0 tamam. T1 imkânsızdır: $0$'ı içeren
tek açık $X$'tir, dolayısıyla "$0$'ı içerip başka noktayı dışlayan açık" yoktur;
eşdeğer olarak $\{0\}$ kapalı değildir (tümleyeni $\{1,2,3\}$, $0$-içermediği
için açıktır, ama $\{0\}$'ın kendisi açık olmadığından kapalılık $\{0\}$'a
geçmez). T1 düşünce zincirin geri kalanı da düşer.

---

### T3 — Her metrik uzay normaldir (T4)

(ch06 T3 alıştırmasına dön)

**Strateji:** Ayrık iki kapalı küme arasında açık bir Urysohn fonksiyonu
mesafeyle elle inşa edilir; bu fonksiyonun seviye kümeleri aradığımız ayrık
açıkları verir.

$(X, d)$ bir metrik uzay, $C, D \subseteq X$ ayrık kapalı kümeler olsun
($C \cap D = \emptyset$). $A \neq \emptyset$ için $d(x, A) = \inf_{a \in A}
d(x, a)$ mesafe fonksiyonu süreklidir ve $A$ kapalıysa $d(x, A) = 0 \iff
x \in A$ sağlanır.

1. $C, D$ ayrık ve kapalı olduğundan her $x \in X$ için $d(x,C) + d(x,D) > 0$:
   payda hiçbir noktada sıfırlanmaz. (Eğer $d(x,C) = d(x,D) = 0$ olsaydı $x$ hem
   $C$'ye hem $D$'ye ait olurdu — çelişki.)

2.
   $$ f(x) = \frac{d(x,C)}{d(x,C) + d(x,D)} $$
   tanımla. $f$, sürekli fonksiyonların bölümü ve payda sıfırdan farklı
   olduğundan süreklidir; ayrıca $0 \le f \le 1$.

3. $x \in C \Rightarrow d(x,C) = 0 \Rightarrow f(x) = 0$ ve
   $x \in D \Rightarrow d(x,D) = 0 \Rightarrow f(x) = 1$: yani $f|_C \equiv 0$,
   $f|_D \equiv 1$ — tam bir Urysohn fonksiyonu.

4. $U = f^{-1}\big([0, \tfrac12)\big)$ ve $V = f^{-1}\big((\tfrac12, 1]\big)$ al.
   $f$ sürekli olduğundan $U, V$ açıktır; $C \subseteq U$ (çünkü $f|_C = 0$),
   $D \subseteq V$ (çünkü $f|_D = 1$) ve $U \cap V = \emptyset$ (bir nokta hem
   $<\tfrac12$ hem $>\tfrac12$ olamaz).

O halde her ayrık kapalı çift ayrık açıklara konabilir: metrik uzay normaldir.
Metrik uzaylar ayrıca T1'dir (tekiller kapalı), dolayısıyla **T4**'tür — ve
zincirin tüm üst basamakları (T3, T2.5, T2) bundan gelir. ∎

---

## Bölüm 7: Kompaktlık

### K1 — Sonlu uzaylar: zincir vs ayrık

(ch07 K1 alıştırmasına dön)

```python
from pytop import finite_chain_space, discrete_topology, is_compact

print("chain(5)   compact?", is_compact(finite_chain_space(5)).status)
print("discrete(5) compact?", is_compact(discrete_topology(1, 2, 3, 4, 5)).status)
```

```
chain(5)   compact? true
discrete(5) compact? true
```

Her ikisi de kompakttır — topolojinin inceliğinden bağımsız olarak **sonlu** her
uzay kompakttır: bir açık örtüde uzayı kaplayan elemanları seçersek zaten sonlu
çoklukta eleman almış oluruz.

### K2 — Kosonlu doğal sayılar

(ch07 K2 alıştırmasına dön)

```python
from pytop import naturals_cofinite, is_compact, is_lindelof
from pytop.compactness_variants import is_countably_compact

nc = naturals_cofinite()
print("compact?  ", is_compact(nc).status)
print("lindelof? ", is_lindelof(nc).status)
print("countably?", is_countably_compact(nc).status)
```

```
compact?   true
lindelof?  true
countably? true
```

Sonsuz olmasına rağmen kompakt: herhangi bir açık örtüden tek bir `U` seçtiğimizde
tümleyeni `X \ U` sonludur (kosonlu topolojinin tanımı); kalan sonlu çoklukta
noktayı kapatacak sonlu sayıda eleman eklenir. Bu, "kompakt = sınırlı" sezgisinin
yalnız metrik uzaylara özgü olduğunu gösterir.

### K3 — [0,1] vs ℝ karşılaştırması

(ch07 K3 alıştırmasına dön)

```python
from pytop import closed_unit_interval_metric, real_line_metric
from pytop.compactness_variants import analyze_compactness_variants

for name, space in [("[0,1]", closed_unit_interval_metric()),
                    ("R", real_line_metric())]:
    r = analyze_compactness_variants(space)
    lind = r.value["lindelof"]
    print(f"{name:6s} lindelof = {getattr(lind, 'status', lind)}")
```

```
[0,1]  lindelof = true
R      lindelof = true
```

İki uzay da Lindelöf'tür, ama temel fark `is_compact`'tedir: `[0,1]` kompakt
(kapalı + sınırlı), `ℝ` değil (sınırsız). Lindelöf, kompaktlıktan zayıf bir
özelliktir — sayılabilir alt-örtü garanti eder, sonlu değil.

### K4 — Tek-nokta kompaktifikasyon

(ch07 K4 alıştırmasına dön)

```python
from pytop import real_line_metric, one_point_compactification_of_reals, is_compact

print("R  compact?", is_compact(real_line_metric()).status)
print("R* compact?", is_compact(one_point_compactification_of_reals()).status)
```

```
R  compact? false
R* compact? true
```

ℝ lokal kompakt Hausdorff'tur ama kompakt değildir (Örnek 5.2). Alexandroff
inşası tek bir `∞` noktası ekler: sınırsız "kaçan" diziler artık `∞`'da yakınsar,
böylece her açık örtü `∞`'u içeren bir elemana — ve onun tümleyenindeki kompakt
parçaya sonlu alt-örtüye — sahip olur. Sonuç ℝ\* ≅ S¹ kompakttır.

### T1 — Kompakt + sürekli ⟹ görüntü kompakt

(ch07 T1 alıştırmasına dön)

`f: X → Y` sürekli, `X` kompakt olsun. `{V_α}`, `f(X)`'i örten açık aile olsun.
Süreklilikten her `f⁻¹(V_α)` açıktır ve `{f⁻¹(V_α)}`, `X`'i örter. `X` kompakt
olduğundan sonlu alt-örtü `f⁻¹(V_{α₁}), …, f⁻¹(V_{αₖ})` vardır. Bu kümeler `X`'i
kapladığından, görüntüleri `V_{α₁}, …, V_{αₖ}` de `f(X)`'i kaplar. Demek ki keyfi
açık örtünün sonlu alt-örtüsü var: `f(X)` kompakt. ∎

### T2 — Heine-Borel: [0,1] vs (0,1)

(ch07 T2 alıştırmasına dön)

`[0,1]` **kapalı ve sınırlıdır**, dolayısıyla Heine-Borel ile kompakttır. `(0,1)`
sınırlıdır ama **kapalı değildir** (uç noktaları içermez). Kapalılığın eksikliği
$U_n = (1/n, 1)$ "kaçan örtüsüyle" görünür hale gelir: bu aile `(0,1)`'i örter,
fakat herhangi sonlu alt-aile yalnız en büyük indis `N` için `(1/N, 1)`'i kaplar
ve `0`'a yakın noktalar dışarıda kalır. Sonlu alt-örtü olmadığından `(0,1)`
kompakt değildir. `[0,1]`'de `0` dahil olduğundan bu kaçış engellenir.

### T3 — Neden kompaktlık gerekir (T4 ispatında)

(ch07 T3 alıştırmasına dön)

Teorem 2.2 ispatında, sabit `a` için `{V_b}_{b∈B}` ailesi `B`'yi örten açık
kümelerden oluşur. `a` ile `B`'yi ayıran tek bir açık küme elde etmek için bu
aileden **sonlu** bir alt-örtü seçip `V_a = V_{b₁} ∪ … ∪ V_{bₖ}` ve
`U_a = U_{b₁} ∩ … ∩ U_{bₖ}` kurarız. Kesişimin açık kalması **sonluluğa**
bağlıdır: sonsuz çoklukta açık kümenin kesişimi açık olmak zorunda değildir. İşte
bu yüzden `B`'nin (ve sonra `A`'nın) **kompakt** olması şarttır — kompaktlık, bu
kritik sonlu-kesişim adımını mümkün kılar. ∎

---

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

---

## Bölüm 9: Sayılabilirlik

Bu bölüm, Bölüm 9 (Sayılabilirlik Aksiyomları) alıştırmalarının tam çözümlerini
içerir. Kodlama çözümlerindeki tüm çıktılar gerçek çalıştırmadan alınmıştır; teori
çözümleri tam argüman verir.

---

### K1 — finite_chain_space(5): 1. ve 2. sayılabilir

(ch09 K1 alıştırmasına dön)

```python
from pytop import finite_chain_space, is_first_countable, is_second_countable

c = finite_chain_space(5)
print("1st countable?", is_first_countable(c).status)
print("2nd countable?", is_second_countable(c).status)
```

```
1st countable? true
2nd countable? true
```

Sonlu uzayda topolojinin kendisi sonlu, dolayısıyla sayılabilir bir bazdır; her
nokta için komşuluk sistemi de sonludur. Bu yüzden her sonlu uzay hem 1. hem 2.
sayılabilirdir — sayılabilirlik aksiyomları yalnızca sonsuz uzaylarda ayırt edicidir.

---

### K2 — İki noktalı ayrık ve indirgenmiş: ayrılabilirlik

(ch09 K2 alıştırmasına dön)

```python
from pytop import two_point_discrete_space, two_point_indiscrete_space, is_separable

print("disc sep  ", is_separable(two_point_discrete_space()).status)
print("indisc sep", is_separable(two_point_indiscrete_space()).status)
```

```
disc sep   true
indisc sep true
```

İkisi de ayrılabilirdir, ama nedenleri farklıdır. Ayrık `{a,b}`'de yoğun küme her
açığı (`{a}` ve `{b}` dâhil) kesmek zorunda olduğundan taşıyıcının tamamı `{a,b}`
gerekir — sonlu olduğundan sayılabilir, dolayısıyla ayrılabilir. İndirgenmiş
`{a,b}`'de açıklar yalnız `∅` ve `X` olduğundan tek noktalı `{a}` bile yoğundur:
`X`'i keser. Ayrılabilirlik "sayılabilir yoğun küme var mı?" sorusudur; sonlu
uzayda yanıt her zaman evettir.

---

### K3 — integers_discrete(): sayılabilir ayrık 2. sayılabilirdir

(ch09 K3 alıştırmasına dön)

```python
from pytop import integers_discrete, is_second_countable

print("2nd countable?", is_second_countable(integers_discrete()).status)
```

```
2nd countable? true
```

Sayılabilir ayrık uzayda `{ {n} : n ∈ ℤ }` ailesi bir bazdır; ℤ sayılabilir
olduğundan bu baz da sayılabilirdir — uzay 2. sayılabilirdir. **Kritik nokta**
taşıyıcının sayılabilirliğidir: ayrık topolojide baz tüm tekilleri içermek
zorundadır, dolayısıyla baz büyüklüğü en az taşıyıcının büyüklüğüdür. Taşıyıcı
sayılabilirse 2. sayılabilir; sayılamazsa değil (bkz. K4).

---

### K4 — Sayılamaz ayrık vs sayılabilir ayrık

(ch09 K4 alıştırmasına dön)

```python
from pytop import (integers_discrete, uncountable_discrete_space,
                   countability_report)

print("integers_discrete:")
for k, v in countability_report(integers_discrete()).items():
    print(f"  {k:<17}: {v.status}")
print("uncountable_discrete:")
for k, v in countability_report(uncountable_discrete_space()).items():
    print(f"  {k:<17}: {v.status}")
```

```
integers_discrete:
  first_countable  : true
  second_countable : true
  separable        : true
  lindelof         : true
uncountable_discrete:
  first_countable  : true
  second_countable : false
  separable        : false
  lindelof         : false
```

Her ikisi de **1. sayılabilir**dir: ayrık uzayda her nokta için `{ {x} }` tek
elemanlı yerel bazdır, taşıyıcının büyüklüğünden bağımsız. **2. sayılabilir,
ayrılabilir ve Lindelöf** aksiyomlarında ise ayrışırlar. Üçü de "sayılabilir bir
küme tüm noktalara erişebilir mi?" sorusunun farklı yüzleridir: ayrık topolojide
bir baz tüm tekilleri, yoğun bir küme tüm noktaları, bir alt-örtü yine tüm
tekilleri içermek zorundadır. Taşıyıcı sayılabilirse hepsi mümkün, sayılamazsa
hiçbiri. Ayrım kaynağı tek başına **taşıyıcının kardinalitesi**dir.

---

### T1 — 2. sayılabilir ⟹ ayrılabilir

(ch09 T1 alıştırmasına dön)

`{B_n}` sayılabilir bir baz olsun. Her boş olmayan `B_n`'den bir nokta `d_n ∈ B_n`
seç (seçim aksiyomu sayılabilir aile için yeterli). `D = { d_n : B_n ≠ ∅ }` kümesi
sayılabilirdir, çünkü indeks kümesi `ℕ`'nin bir alt kümesidir.

`D`'nin yoğun olduğunu gösterelim: boş olmayan herhangi açık `U` alalım ve `x ∈ U`
olsun. Baz tanımı gereği `x ∈ B_n ⊆ U` olan bir `B_n` vardır. Bu `B_n` boş
değildir (en az `x` içerir), dolayısıyla `d_n ∈ B_n ⊆ U`. Demek ki `d_n ∈ U ∩ D`,
yani `U ∩ D ≠ ∅`. Boş olmayan her açık `D`'yi kestiğinden `D` yoğundur. `D`
sayılabilir olduğundan uzay ayrılabilirdir. ∎

---

### T2 — Sorgenfrey doğrusu 2. sayılabilir değildir

(ch09 T2 alıştırmasına dön)

Sorgenfrey doğrusu `ℝ_ℓ`, `[a,b)` biçimli yarı-açık aralıklarla üretilir. `{B_n}`
herhangi bir baz olsun ve bir `x ∈ ℝ` sabitleyelim. `[x, x+1)` açıktır ve `x`'i
içerir; baz tanımı gereği `x ∈ B_n ⊆ [x, x+1)` olan bir baz elemanı `B(x) := B_n`
vardır. Bu eleman `x`'i içerip `x`'in solundaki hiçbir noktayı içermez, yani
`inf B(x) = x`'tir.

Şimdi `x ↦ B(x)` eşlemesi **birebir**dir: `x < y` ise `inf B(x) = x ≠ y = inf B(y)`,
dolayısıyla `B(x) ≠ B(y)`. Demek ki baz, sayılamaz `ℝ` kümesinden bazına giden bir
injeksiyon barındırır; baz en az `|ℝ| = 𝔠` büyüklüktedir — sayılamaz. Hiçbir
sayılabilir baz olamayacağından `ℝ_ℓ` 2. sayılabilir değildir. (Buna karşılık `ℚ`
yoğun olduğundan ayrılabilir, ve uzay Lindelöf'tür — Teorem 2.4.) ∎

---

### T3 — "1. sayılabilir ⟹ ayrılabilir" yanlıştır

(ch09 T3 alıştırmasına dön)

Karşı-örnek: **sayılamaz bir kümede ayrık topoloji** (örn. `ℝ` üzerinde ayrık
topoloji, `uncountable_discrete_space()`).

**1. sayılabilir:** Her `x` için `{ {x} }` tek elemanlı bir yerel bazdır, çünkü `{x}`
açıktır ve `x`'in en küçük komşuluğudur. Sayılabilirlik (hatta sonluluk) sağlanır.

**Ayrılabilir değil:** `D ⊆ X` yoğun olsun. Her `x ∈ X` için `{x}` açık ve boş
olmadığından `D` onu kesmelidir: `x ∈ D`. Bu her `x` için geçerli olduğundan
`D = X`. Ama `X` sayılamaz olduğundan `D` de sayılamaz; sayılabilir yoğun küme
yoktur. Dolayısıyla uzay ayrılabilir değildir.

Sonuç: uzay 1. sayılabilir ama ayrılabilir değil; "1. sayılabilir ⟹ ayrılabilir"
çıkarımı yanlıştır. (Doğru implikasyon yönü 2. sayılabilirden gelir: 2. sayılabilir
⟹ ayrılabilir, T1.) ∎

---

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

---

## Bölüm 11: Altuzay ve Çarpım Topolojisi

Bu ek, Bölüm 11 alıştırmalarının tam çözümlerini içerir. Kodlama
çözümlerindeki tüm çıktılar gerçek çalıştırmadan alınmıştır; teori çözümleri tam
argüman verir.

---

### K1 — Sierpiński'nin {0} ve {1} alt uzayları

(ch11 K1 alıştırmasına dön)

```python
from pytop import finite_subspace, sierpinski_space

s = sierpinski_space()
sub0 = finite_subspace(s, [0])
sub1 = finite_subspace(s, [1])
print("{0}:", sub0.carrier, list(sub0.topology))
print("{1}:", sub1.carrier, list(sub1.topology))
```

```text
{0}: (0,) [set(), {0}]
{1}: (1,) [set(), {1}]
```

Sierpiński uzayı `({0,1}, {∅, {0}, {0,1}})`'dir. `{0}` alt uzayında açıklar
`∅∩{0}=∅` ve `{0}∩{0}={0}` ile `X∩{0}={0}` olup `{∅, {0}}`; `{1}` alt uzayında
ise `∅∩{1}=∅`, `{0}∩{1}=∅`, `X∩{1}={1}` olup `{∅, {1}}`. Tek noktalı her
uzayda tek topoloji vardır; her iki alt uzay da (kaçınılmaz olarak) ayrık =
indiscrete = trivial tek-nokta topolojisini taşır.

---

### K2 — Özel 4-noktalı uzayda {2,3} alt uzayı

(ch11 K2 alıştırmasına dön)

```python
from pytop import finite_subspace, make_topology, make_set, empty_set

X = make_topology(
    [1, 2, 3, 4],
    empty_set(),
    make_set(1, 2),
    make_set(3, 4),
    make_set(1, 2, 3, 4),
)
sub23 = finite_subspace(X, [2, 3])
print("carrier:", sub23.carrier)
print("tau_A:", sorted([sorted(list(u)) for u in sub23.topology], key=lambda x: (len(x), x)))
```

```text
carrier: (2, 3)
tau_A: [[], [2], [3], [2, 3]]
```

τ = {∅, {1,2}, {3,4}, X}'in her elemanını A = {2,3} ile keseriz:
∅∩A=∅, {1,2}∩A={2}, {3,4}∩A={3}, X∩A={2,3}. Sonuç τ_A = {∅, {2}, {3}, {2,3}}
yani A üzerinde **ayrık** topoloji. İlginç olan: X bağlantılı görünmese de
(ayrık parçalar gibi) {2,3} alt uzayı tam ayrık çıkar; alt uzay topolojisi
orijinalin "ne kadarını gördüğüne" bağlıdır.

---

### K3 — Sierpiński × Ayrık(0,1) çarpımı

(ch11 K3 alıştırmasına dön)

```python
from pytop import binary_product, sierpinski_space, discrete_topology, is_compact, is_connected

p = binary_product(sierpinski_space(), discrete_topology(0, 1))
print("compact:", is_compact(p).status)
print("connected:", is_connected(p).status)
```

```text
compact: true
connected: false
```

İki çarpan da sonlu olduğundan çarpım sonlu, dolayısıyla kompakttır.
Bağlantılılık ise korunmaz: Sierpiński bağlantılı olsa da D(0,1) ayrık ve
bağlantısızdır; çarpımda bağlantısız bir çarpan tüm çarpımı bağlantısız kılar
(çarpım bağlantılı ⟺ her iki çarpan bağlantılı).

---

### K4 — İndiscrete(1,2,3,4)'ün {1,2} alt uzayı

(ch11 K4 alıştırmasına dön)

```python
from pytop import finite_subspace, indiscrete_topology, is_connected

ind4 = indiscrete_topology(1, 2, 3, 4)
sub_ind = finite_subspace(ind4, [1, 2])
print("|tau_A|:", len(list(sub_ind.topology)))
print("connected:", is_connected(sub_ind).status)
```

```text
|tau_A|: 2
connected: true
```

İndiscrete uzayda yalnızca ∅ ve X açıktır. Bunları A = {1,2} ile kesince
∅∩A=∅ ve X∩A=A elde edilir; τ_A = {∅, {1,2}}, yani 2 açık küme. Alt uzay yine
indiscrete'tir ve indiscrete uzaylar daima bağlantılıdır. Bu sonuç Örnek 5.7
ile birebir uyumludur: indiscrete topoloji alt uzaya miras kalır.

---

### K5 — Ayrık(1,2,3)'ten alınan {1,2} alt uzayının Hausdorff kalıtımı

(ch11 K5 alıştırmasına dön)

```python
from pytop import finite_subspace, discrete_topology, separation_inherited_by_subspace

d3 = discrete_topology(1, 2, 3)
sub_d = finite_subspace(d3, [1, 2])
inh = separation_inherited_by_subspace(sub_d, "hausdorff")
print("inherited:", inh.status)
```

```text
inherited: true
```

Ayrık uzay Hausdorff'tur (her iki noktanın tekil komşulukları ayrıktır). Teorem
2.1 gereği Hausdorff'luk alt uzaya kalıtır; `separation_inherited_by_subspace`
bunu `true` olarak doğrular. Alt uzay {1,2} de ayrık olduğundan zaten
Hausdorff'tur.

---

### T1 — Dahil etme i: A → X süreklidir

(ch11 T1 alıştırmasına dön)

**İddia.** Alt uzay topolojisi τ_A = {U ∩ A : U ∈ τ} ile, dahil etme
i: A → X, i(a) = a süreklidir.

**Kanıt.** Süreklilik için her açık U ∈ τ'nun ön-görüntüsünün A'da açık olması
gerekir. Tanım gereği

    i⁻¹(U) = {a ∈ A : i(a) ∈ U} = {a ∈ A : a ∈ U} = U ∩ A.

U ∩ A, alt uzay topolojisinin tanımı gereği τ_A'nın bir elemanıdır, yani A'da
açıktır. Her açık U'nun ön-görüntüsü açık olduğundan i süreklidir. ∎

**Not.** Aslında alt uzay topolojisi, i'yi sürekli kılan **en kaba** topolojidir:
i'yi sürekli yapacak herhangi bir τ' topolojisinin her U ∩ A'yı içermesi gerekir,
dolayısıyla τ_A ⊆ τ'. Bu, alt uzay topolojisinin "initial topoloji" karakterizasyonudur.

---

### T2 — X, Y bağlantılı ⟹ X × Y bağlantılı

(ch11 T2 alıştırmasına dön)

**İddia.** X ve Y bağlantılı topolojik uzaylar ise X × Y de bağlantılıdır.

**Kanıt.** Bir y₀ ∈ Y sabitleyelim. "Yatay dilim" X × {y₀}, X'in homeomorf
kopyasıdır (π_X kısıtlaması homeomorfizmadır), dolayısıyla bağlantılıdır.
Benzer şekilde her x ∈ X için "dikey dilim" {x} × Y, Y'nin kopyası olup
bağlantılıdır.

Şimdi her x için {x} × Y dilimi, ortak nokta (x, y₀) üzerinden yatay dilim
X × {y₀} ile kesişir. Yani

    X × Y = (X × {y₀}) ∪ ⋃_{x ∈ X} ({x} × Y),

ve birleştirilen her küme bağlantılıdır ve hepsi X × {y₀} ile (dolayısıyla
ortak noktalar üzerinden birbirleriyle) kesişir. Ortak noktalı bağlantılı
kümelerin birleşimi bağlantılı olduğundan X × Y bağlantılıdır. ∎

**Sezgi.** Çarpımda herhangi iki noktayı, "önce yatay sonra dikey" hareket eden
bağlantılı bir L-yolu ile birleştirebilirsiniz; bağlantısız bir ayrışım bu
yolları kesmek zorunda kalır, ki dilimlerin bağlantılılığı buna izin vermez.

---

### T3 — Çarpımın evrensel özelliği

(ch11 T3 alıştırmasına dön)

**İddia.** f: Z → X × Y verilsin. f süreklidir ⟺ π_X∘f ve π_Y∘f süreklidir.

**Kanıt.**

(⟹) f sürekli olsun. π_X ve π_Y süreklidir (çarpım topolojisi onları sürekli
kılacak şekilde tanımlıdır). Sürekli fonksiyonların bileşkesi sürekli olduğundan
π_X∘f ve π_Y∘f süreklidir.

(⟸) g := π_X∘f ve h := π_Y∘f sürekli olsun. Çarpım topolojisinin bir bazı
{U × V : U ∈ τ_X, V ∈ τ_Y}'dir; süreklilik baz elemanları üzerinde test
edilebilir. Bir baz elemanı U × V için

    f⁻¹(U × V) = {z : f(z) ∈ U × V}
               = {z : (π_X∘f)(z) ∈ U ve (π_Y∘f)(z) ∈ V}
               = g⁻¹(U) ∩ h⁻¹(V).

g ve h sürekli olduğundan g⁻¹(U) ve h⁻¹(V) Z'de açıktır; kesişimleri de açıktır.
Her baz elemanının ön-görüntüsü açık olduğundan ve baz topolojiyi ürettiğinden,
keyfi bir açık (baz elemanlarının birleşimi) için ön-görüntü de açıktır
(ön-görüntü birleşimlerle değişmelidir). Dolayısıyla f süreklidir. ∎

**Not.** Bu özellik çarpımı bir **kategorik çarpım** yapar: X ve Y'ye giden
sürekli fonksiyon çiftleri ile X × Y'ye giden sürekli fonksiyonlar
birebir eşleşir.

---

## Bölüm 12: Bölüm Topolojisi

### K1 — finite_quotient_contract ile blok boyutları

(ch12 K1 alıştırmasına dön)

```python
from pytop import finite_quotient_contract

c = finite_quotient_contract([0, 1, 2, 3, 4], [[0, 4], [1, 3], [2]])
r = c.to_result()
print("Blok sayisi:", c.block_count)
print("Blok boyutlari:", r.metadata['block_sizes'])
```

```
Blok sayisi: 3
Blok boyutlari: [2, 2, 1]
```

`[[0,4],[1,3],[2]]` bölüntüsü 5 noktayı 3 bloğa indirir: iki ikili sınıf
(`{0,4}`, `{1,3}`) ve bir tekil sınıf (`{2}`). Bölüm uzayı 3 noktalıdır;
blok boyutları toplamı taşıyıcı boyutunu (`2+2+1=5`) verir.

---

### K2 — Trivial bölüntü Sierpiński uzayını değiştirmez

(ch12 K2 alıştırmasına dön)

```python
from pytop import sierpinski_space, finite_quotient_summary

s = sierpinski_space()
print("Trivial bolum:", finite_quotient_summary(list(s.carrier), [[0], [1]]))
```

```
Trivial bolum: quotient: status=true, carrier=2, blocks=2
```

Her noktanın kendi sınıfı olduğu (trivial) bölüntüde hiçbir yapıştırma yapılmaz:
`blocks=2 = carrier`. Bölüm haritası q burada bir bijeksiyondur ve aslında bir
homeomorfizmadır — uzay olduğu gibi kalır. Trivial denklik bağıntısı (köşegen)
her zaman bölüm uzayını orijinaline eş yapar.

---

### K3 — Aynı uzay üzerinde iki farklı bölüntü

(ch12 K3 alıştırmasına dön)

```python
from pytop import make_topology, finite_quotient_summary

X = [1, 2, 3, 4]
t = make_topology(X, set(), {1, 2}, {3, 4}, {1, 2, 3, 4})
print("Cift bloklar:", finite_quotient_summary(X, [[1, 2], [3, 4]]))
print("Tekil bloklar:", finite_quotient_summary(X, [[1], [2], [3], [4]]))
```

```
Cift bloklar: quotient: status=true, carrier=4, blocks=2
Tekil bloklar: quotient: status=true, carrier=4, blocks=4
```

`[[1,2],[3,4]]` bölüntüsü açık kümelerle (`{1,2}` ve `{3,4}`) uyumludur ve uzayı
2 noktaya indirir; her blok bir açık kümeye karşılık geldiğinden bölüm uzayı
ayrık iki noktalıdır. Tekil bölüntü ise hiçbir noktayı yapıştırmaz (`blocks=4`)
ve uzayı olduğu gibi bırakır.

---

### K4 — Daha uzun bir şeridin uçlarını yapıştırma

(ch12 K4 alıştırmasına dön)

```python
from pytop import (
    equivalence_from_partition,
    is_equivalence_relation,
    equivalence_class,
)

strip = [0, 1, 2, 3, 4, 5]
classes = [[0, 5], [1], [2], [3], [4]]
rel = equivalence_from_partition(strip, classes)
print("Denklik mi?", is_equivalence_relation(strip, rel))
print("0'in sinifi:", sorted(equivalence_class(strip, rel, 0)))
print("5'in sinifi:", sorted(equivalence_class(strip, rel, 5)))
print("Ayni mi?", equivalence_class(strip, rel, 0) == equivalence_class(strip, rel, 5))
```

```
Denklik mi? True
0'in sinifi: [0, 5]
5'in sinifi: [0, 5]
Ayni mi? True
```

`equivalence_from_partition`, bölüntüyü yansımalı + simetrik + geçişli bir
bağıntıya genişletir; bu yüzden `is_equivalence_relation` `True` döner. 0 ve 5
aynı sınıfta (`[0, 5]`) olduğundan `equivalence_class(0)` ile
`equivalence_class(5)` çıktıları birebir aynıdır — uçlar yapıştırıldı.
Örnek 5.5'teki 5 noktalı çemberin bir nokta uzatılmış halidir: 6 noktalı şerit,
5 noktalı çembere iner.

---

### K5 — Kanonik izdüşüm ve doymuşluk kontrolü

(ch12 K5 alıştırmasına dön)

```python
from pytop import (
    equivalence_from_partition,
    canonical_projection_from_equivalence,
    equivalence_class,
)

car = ['x', 'y', 'z']
prt = [['x', 'y'], ['z']]
rl = equivalence_from_partition(car, prt)

proj = canonical_projection_from_equivalence(car, rl)
for pt in car:
    print(f"q({pt}) =", sorted(proj[pt]))

print("{x,y} doymus mu?", all(equivalence_class(car, rl, p) <= {'x', 'y'} for p in {'x', 'y'}))
print("{x} doymus mu?", equivalence_class(car, rl, 'x') <= {'x'})
```

```
q(x) = ['x', 'y']
q(y) = ['x', 'y']
q(z) = ['z']
{x,y} doymus mu? True
{x} doymus mu? False
```

q, x ve y'yi aynı sınıfa (`{x,y}`) gönderir; z kendi sınıfında kalır.
`{x,y}` doymuştur çünkü içerdiği her noktanın sınıfı tamamen kendisidir.
`{x}` doymuş değildir: x'i içerir ama x'in sınıf arkadaşı y'yi içermez, yani
`{x} ≠ q⁻¹(q({x})) = {x,y}`. Bölüm topolojisinde yalnızca doymuş açık kümeler
gerçek açık kümelere iner.

---

### T1 — Bölüm haritası her zaman süreklidir

(ch12 T1 alıştırmasına dön)

Süreklilik tanımı: q: X → X/~ sürekli ⟺ her açık U ⊆ X/~ için q⁻¹(U) ⊆ X
açıktır. Bölüm topolojisinin tanımı tam olarak şudur:

    U, X/~ içinde açık  ⟺  q⁻¹(U) ∈ τ.

Yani U'nun açık olması, *tanım gereği* q⁻¹(U)'nun X'te açık olmasıyla aynı
şeydir. Dolayısıyla her açık U için q⁻¹(U) açıktır ve q süreklidir. Bu, bölüm
topolojisinin q'yu sürekli kılan **en ince** topoloji olarak seçilmesinin
doğrudan sonucudur: daha fazla açık küme eklersek (daha ince yaparsak) bazı
q⁻¹(U) artık açık olmayabilir ve süreklilik bozulurdu. ∎

---

### T2 — Bağlantılılığın korunumu

(ch12 T2 alıştırmasına dön)

X bağlantılı olsun; X/~'nin bağlantılı olduğunu gösterelim. Aksini varsayalım:
X/~ = A ∪ B, burada A, B boş olmayan, ayrık, açık kümeler olsun (bağlantısızlık
tanımı). q sürekli olduğundan (T1) q⁻¹(A) ve q⁻¹(B) X'te açıktır. Bu iki
ön-görüntü ayrıktır (A ∩ B = ∅ olduğundan) ve birleşimleri q⁻¹(A ∪ B) =
q⁻¹(X/~) = X'tir. Ayrıca q örten olduğundan ve A, B boş olmadığından q⁻¹(A) ve
q⁻¹(B) de boş değildir. O hâlde X = q⁻¹(A) ∪ q⁻¹(B), X'i boş olmayan iki ayrık
açık kümeye böler — X bağlantısız olurdu. Bu, X bağlantılı varsayımıyla çelişir.
Dolayısıyla X/~ bağlantılıdır. (Daha kısaca: X/~ = q(X) ve bağlantılı bir kümenin
sürekli görüntüsü bağlantılıdır.) ∎

---

### T3 — Evrensel özellik

(ch12 T3 alıştırmasına dön)

g: X/~ → Z için "g sürekli ⟺ g ∘ q sürekli" eşdeğerliğini gösterelim.

(⟹) g sürekli ve q sürekli (T1) olduğundan, iki sürekli haritanın bileşkesi
g ∘ q süreklidir.

(⟸) g ∘ q'nun sürekli olduğunu varsayalım. Z'de bir açık V kümesi alın. g'nin
sürekliliği için g⁻¹(V)'nin X/~ bölüm topolojisinde açık olduğunu göstermeliyiz.
Bölüm topolojisinin tanımı gereği bu, q⁻¹(g⁻¹(V))'nin X'te açık olmasına denktir.
Anahtar gözlem, ön-görüntülerin birleşmesidir:

    q⁻¹(g⁻¹(V)) = (g ∘ q)⁻¹(V).

g ∘ q sürekli olduğundan sağ taraf X'te açıktır; o hâlde sol taraf da açıktır ve
böylece g⁻¹(V), X/~'de açıktır. V keyfi olduğundan g süreklidir. ∎

Bu özellik bölüm topolojisini bir **evrensel nesne** olarak karakterize eder:
X/~'den çıkan sürekli haritaları kontrol etmek, çok daha somut olan X üzerindeki
haritaları kontrol etmeye indirgenir.

---

### T4 — Doymuş kümeler ve açıklığın inişi

(ch12 T4 alıştırmasına dön)

A ⊆ X doymuş olsun, yani A = q⁻¹(q(A)). q(A)'nın bölüm uzayında açık olmasının
A'nın X'te açık olmasına denk olduğunu gösterelim.

Bölüm topolojisinin tanımı gereği q(A), X/~'de açıktır ⟺ q⁻¹(q(A)), X'te açıktır.
A doymuş olduğundan q⁻¹(q(A)) = A, dolayısıyla:

    q(A), X/~ içinde açık  ⟺  A, X içinde açık.

Bu, "doymuş açık kümeler ↔ bölüm uzayının açık kümeleri" yazışmasıdır: kanonik
izdüşüm doymuş açık kümeleri açık kümelere bire bir taşır.

**Doymamış A için neden bozulur?** A doymuş değilse q⁻¹(q(A)), A'dan kesin
büyüktür (A'ya, A içindeki noktaların eksik kalan sınıf arkadaşları eklenir).
Bu durumda q(A)'nın açıklığı artık A'nın açıklığına değil, daha büyük doymuş
zarf q⁻¹(q(A))'nın açıklığına bağlıdır. Örnek 5.6'daki `{a}` kümesi tipik
örnektir: `{a}` ayrık uzayda açıktır, ama doymuş zarfı `{a,b}`'dir; `q({a})`'nın
bölümde açık olup olmadığı `{a}`'ya değil `{a,b}`'ye bakılarak belirlenir. Bu
yüzden açıklık ifadesi yalnızca doymuş kümeler için temiz biçimde iner. ∎

---

## Bölüm 13: Başlangıç ve Son Topoloji

Bu dosya, Bölüm 13'ün (Başlangıç ve Son Topoloji) hem mevcut hem de yeni eklenen
alıştırmalarının çözümlerini içerir. Tüm kod blokları paylaşılan bir ad alanında
(namespace) sırayla çalışır: ilk blok daha sonra kullanılan tüm isimleri içe aktarır.

---

### A1 — initial_topology_from_maps vs. finite_subspace

(ch13 1. alıştırmasına dön)

`f: {a,b,c,d} → discrete({0,1})`, $f(a)=f(b)=0$, $f(c)=f(d)=1$ haritasının başlangıç
topolojisi, $f$'nin lif yapısını alt-baz yapar.

```python
from pytop.finite_map_analysis import FiniteMap
from pytop import (
    initial_topology_from_maps,
    discrete_topology,
    make_topology,
    is_continuous_finite_map,
)

carrier = ["a", "b", "c", "d"]
X_ph    = make_topology(carrier, set(), set(carrier))
Yd      = discrete_topology(0, 1)
f1 = FiniteMap(domain=X_ph, codomain=Yd, name="f",
               mapping={"a": 0, "b": 0, "c": 1, "d": 1})

tau = initial_topology_from_maps(carrier, [f1])
print("A1 tau_ini:", sorted([sorted(map(str, u)) for u in tau.topology],
                            key=lambda x: (len(x), x)))
print("A1 eleman sayisi:", len(tau.topology))
```

```text
A1 tau_ini: [[], ['a', 'b'], ['c', 'd'], ['a', 'b', 'c', 'd']]
A1 eleman sayisi: 4
```

Alt-baz $\{f^{-1}(\{0\}), f^{-1}(\{1\})\} = \{\{a,b\},\{c,d\}\}$; ürettiği topoloji
4 elemanlı. Bu, $X$'i iki lif $\{a,b\}$ ve $\{c,d\}$ üzerinde "iki noktalı discrete"
gibi görür — `finite_subspace` ile değil, lif bölmesiyle elde edilen kaba topolojidir.

---

### A2 — Tek projeksiyon başlangıç topolojisi

(ch13 2. alıştırmasına dön)

Yalnızca $\pi_x$ kullanılırsa, $y$-ekseni bilgisi kaybolur; topoloji discrete'den
kabadır.

```python
from pytop import binary_product

d2   = discrete_topology(0, 1)
prod = binary_product(d2, d2)
pi_x = FiniteMap(domain=prod, codomain=d2, name="pi_x",
                 mapping={(0,0):0, (0,1):0, (1,0):1, (1,1):1})

init_x = initial_topology_from_maps(list(prod.carrier), [pi_x])
print("A2 sadece pi_x eleman sayisi:", len(init_x.topology))
print("A2 tau:", sorted([sorted(map(str, u)) for u in init_x.topology],
                       key=lambda x: (len(x), x)))
```

```text
A2 sadece pi_x eleman sayisi: 4
A2 tau: [[], ['(0, 0)', '(0, 1)'], ['(1, 0)', '(1, 1)'], ['(0, 0)', '(0, 1)', '(1, 0)', '(1, 1)']]
```

Evet, discrete'den (16 açık küme) **daha kabadır** — yalnızca 4 açık küme. $\pi_x$
tek başına $x$-koordinatına göre iki şeride ayırır; tek noktaları ayıramaz. İkinci
projeksiyon $\pi_y$ eklenince kesişimler tüm tektonları üretir ve discrete'e ulaşılır
(Bölüm 6 örneği).

---

### A3 — Manuel son topoloji

(ch13 3. alıştırmasına dön)

$X=\{0,1,2,3,4\}$ discrete, $g: X \to \{0,1,2\}$, $g=\{0,1\mapsto0,\ 2,3\mapsto1,\ 4\mapsto2\}$.

```python
Xc     = [0, 1, 2, 3, 4]
sigmaD = discrete_topology(*Xc)
g3     = {0: 0, 1: 0, 2: 1, 3: 1, 4: 2}
Yc     = [0, 1, 2]
tauD   = {frozenset(u) for u in sigmaD.topology}

open_Y = []
for mask in range(1 << len(Yc)):
    V   = frozenset(Yc[i] for i in range(len(Yc)) if mask & (1 << i))
    pre = frozenset(x for x in sigmaD.carrier if g3[x] in V)
    if pre in tauD:
        open_Y.append(set(V))

final_Y = make_topology(Yc, *open_Y)
print("A3 (sigma=discrete) son topoloji eleman sayisi:", len(final_Y.topology))
```

```text
A3 (sigma=discrete) son topoloji eleman sayisi: 8
```

$\sigma_X$ discrete olduğundan **her** ön-görüntü açıktır; dolayısıyla $Y$'nin her alt
kümesi açık olur ve son topoloji $Y$ üzerinde discrete'dir ($2^3 = 8$ açık küme).
$\sigma_X$ inceltildikçe (daha az açık küme) son topoloji de kabalaşır: en-ince koşulu
kaynak topolojisinin inceliğine doğrudan bağlıdır.

---

### A4 — (Teori) Başlangıç topolojisinin evrensel özelliği

(ch13 4. alıştırmasına dön)

**İddia.** $h: Z \to (X, \tau_{\mathrm{ini}})$ sürekli $\iff$ her $f_\alpha \circ h$
sürekli.

**İspat.** ($\Rightarrow$) $h$ sürekli ve her $f_\alpha$ (tanımı gereği) sürekli ise,
sürekli haritaların bileşkesi sürekli olduğundan $f_\alpha \circ h$ süreklidir.

($\Leftarrow$) Her $f_\alpha \circ h$ sürekli olsun. $\tau_{\mathrm{ini}}$ alt-bazı
$\mathcal{S} = \{f_\alpha^{-1}(U) \mid U \in \tau_\alpha\}$ olduğundan, sürekliliği
yalnızca alt-baz elemanlarının ön-görüntülerinde denetlemek yeterlidir. Bir alt-baz
elemanı için

$$h^{-1}\big(f_\alpha^{-1}(U)\big) = (f_\alpha \circ h)^{-1}(U),$$

ve sağ taraf $f_\alpha \circ h$ sürekli olduğundan $Z$'de açıktır. Tüm alt-baz
elemanlarının ön-görüntüleri açık olunca tüm açık kümelerin (birleşim ve sonlu
kesişim) ön-görüntüleri de açıktır; demek ki $h$ süreklidir. $\square$

---

### A5 — (Teori) Son topolojinin en-incelik karakteri

(ch13 5. alıştırmasına dön)

**İddia.** $\tau_{\mathrm{fin}}$'den daha ince hiçbir topoloji her $g_i$'yi sürekli
kılamaz.

**İspat.** $\tau_{\mathrm{fin}} = \{V \subseteq Y \mid g_i^{-1}(V) \in \sigma_i\ \forall i\}$
tanımı, $g_i$'yi sürekli kılan açık kümelerin **tam** koleksiyonudur: bir $V$ açık
sayılmak için her $i$'de $g_i^{-1}(V)$ açık olmalıdır. Şimdi $\tau' \supsetneq
\tau_{\mathrm{fin}}$ olsun, yani $\tau'$ içinde $V_0 \in \tau' \setminus \tau_{\mathrm{fin}}$
bir açık küme bulunsun. $V_0 \notin \tau_{\mathrm{fin}}$ olduğundan en az bir $i$ için
$g_i^{-1}(V_0) \notin \sigma_i$. O hâlde $g_i: (X_i,\sigma_i) \to (Y,\tau')$ bu açık
$V_0$ için ön-görüntü açık olmadığından **sürekli değildir**. Demek ki
$\tau_{\mathrm{fin}}$'den kesin daha ince hiçbir topoloji tüm $g_i$'leri sürekli
tutamaz; $\tau_{\mathrm{fin}}$ en incedir. $\square$

---

### A6 — (Yeni) "En kaba" iddiasının süreklilik yüklemiyle doğrulanması

(ch13 6. alıştırmasına dön)

```python
def powerset_opens(elems):
    elems = list(elems)
    out = []
    for mask in range(1 << len(elems)):
        out.append({elems[i] for i in range(len(elems)) if mask & (1 << i)})
    return out

Xc6  = [0, 1, 2, 3]
Xph6 = make_topology(Xc6, set(), set(Xc6))
Yd6  = discrete_topology(0, 1)
f6   = FiniteMap(domain=Xph6, codomain=Yd6, name="f",
                 mapping={0: 0, 1: 0, 2: 1, 3: 1})

tau6   = initial_topology_from_maps(Xc6, [f6])
ini6   = [set(u) for u in tau6.topology]
codom6 = [set(u) for u in Yd6.topology]
indis6 = [set(), set(Xc6)]            # indiscrete: tau_ini'den daha kaba
disc6  = powerset_opens(Xc6)          # discrete: tau_ini'den daha ince

print("A6 f, tau_ini surekli   :",
      is_continuous_finite_map(Xc6, ini6,   list(Yd6.carrier), codom6, f6.mapping))
print("A6 f, indiscrete surekli:",
      is_continuous_finite_map(Xc6, indis6, list(Yd6.carrier), codom6, f6.mapping))
print("A6 f, discrete surekli  :",
      is_continuous_finite_map(Xc6, disc6,  list(Yd6.carrier), codom6, f6.mapping))
```

```text
A6 f, tau_ini surekli   : True
A6 f, indiscrete surekli: False
A6 f, discrete surekli  : True
```

$f$ hem $\tau_{\mathrm{ini}}$ hem discrete ile süreklidir, ama indiscrete ile değildir.
Bu üç sonuç birlikte "en kaba" iddiasını kanıtlar: $\tau_{\mathrm{ini}}$, $f$'yi sürekli
kılan topolojiler arasında en azını içerir; daha kabası (indiscrete) sürekliliği bozar,
daha incesi (discrete) gereksiz açık küme barındırır.

---

### A7 — (Yeni) Evrensel özelliğin doğrulanması

(ch13 7. alıştırmasına dön)

```python
Xc7  = ["a", "b"]
Xph7 = make_topology(Xc7, set(), set(Xc7))
Yd7  = discrete_topology(0, 1)
f7   = FiniteMap(domain=Xph7, codomain=Yd7, name="f", mapping={"a": 0, "b": 1})
g7   = FiniteMap(domain=Xph7, codomain=Yd7, name="g", mapping={"a": 1, "b": 0})

tau7 = initial_topology_from_maps(Xc7, [f7, g7])
Xop  = [set(u) for u in tau7.topology]
Yop  = [set(u) for u in Yd7.topology]

Zc, Zop = ["p", "q"], [set(), {"p"}, {"q"}, {"p", "q"}]
h  = {"p": "a", "q": "b"}
fh = {z: f7.mapping[h[z]] for z in Zc}     # f . h
gh = {z: g7.mapping[h[z]] for z in Zc}     # g . h

c_fh = is_continuous_finite_map(Zc, Zop, list(Yd7.carrier), Yop, fh)
c_gh = is_continuous_finite_map(Zc, Zop, list(Yd7.carrier), Yop, gh)
c_h  = is_continuous_finite_map(Zc, Zop, Xc7, Xop, h)

print("A7 tau_ini eleman:", len(tau7.topology))
print("A7 fh:", c_fh, "gh:", c_gh, "h:", c_h, "| denk:", c_h == (c_fh and c_gh))
```

```text
A7 tau_ini eleman: 4
A7 fh: True gh: True h: True | denk: True
```

$f$ ve $g$ birlikte $X$ üzerinde discrete topolojiyi (4 açık küme) üretir. $h$
süreklidir ancak ve ancak hem $f\circ h$ hem $g\circ h$ sürekli olduğunda; yüklem bu
denkliği `c_h == (c_fh and c_gh)` ile teyit eder. Bu, Teorem 4'ün (evrensel özellik)
somut, çalıştırılabilir bir tanığıdır.

---

## Bölüm 14: Metrik Uzaylar

### K1 — {A,B,C,D} üzerinde metrik + üçgen ihlali

(ch14 K1 alıştırmasına dön)

Önce geçerli bir metrik (ayrık metrik), sonra üçgen eşitsizliğini ihlal eden bir
mesafe fonksiyonu kuralım.

```python
from pytop.metric_spaces import FiniteMetricSpace, validate_metric

pts = ['A', 'B', 'C', 'D']
good = {(a, b): (0 if a == b else 1) for a in pts for b in pts}
fms_good = FiniteMetricSpace(carrier=tuple(pts), distance=good)
print("ayrik metrik?", validate_metric(fms_good).status)

# uggen esitsizligini bozalim: d(A,C)=5 > d(A,B)+d(B,C)=2
bad = dict(good)
bad[('A', 'C')] = 5
bad[('C', 'A')] = 5
fms_bad = FiniteMetricSpace(carrier=tuple(pts), distance=bad)
r = validate_metric(fms_bad)
print("bozuk metrik?", r.status)
print("neden:", r.justification[0] if r.justification else "")
```

```
ayrik metrik? true
bozuk metrik? false
neden: The triangle inequality failed.
```

Ayrık metrik üç aksiyomu da sağlar. d(A,C)=5 koyduğumuzda ise A→B→C dolaylı yolu
(toplam 2) doğrudan yoldan (5) kısa olur; bu, M3'ün doğrudan ihlalidir.
`validate_metric` bunu yakalayıp `false` döner.

### K2 — Öklid metrikli {0,…,9} üzerinde yuvarlar

(ch14 K2 alıştırmasına dön)

```python
from pytop.metric_spaces import FiniteMetricSpace
from pytop import open_ball, closed_ball

ints = tuple(range(10))
dist = {(a, b): abs(a - b) for a in ints for b in ints}
fms = FiniteMetricSpace(carrier=ints, distance=dist)

print("B(5, 3.0)      =", sorted(open_ball(fms, 5, 3.0)))
print("Bclosed(5, 3.0)=", sorted(closed_ball(fms, 5, 3.0)))
```

```
B(5, 3.0)      = [3, 4, 5, 6, 7]
Bclosed(5, 3.0)= [2, 3, 4, 5, 6, 7, 8]
```

Açık yuvar `d(5,y) < 3` ister: mesafe 0,1,2 olanlar, yani {3,4,5,6,7}. Kapalı yuvar
`d(5,y) ≤ 3` ister: mesafe 3 olan 2 ve 8 noktaları da eklenir. Aradaki tek fark, açık
yuvarın **sınırdaki** (tam mesafe r) noktaları dışlaması, kapalı yuvarın içermesidir.

### K3 — normalized_metric ile [0,1]'e normalleştirme

(ch14 K3 alıştırmasına dön)

`normalized_metric` her metriği `d/(1+d)` dönüşümüyle [0,1)'e taşır; topolojiyi
korur (Teorem 2.2 ile aynı fikir).

```python
from pytop.metric_spaces import FiniteMetricSpace
from pytop import normalized_metric

ints = tuple(range(10))
dist = {(a, b): abs(a - b) for a in ints for b in ints}
fms = FiniteMetricSpace(carrier=ints, distance=dist)

nm = normalized_metric(fms.distance)
print("d(0,9)        =", fms.distance[(0, 9)])
print("normalized(0,9)=", round(nm(0, 9), 4))
print("normalized(5,8)=", round(nm(5, 8), 4))
```

```
d(0,9)        = 9
normalized(0,9)= 0.9
normalized(5,8)= 0.75
```

Sınırsız mesafe 9, normalleştirme sonrası 9/(1+9) = 0.9 olur; mesafe 3 ise
3/(1+3) = 0.75. Tüm değerler [0,1) aralığına çekilir ama hiçbir nokta çiftinin
"yakınlık sırası" değişmez, dolayısıyla aynı topoloji korunur.

### K4 — Karşı-örneği koda dökmek (üçgen ihlali)

(ch14 K4 alıştırmasına dön)

§1.0'daki karşı-örnek tam olarak K1'in ikinci kısmıdır. Ayrık metriği taban alıp
yalnız d(A,C)=5 yaparız:

```python
from pytop.metric_spaces import FiniteMetricSpace, validate_metric

pts = ['A', 'B', 'C', 'D']
dist = {(a, b): (0 if a == b else 1) for a in pts for b in pts}
dist[('A', 'C')] = 5
dist[('C', 'A')] = 5

fms = FiniteMetricSpace(carrier=tuple(pts), distance=dist)
r = validate_metric(fms)
print("status:", r.status)
print("justification:", r.justification[0] if r.justification else "")
```

```
status: false
justification: The triangle inequality failed.
```

`justification` alanı tam olarak hangi aksiyomun bozulduğunu söyler: üçgen
eşitsizliği. Simetri (M2) ve özdeşlik (M1) korunduğu için tek arıza M3'tür. Bu, bir
"mesafe fonksiyonunun" otomatik olarak metrik olmadığını — üç aksiyomun da gerekli
olduğunu — somut biçimde gösterir.

### K5 — Dolu 3×3 ızgara: kalıcı delik yok (TDA köprüsü)

(ch14 K5 alıştırmasına dön)

```python
import math
import pytop
from pytop.metric_spaces import FiniteMetricSpace

grid = [(i, j) for i in range(3) for j in range(3)]   # dolu 3x3 = 9 nokta
carrier = tuple(range(len(grid)))
dist = {(a, b): math.dist(grid[a], grid[b]) for a in carrier for b in carrier}
square = FiniteMetricSpace(carrier=carrier, distance=dist)

pairs = pytop.persistent_homology(square, max_dimension=2, max_scale=2.5)
loops = [p for p in pairs if p.dimension == 1]
print("H1 dongu sayisi:", len(loops))
print("en uzun kalicilik:", round(max(p.persistence for p in loops), 4))
```

```
H1 dongu sayisi: 4
en uzun kalicilik: 0.4142
```

Dört döngü çıkar, ama hepsi **kısa ömürlüdür**: her biri 1.0'da doğup 1.4142'de
ölür (kalıcılık ≈ 0.414). Bunlar gerçek topolojik delikler değil, ızgaranın dört
birim karesinin köşegenleri henüz bağlanmadan önceki anlık boşluklarıdır; köşegen
mesafesi √2 ≈ 1.414'e gelince üçgenlerle dolup yok olurlar.

Örnek 5.8'deki çemberin tek döngüsü kalıcılık ≈ 1.08 ile **uzun ömürlüydü** — bu
gerçek bir deliğin imzası. Dolu kare ise her yeri doludur; "uzun çubuk yok" demek
"kalıcı delik yok" demektir. TDA'nın temel ilkesi budur: kısa çubuklar gürültü,
uzun çubuklar gerçek topolojik özelliktir.

### T1 — Her metrik uzay Hausdorff'tur

(ch14 T1 alıştırmasına dön)

**İddia.** (M, d) metrik uzay, x ≠ y ⟹ x ve y ayrık açık komşuluklarla ayrılır.

**İspat.** x ≠ y olduğundan, (M1) gereği r := d(x,y) > 0'dır. Yarıçapı r/2 olan iki
açık yuvar alalım: U = B(x, r/2) ve V = B(y, r/2). Bunların ayrık olduğunu
gösterelim. Aksini varsayalım: bir z ∈ U ∩ V olsun. O hâlde d(x,z) < r/2 ve
d(y,z) < r/2. Üçgen eşitsizliğinden (M3):

    r = d(x,y) ≤ d(x,z) + d(z,y) < r/2 + r/2 = r,

yani r < r — çelişki. Demek ki U ∩ V = ∅. U ve V açık (açık yuvarlar açıktır),
x ∈ U, y ∈ V, ayrıklar ⟹ uzay Hausdorff'tur (T2). ∎

### T2 — d' = min(d,1) ile d aynı topolojiyi indükler

(ch14 T2 alıştırmasına dön)

**İddia.** τ_d = τ_{d'}, burada d'(x,y) = min(d(x,y), 1).

**İspat.** İki topolojinin eşit olması için, her birinin açık yuvarlarının ötekinin
açık kümeleri olması yeterlidir (yuvarlar bir baz oluşturur). Anahtar gözlem: yarıçap
r ≤ 1 için

    B_{d'}(x, r) = {y : min(d(x,y),1) < r} = {y : d(x,y) < r} = B_d(x, r),

çünkü r ≤ 1 iken `min(d,1) < r` ile `d < r` aynı koşuldur (d ≥ 1 olan noktalar her
iki tanımda da dışarıda kalır). Yani küçük yarıçaplı yuvarlar tam olarak çakışır.

Şimdi U ∈ τ_d olsun ve x ∈ U. Tanım gereği bir ε > 0 ile B_d(x, ε) ⊆ U. ε' :=
min(ε, 1) ≤ 1 alırsak B_{d'}(x, ε') = B_d(x, ε') ⊆ B_d(x, ε) ⊆ U; demek ki U,
d'-açıktır. Simetrik argümanla her d'-açık küme d-açıktır. Dolayısıyla τ_d = τ_{d'}.

Bu, sınırsız bir metriği (değerleri [0,1]'e sıkıştırarak) sınırlı bir metriğe
çevirmenin topolojiyi hiç değiştirmediğini gösterir — `capped_metric`/
`normalized_metric` fonksiyonlarının arkasındaki teorem. ∎

### T3 — Üçgen eşitsizliği Hausdorff ispatında nerede?

(ch14 T3 alıştırmasına dön)

T1'in ispatında üçgen eşitsizliği **tam olarak tek bir yerde** kullanılır: B(x, r/2)
ile B(y, r/2)'nin ayrık olduğunu gösteren adımda. Ortak bir z noktası olduğunu
varsaydığımızda elimizde d(x,z) < r/2 ve d(z,y) < r/2 vardır; bu iki *yerel* bilgiden
*küresel* bir bilgiye — d(x,y)'ye — geçmenin tek yolu M3'tür:

    d(x,y) ≤ d(x,z) + d(z,y).

M3 olmasaydı, x ve y'ye ayrı ayrı yakın bir z'nin bulunması d(x,y)'nin küçük olmasını
gerektirmezdi; küçük yuvarlar kesişebilir ve ayırma başarısız olurdu. Özdeşlik (M1),
r = d(x,y) > 0 olmasını garanti etmek için ispatın *başında* kullanılır; simetri (M2)
ise d(z,y) = d(y,z) yazımında örtük olarak girer. Ama ayrıklığın gerçek motoru
M3'tür — Hausdorff ayrımı doğrudan üçgen eşitsizliğinin bir sonucudur.

---

## Bölüm 15: Metrik Tamlık

### K1 — Rasyoneller ℚ tam mı?

(ch15 K1 alıştırmasına dön)

```python
from pytop import rationals_metric
from pytop.metric_completeness import is_complete

qm = rationals_metric()
print("status:", is_complete(qm).status)
print("not_complete tag:", 'not_complete' in qm.tags)
```

```
status: unknown
not_complete tag: True
```

`rationals_metric()` sembolik (sonsuz) bir uzaydır. `is_complete` yalnızca
**açık sonlu** metrik uzaylarda exact karar verir; ℚ için sonucu dürüstçe
`unknown` bırakır. Ama küratörlü `tags` kümesi √2'ye yakınsayan Cauchy
dizisinin limit bulamamasını `'not_complete'` etiketiyle kayıt altına alır.

---

### K2 — 4-noktalı metrik uzay + metric_compactness_check

(ch15 K2 alıştırmasına dön)

```python
from pytop.metric_spaces import FiniteMetricSpace
from pytop.metric_completeness import metric_compactness_check

pts = ('p', 'q', 'r', 's')
dist = {(a, b): (0 if a == b else 1) for a in pts for b in pts}
fms = FiniteMetricSpace(carrier=pts, distance=dist)

mc = metric_compactness_check(fms)
print("compact:", mc.status, mc.value)
```

```
compact: true True
```

Ayrık (discrete) 4-noktalı metrik: her Cauchy dizisi eninde sonunda sabit
olduğundan **tam**, taşıyıcının kendisi her ε için ε-net olduğundan **tamamen
sınırlı**. İkisi birden ⟹ kompakt.

---

### K3 — analyze_metric_completeness value sözlüğü

(ch15 K3 alıştırmasına dön)

```python
from pytop.metric_spaces import FiniteMetricSpace
from pytop.metric_completeness import analyze_metric_completeness

pts = ('p', 'q', 'r', 's')
dist = {(a, b): (0 if a == b else 1) for a in pts for b in pts}
fms = FiniteMetricSpace(carrier=pts, distance=dist)

r = analyze_metric_completeness(fms)
print("value:", r.value)
```

```
value: {'is_complete': True, 'is_totally_bounded': True, 'metric_compact': True}
```

`analyze_metric_completeness` üç bağımsız kararı tek sözlükte toplar:
tamlık, tamamen sınırlılık ve bunların kesişimi olan metrik kompaktlık. Sonlu
uzayda her üçü de `True`.

---

### K4 — Statü unknown, etiket True neden?

(ch15 K4 alıştırmasına dön)

```python
from pytop import rationals_metric
from pytop.metric_completeness import is_complete

qm = rationals_metric()
print("status:", is_complete(qm).status)
print("not_complete tag:", 'not_complete' in qm.tags)
```

```
status: unknown
not_complete tag: True
```

İki sonuç çelişmez; iki ayrı bilgi katmanıdır. **Statü** kütüphanenin *kanıtla
karar verebildiği* şeydir: sembolik ℚ'da açık kümeleri tarayarak tamlık ispatı
mümkün olmadığından `unknown`. **Etiket** ise küratörlü bir gerçektir: ℚ'nun
tam olmadığı matematiksel olarak bilinir ve `'not_complete'` olarak işaretlenir.
Kütüphane "bilmiyorum" derken yalan söylemez; biliniyor olan gerçeği ayrı bir
kanalda taşır.

---

### K5 — Kararlı (stable) profilin key alanı

(ch15 K5 alıştırmasına dön)

```python
from pytop import get_fixed_point_profiles

stable = [p.key for p in get_fixed_point_profiles() if p.stability == 'stable']
print("stable keys:", stable)
```

```
stable keys: ['attracting_fixed_point']
```

Tek kararlı profil `attracting_fixed_point`'tir ve doğrudan **Banach büzülme
teoremine** karşılık gelir: büzülme bir komşulukta tüm yörüngeleri sabit
noktaya çeker (`fⁿ(x) → x₀`), yani sabit nokta çekicidir.

---

### T1 — Banach sabit-nokta teoremi (sözlü)

(ch15 T1 alıştırmasına dön)

Tam bir (M, d) uzayında, mesafeleri sabit bir K < 1 oranıyla küçülten her
T: M → M dönüşümünün **tek** bir sabit noktası vardır. Sezgi: T her uygulamada
her şeyi en az K kat birbirine yaklaştırır; bu yüzden herhangi bir x_0'dan
başlayan x_{n+1} = T(x_n) yörüngesi giderek sıkışır (Cauchy olur) ve tamlık
sayesinde tek bir noktaya çöker.

**Uygulama:** Picard–Lindelöf teoremi. y' = f(t, y), y(t_0) = y_0 başlangıç-değer
probleminin çözümü, integral operatörü
(Ty)(t) = y_0 + ∫_{t_0}^{t} f(s, y(s)) ds biçiminde bir büzülme olarak yazılır;
yeterince küçük aralıkta K < 1 olur ve Banach teoremi çözümün varlığını ve
tekliğini garanti eder.

---

### T2 — [0,1] tam, (0,1) tam değil

(ch15 T2 alıştırmasına dön)

**[0,1] tamdır.** ℝ tam bir metrik uzaydır ve [0,1] ⊆ ℝ **kapalıdır**. "Tam
uzayın kapalı alt-uzayı tamdır" teoremi gereği [0,1] tamdır: [0,1] içindeki her
Cauchy dizisi ℝ'de bir limite yakınsar, limit kapalılık nedeniyle [0,1]'de kalır.

**(0,1) tam değildir.** x_n = 1/(n+1) dizisini düşünün: tüm terimler (0,1) içinde
ve dizi Cauchy'dir (`d(x_m, x_n) → 0`). Limiti 0'dır, fakat 0 ∉ (0,1). Dolayısıyla
(0,1) içinde yakınsamayan bir Cauchy dizisi vardır: (0,1) tam değildir. Aynı dizi,
biri tam diğeri değil olduğundan, tamlığın **topolojik** değil **metrik** bir
özellik olduğunu gösterir — (0,1) ile ℝ homeomorftur.

---

### T3 — Tam uzayın kapalı alt-uzayı tamdır

(ch15 T3 alıştırmasına dön)

**İspat.** (M, d) tam, A ⊆ M kapalı olsun. {a_n} ⊆ A herhangi bir Cauchy dizisi
olsun. {a_n} M içinde de Cauchy'dir; M tam olduğundan bir a ∈ M limitine
yakınsar. A kapalı olduğundan kendi limit noktalarını içerir, dolayısıyla a ∈ A.
Böylece A içindeki her Cauchy dizisi A içinde bir limite yakınsar: A tamdır. ∎

**Açık alt-uzay için karşı-örnek.** ℝ tamdır; (0,1) ⊆ ℝ **açıktır** ama tam
değildir (bkz. T2: 1/(n+1) dizisi). Demek ki "açık alt-uzay" için benzer bir
teorem **yoktur**; tamlığı miras aldıran şey kapalılıktır, açıklık değil.

---

### T4 — ℚ tam değil + tamlama

(ch15 T4 alıştırmasına dön)

**Cauchy ama limitsiz.** x_1 = 1, x_2 = 1.4, x_3 = 1.41, x_4 = 1.414, ... dizisi
√2'nin ondalık açılımıdır. Her x_n rasyoneldir. m < n için
`|x_m − x_n| < 10^{−(m−1)}` olduğundan dizi Cauchy'dir. ℝ'de limit √2'dir; ama
√2 irrasyoneldir, yani √2 ∉ ℚ. Demek ki bu Cauchy dizisinin ℚ içinde **limiti
yoktur**: ℚ tam değildir.

**Tamlama.** Tamlama inşası, ℚ'daki Cauchy dizilerini denklik sınıflarına ayırıp
(iki dizi "aynı limite gidiyorsa" denk) bu sınıfları yeni noktalar olarak ekler.
Yukarıdaki dizinin sınıfı tam olarak √2 noktasını verir. Tüm bu boşlukları
doldurunca elde edilen tam uzay ℝ = ℚ̂'dir: ℚ, ℝ'de yoğundur ve ℝ'de her Cauchy
dizisi yakınsar.

---

## Bölüm 16: Metrik Dönüşümler

Bu ek, Bölüm 16 (Metrik Fonksiyonlar ve Sözleşmeler) alıştırmalarının tam
çözümlerini içerir. Kodlama çözümlerindeki tüm çıktılar gerçek çalıştırmadan
alınmıştır; teori çözümleri tam argüman verir.

---

### K1 — Ayrık metrikte döngü permütasyonu

(ch16 K1 alıştırmasına dön)

```python
from pytop.metric_spaces import FiniteMetricSpace
from pytop.metric_map_taxonomy import classify_finite_metric_map

pts = [1, 2, 3]
d_disc = {(a, b): (0 if a == b else 1) for a in pts for b in pts}
M = FiniteMetricSpace(carrier=tuple(pts), distance=d_disc)

f_cycle = {1: 2, 2: 3, 3: 1}
p = classify_finite_metric_map(M, M, f_cycle)
print("isometry:", p.isometry)
print("bijective:", p.bijective)
print("homeomorphism:", p.homeomorphism)
print("lipschitz_constant:", p.lipschitz_constant)
```

```text
isometry: True
bijective: True
homeomorphism: True
lipschitz_constant: 1.0
```

Ayrık metrikte farklı iki nokta arası mesafe daima 1'dir. Döngü bir
permütasyon (bijeksiyon) olduğundan her çifti yine farklı bir çifte gönderir;
mesafe 1 → 1 korunur. Demek ki döngü bir izometridir (K=1) ve bijektif izometri
olarak Teorem 2.1 gereği bir homeomorfizmadır.

---

### K2 — Öklid metrikte kaydırma fonksiyonu

(ch16 K2 alıştırmasına dön)

```python
from pytop.metric_spaces import FiniteMetricSpace
from pytop.metric_map_taxonomy import classify_finite_metric_map

pts = [0, 1, 2, 3, 4]
d_eucl = {(a, b): abs(a - b) for a in pts for b in pts}
M = FiniteMetricSpace(carrier=tuple(pts), distance=d_eucl)

# x+1, fakat tasiyiciyi asmamak icin 4'te durur
f_shift = {0: 1, 1: 2, 2: 3, 3: 4, 4: 4}
p = classify_finite_metric_map(M, M, f_shift)
print("lipschitz_constant:", p.lipschitz_constant)
print("isometry:", p.isometry)
print("bijective:", p.bijective)
```

```text
lipschitz_constant: 1.0
isometry: False
bijective: False
```

Kaydırma sınırlı bir taşıyıcıda kalmak için 4'te doyduğundan 3 ve 4 aynı
görüntüye (4) gider: bijektif değildir ve izometri değildir (mesafe 1 olan (3,4)
çifti mesafe 0'a iner). Yine de hiçbir çiftte mesafe büyümediği için Lipschitz
sabiti K=1'dir (genişlemez). Saf bir öteleme (taşma olmadan) tam izometri,
K=1 verirdi.

---

### K3 — Sabit fonksiyon: K = 0

(ch16 K3 alıştırmasına dön)

```python
from pytop.metric_spaces import FiniteMetricSpace
from pytop.metric_map_taxonomy import classify_finite_metric_map

pts = [1, 2, 3, 4]
d_disc = {(a, b): (0 if a == b else 1) for a in pts for b in pts}
M = FiniteMetricSpace(carrier=tuple(pts), distance=d_disc)

f_const = {1: 1, 2: 1, 3: 1, 4: 1}
p = classify_finite_metric_map(M, M, f_const)
print("lipschitz_constant:", p.lipschitz_constant)
print("non_expansive:", p.non_expansive)
print("bijective:", p.bijective)
```

```text
lipschitz_constant: 0.0
non_expansive: True
bijective: False
```

Sabit fonksiyon tüm noktaları tek bir görüntüye gönderir: her çiftte
d₂(f(x),f(y))=0 olduğundan oran daima 0, dolayısıyla K=0 (mümkün en küçük
Lipschitz sabiti). Genişlemezdir (0 ≤ d₁), ama açıkça bijektif değildir.

---

### K4 — Büzülme f(x) = x/2: K < 1

(ch16 K4 alıştırmasına dön)

```python
from pytop.metric_spaces import FiniteMetricSpace
from pytop.metric_map_taxonomy import classify_finite_metric_map

src = [0, 2, 4, 6]
img = [0, 1, 2, 3]
d_src = {(a, b): abs(a - b) for a in src for b in src}
d_img = {(a, b): abs(a - b) for a in img for b in img}
M_src = FiniteMetricSpace(carrier=tuple(src), distance=d_src)
M_img = FiniteMetricSpace(carrier=tuple(img), distance=d_img)

f_half = {0: 0, 2: 1, 4: 2, 6: 3}
p = classify_finite_metric_map(M_src, M_img, f_half)
print("lipschitz_constant:", p.lipschitz_constant)
print("similarity_ratio:", p.similarity_ratio)
print("non_expansive:", p.non_expansive)
```

```text
lipschitz_constant: 0.5
similarity_ratio: 0.5
non_expansive: True
```

Her mesafe tam yarıya indiğinden oran tüm çiftlerde sabit 0.5: bu hem bir
büzülmedir (K=0.5 < 1) hem de oranı c=0.5 olan bir benzerliktir. K<1 koşulu
sağlanır; tam bir metrik uzayda Banach teoremi böyle bir eşlemenin eşsiz sabit
noktasını garanti ederdi.

---

### K5 — Aynı döngü, iki farklı metrik

(ch16 K5 alıştırmasına dön)

```python
from pytop.metric_spaces import FiniteMetricSpace
from pytop.metric_map_taxonomy import classify_finite_metric_map

pts = [1, 2, 3]
cyc = {1: 2, 2: 3, 3: 1}

d_disc = {(a, b): (0 if a == b else 1) for a in pts for b in pts}
d_eucl = {(a, b): abs(a - b) for a in pts for b in pts}
M_disc = FiniteMetricSpace(carrier=tuple(pts), distance=d_disc)
M_eucl = FiniteMetricSpace(carrier=tuple(pts), distance=d_eucl)

p_disc = classify_finite_metric_map(M_disc, M_disc, cyc)
p_eucl = classify_finite_metric_map(M_eucl, M_eucl, cyc)
print("discrete isometry:", p_disc.isometry)
print("euclid isometry:", p_eucl.isometry)
print("euclid lipschitz_constant:", p_eucl.lipschitz_constant)
```

```text
discrete isometry: True
euclid isometry: False
euclid lipschitz_constant: 2.0
```

Metrik, izometri olup olmamayı belirler. Ayrık metrikte her permütasyon
izometridir (mesafe daima 1). Öklid metrikte ise döngü 3→1 eşlemesinde mesafe
|2−3|=1 olan komşu çifti |3−1|=2 olan çifte taşır: mesafe korunmaz, izometri
değildir ve Lipschitz sabiti 2'ye çıkar. Aynı soyut permütasyonun "rijit"
olup olmaması taşıyıcının üzerindeki metriğe bağlıdır.

---

### T1 — İzometri ⟹ genişlemez ⟹ Lipschitz (K=1)

(ch16 T1 alıştırmasına dön)

**İddia.** Her izometri genişlemez, her genişlemez fonksiyon K=1 ile Lipschitz'tir.

**İspat.** f izometri olsun: tüm x,y için d₂(f(x),f(y)) = d₁(x,y).

1. **İzometri ⟹ genişlemez.** Eşitlik özel bir ≤ durumudur:
   d₂(f(x),f(y)) = d₁(x,y) ≤ d₁(x,y). Tanım gereği f genişlemezdir
   (non-expansive).

2. **Genişlemez ⟹ Lipschitz (K=1).** g genişlemez olsun:
   d₂(g(x),g(y)) ≤ d₁(x,y) = 1·d₁(x,y). Bu tam olarak K=1 sabitli Lipschitz
   koşuludur. Lipschitz sabiti, oranların supremumu olduğundan, izometride
   her oran tam 1'dir: K = sup 1 = 1.

Böylece zincir İzometri ⟹ Genişlemez ⟹ Lipschitz (K=1) kurulur. (Tersi yanlıştır:
K=1 Lipschitz ama izometri olmayan eşleme vardır — örn. K4'teki taşan kaydırma
genişlemez/K=1 ama izometri değil.) ∎

---

### T2 — Lipschitz ⟹ üniform sürekli (δ = ε/K)

(ch16 T2 alıştırmasına dön)

**İddia.** Sabiti K>0 olan her Lipschitz fonksiyon düzgün (üniform) süreklidir.

**İspat.** f Lipschitz olsun: tüm x,y için d₂(f(x),f(y)) ≤ K·d₁(x,y).
Verilen herhangi bir ε>0 için **δ = ε/K** seçelim (bu seçim yalnızca ε ve K'ye
bağlı; herhangi bir x noktasına bağlı değil). d₁(x,y) < δ olduğunda:

    d₂(f(x),f(y)) ≤ K·d₁(x,y) < K·δ = K·(ε/K) = ε.

δ noktadan bağımsız seçildiği için bu, düzgün süreklilik tanımının ta kendisidir.
(K=0 sabit fonksiyon durumunda f sabittir ve trivially düzgün süreklidir; δ keyfi
alınabilir.) Düzgün süreklilik her noktada sıradan sürekliliği de içerdiğinden
f süreklidir. ∎

---

### T3 — İzometri injektiftir; sabit fonksiyon izometri olamaz

(ch16 T3 alıştırmasına dön)

**İddia.** Her izometri injektiftir; iki noktadan fazla içeren bir uzayda sabit
bir fonksiyon izometri olamaz.

**İspat (injektiflik).** f izometri ve f(x) = f(y) olsun. İzometri eşitliğinden:

    d₁(x,y) = d₂(f(x),f(y)) = d₂(f(x),f(x)) = 0.

Metriğin ayırma aksiyomu (d(a,b)=0 ⟺ a=b) gereği d₁(x,y)=0 ⟹ x=y. Dolayısıyla
f farklı noktaları farklı noktalara gönderir: injektiftir.

**Sabit fonksiyon neden izometri olamaz.** En az iki farklı noktası (x≠y) olan
bir uzayda sabit fonksiyon c, x ve y'yi aynı görüntüye gönderir: f(x)=f(y).
İzometri olsaydı injektif olması gerekirdi (yukarıdaki argüman), x≠y ile çelişir.
Doğrudan da görülür: d₁(x,y) > 0 iken d₂(f(x),f(y)) = 0, mesafe korunmaz. Bu
yüzden sabit fonksiyon (tek noktalı uzaylar dışında) asla izometri değildir —
Örnek 5.3'te lipschitz_constant=0 ama isometry=False çıkması bunun sayısal
doğrulamasıdır. ∎
