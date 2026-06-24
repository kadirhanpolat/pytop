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
