# Alıştırma Çözümleri

Bu ek, Bölüm 4 ve Bölüm 6 alıştırmalarının tam çözümlerini içerir. Kodlama
çözümlerindeki tüm çıktılar gerçek çalıştırmadan alınmıştır; teori çözümleri tam
argüman verir.

---

## Bölüm 4: Topolojik Uzaylar

### K1 — cofinite_topology keşfi

(ch04 K1 alıştırmasına dön)

```python
from pytop import cofinite_topology, is_t1, is_t2

c = cofinite_topology('a', 'b', 'c')
print("|tau| =", len(c.topology))
print("Etiketler:", sorted(c.tags))
print("T1:", is_t1(c).status, "| T2:", is_t2(c).status)
```

```
|tau| = 8
Etiketler: ['cofinite', 'compact', 'finite', 't1']
T1: true | T2: true
```

Üç elemanlı kümede tüm alt kümeler kosonlu koşulunu sağlar; `|tau| = 2^3 = 8`:
topoloji ayrıktır. Sonlu kümede T1 => tekiller kapalı => her alt küme kapalı =>
her alt küme açık; T1 olan sonlu uzay zorunlu olarak ayrık, dolayısıyla
Hausdorff'tur. T1 olup T2 olmayan örnek için taşıyıcı sonsuz olmalıdır: kosonlu
N'de boş olmayan iki açık daima kesişir.

---

### K2 — topology_from_subbasis keşfi

(ch04 K2 alıştırmasına dön)

```python
from pytop import topology_from_subbasis

s = topology_from_subbasis({1, 2, 3, 4}, [{1, 2}, {3, 4}, {2, 3}])
print("|tau| =", len(s.topology))
print("Acik kumeler:", sorted(sorted(t) for t in s.topology))
```

```
|tau| = 9
Acik kumeler: [[], [1, 2], [1, 2, 3], [1, 2, 3, 4], [2], [2, 3], [2, 3, 4], [3], [3, 4]]
```

Alt-baz çiftlerinin kesişimleri `{2}`, `{3}`, `∅` yeni baz elemanları üretir;
birleşimler `{1,2,3}`, `{2,3,4}` ve `X`'i ekler. Toplam 9 açık küme. Alt-baz bir
topoloji üretmek için yeterlidir: önce sonlu kesişimler altında kapatılır, sonra
keyfi birleşimler altında kapatılır.

---

### K3 — finite_chain_space(5) keşfi

(ch04 K3 alıştırmasına dön)

```python
from pytop import finite_chain_space

c5 = finite_chain_space(5)
print("|tau| =", len(c5.topology))
print("Acik kumeler:", sorted(sorted(t) for t in c5.topology))
```

```
|tau| = 6
Acik kumeler: [[], [1], [1, 2], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 5]]
```

Açıklar 6 önektir. "En açık" nokta 1'dir: tek elemanlı `{1}` açığında ve
dolayısıyla her boş olmayan açıkta yer alır; 5 ise yalnızca `X`'tedir.

---

### T1 — {1,2,3} üzerinde kaç topoloji?

(ch04 T1 alıştırmasına dön)

`X = {1,2,3}` üzerinde tam olarak **29** farklı topoloji vardır (homeomorfizma
sınıfı olarak 9). Doğrudan yöntem `P(P(X))`'in `2^8 = 256` elemanlı aday
ailesinin her birinde üç aksiyomu denetlemeyi gerektirir. Baz teoremi işi tersine
çevirir: (B1)–(B2)'yi sağlayan küçük aileler seçilir, her biri otomatik olarak
geçerli bir topoloji üretir; yalnız üretilen topolojilerin tekrarları ayıklanır.
Aksiyom denetimi aday başına yapılmaz — üretim doğruluğu Baz Teoremi'nce
garantilidir.

---

### T2 — Ayrık en ince, indirgenmiş en kabadır

(ch04 T2 alıştırmasına dön)

**Ayrık en incedir:** Herhangi bir `tau` topolojisi tanım gereği
`tau ⊆ P(X) = tau_disc` sağlar; hiçbir aksiyoma gerek yoktur, "topoloji X'in alt
kümelerinden oluşur" tanımı yeter. **İndirgenmiş en kabadır:** (T1) aksiyomu her
topolojinin `∅` ve `X`'i içermesini zorunlu kılar;
`tau_ind = {∅, X} ⊆ tau`. Kullanılan tek aksiyom (T1)'dir. ∎

---

## Bölüm 6: Ayrılma Aksiyomları

### K1 — make_topology ayrılma zinciri

(ch06 K1 alıştırmasına dön)

```python
from pytop import make_topology, separation_chain

k = make_topology({1, 2, 3}, {1}, {2}, {1, 2})
print("Acik kumeler:", sorted(sorted(t) for t in k.topology))
for prop, r in separation_chain(k).items():
    print(f"  {prop:20s}: {r.status}")
```

```
Acik kumeler: [[], [1], [1, 2], [1, 2, 3], [2]]
  t0                  : true
  t1                  : false
  hausdorff           : false
  urysohn             : false
  t3                  : false
  tychonoff           : unknown
  t4                  : false
  completely_normal   : false
  perfectly_normal    : false
```

T0 sağlanır: `(1,2)` çiftini `{1}`, `(1,3)` çiftini `{1}`, `(2,3)` çiftini `{2}`
ayırır. T1 düşer: 3'ü içerip 1'i dışlayan açık yoktur (3 yalnız `X`'te).
`tychonoff: unknown` — sürekli fonksiyon ayırması açık-küme taramasıyla karara
bağlanmaz; kütüphane dürüstçe "bilinmiyor" der.

---

### K2 — finite_chain_space(3) en yüksek aksiyom

(ch06 K2 alıştırmasına dön)

```python
from pytop import finite_chain_space, separation_chain

for prop, r in separation_chain(finite_chain_space(3)).items():
    print(f"  {prop:20s}: {r.status}")
```

```
  t0                  : true
  t1                  : false
  hausdorff           : false
  urysohn             : false
  t3                  : false
  tychonoff           : unknown
  t4                  : false
  completely_normal   : false
  perfectly_normal    : false
```

En yüksek sağlanan aksiyom **T0**'dır. Önek yapısı her çifti "daha solda olan"
lehine ayırır: `(1,2)` için `{1}`, `(2,3)` için `{1,2}`. T1 imkânsızdır: 2'yi
içerip 1'i dışlayan önek yoktur.

---

### K3 — two_point_indiscrete_space T0/T1/T2

(ch06 K3 alıştırmasına dön)

```python
from pytop import two_point_indiscrete_space, is_t0, is_t1, is_t2

tp = two_point_indiscrete_space()
print("T0:", is_t0(tp).status, "| T1:", is_t1(tp).status, "| T2:", is_t2(tp).status)
```

```
T0: false | T1: false | T2: false
```

Boş olmayan tek açık `X`'tir ve her iki noktayı da içerir; hiçbir çift hiçbir
yönden ayrılamaz. Zincirin tamamı en alt basamakta düşer.

---

### T1 — T2 => T1 => T0

(ch06 T1 alıştırmasına dön)

**T2 => T1:** `x ≠ y` verilsin. T2 ile ayrık `U ∋ x`, `V ∋ y` açıkları vardır.
`U ∩ V = ∅` olduğundan `y ∉ U` ve `x ∉ V`: hem "x'i içerip y'yi dışlayan" hem
"y'yi içerip x'i dışlayan" açık bulundu — T1'in iki yönlü koşulu sağlandı.
**T1 => T0:** T0 yalnız en az bir yönlü ayrım ister; T1'in verdiği iki yönlü
ayrımın herhangi biri yeter. ∎

---

### T2 — Sonlu T1 ⟺ Ayrık

(ch06 T2 alıştırmasına dön)

**(=>)** `X` sonlu ve T1 olsun. T1 gereği her `x` için ve her `y ≠ x` için
`y ∈ U_y`, `x ∉ U_y` olan açık `U_y` vardır; `X \ {x} = ⋃_{y≠x} U_y` açıktır,
yani `{x}` kapalıdır. Herhangi `A ⊆ X`, sonlu sayıda tekilin birleşimi olarak
kapalıdır; o halde tümleyeni `X \ A` açıktır. `A` keyfi olduğundan her alt küme
açıktır: topoloji ayrıktır.

**(<=)** Ayrık topolojide her `{x}` açıktır; `x ≠ y` için `{x}` ve `{y}` iki
yönlü ayrımı doğrudan verir, T1 (hatta T2) sağlanır. ∎
