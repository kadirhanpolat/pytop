## Bölüm 9: Sayılabilirlik

Bu bölüm, Bölüm 9 (Sayılabilirlik Aksiyomları) alıştırmalarının tam çözümlerini
içerir. Kodlama çözümlerindeki tüm çıktılar gerçek çalıştırmadan alınmıştır; teori
çözümleri tam argüman verir.

---

### K1 — finite_chain_space(5): 1. ve 2. sayılabilir

(ch09 K1 alıştırmasına dön)

```python
from pytop import finite_chain_space, is_first_countable, is_second_countable

c = finite_chain_space(5)
print("1st countable?", is_first_countable(c).status)
print("2nd countable?", is_second_countable(c).status)
```

```
1st countable? true
2nd countable? true
```

Sonlu uzayda topolojinin kendisi sonlu, dolayısıyla sayılabilir bir bazdır; her
nokta için komşuluk sistemi de sonludur. Bu yüzden her sonlu uzay hem 1. hem 2.
sayılabilirdir — sayılabilirlik aksiyomları yalnızca sonsuz uzaylarda ayırt edicidir.

---

### K2 — İki noktalı ayrık ve indirgenmiş: ayrılabilirlik

(ch09 K2 alıştırmasına dön)

```python
from pytop import two_point_discrete_space, two_point_indiscrete_space, is_separable

print("disc sep  ", is_separable(two_point_discrete_space()).status)
print("indisc sep", is_separable(two_point_indiscrete_space()).status)
```

```
disc sep   true
indisc sep true
```

İkisi de ayrılabilirdir, ama nedenleri farklıdır. Ayrık `{a,b}`'de yoğun küme her
açığı (`{a}` ve `{b}` dâhil) kesmek zorunda olduğundan taşıyıcının tamamı `{a,b}`
gerekir — sonlu olduğundan sayılabilir, dolayısıyla ayrılabilir. İndirgenmiş
`{a,b}`'de açıklar yalnız `∅` ve `X` olduğundan tek noktalı `{a}` bile yoğundur:
`X`'i keser. Ayrılabilirlik "sayılabilir yoğun küme var mı?" sorusudur; sonlu
uzayda yanıt her zaman evettir.

---

### K3 — integers_discrete(): sayılabilir ayrık 2. sayılabilirdir

(ch09 K3 alıştırmasına dön)

```python
from pytop import integers_discrete, is_second_countable

print("2nd countable?", is_second_countable(integers_discrete()).status)
```

```
2nd countable? true
```

Sayılabilir ayrık uzayda `{ {n} : n ∈ ℤ }` ailesi bir bazdır; ℤ sayılabilir
olduğundan bu baz da sayılabilirdir — uzay 2. sayılabilirdir. **Kritik nokta**
taşıyıcının sayılabilirliğidir: ayrık topolojide baz tüm tekilleri içermek
zorundadır, dolayısıyla baz büyüklüğü en az taşıyıcının büyüklüğüdür. Taşıyıcı
sayılabilirse 2. sayılabilir; sayılamazsa değil (bkz. K4).

---

### K4 — Sayılamaz ayrık vs sayılabilir ayrık

(ch09 K4 alıştırmasına dön)

```python
from pytop import (integers_discrete, uncountable_discrete_space,
                   countability_report)

print("integers_discrete:")
for k, v in countability_report(integers_discrete()).items():
    print(f"  {k:<17}: {v.status}")
print("uncountable_discrete:")
for k, v in countability_report(uncountable_discrete_space()).items():
    print(f"  {k:<17}: {v.status}")
```

```
integers_discrete:
  first_countable  : true
  second_countable : true
  separable        : true
  lindelof         : true
uncountable_discrete:
  first_countable  : true
  second_countable : false
  separable        : false
  lindelof         : false
```

Her ikisi de **1. sayılabilir**dir: ayrık uzayda her nokta için `{ {x} }` tek
elemanlı yerel bazdır, taşıyıcının büyüklüğünden bağımsız. **2. sayılabilir,
ayrılabilir ve Lindelöf** aksiyomlarında ise ayrışırlar. Üçü de "sayılabilir bir
küme tüm noktalara erişebilir mi?" sorusunun farklı yüzleridir: ayrık topolojide
bir baz tüm tekilleri, yoğun bir küme tüm noktaları, bir alt-örtü yine tüm
tekilleri içermek zorundadır. Taşıyıcı sayılabilirse hepsi mümkün, sayılamazsa
hiçbiri. Ayrım kaynağı tek başına **taşıyıcının kardinalitesi**dir.

---

### T1 — 2. sayılabilir ⟹ ayrılabilir

(ch09 T1 alıştırmasına dön)

`{B_n}` sayılabilir bir baz olsun. Her boş olmayan `B_n`'den bir nokta `d_n ∈ B_n`
seç (seçim aksiyomu sayılabilir aile için yeterli). `D = { d_n : B_n ≠ ∅ }` kümesi
sayılabilirdir, çünkü indeks kümesi `ℕ`'nin bir alt kümesidir.

`D`'nin yoğun olduğunu gösterelim: boş olmayan herhangi açık `U` alalım ve `x ∈ U`
olsun. Baz tanımı gereği `x ∈ B_n ⊆ U` olan bir `B_n` vardır. Bu `B_n` boş
değildir (en az `x` içerir), dolayısıyla `d_n ∈ B_n ⊆ U`. Demek ki `d_n ∈ U ∩ D`,
yani `U ∩ D ≠ ∅`. Boş olmayan her açık `D`'yi kestiğinden `D` yoğundur. `D`
sayılabilir olduğundan uzay ayrılabilirdir. ∎

---

### T2 — Sorgenfrey doğrusu 2. sayılabilir değildir

(ch09 T2 alıştırmasına dön)

Sorgenfrey doğrusu `ℝ_ℓ`, `[a,b)` biçimli yarı-açık aralıklarla üretilir. `{B_n}`
herhangi bir baz olsun ve bir `x ∈ ℝ` sabitleyelim. `[x, x+1)` açıktır ve `x`'i
içerir; baz tanımı gereği `x ∈ B_n ⊆ [x, x+1)` olan bir baz elemanı `B(x) := B_n`
vardır. Bu eleman `x`'i içerip `x`'in solundaki hiçbir noktayı içermez, yani
`inf B(x) = x`'tir.

Şimdi `x ↦ B(x)` eşlemesi **birebir**dir: `x < y` ise `inf B(x) = x ≠ y = inf B(y)`,
dolayısıyla `B(x) ≠ B(y)`. Demek ki baz, sayılamaz `ℝ` kümesinden bazına giden bir
injeksiyon barındırır; baz en az `|ℝ| = 𝔠` büyüklüktedir — sayılamaz. Hiçbir
sayılabilir baz olamayacağından `ℝ_ℓ` 2. sayılabilir değildir. (Buna karşılık `ℚ`
yoğun olduğundan ayrılabilir, ve uzay Lindelöf'tür — Teorem 2.4.) ∎

---

### T3 — "1. sayılabilir ⟹ ayrılabilir" yanlıştır

(ch09 T3 alıştırmasına dön)

Karşı-örnek: **sayılamaz bir kümede ayrık topoloji** (örn. `ℝ` üzerinde ayrık
topoloji, `uncountable_discrete_space()`).

**1. sayılabilir:** Her `x` için `{ {x} }` tek elemanlı bir yerel bazdır, çünkü `{x}`
açıktır ve `x`'in en küçük komşuluğudur. Sayılabilirlik (hatta sonluluk) sağlanır.

**Ayrılabilir değil:** `D ⊆ X` yoğun olsun. Her `x ∈ X` için `{x}` açık ve boş
olmadığından `D` onu kesmelidir: `x ∈ D`. Bu her `x` için geçerli olduğundan
`D = X`. Ama `X` sayılamaz olduğundan `D` de sayılamaz; sayılabilir yoğun küme
yoktur. Dolayısıyla uzay ayrılabilir değildir.

Sonuç: uzay 1. sayılabilir ama ayrılabilir değil; "1. sayılabilir ⟹ ayrılabilir"
çıkarımı yanlıştır. (Doğru implikasyon yönü 2. sayılabilirden gelir: 2. sayılabilir
⟹ ayrılabilir, T1.) ∎
