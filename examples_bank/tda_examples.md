# Topolojik Veri Analizi (Persistent Homoloji) -- TDA-01

- Sürüm: `v0.6.0`
- Hat: `TDA-01`
- Kaynak odağı: Basener Böl. 7; Adams & Franzosa (TDA ekleri)
- Dil ilkesi: Bu dosya Türkçedir; Python API adları paket standardı gereği
  İngilizce tutulmuştur.

## 1. Ne Hesaplıyoruz?

`persistent_homology.py` artık betimsel profillerin yanında **gerçek bir TDA
motoru** içerir. Sonlu metrik uzaydan Vietoris–Rips filtrasyonu kurulur, sınır
matrisi ℤ/2 üzerinde standart sütun-indirgemesiyle indirgenir ve her homoloji
sınıfının **doğum–ölüm** çifti (barkod) çıkarılır.

## 2. İki Küme: H₀ Birleşmeyi Görür

```python
import math
from pytop import persistent_homology
from pytop.metric_spaces import FiniteMetricSpace

points = [(0.0, 0.0), (0.0, 0.3), (5.0, 0.0), (5.0, 0.3)]
space = FiniteMetricSpace(carrier=tuple(points), distance=math.dist)

pairs = persistent_homology(space, max_dimension=1)
h0 = [p for p in pairs if p.dimension == 0]
print(sorted(p.death for p in h0 if not p.is_essential))  # [0.3, 0.3, 5.0]
print(sum(1 for p in h0 if p.is_essential))                # 1
```

Küme-içi birleşmeler 0.3'te, kümeler arası birleşme 5.0'da olur: barkoddaki
açık boşluk "iki küme" sinyalidir.

## 3. Çember Örneklemi: Tek Uzun H₁ Barı

```python
import math
from pytop import persistent_homology
from pytop.metric_spaces import FiniteMetricSpace

n = 12
pts = [(math.cos(2*math.pi*k/n), math.sin(2*math.pi*k/n)) for k in range(n)]
space = FiniteMetricSpace(carrier=tuple(pts), distance=math.dist)

pairs = persistent_homology(space, max_dimension=2)
h1 = [p for p in pairs if p.dimension == 1]
longest = max(h1, key=lambda p: p.persistence)
print(round(longest.birth, 3))        # ~0.518 = 2*sin(pi/12) (en yakın komşu)
print(longest.persistence > 0.3)      # True -> belirgin tek delik
```

## 4. Barkod, Diyagram ve Euler Eğrisi

```python
from pytop import vietoris_rips_filtration, euler_characteristic_curve
from pytop.persistent_homology import barcode, persistence_diagram

bars = barcode(pairs, dimension=1)          # [(doğum, ölüm), ...]
diagram = persistence_diagram(pairs)        # {boyut: ((doğum, ölüm), ...)}
filt = vietoris_rips_filtration(space, max_dimension=2)
curve = euler_characteristic_curve(filt, scales=(0.0, 0.5, 1.0, 2.0))
```

## 5. Köprü

Motor `homology.py` ile aynı sınır-matrisi cebirine dayanır; tepe ölçekte
kalan **temel (essential) sınıf** sayısı, oluşan kompleksin Betti sayılarıyla
çakışır (bkz. `tests/core/test_persistent_homology_engine.py`).
