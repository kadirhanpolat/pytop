# Alıştırma Çözümleri

Bu ek, Bölüm 12 (Bölüm Topolojisi) alıştırmalarının tam çözümlerini içerir.
Kodlama çözümlerindeki tüm çıktılar gerçek çalıştırmadan alınmıştır; teori
çözümleri tam argüman verir.

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
