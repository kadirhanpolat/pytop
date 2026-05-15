# Compactness variants examples bank — v1.0.297

Bu dosya Chapter 07--15 dış referans koridorundaki kompaktlık varyantlarını aktif pakete doğrudan kopyalamaz. Amaç, mevcut `compactness_examples.md` dosyasını bozmeden; countably compact, sequentially compact ve Lindelöf ayrımlarını küçük, özgün ve test edilebilir örnek-bankası sözleşmeleri olarak görünür kılmaktır.

## Kapsam ilkesi

Bu sürüm genel bir sonsuz uzay karar vericisi eklemez. Bunun yerine örnek üretimi, test yazımı ve manuskript yönlendirmesi için güvenli ayrım şemaları tanımlar:

- compact, countably compact, sequentially compact, limit point compact ve Lindelöf etiketlerinin birbirine otomatik indirgenmemesi;
- metrik uzaylarda bazı klasik eşdeğerlik sezgilerinin genel topolojiye taşınmaması;
- sayılabilir açık örtü, dizi, alt dizi ve limit noktası tanıklarının ayrı veri tipleri gibi okunması;
- `pytop` tarafında bilinmeyen genel uzaylar için aşırı iddia üretilmemesi.

## Test edilebilir örnek aileleri

### CVA-01 — Sonlu uzay bütün kompaktlık varyantlarını sağlar

- **Model:** sonlu taşıyıcı üzerinde herhangi bir topoloji.
- **Beklenen davranış:** compact, countably compact, sequentially compact, limit point compact ve Lindelöf etiketleri olumlu okunur.
- **pytop sözleşmesi:** testler sonlu bir toy profilde bütün varyantların `True` olduğunu doğrular.
- **Pedagojik vurgu:** Sonluluk birçok örtü/dizi özelliğini aynı anda taşır; fakat bu ortak sonuç sonsuz uzaylar için genelleme lisansı değildir.

### CVA-02 — Sonsuz ayrık uzay varyant ayrımı için negatif temel örnektir

- **Model:** `N` üzerinde ayrık topoloji.
- **Beklenen davranış:** compact değildir; countably compact ve sequentially compact da değildir; Lindelöf sayılabilir ayrık durumda korunabilir.
- **pytop sözleşmesi:** testler tekil açık örtünün sonlu altörtü vermediğini ve kaçan dizinin yakınsak alt dizi taşımadığını kodlar.
- **Pedagojik vurgu:** Aynı uzay bazı örtü özelliklerini kaybederken sayılabilirlik kaynaklı başka bir örtü özelliğini koruyabilir.

### CVA-03 — Sayılamaz ayrık uzay Lindelöf uyarısını da bozar

- **Model:** sayılamaz ayrık taşıyıcı.
- **Beklenen davranış:** singleton örtü sayılabilir altörtüye indirgenemez.
- **pytop sözleşmesi:** testler `cardinality="uncountable"` etiketinin Lindelöf iddiasını engellediğini doğrular.
- **Pedagojik vurgu:** “Ayrık uzay Lindelöf olabilir” ifadesi taşıyıcının büyüklüğüne bağlıdır.

### CVA-04 — Kofinite topoloji kompaktlık tarafında güçlü, dizisel tarafta dikkat ister

- **Model:** sonsuz bir küme üzerinde kofinite topoloji.
- **Beklenen davranış:** compact ve countably compact olumlu; fakat sequentially compact sonucu ek ayırma/metrik varsayımlar olmadan otomatik API iddiası yapılmaz.
- **pytop sözleşmesi:** testler kofinite profilin örtü tarafını olumlu, dizisel tarafı ise kontrollü/etiketli tuttuğunu arar.
- **Pedagojik vurgu:** Örtü dili ile dizi dili genel topolojide aynı karar yüzeyi değildir.

### CVA-05 — Lindelöf olmak kompaktlık değildir

- **Model:** gerçek doğru benzeri ikinci sayılabilir fakat kompakt olmayan metrik uzay.
- **Beklenen davranış:** Lindelöf olumlu; compact olumsuz olabilir.
- **pytop sözleşmesi:** testler `second_countable=True` ve `not_compact=True` etiketlerinin aynı profilde çelişki üretmediğini doğrular.
- **Pedagojik vurgu:** Her açık örtüden sayılabilir altörtü seçmek, sonlu altörtü seçmekten daha zayıf bir taleptir.

### CVA-06 — Sequential compactness dizisel tanık ister

- **Model:** birim aralıkta her dizinin yakınsak alt diziye sahip olduğu metrik kompaktlık sezgisi.
- **Beklenen davranış:** dizisel kompaktlık iddiası açıkça “her dizi için alt dizi” sözleşmesiyle işaretlenir.
- **pytop sözleşmesi:** testler sınırlı bir gözlem listesinde Bolzano-Weierstrass benzeri alt dizi seçme simülasyonunu kullanır; bunu genel ispat motoru diye sunmaz.
- **Pedagojik vurgu:** Bu blok yalnız ders ve test sözleşmesidir; tam sonsuz dizi karar vericisi değildir.

### CVA-07 — Countably compactness sayılabilir açık örtüleri hedefler

- **Model:** sayılabilir açık örtü listesi verilen sembolik uzay.
- **Beklenen davranış:** her sayılabilir açık örtü için sonlu altörtü koşulu countably compactness sözleşmesinin merkezidir.
- **pytop sözleşmesi:** testler küçük bir finite-subcover arayıcısıyla countable-cover etiketini ayrı okur.
- **Pedagojik vurgu:** Countably compact, yalnızca sayılabilir örtülerle ilgili bir koşuldur; tüm açık örtüleri kapsayan compactness ile karıştırılmamalıdır.

### CVA-08 — Limit point compactness ayrı bir tanık dilidir

- **Model:** sonsuz altkümelerin yığılma noktası taşıyıp taşımadığına bakan sembolik profil.
- **Beklenen davranış:** limit point compactness dizi altseçimi veya açık örtü altseçimi olarak otomatik yeniden adlandırılmaz.
- **pytop sözleşmesi:** testler “sonsuz altküme -> limit point witness” şemasını metinsel ve veri-temelli olarak ayrı tutar.
- **Pedagojik vurgu:** Birçok derste bu özellikler metrik veya ikinci sayılabilir bağlamda birleşir; genel topoloji dosyası ayrımı korumalıdır.

### CVA-09 — Metrik kompaktlık köprüsü genelleme uyarısı içerir

- **Model:** metrik profil üzerinde compact, sequentially compact ve limit point compact etiketleri birlikte verilir.
- **Beklenen davranış:** metrik bağlamda bu özellikler arasında güçlü bağlantılar kurulabilir; fakat dosya bunu genel topolojik teorem gibi kaydetmez.
- **pytop sözleşmesi:** testler `metric_context=True` etiketi olmadan eşdeğerlik zinciri kurulmadığını doğrular.
- **Pedagojik vurgu:** Metrik varsayım pedagojik olarak açıkça görünür kalmalıdır.

### CVA-10 — Bilinmeyen genel uzayda varyantlar unknown kalmalıdır

- **Model:** yalnız `symbolic_general_space` etiketi taşıyan genel uzay.
- **Beklenen davranış:** compactness variants için olumlu/olumsuz otomatik karar verilmez.
- **pytop sözleşmesi:** testler belirsiz genel profilin `unknown` olarak kaldığını doğrular.
- **Pedagojik vurgu:** Eksik hipotezle teorem üretmemek, paket güvenilirliğinin parçasıdır.

## Kullanım notu

Bu dosya problem metni deposu değildir. Her `CVA-*` bloğu; soru ailesi, manuskript örneği, notebook hücresi veya pytest sözleşmesi üretirken kullanılabilecek küçük bir model kartıdır. Öncelik, özgünlük ve ayrımların netliğidir.

---

## v0.1.61 — compactness_variants.py API örnekleri

### CV-01 — Sonlu uzayda tüm varyantlar doğru (exact)

- **Model:** $X$ sonlu ayrık, $|X|=n$.
- **API:** `analyze_compactness_variants(X)` → `status="true"`, `mode="exact"`.

### CV-02 — Kompakt etiketli uzay: sayılabilir kompakt

- **Model:** `tags=["compact"]`.
- **API:** `is_countably_compact(X).status` → `"true"`.

### CV-03 — Metrikleşebilir + kompakt: sıralı kompakt

- **Model:** `tags=["metrizable","compact"]`.
- **API:** `is_sequentially_compact(X).status` → `"true"` (Bolzano-Weierstrass).

### CV-04 — Yalnızca kompakt etiketi: sıralı kompakt bilinmiyor

- **Model:** `tags=["compact"]` (metrizable yok).
- **API:** `is_sequentially_compact(X).status` → `"unknown"`.

### CV-05 — Metrikleşebilir Lindelöf: psödokompakt değil

- **Model:** `tags=["metrizable","lindelof"]`.
- **API:** `is_pseudocompact(X).status` → `"false"`.

### CV-06 — İkinci sayılabilir: Lindelöf

- **Model:** `tags=["second_countable"]`.
- **API:** `is_lindelof(X).status` → `"true"`.

### CV-07 — Sayılamaz ayrık: Lindelöf değil

- **Model:** `tags=["uncountable","discrete"]`.
- **API:** `is_lindelof(X).status` → `"false"`.

### CV-08 — Profil: dört varyant bir arada

- **Model:** Herhangi bir uzay.
- **API:** `compactness_variant_profile(X).keys()` → `{"representation","countably_compact","sequentially_compact","pseudocompact","lindelof"}`.
