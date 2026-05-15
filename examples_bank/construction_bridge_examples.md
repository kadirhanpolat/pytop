
# Construction-bridge examples bank — v1.0.294

Bu dosya subspace, product, topological sum ve quotient inşa biçimlerini aynı örnek-bankası koridorunda karşılaştırır. Amaç, Chapter 07--15 aralığındaki dış zipleri aktif pakete kopyalamadan ve herhangi bir dış metni doğrudan devralmadan; öğrencinin “aynı taşıyıcı üzerinde topoloji değiştirmek”, “koordinatlı ürün kurmak”, “bileşenleri etiketli ayırmak” ve “noktaları sınıflarla yapıştırmak” işlemlerini birbirine karıştırmamasını sağlayan küçük, izlenebilir ve test edilebilir bir sözleşme kurmaktır.

## Kapsam ilkesi

Bu sürüm genel bir construction API modülü, keyfî topolojik uzaylar için tam otomatik categorical construction motoru, pushout/pullback hesaplayıcısı veya genel final/initial topology çözücüsü eklemez. v1.0.294 yalnız şu güvenli yüzeyleri örnek bankasına bağlar:

- altuzay topolojisinin açık kümeleri kesişimle devraldığını gösterme;
- inclusion map'in sürekliliğini subspace tanımı üzerinden okuma;
- product topology için açık dikdörtgenlerin taşıyıcı çarpımdan ayrı olduğunu vurgulama;
- projection map'lerin ürün topolojisindeki temel rolünü test edilebilir hale getirme;
- topological sum/disjoint union için etiketli kopya fikrini görünür kılma;
- sum topology membership koşulunu bileşen dilimleriyle okuma;
- quotient construction için saturated/preimage dilini önceki quotient yüzeyine bağlama;
- aynı kaynak ailesinden subspace, product, sum ve quotient yollarının farklı veri kaybı/koruma davranışı verdiğini ayırma.

Aşağıdaki `CB-0*` aileleri theorem-prover değildir. Bunlar ders anlatımı, worksheet üretimi, questionbank bağlantısı ve otomatik doküman testleri için kullanılan örnek-bankası çekirdekleridir. Dış Chapter 07--15 zipleri yalnız yön belirleyici referanstır; bu dosya onları doğrudan pakete kopyalamaz.

## Test edilebilir örnek aileleri

### CB-01 — Altuzay topolojisi açık kümeleri kesişimle üretir

- **Model:** `X={a,b,c}` üzerinde `T={∅,{a,b},X}` ve `A={a,c}` altkümesi.
- **Beklenen davranış:** `A` üzerindeki altuzay açıkları `∅`, `{a}` ve `A` olur.
- **pytop sözleşmesi:** testler her altuzay açığının `U∩A` biçiminde geldiğini ve fazladan açık üretilmediğini doğrular.
- **Pedagojik vurgu:** Altuzay inşası taşıyıcıyı küçültür; açık kümeler dış uzaydan kesilerek gelir.

### CB-02 — Inclusion map subspace tanımıyla süreklidir

- **Model:** `i:A -> X` inclusion map ve `X` içindeki açık küme `{a,b}`.
- **Beklenen davranış:** `i^{-1}({a,b})={a}` altuzayda açıktır.
- **pytop sözleşmesi:** testler inclusion map için açıkların ters görüntülerinin subspace topology içinde kaldığını doğrular.
- **Pedagojik vurgu:** Inclusion map'in sürekliliği ek bir teorem gibi değil, altuzay topolojisinin tasarım amacı gibi okunmalıdır.

### CB-03 — Product topology taşıyıcı çarpımdan daha fazla veri ister

- **Model:** iki sonlu ayrık faktör: `X={0,1}`, `Y={u,v}`.
- **Beklenen davranış:** taşıyıcı dört sıralı çift içerir; product topology açık dikdörtgenlerden üretilir ve bu özel ayrık durumda tüm altkümeleri verir.
- **pytop sözleşmesi:** testler product carrier ile product open family'nin ayrı nesneler olduğunu ve ayrık faktörlerde power set'e ulaşıldığını doğrular.
- **Pedagojik vurgu:** Kartezyen çarpım yalnız nokta kümesini verir; topoloji ayrıca inşa edilmelidir.

### CB-04 — Projection map ürün topolojisinin temel tanığıdır

- **Model:** `π_1:X×Y -> X` ve `X` içinde `{0}` açık kümesi.
- **Beklenen davranış:** `π_1^{-1}({0})={0}×Y` ürün topolojisinde açıktır.
- **pytop sözleşmesi:** testler projection preimage ailesini açık dikdörtgen mantığıyla kontrol eder.
- **Pedagojik vurgu:** Product topology, projection map'leri sürekli kılan en doğal başlangıç topolojisi olarak okunur.

### CB-05 — Topological sum bileşenleri etiketli kopyalarla ayırır

- **Model:** `X={0,1}` ve `Y={1,2}` kümeleri.
- **Beklenen davranış:** sum taşıyıcısında `('X',1)` ile `('Y',1)` farklı noktalardır.
- **pytop sözleşmesi:** testler etiketli taşıyıcıda çakışan ham elemanların ayrıldığını doğrular.
- **Pedagojik vurgu:** Sum inşası bileşenleri yan yana koyar; ortak görünen semboller bile etikete göre ayrılır.

### CB-06 — Sum topology bileşen dilimleriyle test edilir

- **Model:** `X` üzerinde `∅,{0},X`; `Y` üzerinde `∅,{2},Y` topolojileri.
- **Beklenen davranış:** sum içindeki bir altküme açıktır ancak her bileşene düşen dilimi ilgili bileşende açıksa.
- **pytop sözleşmesi:** testler sum subset membership kontrolünü etiketli dilimlere indirger.
- **Pedagojik vurgu:** Sum topology, bileşenleri birbirine yapıştırmaz; her bileşenin kendi topolojisini ayrı ayrı okur.

### CB-07 — Quotient construction sınıfları parçalamayan veri ister

- **Model:** `X={a,b,c,d}` üzerinde `A={a,b}`, `B={c,d}` sınıfları.
- **Beklenen davranış:** `{a}` saturated değildir; `{a,b}` saturated'dır ve quotient tarafında tek nokta gibi görünür.
- **pytop sözleşmesi:** testler saturated subset ve quotient preimage işlemlerini önceki quotient-space sözleşmesiyle uyumlu biçimde doğrular.
- **Pedagojik vurgu:** Quotient inşası altuzay gibi yalnız seçmez; bazı eski noktaları tek yeni noktada birleştirir.

### CB-08 — Dört inşa aynı işlem değildir

- **Model:** aynı küçük veri ailesi üzerinde dört okuma: subspace, product, sum, quotient.
- **Beklenen davranış:** subspace keser, product koordinatlandırır, sum etiketler, quotient yapıştırır.
- **pytop sözleşmesi:** testler her inşa için ayrı bir davranış etiketi ve ayrı bir korunan veri listesi bulunduğunu doğrular.
- **Pedagojik vurgu:** Bu dört işlem aynı “yeni uzay üretme” başlığı altında geçse de öğrencinin kaybettiği/koruduğu veri farklıdır.

### CB-09 — Sum üzerinde quotient, etiketli yapıştırma modeli verebilir

- **Model:** iki aralık-kopyasını temsil eden etiketli uç noktalar ve uçları aynı sınıfa alan oyuncak bölümleme.
- **Beklenen davranış:** önce sum ile kopyalar ayrılır; sonra quotient ile seçilmiş uç noktalar yapıştırılır.
- **pytop sözleşmesi:** testler işlem sırasının kayıt altına alındığını ve quotient sınıfının etiketli noktaları bilinçli olarak birleştirdiğini doğrular.
- **Pedagojik vurgu:** Yapıştırma örneklerinde çoğu zaman önce ayrık kopyalar kurulur, sonra quotient ile seçili noktalar özdeşleştirilir.

## İleri fazlara bırakılanlar

- genel `src/pytop/constructions.py` API katmanı;
- keyfî altuzay/product/sum/quotient inşa motorlarının tek arayüzde birleşmesi;
- final topology ve initial topology hesaplayıcıları;
- pushout/pullback gibi kategori-kuramsal inşalar;
- manuscript içinde inşa şemalarının otomatik şekil üretimi;
- questionbank için parametreli construction problem generator.

## Chapter 07--15 kullanım notu

Bu dosya Chapter 07--15 ziplerini doğrudan pakete kopyalamaz; aktif pakete de nested zip olarak eklemez. Bu zipler yalnız dış referans girdisi olarak kullanılmıştır. İnşa aileleri özgünleştirilmiş, küçük tutulmuş ve mevcut ekosistemin test edilebilir sınırlarına göre yeniden formüle edilmiştir.
