# Connectedness examples bank — v1.0.278

Bu dosya Chapter 13 için connectedness örnek yüzeyini açar. Amaç, dış kaynaklardan doğrudan problem veya cümle kopyalamadan, `pytop` içinde hâlihazırda desteklenen sonlu topoloji, sonsuz aile etiketi ve sembolik metrik uzay yüzeyleriyle uyumlu **küçük, izlenebilir ve test edilebilir** örnek aileleri kurmaktır.

## Kapsam ilkesi

Bu sürüm genel bağlantılılık karar vericisi eklemez. Özellikle keyfî topolojik uzaylarda yol bağlantılılık, yerel bağlantılılık veya bileşen ayrıştırması için evrensel bir ispat motoru açılmaz. Bu dosya yalnız şu güvenli yüzeyleri örnek bankasına bağlar:

- sonlu açık-küme listesi verilen uzaylarda nontrivial clopen altküme kontrolü;
- iki noktalı ayrık / indiscrete / Sierpinski benchmark aileleri;
- partition topology ve açık-kapalı blok uyarıları;
- sonsuz discrete, indiscrete, cofinite ve cocountable ailelerde açıkça kodlanmış sınıf etiketleri;
- metrik reel doğru, kapalı birim aralık ve düzlem gibi sembolik benchmarklarda yalnız taşınan `connected` ve `path_connected` etiketleri;
- ürün ve ayrık toplam örnekleri için yalnız mevcut inşa etiketlerinin izin verdiği sınırlı okuma.

Aşağıdaki `CN-*` örnekleri evrensel theorem-prover değil, ders anlatımı ve otomatik test için kullanılan sözleşme örnekleridir.

## Test edilebilir örnek aileleri

### CN-01 — İki noktalı indiscrete uzay

- **Uzay:** `{a,b}` üzerinde yalnız `∅` ve tüm küme açık.
- **Beklenen davranış:** nontrivial clopen altküme yoktur; uzay bağlantılıdır.
- **pytop sözleşmesi:** `two_point_indiscrete_space()` için `is_connected` doğru sonuç vermelidir.
- **Pedagojik vurgu:** Bağlantılılık, noktaların çokluğu ile değil açık-kapalı ayırmanın varlığıyla ilgilidir.

### CN-02 — İki noktalı ayrık uzay

- **Uzay:** `{a,b}` üzerinde tüm altkümeler açık.
- **Beklenen davranış:** `{a}` ve `{b}` aynı anda açık-kapalıdır; uzay bağlantısızdır.
- **pytop sözleşmesi:** `two_point_discrete_space()` için `is_connected` yanlış sonuç vermelidir.
- **Pedagojik vurgu:** Ayrık topoloji bağlantılılığı hemen kırar; tek noktalı istisna ayrıca ele alınmalıdır.

### CN-03 — Sierpinski uzayı bağlantılıdır

- **Uzay:** `{0,1}` üzerinde `∅`, `{1}`, `{0,1}` açık.
- **Beklenen davranış:** `{1}` açık olsa da tümleyeni açık değildir; nontrivial clopen ayırma yoktur.
- **pytop sözleşmesi:** `sierpinski_space()` için `is_connected` doğru sonuç vermelidir.
- **Pedagojik vurgu:** T0 olmak bağlantısız olmak anlamına gelmez.

### CN-04 — Partition topology içinde blok ayırma

- **Uzay:** iki bloklu sonlu partition topology.
- **Beklenen davranış:** Her blok açık-kapalıdır; uzay bağlantısızdır.
- **pytop sözleşmesi:** `partition_space([["a","b"], ["c"]])` için `is_connected` yanlış sonuç vermelidir.
- **Pedagojik vurgu:** Bölümleme topolojileri, clopen blok fikrini görünür kılar.

### CN-05 — Sonsuz ayrık uzay bağlantısızdır

- **Uzay:** doğal sayılar üzerinde ayrık topoloji.
- **Beklenen davranış:** Tekil kümeler açık-kapalı olduğundan bağlantılılık ve yol bağlantılılık başarısızdır.
- **pytop sözleşmesi:** `naturals_discrete()` için `is_connected_infinite` ve `is_path_connected_infinite` yanlış sonuç vermelidir.
- **Pedagojik vurgu:** Sonsuzluk tek başına bağlantılılık üretmez.

### CN-06 — Sonsuz indiscrete uzay bağlantılıdır

- **Uzay:** reel taşıyıcı üzerinde indiscrete topoloji.
- **Beklenen davranış:** nontrivial açık-kapalı altküme yoktur; bağlantılılık ve sembolik yol bağlantılılık etiketi pozitiftir.
- **pytop sözleşmesi:** `reals_indiscrete()` için `is_connected_infinite` ve `is_path_connected_infinite` doğru sonuç vermelidir.
- **Pedagojik vurgu:** Çok zayıf topoloji ayırmayı engelleyebilir; bu, Hausdorfflukla karıştırılmamalıdır.

### CN-07 — Cofinite ve cocountable warning-line

- **Uzaylar:** `N` üzerindeki cofinite topoloji ve `R` üzerindeki cocountable topoloji.
- **Beklenen davranış:** Her ikisi de `connected` etiketi taşır; fakat ayırma ve kompaktlık davranışları aynı değildir.
- **pytop sözleşmesi:** `naturals_cofinite()` ve `reals_cocountable()` için bağlantılılık doğru okunmalıdır.
- **Pedagojik vurgu:** Bağlantılılık örneği seçilirken aynı anda Hausdorffluk, kompaktlık ve sayılabilirlik aksiyomları da etiketlenmelidir.

### CN-08 — Metrik benchmarklarda etiketli bağlantılılık

- **Uzaylar:** reel doğru, kapalı birim aralık ve Öklid düzlemi.
- **Beklenen davranış:** Bu sembolik metrik benchmarklar `connected` ve `path_connected` etiketleri taşır.
- **pytop sözleşmesi:** `real_line_metric()`, `closed_unit_interval_metric()` ve `real_plane_metric()` için bağlantılılık sonucu pozitif okunmalıdır.
- **Pedagojik vurgu:** Bu sürüm, sürekli yol inşasını otomatik ispatlamaz; yalnız güvenli benchmark etiketlerini test eder.

## Sınır notu

Bu dosya connectedness yüzeyini açar; fakat bileşenleri hesaplayan, yol bileşenlerini çıkaran veya her topolojik uzay için bağlantılılık ispatı yapan tam bir modül değildir. Bu tür genelleştirmeler daha sonraki API planlama ve generator fazlarında ayrıca ele alınmalıdır.

## v0.1.44 note

Bu sürümde Chapter 13 için Cilt II bağlantılılık koridoru tablosu eklendi. Üç özellik (is_connected, is_path_connected, is_locally_connected) standart uzay ailesi üzerinde eşleştirildi. İleri varyantlar notu: yarı-bileşenler (quasi-components) Cilt III'e bırakıldı; bu bölümde connected_components ve path_components işlendi. analyze_connectedness tüm raporu tek çağrıda verir. Tokenlar: connectedness corridor table, advanced variants, connected_components, path_components, is_locally_connected, analyze_connectedness.
