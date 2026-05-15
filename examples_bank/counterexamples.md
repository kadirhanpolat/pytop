# Counterexamples

Bu dosya, Cilt I boyunca öne çıkan karşı örnekleri kısa notlarla bir araya getirir.

## Çekirdek karşı örnekler

- **Indiscrete space on more than one point**: $T_0$ bile olmayan, fakat kompakt olan uzay.
- **Cofinite topology on an infinite set**: $T_1$ olup Hausdorff olmayan klasik karşı örnek.
- **Sorgenfrey line**: Birinci sayılabilir olup ikinci sayılabilir olmayan örnek.
- **Open-ray family on $\mathbb{R}$**: Taşıyıcıyı örtmesine rağmen doğrudan taban olmayan, fakat alt taban olarak çalışan erken warning örneği.
- **Topologist's sine curve**: Bağlı olup yol bağlı olmayan örnek.
- **Open interval $(0,1)$**: Reel doğruda kompakt olmayan temel örnek.
- **Compact non-Hausdorff spaces**: ``Kompakt ise Hausdorff'' çıkarımının yanlış olduğunu gösterir.
- **Non-first-countable spaces**: Dizilerin kapanışı bütünüyle yakalayamadığını gösteren örnek ailesi.
- **Finite $T_1$ spaces**: Sonlu bağlamda $T_1$ koşulunun ayrıklığa zorladığını gösteren karşılaştırma örneği.

## Kullanım önerisi

Bu dosya, bölüm sonu alıştırmalarında ve not defteri bağlantılarında çapraz gönderme için kullanılmalıdır. İleriki sürümlerde her karşı örnek için ayrı kısa açıklama, bölüm numarası ve not defteri bağı eklenmesi planlanmaktadır.

## v1.0.7 foundational contrast additions

Bu sürümde erken bölümler için aşağıdaki contrast örnekleri özellikle görünür kabul edilmelidir; ayrıntılı hesaplar `set_relation_function_examples.md` dosyasında tutulur, burada ise uyarı çizgileri kaydedilir.

- **Görüntü kesişimi warning-line**: her zaman `f[A\cap B]\subseteq f[A]\cap f[B]` olur, fakat eşitlik bozulabilir; `f(x)=x^2`, `A=\{-1\}`, `B=\{1\}` örneği temel uyarıdır.
- **Ters görüntü ile görüntü asimetrisi**: `A\subseteq f^{-1}[f[A]]` ve `f[f^{-1}[C]]\subseteq C` içerimleri her zaman vardır; fakat eşitlik için ek varsayım gerekir. Bu, Chapter 1 fonksiyon hattında temel warning-line'dır.
- **Örtü ama bölümleme olmayan aile**: taşıyıcıyı örten her aile bölümleme değildir; parçaların ayrık olması gerekir. Erken assessment hattında bu ayrım özellikle sorulmalıdır.
- **Yansımalı ve simetrik ama geçişli olmayan bağıntı**: relation checklist'inin mekanik ezbere indirgenmemesi için küçük sonlu örnekler kullanılmalıdır.
- **Önsıra ama kısmi sıralama olmayan örnek**: antisimetri eksikliği nedeniyle preorder ile partial order ayrımı mutlaka ayrı bir warning-line olarak korunmalıdır.



## Chapter 06 continuity warning cluster (v1.0.77)

- **Continuous bijection need not be a homeomorphism**: ayrık topolojiden kaba topolojiye özdeşlik haritası ana warning-line olarak korunmalıdır.
- **Sequentially continuous need not be continuous**: sayılabilir tümleyenli topoloji örneği, Chapter 16'ya giden uyarı hattının Chapter 06'da ilk görünümüdür.
- **Open but not closed**: düzlemden doğruya projeksiyon, map-class ayrımlarında güvenilir benchmark karşı örnektir.
- **Closed but not open**: $[0,\infty)\hookrightarrow \mathbb{R}$ kapsaması, continuity/open/closed ayrımını aynı taşıyıcı geometrisinde görünür kılar.

## Bölüm bazlı kullanım haritası

- **Bölüm 11**: sonlu tümleyenli topoloji ve indiscrete uzay, ayırma aksiyomlarının ayrışmasını göstermek için kullanılmalıdır.
- **Bölüm 12**: Sorgenfrey doğrusu, birinci ve ikinci sayılabilirlik ayrımının temel kaynağıdır.
- **Bölüm 13**: topologist's sine curve, bağlılık ve yol bağlılık ayrımında merkezi karşı örnektir.
- **Bölüm 14**: $(0,1)$ ve kompakt ama Hausdorff olmayan uzaylar, kompaktlık sezgisini dengelemek için birlikte kullanılmalıdır.
- **Bölüm 16**: birinci sayılabilir olmayan uzaylar, dizilerin yetersizliğini görünür kılar.
- **Bölüm 17**: sonlu $T_1$ uzaylar, sonlu bağlamda ayrıklık zorlamasını açıkça gösterir.

## Bölüm 11 ve 14 için specialized-contrast katmanı (v0.8.102)

### Bölüm 11 — warning-line ailesi

Bu bölümde karşı örneklerin görevi yalnız ters yön çıkarımları boşa çıkarmak değildir; aynı zamanda hangi aksiyom sıçramasının gerçekten yeni bilgi taşıdığını görünür kılmaktır.

- **İndiscrete uzay (birden fazla noktalı)**: en alt warning-line örneği; $T_0$ seviyesine bile çıkılamadığını gösterir.
- **Sierpiński uzayı**: tam karşı örnek değil, ama warning-line sınırında duran geçiş örneğidir; $T_0$ ile $T_1$ ayrımını görünür kılar.
- **Sonsuz kofinite topoloji**: bu bölümün ana warning-line karşı örneği; $T_1$ olup Hausdorff olmayan güvenilir test uzayıdır.
- **Düzenli ama normal olmayan uzaylar**: bu ciltte yalnız işaret seviyesinde tutulmalıdır; tam teknik yük daha ileri okumalara bırakılmalıdır.

### Bölüm 14 — warning-line ailesi

Bu bölümde karşı örnekler, kompaktlığın ne olmadığını ve hangi ek varsayımların ayrıca gerektiğini göstermek için kullanılmalıdır.

- **$(0,1)$**: açık örtü tanımına karşı ilk temel warning-line örneği; sınırlı olmanın tek başına kompaktlık vermediğini hatırlatır.
- **Kompakt ama Hausdorff olmayan indiscrete tipli uzaylar**: "kompakt ise Hausdorff" çıkarımının yanlış olduğunu gösterir.
- **Sayılabilir kompakt / ardışık kompakt ayrımları**: bu ciltte tam karakterizasyon hedeflenmez; yalnız warning-line notu olarak tutulmalıdır.

## Bölüm 06--09 için ayrıntılı karşı örnek notları

- **Bölüm 06**: sürekli bijektif olmanın tek başına özdeşbiçimlilik vermediğini göstermek için ayrık topolojiden kaba topolojiye özdeşlik haritası kullanılmalıdır.
- **Bölüm 07**: bir altuzayda kapalı olan bir kümenin ana uzayda kapalı olmak zorunda olmadığını göstermek için $(0,1/2] \subseteq \mathbb{R}$ türü örnekler kullanılmalıdır.
- **Bölüm 08**: kapalı bir kümenin yansıtımı her zaman kapalı olmak zorunda değildir; hiperbol örneği bu ayrımı görünür kılar.
- **Bölüm 09**: sürekli ve örten her fonksiyonun bölüm fonksiyonu olmadığı, ayrık topolojiden standart topolojiye özdeşlik ile açıkça görülür.

## Foundational counterexamples strengthened in v0.5.31

- **Family covering the carrier but not closed under finite intersections**: used in Chapter 03 to show that containing \(\varnothing\) and \(X\) is not enough for being a topology.
- **Large but uneconomical basis/subbasis descriptions**: used in Chapter 04 to contrast existence of a basis with pedagogically useful basis selection.
- **Sets with empty boundary in discrete spaces**: retained in Chapter 05 to show that boundary behavior depends strongly on the surrounding topology.

## v0.5.32 ara notu

06--09 hattındaki karşı örneklerin kullanılma biçimi daha açık hale getirilmelidir:

- **Bölüm 06**: sürekli bijektif olup özdeşbiçimlilik vermeyen özdeşlik örneği, ters yön sürekliliğin neden ayrıca gerekli olduğunu gösterir.
- **Bölüm 07**: altuzayda kapalı olup ana uzayda kapalı olmayan kümeler, göreli kapalılığın bağımsızlığını görünür kılar.
- **Bölüm 08**: hiperbol benzeri kapalı kümelerin yansıtım altında kapalı kalmaması, yansıtımın sürekli olmasının tek başına kapalılığı korumadığını gösterir.
- **Bölüm 09**: sürekli ve örten her fonksiyonun bölüm fonksiyonu olmaması, tanımın neden ters görüntü temelli kurulduğunu açıklar.

## v0.5.33 focus additions

- Chapter 10: metric diameter noted as a metric quantity rather than a topological invariant.
- Chapter 11: cofinite topology on an infinite set retained as the primary `T_1` but not Hausdorff counterexample.
- Chapter 12: Sorgenfrey line and separable/non-second-countable contrasts highlighted.
- Chapter 13: topologist's sine curve retained as the canonical connected-not-path-connected example.
- Chapter 14: $(0,1)$ and indiscrete compact non-Hausdorff examples highlighted for compactness distinctions.

## v0.5.37 notebook note

Bu sürümde seçilmiş karşı örnek aileleri için `notebooks/counterexamples/` altında gerçek not defteri karşılıkları eklendi. Özellikle `compact_not_hausdorff`, `first_countable_not_second_countable`, `separable_vs_second_countable` ve `t1_not_hausdorff_cocountable` başlıkları artık doğrudan not defteri düzeyinde de izlenebilir.


## Foundational contrast pairs (v0.8.102)

Aşağıdaki çiftler, Cilt I içinde specialized-contrast katmanını taşıyan temel eşleşmelerdir:

- **Bölüm 11 benchmark / warning**: ayrık uzay ve Sierpiński uzayı, ayırma aksiyomlarının olumlu basamaklarını göstermek için güvenli benchmark örneklerdir; buna karşılık sonsuz bir küme üzerindeki cofinite topoloji `T_1` olup Hausdorff olmayan temel warning örneğidir.
- **Bölüm 11 boundary note**: indiscrete uzay, ayırma zincirinin en alt sınırını göstermek için kullanılmalıdır; bu örnek olumlu model değil, aksiyomların neden ek varsayım gerektirdiğini hatırlatan uyarı örneğidir.
- **Bölüm 14 benchmark / warning**: `counterexamples` dosyasında öne çıkan `(0,1)` örneği, `[0,1]` ve sonlu uzaylar gibi güvenli kompakt benchmark örneklerinin karşısına yerleştirilmelidir. Bu eşleşme, kompaktlığın yalnız sezgiyle değil açık örtü davranışıyla okunması gerektiğini gösterir.
- **Bölüm 14 boundary note**: kompakt ama Hausdorff olmayan indiscrete tipli örnekler, `kompakt => Hausdorff` gibi yanlış kısa yolları durdurmak için kullanılmalıdır.

Bu katmanın amacı, temel ciltte her karşı örneği çoğaltmak değil, iki kritik hatta -- ayırma ve kompaktlık -- olumlu model ile warning örneğini birlikte okutabilir hale getirmektir.


## v1.0.54 classical warning-line cluster for Chapters 14--16

Aşağıdaki karşı örnekler, bu sürümde özellikle kompaktlık, metrik sezgi ve dizisel tamlık hattı için öne çıkarıldı.

### $(0,1)$
- warning: sınırlı olmak kompaktlık için yetmez
- kullanım: Chapter 14
- not: Heine--Borel konuşulurken ilk negatif örneklerden biri olmalıdır

### $[0,\infty)$
- warning: kapalı olmak kompaktlık için yetmez
- kullanım: Chapter 14
- not: “kapalı ve kompakt” ile “kapalı ve sınırlı” arasındaki bağlam farkını dürüst tutar

### $\mathbb{Q} \cap [0,1]$
- warning: metrik altuzay içinde kapalı/bounded davranışın dış uzay sezgisiyle karıştırılması kolaydır
- kullanım: Chapter 14, Chapter 16
- not: öğrenciyi Heine--Borel'ü otomatik biçimde altuzaylara taşımama konusunda uyarır

### $(\mathbb{Q}, |\cdot|)$ içindeki $\sqrt{2}$ yaklaşıkları
- warning: Cauchy olmak yakınsak olmakla aynı değildir
- kullanım: Chapter 16
- not: tamlık eksikliğinin en dürüst ilk örneklerinden biridir

### $(-1)^n$
- warning: bir dizinin range kümesinin accumulation point taşıması, dizinin o noktaya yakınsadığı anlamına gelmez
- kullanım: Chapter 16
- not: sequence limit ile set accumulation point ayrımını görünür kılar

## Kullanım kuralı

Bu karşı örnekler, olumlu benchmark örneklerin yerine geçmek için değil, onları dengelemek için kullanılmalıdır:

- $[0,1]$ ile $(0,1)$ birlikte,
- $\mathbb{R}$ ile $\mathbb{Q}$,
- açık top ile açık disk,
- yakınsak dizi ile yalnız accumulation point taşıyan dizi

aynı öğretim zincirinde yan yana görünmelidir.


## v1.0.58 Chapter 05 operator-warning note

Aşağıdaki iki uyarı, Chapter 05 için artık çekirdek warning-line olarak tutulmalıdır:

- **İçi boş olmak, nowhere dense olmak değildir**: `\(A=\mathbb{Q}\cap(0,1)\)` için `\(int(A)=\varnothing\)` ama `\(int(cl(A))=(0,1)\)` olur.
- **İç ve kapanış yer değiştirmez**: aynı örnek için `\(cl(int(A))=\varnothing\)` iken `\(int(cl(A))=(0,1)\)` elde edilir.

Bu iki karşı örnek, Chapter 05'in yalnız tanım ezberiyle geçilemeyeceğini; operatörlerin birlikte düşünülmesi gerektiğini gösterir.


## v1.0.60 — Chapter 03/05/16 warning-line additions

### Topolojilerin birleşimi uyarısı

$X=\{a,b,c\}$ üzerinde
\[	au_1=\{arnothing,\{a\},\{a,b\},X\},\qquad 	au_2=\{arnothing,\{c\},\{b,c\},X\}\]
ailelerinin her biri topolojidir; fakat birleşimleri sonlu kesişim altında kapalı değildir. Bu örnek, Chapter 03'te ``uygun görünen aileleri toplamak'' ile ``gerçekten topoloji vermek'' arasındaki farkı gösterir.

### \(int(cl(A))\) ile \(cl(int(A))\) yer değiştirmez

- ambient space: \(\mathbb{R}\)
- subset: \(A=\mathbb{Q}\cap(0,1)\)
- sonuç: \(cl(int(A))=arnothing\), ama \(int(cl(A))=(0,1)\)

### Range accumulation does not imply sequence convergence

- dizi: \(x_n=(-1)^n\)
- değer kümesi: \(\{-1,1\}\)
- warning: değer kümesi yığılma noktaları taşıyabilir; bu, dizinin onlardan birine yakınsadığı anlamına gelmez.



## v1.0.64 Chapter 04 warning additions

- **Açık yarı-doğrular ailesi**: her noktayı örter ama standart topoloji için doğrudan taban değildir; bu örnek ``örten aile'' ile ``taban'' arasındaki farkı erken aşamada sabitler.
- **Alt limit topolojisi / Sorgenfrey doğrusu**: Chapter 04'te artık yalnız ad olarak değil, yarı-açık aralık tabanı üzerinden gerçek bir doğrusal örnek olarak görülmelidir; Chapter 12'deki karşı örnek rolü bunun üzerine inşa edilir.
- **Pedagojik kullanım**: bu uyarı ailesi, öğrencinin ``aynı reel doğru üzerinde bütün makul açık kümeler aynı topolojiyi verir'' türü yanlış sezgisini kırmak için özellikle korunmalıdır.


## v1.0.70 Chapter 04 and 12 warning cluster

Bu sürümde karşı örnek bankası Chapter 04 için daha operasyonel hale getirildi. Amaç yalnız ``garip uzay'' sergilemek değil; özellikle taban ölçütünde hangi kısa yolların yanlış olduğunu görünür kılmaktır.

### Covering family is not automatically a basis

#### açık yarı-doğrular ailesi
- aile: `\(\{(-\infty,b): b\in\mathbb{R}\}\cup\{(a,\infty): a\in\mathbb{R}\}\)`
- warning: bu aile `\(\mathbb{R}\)`'yi örter, fakat standart topoloji için doğrudan taban değildir.
- neden: örneğin `x\in(-\infty,b)\cap(a,\infty)=(a,b)` iken, bu kesişimin içine oturan ve yine aileden gelen bir tek eleman genel olarak yoktur.
- pedagojik rol: ``örter'' ile ``tabandır'' ayrımı Chapter 04'te mutlaka sabitlenmelidir.

### Pairwise intersection can fail refinement

#### sonlu aile warning-line
- uzay: `\(X=\{a,b,c\}\)`
- aile: `\(\mathcal{F}=\{\{a,b\},\{b,c\},X\}\)`
- warning: aile tüm uzayı örter; fakat `b\in\{a,b\}\cap\{b,c\}=\{b\}` için `\mathcal{F}` içinde `b`'yi taşıyıp bu kesişimin içine oturan bir eleman yoktur.
- sonuç: örten aile olmak, hatta ``makul görünen'' bir kesişim yapısına sahip olmak bile yetmez.

### Same carrier, genuinely different topology

#### Sorgenfrey / lower-limit line
- aile: `\(\{[a,b): a<b\}\)`
- warning: bu aile yalnız standart açık aralıkların farklı yazımı değildir; gerçekten farklı bir topoloji üretir.
- Chapter 04 rolü: taban seçiminin topolojiyi gerçekten değiştirebileceğini erken aşamada göstermek.
- Chapter 12 rolü: birinci sayılabilir ama ikinci sayılabilir olmayan warning-line örneği.

### First countable does not force second countable

#### lower-limit line revisited
- local-base reading: her `x` için `\([x,x+1/n)\)` ailesi sayılabilir yerel taban verir.
- warning: buna rağmen tüm uzay için sayılabilir bir global taban yoktur.
- pedagojik rol: ``her noktada küçük veri'' ile ``tüm uzay için küçük veri'' arasındaki farkı Chapter 12'de açık tutmak gerekir.

## v1.0.114 Chapter 12 benchmark-warning sync note

Bu sürümde `04a_countability_axioms` assessment ailesi ile örnek bankası dili senkronize edildi. Chapter 12 için aşağıdaki üçlü artık birlikte düşünülmelidir:

- **benchmark model**: `\mathbb{R}` ve `\mathbb{R}^m`; ikinci sayılabilirlik, Lindelöf ve ayrılabilir metrik güvenli bölge aynı hatta görünür.
- **warning model 1**: Sorgenfrey doğrusu; birinci sayılabilir olup ikinci sayılabilir olmama ayrımını taşır.
- **warning model 2**: ayrılabilirlik genel olarak kalıtsal değildir; bu uyarı, metrik güvenli bölge ile keyfi topolojik uzaylar arasındaki sınırı görünür tutar.

### Chapter 12 için kısa routing

- `04a_countability_axioms.md` içindeki yerel/genel taban görevleriyle birlikte: **`\mathbb{R}`**, rasyonel uçlu aralık tabanı, alt limit doğrusu.
- `04a_countability_axioms.tex` quick-check hattıyla birlikte: **sayılabilir altörtü indirgeme**, **separable metric => second countable** şeması.
- counterexample notebook hattıyla birlikte: **Sorgenfrey warning-line**, **separability-not-hereditary caution**.

### Sequence-only reasoning warning

Chapter 12 assessment yüzeyinde artık şu cümle tek başına bırakılmamalıdır: “diziler yeterlidir.”
Doğru okuma şudur:

- **birinci sayılabilir / metrik güvenli bölgede** dizi testi güvenilir araçtır,
- **güvenli bölge dışında** sequence-only reasoning bir warning-line olarak işaretlenmelidir.


## Chapter 05 operator and convergence warning cluster (v1.0.173)

- **Not open does not mean closed**: Chapter 05 problem ailelerinde clopen ve neither-open-nor-closed örnekler birlikte görünmelidir.
- **Boundary is topological, not only geometric**: sonlu uzaylarda sınır çizimle değil, kapanış/iç ve tümleyen-kapanış kimlikleriyle hesaplanmalıdır.
- **Neighborhood need not be open**: bir komşuluk açık olmak zorunda değildir; noktayı içeren bir açık kümeyi kapsaması yeterlidir.
- **Sequence limits may be non-unique**: non-Hausdorff veya indiscrete tipteki uzaylarda dizi yakınsaklığı metrik sezgideki tekillik beklentisini bozabilir.
- **Sequences do not characterize closure in full generality**: dizi dili yararlıdır fakat genel topolojik uzaylarda kapanış/süreklilik için tek başına nihai test değildir.


## Chapter 06 basis/subbasis warning cluster (v1.0.174)

- **Covering is not enough**: bir aday aile taşıyıcıyı örtse bile kesişim tanığı koşulunu bozabilir.
- **Subbasis is not basis by default**: alt taban elemanlarının kendileri taban oluşturmak zorunda değildir; sonlu kesişim aşaması gerekir.
- **Same topology, different bases**: iki tabanın elemanları eşit olmayabilir; yine de aynı topolojiyi üretebilirler.
- **Relative basis is not subset filtering**: alt uzay tabanı yalnız `B⊂Y` elemanlarıyla değil, `B∩Y` kesişimleriyle kurulur.
- **Basis test for continuity has direction**: hedef uzayın taban elemanlarının ters görüntüleri kaynakta açık olmalıdır.


## v1.0.183 finite negative example stabilization

`FSE-007-FAILED-BASIS-WITNESS`, taşıyıcıyı örtme sezgisinin taban olmak için yeterli olmadığını gösteren kararlı negatif örnektir. Bu örnekte kesişim tanığı koşulu `analyze_basis` ile doğrudan yakalanmalıdır.


## v1.0.184 negative witness diagnostics

Bu sürümde negatif örnekler için kararlı witness kodları eklendi:

- `NEG-TOPOLOGY-MISSING-EMPTY`
- `NEG-TOPOLOGY-UNION-FAILURE`
- `NEG-BASIS-INTERSECTION-WITNESS`
- `NEG-MAP-MISSING-DOMAIN-POINT`
- `NEG-MAP-OUTSIDE-CODOMAIN`
- `NEG-CONTINUITY-PREIMAGE-FAILURE`

Bu kodlar `src/pytop/finite_witness_diagnostics.py` içinde çalıştırılabilir tanı raporlarına bağlanır.

## Chapter 03 union-of-topologies trap -- v0.1.34

A safe finite warning example is \(X=\{a,b,c\}\),
\[
	au_1=\{arnothing,\{a\},X\},\qquad
	au_2=\{arnothing,\{b\},X\}.
\]
Both are topologies, but their union is not a topology because it contains \(\{a\}\) and \(\{b\}\) without containing \(\{a,b\}\).

## Chapter 04 basis/subbasis traps -- v0.1.35

A cover is not automatically a basis. One must check the local refinement condition inside intersections of candidate basic open sets.

## Chapter 05 operator traps -- v0.1.36

Safe warning lines:

1. Empty interior is not nowhere dense.
2. Derived set is not closure.
3. Relative closure is ambient-sensitive.
4. Boundary is not a membership-only notion.

## v0.1.42 Chapter 11 atlas integration note

Bu dosya v0.1.42 ile Chapter 11 karşı örnek atlasının ikincil kaynağı olarak güncellenmiştir. Atlas girişleri CA-1 ... CA-6, bu dosyadaki mevcut Bölüm 11 warning-line ailesiyle tam örtüşmektedir. Özellikle:

- İndiscrete uzay → CA-1 (T0 bile değil)
- Kofinite topoloji → CA-3 (T1 fakat Hausdorff değil)
- Sierpiński → CA-2 (T0 fakat T1 değil)
- Sonlu T1 → CA-5 (sonlu bağlamda T1 ayrıklığı zorunlu kılar)


## v0.1.49 Temel Karşı Örnek Atlası (CE-S ve CE-P Serileri)

Bu dosya v0.1.49 ile temel karşı örnek atlasının ikincil kaynağı olarak güncellenmiştir.
v0.1.42'deki CA-1...CA-6 atlası, burada CE-S-01...CE-S-06 olarak kararlı kimlikler almıştır.
Yeni CE-P serisi (CE-P-01...CE-P-10) koruma tablosundaki her "H" hücresini somutlaştırır.

### Ayrılma aksiyomları (CE-S serisi)

| Kimlik  | Uzay                              | Başarısız özellik | counterexample_class        |
|---------|-----------------------------------|-------------------|-----------------------------|
| CE-S-01 | Belirsiz topoloji {a,b}           | T0                | not_t0                      |
| CE-S-02 | Sierpiński uzayı                  | T1                | t0_not_t1                   |
| CE-S-03 | Kofinite topoloji (sonsuz küme)   | Hausdorff         | t1_not_hausdorff             |
| CE-S-04 | Ko-sayılabilir topoloji           | Hausdorff         | t1_not_hausdorff             |
| CE-S-05 | Sonlu T1 uzay                     | Ayrık-olmama      | finite_t1_forces_discrete   |
| CE-S-06 | Metrik uzay (pozitif referans)    | —                 | metric_hausdorff_anchor     |

### Koruma hataları (CE-P serisi)

| Kimlik  | Özellik               | İnşaat           | counterexample_class                     |
|---------|-----------------------|------------------|------------------------------------------|
| CE-P-01 | Bağlılık              | Altuzay          | connectedness_not_subspace               |
| CE-P-02 | Kompaktlık            | Altuzay          | compactness_not_subspace                 |
| CE-P-03 | Hausdorff             | Bölüm            | hausdorff_not_quotient                   |
| CE-P-04 | Hausdorff             | Sürekli görüntü  | hausdorff_not_continuous_image           |
| CE-P-05 | T1                    | Bölüm            | t1_not_quotient                          |
| CE-P-06 | T1                    | Sürekli görüntü  | t1_not_continuous_image                  |
| CE-P-07 | İkinci sayılabilirlik | Bölüm            | second_countability_not_quotient         |
| CE-P-08 | İkinci sayılabilirlik | Sürekli görüntü  | second_countability_not_continuous_image |
| CE-P-09 | İkinci sayılabilirlik | Sayılamaz çarpım | second_countability_uncountable_product  |
| CE-P-10 | Yol-bağlılık          | Altuzay          | connected_not_path_connected             |

### pytop API token check

<!-- counterexample_lookup counterexample_atlas_by_layer counterexample_atlas_by_property counterexample_atlas_by_construction analyze_counterexample_atlas ATLAS_IDS CE-S-01 CE-P-01 -->
