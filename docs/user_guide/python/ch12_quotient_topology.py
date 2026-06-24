# %% [markdown]
"""
# Bölüm 12 — Bölüm Topolojisi (Quotient Topology)

Bölüm topolojisi, bir topolojik uzayın noktalarını denklik sınıflarına göre
"yapıştırarak" yeni bir uzay kurar.
Alt uzay ve çarpım topolojisiyle birlikte temel üç inşaat yönteminden birini oluşturur.

---
"""

# %% [markdown]
"""
## 1. Konu
"""

# %% [markdown]
"""
### Denklik Bağıntısı ve Bölüm Kümesi

(X, τ) topolojik uzayı ve X üzerinde bir denklik bağıntısı ~ verilsin.
Her x için denklik sınıfı [x] = {y ∈ X : y ~ x}.
Bölüm kümesi X/~ = {[x] : x ∈ X}.
"""

# %% [markdown]
"""
### Bölüm Topolojisi

Bölüm haritası q: X → X/~ tanımı: q(x) = [x].

Bölüm topolojisi τ_{X/~} üzerinde:

    U ⊆ X/~ açıktır  ⟺  q⁻¹(U) ∈ τ

Bu, q'yu sürekli kılan en ince (en fazla açık küme içeren) topolojidir.

> 💡 **Sezgi:** Bölüm topolojisini bir "katlama" gibi düşünün. Elinizde bir kâğıt
> şerit ([0,1]) varsa ve iki ucunu birbirine yapıştırırsanız bir çember (S¹) elde
> edersiniz. Yapıştırma kuralı bir denklik bağıntısıdır (0 ~ 1); bölüm topolojisi
> ise "kâğıdı yırtmadan" yapılan bu katlamanın doğal topolojisidir. q haritası her
> noktayı yapıştırma sonrası bulunduğu konuma gönderir; bir kümenin yapıştırılmış
> uzayda açık olması, geri-çekilmiş halinin (ön-görüntüsünün) orijinal kâğıtta
> açık olmasına bağlıdır.
"""

# %% [markdown]
"""
### Doymuş (Saturated) Kümeler

Bir A ⊆ X kümesi **doymuştur** (saturated) eğer her x ∈ A için x'in tüm
denklik sınıfı [x] yine A içinde kalıyorsa, yani A = q⁻¹(q(A)) ise.
Bölüm topolojisinin açık kümeleri tam olarak X'in doymuş açık kümelerine karşılık gelir:

    q(A), X/~ içinde açık  ⟺  A doymuş ve X içinde açık.

![[0,1] şeridinin uçları yapıştırılarak çember S¹ elde edilir; q haritası her noktayı denklik sınıfına gönderir.](../assets/ch12/fig_ch12_cember_yapistirma.png)
"""

# %% [markdown]
"""
### Topolojik Özelliklerin Korunumu

| Özellik       | Bölüm uzayı için durum                       |
|---------------|----------------------------------------------|
| Kompaktlık    | X kompakt ⟹ X/~ kompakt                    |
| Bağlantılılık | X bağlantılı ⟹ X/~ bağlantılı             |
| Hausdorff     | Genel olarak korunmaz                        |
| T1            | ~ kapalı bağıntı ise korunur                |

![Denklik sınıfları bölüm uzayında birer noktaya çöker: dört nokta {a,b}, {c}, {d} sınıflarıyla üç noktaya iner.](../assets/ch12/fig_ch12_denklik_siniflari.png)

> ❌ **Karşı-örnek:** Hausdorff özelliği bölüm altında korunmaz. ℝ üzerinde
> "x ~ y ⟺ x − y ∈ ℚ" bağıntısını alın. Bölüm uzayı ℝ/ℚ kaba (indiscrete) bir
> uzaydır: tek açık kümeler ∅ ve tüm uzaydır, çünkü ℚ ile öteleme altında doymuş
> tek açık küme boş küme ve ℝ'dir. Dolayısıyla iki farklı nokta hiçbir zaman ayrık
> komşuluklarla ayrılamaz — ℝ Hausdorff olmasına rağmen ℝ/ℚ T1 bile değildir.
> Sonlu modelde aynı tuzak: bir noktayı kapalı yapan açık küme, ancak doymuş
> olduğunda bölüme iner; doymamış açık kümeler yapıştırma sonrası "kaybolur" ve
> ayırma aksiyomlarını bozabilir.

> **Neden bu konu?** Eşdeğerlik bağıntısından yeni uzay üretmek; daire S¹ ve torus bu şekilde inşa edilir.

> 🔍 **Kendin dene:** `quotient_set` ile `equivalence_class` çıktılarını karşılaştırın: hangisi hangi bilgiyi taşır?

> ⚠️ **Sık hata:** `quotient_set` denklik bağıntısı gerektirir; rastgele bağıntı `RelationError` fırlatır.

> ↗️ **Bkz.:** Bölüm 3 (`partition_from_equivalence`), Bölüm 11 (bölüm topolojisi inşası).

> 💭 **Öz-yansıtma:** S¹ = [0,1] / {0~1} yapısını küçük bir taşıyıcı üzerinde modelleyebilir misiniz?

---
"""

# %% [markdown]
"""
## 2. Teoremler

**Teorem 2.1 (Bölüm haritası sürekliliği).**
q: X → X/~ her zaman süreklidir.

**Teorem 2.2 (Evrensel özellik).**
g: X/~ → Z olsun. g süreklidir ⟺ g ∘ q: X → Z süreklidir.

> **İspat eskizi.** (Evrensel özellik) (⟹) g sürekli ve q sürekli (Teorem 2.1)
> olduğundan, iki sürekli haritanın bileşkesi g ∘ q süreklidir. (⟸) Şimdi g ∘ q'nun
> sürekli olduğunu varsayalım; g'nin sürekli olduğunu gösterelim. Z'de bir V açık
> kümesi alın. g⁻¹(V) ⊆ X/~ kümesinin bölüm topolojisinde açık olduğunu
> kanıtlamalıyız. Bölüm topolojisinin tanımı gereği bu, q⁻¹(g⁻¹(V)) kümesinin
> X'te açık olmasına denktir. Ama q⁻¹(g⁻¹(V)) = (g ∘ q)⁻¹(V) ve g ∘ q sürekli
> olduğundan bu küme X'te açıktır. Dolayısıyla g⁻¹(V) bölüm topolojisinde açıktır
> ve g süreklidir. ∎ Bu özellik, bölüm uzayından çıkan sürekli haritaları kontrol
> etmeyi, çok daha somut olan X üzerindeki haritaları kontrol etmeye indirger;
> bölüm topolojisini bir evrensel nesne olarak karakterize eder.

**Teorem 2.3 (Kompaktlık korunumu).**
X kompakt ⟹ X/~ kompakttır.

> **İspat eskizi.** q: X → X/~ sürekli ve örtendir (her sınıf en az bir noktanın
> görüntüsüdür). Kompakt bir kümenin sürekli görüntüsü kompakt olduğundan
> X/~ = q(X) kompakttır. ∎

**Teorem 2.4 (Bağlantılılık korunumu).**
X bağlantılı ⟹ X/~ bağlantılıdır.

**Teorem 2.5.**
X/~ Hausdorff ⟺ ~ grafiği X × X'te kapalıdır.

---
"""

# %% [markdown]
"""
## 3. Algoritmalar
"""

# %% [markdown]
"""
### quotient_set — O(|X|² · α(|X|))

```
QuotientSet(X, ~):
    Initialize: her x için {x} sınıfı
    For each (x, y) in ~:
        Union(x, y)           # union-find
    Return sınıfları tuple olarak
```

Sonuç: X/~'nin elemanları olan dondurulmuş kümeler (frozenset) demeti.
"""

# %% [markdown]
"""
### finite_quotient_contract — O(|X| + |bloklar|)

```
FiniteQuotientContract(X, P):
    // P = X'in bir bölüntüsü
    Validate(P covers X, blocks are disjoint)
    Return FiniteConstructionContract(
        status='true', carrier_size=|X|, block_count=|P|
    )
```

---
"""

# %% [markdown]
"""
## 4. pytop API
"""

# %%
from pytop import (
    quotient_set,               # denklik bağıntısından bölüm kümesi
    finite_quotient_contract,   # bölüntüden inşaat sözleşmesi
    finite_quotient_summary,    # kısa özet dizesi
    make_quotient_map,          # QuotientMap nesnesi
    is_quotient_map,            # Result: harita bölüm haritası mı?
    equivalence_class,          # bir noktanın denklik sınıfı
    partition_from_equivalence, # denklik bağıntısı → bölüntü
    is_equivalence_relation,    # bağıntı denklik bağıntısı mı?
    equivalence_from_partition, # bölüntü → denklik bağıntısı
    equivalence_from_classes,   # sınıf bloklarından denklik bağıntısı
    canonical_projection_from_equivalence,  # q haritasını sözlük olarak
    discrete_topology,          # ayrık topoloji
    sierpinski_space,           # Sierpiński uzayı
    make_topology,              # taşıyıcı + açıklardan FiniteTopologicalSpace
)

# %% [markdown]
"""
`quotient_set(carrier, relation)` → `tuple[frozenset, ...]`
- `relation`: tam denklik bağıntısı (yansımalı + simetrik + geçişli çiftler listesi)

`finite_quotient_contract(carrier, partition)` → `FiniteConstructionContract`
- `partition`: örtüşmeyen liste-listesi
- Alanlar: `.status`, `.block_count`, `.carrier_size`, `.to_result()`

`finite_quotient_summary(carrier, partition)` → `str`

`make_quotient_map(domain, codomain)` → `QuotientMap`

`is_quotient_map(map_obj)` → `Result`

`equivalence_from_partition(universe, partition)` → `set[tuple]` (denklik bağıntısı)

`partition_from_equivalence(carrier, relation)` → `set[frozenset]` (bölüntü)

`equivalence_class(carrier, relation, point)` → `set` (bir noktanın sınıfı)

`canonical_projection_from_equivalence(carrier, relation)` → `dict[nokta, frozenset]`

---
"""

# %% [markdown]
"""
## 5. Örnekler
"""

# %% [markdown]
"""
### Örnek 5.1 — İki Noktayı Özdeşleştirme
"""

# %%
d4 = discrete_topology(0, 1, 2, 3)

partition_1 = [[0, 1], [2], [3]]
qs1 = quotient_set(
    [0, 1, 2, 3],
    [(0,0),(1,1),(2,2),(3,3),(0,1),(1,0)]
)
print("Bölüm kümesi:", qs1)
contract1 = finite_quotient_contract([0, 1, 2, 3], partition_1)
print("Blok sayısı:", contract1.block_count)
print("Durum:", contract1.status)

# %% [markdown]
"""
```text
Bölüm kümesi: (frozenset({2}), frozenset({3}), frozenset({0, 1}))
Blok sayısı: 3
Durum: true
```

4 noktalı ayrık uzayda 0 ve 1 özdeşleştirildi; bölüm uzayı 3 elemanlıdır.
"""

# %% [markdown]
"""
### Örnek 5.2 — Tüm Noktaları Tek Noktaya Çökertme
"""

# %%
carrier = [0, 1, 2, 3]
qs2 = quotient_set(
    carrier,
    [(i, j) for i in carrier for j in carrier]
)
print("Tek blok:", qs2)

contract2 = finite_quotient_contract(carrier, [carrier])
print("Blok sayısı:", contract2.block_count)
r2 = contract2.to_result()
print("Metadata blok boyutları:", r2.metadata['block_sizes'])

# %% [markdown]
"""
```text
Tek blok: (frozenset({0, 1, 2, 3}),)
Blok sayısı: 1
Metadata blok boyutları: [4]
```

Tüm noktalar tek sınıfta toplandığında bölüm uzayı tek noktalıdır.
"""

# %% [markdown]
"""
### Örnek 5.3 — Sierpiński Uzayında Bölüm
"""

# %%
s = sierpinski_space()
print("Sierpinski carrier:", sorted(s.carrier))
print("Sierpinski topology:", sorted([sorted(list(u)) for u in s.topology],
                                     key=lambda x: (len(x), x)))

summary_s = finite_quotient_summary(list(s.carrier), [[0, 1]])
print("Sierpinski / {0,1}:", summary_s)

# %% [markdown]
"""
```text
Sierpinski carrier: [0, 1]
Sierpinski topology: [[], [1], [0, 1]]
Sierpinski / {0,1}: quotient: status=true, carrier=2, blocks=1
```

Sierpiński uzayında her iki nokta özdeşleştirildiğinde bir blok kalır.
"""

# %% [markdown]
"""
### Örnek 5.4 — Özel Topolojide Bölüm Sözleşmesi
"""

# %%
X5 = [1, 2, 3, 4, 5]
tau5 = [set(), {1,2}, {3,4}, {1,2,3,4}, {1,2,3,4,5}]
fts5 = make_topology(X5, *tau5)
print("Uzay:", sorted([sorted(list(u)) for u in fts5.topology],
                      key=lambda x: (len(x), x)))

partition5 = [[1, 2], [3, 4], [5]]
contract5 = finite_quotient_contract(X5, partition5)
r5 = contract5.to_result()
print("Status:", r5.status)
print("Bloklar:", r5.metadata['block_count'])
print("Blok boyutları:", r5.metadata['block_sizes'])

# %% [markdown]
"""
```text
Uzay: [[], [1, 2], [3, 4], [1, 2, 3, 4], [1, 2, 3, 4, 5]]
Status: true
Bloklar: 3
Blok boyutları: [2, 2, 1]
```

τ'daki açık kümelerin tam olarak bloklar üzerinden tanımlı olması bu bölüntünün
uzayın "doğal" bölüntüsü olduğunu gösterir.
"""

# %% [markdown]
"""
### Örnek 5.5 — Bölüm Haritası Nesnesi
"""

# %%
d3 = discrete_topology(0, 1, 2)
d2 = discrete_topology('a', 'b')

qmap = make_quotient_map(d3, d2)
print("QuotientMap türü:", type(qmap).__name__)
print("Etiketler:", sorted(qmap.tags))

r_qmap = is_quotient_map(qmap)
print("is_quotient_map status:", r_qmap.status)
print("Justification:", r_qmap.justification[0])

# %% [markdown]
"""
```text
QuotientMap türü: QuotientMap
Etiketler: ['continuous', 'quotient', 'surjective']
is_quotient_map status: true
Justification: Map tag 'quotient' is explicitly present.
```

`make_quotient_map` bir QuotientMap nesnesi üretir; `is_quotient_map` bu nesne üzerinde
`Result` döner.
"""

# %% [markdown]
"""
### Örnek 5.6 — Bölüm Özetleri Karşılaştırması
"""

# %%
carrier6 = list(range(6))

configs = [
    ("6->6 (trivial)", [[x] for x in carrier6]),
    ("6->3 (çiftler)", [[0,1],[2,3],[4,5]]),
    ("6->2 (üçlüler)", [[0,1,2],[3,4,5]]),
    ("6->1 (tek nokta)",  [carrier6]),
]
for label, part in configs:
    s = finite_quotient_summary(carrier6, part)
    print(f"{label:20s}: {s}")

# %% [markdown]
"""
```text
6->6 (trivial)      : quotient: status=true, carrier=6, blocks=6
6->3 (çiftler)      : quotient: status=true, carrier=6, blocks=3
6->2 (üçlüler)      : quotient: status=true, carrier=6, blocks=2
6->1 (tek nokta)    : quotient: status=true, carrier=6, blocks=1
```

Aynı taşıyıcı üzerinde farklı bölüntüler farklı boyutlarda bölüm uzayları üretir.
"""

# %% [markdown]
"""
### Örnek 5.7 — [0,1] Uçlarını Yapıştırarak Çember S¹

`[0,1]` aralığını 5 noktayla modelliyoruz (`0,1,2,3,4`). İki ucu (0 ve 4)
özdeşleştirmek, şeridi bir çembere yapıştırmaya karşılık gelir.
`equivalence_from_partition` bölüntüyü denklik bağıntısına çevirir; sonra bölüm
kümesini ve uçların ortak sınıfını okuruz.
"""

# %%
ring = [0, 1, 2, 3, 4]
ring_classes = [[0, 4], [1], [2], [3]]      # 0 ve 4 yapıştırılır
ring_rel = equivalence_from_partition(ring, ring_classes)

print("Denklik bağıntısı mı?", is_equivalence_relation(ring, ring_rel))
print("Bölüm kümesi boyutu:", len(quotient_set(ring, ring_rel)))
print("Özet:", finite_quotient_summary(ring, ring_classes))
print("0'in sinifi:", sorted(equivalence_class(ring, ring_rel, 0)))
print("4'un sinifi:", sorted(equivalence_class(ring, ring_rel, 4)))

# %% [markdown]
"""
```text
Denklik bağıntısı mı? True
Bölüm kümesi boyutu: 4
Özet: quotient: status=true, carrier=5, blocks=4
0'in sinifi: [0, 4]
4'un sinifi: [0, 4]
```

Uçlar tek bir sınıfta birleşti (`[0, 4]`): 5 noktalı şerit, 4 noktalı çevrime
(çembere) indi. 0 ve 4 artık aynı noktadır — yapıştırma gerçekleşti.
"""

# %% [markdown]
"""
### Örnek 5.8 — Doymuş Kümeler ve Kanonik İzdüşüm

Kanonik izdüşüm q her noktayı denklik sınıfına gönderir.
`canonical_projection_from_equivalence` bu haritayı bir sözlük olarak verir;
böylece hangi noktaların yapıştırma sonrası çakıştığını okuyabiliriz.
Bir kümenin **doymuş** olması, içerdiği her noktanın sınıfını da tamamen
içermesi demektir.
"""

# %%
sat_carrier = ['a', 'b', 'c', 'd']
sat_part = [['a', 'b'], ['c'], ['d']]       # a ve b yapıştırılır
sat_rel = equivalence_from_partition(sat_carrier, sat_part)

proj = canonical_projection_from_equivalence(sat_carrier, sat_rel)
for pt in sat_carrier:
    print(f"q({pt}) =", sorted(proj[pt]))

cls_a = equivalence_class(sat_carrier, sat_rel, 'a')
print("a'nin sinifi:", sorted(cls_a))
# {a,b} doymustur: a'yi iceriyorsa b'yi de icermek zorunda
A = {'a', 'b'}
saturated = all(equivalence_class(sat_carrier, sat_rel, p) <= A for p in A)
print("{a,b} doymus mu?", saturated)
print("{a} doymus mu?", cls_a <= {'a'})

# %% [markdown]
"""
```text
q(a) = ['a', 'b']
q(b) = ['a', 'b']
q(c) = ['c']
q(d) = ['d']
a'nin sinifi: ['a', 'b']
{a,b} doymus mu? True
{a} doymus mu? False
```

`{a, b}` doymuştur (a'nın sınıfı `{a, b}` tamamen içeride), ama `{a}` doymuş
değildir: a'yı içeriyor ama sınıf arkadaşı b'yi içermiyor. Bölüm topolojisinin
açık kümeleri ancak doymuş açık kümelerden gelir.
"""

# %% [markdown]
"""
### Örnek 5.9 — Sınıflardan Noktalara: Round-Trip

`equivalence_from_classes` doğrudan sınıf bloklarından bir denklik bağıntısı
kurar; `partition_from_equivalence` ise bağıntıyı tekrar bölüntüye çevirir.
Bu ileri-geri dönüşüm, "denklik sınıfları ile bölüm uzayının noktaları"
yazışmasını somutlaştırır.
"""

# %%
rt_blocks = equivalence_from_classes([1, 2], [3], [4, 5])
print("Denklik bağıntısı mı?", is_equivalence_relation([1, 2, 3, 4, 5], rt_blocks))

rt_part = partition_from_equivalence([1, 2, 3, 4, 5], rt_blocks)
print("Geri kazanılan blok sayısı:", len(rt_part))
print("Bloklar:", sorted(sorted(b) for b in rt_part))
print("Özet:", finite_quotient_summary([1, 2, 3, 4, 5],
                                        [sorted(b) for b in rt_part]))

# %% [markdown]
"""
```text
Denklik bağıntısı mı? True
Geri kazanılan blok sayısı: 3
Bloklar: [[1, 2], [3], [4, 5]]
Özet: quotient: status=true, carrier=5, blocks=3
```

Sınıflardan kurulan bağıntı, bölüntüye çevrilip geri okunduğunda aynı üç bloğu
verir: bölüm uzayının 3 noktası, tam olarak 3 denklik sınıfına karşılık gelir.

---
"""

# %% [markdown]
"""
## 6. Alıştırmalar
"""

# %% [markdown]
"""
### Kodlama

K1. `discrete_topology(0, 1, 2, 3, 4)` üzerinde `[[0,4],[1,3],[2]]` bölüntüsünü
    kullanarak `finite_quotient_contract` çağırın; blok sayısını ve boyutlarını yazdırın.

K2. `sierpinski_space()` üzerinde her noktanın kendi sınıfı olduğu (trivial) bölüntü ile
    `finite_quotient_summary` çağırın; çıktıyı yorumlayın.

K3. `make_topology([1,2,3,4], set(), {1,2}, {3,4}, {1,2,3,4})` üzerinde
    `[[1,2],[3,4]]` ve `[[1],[2],[3],[4]]` bölüntülerini karşılaştırın.

K4. `[0,1,2,3,4,5]` taşıyıcısı üzerinde `[[0,5],[1],[2],[3],[4]]` bölüntüsünü
    `equivalence_from_partition` ile denklik bağıntısına çevirin; `is_equivalence_relation`
    ile doğrulayın ve 0 ile 5'in `equivalence_class` çıktılarının aynı olduğunu gösterin.
    (Bu, daha uzun bir şeridin uçlarını yapıştırmaya karşılık gelir.)

K5. `['x','y','z']` taşıyıcısı ve `[['x','y'],['z']]` bölüntüsü için
    `canonical_projection_from_equivalence` çağırıp her noktanın görüntüsünü yazdırın.
    Ardından `{'x','y'}` kümesinin doymuş, `{'x'}` kümesinin doymuş **olmadığını**
    `equivalence_class` ile kontrol edin.
"""

# %% [markdown]
"""
### Teori

T1. q: X → X/~ bölüm haritasının τ_{X/~} tanımı gereği her zaman sürekli olduğunu
    ispatlayın.

T2. X bağlantılı ise X/~ bağlantılıdır; q sürekli ve q(X) = X/~ olduğundan
    bağlantılı kümenin sürekli görüntüsü bağlantılıdır. Bu argümanı formalize edin.

T3. Bölüm haritasının **evrensel özelliğini** ispatlayın: g: X/~ → Z için
    g sürekli ⟺ g ∘ q sürekli. (İpucu: bölüm topolojisinin tanımıyla
    (g ∘ q)⁻¹(V) = q⁻¹(g⁻¹(V)) eşitliğini birleştirin.)

T4. A ⊆ X **doymuş** (A = q⁻¹(q(A))) ise q(A)'nın bölüm uzayında açık olması için
    A'nın X'te açık olmasının yeterli ve gerekli olduğunu gösterin. Doymamış bir A
    için bu yazışmanın neden bozulduğunu açıklayın.
"""
