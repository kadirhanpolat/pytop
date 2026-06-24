## Bölüm 4 (ek): Topolojik Uzaylar

Bu dosya, Bölüm 4'e eklenen yeni alıştırmaların (K4, T3) çözümlerini içerir;
mevcut `solutions.md` içindeki Bölüm 4 çözümleri (K1–K3, T1–T2) olduğu gibi kalır.

### K4 — count_topologies_on_n_points doğrulaması

(ch04 K4 alıştırmasına dön)

```python
from pytop import count_topologies_on_n_points

for n in range(0, 5):
    print(f"n={n}: {count_topologies_on_n_points(n)}")
```

```
n=0: 1
n=1: 1
n=2: 4
n=3: 29
n=4: 355
```

`n=3` satırı T1 alıştırmasındaki "29 topoloji" iddiasını birebir doğrular. `n=4`
için sonuç `355`'tir; oysa $\{1,2,3,4\}$'ün açık küme ailesi olarak seçilebilecek
aday sayısı $2^{2^4}=65536$'dır. Aradaki uçurum, üç aksiyomun (T1–T3) bu
adayların ezici çoğunluğunu elemesinden gelir: rastgele bir alt-küme ailesi
neredeyse hiçbir zaman birleşim/kesişim altında kapalı değildir. Dizi OEIS
A000798'dir (sonlu topolojilerin sayısı) ve etiketsiz uzaylar üzerinde tanımlıdır.

### T3 — excluded_point_topology(3, 0): T0 ama T1 değil

(ch04 T3 alıştırmasına dön)

```python
from pytop import excluded_point_topology, is_t0, is_t1, is_t2

ep = excluded_point_topology(3, 0)   # X = {0,1,2}, 0 dislanir
print("Acik:", sorted(sorted(t) for t in ep.topology))
print("T0:", is_t0(ep).status, "| T1:", is_t1(ep).status, "| T2:", is_t2(ep).status)
```

```
Acik: [[], [0, 1, 2], [1], [1, 2], [2]]
T0: true | T1: false | T2: false
```

**Kanıt.** Dışlanan-nokta topolojisinde bir küme açıktır ancak ve ancak ya
dışlanan nokta $0$'ı içermez ya da tüm uzaydır. Dolayısıyla $0$'ı içeren *tek*
açık küme $X=\{0,1,2\}$'dir.

- **T0 (sağlanır):** İki farklı nokta alalım. Eğer çift `{0, y}` ise (`y` farklı),
  `{y}` açıktır, `y`'yi içerir, `0`'ı içermez — bir yön ayırır. Eğer çift
  `{x, y}` ve ikisi de `0` değilse, `{x}` açıktır ve `x`'i `y`'den ayırır. Her
  durumda en az bir yön ayrıldığından uzay T0'dır.
- **T1 (sağlanmaz):** T1 için *her iki yönün de* ayrılması gerekir. `0` ile
  `1` çiftine bakalım: `1`'i içerip `0`'ı dışlayan açık vardır (`{1}`), ama
  `0`'ı içerip `1`'i dışlayan açık **yoktur** — çünkü `0`'ı içeren tek açık
  küme bütün uzaydır ve o da `1`'i içerir. Bu yüzden `(0, 1)` çifti `0→1`
  yönünde ayrılamaz ve uzay T1 değildir.

**Sierpiński ile karşılaştırma.** Sierpiński uzayı $X=\{0,1\}$, $\tau=\{\emptyset,\{1\},X\}$
tam olarak `excluded_point_topology(2, 0)`'a denktir: dışlanan nokta `0`, açık olan
yegâne öz alt-küme `{1}`'dir. `excluded_point_topology(3, 0)` ise bu aynı T0-ama-T1-değil
asimetrisini üç noktaya genişletir; "dışlanan nokta" daima en küçük açık komşuluğu tüm
uzay olan, topolojik olarak "yapışkan" noktadır.
