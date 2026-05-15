# Compactness examples bank — v1.0.276

Bu dosya Chapter 11 için kompaktlık örnek bankası iskeletidir. Amaç, dış kaynaklardan doğrudan cümle veya problem kopyalamadan, `pytop` içinde hâlihazırda desteklenen karar yüzeyleriyle uyumlu **küçük, test edilebilir ve genişletilebilir** örnek aileleri kurmaktır.

## Kapsam ilkesi

Bu sürüm genel bir sonsuz topolojik uzay kompaktlık karar vericisi eklemez. Bunun yerine şu kontrollü yüzeyleri örnek bankasına bağlar:

- sonlu topolojik uzaylarda kesin kompaktlık;
- açıkça etiketlenmiş metrik-benzeri uzaylarda kompakt / kompakt değil ayrımı;
- kofinite, kokountable, indiscrete ve infinite discrete gibi sembolik sonsuz aileler;
- Lindelöf, sayılabilir kompaktlık, ardışıl kompaktlık ve limit noktası kompaktlığı için mevcut API'nin desteklediği güvenli sınırlar.

Bu nedenle aşağıdaki örnekler, hem ders anlatımında hem de otomatik testte kullanılabilecek “sözleşme örnekleri” olarak okunmalıdır.

## Test edilebilir örnek aileleri

### CO-01 — Sonlu uzay kompaktlık zemini

- **Taşıyıcı:** `{a, b}`.
- **Topoloji:** `∅, {a, b}` veya sonlu taşıyıcı üzerindeki herhangi bir geçerli topoloji.
- **Beklenen sonuç:** kompakt.
- **pytop sözleşmesi:** `FiniteTopologicalSpace` ile temsil edilen her sonlu uzay için `is_compact` sonucu `true/exact` olmalıdır.
- **Pedagojik vurgu:** Sonlu uzaylarda açık örtü tanımı soyut görünse de altörtü seçimi sonlu bir kontrol problemine indirgenir.

### CO-02 — Sonlu uzayda güçlendirilmiş kompaktlık profili

- **Taşıyıcı:** tek veya çok elemanlı sonlu bir küme.
- **Beklenen sonuçlar:** kompakt, sayılabilir kompakt, ardışıl kompakt, limit noktası kompakt ve Lindelöf.
- **pytop sözleşmesi:** `analyze_compactness(space, property_name)` çağrıları bu beş özellik için `true/exact` dönmelidir.
- **Pedagojik vurgu:** Bu örnek, sonlu uzayların kompaktlık ailesindeki birçok özelliği otomatik olarak sağladığını gösterir; ancak bu durum sonsuz uzaylara doğrudan taşınmamalıdır.

### CO-03 — Sonsuz discrete uzayda kompaktlık uyarısı

- **Taşıyıcı:** `N` gibi sonsuz sayılabilir sembolik taşıyıcı.
- **Topoloji ailesi:** discrete.
- **Beklenen sonuç:** kompakt değil.
- **pytop sözleşmesi:** `DiscreteInfiniteSpace("N")` için `is_compact_infinite` sonucu `false/exact` olmalıdır.
- **Pedagojik vurgu:** Her noktanın tekil açık olması, sonsuz açık örtülerde sonlu altörtünün bozulabileceği en yalın uyarı hattıdır.

### CO-04 — Indiscrete sonsuz uzayda kompakt fakat ayrılabilirlik zayıf

- **Taşıyıcı:** sonsuz sembolik bir küme.
- **Topoloji ailesi:** indiscrete.
- **Beklenen sonuç:** kompakt ve Lindelöf.
- **pytop sözleşmesi:** `IndiscreteInfiniteSpace("X")` için `is_compact_infinite` ve `is_lindelof_infinite` sonuçları `true/exact` olmalıdır.
- **Pedagojik vurgu:** Kompaktlık tek başına Hausdorffluk veya T1 davranışı üretmez. Bu örnek, kompaktlığı ayırma aksiyomlarından bağımsız okumayı zorlar.

### CO-05 — Kofinite topolojide kompaktlık / Hausdorff ayrımı

- **Taşıyıcı:** `R` gibi sonsuz sembolik taşıyıcı.
- **Topoloji ailesi:** cofinite.
- **Beklenen sonuç:** kompakt; ancak genel olarak Hausdorff değil.
- **pytop sözleşmesi:** `CofiniteSpace("R")` için `is_compact_infinite` sonucu `true/exact` olmalıdır.
- **Pedagojik vurgu:** Bu aile, “kompakt + T1” ifadesinin Hausdorff sonucunu tek başına vermediğini görünür kılar.

### CO-06 — Kokountable topolojide Lindelöf / kompaktlık ayrımı

- **Taşıyıcı:** `R` gibi sayılamaz sembolik taşıyıcı.
- **Topoloji ailesi:** cocountable.
- **Beklenen sonuçlar:** Lindelöf; kompakt değil.
- **pytop sözleşmesi:** `CocountableSpace("R")` için `is_lindelof_infinite` sonucu `true/exact`, `is_compact_infinite` sonucu `false/exact` olmalıdır.
- **Pedagojik vurgu:** Lindelöf olmak kompaktlıkla aynı şey değildir; bu örnek iki örtü özelliğini birbirinden ayırmak için kullanılır.

### CO-07 — Metrik-benzeri uzayda açık negatif etiket

- **Taşıyıcı:** `R` veya benzeri sembolik metrik taşıyıcı.
- **Ek bilgi:** `not_compact` etiketi.
- **Beklenen sonuç:** kompakt değil.
- **pytop sözleşmesi:** `MetricLikeSpace("R", tags={"not_compact"})` için `is_compact` sonucu `false` olmalıdır.
- **Pedagojik vurgu:** Bu sürümde gerçek sayı doğrusunun tüm açık örtü ispatını otomatikleştirmek yerine, bilinen sınıflandırma açık ve test edilebilir bir etiket olarak temsil edilir.

### CO-08 — İkinci sayılabilirlikten Lindelöf köprüsü

- **Taşıyıcı:** basis-defined sembolik uzay.
- **Ek bilgi:** sayılabilir baz (`basis_size="aleph_0"`) veya `second_countable` etiketi.
- **Beklenen sonuç:** Lindelöf.
- **pytop sözleşmesi:** `BasisDefinedSpace(..., metadata={"basis_size": "aleph_0"})` için `is_lindelof` sonucu theorem-based `true` olmalıdır.
- **Pedagojik vurgu:** Bu örnek, Chapter 09 sayılabilirlik yüzeyi ile Chapter 11 kompaktlık/örtü özellikleri arasında güvenli bir köprü kurar.

## Kullanım notu

Bu dosyadaki örnekler doğrudan problem metni olarak değil, problem üretimi için yapı taşı olarak kullanılmalıdır. Bir soru ailesi üretileceğinde önce `CO-*` kodu seçilmeli, ardından taşıyıcı, topoloji ailesi, beklenen sonuç ve yanlış genelleme uyarısı açıkça belirtilmelidir.

## v0.1.45 note

Bu sürümde Chapter 14 için Cilt II kompaktlık koridoru tablosu eklendi. Üç özellik (is_compact, is_locally_compact, is_sigma_compact) standart uzay ailesi üzerinde eşleştirildi. Sonlu altörtü tanığı (finite_subcover_witness) ve Heine-Borel kontrolü (heine_borel_check) hesaplamalı doğrulama katmanını oluşturur. analyze_compactness tüm raporu tek çağrıda verir. Tokenlar: compactness corridor table, finite-subcover witness.
