# Geometrik Hesaplamalar: Sarım, Yüzey, Planarlık -- GEOCOMP-01

- Sürüm: `v0.6.0`
- Hat: `GEOCOMP-01`
- Kaynak odağı: Basener (derece, vektör alanı); Adams & Franzosa (yüzeyler, graflar)
- Dil ilkesi: Bu dosya Türkçedir; Python API adları paket standardı gereği
  İngilizce tutulmuştur.

## 1. Sarım Sayısı ve Derece

`winding_number.py`, örneklenmiş geometrik veriden tamsayı topolojik değişmezler hesaplar.

```python
import math
from pytop import winding_number, circle_map_degree, vector_field_index

circle = [(math.cos(2*math.pi*k/12), math.sin(2*math.pi*k/12)) for k in range(12)]
print(winding_number(circle))                       # 1  (orijini bir kez sarar)

# z -> z^2 derecesi 2 (açıyı ikiye katlar)
imgs = [(math.cos(2*2*math.pi*k/24), math.sin(2*2*math.pi*k/24)) for k in range(24)]
print(circle_map_degree(imgs))                       # 2

# v(x,y) = (x,-y) eyer alanının izole sıfırdaki indeksi
print(vector_field_index([(x, -y) for x, y in circle]))   # -1
```

## 2. Çokgen Kelimesinden Yüzey Sınıflandırma

`classify_surface_word`, bir çokgenin kenar-özdeşleştirme kelimesinden kapalı
yüzeyin topolojik tipini hesaplar (köşe özdeşleştirmesi → V−E+F).

```python
from pytop import classify_surface_word

for word in ["a a^-1", "a b a^-1 b^-1", "a a", "a b a^-1 b", "a b a^-1 b^-1 c d c^-1 d^-1"]:
    s = classify_surface_word(word)
    print(f"{word:30} -> chi={s.euler_characteristic:>2}  {s.name}")
# a a^-1                         -> chi= 2  sphere
# a b a^-1 b^-1                  -> chi= 0  torus
# a a                           -> chi= 1  projective plane
# a b a^-1 b                    -> chi= 0  Klein bottle
# a b a^-1 b^-1 c d c^-1 d^-1    -> chi=-2  orientable genus-2 surface
```

## 3. Graf Planarlığı ve Genus (kesin)

`graph_planarity.py`, küçük graflar için rotasyon-sistemi aramasıyla **kesin**
planarlık ve genus hesaplar.

```python
from itertools import combinations
from pytop import is_planar, graph_genus

K5 = list(combinations(range(5), 2))
K33 = [(i, 3 + j) for i in range(3) for j in range(3)]
print(is_planar(list(combinations(range(4), 2))))   # True  (K4 planar)
print(is_planar(K5), graph_genus(K5))               # False 1
print(is_planar(K33), graph_genus(K33))             # False 1
```

## 4. Köprü

Bu üç motor, `degree_theory.py`, `surface_classification.py`/`surface_gluing.py`
ve `graph_topology.py`'deki betimsel profillerin hesaplamalı karşılıklarıdır:
profiller "ne olduğunu bilir", bu motorlar "senin girdinden hesaplar".
