# Çözümler

## Bölüm 15: Metrik Tamlık

### K1 — Rasyoneller ℚ tam mı?

(ch15 K1 alıştırmasına dön)

```python
from pytop import rationals_metric
from pytop.metric_completeness import is_complete

qm = rationals_metric()
print("status:", is_complete(qm).status)
print("not_complete tag:", 'not_complete' in qm.tags)
```

```
status: unknown
not_complete tag: True
```

`rationals_metric()` sembolik (sonsuz) bir uzaydır. `is_complete` yalnızca
**açık sonlu** metrik uzaylarda exact karar verir; ℚ için sonucu dürüstçe
`unknown` bırakır. Ama küratörlü `tags` kümesi √2'ye yakınsayan Cauchy
dizisinin limit bulamamasını `'not_complete'` etiketiyle kayıt altına alır.

---

### K2 — 4-noktalı metrik uzay + metric_compactness_check

(ch15 K2 alıştırmasına dön)

```python
from pytop.metric_spaces import FiniteMetricSpace
from pytop.metric_completeness import metric_compactness_check

pts = ('p', 'q', 'r', 's')
dist = {(a, b): (0 if a == b else 1) for a in pts for b in pts}
fms = FiniteMetricSpace(carrier=pts, distance=dist)

mc = metric_compactness_check(fms)
print("compact:", mc.status, mc.value)
```

```
compact: true True
```

Ayrık (discrete) 4-noktalı metrik: her Cauchy dizisi eninde sonunda sabit
olduğundan **tam**, taşıyıcının kendisi her ε için ε-net olduğundan **tamamen
sınırlı**. İkisi birden ⟹ kompakt.

---

### K3 — analyze_metric_completeness value sözlüğü

(ch15 K3 alıştırmasına dön)

```python
from pytop.metric_spaces import FiniteMetricSpace
from pytop.metric_completeness import analyze_metric_completeness

pts = ('p', 'q', 'r', 's')
dist = {(a, b): (0 if a == b else 1) for a in pts for b in pts}
fms = FiniteMetricSpace(carrier=pts, distance=dist)

r = analyze_metric_completeness(fms)
print("value:", r.value)
```

```
value: {'is_complete': True, 'is_totally_bounded': True, 'metric_compact': True}
```

`analyze_metric_completeness` üç bağımsız kararı tek sözlükte toplar:
tamlık, tamamen sınırlılık ve bunların kesişimi olan metrik kompaktlık. Sonlu
uzayda her üçü de `True`.

---

### K4 — Statü unknown, etiket True neden?

(ch15 K4 alıştırmasına dön)

```python
from pytop import rationals_metric
from pytop.metric_completeness import is_complete

qm = rationals_metric()
print("status:", is_complete(qm).status)
print("not_complete tag:", 'not_complete' in qm.tags)
```

```
status: unknown
not_complete tag: True
```

İki sonuç çelişmez; iki ayrı bilgi katmanıdır. **Statü** kütüphanenin *kanıtla
karar verebildiği* şeydir: sembolik ℚ'da açık kümeleri tarayarak tamlık ispatı
mümkün olmadığından `unknown`. **Etiket** ise küratörlü bir gerçektir: ℚ'nun
tam olmadığı matematiksel olarak bilinir ve `'not_complete'` olarak işaretlenir.
Kütüphane "bilmiyorum" derken yalan söylemez; biliniyor olan gerçeği ayrı bir
kanalda taşır.

---

### K5 — Kararlı (stable) profilin key alanı

(ch15 K5 alıştırmasına dön)

```python
from pytop import get_fixed_point_profiles

stable = [p.key for p in get_fixed_point_profiles() if p.stability == 'stable']
print("stable keys:", stable)
```

```
stable keys: ['attracting_fixed_point']
```

Tek kararlı profil `attracting_fixed_point`'tir ve doğrudan **Banach büzülme
teoremine** karşılık gelir: büzülme bir komşulukta tüm yörüngeleri sabit
noktaya çeker (`fⁿ(x) → x₀`), yani sabit nokta çekicidir.

---

### T1 — Banach sabit-nokta teoremi (sözlü)

(ch15 T1 alıştırmasına dön)

Tam bir (M, d) uzayında, mesafeleri sabit bir K < 1 oranıyla küçülten her
T: M → M dönüşümünün **tek** bir sabit noktası vardır. Sezgi: T her uygulamada
her şeyi en az K kat birbirine yaklaştırır; bu yüzden herhangi bir x_0'dan
başlayan x_{n+1} = T(x_n) yörüngesi giderek sıkışır (Cauchy olur) ve tamlık
sayesinde tek bir noktaya çöker.

**Uygulama:** Picard–Lindelöf teoremi. y' = f(t, y), y(t_0) = y_0 başlangıç-değer
probleminin çözümü, integral operatörü
(Ty)(t) = y_0 + ∫_{t_0}^{t} f(s, y(s)) ds biçiminde bir büzülme olarak yazılır;
yeterince küçük aralıkta K < 1 olur ve Banach teoremi çözümün varlığını ve
tekliğini garanti eder.

---

### T2 — [0,1] tam, (0,1) tam değil

(ch15 T2 alıştırmasına dön)

**[0,1] tamdır.** ℝ tam bir metrik uzaydır ve [0,1] ⊆ ℝ **kapalıdır**. "Tam
uzayın kapalı alt-uzayı tamdır" teoremi gereği [0,1] tamdır: [0,1] içindeki her
Cauchy dizisi ℝ'de bir limite yakınsar, limit kapalılık nedeniyle [0,1]'de kalır.

**(0,1) tam değildir.** x_n = 1/(n+1) dizisini düşünün: tüm terimler (0,1) içinde
ve dizi Cauchy'dir (`d(x_m, x_n) → 0`). Limiti 0'dır, fakat 0 ∉ (0,1). Dolayısıyla
(0,1) içinde yakınsamayan bir Cauchy dizisi vardır: (0,1) tam değildir. Aynı dizi,
biri tam diğeri değil olduğundan, tamlığın **topolojik** değil **metrik** bir
özellik olduğunu gösterir — (0,1) ile ℝ homeomorftur.

---

### T3 — Tam uzayın kapalı alt-uzayı tamdır

(ch15 T3 alıştırmasına dön)

**İspat.** (M, d) tam, A ⊆ M kapalı olsun. {a_n} ⊆ A herhangi bir Cauchy dizisi
olsun. {a_n} M içinde de Cauchy'dir; M tam olduğundan bir a ∈ M limitine
yakınsar. A kapalı olduğundan kendi limit noktalarını içerir, dolayısıyla a ∈ A.
Böylece A içindeki her Cauchy dizisi A içinde bir limite yakınsar: A tamdır. ∎

**Açık alt-uzay için karşı-örnek.** ℝ tamdır; (0,1) ⊆ ℝ **açıktır** ama tam
değildir (bkz. T2: 1/(n+1) dizisi). Demek ki "açık alt-uzay" için benzer bir
teorem **yoktur**; tamlığı miras aldıran şey kapalılıktır, açıklık değil.

---

### T4 — ℚ tam değil + tamlama

(ch15 T4 alıştırmasına dön)

**Cauchy ama limitsiz.** x_1 = 1, x_2 = 1.4, x_3 = 1.41, x_4 = 1.414, ... dizisi
√2'nin ondalık açılımıdır. Her x_n rasyoneldir. m < n için
`|x_m − x_n| < 10^{−(m−1)}` olduğundan dizi Cauchy'dir. ℝ'de limit √2'dir; ama
√2 irrasyoneldir, yani √2 ∉ ℚ. Demek ki bu Cauchy dizisinin ℚ içinde **limiti
yoktur**: ℚ tam değildir.

**Tamlama.** Tamlama inşası, ℚ'daki Cauchy dizilerini denklik sınıflarına ayırıp
(iki dizi "aynı limite gidiyorsa" denk) bu sınıfları yeni noktalar olarak ekler.
Yukarıdaki dizinin sınıfı tam olarak √2 noktasını verir. Tüm bu boşlukları
doldurunca elde edilen tam uzay ℝ = ℚ̂'dir: ℚ, ℝ'de yoğundur ve ℝ'de her Cauchy
dizisi yakınsar.
