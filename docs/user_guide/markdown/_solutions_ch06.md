## Bölüm 6 (ek): Ayrılma Aksiyomları

### K4 — excluded_point_topology(4, 0) en yüksek aksiyom

(ch06 K4 alıştırmasına dön)

```python
from pytop import excluded_point_topology, separation_chain

ep = excluded_point_topology(4, 0)   # X = {0,1,2,3}, dışlanan nokta 0
for prop, r in separation_chain(ep).items():
    print(f"  {prop:20s}: {r.status}")
```

```text
  t0                  : true
  t1                  : false
  hausdorff           : false
  urysohn             : false
  t3                  : false
  tychonoff           : false
  t4                  : false
  completely_normal   : false
  perfectly_normal    : false
```

Sağlanan en yüksek aksiyom **T0**'dır. Dışlanan-nokta topolojisinde bir küme ya
$0$'ı içermez ya da $X$'in kendisidir. Bu yüzden $1,2,3$ noktaları $\{1\},\{2\},
\{3\}$ gibi açıklarla iki yönlü; her $\{i, 0\}$ çifti ise $i$'yi içerip $0$'ı
dışlayan bir açıkla tek yönlü ayrılır — T0 tamam. T1 imkânsızdır: $0$'ı içeren
tek açık $X$'tir, dolayısıyla "$0$'ı içerip başka noktayı dışlayan açık" yoktur;
eşdeğer olarak $\{0\}$ kapalı değildir (tümleyeni $\{1,2,3\}$, $0$-içermediği
için açıktır, ama $\{0\}$'ın kendisi açık olmadığından kapalılık $\{0\}$'a
geçmez). T1 düşünce zincirin geri kalanı da düşer.

---

### T3 — Her metrik uzay normaldir (T4)

(ch06 T3 alıştırmasına dön)

**Strateji:** Ayrık iki kapalı küme arasında açık bir Urysohn fonksiyonu
mesafeyle elle inşa edilir; bu fonksiyonun seviye kümeleri aradığımız ayrık
açıkları verir.

$(X, d)$ bir metrik uzay, $C, D \subseteq X$ ayrık kapalı kümeler olsun
($C \cap D = \emptyset$). $A \neq \emptyset$ için $d(x, A) = \inf_{a \in A}
d(x, a)$ mesafe fonksiyonu süreklidir ve $A$ kapalıysa $d(x, A) = 0 \iff
x \in A$ sağlanır.

1. $C, D$ ayrık ve kapalı olduğundan her $x \in X$ için $d(x,C) + d(x,D) > 0$:
   payda hiçbir noktada sıfırlanmaz. (Eğer $d(x,C) = d(x,D) = 0$ olsaydı $x$ hem
   $C$'ye hem $D$'ye ait olurdu — çelişki.)

2.
   $$ f(x) = \frac{d(x,C)}{d(x,C) + d(x,D)} $$
   tanımla. $f$, sürekli fonksiyonların bölümü ve payda sıfırdan farklı
   olduğundan süreklidir; ayrıca $0 \le f \le 1$.

3. $x \in C \Rightarrow d(x,C) = 0 \Rightarrow f(x) = 0$ ve
   $x \in D \Rightarrow d(x,D) = 0 \Rightarrow f(x) = 1$: yani $f|_C \equiv 0$,
   $f|_D \equiv 1$ — tam bir Urysohn fonksiyonu.

4. $U = f^{-1}\big([0, \tfrac12)\big)$ ve $V = f^{-1}\big((\tfrac12, 1]\big)$ al.
   $f$ sürekli olduğundan $U, V$ açıktır; $C \subseteq U$ (çünkü $f|_C = 0$),
   $D \subseteq V$ (çünkü $f|_D = 1$) ve $U \cap V = \emptyset$ (bir nokta hem
   $<\tfrac12$ hem $>\tfrac12$ olamaz).

O halde her ayrık kapalı çift ayrık açıklara konabilir: metrik uzay normaldir.
Metrik uzaylar ayrıca T1'dir (tekiller kapalı), dolayısıyla **T4**'tür — ve
zincirin tüm üst basamakları (T3, T2.5, T2) bundan gelir. ∎
