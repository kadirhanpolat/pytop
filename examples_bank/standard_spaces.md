# Standard spaces

Bu dosya, Cilt I boyunca tekrarlanan temel örnek uzayları kısa notlarla bir araya getirir.

## Çekirdek örnekler

- **Discrete space**: Her altkümenin açık olduğu uzay. Ayırma, sayılabilirlik ve yakınsaklık tartışmalarında uç örnek.
- **Indiscrete space**: Yalnız boş küme ve tüm uzayın açık olduğu uzay. Birçok olumlu özelliğin neden ek varsayım gerektirdiğini gösterir.
- **Sierpiński space**: $T_0$ olup $T_1$ olmayan temel sonlu örnek.
- **Cofinite topology**: Sonsuz kümelerde $T_1$ olup Hausdorff olmayan klasik örnek.
- **Cocountable topology**: Sayılabilirlik ve yakınsaklık davranışlarını test etmek için yararlı sonsuz örnek.
- **Real line** $\mathbb{R}$: İkinci sayılabilir, ayrılabilir, Lindelöf ve metrik temel örnek.
- **Rationals** $\mathbb{Q}$: Yoğun, sayılabilir ve metrik altuzay örneği.
- **Intervals in $\mathbb{R}$**: Bağlılığın ilk doğal örnekleri.
- **Order topology on $\mathbb{R}$**: Standart topolojinin sıralama temelli ikinci okunuşu; açık aralıkları doğal alt tabandan yeniden üretir.
- **Lower limit topology on $\mathbb{R}$**: $[a,b)$ tabanı ile üretilen klasik doğrusal örnek; Chapter 04'te taban ölçütü, Chapter 12'de sayılabilirlik ayrımı için kullanılır.
- **Upper limit topology on $\mathbb{R}$**: $(a,b]$ tabanı ile üretilen simetrik doğrusal örnek; ``aynı taşıyıcı, farklı taban'' ilkesini görünür kılar.
- **Finite topological spaces**: Kompaktlık ve Aleksandrov köprüsü için hesaplamalı laboratuvar.

## Bölüm ilişkileri

- Bölüm 03--05: temel topoloji örnekleri
- Bölüm 11--12: ayırma ve sayılabilirlik örnekleri
- Bölüm 13--16: bağlılık, kompaktlık, metrik ve dizi örnekleri
- Bölüm 17: sonlu uzay örnekleri

## Bölüm bazlı gönderme ağı

- **Bölüm 03--05**: ayrık, indiscrete, Sierpiński, sonlu tümleyenli ve sayılabilir tümleyenli uzaylar temel omurgayı taşır.
- **Bölüm 06--09**: özdeşbiçimlilik, altuzay, çarpım ve bölüm uzayı örnekleri için reel doğru, aralıklar ve çember örnekleri öne çıkar.
- **Bölüm 10--14**: topolojik özellikler, ayırma, sayılabilirlik, bağlılık ve kompaktlık için aynı örneklerin farklı açılardan yeniden kullanılması önerilir.
- **Bölüm 15--16**: metrik uzay ve yakınsaklık örneklerinde $\mathbb{R}$, $\mathbb{Q}$ ve aralıklar ana başvuru sınıfıdır.
- **Bölüm 17**: sonlu uzaylar ve Aleksandrov tipi örnekler, hesaplamalı laboratuvar rolü görür.

## Bölüm 11 ve 14 için specialized-contrast katmanı (v0.8.102)

### Bölüm 11 — benchmark ailesi

Bu bölümde standart uzayların görevi, her aksiyom seviyesini güvenli ve tekrar kullanılabilir örnekler üzerinden sabitlemektir.

- **Ayrık uzay**: Hausdorff çizginin en temiz benchmark örneği; ayırma aksiyomlarının olumlu ucu burada görünür.
- **Sierpiński uzayı**: $T_0$ ile $T_1$ ayrımını tek bakışta görünür kılan minimal benchmark örneği.
- **Metrik uzaylar / reel doğru**: Hausdorff olmanın yalnız soyut bir aksiyom değil, doğal örneklerde sürekli görülen bir yapı olduğunu gösterir.

### Bölüm 14 — benchmark ailesi

Bu bölümde standart uzaylar, kompaktlığın olumlu yüzünü güvenli başlangıç örnekleriyle sabitlemelidir.

- **$[0,1]$**: açık örtü tanımının ilk temel olumlu benchmark örneği.
- **Sonlu topolojik uzaylar**: kompaktlık fikrinin hesaplanabilir ve sezgisel laboratuvarı.
- **Sürekli görüntü altında kompaktlık**: $[0,1]$ ve sonlu uzaylar üzerinden, tanımın korunum ilkesi ile nasıl çalıştığını görünür kılar.


## Chapter 06 continuity benchmark cluster (v1.0.77)

- **Constant maps**: ters görüntü tanımının en kısa olumlu örneği; her topoloji çiftinde süreklidir.
- **Identity map under finer/coarser topologies**: aynı taşıyıcı üzerinde sürekliliğin topoloji kapsaması ile nasıl değiştiğini görünür kılar.
- **Absolute value map on $\mathbb{R}$**: taban elemanlarının ters görüntüsüyle okunabilen ilk standart reel örneklerden biridir.
- **Projection $\pi_1:\mathbb{R}^2	o\mathbb{R}$**: sürekli ve açık davranışın, ama zorunlu olarak kapalı davranışın değil, klasik benchmark örneğidir.
- **$(0,1)\cong \mathbb{R}$**: özdeşbiçimlilik sezgisinin temel benchmark örneği; boundedness / length warning-line'ları için de kullanılır.

## Bölüm 06--09 için ayrıntılı gönderme notları

- **Bölüm 06**: özdeşlik, sabit fonksiyon, $(0,1)\cong \mathbb{R}$ ve kapsama haritaları sürekli fonksiyon dilini kurmak için kullanılır.
- **Bölüm 07**: $(0,1] \subseteq \mathbb{R}$, $(0,1/2] \subseteq (0,1]$ ve $\mathbb{Q} \subseteq \mathbb{R}$ altuzay ve yoğunluk örneklerinin ana kaynağıdır.
- **Bölüm 08**: $\mathbb{R}^2$, ayrık uzay çarpımları ve yansıtım fonksiyonları çarpım topolojisi sezgisini taşır.
- **Bölüm 09**: ayrık birleşimler ile $[0,1]/(0\sim 1)$ özdeşleştirmesi, bölüm topolojisi için ana olumlu örneklerdir.

## Volume I early-chapter additions (v0.5.31)

- **Sierpiński-type two-point space**: useful in Chapter 03 as a minimal nontrivial topology and as a bridge toward continuity/homeomorphism discussions.
- **Rational-endpoint interval basis on \(\mathbb{R}\)**: emphasized in Chapter 04 as the canonical countable basis example.
- **Half-line subbasis of the real line**: emphasized in Chapter 04 to show how a smaller generating family can recover the standard topology.
- **Dense set with empty interior**: the pair \(\mathbb{Q}\subseteq\mathbb{R}\) is highlighted in Chapter 05 as the model example separating density from interior largeness.

## v0.5.32 ara notu

06--09 hattı için aşağıdaki örneklerin artık yalnız isim olarak değil, ispat kalıbı bağlamında da okunması önerilir:

- **Bölüm 06**: özdeşlik ve sabit fonksiyon örnekleri, ters görüntü tanımının en kısa sınama örnekleridir.
- **Bölüm 07**: $(0,1] \subseteq \mathbb{R}$ ve $\mathbb{Q}\subseteq \mathbb{R}$, göreli açıklık ile yoğunluk ispatlarının temel laboratuvarıdır.
- **Bölüm 08**: $\mathbb{R}^2$ ve doğal yansıtımlar, çarpım topolojisinde taban elemanı ters görüntüsü stratejisinin ana örneğidir.
- **Bölüm 09**: $[0,1]/(0\sim 1)$ ve ayrık birleşim örnekleri, evrensel özellik ve bölüm topolojisinin ters görüntü üzerinden kurulmasını görünür kılar.

## v0.5.33 focus additions

- Chapter 10: property/invariant contrast anchored by compactness, connectedness, weight, and density.
- Chapter 11: Sierpiński space, cofinite topology, and discrete spaces highlighted as the minimal comparison family for separation axioms.
- Chapter 12: real line and rational-endpoint interval basis emphasized as the standard second-countable model.
- Chapter 13: intervals in $\mathbb{R}$ and convex subsets stressed as canonical connected/path-connected examples.
- Chapter 14: $[0,1]$ and finite spaces foregrounded as the canonical compact examples.

## v0.5.37 notebook note

Bu sürümde seçilmiş olumlu örnek aileleri için `notebooks/exploration/` altında doğrudan not defteri karşılıkları eklendi. Özellikle iki noktalı uzaylar, taban/alt taban örnekleri, kapanış-iç-sınır deneyleri, metrik/sayılabilirlik köprüleri ve sonlu Aleksandrov örnekleri artık ayrı keşif not defterleriyle desteklenmektedir.

## v0.6.13 — Cilt II nicel/kardinal hat köprüsü

Aşağıdaki notlar, standart uzayların Cilt II `24--31` hattında neden yeniden öne çıktığını kaydeder:

- **\(\mathbb{R}\)**: ikinci sayılabilirlik, ayrılabilirlik ve Lindelöf davranışı aynı uzayda birlikte görüldüğü için `w(X)`, `d(X)`, `\chi(X)` ve `L(X)` çevresindeki ilk olumlu modeldir.
- **\(\mathbb{Q}\)**: sayılabilir ve yoğun oluşu sayesinde, yoğunluk ile taban büyüklüğü arasındaki sezgiyi destekler; aynı zamanda `\mathbb{R}` altuzayı olarak karşılaştırmalı okunabilir.
- **Sonsuz ayrık uzay**: her noktada çok küçük yerel veri bulunmasına rağmen tüm uzayın yoğun denetimi için büyük küme gerekebileceğini gösterir; bu yüzden karakter ile yoğunluk/ağırlık ayrımı için ana örnektir.
- **İndiscrete uzay**: çok küçük tabansal veri ile çok zayıf ayırma davranışının aynı anda görülebileceği uç örnektir; nicel küçüklük ile topolojik zenginliğin aynı şey olmadığını hatırlatır.
- **Kofinite / cocountable topolojiler**: sayılabilirlik ve ayırma aksiyomları ile nicel eşikler arasındaki doğrudan olmayan ilişkiyi görünür kılar.
- **Sonlu uzaylar**: nicel değişmezlerin `pytop.invariants` ile hesaplanabildiği laboratuvar olarak, soyut kardinal fonksiyon tartışmasını pedagojik olarak somutlar.

## 24--31 hattı için kısa kullanım tablosu

| Uzay | En doğal bölümler | Taşıdığı ana mesaj |
|---|---|---|
| \(\mathbb{R}\) | 24, 25, 30, 31 | küçük taban + küçük yoğunluk + metrik olumlu model |
| \(\mathbb{Q}\) | 25, 30, 31 | yoğun sayılabilir altuzay sezgisi |
| sonsuz ayrık uzay | 24, 25, 30, 31 | küçük karakter / büyük yoğunluk / büyük ağırlık ayrımı |
| indiscrete uzay | 24, 25 | küçük veri ile zayıf yapı birlikte olabilir |
| kofinite / cocountable uzaylar | 21, 25, 30, 31 | nitel olumlu özellikler ile nicel küçüklük farklı yönlere gidebilir |
| sonlu uzaylar | 24, 25, 29, 30 | hesaplanabilir örnek laboratuvarı |


## v1.0.60 Chapter 03/05/07/18 integration note

Aşağıdaki kısa çizgi, kaynak Bölüm 5'in bizim modüler yapıya nasıl dağıldığını görünür kılmak için eklendi.

- **Discrete / indiscrete uzaylar**: Chapter 03'te topoloji aksiyomları için, Chapter 05'te iç-kapanış-sınır davranışı için, Chapter 18'de komşuluk sisteminin uç halleri için birlikte okunmalıdır.
- **Cofinite topology**: Chapter 03'te ara topoloji örneği, Chapter 05'te yoğunluk/closure davranışı, Chapter 16'da dizisel sezginin sınırlılığı için warning-line rolü görür.
- **\(\mathbb{Q}\subseteq\mathbb{R}\)**: Chapter 05'te dense ama içi boş olabilen küme, Chapter 07'de yoğun altuzay, Chapter 16'da metric/sequential sezgi ile topolojik closure arasındaki köprü olarak kullanılmalıdır.
- **Sonlu uzaylar**: Chapter 03'te hangi aile topolojidir sorusunun laboratuvarı, Chapter 07'de göreli açıklık/kapalılık laboratuvarı, Chapter 18'de komşuluk sistemini elle listeleme laboratuvarıdır.

## Foundational benchmark pairs (v0.8.102)

Bu sürümde Cilt I specialized-contrast katmanı için aşağıdaki benchmark eşleşmeleri açık hale getirildi:

- **Bölüm 11**: ayrık uzay ve Sierpiński uzayı, ayırma aksiyomları zincirinin güvenli başlangıç benchmark çiftidir. Bu iki örnek, `counterexamples.md` içindeki cofinite ve indiscrete warning örnekleriyle birlikte okunmalıdır.
- **Bölüm 14**: `[0,1]` aralığı ile sonlu topolojik uzaylar, kompaktlık için temel benchmark çiftidir. Bunlar, `(0,1)` ve kompakt ama Hausdorff olmayan örneklerle birlikte okutulduğunda kavramın sınırı daha görünür olur.
- **Pedagojik kural**: bu benchmark örnekler, yalnız olumlu tanım uygulaması için değil, yanlış kısa çıkarımları önleyen contrast okumaları için de kullanılmalıdır.

Böylece `standard_spaces` ile `counterexamples` dosyaları arasında yalnız gevşek bir çapraz gönderme değil, doğrudan bir benchmark-versus-warning hattı kurulmuş olur.


## v1.0.54 classical line-and-plane strengthening

Bu sürümde standart uzay ailesi içinde özellikle Chapters `14--16` için aşağıdaki benchmark omurga açık hale getirildi.

### Reel doğru benchmark hattı

- **$\mathbb{R}$**: metrik, ikinci sayılabilir ve ayrılabilir güvenli temel uzay. Komşuluk, açık küme, limit, closure ve continuity dili burada ilk kez doğal görünür.
- **Açık aralıklar**: metrik açık top sezgisinin çizgisel yüzü. “Her noktada içeride daha küçük bir açıklık vardır” fikrini temiz biçimde taşır.
- **Kapalı aralıklar $[a,b]$**: kompaktlık için klasik olumlu benchmark. Heine--Borel anlatımında ilk güvenli laboratuvar burasıdır.
- **$\mathbb{Q}$ ve irrasyoneller**: yoğunluk, boş iç, boundary ve closure ayrımlarını aynı uzayda görünür kılan çift örnek.

### Reel düzlem benchmark hattı

- **$\mathbb{R}^2$**: açık top ile açık disk arasındaki iki boyutlu sezgiyi taşır; çarpım topolojisi ile metrik topoloji arasındaki köprü için özellikle yararlıdır.
- **Açık diskler**: $\mathbb{R}^2$ içindeki temel yerel komşuluk modeli. Bölüm 15 için yalnız bir kenar notu değil, pedagojik merkez örnektir.
- **Rasyonel merkezli/rasyonel yarıçaplı diskler**: ikinci sayılabilirliği somutlayan sayılabilir taban ailesi.

### Bölüm 14--16 için açık kullanım önerisi

- **Bölüm 14**: $[0,1]$ ve $(0,1)$ birlikte okutulmalı; biri benchmark, diğeri warning-line örneğidir.
- **Bölüm 15**: açık aralık / açık top / açık disk üçlüsü aynı zincir içinde gösterilmelidir.
- **Bölüm 16**: $1/n$, $(-1)^n$, rasyonel yaklaşık dizileri gibi örnekler standart uzay omurgasının doğal uzantısı olarak kullanılmalıdır.


## v1.0.58 Chapter 05 operational note

Bu sürümde Chapter 05 için standart uzay örnekleri yalnız isim olarak değil, işleç davranışı açısından da sabitlendi. Özellikle şu dört örnek birlikte okunmalıdır:

- **Ayrık uzay**: her altküme için `int(A)=A`, `cl(A)=A`, `ext(A)=X\setminus A`, `bd(A)=\varnothing`, `A'=\varnothing`.
- **İndiscrete uzay**: boş olmayan uygun altkümelerde iç ve dış boş, sınır tüm uzaydır.
- **Kofinite topoloji**: sonsuz altkümelerin kapanışı çoğu kez tüm uzaya çıkar; yoğunluk davranışı erken safhada burada test edilmelidir.
- **\(\mathbb{Q}\subseteq\mathbb{R}\)** ile **\(\{1/n:n\in\mathbb{N}\}\)**: biri yoğun ama nowhere dense olmayan, diğeri nowhere dense olan klasik çift örnektir.

Bu dört örnek, Chapter 05'teki closure/interior/boundary/ext/derived ayrımlarının güvenli benchmark ailesi olarak kullanılmalıdır.


## v1.0.64 Chapter 04 classical-line note

Bu sürümde Chapter 04 için aşağıdaki doğrusal örnek hattı artık açıkça birlikte okunmalıdır:

- **Doğal düzen topolojili $\mathbb{R}$**: standart topolojinin yalnız metrik değil, düzen kaynaklı da okunabildiğini gösterir.
- **Alt limit topolojisi**: $[a,b)$ tabanının gerçekten taban ölçütlerini sağladığını gösteren ilk yarı-açık aralık örneğidir.
- **Üst limit topolojisi**: $(a,b]$ tabanı ile simetrik ikinci yarı-açık aralık örneği; standart topolojiden daha ince ama onunla yakından ilişkili bir modeldir.
- **Pedagojik rol**: bu üçlü, Chapter 04'te taban/alt taban inşasını zenginleştirir; Chapter 12'de ise özellikle alt limit topolojisi warning-example ailesine geri döner.


## v1.0.70 Chapter 04 benchmark widening

Bu sürümde `standard_spaces` dosyasının Chapter 04 koridoru daha dürüst ve daha kullanışlı hale getirildi. Artık yalnız ``hangi uzaylar standarttır?'' sorusu değil, ``hangi standart uzay hangi taban/yerel taban fikrini en temiz taşır?'' sorusu da görünür tutulmalıdır.

### Rational-endpoint interval basis on \(\mathbb{R}\)

- aile: `\(\mathcal{B}_{\mathbb{Q}}=\{(p,q): p,q\in\mathbb{Q},\ p<q\}\)`
- rol: standart reel topolojisinin sayılabilir taban benchmark'ı
- en doğal kullanım: Bölüm 04, Bölüm 12
- pedagojik mesaj: aynı topoloji, daha ``ekonomik'' bir taban ailesi ile de üretilebilir; tüm açık aralıkları tek tek taşımak zorunlu değildir.

### Local-base benchmark family

Aşağıdaki dört örnek, yerel taban fikri için birlikte okunmalıdır:

- **\(\mathbb{R}\) içinde bir nokta \(x\)**: `\((x-\varepsilon,x+\varepsilon)\)` aileleri yerel tabandır.
- **\(\mathbb{R}^2\) içinde bir nokta \((a,b)\)**: açık diskler veya açık dikdörtgenler aynı yerel dili taşır.
- **Alt limit doğrusu**: `\([x,x+\varepsilon)\)` aileleri, standart çizgi sezgisinin neden tek seçenek olmadığını gösterir.
- **Ayrık uzay**: `\(\{x\}\)` ailesi, yerel tabanın tek üyeye kadar küçülebileceğini gösterir.

Pedagojik mesaj: ``yerel taban'' yalnız bir tanım değil, aynı uzayı farklı açıklık aileleriyle okumayı mümkün kılan karşılaştırma aracıdır.

### Same-topology / different-basis note

Chapter 04'te şu üç çizgi artık birlikte verilmelidir:

- standart açık aralık tabanı,
- rasyonel uçlu açık aralık tabanı,
- açık yarı-doğrular alt tabanı.

Bu üçlü, şu iki farkı temiz biçimde ayırır:

1. **aynı topolojiyi veren farklı üretici aileler**,
2. **farklı topoloji veren farklı üretici aileler**.

İlk grupta standart açık aralıklar ile rasyonel uçlu açık aralıklar aynı topolojiyi verir. İkinci grupta alt limit topolojisi artık gerçekten farklı bir doğrusal modeldir.

## v1.0.114 Chapter 12 assessment-routing note

Bu sürümde `standard_spaces` dosyası, dedicated `04a_countability_axioms` worksheet ve quick-check ailesiyle hizalanacak biçimde yeniden okunmalıdır.

### Assessment-ready benchmark family

- **`\mathbb{R}`**: Chapter 12 için ana güvenli benchmark. Yerel taban, rasyonel uçlu sayılabilir taban, Lindelöf indirgeme ve metrik güvenli bölge aynı omurgada görünür.
- **`\mathbb{R}^m`**: `separable metric => second countable` teoreminin sınıfta somutlaştırıldığı ana çok boyutlu benchmark.
- **Rational-endpoint intervals on `\mathbb{R}`**: ``ekonomik taban'' fikrinin assessment-friendly yüzü.
- **Rational-center / rational-radius balls in `\mathbb{R}^m`**: yoğun küme + `\mathbb{Q}_{>0}` şemasının doğrudan sınıf içi modeli.

### Chapter 12 için örnek-bankası okuma kuralı

Önce benchmark aile okunmalı, sonra warning-line aileye geçilmelidir:

1. `\mathbb{R}` ve `\mathbb{R}^m` ile güvenli countability koridoru,
2. ardından alt limit doğrusu ve benzeri warning örnekleri,
3. en son hereditary caution ve sequence-only warning.

Bu sıralama, `04a_countability_axioms` değerlendirme ailesinin dilini daha dürüst hale getirir; öğrenci doğrudan warning örneğe atlamadan önce güvenli modeli görmüş olur.


## Chapter 05 finite-operator laboratory (v1.0.173)

- **Finite topology verifier spaces**: küçük taşıyıcı kümeler üzerinde aday açık küme ailelerinin topoloji aksiyomlarını sağlayıp sağlamadığını tanıkla kontrol etmek için kullanılır.
- **Operator-calculus finite spaces**: `cl(A)`, `int(A)`, `ext(A)` ve `bd(A)` işlemlerinin aynı örnekte birlikte hesaplandığı özgün alıştırma aileleri için ayrılmıştır.
- **Relative-topology carriers**: alt uzay topolojisinde farklı ambient açık kümelerin aynı göreli açık kümeyi verebileceğini göstermek için kullanılmalıdır.
- **Finer/coarser comparison triples**: aynı taşıyıcı üzerindeki üç topolojinin kapsama düzeni ve özdeşlik haritası sürekliliği ön okuması için benchmark görevi görür.


## Chapter 06 basis/subbasis standard generation surfaces (v1.0.174)

- **Basis witness carriers**: küçük taşıyıcı kümelerde örtme ve kesişim tanığını aynı anda sınamak için kullanılacak özgün finite-space örnekleri.
- **Subbasis-to-basis engines**: alt taban elemanlarından sonlu kesişim tabanı üretmeyi görünür kılan yapılandırılmış örnekler.
- **Relative basis restrictions**: alt uzay topolojisinde `B∩Y` biçimli taban elemanlarını tekrar temizliğiyle üretmek için kullanılacak örnek yüzeyi.
- **Continuity-through-basis bridge spaces**: hedef uzayın taban elemanlarının ters görüntüleri üzerinden süreklilik kontrolü için kullanılacak küçük fonksiyon örnekleri.


## v1.0.183 finite example stabilization

`examples_bank/finite_spaces_catalog_v1_0_183.md` ve `src/pytop_publish/finite_space_example_catalog.py` dosyaları, Sierpiński, ayrık/indiscrete iki noktalı uzay, üç noktalı zincir Aleksandrov uzayı ve süreklilik laboratuvarı gibi örnekleri kararlı kodlarla tanımlar.

## Chapter 03 anchor note -- v0.1.34

Chapter 03 should be read as the first durable topological-space anchor. Each standard example must be interpreted as a pair consisting of a carrier set and a specified open-set family.

## Chapter 04 bases/subbases bridge note -- v0.1.35

Chapter 04 should be read as the bridge from complete open-set data to smaller generating data: basis, subbasis, finite-intersection basis, generated topology, and local basis.

## Chapter 05 closure/interior/boundary bridge note -- v0.1.36

Chapter 05 should now be read as the standard-space operator corridor. Every standard example should record the ambient topology before closure, interior, exterior, boundary, derived-set, dense, and nowhere-dense claims are made.
