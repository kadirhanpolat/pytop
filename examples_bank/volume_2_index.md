# Volume II example-bank index

Bu dosya, Cilt II örnek bankasını yalnız dosya listesi olarak değil, **bölüm amacı / kullanılacak standart uzay / gösterilen ayrım / ilgili örnek dosyası** eksenlerinde okumak için hazırlanmıştır.

## Ana kaynak dosyalar

- `standard_spaces.md`
- `counterexamples.md`
- `neighborhoods_nets_filters_examples.md`
- `separation_compactification_metrization_examples.md`
- `compactification_examples.md`
- `metrization_examples.md`
- `quantitative_topology_examples.md`
- `basic_invariants_examples.md`
- `cardinal_number_examples.md`
- `ordinal_examples.md`
- `cofinality_regularity_examples.md`
- `cardinal_functions_framework_examples.md`
- `basic_cardinal_functions_examples.md`
- `properties_cardinal_functions_links_examples.md`

## Bölüm bazlı amaç haritası

| Bölüm | Ana amaç | Standart uzay / örnek ailesi | Gösterilen ayrım | Ana örnek bankası dosyaları |
|---|---|---|---|---|
| 18--20 | komşuluk, ağ, süzgeç dilini dizi sezgisinin ötesine taşımak | ayrık uzaylar, indiscrete uzay, kofinite/cocountable örnekler, reel doğru, sonlu uzaylar | dizi ile ağ/süzgeç yaklaşımının farkı; yerel veri ile global yakınsaklık farkı | `neighborhoods_nets_filters_examples.md`, `standard_spaces.md`, `counterexamples.md` |
| 21 | ileri ayırma sonuçlarının neden ek varsayım istediğini göstermek | Sierpiński uzayı, kofinite topoloji, metrik uzaylar | `T_0`, `T_1`, Hausdorff ve normal davranışların ayrımı | `separation_compactification_metrization_examples.md`, `standard_spaces.md`, `counterexamples.md` |
| 22 | yerel kompaktlık ile kompaktlaştırma arasındaki köprüyü görünür kılmak | \(\mathbb{R}\), yerel kompakt Hausdorff örnekler, bir-nokta kompaktlaştırma örnekleri | yerel kompaktlık ile global kompaktlığın aynı şey olmaması | `separation_compactification_metrization_examples.md`, `compactification_examples.md`, `standard_spaces.md` |
| 23 | metrikleşebilirlik için olumlu/olumsuz yönleri görmek | \(\mathbb{R}\), sayılabilir tabanlı metrik uzaylar, metrik olmayan iyi uzaylar | sayılabilirlik + ayırma ile metrikleşebilirlik arasındaki ilişki | `separation_compactification_metrization_examples.md`, `metrization_examples.md`, `counterexamples.md`, `standard_spaces.md` |
| 24 | nitel özelliklerden nicel sorulara geçmek | reel doğru, sonsuz ayrık uzay, indiscrete uzay, sonlu uzaylar | “özellik var mı?” ile “en küçük veri ne kadar büyük?” ayrımı | `quantitative_topology_examples.md`, `standard_spaces.md` |
| 25 | ilk nicel katalogu kurmak | \(\mathbb{R}\), \(\mathbb{Q}\), sonsuz ayrık uzay, kofinite topoloji, sonlu uzaylar | küçük karakter / büyük yoğunluk; küçük taban / zengin topoloji | `basic_invariants_examples.md`, `counterexamples.md`, `standard_spaces.md` |
| 26 | kardinal büyüklük dilini yerleştirmek | \(\mathbb{N}, \mathbb{Z}, \mathbb{Q}, \mathbb{R}\), interval bijeksiyonları, cebirsel/transandant sayı ayrımı ve kuvvet kümesi örnekleri | sayılabilir / sayılamaz; eşgüçlü gerçek altküme; yoğunluk ile kardinal büyüklük ayrımı; iki yönlü gömü ve strict power-set growth | `cardinal_number_examples.md`, `standard_spaces.md` |
| 27 | ordinal düzen tipini kardinal büyüklükten ayırmak | sonlu ordinals, \(\omega\), \(\omega+1\), limit ordinals | sıra tipi ile salt büyüklük ayrımı | `ordinal_examples.md`, `cardinal_number_examples.md` |
| 28 | kofinalite ve düzenlilik dilini kardinal fonksiyon hazırlığına bağlamak | \(\omega\), \(\omega_1\), düzenli/tekil kardinal şemaları | limit büyüme ile düzenli/tekil ayrımı | `cofinality_regularity_examples.md`, `ordinal_examples.md` |
| 29 | kardinal fonksiyonların ortak çerçevesini kurmak | reel doğru, ayrık uzaylar, sonlu uzaylar, ağ-taban karşılaştırmaları | nitel özellik ile nicel değişmez ayrımı; noktasal/genel okuma ayrımı | `cardinal_functions_framework_examples.md`, `basic_invariants_examples.md`, `quantitative_topology_examples.md` |
| 30 | temel kardinal fonksiyonları somutlaştırmak | \(\mathbb{R}\), \(\mathbb{Q}\), sonsuz ayrık uzay, metrik uzaylar, cocountable örnekler | `w(X)`, `d(X)`, `\chi(X)`, `L(X)`, `nw(X)` ayrımları | `basic_cardinal_functions_examples.md`, `basic_invariants_examples.md`, `cardinal_functions_framework_examples.md`, `standard_spaces.md` |
| 31 | nitel özellikleri sayılabilir eşiklerle yeniden okumak | \(\mathbb{R}\), \(\mathbb{Q}\), sonsuz ayrık metrik uzaylar, cocountable topolojiler | ikinci sayılabilirlik/ağırlık, ayrılabilirlik/yoğunluk, birinci sayılabilirlik/karakter, Lindelöf/Lindelöf sayısı | `properties_cardinal_functions_links_examples.md`, `basic_cardinal_functions_examples.md`, `quantitative_topology_examples.md`, `standard_spaces.md` |

## 18--23 hattı için editöryal dengeleme notu

- `v0.6.15` itibarıyla Cilt II'nin açılış ve orta hattı da artık açık örnek-bankası merkezlerine bağlanmıştır.
- Böylece `18--23` bölümleri yalnız bölüm içi örneklerle değil, ortak standart uzay havuzu ve karşı-örnek uyarılarıyla birlikte okunabilir.
- Bu dengeleme, `v0.6.16` sonrası planlanan exploration/teaching notebook ailesi için doğrudan hazırlık işlevi görür.

## 24--31 hattı için çekirdek örnek kümeleri

### 1. Reel doğru ve rasyoneller
- \(\mathbb{R}\) ve \(\mathbb{Q}\), Cilt II'nin nicel hattında **sayılabilir taban**, **sayılabilir yoğun altküme** ve **Lindelöf davranışı** için temel olumlu modeldir.
- Özellikle Bölüm 24, 25, 30 ve 31'de bu ikili tekrar tekrar kullanılmalıdır.

### 2. Sonsuz ayrık uzay ailesi
- Küçük yerel taban / büyük yoğunluk ayrımını görünür kılar.
- Karakterin küçük, ama ağırlık ve yoğunluğun büyük olabildiğini açıkça göstermesi bakımından Bölüm 25, 30 ve 31 için ana kaynaktır.

### 3. İndiscrete, kofinite ve cocountable örnekler
- “az açık küme” ile “küçük nicel veri” arasındaki sezgiyi başlatır.
- Ayrılabilirlik, Lindelöf benzeri davranış ve ayırma aksiyomları arasındaki gerilimleri göstermek için kullanılır.

### 4. Sonlu uzaylar
- Nicel topoloji hattının hesaplamalı laboratuvarıdır.
- Özellikle `pytop.invariants` köprüsü kurulan bölümlerde, soyut niceliklerin sonlu uzaylarda gerçekten hesaplanabilir olduğunu gösterir.

## Bölüm yazımı için kullanım ilkesi

Bu indeksin amacı, her bölüm dosyasına örnekleri yeniden kopyalamak değildir. Amaç:
- hangi bölümde hangi örnek dosyasının ana başvuru merkezi olduğunu,
- hangi standart uzayın hangi ayrımı taşımak için seçileceğini,
- ve örnek bankasının manuskript içinde nerede görünür hale getirilmesi gerektiğini
tek bakışta göstermektir.

## v0.6.13 integration note

Bu sürümde `volume_2_index.md` artık yalnız “hangi dosya var” listesi değildir. Dosya, özellikle Bölüm `24--31` hattı için **amaç-uzay-ayrım** haritasına çevrilmiştir. Böylece örnek bankası, nicel topoloji ve kardinal fonksiyon hattında gerçek bir yönlendirme merkezi olarak kullanılabilir hale gelmeye başlamıştır.

## v0.6.15 integration note

Bu sürümde aynı indeks, `18--23` hattını da açık örnek-bankası merkezlerine bağlayacak biçimde genişletildi. Böylece Cilt II genelinde bölüm açılışları, örnek seçimi ve sonraki notebook açılımı için daha dengeli bir editöryal taban kurulmuş oldu.

## v0.6.16 notebook opening note

Bu sürümde `18--20` hattı için ilk exploration notebook ailesi açıldı:

- `notebooks/exploration/10_neighborhood_systems.ipynb`
- `notebooks/exploration/11_nets.ipynb`
- `notebooks/exploration/12_filters.ipynb`

Böylece Cilt II örnek bankasının açılış hattı artık yalnız bölüm dosyalarına değil, doğrudan kullanılabilir küçük deney not defterlerine de bağlanmış oldu.

## v0.6.18 notebook opening note

Bu sürümde `24--28` hattı için ikinci Cilt II exploration notebook ailesi açıldı:

- `notebooks/exploration/13_quantitative_topology.ipynb`
- `notebooks/exploration/14_basic_topological_invariants.ipynb`
- `notebooks/exploration/15_cardinal_numbers.ipynb`
- `notebooks/exploration/16_ordinals.ipynb`
- `notebooks/exploration/17_cofinality_and_regularity.ipynb`

Böylece Cilt II'nin nicel topoloji ve kardinal hazırlık bandı da gerçek not defterleriyle desteklenmiş oldu.

## v0.6.19 notebook opening note

Bu sürümde `29--31` hattı için ilk gerçek teaching + counterexample notebook ailesi açıldı:

- `notebooks/teaching/lesson_11_cardinal_functions_framework.ipynb`
- `notebooks/exploration/22_cardinal_functions_framework.ipynb`
- `notebooks/teaching/lesson_12_basic_cardinal_functions.ipynb`
- `notebooks/teaching/lesson_13_properties_and_cardinal_functions.ipynb`
- `notebooks/counterexamples/small_character_large_weight.ipynb`
- `notebooks/counterexamples/countable_threshold_failures.ipynb`

Böylece Cilt II örnek bankasının kardinal fonksiyon bandı da artık yalnız bölüm dosyaları ve örnek notlarıyla değil, doğrudan öğretim ve karşı-örnek not defterleriyle okunabilir hale geldi.


## v0.7.0 threshold note

Bu indeks artık yalnız Cilt II içi gezinme dosyası olarak değil; notebook, assessment ve glossary zinciriyle birlikte çalışan bir referans yüzeyi olarak ele alınır. `v0.7.0` audit adımı, özellikle şu notebook eşleşmelerini de doğrular:

- `notebooks/exploration/17_cofinality_and_regularity.ipynb`
- `notebooks/teaching/lesson_13_properties_and_cardinal_functions.ipynb`
- `manuscript/volume_2/quick_checks/main.tex`
- `manuscript/volume_2/quick_checks/quiz_forms/main.tex`
- `manuscript/volume_2/quick_checks/answer_keys/main.tex`


## v0.7.6 bridge audit note

Bu sürümde Cilt II indeks dosyası, named bridge rotalarının orta düğümü olarak da okunur. Özellikle **Separation-to-warning route** ve **Sequence/filter/research route** bu dosyanın notebook/example-bank eşleşmeleri üzerinden izlenebilir hale getirildi.


## v0.8.60 metrization exploration note

Bu sürümde Bölüm 23 için exploration companion da açıldı:

- `notebooks/exploration/21_metrization_directions.ipynb`

Böylece metrikleşebilirlik bandı artık yalnız teaching notebook ile değil, olumlu/olumsuz sinyallerin küçük görevlerle karşılaştırıldığı bir exploration yüzeyiyle de desteklenmiş oldu.


## v0.8.61 cardinal-framework exploration note

Bu sürümde `Chapter 29 — Cardinal Functions Framework` için gerçek bir exploration companion açıldı:

- `notebooks/exploration/22_cardinal_functions_framework.ipynb`

Böylece `29--31` hattı artık yalnız teaching + counterexample yüzeyiyle değil; Chapter 29'un eşik dilini daha yavaş okutan küçük bir keşif not defteriyle de desteklenmiş oldu.


## v0.8.76 notebook stabilization note

Bu sürümde Cilt II curated bundle hattındaki son iki notebook eşiği de kapatıldı:

- `notebooks/teaching/lesson_16b_filters.ipynb`
- `notebooks/exploration/24_basic_cardinal_functions.ipynb`

Böylece Bölüm 20 artık exploration + teaching ikilisiyle, Bölüm 30 ise teaching + exploration ikilisiyle okunabilir hale geldi; curated chapter bundle recommendation hattında artık growth-ready düğüm kalmadı.


## v1.0.50 Chapter 28 pedagogy note

Bu sürümle `notebooks/exploration/17_cofinality_and_regularity.ipynb` artık dedicated worksheet / quick-check / teaching notebook zinciriyle de bağlanmıştır:

- `manuscript/volume_2/worksheets/03c_cofinality_regularity.md`
- `manuscript/volume_2/quick_checks/03c_cofinality_regularity.tex`
- `notebooks/teaching/lesson_10d_cofinality_and_regularity.ipynb`

Böylece Cilt II Chapter 28 hattı örnek-bankası bakımından da notebook-only durumundan çıkmıştır.
## v0.1.137 geometric examples-bank consolidation note

Geometric topology examples are now discoverable through `examples_bank/geometric_topology_index.md`. This route-level index is the canonical entry point for `GEO-01`--`GEO-08` examples and avoids copying the same examples across volume indexes.
