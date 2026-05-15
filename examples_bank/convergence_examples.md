# Convergence examples bank — v1.0.295

Bu dosya yakınsaklık hattını örnek bankasına açar. Amaç, Chapter 07--15 aralığındaki dış zipleri aktif pakete kopyalamadan ve herhangi bir dış metni doğrudan devralmadan; diziler, alt diziler, ağlar, süzgeçler, metrik yakınsaklık ve topolojik yakınsaklık arasındaki ayrımları küçük, izlenebilir ve test edilebilir sözleşmelere dönüştürmektir.

## Kapsam ilkesi

Bu sürüm genel bir convergence API modülü, keyfî topolojik uzay için tam otomatik net/filter yakınsaklık motoru, tam kapsamlı sıralı süreklilik karar vericisi veya genel kompaktlık ispatlayıcısı eklemez. v1.0.295 yalnız şu güvenli yüzeyleri örnek bankasına bağlar:

- dizisel yakınsaklığın açık komşuluklarla “sonunda içinde kalma” biçiminde okunması;
- metrik uzaylarda yakınsaklığın uzaklığın sıfıra gitmesiyle test edilmesi;
- sürekliliğin dizileri limite taşıması ilkesinin küçük sayısal tanıklarla izlenmesi;
- dizisel süreklilik ile süreklilik arasındaki ayrım için warning-line hazırlanması;
- koordinat yakınsaklığı ile norm yakınsaklığı arasındaki farkın görünür kılınması;
- ağların dizilerden daha esnek yönlendirilmiş indeks mantığıyla okunması;
- süzgeçlerin kuyruk ailesi ve komşuluk ailesi üzerinden yakınsaklık fikrini desteklemesi;
- Hausdorff olmayan ortamlarda limitin tekil olmayabileceğinin gösterilmesi;
- alt dizilerin ve Cauchy dizilerinin hangi koşullarda kullanılabileceğinin ayrılması;
- Cauchy olmanın metrik bir özellik olduğu, salt topolojik invariant olmadığı konusunda güvenli uyarı kurulması.

Aşağıdaki `CV-0*` ve `CV-10` aileleri theorem-prover değildir. Bunlar ders anlatımı, worksheet üretimi, questionbank bağlantısı ve otomatik doküman testleri için kullanılan örnek-bankası çekirdekleridir. Dış Chapter 07--15 zipleri yalnız yön belirleyici referanstır; bu dosya onları doğrudan pakete kopyalamaz.

## Test edilebilir örnek aileleri

### CV-01 — Topolojik dizi yakınsaklığı komşuluk kuyruğudur

- **Model:** bir uzayda `x_n -> p` ifadesi, `p`'nin her açık komşuluğu için dizinin yeterince ileri terimlerinin bu komşulukta kalması olarak okunur.
- **Beklenen davranış:** seçilen her komşuluk için bir kuyruk eşiği bulunur.
- **pytop sözleşmesi:** testler sonlu gözlemli bir komşuluk ailesinde kuyruk üyeliğini doğrular.
- **Pedagojik vurgu:** Yakınsaklık yalnız sayısal mesafe değildir; genel topolojide temel veri komşuluklardır.

### CV-02 — Metrik yakınsaklık uzaklığın sıfıra gitmesidir

- **Model:** reel doğru üzerinde `x_n=1/n` dizisi ve limit `0`.
- **Beklenen davranış:** her pozitif hata eşiği için yeterince büyük `n` değerlerinde `|x_n-0|` küçük kalır.
- **pytop sözleşmesi:** testler belirli epsilon değerleri için açık bir kuyruk eşiği üretir.
- **Pedagojik vurgu:** Metrik uzayda komşuluk dili epsilon-dilini doğurur; fakat bu özel durum genel topolojiyle karıştırılmamalıdır.

### CV-03 — Sürekli harita dizisel limitleri taşır

- **Model:** `x_n=1/n` ve `f(x)=x^2`.
- **Beklenen davranış:** `x_n -> 0` ise `f(x_n) -> f(0)` olur.
- **pytop sözleşmesi:** testler kare alma işleminin kuyruk hata sınırını daha da küçülttüğünü doğrular.
- **Pedagojik vurgu:** Süreklilik, limit alma ile fonksiyon uygulama işlemlerinin uyumlu olduğunu gösterir.

### CV-04 — Dizisel süreklilik tek başına genel süreklilik değildir

- **Model:** çok kaba olmayan ama dizilerin sınırlı bilgi taşıdığı bir topolojik uyarı yüzeyi.
- **Beklenen davranış:** bazı uzaylarda bütün dizisel testleri geçmek, açık-küme preimage sürekliliğini garanti etmeyebilir.
- **pytop sözleşmesi:** bu sürüm tam karar verici açmaz; test yalnız “dizisel tanık yokluğu süreklilik kanıtı değildir” uyarı sözleşmesini arar.
- **Pedagojik vurgu:** Birinci sayılabilir uzaylarda dizi dili güçlüdür; genel topolojide ağ veya süzgeç diline ihtiyaç duyulur.

### CV-05 — Koordinat yakınsaklığı norm yakınsaklığı olmayabilir

- **Model:** sonsuz koordinatlı bir uzayda birim vektörler `e_n`.
- **Beklenen davranış:** her sabit koordinatta değer sonunda sıfır olur; buna rağmen tüm vektörün normu sıfıra yaklaşmaz.
- **pytop sözleşmesi:** testler sabit koordinat projeksiyonunun sonunda sıfır olduğunu, fakat norm uzaklığının `1` kaldığını doğrular.
- **Pedagojik vurgu:** Ürün/koordinat sezgisi ile metrik/norm sezgisi aynı şey değildir.

### CV-06 — Ağlar yönlendirilmiş indekslerle komşuluk yakalar

- **Model:** indeksler iki hata parametresiyle yönlendirilir; ilerlemek iki parametreyi de küçültmek anlamına gelir.
- **Beklenen davranış:** her komşuluk eşiği için daha ileri indekslerde ağ terimleri komşulukta kalır.
- **pytop sözleşmesi:** testler iki parametreli küçük bir directed toy model üzerinden eventual control yapar.
- **Pedagojik vurgu:** Ağlar, dizilerin sayılabilir kuyruk mantığını daha genel yönlendirilmiş kümelere taşır.

### CV-07 — Süzgeç yakınsaklığı komşuluk ailesini içerir

- **Model:** bir dizinin kuyruk süzgeci ve `0` noktasının epsilon-komşulukları.
- **Beklenen davranış:** her komşuluğun preimage kuyruğu süzgeçte görünür.
- **pytop sözleşmesi:** testler `1/n` dizisinin tail-filter sözleşmesini epsilon eşiğiyle doğrular.
- **Pedagojik vurgu:** Süzgeç dili, “sonunda” ifadesini kümeler ailesiyle kodlar.

### CV-08 — Hausdorff olmayan uzaylarda limit tekil olmayabilir

- **Model:** iki noktalı Sierpinski tipi toy topoloji.
- **Beklenen davranış:** sabit bir dizi birden fazla noktaya yakınsayabilir.
- **pytop sözleşmesi:** testler aynı sabit dizinin iki farklı limit adayını geçtiğini gösterir.
- **Pedagojik vurgu:** Limitin tekliği Hausdorff ayrım aksiyomlarıyla ilişkilidir.

### CV-09 — Alt dizi yakınsaklığı kuyruk bilgisini miras alır

- **Model:** `1/n` dizisinin çift indeksli alt dizisi `1/(2n)`.
- **Beklenen davranış:** ana dizi `0`'a yakınsıyorsa alt dizi de `0`'a yakınsar.
- **pytop sözleşmesi:** testler alt dizinin aynı epsilon eşiğini daha kolay sağladığını doğrular.
- **Pedagojik vurgu:** Alt dizi argümanları kompaktlık ve sequential compactness ayrımlarında sık kullanılır.

### CV-10 — Cauchy olmak metrik veriye bağlıdır

- **Model:** `(0,∞)` üzerinde `x_n=1/n` ve homeomorfik dönüşüm olarak `h(x)=1/x` fikri.
- **Beklenen davranış:** kaynak metrikte Cauchy davranışı görülebilirken görüntü dizisi `n` biçiminde uzaklaşır.
- **pytop sözleşmesi:** testler sonlu kuyruklarda Cauchy kontrolü ile görüntüde başarısızlığı ayırır.
- **Pedagojik vurgu:** Cauchy olmak salt topolojik invariant değildir; metrik seçimine bağlıdır.

## Entegrasyon notu

Bu yüzey, önceki `metric_space_examples.md`, `function_space_examples.md`, `quotient_space_examples.md` ve `construction_bridge_examples.md` dosyalarını tamamlar. v1.0.295, yakınsaklık kavramını şimdilik örnek-bankası ve test sözleşmesi düzeyinde tutar; genel net/filter motoru ileride `pytop` çekirdeği güçlendirildiğinde ayrı bir API olarak değerlendirilecektir.

## v0.1.46 note

Bu sürümde Chapter 16 için Cilt II diziler konumlandırma tablosu eklendi. Lisans yakınsama rotası: diziler → ağlar → filtreler. Ağlar ve filtreler Cilt III'e bırakıldı. Tokenlar: sequences-nets-filters positioning table, undergraduate convergence route, sequence_converges_to, is_sequentially_compact, sequence_cluster_point, sequential_closure, analyze_sequences.
