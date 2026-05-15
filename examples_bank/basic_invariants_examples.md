# Basic topological invariants examples

Bu dosya, Cilt II Bölüm 25 için temel değişmez örneklerini toplar.

## Çekirdek nicelikler

- ağırlık \(w(X)\)
- yoğunluk \(d(X)\)
- karakter \(\chi(X)\)
- Lindelöf sayısı \(L(X)\)
- hücresellik \(c(X)\)
- yayılım \(s(X)\)
- ağ ağırlığı \(nw(X)\)

## Ana örnek ailesi

### Reel doğru \(\mathbb{R}\)
- sayılabilir taban;
- sayılabilir yoğun altküme;
- yerel tabanların sayılabilirliği.

**Verdiği mesaj:** birçok nicel küçüklüğün aynı uzayda birlikte görülebileceği temel olumlu model.

### Rasyoneller \(\mathbb{Q}\)
- sayılabilirlik ve yoğun altuzay rolü.

**Verdiği mesaj:** yoğunluk niceliğinin nasıl gerçek altuzaylarla ilişkilendiğini görünür kılar.

### Sonsuz ayrık uzay
- her nokta için küçük yerel taban;
- yoğunluk tüm uzayın kardinaline eşit.

**Verdiği mesaj:** `\chi(X)` ile `d(X)` ya da `w(X)` aynı büyüklükte olmak zorunda değildir.

### Sonlu uzaylar
- seçilmiş nicelikler doğrudan hesaplanabilir.

**Verdiği mesaj:** değişmez tanımları yalnız varoluşsal değil, gerçekten ölçülebilir olabilir.

### Kofinite / cocountable örnekler
- sayılabilirlik, ayırma ve örtü davranışları arasındaki gerilimler.

**Verdiği mesaj:** olumlu nitel özellikler ile küçük nicel eşikler arasında otomatik bir özdeşlik beklenmemelidir.

## Bölüm 25 için ayrım çiftleri

- küçük karakter / büyük yoğunluk
- küçük taban / zengin açık küme yapısı
- sayılabilir yerel veri / sayılabilir olmayan global denetim
- olumlu ayırma davranışı / olumsuz nicel kontrol

## `pytop.invariants` bağı

`pytop.invariants` katmanı seçilmiş sonlu uzaylarda şu nicelikler için doğrudan sonuç üretir:

- `weight`
- `density`
- `character`
- `lindelof_number`
- `cellularity`

Bu yüzden Bölüm 25'te soyut katalog ile hesaplamalı laboratuvar arasında doğal bir köprü kurulabilir.

## v0.6.18 notebook bridge

Bu dosya artık `notebooks/exploration/14_basic_topological_invariants.ipynb` için ana örnek havuzudur. Ağırlık, yoğunluk, karakter ve Lindelöf sayısı karşılaştırmaları notebook içinde tablosal olarak yeniden okunur.

## v0.1.41 Cilt II property-language bridge note

Bu dosya v0.1.41 ile Cilt II açılış hattının birincil değişmez örnek kaynağı olarak işaretlenmiştir. Her örnek artık iki katmanda okunmalıdır:

1. Özellik katmanı: uzay bağlı mı, kompakt mı, Hausdorff mu?
2. Değişmez katmanı: ağırlık, yoğunluk, yerel taban sayısı kaç?

Bu ayrım, undergraduate preservation route'un başlangıç noktasıdır ve Chapter 10'daki temel koruma tablosuyla doğrudan bağlantılıdır.

## v0.1.43 note

Sayılabilirlik koridoru köprüsü: Chapter 12 corridor table (is_first_countable, is_second_countable, is_separable, is_lindelof) ve metric bridge bu dosyaya eklendi. weight ve density cardinal fonksiyonları corridor tablosunun sayısal boyutunu verir; analyze_countability ise dört özelliği tek bir raporda birleştirir.

## v0.1.44 note

Bağlantılılık koridoru köprüsü: Chapter 13 corridor table (is_connected, is_path_connected, is_locally_connected) ve advanced variants notu (quasi-components deferred) bu dosyaya eklendi. connected_components ve path_components bileşen sayısını verir; analyze_connectedness tüm raporu birleştirir.

## v0.1.45 note

Kompaktlık koridoru köprüsü: Chapter 14 corridor table (is_compact, is_locally_compact, is_sigma_compact) ve finite-subcover witness notu bu dosyaya eklendi. heine_borel_check ve analyze_compactness araçları doğrulama katmanını tamamlar.

## v0.1.46 note

Diziler konumlandırma köprüsü: Chapter 16 sequences-nets-filters positioning table ve undergraduate convergence route notu bu dosyaya eklendi. sequence_converges_to ve analyze_sequences temel araçlardır; is_sequentially_compact ve sequence_cluster_point dizi yakınsaması ile kompaktlık arasındaki bağı kurar.

## v0.1.47 note

Tamlık-total sınırlılık-metrik kompaktlık koridoru köprüsü: Chapter 15 ileri metrik hat için completeness corridor table ve totally bounded witness notu bu dosyaya eklendi. is_complete, is_totally_bounded ve metric_compactness_check araçları, tamlık ile kompaktlık arasındaki metrik eşdeğerliği gösterir; analyze_metric_completeness tüm raporu birleştirir.

## v0.1.48 note

Temel koruma tablosu koridoru: beş özellik (bağlılık, kompaktlık, Hausdorff, T1, ikinci sayılabilirlik) için beş inşaatın (altuzay, sonlu çarpım, sayılabilir çarpım, bölüm, sürekli görüntü) koruma durumu bir tablo olarak kaydedildi. Tokenlar: basic preservation table, preservation corridor, preservation_table_lookup, preservation_table_row, preservation_table_column, analyze_preservation_table.


## v0.1.49 note

Temel karşı örnek atlası koridoru: CE-S-01...CE-S-06 ayrılma aksiyomları serisi ve CE-P-01...CE-P-10 koruma hatası serisi, iki katmanlı yapılandırılmış atlas olarak kaydedildi. CE-S serisi v0.1.42 CA-1...CA-6 ile eşleşir; CE-P serisi v0.1.48 koruma tablosundaki tüm "H" hücrelerini somutlaştırır. Tokenlar: counterexample atlas, CE-S-01, CE-P-01, counterexample_lookup, counterexample_atlas_by_layer, counterexample_atlas_by_property, counterexample_atlas_by_construction, analyze_counterexample_atlas, ATLAS_IDS.
