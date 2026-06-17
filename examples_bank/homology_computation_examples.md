# Simplisel Homoloji Hesabı -- HOMOLOGY-01

- Sürüm: `v0.6.0`
- Hat: `HOMOLOGY-01`
- Kaynak odağı: Manetti Böl. 9–14; Adams & Franzosa Böl. 6
- Dil ilkesi: Bu dosya Türkçedir; Python API adları paket standardı gereği
  İngilizce tutulmuştur.

## 1. Ne Hesaplıyoruz?

`homology.py`, sonlu bir `SimplicialComplex`'ten **tamsayı simplisel homolojiyi**
gerçekten hesaplar — hardcoded değer okumaz. Yönlendirilmiş sınır matrisleri
`∂_k` kurulur, ℤ üzerinde Smith Normal Form alınır, ve

```text
H_k(K; ℤ) = ker(∂_k) / im(∂_{k+1})
```

serbest kısmı (Betti sayısı) ile torsiyon kısmına (1'den büyük değişmez
çarpanlar) ayrıştırılır.

## 2. Küre S² (Δ³'ün sınırı)

```python
from pytop import generated_subcomplex, betti_numbers, homology_groups

sphere = generated_subcomplex([{1, 2, 3}, {1, 2, 4}, {1, 3, 4}, {2, 3, 4}])
print(betti_numbers(sphere))            # (1, 0, 1)  -> H0=ℤ, H1=0, H2=ℤ
print([g.describe() for g in homology_groups(sphere)])  # ['Z', '0', 'Z']
```

## 3. Torus T² ve Torsiyon Örneği ℝP²

```python
from pytop import betti_numbers, simplicial_homology, generated_subcomplex

# 3x3 ızgaranın toroidal özdeşleştirmesiyle torus: H1 = ℤ²
# (bkz. tests/core/test_homology.py içindeki kurucu)

rp2 = generated_subcomplex([
    {1, 2, 3}, {1, 3, 4}, {1, 4, 5}, {1, 5, 6}, {1, 2, 6},
    {2, 3, 5}, {2, 4, 5}, {2, 4, 6}, {3, 4, 6}, {3, 5, 6},
])
h1 = simplicial_homology(rp2, 1)
print(h1.betti, h1.torsion)   # 0 (2,)  ->  H1(ℝP²) = ℤ/2
print(h1.describe())          # 'Z/2'
```

ℝP² torsiyonu (ℤ/2), homolojinin homotopinin yakalayamadığı bilgiyi nasıl
taşıdığının klasik kanıtıdır.

## 4. Euler Karakteristiği Çapraz Doğrulaması

`euler_characteristic_via_homology`, Betti sayılarının alternatif toplamını
verir; Euler–Poincaré teoremi gereği bu, kombinatorik yüz sayımıyla
(`SimplicialComplex.euler_characteristic`) eşit olmalıdır:

```python
from pytop import euler_characteristic_via_homology
assert euler_characteristic_via_homology(sphere) == sphere.euler_characteristic() == 2
```

## 5. Köprü

Bu motor, `persistent_homology.py`'deki TDA hattının cebirsel temelidir ve
`combinatorial_topology.py`'deki hardcoded `betti_numbers` profillerini
doğrulamak için kullanılabilir.
