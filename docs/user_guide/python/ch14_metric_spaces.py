# %% [markdown]
"""
# Bölüm 14 — Metrik Uzaylar

Metrik uzaylar, mesafe fonksiyonuna dayanan topolojik yapılardır. Her metrik uzay
doğal olarak bir topolojik uzay oluşturur; bu yapı "indüklenen topoloji" olarak adlandırılır.

---
"""

# %% [markdown]
"""
## 1. Konu
"""

# %% [markdown]
"""
### 1.0 Sezgisel Giriş — "Mesafe Topolojiyi Doğurur"

Metrik uzayı tek cümlede özetlemek gerekirse: **noktalar arasındaki mesafe
fikrinden bir topoloji üretmektir.** Elimizde yalnızca "iki nokta ne kadar uzak?"
sorusunu yanıtlayan bir `d(x,y)` fonksiyonu vardır; bu fonksiyondan, "bir noktanın
yakınında olmak" kavramını — yani açık kümeleri — kurarız. Köprü tek bir nesnedir:
**açık yuvar.**

![Açık yuvar B(x,r): merkez x'ten r'den daha yakın olan tüm noktalar; kesikli sınır yuvara dahil değildir.](../assets/ch14/fig_ch14_acik_yuvar.png)

Bir noktanın etrafına yarıçapı `r` olan bir yuvar `B(x,r)` çizdiğimizde, "x'e
yeterince yakın" noktaları topluca işaretlemiş oluruz. Bu yuvarları temel taş
yaparak indüklenen topolojiyi kurarız: bir küme açıktır ⟺ her noktasının etrafına
tümüyle içeride kalan bir açık yuvar sığar.

> 💡 **Sezgi:** Metrik, sayısal bir "uzaklık cetveli"dir; topoloji ise yalnızca
> "yakın mı, uzak mı?" sorusunu önemser. Aynı topolojiyi farklı cetveller
> (metrikler) üretebilir — önemli olan hangi noktaların hangi yuvarın *içinde*
> kaldığıdır, mesafenin tam sayısal değeri değil.

Aynı düzlem üzerinde farklı metrikler farklı biçimde yuvarlar üretir ama çoğu
zaman **aynı topolojiyi** indükler:

![Üç farklı metriğin birim yuvarı: Öklid çember, taksi (Manhattan) elması, maksimum metrik karesi — biçimleri farklı, indükledikleri topoloji aynı.](../assets/ch14/fig_ch14_birim_yuvarlar.png)
"""

# %% [markdown]
"""
### Metrik Aksiyomları

Bir M kümesi ve d: M×M → [0,∞) fonksiyonu verilsin. (M, d) bir **metrik uzay**,
d ise bir **metrik** olarak adlandırılır, eğer:

- **(M1) Özdeşlik:** d(x,y) = 0 ⟺ x = y
- **(M2) Simetri:** d(x,y) = d(y,x)
- **(M3) Üçgen eşitsizliği:** d(x,z) ≤ d(x,y) + d(y,z)

(M3'ten M1 ile birlikte **pozitif tanımlılık** türer: d(x,y) ≥ 0.)

Üçgen eşitsizliği, üç aksiyom içinde en derin olanıdır: "x'ten z'ye doğrudan
gitmek, y'ye uğrayıp gitmekten kısadır" der.

![Üçgen eşitsizliği: x'ten z'ye doğrudan mesafe, y üzerinden geçen dolaylı yoldan kısadır.](../assets/ch14/fig_ch14_ucgen.png)

> ❌ **Karşı-örnek (üçgen eşitsizliği şart):** {A,B,C} üzerinde d(A,B)=1, d(B,C)=1
> ama d(A,C)=5 koyalım (özdeşlik ve simetri korunsun). M1 ve M2 sağlanır, ama
> d(A,C)=5 > d(A,B)+d(B,C)=2 olduğundan M3 **ihlal edilir.** Bu fonksiyon bir
> *metrik değildir* — ürettiği "yuvarlar" tutarlı bir topoloji vermez. pytop'ta
> `validate_metric` bu durumu yakalar (bkz. Alıştırma K4).
"""

# %% [markdown]
"""
### Temel Kavramlar

- **Açık top:** B(x, r) = {y ∈ M : d(x,y) < r}
- **Kapalı top:** B̄(x, r) = {y ∈ M : d(x,y) ≤ r}
- **İndüklenen topoloji:** τ_d = {U : ∀x∈U, ∃ε>0, B(x,ε)⊆U}
- **Çap:** diam(A) = sup{d(x,y) : x,y ∈ A}
"""

# %% [markdown]
"""
### Standart Metrikler

| Metrik | Tanım | Uzay |
|--------|-------|------|
| Öklid | d(x,y) = \|x-y\| | ℝ |
| Ayrık | d(x,y) = 0 veya 1 | Herhangi X |
| l∞ (max) | max_i d_i(x_i,y_i) | Çarpım uzayı |
| Sınırlı (capped) | d'(x,y) = min(d(x,y), 1) | Eşdeğer topoloji |

> **Neden bu konu?** Metrik uzaylar topolojik uzayların en somut alt sınıfı; ℝⁿ ve Hilbert uzayları burada yaşar.

> 🔍 **Kendin dene:** `real_line_metric()` için `is_t2` ve `is_metrizable` sonuçlarını kontrol edin.

> ⚠️ **Sık hata:** Her metrik uzay T4 (normal Hausdorff); `is_t2 False` dönerse metrik tanımında hata var demektir.

> ↗️ **Bkz.:** Bölüm 9 (metrik ⟹ 2. sayılabilir iff ayrılabilir).

> 💭 **Öz-yansıtma:** Metrik topoloji ne zaman ayrık topolojiyle çakışır?

---
"""

# %% [markdown]
"""
## 2. Teoremler

**Teorem 2.1.** Her metrik uzay Hausdorff (T2) ve 1. sayılabilirdir.

> **İspat eskizi.** (T2) x ≠ y olsun; o hâlde r = d(x,y) > 0'dır (M1). Yarıçapı
> r/2 olan B(x, r/2) ve B(y, r/2) yuvarlarını alalım. Bunlar ayrıktır: ortak bir z
> noktası olsaydı, üçgen eşitsizliğinden (M3) r = d(x,y) ≤ d(x,z) + d(z,y) < r/2 +
> r/2 = r çelişkisi çıkardı. Demek ki x ve y açık komşuluklarla ayrılır ⟹ T2.
> (1. sayılabilir) Her x için sayılabilir {B(x, 1/n) : n ∈ ℕ} ailesi bir yerel
> bazdır: x'i içeren herhangi açık U için, ε > 0 ile B(x, ε) ⊆ U; 1/n < ε seçince
> B(x, 1/n) ⊆ U olur. ∎

**Teorem 2.2 (Sınırlı Metrik Eşdeğerliği).**
d'(x,y) = min(d(x,y),1) ile d aynı topolojiyi indükler.

> **İspat eskizi.** İki metriğin aynı topolojiyi indüklemesi için, her d-açık
> yuvarın içine bir d'-açık yuvar sığması ve tersi yeterlidir. r ≤ 1 olan
> yarıçaplar için B_d(x, r) = B_{d'}(x, r) tam olarak çakışır, çünkü d ile d' yalnız
> mesafe ≥ 1 olan çiftlerde ayrışır. Topoloji "yeterince küçük yuvarlar" tarafından
> belirlendiğinden (her açık küme küçük yuvarların birleşimidir), büyük yarıçaplı
> farklılık topolojiyi değiştirmez. Demek ki τ_d = τ_{d'}. ∎

**Teorem 2.3.** ℝⁿ üzerindeki max, sum ve Öklid metrikleri topolojik olarak eşdeğerdir.

> **İspat eskizi.** Üç metrik karşılıklı olarak sabit çarpanlarla sınırlanır: her
> x, y için d_∞ ≤ d_2 ≤ d_1 ≤ n·d_∞ (max ≤ Öklid ≤ taksi ≤ n·max). Böyle bir
> "sandviç" eşitsizliği her metriğin yuvarının içine ötekinin yuvarını sığdırır:
> B_∞(x, r/n) ⊆ B_1(x, r) ⊆ B_∞(x, r) gibi. Karşılıklı içerme ⟹ aynı açık kümeler ⟹
> aynı topoloji. (Bölüm 1.0'daki birim-yuvar figürü bu üç biçimi yan yana
> gösterir.) ∎

---
"""

# %% [markdown]
"""
## 3. Algoritmalar
"""

# %% [markdown]
"""
### validate_metric — O(|X|³)

```
ValidateMetric(X, d):
    // M1: özdeşlik
    for each x in X:
        if d(x,x) != 0: return False
        for each y != x:
            if d(x,y) == 0: return False
    // M2: simetri
    for each x,y in X:
        if d(x,y) != d(y,x): return False
    // M3: üçgen
    for each x,y,z in X:
        if d(x,z) > d(x,y) + d(y,z): return False
    return True
```

Karmaşıklık: O(|X|³) — üçgen eşitsizliği dominates.
"""

# %% [markdown]
"""
### open_ball — O(|X|)

```
OpenBall(x, r, X, d):
    return {y in X : d(x,y) < r}
```

---
"""

# %% [markdown]
"""
## 4. pytop API
"""

# %%
from pytop.metric_spaces import (
    FiniteMetricSpace,
    SymbolicMetricSpace,
    validate_metric,
)
from pytop import (
    open_ball,
    closed_ball,
    distance_to_subset,
    diameter_of_subset,
    is_bounded_subset,
    capped_metric,
    normalized_metric,
)

# %% [markdown]
"""
`FiniteMetricSpace(carrier=tuple, distance=dict)` — mesafe sözlüğü `(a,b): float` şeklinde.

`open_ball(fms, point, radius)` → `set` döner (Result değil).

`capped_metric(distance_fn, cap=1.0)` → `Callable` döner; yeni `FiniteMetricSpace` değil.

**Metrik → TDA köprüsü:** Bir `FiniteMetricSpace` (`carrier` + `distance`),
doğrudan `pytop.persistent_homology(space, max_dimension=, max_scale=)` fonksiyonuna
beslenebilir. Bu, ham nokta bulutunu Vietoris–Rips filtrasyonuna çevirip kalıcı
homolojiyi (barcode) hesaplar. Dönen `PersistencePair` nesnelerinin alanları:
`dimension`, `birth`, `death`, `persistence`, `is_essential` (bkz. Örnek 5.8).

---
"""

# %% [markdown]
"""
## 5. Örnekler
"""

# %% [markdown]
"""
### Örnek 5.1 — Ayrık Metrik Uzay Oluşturma
"""

# %%
from pytop.metric_spaces import FiniteMetricSpace

points = [1, 2, 3, 4]
dist_discrete = {(a, b): (0 if a == b else 1) for a in points for b in points}
fms = FiniteMetricSpace(carrier=tuple(points), distance=dist_discrete)

print("carrier:", fms.carrier)
print("d(1,2):", fms.distance[(1,2)])
print("d(1,1):", fms.distance[(1,1)])

# %% [markdown]
"""
```text
carrier: (1, 2, 3, 4)
d(1,2): 1
d(1,1): 0
```
"""

# %% [markdown]
"""
### Örnek 5.2 — validate_metric
"""

# %%
from pytop.metric_spaces import validate_metric

r = validate_metric(fms)
print("status:", r.status)
print("justification:", r.justification[0] if r.justification else "")

# %% [markdown]
"""
```text
status: true
justification: All metric axioms hold on the explicit finite carrier.
```
"""

# %% [markdown]
"""
### Örnek 5.3 — open_ball ve closed_ball
"""

# %%
from pytop import open_ball, closed_ball

print("B(1, 0.5) =", open_ball(fms, 1, 0.5))    # yalnizca {1}
print("B(1, 1.5) =", open_ball(fms, 1, 1.5))    # tum uzay
print("Bclosed(1, 1.0) =", closed_ball(fms, 1, 1.0))  # tum uzay

# %% [markdown]
"""
```text
B(1, 0.5) = {1}
B(1, 1.5) = {1, 2, 3, 4}
Bclosed(1, 1.0) = {1, 2, 3, 4}
```

Ayrık metrikte B(1, r): r < 1 ise yalnız {1}, r ≥ 1 ise tüm uzay.
"""

# %% [markdown]
"""
### Örnek 5.4 — diameter ve distance_to_subset
"""

# %%
from pytop import diameter_of_subset, distance_to_subset, is_bounded_subset

print("diam({1,2,3}):", diameter_of_subset(fms, {1, 2, 3}))
print("d(1, {2,3}):", distance_to_subset(fms, 1, {2, 3}))
print("is_bounded({1,2}):", is_bounded_subset(fms, {1, 2}))

# %% [markdown]
"""
```text
diam({1,2,3}): 1.0
d(1, {2,3}): 1.0
is_bounded({1,2}): True
```
"""

# %% [markdown]
"""
### Örnek 5.5 — Öklid Metriki
"""

# %%
points_line = [0, 1, 2, 3]
dist_eucl = {(a, b): abs(a - b) for a in points_line for b in points_line}
fms_line = FiniteMetricSpace(carrier=tuple(points_line), distance=dist_eucl)

print("d(0,3):", fms_line.distance[(0,3)])
print("B(1, 1.5) =", open_ball(fms_line, 1, 1.5))
print("diam({0,1,2,3}):", diameter_of_subset(fms_line, {0,1,2,3}))

# %% [markdown]
"""
```text
d(0,3): 3
B(1, 1.5) = {0, 1, 2}
diam({0,1,2,3}): 3.0
```
"""

# %% [markdown]
"""
### Örnek 5.6 — capped_metric
"""

# %%
from pytop import capped_metric

cap_fn = capped_metric(fms_line.distance, cap=1.0)
print("d(0,3) capped:", cap_fn(0, 3))  # min(3, 1.0) = 1.0
print("d(0,1) capped:", cap_fn(0, 1))  # min(1, 1.0) = 1.0

# %% [markdown]
"""
```text
d(0,3) capped: 1.0
d(0,1) capped: 1.0
```

`capped_metric` eşit topoloji üretir ama değerler [0, cap] aralığındadır.
"""

# %% [markdown]
"""
### Örnek 5.7 — Üç Metrik, Üç Yuvar, Aynı Geçerlilik

Düzlemdeki aynı beş nokta üzerinde Öklid, taksi (ℓ¹) ve maksimum (ℓ∞) metriklerini
kurarız. Üçü de geçerli metriktir ama aynı çift için farklı mesafe verir — Bölüm
1.0'daki birim-yuvar figürünün sayısal karşılığı.
"""

# %%
import math
from pytop.metric_spaces import FiniteMetricSpace, validate_metric

grid = [(0, 0), (1, 0), (0, 1), (1, 1), (2, 1)]
carrier = tuple(range(len(grid)))

def euclid(i, j):    return math.dist(grid[i], grid[j])
def taxicab(i, j):   return abs(grid[i][0]-grid[j][0]) + abs(grid[i][1]-grid[j][1])
def chebyshev(i, j): return max(abs(grid[i][0]-grid[j][0]), abs(grid[i][1]-grid[j][1]))

for name, d in [("Oklid   ", euclid), ("Taksi   ", taxicab), ("Maksimum", chebyshev)]:
    dist = {(i, j): d(i, j) for i in carrier for j in carrier}
    fms = FiniteMetricSpace(carrier=carrier, distance=dist)
    print(f"{name} d(0,4)={dist[(0,4)]:.4f}  metrik? {validate_metric(fms).status}")

# %% [markdown]
"""
```text
Oklid    d(0,4)=2.2361  metrik? true
Taksi    d(0,4)=3.0000  metrik? true
Maksimum d(0,4)=2.0000  metrik? true
```

Nokta 0 = (0,0) ile nokta 4 = (2,1) arası: Öklid √5 ≈ 2.236, taksi |2|+|1| = 3,
maksimum max(2,1) = 2. Mesafeler farklı, ama üçü de aynı topolojiyi indükler
(Teorem 2.3).
"""

# %% [markdown]
"""
### Örnek 5.8 — Metrik → Kalıcı Homoloji (TDA Köprüsü)

Metrik uzayın hesaplama gücüne köprü: bir nokta bulutundan `FiniteMetricSpace`
kurup doğrudan `persistent_homology`'ye veririz. Çember üzerinde örneklenmiş 8 nokta
— "delik" (1-boyutlu döngü) topolojik imza olarak ortaya çıkmalıdır.
"""

# %%
import math
import pytop
from pytop.metric_spaces import FiniteMetricSpace

n = 8
pts = [(math.cos(2*math.pi*k/n), math.sin(2*math.pi*k/n)) for k in range(n)]
carrier = tuple(range(n))
dist = {(i, j): math.dist(pts[i], pts[j]) for i in carrier for j in carrier}
circle = FiniteMetricSpace(carrier=carrier, distance=dist)

pairs = pytop.persistent_homology(circle, max_dimension=2, max_scale=2.5)
components = [p for p in pairs if p.dimension == 0 and p.is_essential]
loops = [p for p in pairs if p.dimension == 1]

print("bilesen sayisi (essential H0):", len(components))
print("dongu  sayisi (H1):", len(loops))
loop = loops[0]
print(f"dongu: dogum={loop.birth:.4f} olum={loop.death:.4f} kalicilik={loop.persistence:.4f}")

# %% [markdown]
"""
```text
bilesen sayisi (essential H0): 1
dongu  sayisi (H1): 1
dongu: dogum=0.7654 olum=1.8478 kalicilik=1.0824
```

Tam olarak beklenen sonuç: çember **bağlantılı** olduğundan tek bir kalıcı bileşen
(H₀), ve **bir deliği** olduğundan tek bir kalıcı döngü (H₁). Döngü, komşu noktalar
birbirine bağlandığında doğar (≈ 0.765, en yakın komşu mesafesi) ve yarıçap deliği
dolduracak kadar büyüdüğünde ölür (≈ 1.848). Mesafe fonksiyonu `math.dist` ile
verilen ham koordinatlardan, pytop topolojik bir özelliği (deliğin varlığı) sayısal
olarak çıkardı.

---
"""

# %% [markdown]
"""
## 6. Alıştırmalar
"""

# %% [markdown]
"""
### Kodlama

K1. {A, B, C, D} noktaları üzerinde bir metrik tanımlayın ve `validate_metric` ile
    doğrulayın. Üçgen eşitsizliğini ihlal eden bir örnek de deneyin.

K2. Öklid metrikli {0,1,...,9} üzerinde `open_ball(fms, 5, 3.0)` ve
    `closed_ball(fms, 5, 3.0)` hesaplayın.

K3. `normalized_metric` kullanarak bir metriği [0,1]'e normalleştirin.

K4. §1.0'daki karşı-örneği koda dökün: {A,B,C,D} üzerinde d(A,C)=5, d(A,B)=d(B,C)=1
    olan bir mesafe sözlüğü kurun (geri kalanını ayrık metrikle doldurun) ve
    `validate_metric` ile üçgen eşitsizliğinin ihlal edildiğini gösterin. Çıktının
    `justification` alanını yazdırın.

K5. *(TDA köprüsü)* Birim kareyi örnekleyen **dolu** bir 3×3 ızgara (9 nokta)
    üzerinde Öklid `FiniteMetricSpace` kurun ve `persistent_homology(space,
    max_dimension=2, max_scale=2.5)` çalıştırın. H₁ döngülerinin `persistence`
    değerlerine bakın: Örnek 5.8'deki çemberin uzun ömürlü (kalıcılık ≈ 1.08)
    döngüsüne benzer **kalıcı** bir döngü var mı? Dolu karenin neden gerçek bir
    deliği yoktur — çıkan döngüler neyi temsil eder?
"""

# %% [markdown]
"""
### Teori

T1. Her metrik uzayın Hausdorff olduğunu ispatlayın.
    (İpucu: d(x,y)>0 için B(x, ε) ∩ B(y, ε) = ∅ seçin.)

T2. d' = min(d, 1) ve d aynı topolojiyi indüklediğini gösterin.

T3. Üçgen eşitsizliğinin (M3) Teorem 2.1'deki Hausdorff ispatında tam olarak
    nerede kullanıldığını açıklayın. (İpucu: B(x, r/2) ve B(y, r/2)'nin ayrık
    olduğunu gösterirken hangi adım M3'e dayanır?)
"""
