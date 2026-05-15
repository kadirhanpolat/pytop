# Cardinal number examples

Bu dosya, Cilt II Bölüm 26 için temel örnek ailesini daha görünür ve daha öğretilebilir biçimde toplar.
Amaç, yalnız bir kaç slogan cümlesi vermek değil; eşgüçlülük, sayılabilirlik, sayılamazlık ve kardinal karşılaştırma dilinin hangi klasik örneklerle taşındığını açık seçik göstermektir.

## Bölüm 26 için çekirdek örnek aileleri

### 1. \(\mathbb{N}\) ile gerçek altkümeleri

#### \(\mathbb{N}\sim 2\mathbb{N}\)
**Örnek:**
\[
 f\colon \mathbb{N}\to 2\mathbb{N},\qquad f(n)=2n.
\]

**Gösterilen ana fikir:** sonsuz bir küme, gerçek bir altkümesiyle eşgüçlü olabilir.

**Pedagojik kullanım:** Bu örnek, ``gerçek altküme mutlaka daha küçüktür'' sezgisinin sonsuz kümelerde neden güvenilir olmadığını açar. Bölüm 26'nın giriş örneği olarak doğal merkezdir.

#### \(\mathbb{N}\sim 2\mathbb{N}+1\)
**Örnek:**
\[
 g\colon \mathbb{N}\to \{1,3,5,\dots\},\qquad g(n)=2n+1.
\]

**Gösterilen ana fikir:** yalnız çiftler değil, tekler gibi başka aritmetik alt aileler de tüm \(\mathbb{N}\) ile aynı kardinal büyüklükte olabilir.

**Pedagojik kullanım:** Öğrenciye ``aynı tip numaralandırma'' ile farklı alt ailelerde yeni bijeksiyonlar kurdurmak için iyi bir ilk alıştırma yüzeyidir.

### 2. \(\mathbb{N}\), \(\mathbb{Z}\) ve \(\mathbb{Q}\) hattı

#### \(\mathbb{N}\sim \mathbb{Z}\)
**Örnek numaralandırma:**
\[
0,1,-1,2,-2,3,-3,\dots
\]

**Gösterilen ana fikir:** iki-yönlü sonsuza gitmek, kardinal büyüklüğü otomatik olarak büyütmez.

**Pedagojik kullanım:** ``daha yaygın görünmek'' ile ``daha büyük olmak'' arasındaki farkı görünür kılar. Sonraki ordinal bölümünde sıra tipi ile kardinal büyüklük farkını hazırlamak için de kullanışlıdır.

#### \(\mathbb{N}\times\mathbb{N}\) sayılabilirdir
**Örnek strateji:** köşegen tarama.

**Gösterilen ana fikir:** tablo biçimli sonsuz veri tek bir dizi halinde toplanabilir.

**Pedagojik kullanım:** Sayılabilir çoklukta sayılabilir kümenin birleşiminin neden sayılabilir kaldığını sezgisel olarak destekleyen ana laboratuvardır.

#### \(\mathbb{Q}\) sayılabilirdir
**Örnek strateji:**
- önce \(\mathbb{Q}_{>0}\) sade kesirlerle \(\mathbb{N}\times\mathbb{N}\) içine gömülür,
- sonra \(0\) ve negatifler eklenir.

**Gösterilen ana fikir:** cebirsel ve aritmetik olarak zengin görünen bir küme yine de sayılabilir olabilir.

**Pedagojik kullanım:** Topolojik yoğunluk ile kardinal büyüklüğün aynı şey olmadığını anlatmak için temel örnektir.

### 3. Yoğunluk ile kardinal büyüklüğün ayrımı

#### \(\mathbb{Q}\subseteq \mathbb{R}\) yoğundur ama \(|\mathbb{Q}|<|\mathbb{R}|\)
**Mesaj:** Yoğun olmak, kardinal olarak büyük olmak anlamına gelmez.

**Topoloji köprüsü:** Bu örnek, daha sonra ``ayrılabilirlik'' ile ``ağırlık'' veya ``yoğunluk'' gibi niceliklerin aynı düzleme ait ama özdeş olmayan veriler olduğunu anlatırken tekrar kullanılır.

#### ``Her aralıkta rasyonel var'' ile ``tüm reel doğruyu numaralayabilmek'' farklıdır
**Mesaj:** yerel yaygınlık ile global büyüklük farklı kavramlardır.

**Pedagojik kullanım:** Öğrencinin sayılabilir/sayılamaz ayrımını yalnız listeleme diliyle değil, topolojik sezgiye karşı dikkat uyarısı olarak da okumasını sağlar.

### 4. \(\mathbb{R}\) ve continuum hattı

#### \((0,1)\) sayılamazdır
**Örnek strateji:** Cantor köşegen argümanı.

**Gösterilen ana fikir:** sayılabilir bir liste verildiğinde, listede olmayan yeni bir reel sayı sistematik biçimde üretilebilir.

**Pedagojik kullanım:** Bu, Bölüm 26'nın yalnız ``büyük küme var'' demesine değil, ``neden hiçbir listeleme yeterli olmaz'' sorusuna da cevap verir.

#### Her dejenere olmayan açık aralık \(\mathbb{R}\) ile eşgüçlüdür
**Örnek stratejiler:**
- iki açık aralık arasında afin dönüşüm,
- \((0,1)\to\mathbb{R}\) için tanjant türü bir bijeksiyon.

**Gösterilen ana fikir:** geometrik olarak kısa görünen bir açık aralık, kardinal büyüklük bakımından tüm reel doğru kadar büyüktür.

**Topoloji köprüsü:** Yerel pencere ile global evren arasındaki bu ``kardinal küçülmeme'' olgusu, topolojik yerellik ile kardinal büyüklüğün farklı ölçekler olduğunu anlatmak için önemlidir.

#### Sonlu kapalı veya yarı açık aralıklar da continuum büyüklüğündedir
**Mesaj:** aralık uçlarının açık/kapalı olması, bu bağlamda kardinal katmanı değiştirmez.

**Pedagojik kullanım:** Açık aralık sonucu oturduktan sonra, öğrenciye küçük varyasyonların neden kardinali değiştirmediğini sorgulatmak için iyi bir takip alıştırmasıdır.

### 5. Cebirsel ve transandant sayı örnekleri

#### Cebirsel sayılar sayılabilirdir
**Örnek strateji:**
- tam sayı katsayılı polinomlar sayılabilir çokluktadır,
- her polinomun sonlu sayıda kökü vardır,
- sayılabilir çoklukta sonlu kümelerin birleşimi sayılabilirdir.

**Gösterilen ana fikir:** cebirsel tanımlanabilirlik, büyük kardinal büyüklük zorunlu kılmaz.

**Pedagojik kullanım:** Sayılabilir birleşim teoreminin doğal ve etkileyici bir uygulamasıdır.

#### Transandant sayılar sayılamazdır
**Mesaj:**
\[
\mathbb{R}=\text{cebirsel sayılar} \cup \text{transandant sayılar}
\]
ve ilk parça sayılabilir, tüm \(\mathbb{R}\) ise sayılamaz olduğundan ikinci parça sayılamaz olmalıdır.

**Gösterilen ana fikir:** ``çok az istisna'' ile ``çok büyük geri kalan'' ayrımı kardinal dilde ciddi sonuç verir.

**Pedagojik kullanım:** Öğrenciye sayılamazlığın yalnız \(\mathbb{R}\) için değil, reel sayıların önemli alt aileleri için de güçlü bir olgu olduğunu gösterir.

### 6. Karşılaştırma ve iki yönlü gömü örnekleri

#### \((0,1)\preccurlyeq \mathbb{R}\) ve \(\mathbb{R}\preccurlyeq (0,1)\)
**Örnek:**
- doğal içleme ile \((0,1)\subseteq\mathbb{R}\),
- uygun bir açık fonksiyonla \(\mathbb{R}\to(0,1)\).

**Gösterilen ana fikir:** iki yönde birebir gömü kurulduğunda, Schröder--Bernstein kardinal eşitliği güvenle verir.

**Pedagojik kullanım:** Bölüm 26'da karşılaştırma dilinin neden doğrudan bijeksiyon aramaktan daha esnek olduğunu anlatır.

#### \([0,1]\sim (0,1)\)
**Mesaj:** aralığa birkaç uç nokta eklemek ya da çıkarmak, continuum büyüklüğünü değiştirmez.

**Pedagojik kullanım:** ``az sayıda nokta'' ekleyip çıkarmanın sayılabilir/continuum eşiği üzerindeki etkisini tartıştırmak için iyi bir örnektir.

### 7. Kuvvet kümesi örnekleri

#### \(A\hookrightarrow \mathcal P(A)\)
**Örnek:**
\[
 a\longmapsto \{a\}.
\]

**Gösterilen ana fikir:** her küme, kuvvet kümesine tekil noktalar üzerinden gömülür.

**Pedagojik kullanım:** Cantor'un kuvvet kümesi teoreminin ``\(\le\)'' kısmını görünür kılar.

#### \(A\not\sim \mathcal P(A)\)
**Örnek strateji:** çapraz küme
\[
 D=\{a\in A:a\notin f(a)\}.
\]

**Gösterilen ana fikir:** hiçbir küme kendi kuvvet kümesini örtemez; yani kuvvet kümesi işlemi gerçekten yeni bir kardinal katman üretir.

**Topoloji köprüsü:** Nicel topolojide ``bir veri ailesinin tüm alt aileleri'' ile ``ailenin kendisi'' arasındaki büyüklük farkını düşünürken bu yapı arka planda durur.

#### Sonlu kümelerde bile ilk model görülebilir
**Örnek:** \(|\{1,2,3\}|=3\), ama \(|\mathcal P(\{1,2,3\})|=8\).

**Pedagojik kullanım:** Sonsuz teoremin sonlu laboratuvarda önsezgi üretmesini sağlar.

## Chapter 26 için öğretimsel kullanım önerileri

### Hızlı açılış sırası
1. \(\mathbb{N}\sim 2\mathbb{N}\)
2. \(\mathbb{N}\sim \mathbb{Z}\)
3. \(\mathbb{Q}\) sayılabilir, \(\mathbb{R}\) sayılamaz
4. her açık aralık continuum büyüklüğündedir
5. \(|A|<|\mathcal P(A)|\)

Bu sıra, şaşırtıcı ama yönetilebilir bir öğretim ritmi verir.

### Orta seviye alıştırma kümeleri
- açık bir bijeksiyon yazma,
- bir kümenin sayılabilirliğini gömü ile gösterme,
- sayılabilir birleşim ilkesini uygulama,
- yoğunluk ile kardinal büyüklüğü karıştıran yanlış sezgiyi düzeltme,
- kuvvet kümesi teoremindeki çapraz kümenin işlevini açıklama.

### İleri seviye köprü örnekleri
- cebirsel sayıların sayılabilirliği,
- transandant sayıların sayılamazlığı,
- \([0,1]\sim \mathbb{R}\) ya da \((0,1)\sim \mathbb{R}\) için iki farklı yol,
- Schröder--Bernstein uygulamaları.

## Bölüm 26 için kullanım notu

Bu örnekler salt kümeler kuramsal hazırlık olarak kalmamalıdır. Özellikle Bölüm 30 ve 31'de geçen
- sayılabilir taban,
- sayılabilir yoğun altküme,
- sayılabilir yerel taban,
- sayılabilir alt örtü
ifadelerinin hepsi burada hazırlanan kardinal dilin uygulamalarıdır.

Ayrıca Bölüm 27 ve 28'e geçerken şu ayrım görünür tutulmalıdır:
- kardinal sayı, ``kaç tane'' sorusunu taşır,
- ordinal sayı ise ``hangi sıra tipiyle'' sorusunu taşır.

Bu yüzden \(\mathbb{N}\), \(\mathbb{Z}\), \(\mathbb{Q}\), \(\mathbb{R}\) ve aralık örnekleri yalnız büyüklük dili için değil, sonraki bölümde gelecek sıra tipi ayrımının sınırlarını da işaretler.

## Notebook görev eşleşmesi

Bu dosya artık `notebooks/exploration/15_cardinal_numbers.ipynb` ile daha güçlü biçimde eşleştirilmiştir. Özellikle şu görev aileleri doğrudan notebook'a çevrilebilir:

- `\mathbb{N} \leftrightarrow 2\mathbb{N}` ve `\mathbb{N} \leftrightarrow \mathbb{Z}` için açık numaralandırma görevleri,
- `\mathbb{N}\times\mathbb{N}` köşegen taramasının tablo üzerinden izlenmesi,
- `\mathbb{Q}` sayılabilir / `\mathbb{R}` sayılamaz ayrımının karşılaştırmalı okunması,
- kısa açık aralık ile tüm reel doğru arasında bijeksiyon kurma,
- tekil nokta gömüsü ve çapraz küme üzerinden `|A|<|\mathcal P(A)|` düşüncesi,
- cebirsel / transandant sayı ayrımını sayılabilir birleşim mantığıyla okuma.

## v1.0.43 integration note

Bu sürümde dosya, kısa başlık notu olmaktan çıkarılıp gerçek bir Chapter 26 örnek koridoruna çevrildi. Böylece manuskriptte kurulan sayılabilirlik, interval-cardinality, Schröder--Bernstein ve kuvvet-kümesi omurgası artık örnek bankasında da görünür bir karşılık bulmuş oldu.

---

## v0.1.65 — pytop API örnek ailesi (CN-01 … CN-06)

Bu bölüm, `cardinal_numbers.py` modülünün durable public API'sini gösteren çekirdek örnek kimliklerini tanımlar.

### CN-01 — Sonlu uzay: kesin kardinalite

**Uzay:** `make_finite(4)` — 4 noktalı ayrık topoloji  
**Beklenti:** `cardinality_class` → `"finite"`, `analyze_cardinal_numbers` modu `"exact"`, etiket `"4"`.  
**Pedagojik kullanım:** Sonlu uzaylarda kardinalite bir doğal sayıdır; cardinal fonksiyonlar (ağırlık, yoğunluk) da bu doğal sayıya göre hesaplanır.

### CN-02 — Sayılabilir sonsuz: omega katmanı

**Uzay:** `_Tagged(tags=["omega"])` — ayrık sayılabilir uzay (ℕ modeli)  
**Beklenti:** `cardinality_class` → `"countably_infinite"`, label `"aleph_0"`, mod `"theorem"`.  
**Pedagojik kullanım:** Sayılabilir eşik; ikinci sayılabilirlik, ayrılabilirlik ve Lindelöf özelliklerinin temel kardinal referans noktası.

### CN-03 — Kontinuum: gerçek doğru

**Uzay:** `_Tagged(tags=["real_line"])` — standart topolojili ℝ  
**Beklenti:** `cardinality_class` → `"continuum"`, label içinde `c = 2^{aleph_0}`.  
**Pedagojik kullanım:** `w(ℝ) = aleph_0` iken `|ℝ| = c` olduğunu göstererek kardinal fonksiyon ile küme büyüklüğünün farklı ölçütler olduğunu vurgular.

### CN-04 — Sayılamaz: belirsiz üst katman

**Uzay:** `_Tagged(tags=["uncountable"])` — genel sayılamaz uzay  
**Beklenti:** `cardinality_class` → `"uncountable"`, mod `"theorem"`, label `"> aleph_0 (precise tier unknown)"`.  
**Pedagojik kullanım:** Sayılamazlık tek bir kadinal katman değildir; Cantor teoremi sayesinde üst sınır yoktur.

### CN-05 — Bilinmeyen katman: yetersiz etiket

**Uzay:** `_Tagged()` — etiket yok  
**Beklenti:** `cardinality_class` → `"unknown"`, mod `"symbolic"`.  
**Pedagojik kullanım:** API'nin eksik bilgi durumunda sessizce başarısız olmak yerine güvenli `"unknown"` döndürdüğünü gösterir.

### CN-06 — Kuvvet kümesi köprüsü

**Beklenti:** Profil `power_set_tier` anahtarı;  
- finite X için `"2^n"` formatı,  
- countable için `"2^{aleph_0} = c"`,  
- continuum için `"2^c, strictly larger than c"`.  
**Pedagojik kullanım:** Cantor'un kuvvet kümesi teoreminin `analyze_cardinal_numbers` çıktısında doğrudan görülebileceğini gösterir.
