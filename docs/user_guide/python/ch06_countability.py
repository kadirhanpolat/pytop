# %% [markdown]
"""
# Bölüm 6 — Sayılabilirlik Aksiyomları

Sayılabilirlik aksiyomları, bir topolojik uzaydaki "bilgi"nin sayılabilir büyüklükte
yapılarla tanımlanıp tanımlanamayacağını araştırır.
"""

# %% [markdown]
"""
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
"""

# %% [markdown]
"""
## 2. Teoremler

**Teorem 2.1.** 2nd countable ⟹ separable ∧ Lindelöf.
*(Kanıt: baz elemanlarından yoğun küme seç; örtüyü baza indirge.)*

**Teorem 2.2.** Metrik uzay ⟹ 1st countable.
*(Kanıt: her nokta için {B(x, 1/n)} yerel baz.)*

**Teorem 2.3.** Ayrılabilir + metrik ⟹ 2nd countable.
*(Kanıt: D ⊆ X yoğun sayılabilir; {B(d, 1/n) : d∈D, n∈ℕ} baz.)*

**Teorem 2.4 (Sorgenfrey Karşı Örneği).** Sorgenfrey doğrusu ayrılabilir ve
Lindelöf'tür ama 2. sayılabilir değildir.
"""

# %% [markdown]
"""
## 3. Algoritmalar

### Sonlu Uzayda Sayılabilirlik

Sonlu uzayda her aksiyom trivially sağlanır. Yerel baz boyutu = noktanın
komşuluk sistemi boyutu (χ(x) = |N(x)|). Baz: topoloji kendisi.

### Sonsuz Uzayda: Tag-Tabanlı Çıkarım

pytop sembolik uzaylarda sayılabilirlik özelliklerini etiket koridorlarından çıkarır:
- 'second_countable' etiketi ⟹ tüm aksiyomlar sağlanır (zincir)
- 'metric' ∧ 'separable' etiketi ⟹ 'second_countable' çıkarılır
"""

# %% [markdown]
"""
## 4. pytop API
"""

# %%
from pytop import (
    sierpinski_space,
    discrete_topology,
    finite_chain_space,
    real_line_metric,
    naturals_cofinite,
    is_first_countable,
    is_second_countable,
    is_separable,
    is_lindelof,
)
try:
    from pytop import countability_report
except ImportError:
    countability_report = None

try:
    from pytop.countability import analyze_countability
except ImportError:
    analyze_countability = None

# %% [markdown]
"""
## 5. Örnekler

### Örnek 5.1 — Gerçek Doğru: Tüm 4 Aksiyom ✓
"""

# %%
rl = real_line_metric()
print("=== Ornek 5.1: Gercek Dogru ===")
print("1st countable? ", is_first_countable(rl).status)
print("2nd countable? ", is_second_countable(rl).status)
print("separable?     ", is_separable(rl).status)
print("lindelof?      ", is_lindelof(rl).status)
print()
# Gercek dogru 4 aksiyomu da saglar: {(a,b): a,b∈Q} sayilabilir baz; Q yogun alt kume.

# %% [markdown]
"""
### Örnek 5.2 — Kosonlu Doğal Sayılar
"""

# %%
nc = naturals_cofinite()
print("=== Ornek 5.2: Naturals Cofinite ===")
print("1st countable? ", is_first_countable(nc).status)
print("2nd countable? ", is_second_countable(nc).status)
print("separable?     ", is_separable(nc).status)
print("lindelof?      ", is_lindelof(nc).status)
print()

# %% [markdown]
"""
### Örnek 5.3 — Sierpiński Uzayı
"""

# %%
s = sierpinski_space()
print("=== Ornek 5.3: Sierpinski ===")
print("1st countable? ", is_first_countable(s).status)
print("2nd countable? ", is_second_countable(s).status)
print("separable?     ", is_separable(s).status)
print()
# Sierpinski sonlu: tüm sayilabilirlik aksiyomları trivially saglanir.

# %% [markdown]
"""
### Örnek 5.4 — Ayrık Topoloji: Sonlu Uzay
"""

# %%
d = discrete_topology(1, 2, 3)
print("=== Ornek 5.4: Discrete{1,2,3} ===")
print("1st countable? ", is_first_countable(d).status)
print("2nd countable? ", is_second_countable(d).status)
print("separable?     ", is_separable(d).status)
print("lindelof?      ", is_lindelof(d).status)
print()
# Sonlu ayrik: tüm aksiyomlar saglanir (trivial).

# %% [markdown]
"""
### Örnek 5.5 — Karşılaştırma: Sayılabilirlik Özellikleri
"""

# %%
from pytop import sorgenfrey_line_like

sl = sorgenfrey_line_like()
print("=== Ornek 5.5: Sorgenfrey Dogrusu ===")
print("1st countable?  ", is_first_countable(sl).status)
print("2nd countable?  ", is_second_countable(sl).status)
print("separable?      ", is_separable(sl).status)
print("lindelof?       ", is_lindelof(sl).status)
print()
# Sorgenfrey: 1. sayilabilir ✓, ayrilabilir ✓, Lindelof ✓
# ama 2. sayilabilir DEGIL — baz boyutu continuum.

# %% [markdown]
"""
## 6. Alıştırmalar

### Kodlama

K1. finite_chain_space(5) üzerinde is_first_countable ve is_second_countable hesaplayın.

K2. two_point_discrete_space() ve two_point_indiscrete_space() üzerinde separability
    karşılaştırın.

K3. integers_discrete() (sayılabilir ayrık) için 2nd countable mi yoksa değil mi?

### Teori

T1. 2nd countable ⟹ separable olduğunu ispatlayın.
    (İpucu: her baz elemanından bir nokta seç.)

T2. Sorgenfrey doğrusunun 2. sayılabilir olmadığını nasıl gösterirsiniz?
    (Hint: alt intervaller [a,b) baz oluşturur ama uncountable.)
"""

if __name__ == "__main__":
    print("pytop Kullanim Kilavuzu — Bolum 6: Sayilabilirlik")
    print("=" * 50)
