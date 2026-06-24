## Bölüm 13: Başlangıç ve Son Topoloji

Bu dosya, Bölüm 13'ün (Başlangıç ve Son Topoloji) hem mevcut hem de yeni eklenen
alıştırmalarının çözümlerini içerir. Tüm kod blokları paylaşılan bir ad alanında
(namespace) sırayla çalışır: ilk blok daha sonra kullanılan tüm isimleri içe aktarır.

---

### A1 — initial_topology_from_maps vs. finite_subspace

(ch13 1. alıştırmasına dön)

`f: {a,b,c,d} → discrete({0,1})`, $f(a)=f(b)=0$, $f(c)=f(d)=1$ haritasının başlangıç
topolojisi, $f$'nin lif yapısını alt-baz yapar.

```python
from pytop.finite_map_analysis import FiniteMap
from pytop import (
    initial_topology_from_maps,
    discrete_topology,
    make_topology,
    is_continuous_finite_map,
)

carrier = ["a", "b", "c", "d"]
X_ph    = make_topology(carrier, set(), set(carrier))
Yd      = discrete_topology(0, 1)
f1 = FiniteMap(domain=X_ph, codomain=Yd, name="f",
               mapping={"a": 0, "b": 0, "c": 1, "d": 1})

tau = initial_topology_from_maps(carrier, [f1])
print("A1 tau_ini:", sorted([sorted(map(str, u)) for u in tau.topology],
                            key=lambda x: (len(x), x)))
print("A1 eleman sayisi:", len(tau.topology))
```

```text
A1 tau_ini: [[], ['a', 'b'], ['c', 'd'], ['a', 'b', 'c', 'd']]
A1 eleman sayisi: 4
```

Alt-baz $\{f^{-1}(\{0\}), f^{-1}(\{1\})\} = \{\{a,b\},\{c,d\}\}$; ürettiği topoloji
4 elemanlı. Bu, $X$'i iki lif $\{a,b\}$ ve $\{c,d\}$ üzerinde "iki noktalı discrete"
gibi görür — `finite_subspace` ile değil, lif bölmesiyle elde edilen kaba topolojidir.

---

### A2 — Tek projeksiyon başlangıç topolojisi

(ch13 2. alıştırmasına dön)

Yalnızca $\pi_x$ kullanılırsa, $y$-ekseni bilgisi kaybolur; topoloji discrete'den
kabadır.

```python
from pytop import binary_product

d2   = discrete_topology(0, 1)
prod = binary_product(d2, d2)
pi_x = FiniteMap(domain=prod, codomain=d2, name="pi_x",
                 mapping={(0,0):0, (0,1):0, (1,0):1, (1,1):1})

init_x = initial_topology_from_maps(list(prod.carrier), [pi_x])
print("A2 sadece pi_x eleman sayisi:", len(init_x.topology))
print("A2 tau:", sorted([sorted(map(str, u)) for u in init_x.topology],
                       key=lambda x: (len(x), x)))
```

```text
A2 sadece pi_x eleman sayisi: 4
A2 tau: [[], ['(0, 0)', '(0, 1)'], ['(1, 0)', '(1, 1)'], ['(0, 0)', '(0, 1)', '(1, 0)', '(1, 1)']]
```

Evet, discrete'den (16 açık küme) **daha kabadır** — yalnızca 4 açık küme. $\pi_x$
tek başına $x$-koordinatına göre iki şeride ayırır; tek noktaları ayıramaz. İkinci
projeksiyon $\pi_y$ eklenince kesişimler tüm tektonları üretir ve discrete'e ulaşılır
(Bölüm 6 örneği).

---

### A3 — Manuel son topoloji

(ch13 3. alıştırmasına dön)

$X=\{0,1,2,3,4\}$ discrete, $g: X \to \{0,1,2\}$, $g=\{0,1\mapsto0,\ 2,3\mapsto1,\ 4\mapsto2\}$.

```python
Xc     = [0, 1, 2, 3, 4]
sigmaD = discrete_topology(*Xc)
g3     = {0: 0, 1: 0, 2: 1, 3: 1, 4: 2}
Yc     = [0, 1, 2]
tauD   = {frozenset(u) for u in sigmaD.topology}

open_Y = []
for mask in range(1 << len(Yc)):
    V   = frozenset(Yc[i] for i in range(len(Yc)) if mask & (1 << i))
    pre = frozenset(x for x in sigmaD.carrier if g3[x] in V)
    if pre in tauD:
        open_Y.append(set(V))

final_Y = make_topology(Yc, *open_Y)
print("A3 (sigma=discrete) son topoloji eleman sayisi:", len(final_Y.topology))
```

```text
A3 (sigma=discrete) son topoloji eleman sayisi: 8
```

$\sigma_X$ discrete olduğundan **her** ön-görüntü açıktır; dolayısıyla $Y$'nin her alt
kümesi açık olur ve son topoloji $Y$ üzerinde discrete'dir ($2^3 = 8$ açık küme).
$\sigma_X$ inceltildikçe (daha az açık küme) son topoloji de kabalaşır: en-ince koşulu
kaynak topolojisinin inceliğine doğrudan bağlıdır.

---

### A4 — (Teori) Başlangıç topolojisinin evrensel özelliği

(ch13 4. alıştırmasına dön)

**İddia.** $h: Z \to (X, \tau_{\mathrm{ini}})$ sürekli $\iff$ her $f_\alpha \circ h$
sürekli.

**İspat.** ($\Rightarrow$) $h$ sürekli ve her $f_\alpha$ (tanımı gereği) sürekli ise,
sürekli haritaların bileşkesi sürekli olduğundan $f_\alpha \circ h$ süreklidir.

($\Leftarrow$) Her $f_\alpha \circ h$ sürekli olsun. $\tau_{\mathrm{ini}}$ alt-bazı
$\mathcal{S} = \{f_\alpha^{-1}(U) \mid U \in \tau_\alpha\}$ olduğundan, sürekliliği
yalnızca alt-baz elemanlarının ön-görüntülerinde denetlemek yeterlidir. Bir alt-baz
elemanı için

$$h^{-1}\big(f_\alpha^{-1}(U)\big) = (f_\alpha \circ h)^{-1}(U),$$

ve sağ taraf $f_\alpha \circ h$ sürekli olduğundan $Z$'de açıktır. Tüm alt-baz
elemanlarının ön-görüntüleri açık olunca tüm açık kümelerin (birleşim ve sonlu
kesişim) ön-görüntüleri de açıktır; demek ki $h$ süreklidir. $\square$

---

### A5 — (Teori) Son topolojinin en-incelik karakteri

(ch13 5. alıştırmasına dön)

**İddia.** $\tau_{\mathrm{fin}}$'den daha ince hiçbir topoloji her $g_i$'yi sürekli
kılamaz.

**İspat.** $\tau_{\mathrm{fin}} = \{V \subseteq Y \mid g_i^{-1}(V) \in \sigma_i\ \forall i\}$
tanımı, $g_i$'yi sürekli kılan açık kümelerin **tam** koleksiyonudur: bir $V$ açık
sayılmak için her $i$'de $g_i^{-1}(V)$ açık olmalıdır. Şimdi $\tau' \supsetneq
\tau_{\mathrm{fin}}$ olsun, yani $\tau'$ içinde $V_0 \in \tau' \setminus \tau_{\mathrm{fin}}$
bir açık küme bulunsun. $V_0 \notin \tau_{\mathrm{fin}}$ olduğundan en az bir $i$ için
$g_i^{-1}(V_0) \notin \sigma_i$. O hâlde $g_i: (X_i,\sigma_i) \to (Y,\tau')$ bu açık
$V_0$ için ön-görüntü açık olmadığından **sürekli değildir**. Demek ki
$\tau_{\mathrm{fin}}$'den kesin daha ince hiçbir topoloji tüm $g_i$'leri sürekli
tutamaz; $\tau_{\mathrm{fin}}$ en incedir. $\square$

---

### A6 — (Yeni) "En kaba" iddiasının süreklilik yüklemiyle doğrulanması

(ch13 6. alıştırmasına dön)

```python
def powerset_opens(elems):
    elems = list(elems)
    out = []
    for mask in range(1 << len(elems)):
        out.append({elems[i] for i in range(len(elems)) if mask & (1 << i)})
    return out

Xc6  = [0, 1, 2, 3]
Xph6 = make_topology(Xc6, set(), set(Xc6))
Yd6  = discrete_topology(0, 1)
f6   = FiniteMap(domain=Xph6, codomain=Yd6, name="f",
                 mapping={0: 0, 1: 0, 2: 1, 3: 1})

tau6   = initial_topology_from_maps(Xc6, [f6])
ini6   = [set(u) for u in tau6.topology]
codom6 = [set(u) for u in Yd6.topology]
indis6 = [set(), set(Xc6)]            # indiscrete: tau_ini'den daha kaba
disc6  = powerset_opens(Xc6)          # discrete: tau_ini'den daha ince

print("A6 f, tau_ini surekli   :",
      is_continuous_finite_map(Xc6, ini6,   list(Yd6.carrier), codom6, f6.mapping))
print("A6 f, indiscrete surekli:",
      is_continuous_finite_map(Xc6, indis6, list(Yd6.carrier), codom6, f6.mapping))
print("A6 f, discrete surekli  :",
      is_continuous_finite_map(Xc6, disc6,  list(Yd6.carrier), codom6, f6.mapping))
```

```text
A6 f, tau_ini surekli   : True
A6 f, indiscrete surekli: False
A6 f, discrete surekli  : True
```

$f$ hem $\tau_{\mathrm{ini}}$ hem discrete ile süreklidir, ama indiscrete ile değildir.
Bu üç sonuç birlikte "en kaba" iddiasını kanıtlar: $\tau_{\mathrm{ini}}$, $f$'yi sürekli
kılan topolojiler arasında en azını içerir; daha kabası (indiscrete) sürekliliği bozar,
daha incesi (discrete) gereksiz açık küme barındırır.

---

### A7 — (Yeni) Evrensel özelliğin doğrulanması

(ch13 7. alıştırmasına dön)

```python
Xc7  = ["a", "b"]
Xph7 = make_topology(Xc7, set(), set(Xc7))
Yd7  = discrete_topology(0, 1)
f7   = FiniteMap(domain=Xph7, codomain=Yd7, name="f", mapping={"a": 0, "b": 1})
g7   = FiniteMap(domain=Xph7, codomain=Yd7, name="g", mapping={"a": 1, "b": 0})

tau7 = initial_topology_from_maps(Xc7, [f7, g7])
Xop  = [set(u) for u in tau7.topology]
Yop  = [set(u) for u in Yd7.topology]

Zc, Zop = ["p", "q"], [set(), {"p"}, {"q"}, {"p", "q"}]
h  = {"p": "a", "q": "b"}
fh = {z: f7.mapping[h[z]] for z in Zc}     # f . h
gh = {z: g7.mapping[h[z]] for z in Zc}     # g . h

c_fh = is_continuous_finite_map(Zc, Zop, list(Yd7.carrier), Yop, fh)
c_gh = is_continuous_finite_map(Zc, Zop, list(Yd7.carrier), Yop, gh)
c_h  = is_continuous_finite_map(Zc, Zop, Xc7, Xop, h)

print("A7 tau_ini eleman:", len(tau7.topology))
print("A7 fh:", c_fh, "gh:", c_gh, "h:", c_h, "| denk:", c_h == (c_fh and c_gh))
```

```text
A7 tau_ini eleman: 4
A7 fh: True gh: True h: True | denk: True
```

$f$ ve $g$ birlikte $X$ üzerinde discrete topolojiyi (4 açık küme) üretir. $h$
süreklidir ancak ve ancak hem $f\circ h$ hem $g\circ h$ sürekli olduğunda; yüklem bu
denkliği `c_h == (c_fh and c_gh)` ile teyit eder. Bu, Teorem 4'ün (evrensel özellik)
somut, çalıştırılabilir bir tanığıdır.
