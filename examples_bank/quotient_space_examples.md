# Quotient-space examples bank — v1.0.293

Bu dosya quotient-space hattını örnek bankasına açar. Amaç, Chapter 07--15 aralığındaki dış zipleri aktif pakete kopyalamadan ve herhangi bir dış metni doğrudan devralmadan; eşdeğerlik sınıfları, bölüm kümesi, quotient map, saturation ve quotient topology kavramlarını küçük, izlenebilir ve test edilebilir sözleşmelere dönüştürmektir.

## Kapsam ilkesi

Bu sürüm genel bir quotient-space API modülü, keyfî topolojik uzay için tam otomatik bölüm uzayı inşa motoru, genel kategori-kuramsal final topology hesaplayıcısı veya manifold/identification space sınıflandırıcısı eklemez. v1.0.293 yalnız şu güvenli yüzeyleri örnek bankasına bağlar:

- eşdeğerlik bağıntısından bölüm kümesine geçiş;
- quotient map'in noktaları sınıflara gönderen doğal izdüşüm olarak okunması;
- saturation koşulunun quotient dilinde neden zorunlu olduğunun gösterilmesi;
- quotient topology tanımının `U` açık iff `q^{-1}(U)` açık ilkesiyle test edilmesi;
- uçları yapıştırılmış aralık gibi identification örneklerinin küçük tanık modellerle anlatılması;
- indiscrete collapse ve endpoint identification gibi uç örneklerin ayrılması;
- metrik sezginin quotient altında otomatik taşınmadığına dair warning-line;
- ilerideki `pytop` çekirdek quotient yardımcıları için davranış sözleşmesi hazırlanması.

Aşağıdaki `QS-0*` aileleri theorem-prover değildir. Bunlar ders anlatımı, worksheet üretimi, questionbank bağlantısı ve otomatik doküman testleri için kullanılan örnek-bankası çekirdekleridir. Dış Chapter 07--15 zipleri yalnız yön belirleyici referanstır; bu dosya onları doğrudan pakete kopyalamaz.

## Test edilebilir örnek aileleri

### QS-01 — Eşdeğerlik sınıfları bölüm kümesinin noktalarıdır

- **Model:** `X={a,b,c,d}` kümesi üzerinde iki sınıflı bir bölümleme: `A={a,b}` ve `B={c,d}`.
- **Beklenen davranış:** quotient set artık `A` ve `B` adlı iki noktadan oluşur; `a` ve `b` aynı quotient noktasına gider.
- **pytop sözleşmesi:** testler, bölüm kümesinin sınıf sayısını ve sınıf üyeliklerinin ayrık/örtücü olduğunu doğrular.
- **Pedagojik vurgu:** Bölüm uzayında eski noktaların bazıları tek bir yeni nokta gibi okunur.

### QS-02 — Quotient map sınıf etiketini okur

- **Model:** `q:X -> X/~` haritası, her elemanı ait olduğu sınıf etiketine gönderir.
- **Beklenen davranış:** `q(a)=q(b)=A`, `q(c)=q(d)=B`.
- **pytop sözleşmesi:** testler quotient map'in sürjektif olduğunu ve her quotient noktasının boş olmayan bir preimage sınıfı bulunduğunu doğrular.
- **Pedagojik vurgu:** Quotient map yalnız bir fonksiyon değil, topolojiyi quotient tarafa taşıyan ana kapıdır.

### QS-03 — Saturated altküme sınıfların birleşimi olmalıdır

- **Model:** `A={a,b}` sınıfı varken `{a}` tek başına seçilir.
- **Beklenen davranış:** `{a}` saturated değildir; çünkü sınıfın yalnız bir parçasını alır. `{a,b}` ve `X` saturated altkümelerdir.
- **pytop sözleşmesi:** testler bir altkümenin her sınıfı ya tümüyle içerip ya hiç içermediğini kontrol eder.
- **Pedagojik vurgu:** Quotient tarafta görülebilen altkümeler, kaynakta sınıfları parçalamayan altkümelerdir.

### QS-04 — Quotient topology preimage ile tanınır

- **Model:** `X={a,b,c,d}` üzerinde `∅, {a,b}, {c,d}, X` açıkları ve `A={a,b}`, `B={c,d}` bölümlemesi.
- **Beklenen davranış:** quotient topology, `∅, {A}, {B}, {A,B}` altkümelerini içerir; çünkü preimage'leri kaynakta açıktır.
- **pytop sözleşmesi:** testler quotient topolojisini yalnız preimage açık olan quotient altkümelerinden üretir.
- **Pedagojik vurgu:** Quotient topolojisi quotient tarafta keyfî seçilmez; kaynak uzaydaki açıklık verisiyle zorlanır.

### QS-05 — Endpoint identification küçük tanık modeli

- **Model:** `[0,1]` aralığının uçlarını yapıştırma fikri, sonlu tanık noktalar `0, 1/4, 1/2, 3/4, 1` üzerinde izlenir.
- **Beklenen davranış:** `0` ve `1` aynı quotient noktasına gider; ara tanıklar ayrı sınıflarda kalır.
- **pytop sözleşmesi:** testler `q(0)=q(1)` ve `q(1/4) != q(1/2)` ayrımını kontrol eder.
- **Pedagojik vurgu:** Çember sezgisinin temelinde, aralığın iki ucunun tek bir nokta olarak okunması vardır.

### QS-06 — Collapse örneği quotient davranışının uç halidir

- **Model:** sabit harita tüm `X` elemanlarını tek `*` sınıfına gönderir.
- **Beklenen davranış:** quotient set tek noktalıdır ve quotient topology yalnız `∅` ile `{*}` içerir.
- **pytop sözleşmesi:** testler tek sınıflı bölümlemenin indiscrete/trivial quotient yüzeyini verdiğini doğrular.
- **Pedagojik vurgu:** Her şeyi tek noktaya çökertmek, quotient fikrinin en sert ama en öğretici örneğidir.

### QS-07 — Non-saturated açıklık uyarısı

- **Model:** kaynakta `{a}` açık olsa bile `a~b` tanımlıysa `{a}` quotient tarafta doğrudan bir açık küme adayı değildir.
- **Beklenen davranış:** quotient açıkları sınıf etiketleriyle ifade edilir; sınıfın yarısını seçen veri quotient altkümesi değildir.
- **pytop sözleşmesi:** testler non-saturated kaynak altkümesinin quotient altkümesi gibi yorumlanmamasını sağlar.
- **Pedagojik vurgu:** Quotient uzaylarda en sık hata, kaynak uzayın her açık kümesini quotient tarafta açık sanmaktır.

### QS-08 — Metrik sezgi quotient altında otomatik taşınmaz

- **Model:** uçları yapıştırılmış aralık için tanık pseudo-distance `d_q(q(x),q(y))=min(|x-y|,1-|x-y|)`.
- **Beklenen davranış:** `0` ve `1` aynı quotient noktası olduğundan mesafe `0` okunur; bu yapı özel bir iyi davranışlı örnektir.
- **pytop sözleşmesi:** testler endpoint pseudo-distance davranışını kontrol eder, fakat bunu genel quotient-metrik inşa motoru saymaz.
- **Pedagojik vurgu:** Bazı quotient örnekleri metrikle anlatılabilir; fakat her quotient topology otomatik olarak metrikten gelmez.

## Paket politikası notu

Bu dosya aktif kaynak olarak açık klasörde durur. Chapter 07--15 zipleri aktif nested zip'e dönüştürülmez. `docs/archive/` altındaki tarihsel bundle dışındaki zipler aktif kaynak kabul edilmez.
