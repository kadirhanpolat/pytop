# Complete metric-space examples bank — v1.0.279

Bu dosya Chapter 14 için complete metric-space örnek bankası iskeletini açar. Amaç, dış kaynaklardan doğrudan problem veya cümle kopyalamadan, `pytop` içinde hâlihazırda desteklenen sonlu metrik, sembolik metrik ve örnek-etiket yüzeyleriyle uyumlu **küçük, izlenebilir ve test edilebilir** örnek aileleri kurmaktır.

## Kapsam ilkesi

Bu sürüm genel bir Cauchy dizi üreticisi, keyfî metrik uzay tamlık karar vericisi veya tamamlanma inşa motoru eklemez. Tamlık bu sürümde yalnız aşağıdaki güvenli yüzeylerde kullanılır:

- sonlu metrik uzaylarda tamlık için sonlu-taşıyıcı benchmark;
- `real_line_metric()`, `closed_unit_interval_metric()` ve `real_plane_metric()` için açık `complete` etiketi;
- `rationals_metric()` için açık `not_complete` etiketi;
- Cauchy fakat uzay içinde yakınsamayan rasyonel yaklaşıklar için sayısal warning-line;
- kompakt metrik, tam metrik, totally bounded ve tamamlanma kavramlarını karıştırmamak için kontrollü açıklamalar;
- eşdeğer metriklerin topolojiyi koruyabileceği, fakat tamlığı otomatik olarak korumayacağı uyarısı.

Aşağıdaki `CM-*` aileleri evrensel theorem-prover değil, ders anlatımı ve otomatik test için kullanılan sözleşme örnekleridir.

## Test edilebilir örnek aileleri

### CM-01 — Sonlu metrik uzaylar tamdır

- **Uzay:** üç noktalı bir sonlu metrik uzay.
- **Beklenen davranış:** her Cauchy davranışı sonunda sabitleşir; bu nedenle sonlu metrik uzay tamdır.
- **pytop sözleşmesi:** `FiniteMetricSpace` üzerinde metrik aksiyomları `validate_metric` ile doğrulanır; tamlık sonucu örnek-bank sözleşmesinde sonlu-taşıyıcı kuralı olarak okunur.
- **Pedagojik vurgu:** Sonlu metrik uzaylarda tamlık, kompaktlık ve ayrıklık birlikte görünür; fakat bu üç kavram genel uzaylarda aynı şey değildir.

### CM-02 — Reel doğru tam fakat kompakt değildir

- **Uzay:** `real_line_metric()`.
- **Beklenen davranış:** `complete`, `connected`, `path_connected`, `second_countable`, `separable`, `lindelof` ve `not_compact` etiketlerini taşır.
- **pytop sözleşmesi:** reel doğru benchmarkı tamlık ve kompaktlık ayrımını aynı örnekte görünür kılar.
- **Pedagojik vurgu:** Tamlık, sınırlılık veya kompaktlık anlamına gelmez.

### CM-03 — Kapalı birim aralık kompakt metrik benchmarktır

- **Uzay:** `closed_unit_interval_metric()`.
- **Beklenen davranış:** `compact` ve `complete` etiketleri birlikte taşınır.
- **pytop sözleşmesi:** kapalı aralık örneği, kompakt metrik uzayların tamlık sezgisini güvenli biçimde temsil eder.
- **Pedagojik vurgu:** Bu örnek, Heine--Borel hattını doğrudan ispatlamaz; yalnız kitap ve test yüzeyi için güvenli benchmark sağlar.

### CM-04 — Öklid düzlemi tam fakat kompakt değildir

- **Uzay:** `real_plane_metric()`.
- **Beklenen davranış:** `complete`, `connected`, `path_connected`, `second_countable`, `separable`, `lindelof` ve `not_compact` etiketlerini taşır.
- **pytop sözleşmesi:** düzlem benchmarkı, sonsuz boyut iddiası olmadan çok değişkenli metrik sezgi verir.
- **Pedagojik vurgu:** Düzlemin tamlığı, kapalı ve sınırlı altkümeler üzerine yapılacak daha sonraki tartışmalar için hazırlık sağlar.

### CM-05 — Rasyoneller eksik metrik altuzaydır

- **Uzay:** `rationals_metric()`.
- **Beklenen davranış:** `not_complete`, `second_countable`, `separable` ve `not_compact` etiketlerini taşır.
- **pytop sözleşmesi:** `Q` içinde `sqrt(2)`'ye yaklaşan rasyonel diziler Cauchy sezgisi verir, fakat limit `Q` içinde değildir.
- **Pedagojik vurgu:** Yoğun olmak tam olmak değildir; rasyoneller reel doğru içinde yoğundur ama kendi olağan metriğiyle tam değildir.

### CM-06 — Cauchy tanığı sayısal olarak izlenebilir olmalıdır

- **Tanık:** `sqrt(2)` için ondalık kesmeler veya rasyonel alt/üst yaklaşıklar.
- **Beklenen davranış:** ardışık farklar küçülür; fakat hedef değer rasyonel uzay elemanı olarak kabul edilmez.
- **pytop sözleşmesi:** testler bu örneği tam ispat motoru olarak değil, eksiklik warning-line'ı olarak sayısal yaklaşımla kontrol eder.
- **Pedagojik vurgu:** Cauchy olmak, “bir şeye yaklaşıyor gibi olmak”tır; tamlık ise o şeyin uzayın içinde kalmasını ister.

### CM-07 — Topolojik eşdeğerlik tamlığı otomatik korumaz

- **Model:** `R` ile `(0,1)` homeomorfiktir; fakat olağan metrikle `(0,1)` tam değildir.
- **Beklenen davranış:** topolojik benzerlik ve metrik tamlık ayrı katmanlarda tutulur.
- **pytop sözleşmesi:** bu sürümde yalnız warning-line metni ve testte anahtar ifadeler doğrulanır; genel homeomorfizm motoru eklenmez.
- **Pedagojik vurgu:** Tamlık topolojik değil metrik/uniform bir özelliktir.

### CM-08 — Complete + totally bounded => compact hattı ayrı faza bırakılır

- **Model:** kapalı birim aralık pozitif benchmark, reel doğru negatif boundedness uyarısıdır.
- **Beklenen davranış:** `complete` ve `compact` etiketleri görülebilir; fakat totally bounded karar vericisi bu sürümde açılmaz.
- **pytop sözleşmesi:** total boundedness, compactness ve completeness arasındaki bağ sonraki API/generator fazlarında açık gereksinim olarak kalır.
- **Pedagojik vurgu:** Öğrencinin “tam + sınırlı = kompakt” gibi yanlış genellemeye gitmesi özellikle engellenmelidir.

## Sınır notu

Bu dosya complete metric-space örnek yüzeyini açar; fakat keyfî metrik uzay için Cauchy dizisi sınıflandıran, tamamlanma üreten veya total boundedness karar veren tam bir modül değildir. Bu tür genelleştirmeler daha sonraki API planlama ve generator fazlarında ayrıca ele alınmalıdır.

## v0.1.47 note

Bu sürümde Chapter 15 ileri metrik hat için Cilt II tamlık-total sınırlılık-metrik kompaktlık koridoru eklendi. Tokenlar: completeness corridor table, totally bounded witness, metric compactness equivalence, is_complete, is_totally_bounded, metric_compactness_check, analyze_metric_completeness.
