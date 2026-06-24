# Bölüm 16: Metrik Dönüşümler

Bu ek, Bölüm 16 (Metrik Fonksiyonlar ve Sözleşmeler) alıştırmalarının tam
çözümlerini içerir. Kodlama çözümlerindeki tüm çıktılar gerçek çalıştırmadan
alınmıştır; teori çözümleri tam argüman verir.

---

### K1 — Ayrık metrikte döngü permütasyonu

(ch16 K1 alıştırmasına dön)

```python
from pytop.metric_spaces import FiniteMetricSpace
from pytop.metric_map_taxonomy import classify_finite_metric_map

pts = [1, 2, 3]
d_disc = {(a, b): (0 if a == b else 1) for a in pts for b in pts}
M = FiniteMetricSpace(carrier=tuple(pts), distance=d_disc)

f_cycle = {1: 2, 2: 3, 3: 1}
p = classify_finite_metric_map(M, M, f_cycle)
print("isometry:", p.isometry)
print("bijective:", p.bijective)
print("homeomorphism:", p.homeomorphism)
print("lipschitz_constant:", p.lipschitz_constant)
```

```text
isometry: True
bijective: True
homeomorphism: True
lipschitz_constant: 1.0
```

Ayrık metrikte farklı iki nokta arası mesafe daima 1'dir. Döngü bir
permütasyon (bijeksiyon) olduğundan her çifti yine farklı bir çifte gönderir;
mesafe 1 → 1 korunur. Demek ki döngü bir izometridir (K=1) ve bijektif izometri
olarak Teorem 2.1 gereği bir homeomorfizmadır.

---

### K2 — Öklid metrikte kaydırma fonksiyonu

(ch16 K2 alıştırmasına dön)

```python
from pytop.metric_spaces import FiniteMetricSpace
from pytop.metric_map_taxonomy import classify_finite_metric_map

pts = [0, 1, 2, 3, 4]
d_eucl = {(a, b): abs(a - b) for a in pts for b in pts}
M = FiniteMetricSpace(carrier=tuple(pts), distance=d_eucl)

# x+1, fakat tasiyiciyi asmamak icin 4'te durur
f_shift = {0: 1, 1: 2, 2: 3, 3: 4, 4: 4}
p = classify_finite_metric_map(M, M, f_shift)
print("lipschitz_constant:", p.lipschitz_constant)
print("isometry:", p.isometry)
print("bijective:", p.bijective)
```

```text
lipschitz_constant: 1.0
isometry: False
bijective: False
```

Kaydırma sınırlı bir taşıyıcıda kalmak için 4'te doyduğundan 3 ve 4 aynı
görüntüye (4) gider: bijektif değildir ve izometri değildir (mesafe 1 olan (3,4)
çifti mesafe 0'a iner). Yine de hiçbir çiftte mesafe büyümediği için Lipschitz
sabiti K=1'dir (genişlemez). Saf bir öteleme (taşma olmadan) tam izometri,
K=1 verirdi.

---

### K3 — Sabit fonksiyon: K = 0

(ch16 K3 alıştırmasına dön)

```python
from pytop.metric_spaces import FiniteMetricSpace
from pytop.metric_map_taxonomy import classify_finite_metric_map

pts = [1, 2, 3, 4]
d_disc = {(a, b): (0 if a == b else 1) for a in pts for b in pts}
M = FiniteMetricSpace(carrier=tuple(pts), distance=d_disc)

f_const = {1: 1, 2: 1, 3: 1, 4: 1}
p = classify_finite_metric_map(M, M, f_const)
print("lipschitz_constant:", p.lipschitz_constant)
print("non_expansive:", p.non_expansive)
print("bijective:", p.bijective)
```

```text
lipschitz_constant: 0.0
non_expansive: True
bijective: False
```

Sabit fonksiyon tüm noktaları tek bir görüntüye gönderir: her çiftte
d₂(f(x),f(y))=0 olduğundan oran daima 0, dolayısıyla K=0 (mümkün en küçük
Lipschitz sabiti). Genişlemezdir (0 ≤ d₁), ama açıkça bijektif değildir.

---

### K4 — Büzülme f(x) = x/2: K < 1

(ch16 K4 alıştırmasına dön)

```python
from pytop.metric_spaces import FiniteMetricSpace
from pytop.metric_map_taxonomy import classify_finite_metric_map

src = [0, 2, 4, 6]
img = [0, 1, 2, 3]
d_src = {(a, b): abs(a - b) for a in src for b in src}
d_img = {(a, b): abs(a - b) for a in img for b in img}
M_src = FiniteMetricSpace(carrier=tuple(src), distance=d_src)
M_img = FiniteMetricSpace(carrier=tuple(img), distance=d_img)

f_half = {0: 0, 2: 1, 4: 2, 6: 3}
p = classify_finite_metric_map(M_src, M_img, f_half)
print("lipschitz_constant:", p.lipschitz_constant)
print("similarity_ratio:", p.similarity_ratio)
print("non_expansive:", p.non_expansive)
```

```text
lipschitz_constant: 0.5
similarity_ratio: 0.5
non_expansive: True
```

Her mesafe tam yarıya indiğinden oran tüm çiftlerde sabit 0.5: bu hem bir
büzülmedir (K=0.5 < 1) hem de oranı c=0.5 olan bir benzerliktir. K<1 koşulu
sağlanır; tam bir metrik uzayda Banach teoremi böyle bir eşlemenin eşsiz sabit
noktasını garanti ederdi.

---

### K5 — Aynı döngü, iki farklı metrik

(ch16 K5 alıştırmasına dön)

```python
from pytop.metric_spaces import FiniteMetricSpace
from pytop.metric_map_taxonomy import classify_finite_metric_map

pts = [1, 2, 3]
cyc = {1: 2, 2: 3, 3: 1}

d_disc = {(a, b): (0 if a == b else 1) for a in pts for b in pts}
d_eucl = {(a, b): abs(a - b) for a in pts for b in pts}
M_disc = FiniteMetricSpace(carrier=tuple(pts), distance=d_disc)
M_eucl = FiniteMetricSpace(carrier=tuple(pts), distance=d_eucl)

p_disc = classify_finite_metric_map(M_disc, M_disc, cyc)
p_eucl = classify_finite_metric_map(M_eucl, M_eucl, cyc)
print("discrete isometry:", p_disc.isometry)
print("euclid isometry:", p_eucl.isometry)
print("euclid lipschitz_constant:", p_eucl.lipschitz_constant)
```

```text
discrete isometry: True
euclid isometry: False
euclid lipschitz_constant: 2.0
```

Metrik, izometri olup olmamayı belirler. Ayrık metrikte her permütasyon
izometridir (mesafe daima 1). Öklid metrikte ise döngü 3→1 eşlemesinde mesafe
|2−3|=1 olan komşu çifti |3−1|=2 olan çifte taşır: mesafe korunmaz, izometri
değildir ve Lipschitz sabiti 2'ye çıkar. Aynı soyut permütasyonun "rijit"
olup olmaması taşıyıcının üzerindeki metriğe bağlıdır.

---

### T1 — İzometri ⟹ genişlemez ⟹ Lipschitz (K=1)

(ch16 T1 alıştırmasına dön)

**İddia.** Her izometri genişlemez, her genişlemez fonksiyon K=1 ile Lipschitz'tir.

**İspat.** f izometri olsun: tüm x,y için d₂(f(x),f(y)) = d₁(x,y).

1. **İzometri ⟹ genişlemez.** Eşitlik özel bir ≤ durumudur:
   d₂(f(x),f(y)) = d₁(x,y) ≤ d₁(x,y). Tanım gereği f genişlemezdir
   (non-expansive).

2. **Genişlemez ⟹ Lipschitz (K=1).** g genişlemez olsun:
   d₂(g(x),g(y)) ≤ d₁(x,y) = 1·d₁(x,y). Bu tam olarak K=1 sabitli Lipschitz
   koşuludur. Lipschitz sabiti, oranların supremumu olduğundan, izometride
   her oran tam 1'dir: K = sup 1 = 1.

Böylece zincir İzometri ⟹ Genişlemez ⟹ Lipschitz (K=1) kurulur. (Tersi yanlıştır:
K=1 Lipschitz ama izometri olmayan eşleme vardır — örn. K4'teki taşan kaydırma
genişlemez/K=1 ama izometri değil.) ∎

---

### T2 — Lipschitz ⟹ üniform sürekli (δ = ε/K)

(ch16 T2 alıştırmasına dön)

**İddia.** Sabiti K>0 olan her Lipschitz fonksiyon düzgün (üniform) süreklidir.

**İspat.** f Lipschitz olsun: tüm x,y için d₂(f(x),f(y)) ≤ K·d₁(x,y).
Verilen herhangi bir ε>0 için **δ = ε/K** seçelim (bu seçim yalnızca ε ve K'ye
bağlı; herhangi bir x noktasına bağlı değil). d₁(x,y) < δ olduğunda:

    d₂(f(x),f(y)) ≤ K·d₁(x,y) < K·δ = K·(ε/K) = ε.

δ noktadan bağımsız seçildiği için bu, düzgün süreklilik tanımının ta kendisidir.
(K=0 sabit fonksiyon durumunda f sabittir ve trivially düzgün süreklidir; δ keyfi
alınabilir.) Düzgün süreklilik her noktada sıradan sürekliliği de içerdiğinden
f süreklidir. ∎

---

### T3 — İzometri injektiftir; sabit fonksiyon izometri olamaz

(ch16 T3 alıştırmasına dön)

**İddia.** Her izometri injektiftir; iki noktadan fazla içeren bir uzayda sabit
bir fonksiyon izometri olamaz.

**İspat (injektiflik).** f izometri ve f(x) = f(y) olsun. İzometri eşitliğinden:

    d₁(x,y) = d₂(f(x),f(y)) = d₂(f(x),f(x)) = 0.

Metriğin ayırma aksiyomu (d(a,b)=0 ⟺ a=b) gereği d₁(x,y)=0 ⟹ x=y. Dolayısıyla
f farklı noktaları farklı noktalara gönderir: injektiftir.

**Sabit fonksiyon neden izometri olamaz.** En az iki farklı noktası (x≠y) olan
bir uzayda sabit fonksiyon c, x ve y'yi aynı görüntüye gönderir: f(x)=f(y).
İzometri olsaydı injektif olması gerekirdi (yukarıdaki argüman), x≠y ile çelişir.
Doğrudan da görülür: d₁(x,y) > 0 iken d₂(f(x),f(y)) = 0, mesafe korunmaz. Bu
yüzden sabit fonksiyon (tek noktalı uzaylar dışında) asla izometri değildir —
Örnek 5.3'te lipschitz_constant=0 ama isometry=False çıkması bunun sayısal
doğrulamasıdır. ∎
