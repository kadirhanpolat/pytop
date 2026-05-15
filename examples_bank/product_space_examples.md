# Product-space examples bank — v1.0.277

Bu dosya Chapter 12 için product-space örnek yüzeyini açar. Amaç, dış kaynaklardan doğrudan problem veya cümle kopyalamadan, `pytop` içinde hâlihazırda desteklenen sonlu ürün, sonlu metrik ürün ve sembolik ürün etiketleriyle uyumlu **küçük, izlenebilir ve test edilebilir** örnek aileleri kurmaktır.

## Kapsam ilkesi

Bu sürüm genel bir sonsuz çarpım uzayı karar vericisi eklemez. Özellikle keyfî indeks kümeleri üzerinde Tychonoff düzeyinde otomatik ispat motoru açılmaz. Bu dosya yalnız şu güvenli yüzeyleri örnek bankasına bağlar:

- sonlu topolojik uzayların ikili/sonlu ürün topolojisi;
- ayrık ve indiscrete sonlu faktörlerde ürün davranışı;
- sonlu metrik uzayların `max`, `sum` ve `euclidean` ürün metrikleri;
- sembolik sonsuz uzaylarda yalnız açıkça taşınan etiketlerin ürün yüzeyine aktarılması;
- connected, path-connected, compact, metric ve countability etiketlerinin hangi şartla kullanılacağına dair kontrollü uyarılar.

Bu nedenle aşağıdaki `PS-*` örnekleri doğrudan evrensel teorem motoru değil, ders anlatımı ve otomatik test için kullanılan sözleşme örnekleridir.

## Test edilebilir örnek aileleri

### PS-01 — İki sonlu ayrık uzayın ürünü

- **Faktörler:** iki adet iki noktalı ayrık uzay.
- **Beklenen taşıyıcı:** dört noktalı Kartezyen çarpım.
- **Beklenen topolojik davranış:** sonlu, kompakt, Hausdorff ve bağlantısız.
- **pytop sözleşmesi:** `binary_product(two_point_discrete_space(), two_point_discrete_space())` sonlu ürün uzayı üretir; `is_compact` doğru, `is_connected` yanlış ve `is_hausdorff` doğru sonuç vermelidir.
- **Pedagojik vurgu:** Ürün uzayının noktaları sıralı ikilerdir; topoloji yalnız taşıyıcı çarpımı değil, açık dikdörtgenlerden üretilen yapıdır.

### PS-02 — İki sonlu indiscrete uzayın ürünü

- **Faktörler:** iki adet iki noktalı indiscrete uzay.
- **Beklenen davranış:** ürün yine yalnız boş küme ve tüm uzay dışında açık üretmez; bu nedenle bağlantılıdır fakat Hausdorff değildir.
- **pytop sözleşmesi:** ürünün topolojisi iki açık kümeden oluşmalı; `is_connected` doğru, `is_hausdorff` yanlış dönmelidir.
- **Pedagojik vurgu:** Ürün işlemi ayrılabilirliği otomatik olarak iyileştirmez; zayıf faktörlerden güçlü ayırma aksiyomu beklenmemelidir.

### PS-03 — Ayrık × indiscrete ürününde açık şeritler

- **Faktörler:** bir iki noktalı ayrık uzay ve bir iki noktalı indiscrete uzay.
- **Beklenen davranış:** ürün, birinci koordinata göre iki açık şerit üretir ve bağlantılı olmak zorunda değildir.
- **pytop sözleşmesi:** ürün uzayında `{'a'} × Y` ve `{'b'} × Y` tipinde açık parçalar görünür; `is_connected` yanlış olmalıdır.
- **Pedagojik vurgu:** Product topology, faktörlerdeki açıkların dikdörtgensel kombinasyonunu izler. Bu örnek, bir faktörün ayrık olmasının ürüne nasıl keskin ayırımlar taşıyabildiğini gösterir.

### PS-04 — Sonlu metrik ürünlerinde üç güvenli metrik modu

- **Faktörler:** açıkça verilen iki sonlu metrik uzay.
- **Metrik modları:** `max`, `sum`, `euclidean`.
- **Beklenen davranış:** her üç modda da metrik aksiyomları sonlu taşıyıcı üzerinde doğrulanabilir.
- **pytop sözleşmesi:** `finite_product_metric_space(left, right, mode=...)` ürün taşıyıcıyı kurmalı, beklenen uzaklık değerlerini vermeli ve `validate_metric` doğru/exact dönmelidir.
- **Pedagojik vurgu:** Aynı Kartezyen taşıyıcı üzerinde birden çok doğal ürün metriği kurulabilir; bu metrikler aynı topolojik sezgiye hizmet edebilir ama uzaklık değerleri aynı olmak zorunda değildir.

### PS-05 — Sembolik metrik ve bağlantılı ürün köprüsü

- **Faktörler:** olağan metrik topolojiyle iki sembolik gerçek doğru kopyası.
- **Beklenen davranış:** ürün yüzeyi metric, connected ve path_connected etiketlerini taşır.
- **pytop sözleşmesi:** `infinite_constructions.product(real_line_metric(), real_line_metric())` sonucu `metric`, `connected` ve `path_connected` etiketlerine sahip olmalıdır.
- **Pedagojik vurgu:** Bu sürümde ürünün tüm açık kümeleri materyalize edilmez; güvenli bilgi, faktörlerin ortak taşıdığı etiketlerden gelir.

### PS-06 — Kompakt ürün etiketi ve Tychonoff sınırı

- **Faktörler:** iki adet kapalı birim aralık sembolik metrik modeli.
- **Beklenen davranış:** sonlu ürün yüzeyi `compact` etiketi taşır ve mevcut compactness analizörü bunu desteklenen bir sonuç olarak okuyabilir.
- **pytop sözleşmesi:** `product(closed_unit_interval_metric(), closed_unit_interval_metric())` sonucu `compact` etiketi taşımalı; `is_compact` olumsuz dönmemelidir.
- **Pedagojik vurgu:** Bu örnek yalnız sonlu sembolik ürün hattıdır. Keyfî ürünlerde kompaktlık için ayrı teorem, varsayım ve kanıt yönetimi gerekir.

### PS-07 — İkinci sayılabilirlik ve ürün etiketi

- **Faktörler:** iki adet ikinci sayılabilir sembolik metrik uzay.
- **Beklenen davranış:** ürün yüzeyi second_countable etiketini taşır.
- **pytop sözleşmesi:** iki gerçek doğru kopyasının sembolik ürünü `second_countable` ve `metric` etiketlerini birlikte taşımalıdır.
- **Pedagojik vurgu:** Bu dosya countability örnek bankasıyla ürün uzaylarını birbirine bağlar; fakat sayılamaz indeksli ürünlerde aynı sonucun otomatik geçerli olduğu söylenmemelidir.

### PS-08 — Ürün işleminin güvenli giriş sınırı

- **Durum:** boş faktör listesi veya desteği belirtilmemiş keyfî ürün.
- **Beklenen davranış:** bu sürümde boş ürün sessizce üretilmez; belirsiz keyfî ürünlerde sonuç yalnız metadata/etiket seviyesinde tutulur.
- **pytop sözleşmesi:** `product()` çağrısı hata vermelidir; desteklenmeyen sonsuz ürünlerde otomatik “kanıtlanmış” sonuç iddiası kurulmaz.
- **Pedagojik vurgu:** Öğrenciye önce sonlu ürün ve açık dikdörtgen mantığı öğretilmeli; sonra keyfî ürünler için indeks kümesi, altbaz, kutu topolojisi ve ürün topolojisi ayrımı ayrı başlık olarak açılmalıdır.

## Kullanım notu

Bu dosyadaki örnekler problem üretiminde `PS-*` kodlarıyla çağrılmalıdır. Her problemde faktör uzayları, ürün türü, beklenen özellikler ve geçerli olmayan aşırı genelleme açıkça yazılmalıdır. Özellikle “Kartezyen çarpım”, “ürün topolojisi”, “kutu topolojisi” ve “ürün metriği” ifadeleri birbirinin yerine kullanılmamalıdır.
