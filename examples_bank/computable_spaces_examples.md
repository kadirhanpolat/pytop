# Hesaplanabilir Uzaylar ve Yapı-Koruma Çıkarımı (deneysel) -- SPACES-01

- Sürüm: `v0.6.0+` (deneysel, kararsız API)
- Hat: `SPACES-01`
- Kaynak odağı: Araştırma-sınıfı yol haritası, Faz 1 (bkz. `docs/CAPABILITIES_AND_ROADMAP.md`)
- Dil ilkesi: Bu dosya Türkçedir; Python API adları paket standardı gereği
  İngilizce tutulmuştur.

## 1. Ne Sağlıyor?

`pytop.experimental.spaces`, sonlu **ve sonlu-temsilli sonsuz** uzayları tek bir
`Space` protokolünde birleştirir; yüklemler **tanık/karşı-örnek** üretir ve
**karar-verilebilirlik** konusunda dürüsttür (decided / undecidable). Kurulmuş
uzayların özellikleri — sonsuz olanlar dahil, **saymadan** — koruma teoremleriyle
türetilir.

## 2. Yüklemler: hesapla, sertifika, veya dürüstçe "bilinmiyor"

```python
from pytop.experimental.spaces import (
    FiniteSpace, CofiniteSpace, OrderTopologySpace, rational_metric_space,
    is_hausdorff, is_compact, is_connected,
)

sierpinski = FiniteSpace("Sierpinski", {0, 1}, [set(), {0}, {0, 1}])
is_hausdorff(sierpinski).value          # False (DECIDED, karşıörnek=(0,1)) — sonlu, hesaplandı

is_hausdorff(CofiniteSpace()).value     # False — sonsuz, yapı sertifikası
is_connected(CofiniteSpace()).value     # True  — hyperconnected
is_compact(OrderTopologySpace()).value  # False — Q kompakt değil

is_compact(rational_metric_space()).decidability   # UNDECIDABLE — "metrik olmak" kompaktlığı belirlemez
```

## 3. Sonlu yapı kapanışı (S2)

```python
from pytop.experimental.spaces import discrete_finite_space, binary_product, is_hausdorff

p = binary_product(discrete_finite_space({0, 1}), discrete_finite_space({0, 1}))
is_hausdorff(p).value        # True — Hausdorff × Hausdorff, hesaplanıp doğrulandı
```

## 4. Yapı-koruma çıkarımı (S3) — sonsuz uzaylar, saymadan, KANITLA

```python
from pytop.experimental.spaces import (
    ProductSpace, SubspaceSpace, CofiniteSpace, OrderTopologySpace,
    rational_metric_space, derive, explain,
)

# İki SONSUZ uzayın çarpımı T1 mi? (productivity)
prod = ProductSpace([CofiniteSpace(), OrderTopologySpace()])
print(explain(prod, "T1"))
# - T1 holds for cofinite(N)×order topology(Q): T1 is preserved by product
#   - T1 holds for cofinite(N): leaf: cofinite topology is T1 (points are closed)
#   - T1 holds for order topology(Q): leaf: order topology on Q is T1 ...

# Sonsuz metrik uzayın alt-uzayı regular mı? (heredity)
sub = SubspaceSpace(rational_metric_space(), member=lambda x: True)
derive(sub, "regular").verdict.value     # True — "subspace of a regular space is regular"
```

## 5. Karşı-örnek sentezi

```python
from pytop.experimental.spaces import synthesize, derive

s = synthesize(has=["connected"], lacks=["T2"])   # bağlantılı ama Hausdorff olmayan bir uzay bul
derive(s, "connected").verdict.value, derive(s, "T2").verdict.value   # (True, False)
```

## 6. pi-Base ile çapraz doğrulama

Koruma tablosu (subspace→hereditary, product→productive, sum→coproduct) elle
küratörlüdür ama **pi-Base meta-özellikleriyle çapraz doğrulanır**: pi-Base bir
özelliği "hereditary"/"preserved by products" olarak işaretlediğinde tablomuz
buna uymak zorundadır (bkz. `tests/experimental/test_preservation_crossvalidation.py`).
pi-Base meta'sı seyrek olduğundan tabloyu **doğrular** ama **belirlemez**.

```python
from pytop.experimental.pi_base import property_meta
property_meta("Compact")   # ('coarser', 'hereditary_closed', 'products_arbitrary', 'sums_finite')
property_meta("T0")        # ('hereditary', 'sums_arbitrary')
```
