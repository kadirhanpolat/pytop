# Bölüm 6 — Sayılabilirlik Aksiyomları

Sayılabilirlik aksiyomları, bir topolojik uzaydaki "bilgi"nin sayılabilir büyüklükte
yapılarla tanımlanıp tanımlanamayacağını araştırır.

---

## 1. Konu

### Sayılabilirlik Aksiyomları

| Aksiyom | Tanım |
|---------|-------|
| **Birinci sayılabilir (1st countable)** | Her x∈X için sayılabilir yerel baz var |
| **İkinci sayılabilir (2nd countable)** | Tüm topoloji için sayılabilir global baz var |
| **Ayrılabilir (separable)** | X'in sayılabilir yoğun bir alt kümesi var |
| **Lindelöf** | Her açık örtünün sayılabilir alt-örtüsü var |

**Sıralama:**
- 2nd countable ⟹ 1st countable
- 2nd countable ⟹ separable ∧ Lindelöf

**Metrik uzay için:**
- Metrik ⟹ 1st countable
- Ayrılabilir metrik ⟹ 2nd countable

### Önemli Örnekler

| Uzay | 1st | 2nd | Sep | Lindelöf |
|------|-----|-----|-----|---------|
| ℝ (metrik) | ✓ | ✓ | ✓ | ✓ |
| Sorgenfrey doğrusu | ✓ | ✗ | ✓ | ✓ |
| Ayrık örtme | ✓ | sadece sayılabilir X | sadece sayılabilir | sadece sayılabilir |
| Kosonlu ℕ | ✓ | ✓ | ✓ | ✓ |

---

## 2. Teoremler

**Teorem 2.1.** 2nd countable ⟹ separable ∧ Lindelöf.
*(Kanıt: baz elemanlarından yoğun küme seç; örtüyü baza indirge.)*

**Teorem 2.2.** Metrik uzay ⟹ 1st countable.
*(Kanıt: her nokta için {B(x, 1/n)} yerel baz.)*

**Teorem 2.3.** Ayrılabilir + metrik ⟹ 2nd countable.
*(Kanıt: D ⊆ X yoğun sayılabilir; {B(d, 1/n) : d∈D, n∈ℕ} baz.)*

**Teorem 2.4 (Sorgenfrey Karşı Örneği).** Sorgenfrey doğrusu ayrılabilir ve
Lindelöf'tür ama 2. sayılabilir değildir.

---

## 3. Algoritmalar

### Sonlu Uzayda Sayılabilirlik

Sonlu uzayda her aksiyom trivially sağlanır.

- Yerel baz boyutu = noktanın komşuluk sistemi boyutu.
- Global baz = topoloji kendisi; sonlu ⟹ sayılabilir.
- Yoğun küme = carrier'ın kendisi.

Algoritma: O(1).

### Sonsuz Uzayda: Tag-Tabanlı Çıkarım

pytop sembolik uzaylarda tag koridorlarından sayılabilirlik çıkarır:
- `'second_countable'` etiketi ⟹ tüm aksiyomlar sağlanır
- `'metric'` ∧ `'separable'` etiketi ⟹ `'second_countable'` çıkarılır

---

## 4. pytop API

```python
from pytop import (
    is_first_countable,
    is_second_countable,
    is_separable,
    is_lindelof,
)
try:
    from pytop import countability_report
except ImportError:
    countability_report = None
```

Tüm fonksiyonlar `Result` döner: `.status` ('true'/'false'/'unknown').

---

## 5. Örnekler

### Örnek 5.1 — Gerçek Doğru: Tüm 4 Aksiyom

```python
from pytop import real_line_metric
from pytop import is_first_countable, is_second_countable, is_separable, is_lindelof

rl = real_line_metric()
print("1st countable?", is_first_countable(rl).status)
print("2nd countable?", is_second_countable(rl).status)
print("separable?", is_separable(rl).status)
print("lindelof?", is_lindelof(rl).status)
```

```text
1st countable?  true
2nd countable?  true
separable?      true
lindelof?       true
```

ℝ: {(a,b): a,b∈ℚ} sayılabilir baz; ℚ yoğun alt küme.

### Örnek 5.2 — Kosonlu Doğal Sayılar

```python
from pytop import naturals_cofinite

nc = naturals_cofinite()
print("1st countable?", is_first_countable(nc).status)
print("2nd countable?", is_second_countable(nc).status)
print("separable?", is_separable(nc).status)
print("lindelof?", is_lindelof(nc).status)
```

```text
1st countable?  true
2nd countable?  true
separable?      true
lindelof?       true
```

### Örnek 5.3 — Sierpiński Uzayı

```python
from pytop import sierpinski_space

s = sierpinski_space()
print("1st countable?", is_first_countable(s).status)
print("2nd countable?", is_second_countable(s).status)
print("separable?", is_separable(s).status)
```

```text
1st countable?  true
2nd countable?  true
separable?      true
```

Sierpiński sonlu: tüm sayılabilirlik aksiyomları trivially sağlanır.

### Örnek 5.4 — Ayrık Topoloji

```python
from pytop import discrete_topology

d = discrete_topology(1, 2, 3)
print("1st countable?", is_first_countable(d).status)
print("2nd countable?", is_second_countable(d).status)
print("separable?", is_separable(d).status)
print("lindelof?", is_lindelof(d).status)
```

```text
1st countable?  true
2nd countable?  true
separable?      true
lindelof?       true
```

### Örnek 5.5 — Sorgenfrey Doğrusu: 2nd Countable ✗

```python
from pytop import sorgenfrey_line_like

sl = sorgenfrey_line_like()
print("1st countable?", is_first_countable(sl).status)
print("2nd countable?", is_second_countable(sl).status)
print("separable?", is_separable(sl).status)
print("lindelof?", is_lindelof(sl).status)
```

```text
1st countable?   true
2nd countable?   false
separable?       true
lindelof?        true
```

Sorgenfrey: 1. sayılabilir ✓, ayrılabilir ✓, Lindelöf ✓
ama 2. sayılabilir değil — baz boyutu continuum.

---

## 6. Alıştırmalar

### Kodlama

K1. `finite_chain_space(5)` üzerinde `is_first_countable` ve `is_second_countable`
    hesaplayın.

K2. `two_point_discrete_space()` ve `two_point_indiscrete_space()` üzerinde
    `is_separable` karşılaştırın.

K3. `integers_discrete()` (sayılabilir ayrık) için 2nd countable mi yoksa değil mi?

### Teori

T1. 2nd countable ⟹ separable olduğunu ispatlayın.
    (İpucu: her baz elemanından bir nokta seç.)

T2. Sorgenfrey doğrusunun 2. sayılabilir olmadığını nasıl gösterirsiniz?
    (Hint: alt intervaller [a,b) baz oluşturur ama uncountable.)
