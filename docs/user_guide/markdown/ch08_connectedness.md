# Bölüm 8 — Bağlantılılık

Bağlantılılık, bir topolojik uzayın iki ayrı açık parçaya bölünememesi özelliğidir.
Yol-bağlantılılık daha güçlü bir kavramdır ve sürekli yolların varlığına dayanır.

---

## 1. Konu

### Bağlantılılık Kavramları

| Kavram | Tanım |
|--------|-------|
| **Bağlantılı (connected)** | X = U ∪ V, U∩V = ∅, U,V açık ⟹ U=∅ veya V=∅ |
| **Yol-bağlantılı (path-connected)** | ∀ x,y ∈ X: ∃ sürekli f:[0,1]→X, f(0)=x, f(1)=y |
| **Ark-bağlantılı (arc-connected)** | Yol-bağlantılı; üstelik yollar enjektif |
| **Lokal bağlantılı** | Her noktanın bağlantılı komşulukları var |
| **Tamamen bağlantısız** | Her bağlantılı alt küme tek-noktadır |

**Sıralama:** Ark-bağlantılı ⟹ Yol-bağlantılı ⟹ Bağlantılı.

### Clopen Ayrılma

X bağlantısız ⟺ boş olmayan trivial olmayan bir clopen A ⊆ X vardır.

> **Neden bu konu?** Bağlantılılık ve yol-bağlantılılık aynı kavram değildir; pytop ikisini ayrı ayrı test eder.

> 🔍 **Kendin dene:** Sierpiński `is_connected` mı? Cevabınızı tahmin edin, sonra test edin.

> ⚠️ **Sık hata:** Yol-bağlantılı ⟹ Bağlantılı, ama tersi yanlış; `is_path_connected True` iken `is_connected False` olamaz.

> ↗️ **Bkz.:** Bölüm 10 (sürekli görüntü bağlantılıdır).

> 💭 **Öz-yansıtma:** Ayrık topoloji neden bağlantısızdır?

---

## 2. Teoremler

**Teorem 2.1.** Bağlantılı küme süreklilik altında bağlantılıdır:
f: X → Y sürekli, X bağlantılı ⟹ f(X) bağlantılı.

**Teorem 2.2.** Yol-bağlantılı ⟹ bağlantılı. Tersi genel olarak yanlış.
(Karşı örnek: Topolojist sinüs eğrisi — bağlantılı ama yol-bağlantısız.)

**Teorem 2.3 (Ara Değer Teoremi).** f: X → ℝ sürekli, X bağlantılı, a,b ∈ f(X) ise
her c ∈ [a,b] için f⁻¹(c) ≠ ∅.

**Teorem 2.4.** Gerçek doğru ℝ'de bağlantılı alt kümeler tam olarak aralıklardır.

---

## 3. Algoritmalar

### Sonlu Bağlantılılık — O(|τ|²)

```
BagliMi(X, tau):
    for each non-empty A ⊊ X:
        if A ∈ tau and X\A ∈ tau:
            return False   // A clopen bölme bulundu
    return True
```

Karmaşıklık: O(|τ|²) — clopen küme taraması.

---

## 4. pytop API

```python
from pytop import (
    is_connected,
    is_path_connected,
    is_locally_connected,
    is_totally_disconnected,
)
try:
    from pytop import is_arc_connected
except ImportError:
    is_arc_connected = None
```

Tüm fonksiyonlar `Result` döner: `.status` ('true'/'false'/'unknown').

---

## 5. Örnekler

### Örnek 5.1 — Sierpiński: Bağlantılı

```python
from pytop import sierpinski_space, is_connected, is_path_connected

s = sierpinski_space()
print("connected?", is_connected(s).status)
print("path_connected?", is_path_connected(s).status)
```

```text
connected?       true
path_connected?  unknown
```

Sierpiński {0,1} uzayı bağlantılıdır: {1} açık, {0} kapalı; clopen bölme yok.

### Örnek 5.2 — Ayrık Topoloji: Tamamen Bağlantısız

```python
from pytop import discrete_topology, is_connected, is_totally_disconnected

d = discrete_topology(1, 2, 3)
print("connected?", is_connected(d).status)
print("totally_disconn?", is_totally_disconnected(d).status)
```

```text
connected?          false
totally_disconn?    true
```

Ayrık topolojide {1} hem açık hem kapalı — clopen bölme var.

### Örnek 5.3 — İndiscrete: Bağlantılı

```python
from pytop import indiscrete_topology, is_connected

ind = indiscrete_topology('a', 'b')
print("connected?", is_connected(ind).status)
```

```text
connected?  true
```

### Örnek 5.4 — Gerçek Doğru ve [0,1]

```python
from pytop import real_line_metric, closed_unit_interval_metric
from pytop import is_connected, is_path_connected

rl = real_line_metric()
ui = closed_unit_interval_metric()
print("R connected?", is_connected(rl).status)
print("R path_connected?", is_path_connected(rl).status)
print("[0,1] connected?", is_connected(ui).status)
print("[0,1] path_connected?", is_path_connected(ui).status)
```

```text
R connected?          true
R path_connected?     true
[0,1] connected?      true
[0,1] path_connected? true
```

### Örnek 5.5 — Kosonlu Topoloji

```python
from pytop import naturals_cofinite, is_connected, is_path_connected

nc = naturals_cofinite()
print("connected?", is_connected(nc).status)
print("path_connected?", is_path_connected(nc).status)
```

```text
connected?       true
path_connected?  unknown
```

### Örnek 5.6 — Lokal Bağlantılılık

```python
from pytop import is_locally_connected

print("Sierpinski locally_connected?", is_locally_connected(s).status)
print("Discrete locally_connected?", is_locally_connected(d).status)
print("R locally_connected?", is_locally_connected(rl).status)
```

```text
Sierpinski locally_connected?  unknown
Discrete locally_connected?    unknown
R locally_connected?           unknown
```

---

## 6. Alıştırmalar

### Kodlama

K1. `make_topology({1,2,3}, {1}, {2,3})` topolojisi için `is_connected` hesaplayın.
    {1} ve {2,3} clopen bölme gösteriyor mu?

K2. `finite_chain_space(4)` zincirinin bağlantılı olup olmadığını kontrol edin.

K3. `two_point_discrete_space()` ve `two_point_indiscrete_space()` üzerinde
    `is_connected`, `is_path_connected` karşılaştırın.

### Teori

T1. Bağlantılı + sürekli ⟹ görüntü bağlantılı teoremini ispatlayın.

T2. Yol-bağlantılı ⟹ bağlantılı implicasyonunu ispatlayın.
