## Bölüm 11: Altuzay ve Çarpım Topolojisi

Bu ek, Bölüm 11 alıştırmalarının tam çözümlerini içerir. Kodlama
çözümlerindeki tüm çıktılar gerçek çalıştırmadan alınmıştır; teori çözümleri tam
argüman verir.

---

### K1 — Sierpiński'nin {0} ve {1} alt uzayları

(ch11 K1 alıştırmasına dön)

```python
from pytop import finite_subspace, sierpinski_space

s = sierpinski_space()
sub0 = finite_subspace(s, [0])
sub1 = finite_subspace(s, [1])
print("{0}:", sub0.carrier, list(sub0.topology))
print("{1}:", sub1.carrier, list(sub1.topology))
```

```text
{0}: (0,) [set(), {0}]
{1}: (1,) [set(), {1}]
```

Sierpiński uzayı `({0,1}, {∅, {0}, {0,1}})`'dir. `{0}` alt uzayında açıklar
`∅∩{0}=∅` ve `{0}∩{0}={0}` ile `X∩{0}={0}` olup `{∅, {0}}`; `{1}` alt uzayında
ise `∅∩{1}=∅`, `{0}∩{1}=∅`, `X∩{1}={1}` olup `{∅, {1}}`. Tek noktalı her
uzayda tek topoloji vardır; her iki alt uzay da (kaçınılmaz olarak) ayrık =
indiscrete = trivial tek-nokta topolojisini taşır.

---

### K2 — Özel 4-noktalı uzayda {2,3} alt uzayı

(ch11 K2 alıştırmasına dön)

```python
from pytop import finite_subspace, make_topology, make_set, empty_set

X = make_topology(
    [1, 2, 3, 4],
    empty_set(),
    make_set(1, 2),
    make_set(3, 4),
    make_set(1, 2, 3, 4),
)
sub23 = finite_subspace(X, [2, 3])
print("carrier:", sub23.carrier)
print("tau_A:", sorted([sorted(list(u)) for u in sub23.topology], key=lambda x: (len(x), x)))
```

```text
carrier: (2, 3)
tau_A: [[], [2], [3], [2, 3]]
```

τ = {∅, {1,2}, {3,4}, X}'in her elemanını A = {2,3} ile keseriz:
∅∩A=∅, {1,2}∩A={2}, {3,4}∩A={3}, X∩A={2,3}. Sonuç τ_A = {∅, {2}, {3}, {2,3}}
yani A üzerinde **ayrık** topoloji. İlginç olan: X bağlantılı görünmese de
(ayrık parçalar gibi) {2,3} alt uzayı tam ayrık çıkar; alt uzay topolojisi
orijinalin "ne kadarını gördüğüne" bağlıdır.

---

### K3 — Sierpiński × Ayrık(0,1) çarpımı

(ch11 K3 alıştırmasına dön)

```python
from pytop import binary_product, sierpinski_space, discrete_topology, is_compact, is_connected

p = binary_product(sierpinski_space(), discrete_topology(0, 1))
print("compact:", is_compact(p).status)
print("connected:", is_connected(p).status)
```

```text
compact: true
connected: false
```

İki çarpan da sonlu olduğundan çarpım sonlu, dolayısıyla kompakttır.
Bağlantılılık ise korunmaz: Sierpiński bağlantılı olsa da D(0,1) ayrık ve
bağlantısızdır; çarpımda bağlantısız bir çarpan tüm çarpımı bağlantısız kılar
(çarpım bağlantılı ⟺ her iki çarpan bağlantılı).

---

### K4 — İndiscrete(1,2,3,4)'ün {1,2} alt uzayı

(ch11 K4 alıştırmasına dön)

```python
from pytop import finite_subspace, indiscrete_topology, is_connected

ind4 = indiscrete_topology(1, 2, 3, 4)
sub_ind = finite_subspace(ind4, [1, 2])
print("|tau_A|:", len(list(sub_ind.topology)))
print("connected:", is_connected(sub_ind).status)
```

```text
|tau_A|: 2
connected: true
```

İndiscrete uzayda yalnızca ∅ ve X açıktır. Bunları A = {1,2} ile kesince
∅∩A=∅ ve X∩A=A elde edilir; τ_A = {∅, {1,2}}, yani 2 açık küme. Alt uzay yine
indiscrete'tir ve indiscrete uzaylar daima bağlantılıdır. Bu sonuç Örnek 5.7
ile birebir uyumludur: indiscrete topoloji alt uzaya miras kalır.

---

### K5 — Ayrık(1,2,3)'ten alınan {1,2} alt uzayının Hausdorff kalıtımı

(ch11 K5 alıştırmasına dön)

```python
from pytop import finite_subspace, discrete_topology, separation_inherited_by_subspace

d3 = discrete_topology(1, 2, 3)
sub_d = finite_subspace(d3, [1, 2])
inh = separation_inherited_by_subspace(sub_d, "hausdorff")
print("inherited:", inh.status)
```

```text
inherited: true
```

Ayrık uzay Hausdorff'tur (her iki noktanın tekil komşulukları ayrıktır). Teorem
2.1 gereği Hausdorff'luk alt uzaya kalıtır; `separation_inherited_by_subspace`
bunu `true` olarak doğrular. Alt uzay {1,2} de ayrık olduğundan zaten
Hausdorff'tur.

---

### T1 — Dahil etme i: A → X süreklidir

(ch11 T1 alıştırmasına dön)

**İddia.** Alt uzay topolojisi τ_A = {U ∩ A : U ∈ τ} ile, dahil etme
i: A → X, i(a) = a süreklidir.

**Kanıt.** Süreklilik için her açık U ∈ τ'nun ön-görüntüsünün A'da açık olması
gerekir. Tanım gereği

    i⁻¹(U) = {a ∈ A : i(a) ∈ U} = {a ∈ A : a ∈ U} = U ∩ A.

U ∩ A, alt uzay topolojisinin tanımı gereği τ_A'nın bir elemanıdır, yani A'da
açıktır. Her açık U'nun ön-görüntüsü açık olduğundan i süreklidir. ∎

**Not.** Aslında alt uzay topolojisi, i'yi sürekli kılan **en kaba** topolojidir:
i'yi sürekli yapacak herhangi bir τ' topolojisinin her U ∩ A'yı içermesi gerekir,
dolayısıyla τ_A ⊆ τ'. Bu, alt uzay topolojisinin "initial topoloji" karakterizasyonudur.

---

### T2 — X, Y bağlantılı ⟹ X × Y bağlantılı

(ch11 T2 alıştırmasına dön)

**İddia.** X ve Y bağlantılı topolojik uzaylar ise X × Y de bağlantılıdır.

**Kanıt.** Bir y₀ ∈ Y sabitleyelim. "Yatay dilim" X × {y₀}, X'in homeomorf
kopyasıdır (π_X kısıtlaması homeomorfizmadır), dolayısıyla bağlantılıdır.
Benzer şekilde her x ∈ X için "dikey dilim" {x} × Y, Y'nin kopyası olup
bağlantılıdır.

Şimdi her x için {x} × Y dilimi, ortak nokta (x, y₀) üzerinden yatay dilim
X × {y₀} ile kesişir. Yani

    X × Y = (X × {y₀}) ∪ ⋃_{x ∈ X} ({x} × Y),

ve birleştirilen her küme bağlantılıdır ve hepsi X × {y₀} ile (dolayısıyla
ortak noktalar üzerinden birbirleriyle) kesişir. Ortak noktalı bağlantılı
kümelerin birleşimi bağlantılı olduğundan X × Y bağlantılıdır. ∎

**Sezgi.** Çarpımda herhangi iki noktayı, "önce yatay sonra dikey" hareket eden
bağlantılı bir L-yolu ile birleştirebilirsiniz; bağlantısız bir ayrışım bu
yolları kesmek zorunda kalır, ki dilimlerin bağlantılılığı buna izin vermez.

---

### T3 — Çarpımın evrensel özelliği

(ch11 T3 alıştırmasına dön)

**İddia.** f: Z → X × Y verilsin. f süreklidir ⟺ π_X∘f ve π_Y∘f süreklidir.

**Kanıt.**

(⟹) f sürekli olsun. π_X ve π_Y süreklidir (çarpım topolojisi onları sürekli
kılacak şekilde tanımlıdır). Sürekli fonksiyonların bileşkesi sürekli olduğundan
π_X∘f ve π_Y∘f süreklidir.

(⟸) g := π_X∘f ve h := π_Y∘f sürekli olsun. Çarpım topolojisinin bir bazı
{U × V : U ∈ τ_X, V ∈ τ_Y}'dir; süreklilik baz elemanları üzerinde test
edilebilir. Bir baz elemanı U × V için

    f⁻¹(U × V) = {z : f(z) ∈ U × V}
               = {z : (π_X∘f)(z) ∈ U ve (π_Y∘f)(z) ∈ V}
               = g⁻¹(U) ∩ h⁻¹(V).

g ve h sürekli olduğundan g⁻¹(U) ve h⁻¹(V) Z'de açıktır; kesişimleri de açıktır.
Her baz elemanının ön-görüntüsü açık olduğundan ve baz topolojiyi ürettiğinden,
keyfi bir açık (baz elemanlarının birleşimi) için ön-görüntü de açıktır
(ön-görüntü birleşimlerle değişmelidir). Dolayısıyla f süreklidir. ∎

**Not.** Bu özellik çarpımı bir **kategorik çarpım** yapar: X ve Y'ye giden
sürekli fonksiyon çiftleri ile X × Y'ye giden sürekli fonksiyonlar
birebir eşleşir.
