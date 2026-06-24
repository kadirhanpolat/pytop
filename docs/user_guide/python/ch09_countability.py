# %% [markdown]
"""
# Bölüm 9 — Sayılabilirlik Aksiyomları

Sayılabilirlik aksiyomları, bir topolojik uzaydaki "bilgi"nin sayılabilir büyüklükte
yapılarla tanımlanıp tanımlanamayacağını araştırır.

---
"""

# %% [markdown]
"""
## 1. Konu
"""

# %% [markdown]
"""
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

![2. sayılabilirden 1. sayılabilir, ayrılabilir ve Lindelöf'e implikasyonlar; metrik ⟹ 1. sayılabilir; Sorgenfrey karşı-örneği](../assets/ch09/fig_ch09_sayilabilirlik_implikasyon.png)

> 💡 **Sezgi:** Sayılabilirlik aksiyomları, bir uzayı "sayılabilir bir sözlükle" anlatabilme sorusudur. **2. sayılabilirlik** uzayın *tüm* açıklarını sayılabilir bir baz listesinden kurar — tek bir küresel sözlük. **1. sayılabilirlik** ise yalnızca *her nokta için ayrı* bir sayılabilir komşuluk listesi ister — yerel sözlükler. Küresel bir liste her noktaya yerel liste verdiği için 2. ⟹ 1.; tersi her zaman doğru değildir, çünkü tek tek noktalar zengin olsa bile bütünü sayılabilir bir listeyle örtmek mümkün olmayabilir.

![Bir x noktası çevresinde iç içe küçülen B1 ⊃ B2 ⊃ B3 komşulukları: sayılabilir yerel baz](../assets/ch09/fig_ch09_yerel_baz.png)

> ❌ **Karşı-örnek (Sorgenfrey doğrusu):** $[a,b)$ biçimli yarı-açık aralıklarla üretilen Sorgenfrey doğrusu **1. sayılabilir, ayrılabilir ve Lindelöf**'tür ama **2. sayılabilir değildir**. Her $x$ için $\{[x, x+1/n) : n\in\mathbb{N}\}$ sayılabilir yerel baz verir (1. sayılabilir); $\mathbb{Q}$ yoğundur (ayrılabilir). Ama herhangi bir baz, her $x$ için tam olarak $x$'te başlayan bir baz elemanı içermek zorundadır; farklı $x$'ler farklı eleman gerektirdiğinden baz en az continuum büyüklüktedir — sayılamaz. Bu örnek "2. ⟸ 1. ∧ ayrılabilir ∧ Lindelöf" çıkarımının **geçersiz** olduğunu gösterir.
"""

# %% [markdown]
"""
### Önemli Örnekler

| Uzay | 1st | 2nd | Sep | Lindelöf |
|------|-----|-----|-----|---------|
| ℝ (metrik) | ✓ | ✓ | ✓ | ✓ |
| Sorgenfrey doğrusu | ✓ | ✗ | ✓ | ✓ |
| Ayrık örtme | ✓ | sadece sayılabilir X | sadece sayılabilir | sadece sayılabilir |
| Kosonlu ℕ | ✓ | ✓ | ✓ | ✓ |

> **Neden bu konu?** 1. ve 2. sayılabilirlik aksiyomları analizin temel araçları; metrik uzaylar her ikisini de sağlar.

> 🔍 **Kendin dene:** `discrete_topology(0,1,2)` için `is_first_countable` ve `is_second_countable` sonuçlarını karşılaştırın.

> ⚠️ **Sık hata:** 2. sayılabilirlik ⟹ 1. sayılabilirlik; 1. için `True`, 2. için `False` mümkündür ama tersi mümkün değil.

> ↗️ **Bkz.:** Bölüm 7 (Lindelöf ↔ 2. sayılabilir + T3).

> 💭 **Öz-yansıtma:** Metrik uzay neden her zaman 1. sayılabilirdir?

---
"""

# %% [markdown]
"""
## 2. Teoremler

**Teorem 2.1.** 2nd countable ⟹ separable ∧ Lindelöf.

> **İspat eskizi.** $\mathcal{B}=\{B_n\}$ sayılabilir baz olsun. **Ayrılabilir:** her boş olmayan $B_n$'den bir $d_n$ seç; $D=\{d_n\}$ sayılabilirdir. Boş olmayan herhangi açık $U$ bir $B_n\subseteq U$ içerir, dolayısıyla $d_n\in U\cap D$ — yani $\overline{D}=X$. **Lindelöf:** keyfi açık örtü $\{U_\alpha\}$ verilsin; örtüde yer alan her noktayı içeren bir $B_n$'i, onu kapsayan bir $U_\alpha$ ile eşle. Böyle kullanılan $B_n$'ler sayılabilir, dolayısıyla seçilen $U_\alpha$'lar sayılabilir bir alt-örtü oluşturur. ∎

**Teorem 2.2.** Metrik uzay ⟹ 1st countable.

> **İspat eskizi.** Her $x$ için $\{B(x, 1/n) : n\in\mathbb{N}\}$ sayılabilirdir ve bir yerel bazdır: $x$'in her $U$ komşuluğu bir $\varepsilon>0$ ile $B(x,\varepsilon)\subseteq U$ içerir; $1/n<\varepsilon$ seçilince $B(x,1/n)\subseteq U$. (Şekildeki iç içe küçülen toplar bu yerel bazı resmeder.) ∎

**Teorem 2.3.** Ayrılabilir + metrik ⟹ 2nd countable.

> **İspat eskizi.** $D\subseteq X$ yoğun sayılabilir olsun; $\{B(d, 1/n) : d\in D,\, n\in\mathbb{N}\}$ ailesi sayılabilirdir. Açık $U$ ve $x\in U$ verildiğinde $B(x,\varepsilon)\subseteq U$ al; yoğunlukla $d\in D\cap B(x,\varepsilon/2)$ bulunur ve $1/n<\varepsilon/2$ seçilince $x\in B(d,1/n)\subseteq U$. Demek ki bu sayılabilir aile bir bazdır. ∎

**Teorem 2.4 (Sorgenfrey Karşı Örneği).** Sorgenfrey doğrusu ayrılabilir ve
Lindelöf'tür ama 2. sayılabilir değildir. (Yukarıdaki karşı-örnek kutusuna bakın.)

**Teorem 2.5 (Sayılamaz Ayrık Uzay — İkinci Karşı Örnek).** Sayılamaz bir taşıyıcı
üzerindeki ayrık topoloji **1. sayılabilir**dir ama **ayrılabilir, Lindelöf ve 2.
sayılabilir değildir**.

> **İspat eskizi.** Ayrık uzayda her $\{x\}$ açıktır, dolayısıyla $\{\{x\}\}$ tek
> elemanlı yerel bazdır — 1. sayılabilir. Yoğun bir küme her açığı, özellikle her
> $\{x\}$'i kesmek zorundadır, yani taşıyıcının tamamını içermelidir; taşıyıcı
> sayılamaz olduğundan ayrılabilir değildir. $\{\{x\}\}_{x\in X}$ açık örtüsünün
> hiçbir öz alt-örtüsü yoktur, sayılabilir alt-örtüsü de yoktur — Lindelöf değil.
> Herhangi bir baz her $\{x\}$'i (tek üreteci) içermek zorunda olduğundan sayılamaz
> — 2. sayılabilir değil. Örnek 5.7'de `uncountable_discrete_space()` ile doğrulanır.

![ℚ ⊂ ℝ yoğun sayılabilir alt küme: her açık aralık bir rasyonel içerir, dolayısıyla ℝ ayrılabilirdir](../assets/ch09/fig_ch09_ayrilabilirlik.png)

---
"""

# %% [markdown]
"""
## 3. Algoritmalar
"""

# %% [markdown]
"""
### Sonlu Uzayda Sayılabilirlik

Sonlu uzayda her aksiyom trivially sağlanır.

- Yerel baz boyutu = noktanın komşuluk sistemi boyutu.
- Global baz = topoloji kendisi; sonlu ⟹ sayılabilir.
- Yoğun küme = carrier'ın kendisi.

Algoritma: O(1).
"""

# %% [markdown]
"""
### Sonsuz Uzayda: Tag-Tabanlı Çıkarım

pytop sembolik uzaylarda tag koridorlarından sayılabilirlik çıkarır:
- `'second_countable'` etiketi ⟹ tüm aksiyomlar sağlanır
- `'metric'` ∧ `'separable'` etiketi ⟹ `'second_countable'` çıkarılır

---
"""

# %% [markdown]
"""
## 4. pytop API
"""

# %%
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

# %% [markdown]
"""
Tüm fonksiyonlar `Result` döner: `.status` ('true'/'false'/'unknown').

Ek olarak iki yardımcı vardır:
- `countability_report(space)` → 4 aksiyomu bir `dict[str, Result]` içinde toplar.
- `is_dense_subset(space, subset)` → verilen alt kümenin yoğun olup olmadığını döner
  (ayrılabilirliği somut bir tanıkla gösterir).
"""

# %%
from pytop import countability_report, is_dense_subset

# %% [markdown]
"""
---
"""

# %% [markdown]
"""
## 5. Örnekler
"""

# %% [markdown]
"""
### Örnek 5.1 — Gerçek Doğru: Tüm 4 Aksiyom
"""

# %%
from pytop import real_line_metric
from pytop import is_first_countable, is_second_countable, is_separable, is_lindelof

rl = real_line_metric()
print("1st countable?", is_first_countable(rl).status)
print("2nd countable?", is_second_countable(rl).status)
print("separable?", is_separable(rl).status)
print("lindelof?", is_lindelof(rl).status)

# %% [markdown]
"""
```text
1st countable?  true
2nd countable?  true
separable?      true
lindelof?       true
```

ℝ: {(a,b): a,b∈ℚ} sayılabilir baz; ℚ yoğun alt küme.
"""

# %% [markdown]
"""
### Örnek 5.2 — Kosonlu Doğal Sayılar
"""

# %%
from pytop import naturals_cofinite

nc = naturals_cofinite()
print("1st countable?", is_first_countable(nc).status)
print("2nd countable?", is_second_countable(nc).status)
print("separable?", is_separable(nc).status)
print("lindelof?", is_lindelof(nc).status)

# %% [markdown]
"""
```text
1st countable?  true
2nd countable?  true
separable?      true
lindelof?       true
```
"""

# %% [markdown]
"""
### Örnek 5.3 — Sierpiński Uzayı
"""

# %%
from pytop import sierpinski_space

s = sierpinski_space()
print("1st countable?", is_first_countable(s).status)
print("2nd countable?", is_second_countable(s).status)
print("separable?", is_separable(s).status)

# %% [markdown]
"""
```text
1st countable?  true
2nd countable?  true
separable?      true
```

Sierpiński sonlu: tüm sayılabilirlik aksiyomları trivially sağlanır.
"""

# %% [markdown]
"""
### Örnek 5.4 — Ayrık Topoloji
"""

# %%
from pytop import discrete_topology

d = discrete_topology(1, 2, 3)
print("1st countable?", is_first_countable(d).status)
print("2nd countable?", is_second_countable(d).status)
print("separable?", is_separable(d).status)
print("lindelof?", is_lindelof(d).status)

# %% [markdown]
"""
```text
1st countable?  true
2nd countable?  true
separable?      true
lindelof?       true
```
"""

# %% [markdown]
"""
### Örnek 5.5 — Sorgenfrey Doğrusu: 2nd Countable ✗
"""

# %%
from pytop import sorgenfrey_line_like

sl = sorgenfrey_line_like()
print("1st countable?", is_first_countable(sl).status)
print("2nd countable?", is_second_countable(sl).status)
print("separable?", is_separable(sl).status)
print("lindelof?", is_lindelof(sl).status)

# %% [markdown]
"""
```text
1st countable?   true
2nd countable?   false
separable?       true
lindelof?        true
```

Sorgenfrey: 1. sayılabilir ✓, ayrılabilir ✓, Lindelöf ✓
ama 2. sayılabilir değil — baz boyutu continuum.
"""

# %% [markdown]
"""
### Örnek 5.6 — Toplu Rapor + Yoğunluk Tanığı

`countability_report` dört aksiyomu tek seferde toplar; `is_dense_subset` ise
ayrılabilirliği somut bir küme ile gösterir.
"""

# %%
from pytop import countability_report, is_dense_subset, sorgenfrey_line_like, discrete_topology

sl = sorgenfrey_line_like()
rep = countability_report(sl)
for key in ['first_countable', 'second_countable', 'separable', 'lindelof']:
    print(f"  {key:<17}: {rep[key].status}")

d = discrete_topology(1, 2, 3)
print("dense {1,2,3}?", is_dense_subset(d, {1, 2, 3}).status)
print("dense {1,2}?  ", is_dense_subset(d, {1, 2}).status)

# %% [markdown]
"""
```text
  first_countable  : true
  second_countable : false
  separable        : true
  lindelof         : true
dense {1,2,3}? true
dense {1,2}?   false
```

Ayrık `{1,2,3}`'te `{1,2}` yoğun değildir: `{3}` açığını kesmez. Tüm taşıyıcı
ise her açığı kestiği için yoğundur — sonlu ayrık uzayın yoğun olabilen tek
sayılabilir kümesi taşıyıcının kendisidir.
"""

# %% [markdown]
"""
### Örnek 5.7 — Sayılamaz Ayrık Uzay: İkinci Karşı Örnek

Sorgenfrey "1. var, 2. yok"un kanonik örneğidir; sayılamaz ayrık uzay ise
"1. sayılabilir tek başına ayrılabilirlik/Lindelöf'ü getirmez"i gösterir.
"""

# %%
from pytop import uncountable_discrete_space
from pytop import is_first_countable, is_second_countable, is_separable, is_lindelof

u = uncountable_discrete_space()
print("1st countable?", is_first_countable(u).status)
print("2nd countable?", is_second_countable(u).status)
print("separable?    ", is_separable(u).status)
print("lindelof?     ", is_lindelof(u).status)

# %% [markdown]
"""
```text
1st countable? true
2nd countable? false
separable?     false
lindelof?      false
```

Her tekil `{x}` açık olduğundan yerel baz tek elemanlıdır (1. sayılabilir),
ama `{{x}}` örtüsünün sayılabilir alt-örtüsü ve yoğun sayılabilir alt kümesi
yoktur. Sorgenfrey ile birleştirildiğinde: 1. sayılabilirlik, ne 2.
sayılabilirliği ne de ayrılabilirlik/Lindelöf'ü tek başına gerektirir.

---
"""

# %% [markdown]
"""
## 6. Alıştırmalar
"""

# %% [markdown]
"""
### Kodlama

K1. `finite_chain_space(5)` üzerinde `is_first_countable` ve `is_second_countable`
    hesaplayın.

K2. `two_point_discrete_space()` ve `two_point_indiscrete_space()` üzerinde
    `is_separable` karşılaştırın.

K3. `integers_discrete()` (sayılabilir ayrık) için 2nd countable mi yoksa değil mi?

K4. `uncountable_discrete_space()` üzerinde dört aksiyomu `countability_report` ile
    hesaplayın ve `integers_discrete()` ile karşılaştırın. Hangi aksiyom(lar)da
    ayrışıyorlar ve neden? (İpucu: fark, taşıyıcının sayılabilir olup olmamasında.)
"""

# %% [markdown]
"""
### Teori

T1. 2nd countable ⟹ separable olduğunu ispatlayın.
    (İpucu: her baz elemanından bir nokta seç.)

T2. Sorgenfrey doğrusunun 2. sayılabilir olmadığını nasıl gösterirsiniz?
    (Hint: alt intervaller [a,b) baz oluşturur ama uncountable.)

T3. "1. sayılabilir ⟹ ayrılabilir" çıkarımının yanlış olduğunu bir karşı-örnekle
    gösterin. (İpucu: sayılamaz ayrık uzay; yoğun bir küme her `{x}`'i kesmek
    zorundadır.)
"""
