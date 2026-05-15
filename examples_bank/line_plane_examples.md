# Line and plane examples

Bu dosya, Cilt I'in özellikle 05, 14, 15 ve 16. bölümlerinde tekrar tekrar kullanılan reel doğru ve reel düzlem örneklerini tek yerde toplar.

Amaç, bu örnekleri yalnız “bilinen klasik uzaylar” diye anmak değil; hangi kavramı hangi örnekle öğretmenin daha temiz olduğunu görünür kılmaktır.

## 1. Reel doğru üzerindeki temel benchmark kümeler

### $(a,b)$ — açık aralık
- rol: standart açık küme sezgisi
- en doğal kullanım: Bölüm 03, 04, 15
- pedagojik mesaj: bir noktanın çevresinde tamamen içeride kalan küçük bir parça bulunması fikri

### $[a,b]$ — kapalı ve sınırlı aralık
- rol: kompaktlık benchmark örneği
- en doğal kullanım: Bölüm 14
- pedagojik mesaj: açık örtü dilinin gerçekten güçlü ve sonlu kontrol veren biçimi

### $(0,1)$ — warning-line örneği
- rol: sınırlı olmanın tek başına kompaktlık vermediğini göstermek
- en doğal kullanım: Bölüm 14
- pedagojik mesaj: “küçük görünmek” ile “kompakt olmak” aynı şey değildir

### $[0,\infty)$ — ikinci warning-line örneği
- rol: kapalı olmanın tek başına kompaktlık vermediğini göstermek
- en doğal kullanım: Bölüm 14
- pedagojik mesaj: kapalılık tek başına yeterli değildir; sınırlılık da gereklidir ve bu da yalnız Öklidyen bağlamda güvenli okunmalıdır

### $\mathbb{N} \subseteq \mathbb{R}$
- rol: yığılma noktası olmayan sonsuz küme örneği
- en doğal kullanım: Bölüm 05, 16
- pedagojik mesaj: sonsuzluk tek başına accumulation point garantisi vermez

### $\mathbb{Q} \subseteq \mathbb{R}$
- rol: yoğun ama içi boş klasik örnek
- en doğal kullanım: Bölüm 05, 12, 16
- pedagojik mesaj: yoğunluk ile açıklık/iç nokta fikri farklı şeylerdir

### $\mathbb{R} \setminus \mathbb{Q}$
- rol: irrasyonellerin de her açık aralıkta görünmesi
- en doğal kullanım: Bölüm 05, 12
- pedagojik mesaj: hem rasyoneller hem irrasyoneller reel doğrunun yerel yapısında her yerde bulunur

## 2. Yığılma noktası ve kapanış için seçilmiş çizgi örnekleri

### $A=\{1,1/2,1/3,\ldots\}$
- derived set: $A'=\{0\}$
- kullanım: Bölüm 05 ve Bölüm 16 arasında köprü
- mesaj: accumulation point kümenin içinde olmak zorunda değildir

### $\mathbb{N}$
- derived set: boş
- kullanım: Bölüm 05
- mesaj: sonsuz küme olup hiç yığılma noktası taşımayabilir

### $\mathbb{Q}$
- closure in $\mathbb{R}$: $\mathbb{R}$
- interior in $\mathbb{R}$: $\varnothing$
- boundary in $\mathbb{R}$: $\mathbb{R}$
- kullanım: Bölüm 05
- mesaj: yoğunluk, iç nokta büyüklüğü anlamına gelmez

## 3. Reel düzlem için temel benchmark kümeler

### $B((a,b),r)$ — açık disk
- rol: $\mathbb{R}^2$ içindeki temel açık küme modeli
- en doğal kullanım: Bölüm 15
- pedagojik mesaj: açık aralığın iki boyutlu analoğu açık disktir; “çevrede kalma” fikri burada yuvarlak komşulukla görünür olur

### $\mathbb{R}^2$ içindeki açık dikdörtgenler
- rol: çarpım topolojisi ile metrik topoloji arasındaki sezgisel köprü
- en doğal kullanım: Bölüm 08, 15
- pedagojik mesaj: açık disk ile açık dikdörtgen aynı yerel topolojik dili farklı biçimde taşır

### kapalı disk $\overline{B}((a,b),r)$
- rol: açık disk ile sınır ayrımını görünür kılmak
- en doğal kullanım: Bölüm 05, 15
- pedagojik mesaj: sınır noktaları topolojik konuşmayı metrik sezgiye bağlar

### delinmiş disk $B((a,b),r)\setminus\{(a,b)\}$
- rol: komşuluk ile merkez nokta ayrımını vurgulamak
- en doğal kullanım: Bölüm 05, 15
- pedagojik mesaj: bir noktanın silinmesi yerel konuşmayı her zaman bütünüyle bozmaz; ama closure/boundary davranışı değişir

## 4. Sayılabilir taban sezgisi için seçilmiş aile

### rasyonel merkezli, rasyonel yarıçaplı açık diskler
- rol: $\mathbb{R}^2$ için sayılabilir taban fikri
- en doğal kullanım: Bölüm 12, 15
- pedagojik mesaj: düzlemde tüm yerel bilgiyi sayılabilir bir aileyle yakalayabilmek, ikinci sayılabilirliğin yalnız soyut bir özellik olmadığını gösterir

## 5. Dizi ve alt dizi köprüsü için örnekler

### $x_n = 1/n$
- yakınsaklık: $x_n \to 0$
- kullanım: Bölüm 16
- mesaj: bir limitin aynı zamanda range kümesi için accumulation point olabileceğini güvenli biçimde gösterir

### $x_n = (-1)^n$
- yakınsaklık: yok
- ama iki sabit alt dizi vardır
- kullanım: Bölüm 16
- mesaj: bir dizi yakınsamasa bile yakınsak alt diziler taşıyabilir

### $x_n$ rasyonel yaklaşıklar ile $\sqrt 2$
- $\mathbb{Q}$ içinde Cauchy, fakat $\mathbb{Q}$ içinde yakınsak değil
- kullanım: Bölüm 16
- mesaj: tamlık, yalnız Cauchy olma ile bitmeyen ayrı bir yapıdır

## 6. Öğretim kullanım önerisi

### Bölüm 05
Önce reel doğru üzerindeki $A=\{1,1/2,1/3,\ldots\}$ ve $\mathbb{Q}$ örnekleriyle accumulation point / closure / boundary dili kurulmalıdır.

### Bölüm 14
Kompaktlık anlatımında ilk olumlu benchmark doğrudan $[0,1]$ veya genel $[a,b]$ olmalıdır. Hemen ardından $(0,1)$ ve $[0,\infty)$ warning-line çifti verilmelidir.

### Bölüm 15
Açık aralık, açık top ve açık disk aynı paragraf ailesinde birlikte okutulmalıdır. $\mathbb{R}^2$ yalnız kısa bir örnek diye geçmemelidir.

### Bölüm 16
Dizi yakınsaklığı, alt dizi, accumulation point ve Cauchy/tamlık hattı reel doğru ve $\mathbb{Q}$ örnekleriyle birlikte işlenmelidir.

## 7. Kırmızı çizgi

Bu dosyadaki örnekler, genel topoloji sonuçlarını yanlış biçimde “yalnız Öklidyen sezgi”ye indirmek için kullanılmamalıdır. Özellikle

- “kapalı ve sınırlı ise kompakt” ifadesi genel uzay cümlesi değildir,
- dizisel karakterizasyonlar her uzayda tam güçte geçerli değildir,
- düzlem sezgisi yararlı olsa da soyut tanımların yerini almamalıdır.


## 8. Chapter 05 operational table strengthening (v1.0.58)

### Dört interval modeli
Aşağıdaki dört küme, Chapter 05 için birlikte okutulmalıdır:

- `\([a,b]\)`
- `\((a,b)\)`
- `\((a,b]\)`
- `\([a,b)\)`

Bu dörtlüde ortak davranış şudur:

- hepsinin içi `\((a,b)\)` olur,
- hepsinin kapanışı `\([a,b]\)` olur,
- hepsinin sınırı `\(\{a,b\}\)` olur.

Pedagojik mesaj: açıklık/kapalılık statüsü değişse bile closure-boundary iskeleti aynı kalabilir.

### Dense versus nowhere dense contrast
Chapter 05 için aşağıdaki iki örnek yan yana tutulmalıdır:

- `\(\mathbb{Q}\cap(0,1)\)`: içi boş ama nowhere dense olmayan örnek
- `\(\{1/n:n\in\mathbb{N}\}\)`: nowhere dense örnek

Pedagojik mesaj: `int(A)=\varnothing` ile `int(cl(A))=\varnothing` tamamen farklı iki koşuldur.


## v1.0.60 — Chapter 05 and Chapter 16 corridor examples

### Interval operator table

Standart topoloji altında aşağıdaki örnekler birlikte okutulmalıdır:

| Küme | İç | Kapanış | Sınır | Dış |
|---|---|---|---|---|
| \((a,b)\) | \((a,b)\) | \([a,b]\) | \(\{a,b\}\) | \(( -\infty,a]\cup[b,\infty)\) |
| \([a,b]\) | \((a,b)\) | \([a,b]\) | \(\{a,b\}\) | \(( -\infty,a)\cup(b,\infty)\) |
| \((a,b]\) | \((a,b)\) | \([a,b]\) | \(\{a,b\}\) | \(( -\infty,a]\cup(b,\infty)\) |
| \([a,b)\) | \((a,b)\) | \([a,b]\) | \(\{a,b\}\) | \(( -\infty,a)\cup[b,\infty)\) |

### Rational / irrational operator pair

- **\(\mathbb{Q}\)**: içi boştur, kapanışı \(\mathbb{R}\)'dir, sınırı \(\mathbb{R}\)'dir.
- **\(\mathbb{R}\setminus\mathbb{Q}\)**: aynı biçimde içi boştur (relative değil, ambient \(\mathbb{R}\) içinde düşünüldüğünde), kapanışı \(\mathbb{R}\)'dir, sınırı \(\mathbb{R}\)'dir.
- Bu çift, Chapter 05 için yoğunluk ile iç büyüklüğünün ayrıldığını gösteren ana benchmark hattıdır.

### The set \(\{1/n:n\in\mathbb{N}\}\)

- kapanış: \(\{1/n:n\in\mathbb{N}\}\cup\{0\}\)
- iç: \(arnothing\)
- tek yığılma noktası: \(0\)
- pedagojik rol: Chapter 05'te derived set, Chapter 16'da dizi limiti ile küme yığılma noktası arasındaki bağı görünür kılar.



## 5. Yarı-açık aralık tabanları ve doğrusal varyantlar (v1.0.64)

### 5.1. Alt limit topolojisi için temel aile

- uzay: $\mathbb{R}$
- taban: $\{[a,b): a<b\}$
- rol: Chapter 04'te taban ölçütünü standart açık aralıkların ötesinde test etmek
- ana mesaj: yarı-açık aralıklar da tutarlı bir topoloji üretebilir; ``temel açık küme'' fikri yalnız $(a,b)$ biçimiyle sınırlı değildir.

### 5.2. Üst limit topolojisi için simetrik aile

- uzay: $\mathbb{R}$
- taban: $\{(a,b]: a<b\}$
- rol: alt limit topolojisine simetrik ikinci doğrusal örnek
- ana mesaj: aynı taşıyıcı kümede taban seçimi değiştiğinde topoloji gerçekten değişebilir.

### 5.3. Düzen topolojisi okuması

- uzay: doğal sıralı $\mathbb{R}$ veya sonlu zincirler
- alt taban: $(-\infty,b)$ ve $(a,\infty)$ aileleri
- rol: standart topolojinin yalnız metrik değil, düzen teorik okunuşunu da görünür kılmak
- ana mesaj: açık aralıklar çoğu zaman daha küçük bir doğrusal alt tabanın sonlu kesişimlerinden doğar.


## 9. v1.0.70 Chapter 04 basis families on the line and the plane

Bu sürümde `line_plane_examples` dosyası yalnız Chapter 05/14/15/16 koridoruna hizmet eden bir depo olmaktan çıkarılıp, Chapter 04 için de gerçek bir taban laboratuvarı haline getirildi.

### 9.1. Reel doğru için aynı topolojiyi veren iki taban

#### tüm açık aralıklar
- aile: `\(\{(a,b): a<b\}\)`
- rol: standart topolojinin en doğrudan tabanı
- mesaj: ``temel açık küme'' fikrinin ilk güvenli modeli

#### rasyonel uçlu açık aralıklar
- aile: `\(\{(p,q): p,q\in\mathbb{Q},\ p<q\}\)`
- rol: standart topoloji için sayılabilir taban benchmark'ı
- mesaj: aynı topolojiyi veren daha küçük bir üretici aile seçilebilir.

### 9.2. Reel doğru için alt taban okuması

#### açık yarı-doğrular
- aile: `\(\{(-\infty,b): b\in\mathbb{R}\}\cup\{(a,\infty): a\in\mathbb{R}\}\)`
- rol: düzen topolojisinin doğal alt tabanı
- mesaj: bu aile tek başına taban gibi değil, **sonlu kesişimlerden sonra** tabana dönüşen üretici ailedir.

### 9.3. Düzlem için iki eşdeğer yerel model

#### açık diskler
- aile: `\(\{B((a,b),r): r>0\}\)`
- rol: metrik komşuluk dili
- mesaj: nokta çevresinde ``yarıçap küçültme'' yöntemi ile yerel taban kurulur.

#### açık dikdörtgenler
- aile: `\(\{(a,b)\times(c,d)\}\)`
- rol: çarpım topolojisi komşuluk dili
- mesaj: açık disk ile açık dikdörtgen farklı görünümler olsa da aynı düzlem topolojisini taşır.

### 9.4. Sayılabilirlik için düzlem benchmark'ı

#### rasyonel köşeli açık dikdörtgenler
- aile: `\(\{(p,q)\times(r,s): p,q,r,s\in\mathbb{Q},\ p<q,\ r<s\}\)`
- rol: `\(\mathbb{R}^2\)` için sayılabilir taban
- mesaj: Chapter 12'deki ikinci sayılabilirlik hattı, Chapter 04'teki bu somut aileye geri bağlanmalıdır.

#### rasyonel merkezli / rasyonel yarıçaplı açık diskler
- rol: aynı fikrin metrik versiyonu
- mesaj: dikdörtgen ve disk aileleri, ``aynı uzay — farklı kullanışlı tabanlar'' ilkesini birlikte taşır.

### 9.5. Strip families as subbasis hints

#### düşey ve yatay açık şeritler
- aileler:
  - `\((a,b)\times\mathbb{R}\)`
  - `\(\mathbb{R}\times(c,d)\)`
- rol: düzlemde çarpım topolojisinin alt taban sezgisi
- mesaj: açık dikdörtgenler bu iki tip şeridin sonlu kesişimlerinden doğar; bu yüzden Chapter 08 ve Chapter 15 köprüsü için özellikle değerlidir.


## v1.0.172 Chapter 04 real-line / metric-topology integration pointers

This release connects the line-and-plane example bank to the new Chapter 04
question-bank families.  The examples here remain benchmark reminders; the
actual testable family contracts live in
`src/pytop_questionbank/chapter_04_real_line_metric_families.py`.

Recommended fresh-generation directions:

- interval-like sets with explicit open/closed predicate witnesses;
- hybrid finite-plus-tail subsets for closure and derived-set questions;
- deleted-limit-point subspaces for Cauchy/completeness boundary tasks;
- claim cards that mark when Heine-Borel style reasoning is Euclidean-specific;
- plane regions where openness depends on an actual ball-radius witness.
