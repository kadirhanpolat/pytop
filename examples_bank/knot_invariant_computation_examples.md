# Düğüm Değişmezi Hesabı -- KNOT-INV-01

- Sürüm: `v0.6.0`
- Hat: `KNOT-INV-01`
- Kaynak odağı: Adams & Franzosa Böl. 12; Basener (düğüm uygulamaları)
- Dil ilkesi: Bu dosya Türkçedir; Python API adları paket standardı gereği
  İngilizce tutulmuştur.

## 1. Ne Hesaplıyoruz?

`knot_invariants.py`, bir düğüm diyagramının **planar diyagram (PD) kodundan**
gerçek değişmezleri hesaplar: Kauffman parantezi → Jones polinomu, ve braid
kelimesinden indirgenmiş Burau temsili → Alexander polinomu. `knots.py`'deki
betimsel profiller korunur; bu modül hesaplama katmanıdır.

## 2. Jones Polinomu (Kauffman parantezi)

```python
from pytop import KnotDiagram, jones_polynomial

# Sağ trefoil (bu modülün işaret konvansiyonunda üç negatif kesişim)
trefoil = KnotDiagram([(1, 4, 2, 5), (3, 6, 4, 1), (5, 2, 6, 3)], signs=(-1, -1, -1))
print(dict(sorted(jones_polynomial(trefoil).coeffs.items())))
# {-4: -1, -3: 1, -1: 1}  ->  V = -t^-4 + t^-3 + t^-1

fig8 = KnotDiagram([(4, 2, 5, 1), (8, 6, 1, 5), (6, 3, 7, 4), (2, 7, 3, 8)],
                   signs=(1, -1, 1, -1))
print(dict(sorted(jones_polynomial(fig8).coeffs.items())))
# {-2: 1, -1: -1, 0: 1, 1: -1, 2: 1}  ->  amfikiral sekiz düğümü
```

## 3. Alexander Polinomu (braid kapanışı)

```python
from pytop import alexander_polynomial_from_braid

# trefoil = σ1^3 (B_2);  fig-8 = (σ1 σ2^-1)^2 (B_3)
print(dict(sorted(alexander_polynomial_from_braid([1, 1, 1], 2).coeffs.items())))
# {-1: 1, 0: -1, 1: 1}  ->  Δ = t - 1 + t^-1
print(dict(sorted(alexander_polynomial_from_braid([1, -2, 1, -2], 3).coeffs.items())))
# {-1: 1, 0: -3, 1: 1}  ->  Δ = t - 3 + t^-1
```

## 4. Writhe ve Bağlantı Sayısı

```python
from pytop import writhe, linking_number, is_valid_pd_code

print(writhe(trefoil))            # -3
print(is_valid_pd_code(trefoil))  # True (her etiket tam iki kez)
print(linking_number([1, 1]))     # 1  -> pozitif Hopf link
```

## 5. Köprü

Hesaplanan kesişim sayısı `knots.py`'deki `get_knot_profiles()` profilleriyle
çapraz doğrulanabilir (bkz. `tests/core/test_knot_invariants.py`). İşaret
konvansiyonu için modül docstring'ine bakınız.
