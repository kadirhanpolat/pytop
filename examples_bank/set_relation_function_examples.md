# Set / relation / function examples

Bu dosya, Cilt I'in ilk iki bölümü için gerekli olan kümesel, fonksiyonel ve bağıntısal örnekleri ortak bir yerde toplar. `v1.0.28` ile birlikte dosya yalnız uzun bir örnek listesi olmaktan çıkarılıp daha açık bir **koridor yapısı** içinde yeniden düzenlenmiştir. Amaç, erken ciltteki örnekleri şu üç ihtiyaca göre erişilebilir kılmaktır:

- **metin içi okuma desteği**
- **tahta / ders akışı desteği**
- **worksheet / quiz hazırlama desteği**

## Hızlı kullanım haritası

### Bölüm bazlı hızlı yönlendirme

- **Bölüm 01 çekirdeği**: §A0, §A1, §A2, §A3, §A4, §A5, §A6, §A7
- **Bölüm 02 relation foundation**: §B0, §B1, §B2, §B3
- **Bölüm 02 equivalence corridor**: §C1, §C2
- **Bölüm 02 order corridor**: §D1, §D2, §D3
- **Bölüm 09 köprüsü**: §C1, §C2
- **Bölüm 12 köprüsü**: §A5
- **Bölüm 17 köprüsü**: §D1, §D3

### Kullanım tipi bazlı hızlı yönlendirme

- **kısa worked example arayanlar**: §A2, §A4, §A7, §B0, §B2, §C2, §D2
- **karşı örnek arayanlar**: §A6, §B1, §D1, §D2
- **sınıflandırma tablosu hazırlayanlar**: §B1, §D1
- **ölçme-değerlendirme için hazır veri arayanlar**: §A4, §A7, §B2, §C2, §D2

## Yapısal iskelet

Bu dosya artık dört ana kümeye ayrılır:

- **A Bloğu — Bölüm 01 çekirdeği**
- **B Bloğu — bağıntı işlemleri ve relation hesabı**
- **C Bloğu — eşdeğerlik ve bölümleme koridoru**
- **D Bloğu — önsıra / kısmi sıralama / doğrusal sıralama koridoru**

Böylece aynı dosya hem metin içi örnek deposu, hem tahta akışı, hem de assessment hazırlık bankası gibi kullanılabilir.

---

# A Bloğu — Bölüm 01 çekirdeği

## A0. Gösterim, bağlam ve tip kontrolü

**Etiketler:** `Ch01-Core`, `notation-discipline`, `context-check`, `type-check`

Bu alt blok `v0.1.31` ile Cilt I başlangıcını daha güvenli hale getirmek için belirginleştirilmiştir. Burada tutulacak örnek türleri şunlardır:

- aynı altkümenin farklı evrensel kümeler içindeki tümleyenlerinin karşılaştırılması,
- `f\colon X\to Y` yazımında tanım kümesi ve hedef kümenin problem verisinin parçası olduğunu gösteren kısa görevler,
- bir ifadenin eleman mı, altküme mi, aile mi, yoksa fonksiyon değeri mi olduğunu sınıflandıran hızlı tip-kontrol soruları,
- topolojiye geçmeden önce kullanılacak bağlam cümleleri: "hangi uzayın içinde?", "hangi hedef kümeye?", "hangi indis kümesiyle?"

Bu blok, yeni örnek üretmek için kalıcı bir sorumluluk alanıdır; fakat fiziksel yeni dosya açılmadan mevcut foundation example corridor içinde tutulur.


## A1. Kümenin verilme biçimleri

**Etiketler:** `Ch01-Core`, `set-language`, `membership-subset`

Bu alt blok, Chapter 01 içindeki temel küme dilini tek noktadan çağırmak için tutulur. Özellikle şu örnekler burada gruplanır:

- eleman ile tek elemanlı küme ayrımı,
- boş küme ile boş olmayan tekil küme ayrımı,
- karışık elemanlı kümelerde üyelik ve altküme ayrımı,
- listeleme ile özellik-yazımı arasındaki geçiş.

## A2. Aralıklar ve temel altküme örnekleri

**Etiketler:** `Ch01-Core`, `intervals`, `subset-chain`

Bu blok şu örnek kümelerini birlikte tutar:

- açık, kapalı ve yarı açık aralıklar,
- ışın örnekleri,
- altküme ve özaltküme zincirleri,
- `\mathbb{N}\subsetneq\mathbb{Z}\subsetneq\mathbb{Q}\subsetneq\mathbb{R}` tipi temel gömme örnekleri.

## A3. Kuvvet kümesi ve aile örnekleri

**Etiketler:** `Ch01-Core`, `power-set`, `families`, `partitions-prep`

Bu blokta aynı türden ama farklı amaçlı üç örnek ailesi birlikte tutulur:

- küçük sonlu kümelerin kuvvet kümesi listeleri,
- ayrık ve ayrık olmayan aile örnekleri,
- bölümlemeye hazırlık yapan küçük aile örnekleri.

Bu düzenleme, Chapter 01 ile Chapter 02 arasında “family language → partition language” geçişini daha görünür kılar.

## A4. Kartezyen çarpım ve bağıntıya hazırlık

**Etiketler:** `Ch01->Ch02`, `cartesian-product`, `relation-gateway`, `finite-data`

Bu blok özellikle Chapter 01 sonu ile Chapter 02 başı arasında köprü kurmak için ayrılmıştır. Kullanım sırası şöyledir:

- önce sonlu Kartezyen çarpım yazılır,
- sonra bir çiftler kümesinin gerçekten `A\times B` içinde olup olmadığı kontrol edilir,
- ardından bu altkümenin bağıntı olarak okunmasına geçilir.

Bu yüzden bu blok hem Chapter 01 örneği, hem de Chapter 02 giriş verisi gibi çalışır.

## A5. Küme cebiri ve indisli aile örnekleri

**Etiketler:** `Ch01-Core`, `set-algebra`, `indexed-families`, `Ch12-bridge`

Bu blokta şu örnek aileleri tutulur:

- birleşim / kesişim / fark / tümleyen hesapları,
- De Morgan doğrulamaları,
- azalan ve artan indisli aileler,
- sayılabilir tekli aileler,
- boş indis kümesi uyarısı ve bağlamlı kesişim sözleşmesi,
- örtü ile bölümleme arasındaki ilk ayrım.

Böylece Chapter 12’deki sayılabilir aile dili için de erken bir köprü korunur.

## A6. Görüntü / ters görüntü ve erken karşı örnekler

**Etiketler:** `Ch01-Core`, `image-preimage`, `counterexamples`, `worksheet-ready`

Bu blok şu amaçla korunur:

- görüntü ile ters görüntünün aynı davranmadığını göstermek,
- eşitlik yerine yalnız içerim çıkan durumları görünür kılmak,
- Chapter 01 worksheet hattına hazır kısa karşı örnekler vermek.

## A7. Fonksiyon koridoru: özdeşlik, izdüşüm ve kodomain farkı

**Etiketler:** `Ch01-Core`, `functions`, `identity`, `projection`, `codomain-range`, `worksheet-ready`

Bu blok, dış Chapter 02 karşılaştırmasından sonra özellikle function tarafını daha görünür tutmak için açılmış hafif bir ek yüzeydir. Aynı yerde şu kısa örnek aileleri tutulur:

- **özdeşlik fonksiyonu**: `\operatorname{id}_A\colon A\to A` örneğinin neden hem birebir hem örten olduğunu sabitleyen mikro örnekler,
- **aynı kural, farklı hedef küme**: aynı formülle yazılan bir fonksiyonun hedef küme değişince örtenlik durumunun değişebildiğini gösteren kısa örnekler,
- **koordinat izdüşümleri**: `\pi_1\colon A\times B\to A` ve `\pi_2\colon A\times B\to B` için sonlu veri üstünde görüntü hesabı,
- **görüntü / ters görüntü ayrımını fonksiyon diliyle okuma**: `f[f^{-1}[V]]\subseteq V` ve `U\subseteq f^{-1}[f[U]]` içerimlerinin ne zaman eşitliğe dönüşmediğini gösteren küçük görevler.

Bu blok özellikle Chapter 01 ders akışında “fonksiyon dili yalnız tanımda kalmasın, küçük hesap örnekleriyle görülsün” ihtiyacını karşılar. Aynı zamanda product-topology öncesi izdüşüm sezgisi için de erken bir hazırlık yüzeyi sunar.

---

# B Bloğu — Bağıntı işlemleri ve relation hesabı

## B0. Chapter 01--02 geçiş kontrolü

Bu koridor, v0.1.32 ile Chapter 02 güçlendirmesine eklenen taşıyıcı-çarpım ve ilişki-tipi disiplinini örnek bankasına bağlar.

### B0.1. Aynı ikililer, farklı taşıyıcılar

\[
R=\{(1,a),(2,b)\}
\]
kümesini iki farklı bağlamda okuyalım:

- \(R\subseteq \{1,2\}	imes\{a,b\}\),
- \(R\subseteq \{1,2,3\}	imes\{a,b,c\}\).

İkililer aynı olsa da ikinci okumada \(3\) ve \(c\) taşıyıcıda bulunup bağıntı tarafından kullanılmayan elemanlardır. Bu nedenle bir bağıntı görevi verildiğinde yalnız ikili listesi değil, taşıyıcı çarpım da açık yazılmalıdır.

### B0.2. Bağıntı mı, fonksiyon grafiği mi?

\(X=\{0,1,2\}\), \(Y=\{u,v\}\) ve
\[
S=\{(0,u),(1,u),(1,v)\}\subseteq X	imes Y
\]
olsun. Bu küme bir bağıntıdır; fakat \(X\)'ten \(Y\)'ye bir fonksiyonun grafiği değildir. Çünkü \(1\) elemanı iki farklı hedefle ilişkilidir.

### B0.3. Önsıra / kısmi sıralama ayrımı

\(X=\{a,b,c\}\) üzerinde
\[
a\preceq b,\quad b\preceq a,\quad b\preceq c
\]
ve yansımalılık/geçişlilik için zorunlu olan çiftler de eklensin. Bu yapı bir önsıra olabilir; ancak \(a\preceq b\) ve \(b\preceq a\) iken \(a
eq b\) olduğu için antisimetriklik bozulur. Bu örnek, özelleşme önsırasının neden \(T_0\) koşulu olmadan kısmi sıralama olmak zorunda olmadığını hatırlatır.


## B1. Bağıntı özelliklerini sınıflandırma

**Etiketler:** `Ch02-Relation`, `classification`, `counterexamples`, `assessment-ready`

Bu blokta aşağıdaki örnek aileleri birlikte tutulur:

- bir çiftler kümesinin gerçekten `A\times B` altkümesi olup olmadığını kontrol etme,
- yansımalı / simetrik / geçişli / antisimetrik ayrımlarını görünür kılan sonlu örnekler,
- özelliklerin bağımsızlığını gösteren kısa karşı örnekler.

Bu yeniden düzenlemenin asıl amacı, Chapter 02 içinde dağınık duran relation örneklerini tek bir sınıflandırma yüzeyinde toplamak oldu.

## B2. Domain / range / inverse / composition koridoru

**Etiketler:** `Ch02-Relation`, `domain-range`, `inverse`, `composition`, `finite-computation`

Bu blokta şu işlemler aynı aile içinde tutulur:

- `\operatorname{dom}(R)` ve `\operatorname{ran}(R)` hesabı,
- ters bağıntı `R^{-1}` hesabı,
- bileşkenin sıralı iki-adımlı yol okuması,
- bileşke sırasının fark yarattığı sonlu örnekler,
- inverse-of-composition kimliğini sonlu veriyle doğrulayan örnekler.

Bu yapı sayesinde Chapter 02’nin relation hesabı kısmı tek başlık altında tekrar kullanılabilir hale gelir.

## B3. Assessment için hazır mikro görevler

**Etiketler:** `worksheet-ready`, `quiz-ready`, `classification`, `finite-computation`

Bu blok özellikle şu kısa soru tipleri için kaynak olarak tutulur:

- verilen çiftler kümesi gerçekten bağıntı mıdır,
- yansımalı / simetrik / geçişli mi,
- domain / range / inverse hesapla,
- bileşke sıraya duyarlı mı,
- inverse-of-composition özdeşliğini doğrudan doğrula.

---

# C Bloğu — Eşdeğerlik ve bölümleme koridoru

## C1. Eşdeğerlik sınıfı örnekleri

**Etiketler:** `Ch02-Equivalence`, `equivalence-classes`, `quotient-bridge`, `Ch09-bridge`

Bu blokta şu örnek aileleri birlikte tutulur:

- modüler aritmetik ile eşdeğerlik sınıfı okuma,
- aynı mutlak değere sahip olma gibi standart ama farklı eşdeğerlik örnekleri,
- bölüm kümesine geçişte kullanılacak sınıf dili.

Bu düzenleme, Chapter 09’daki bölüm kümesi ve bölüm uzayı sezgisini besleyen altyapıyı daha görünür hale getirir.

## C2. Sonlu blok okuması ve bölümleme geri dönüşü

**Etiketler:** `Ch02-Equivalence`, `finite-blocks`, `partition-roundtrip`, `assessment-ready`

Bu blokta özellikle şunlar yan yana durur:

- sonlu bir bağıntıyı bloklar halinde okuma,
- bölümlemeden bağıntı üretme,
- sınıfların ya eşit ya da ayrık olması ilkesini hızlı tanıma ölçütü olarak kullanma.

Bu düzenleme, Chapter 02 assessment yüzeyi ayrıştığında aynı örneklerin kolayca yeniden kullanılmasını hedefler.

---

# D Bloğu — Önsıra / kısmi sıralama / doğrusal sıralama koridoru

## D1. Temel karşılaştırma örnekleri

**Etiketler:** `Ch02-Orders`, `preorder`, `partial-order`, `linear-order`, `comparison`

Bu blokta şu karşılaştırmalar birlikte tutulur:

- preorder ama partial order olmayan örnek,
- partial order ama linear order olmayan örnek,
- linear order örneği,
- karşılaştırılamama vurgusu.

Bu sayede order koridoru yalnız terim listesi değil, örnek kümeleriyle bölünmüş bir öğretim yüzeyi haline gelir.

## D2. Minimal / maksimal / least / greatest ayrımı

**Etiketler:** `Ch02-Orders`, `minimal-vs-least`, `maximal-vs-greatest`, `assessment-ready`

Bu blok, Chapter 02 order koridorunda sık karışan terimleri ayrık örnek aileleri üzerinden sabitlemek için korunur:

- minimal ama least olmayan yapı,
- maximal ama greatest olmayan yapı,
- en küçük / en büyük kavramlarının tekillik yönü,
- worksheet için uygun kısa poset örnekleri.

## D3. Üst sınır ve Hasse okuması

**Etiketler:** `Ch02-Orders`, `upper-bounds`, `hasse`, `Ch17-bridge`

Bu blokta şu iki hedef öne çıkar:

- upper bound ile greatest element farkını görünür kılmak,
- Hasse diyagramında neden yalnız örtme ilişkilerinin bırakıldığını açıklamak.

Bu blok aynı zamanda Chapter 17 öncesi küçük sıralama laboratuvarı görevi görür.

---

# Assessment ve öğretim için kısa görev matrisi

## Tahta akışı için en uygun örnek kümeleri

- **ilk 15 dakika**: A2 + A4
- **Chapter 02 girişi**: B1 + B2
- **eşdeğerlik sınıfı oturumu**: C1 + C2
- **order oturumu**: D1 + D2 + D3

## Worksheet / quick-check için en uygun örnek kümeleri

- **doğrudan hesap**: A5, A6, A7, B2
- **doğru/yanlış veya sınıflandırma**: B1, D1
- **blok okuma / bölümleme**: C2
- **karşı örnek üretimi**: A6, A7, B1, D2

## Dosyanın yeni rolü

`v1.0.28` itibarıyla bu dosya artık yalnız örnek toplamı değil; erken cilt için bir **foundation example corridor** işlevi de görür. Bu yapı, sonraki sürümlerde Chapter 02 worksheet ayrıştırması ve notebook genişletmesi yapılırken doğrudan kaynak olarak kullanılacaktır.

---

# v1.0.169 — Chapter 01 gerçek item-family entegrasyon ek yüzeyi

Bu ek yüzey, Chapter 01 için önceki plan/preview notlarının gerçek questionbank ailelerine dönüştürülmesinden sonra örnek bankasının nasıl kullanılacağını netleştirir. Buradaki amaç, dış kaynaklardan örnek taşımak değil; aynı matematiksel becerileri bizim kitap ekosisteminin terminolojisiyle yeniden üretilebilir görev ailelerine bağlamaktır.

## E1. Üyelik–altküme tanılama ailesi

**Bağlı kod:** `QB-CH01-SET-LANG`

Tahta veya kısa quiz için küçük bir sonlu taşıyıcı seçilir. Öğrenciden şu üç ayrımı aynı anda yapması beklenir: eleman olma, tek elemanlı küme olma, altküme olma. Bu aile özellikle `a`, `{a}` ve `{{a}}` tipindeki gösterim karışıklıklarını erken yakalamak için kullanılmalıdır.

## E2. Evrensel kümeye bağlı işlem ailesi

**Bağlı kod:** `QB-CH01-SET-OPS`

Birleşim/kesişim/fark hesapları tek başına bırakılmaz; en az bir görevde tümleyenin hangi evrensel kümeye göre alındığı sorulur. Böylece öğrencinin işlemi mekanik yapması yerine, bağlamı okuması sağlanır.

## E3. Kuvvet kümesi–aile–bölümleme köprüsü

**Bağlı kod:** `QB-CH01-POWER-FAMILY`

Küçük bir taşıyıcıdan seçilen altküme aileleri cover, partition veya ikisi de olmayan yapı olarak sınıflandırılır. Bu aile Chapter 02'deki bölümleme/eşdeğerlik sınıfı diline hazırlık görevi görür.

## E4. Ürün kümesi ve bağıntıya geçiş ailesi

**Bağlı kodlar:** `QB-CH01-CART-PROD`, `QB-CH01-REL-GATEWAY`

Önce `A x B` açıkça listelenir; sonra seçilen bir altküme ilişki olarak yorumlanır. Son adımda aynı verinin fonksiyon olup olmadığı sorulur. Bu akış, ürün kümesini yalnız listeleme konusu olmaktan çıkarıp bağıntı diline bağlar.

## E5. Görüntü–ters görüntü ve kodomain farkı ailesi

**Bağlı kodlar:** `QB-CH01-IMG-PREIMG`, `QB-CH01-CODOMAIN-IMG`

Sonlu fonksiyon tabloları üzerinden görüntü ve ters görüntü hesaplanır. Ardından aynı tabloya farklı hedef küme verildiğinde örtenlik durumunun nasıl değiştiği tartışılır. Bu aile süreklilikteki ters görüntü diline erken hazırlık sağlar.

## E6. İndisli aile ve izdüşüm ailesi

**Bağlı kodlar:** `QB-CH01-FAMILY-OPS`, `QB-CH01-PROJECTION`

Bir indisli ailede önce birkaç somut aşama hesaplanır, sonra genel birleşim/kesişim paterni okunur. Ürün kümesindeki izdüşüm görevleriyle birlikte kullanıldığında, ilerideki ürün topolojisi ve taban/alt taban konularına kavramsal hazırlık sağlar.

## v1.0.170 — Chapter 02 relation--function bridge families

The Chapter 02 real-integration layer promotes earlier preview route notes into reusable task families. These are package-native generation surfaces, not copied exercises.

- `QB-CH02-REL-FUNC-GRAPH`: finite relation graphs are tested against the function criterion by varying omitted and repeated first-coordinate patterns.
- `QB-CH02-COMP-PATH`: composition is treated as two-step path reading before quotient and finite-space reachability examples.
- `QB-CH02-INJ-SURJ-INV`: inverse-relation and inverse-function claims are separated through finite carrier data.
- `QB-CH02-RESTRICT-EXTEND`: restriction, extension, and inclusion maps are prepared for later subspace language.
- `QB-CH02-INDEXED-PRODUCT`: indexed families and projections are introduced as product-topology preparation.
- `QB-CH02-GEN-UNION-INTER`: generalized union/intersection tasks are framed as proof skeletons.
- `QB-CH02-IMAGE-PREIMAGE`: image/preimage comparisons are marked as continuity preparation.
- `QB-CH02-QUOTIENT-FACTOR`: same-value partitions and quotient factorization bridge Chapter 02 to quotient topology and T0-reduction language.



---

## v0.1.31 — Cilt I foundation strengthening note

Bu sürümde Chapter 01 örnek koridorunun amacı, yeni fiziksel dosya üretmeden üç zayıf noktayı güçlendirmektir:

1. tümleyen hesabında bağlam kümesini açık yazma,
2. indisli aileleri yalnız "kümelerin kümesi" değil, indisli atama olarak okuma,
3. fonksiyonlarda hedef küme ile görüntü kümesini karıştırmama.

Bu not, `manuscript/volume_1/chapters/01_sets_functions_families.tex`, quick-check yüzeyleri ve Chapter 01 questionbank starter-task diliyle uyumlu tutulmalıdır.

## v0.1.32 — Cilt I relation/order strengthening note

v0.1.32 strengthens the Chapter 02 corridor without adding a new file. The example-bank emphasis is now:

- always record the carrier product before classifying a relation;
- distinguish a general relation from a function graph;
- read equivalence relations and partitions as mutually converting but conceptually different data;
- keep preorder, partial order, and linear order separate;
- connect specialization preorder and finite \(T_0\) spaces to the later topology chapters.

