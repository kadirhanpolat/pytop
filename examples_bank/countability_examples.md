# Sayılabilirlik örnek bankası

Bu dosya, Chapter 09 merkezli sayılabilirlik aksiyomları hattı için açılmış test edilebilir örnek iskeletidir. Amaç, birinci sayılabilirlik, ikinci sayılabilirlik, ayrılabilirlik ve Lindelöf özelliğini aynı şeymiş gibi sunmamak; her kavramı güvenli benchmark aileleri üzerinden ayrı ayrı izlemektir.

## v1.0.274 countability examples-bank skeleton

### Kullanım sınırı

Bu iskelet bir teorem deposu değil, örnek-bankası yüzeyidir. Her örnek için şu dört alan ayrı tutulur:

- `first_countable`
- `second_countable`
- `separable`
- `lindelof`

Bir satırda olumlu sonuç yazılması, diğer satırların otomatik olumlu olduğu anlamına gelmez. Özellikle metrik uzaylarda bazı güçlü koridorlar vardır; fakat genel topolojik uzaylarda bu koridorlar dikkatli kullanılmalıdır.

### CE-01 — Sonlu topolojik uzay güvenli başlangıcı

- Taşıyıcı: sonlu bir küme `X`.
- Durum: `X` üzerinde verilen her topoloji sonlu olduğundan tüm açık kümeler ailesi de sonludur.
- Beklenen sayılabilirlik profili:
  - `first_countable`: evet
  - `second_countable`: evet
  - `separable`: evet
  - `lindelof`: evet
- `pytop` bağlantısı: `FiniteTopologicalSpace(...)`, `countability_report(...)`.
- Pedagojik rol: tanımların ilk kez küçük ve elle kontrol edilebilir bir modelde görülmesi.

### CE-02 — Metrik uzaylarda yerel taban benchmark'ı

- Uzay tipi: herhangi bir metrik uzay `(X,d)`.
- Yerel taban fikri: her `x in X` için `B(x,1/n)` topları merkezde sayılabilir bir yerel taban adayı verir.
- Beklenen profil:
  - `first_countable`: evet
  - diğer özellikler: ek veri olmadan otomatik yazılmamalıdır
- `pytop` bağlantısı: `MetricLikeSpace(...)`, `is_first_countable(...)`.
- Warning line: "metrik" demek tek başına "ikinci sayılabilir" demek değildir.

### CE-03 — Ayrılabilir metrik uzaydan ikinci sayılabilirliğe güvenli koridor

- Uzay tipi: `metric + separable`.
- Veri: sayılabilir yoğun küme ve sayılabilir yarıçap ailesi.
- Beklenen profil:
  - `second_countable`: evet
  - `first_countable`: evet
  - `separable`: evet
- `pytop` bağlantısı: `MetricLikeSpace(tags={"separable"})`, `is_second_countable(...)`.
- Pedagojik rol: ikinci sayılabilirliğin metrik bağlamda nasıl sayılabilir merkezler ve yarıçaplarla üretildiğini göstermek.

### CE-04 — Reel doğru için rasyonel uçlu aralık benchmark'ı

- Uzay: standart topolojili `R`.
- Taban sezgisi: rasyonel uçlu açık aralıklar.
- Beklenen profil:
  - `first_countable`: evet
  - `second_countable`: evet
  - `separable`: evet
  - `lindelof`: evet
- Kitap bağlantısı: Chapter 04, Chapter 09, Chapter 12.
- Dürüst sınır: Bu satır örnek-bankası benchmark'ıdır; çekirdekte reel doğrunun tüm klasik ispatları otomatik üretilmez.

### CE-05 — Sayılabilir ayrık uzay

- Taşıyıcı: `N` gibi sayılabilir sonsuz bir küme.
- Topoloji: ayrık topoloji.
- Beklenen profil:
  - `first_countable`: evet
  - `second_countable`: evet
  - `separable`: evet
  - `lindelof`: evet
- `pytop` bağlantısı: `DiscreteInfiniteSpace(carrier="N", tags={"countable"})`.
- Pedagojik rol: ayrık topolojinin sayılabilir taşıyıcı üzerinde sayılabilirlik aksiyomlarıyla uyumlu olduğunu göstermek.

### CE-06 — Sayılamaz ayrık uzay warning-line'ı

- Taşıyıcı: `R` gibi sayılamaz bir küme.
- Topoloji: ayrık topoloji.
- Beklenen profil:
  - `first_countable`: evet
  - `second_countable`: hayır
  - `separable`: hayır
  - `lindelof`: hayır
- `pytop` bağlantısı: `DiscreteInfiniteSpace(carrier="R")`, `is_second_countable(...)`, `is_separable(...)`.
- Pedagojik rol: "her nokta tek başına açık" olduğunda yerel kontrol kolaydır; fakat küresel sayılabilir taban veya sayılabilir yoğun küme yoktur.

### CE-07 — Sorgenfrey-benzeri ayrım benchmark'ı

- Uzay tipi: alt limit topolojisini temsil eden `SorgenfreyLikeSpace`.
- Beklenen profil:
  - `separable`: evet
  - `second_countable`: hayır
- `pytop` bağlantısı: `SorgenfreyLikeSpace(...)`, `is_separable(...)`, `is_second_countable(...)`.
- Pedagojik rol: ayrılabilirliğin ikinci sayılabilirliği genel topolojik uzaylarda zorunlu kılmadığını göstermek.

### CE-08 — Kofinite ve kosayılabilir topolojiler için dikkatli sınır

- Kofinite topoloji: sonlu tamamlayıcılı açık kümeler üzerinden okunur.
- Kosayılabilir topoloji: sayılabilir tamamlayıcılı açık kümeler üzerinden okunur.
- Beklenen kullanım: bu aileler genel teoremlerin terslerinin otomatik olmadığını göstermek için warning-line örnekleri olarak kullanılmalıdır.
- `pytop` bağlantısı: `CofiniteSpace(...)`, `CocountableSpace(...)`, `analyze_infinite_countability(...)`.
- Dürüst sınır: taşıyıcının sayılabilir/sayılamaz oluşu açık belirtilmeden nihai profil yazılmamalıdır.

## Test edilebilir sözleşme

Bu dosyanın v1.0.274 sözleşmesi şudur:

1. `CE-01` ile `CE-08` kodları korunur.
2. Metrik uzaylar için birinci sayılabilirlik ayrı; ayrılabilir metrik uzaylar için ikinci sayılabilirlik ayrı satırda tutulur.
3. Sayılabilir ayrık uzay ile sayılamaz ayrık uzay aynı örnekmiş gibi sunulmaz.
4. Sorgenfrey-benzeri örnek, ayrılabilirlik ile ikinci sayılabilirlik arasındaki ayrımı görünür tutar.
5. Sonsuz klasik örneklerde otomatik API kararının olmadığı yerler açıkça "örnek-bankası benchmark" veya "dürüst sınır" olarak etiketlenir.

## Öğretim kararı — v1.0.274

Chapter 09 sayılabilirlik hattı, tek bir "sayılabilir" etiketiyle yürütülmemelidir. Bu dosya, yerel taban, küresel taban, yoğun altküme ve açık örtü indirgeme fikirlerini ayrı ayrı takip eden bir örnek-bankası iskeleti olarak kullanılmalıdır.

## v0.1.43 note

Bu sürümde Chapter 12 için Cilt II sayılabilirlik-aksiyomları koridoru tablosu eklendi. Dört özellik (is_first_countable, is_second_countable, is_separable, is_lindelof) standart uzay ailesi üzerinde eşleştirildi. Metric bridge notu: metrikleşebilir uzaylarda ikinci sayılabilirlik, ayrılabilirlik ve Lindelöf birbirine denkedir; bu denklik genel uzaylarda bozulur. Tokenlar: countability corridor table, metric bridge, weight, density, analyze_countability.
