# Local properties examples bank — v1.0.296

Bu dosya, Chapter 07--15 dış referans koridorundan gelen yerel özellik dilini aktif pakete doğrudan kopyalamadan örnek bankasına bağlar. Amaç, **local compactness**, **local connectedness**, **first countability** ve **second countability** kavramlarını birbirine karıştırmadan küçük, izlenebilir ve test edilebilir sözleşmeler halinde tutmaktır.

## Kapsam ilkesi

Bu sürüm genel bir yerel özellik karar vericisi, keyfî sonsuz topolojik uzay ispat motoru veya dış Chapter 07--15 metinlerinin aktarımı değildir. v1.0.296 yalnız şu güvenli yüzeyleri kurar:

- yerel özelliklerin nokta-komşuluk düzeyinde okunması;
- sonlu uzayların güvenli benchmark olarak kullanılması;
- standart reel doğru üzerinde local compactness, local connectedness ve sayılabilirlik aksiyomlarının birlikte görülmesi;
- ayrık uzaylarda yerel iyi davranış ile global ikinci sayılabilirliğin ayrılması;
- birinci sayılabilirlik ile ikinci sayılabilirliğin farklı niceleyici düzeylerinde çalıştığının gösterilmesi;
- yerel bağlantılılık ile bağlantılılık arasındaki farkın ayrık toplam örneğiyle görünür yapılması;
- topolojik toplamlarda local davranışın bileşenlerde korunurken global küçük taban davranışını garanti etmeyebileceğinin vurgulanması;
- rasyonel altuzay gibi tanıdık metrik örneklerde local compactness için ek dikkat gerektiğinin belirtilmesi.

Aşağıdaki `LP-*` örnekleri theorem-prover değildir. Bunlar ders anlatımı, worksheet üretimi, questionbank bağlantısı ve otomatik doküman testleri için kullanılan örnek-bankası sözleşmeleridir. Dış Chapter 07--15 zipleri yalnız yön belirleyici referanstır; bu dosya onları doğrudan pakete kopyalamaz.

## Test edilebilir örnek aileleri

### LP-01 — Yerel özellik nokta düzeyinde okunur

- **Model:** bir özellik `P`, her `x in X` için `x` çevresinde `P` taşıyan uygun bir komşuluk bulunmasıyla yerel biçimde okunur.
- **Beklenen davranış:** testler local kelimesinin tek bir global sonuç iddiası olmadığını, nokta ve komşuluk niceleyicileriyle çalıştığını doğrular.
- **pytop sözleşmesi:** örnek bankası `local_property_schema(point, neighborhood, property)` gibi ileride açılabilecek yüzeyler için veri ayrımını korur.
- **Pedagojik vurgu:** “X yerel olarak P'dir” ile “X P'dir” aynı cümle değildir.

### LP-02 — Sonlu topolojik uzaylar yerel kompaktlık için güvenli benchmark'tır

- **Model:** sonlu taşıyıcılı herhangi bir topolojik uzay.
- **Beklenen davranış:** her nokta tüm uzayın içinde yer alır ve sonlu uzay kompakt benchmark olarak kullanılabilir.
- **pytop sözleşmesi:** `FiniteTopologicalSpace` yüzeyinde local compactness örnekleri güvenli biçimde olumlu etiketlenebilir.
- **Pedagojik vurgu:** Sonlu model, tanımı ilk kez elle kontrol etmek için uygundur; fakat sonsuz örneklerin zorluğunu saklamaz.

### LP-03 — Standart reel doğru yerel kompakt fakat kompakt değildir

- **Model:** `R` standart topolojisi.
- **Beklenen davranış:** her noktanın küçük kapalı aralık kapanışı kompakt bir yerel tanık verir; buna rağmen `R` global olarak kompakt değildir.
- **pytop sözleşmesi:** sembolik reel doğru örneği `locally_compact=true`, `compact=false` etiket ayrımını taşımalıdır.
- **Pedagojik vurgu:** Yerel kompaktlık, uzayın tamamının kompakt olduğu anlamına gelmez.

### LP-04 — Standart reel doğru yerel bağlantılı ve bağlantılıdır

- **Model:** `R` standart topolojisi ve açık aralık komşulukları.
- **Beklenen davranış:** her noktanın bağlantılı açık aralık komşulukları vardır; ayrıca `R` bağlantılı benchmark'tır.
- **pytop sözleşmesi:** `connectedness_examples.md` ile çelişmeden, local connectedness etiketi ayrı tutulmalıdır.
- **Pedagojik vurgu:** Bu örnekte local ve global bağlantılılık birlikte doğrudur; fakat bu birliktelik genel bir zorunluluk değildir.

### LP-05 — Ayrık uzaylar yerel olarak iyi davranabilir

- **Model:** herhangi bir ayrık uzay.
- **Beklenen davranış:** her tekil küme açık olduğundan local compactness, local connectedness ve first countability için küçük yerel tanıklar vardır.
- **pytop sözleşmesi:** ayrık uzay örnekleri noktasal yerel taban olarak `{x}` ailesini kullanabilir.
- **Pedagojik vurgu:** Yerel iyi davranış, global sayılabilirlik veya global bağlantılılık iddiası vermez.

### LP-06 — Birinci sayılabilirlik yerel taban şartıdır

- **Model:** metrik uzayda bir nokta `x` ve `B(x,1/n)` topları.
- **Beklenen davranış:** bu sayılabilir aile `x` için yerel taban adayıdır.
- **pytop sözleşmesi:** metrik-benzeri örneklerde `first_countable=true` etiketi yerel taban tanığıyla açıklanmalıdır.
- **Pedagojik vurgu:** Birinci sayılabilirlik nokta başına sayılabilirliktir; tüm uzay için tek bir global taban iddiası değildir.

### LP-07 — İkinci sayılabilirlik global taban şartıdır

- **Model:** `R` üzerinde rasyonel uçlu açık aralıklar.
- **Beklenen davranış:** sayılabilir bir global taban elde edilir.
- **pytop sözleşmesi:** ikinci sayılabilirlik etiketi bütün açık kümeleri üreten tek sayılabilir taban verisine bağlanmalıdır.
- **Pedagojik vurgu:** Second countability global bir kontrol ister; first countability'den otomatik çıkmaz.

### LP-08 — Sayılamaz ayrık uzay first countable olup second countable değildir

- **Model:** sayılamaz ayrık taşıyıcı.
- **Beklenen davranış:** her nokta için `{x}` yerel tabanı first countability verir; fakat global taban tüm tekilleri ayırmak zorunda olduğundan sayılamaz olur.
- **pytop sözleşmesi:** `uncountable_discrete` etiketi `first_countable=true`, `second_countable=false` ayrımını güvenli biçimde taşımalıdır.
- **Pedagojik vurgu:** Birinci ve ikinci sayılabilirlik arasındaki fark en temiz biçimde ayrık uzayda görülür.

### LP-09 — Ayrık toplam local connected fakat disconnected olabilir

- **Model:** iki kopya açık aralığın topolojik toplamı.
- **Beklenen davranış:** her nokta kendi bileşeni içinde bağlantılı küçük aralık komşuluklarına sahiptir; ancak toplam uzay iki açık-kapalı parçaya ayrılır.
- **pytop sözleşmesi:** `construction_bridge_examples.md` içindeki topological sum ayrımıyla uyumlu biçimde local/global bağlantılılık farkı korunmalıdır.
- **Pedagojik vurgu:** Local connectedness, connectedness anlamına gelmez.

### LP-10 — Rasyonel doğru local compactness için uyarı örneğidir

- **Model:** `Q` altuzayı ve standart metrik/topoloji.
- **Beklenen davranış:** rasyonel aralık kapanışları `Q` içinde kompaktlık tanığı gibi kullanılmamalıdır; irrasyonel limite yaklaşan Cauchy tanıkları dikkat gerektirir.
- **pytop sözleşmesi:** bu sürüm `Q` için otomatik local compactness ispatı üretmez; örnek bankası bunu warning-line olarak tutar.
- **Pedagojik vurgu:** Metrik olmak local compactness için yeterli değildir.

### LP-11 — Topolojik toplam local second countable olabilir ama second countable olmayabilir

- **Model:** sayılamaz çoklukta `R` kopyasının ayrık topolojik toplamı.
- **Beklenen davranış:** her nokta kendi kopyasında sayılabilir yerel tabana sahiptir; fakat tüm bileşenleri global olarak yakalayan sayılabilir taban yoktur.
- **pytop sözleşmesi:** sum inşa sözleşmesi local countability ile global countability ayrımını ayrı alanlarda saklamalıdır.
- **Pedagojik vurgu:** Local smallness, çok bileşenli uzaylarda global smallness'a dönüşmeyebilir.

## Mevcut yüzeylerle bağlantı

- `countability_examples.md`: birinci/ikinci sayılabilirlik aksiyomları.
- `compactness_examples.md`: kompaktlık benchmarkları.
- `connectedness_examples.md`: bağlantılılık ve bileşen uyarıları.
- `construction_bridge_examples.md`: topological sum ve quotient/subspace/product ayrımı.
- `convergence_examples.md`: first countability altında dizisel testlerin neden daha anlamlı hale geldiği uyarısı.

## Sonraki genişleme notu

v1.0.297, bu yerel özellik yüzeyinden sonra kompaktlık varyantlarını ayırmalıdır: countably compact, sequentially compact ve Lindelöf davranışları aynı özellikmiş gibi işlenmemelidir.
