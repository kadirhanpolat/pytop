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
