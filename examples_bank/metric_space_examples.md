# Metrik uzay örnekleri

Bu dosya, Cilt I'in özellikle 15--16. bölümleri için seçilmiş temel metrik uzay örneklerini toplar.

## 1. Reel doğru

- Küme: `\mathbb{R}`
- Metrik: `d(x,y)=|x-y|`
- Rol: standart açık top sezgisi, birinci sayılabilirlik, Hausdorffluk
- Kitap bağlantısı: Chapter 15, Chapter 16
- `pytop` bağlantısı: `real_line_metric()`, `open_ball(...)`, `is_first_countable(...)`

## 2. Rasyonel sayılar

- Küme: `\mathbb{Q}`
- Metrik: reel doğrudan kısıtlanan mutlak değer metriği
- Rol: altuzay topolojisi ile metrik yapı arasındaki bağ
- Kitap bağlantısı: Chapter 07, Chapter 15
- `pytop` bağlantısı: `rationals_metric()`

## 3. Ayrık metrik

- Küme: herhangi bir `X`
- Metrik:
  - `d(x,y)=0` eğer `x=y`
  - `d(x,y)=1` eğer `x\neq y`
- Rol: ayrık topolojinin her zaman metrikten gelebileceğini göstermek
- Kitap bağlantısı: Chapter 03, Chapter 15

## 4. Kesilmiş metrik örneği

- Aynı topolojiyi üreten ama farklı sayısal değerler veren iki metrik karşılaştırılır:
  - `d_1(x,y)=|x-y|`
  - `d_2(x,y)=min\{1,|x-y|\}`
- Rol: ``aynı topoloji'' ile ``aynı metrik'' ayrımını netleştirmek
- Kitap bağlantısı: Chapter 15

## 5. Sonlu metrik uzay örnekleri

- Küme: küçük sonlu taşıyıcılar
- Rol: sonlu topolojik uzaylarla metrikten gelen topolojilerin farkını karşılaştırmak
- `pytop` bağlantısı: `FiniteMetricSpace(...)`, `induced_topological_space(...)`

## Kullanım notu

Bu dosya, `notebooks/teaching/lesson_06b_metric_and_sequences.ipynb` ve seçilmiş exploration not defterleriyle birlikte okunmalıdır. Amaç, metrik uzayların yalnız soyut tanımlarla değil, küçük hesaplamalı deneylerle de görünür hale gelmesidir.


## v1.0.54 classical benchmark corridor

Aşağıdaki ek katman, Chapter 15--16 anlatımının yalnız “metrik tanımı” düzeyinde kalmaması için açılmıştır.

### 6. Reel düzlem

- Küme: $\mathbb{R}^2$
- Metrik: Öklid metriği $d((x_1,y_1),(x_2,y_2))=\sqrt{(x_1-x_2)^2+(y_1-y_2)^2}$
- Rol: açık disk sezgisi, çarpım-topolojisi köprüsü, sayılabilir taban fikri
- Kitap bağlantısı: Chapter 08, Chapter 12, Chapter 15
- Pedagojik not: açık aralığın iki boyutlu analoğu olarak açık disk özellikle görünür tutulmalıdır; aksi halde $\mathbb{R}^2$ yalnız sembolik bir örnek gibi kalır.

### 7. Aynı topolojiyi veren iki metrik için güvenli benchmark

- Uzay: $\mathbb{R}$
- Metrikler:
  - $d_1(x,y)=|x-y|$
  - $d_2(x,y)=\min\{1,|x-y|\}$
- Rol: “aynı açık kümeler” ile “aynı uzaklık sayıları” ayrımını görünür kılmak
- Kitap bağlantısı: Chapter 15
- Pedagojik not: öğrencinin topolojik eşdeğerlik ile sayısal eşitliği karıştırmasını engellemek için güvenli ilk örnektir.

### 8. Birinci sayılabilirlik için metrik güvenli bölge

- Her metrik uzay birinci sayılabilirdir.
- Yerel taban, merkezde seçilen $B(x,1/n)$ toplarıyla kurulabilir.
- Kitap bağlantısı: Chapter 12, Chapter 15, Chapter 16
- Pedagojik not: dizilerin neden metrik uzaylarda daha güçlü çalıştığını anlatırken bu nokta açıkça kullanılmalıdır.

### 9. Cauchy ve tamlık için temel karşılaştırma çifti

#### $(\mathbb{R},|\cdot|)$
- her Cauchy dizi $\mathbb{R}$ içinde yakınsar
- rol: tamlık benchmark uzayı

#### $(\mathbb{Q},|\cdot|)$
- her Cauchy dizi yakınsamaz; örn. $\sqrt{2}$'ye giden rasyonel yaklaşıklar
- rol: eksik altuzay warning-line örneği

- Kitap bağlantısı: Chapter 16
- Pedagojik not: “Cauchy ise yakınsar” cümlesinin metrik uzay teoremi değil, tam uzay teoremi olduğu burada görülmelidir.

### 10. Sequence-facing benchmark family

- $x_n=1/n$: yakınsayan ve tek accumulation point taşıyan güvenli ilk örnek
- $x_n=(-1)^n$: yakınsamayan ama iki sabit alt dizi taşıyan örnek
- $x_n=n$: sınırsız dizi; yakınsak alt dizi yok
- bounded oscillating sequences: Bolzano--Weierstrass koridoru için güvenli laboratuvar

## Öğretim kararı

Bu dosya artık yalnız metrik tanımı örnekleri için değil, Chapter 16'daki dizi/tamlık hattını da hazırlayan bir destek dosyası olarak okunmalıdır.


## v1.0.88 metric-quantity widening corridor

Aşağıdaki yeni bant, Chapter 15'in yalnız açık-top sezgisiyle kalmaması; nokta-küme uzaklığı, küme-küme uzaklığı ve çap gibi nicelikleri de görünür biçimde taşıması için eklendi.

### 11. `C[0,1]` üzerinde integral metriği

- Küme: $C[0,1]$
- Metrik: $d(f,g)=\int_0^1 |f(x)-g(x)|\,dx$
- Rol: fonksiyon uzaylarında uzaklığın yalnız noktasal fark değil, toplam alan farkı olarak da okunabileceğini göstermek
- Kitap bağlantısı: Chapter 15 için ileri örnek; Chapter 16 için yakınsaklık sezgisi
- Dürüst not: bu örnek şu aşamada `pytop` çekirdeğinde doğrudan hesaplatılmıyor; şimdilik manuscript ve notebook hattı için örnek-bank rolü taşıyor.

### 12. `C[0,1]` üzerinde sup metriği

- Küme: $C[0,1]$
- Metrik: $d_\infty(f,g)=\sup\{|f(x)-g(x)|:x\in[0,1]\}$
- Rol: iki fonksiyon arasındaki en büyük düşey farkı metrik olarak okumak
- Kitap bağlantısı: Chapter 15, Chapter 16
- Pedagojik not: integral metriği ile sup metriği aynı uzay üzerinde farklı yakınlık sezgileri kurar; bu yüzden öğrenciye ``aynı küme üzerinde farklı metrik'' fikrini güvenli biçimde gösterir.

### 13. `\mathbb{R}^2` üzerinde üç standart metrik

- Küme: $\mathbb{R}^2$
- Metrikler:
  - $d_2((x_1,y_1),(x_2,y_2))=\sqrt{(x_1-x_2)^2+(y_1-y_2)^2}$
  - $d_1((x_1,y_1),(x_2,y_2))=|x_1-x_2|+|y_1-y_2|$
  - $d_\infty((x_1,y_1),(x_2,y_2))=\max\{|x_1-x_2|,|y_1-y_2|\}$
- Rol: aynı düzlem üzerinde farklı açık-top geometrileri görmek
- Kitap bağlantısı: Chapter 15
- Pedagojik not: birim açık topların daire, elmas ve kare görünmesi; topoloji ile metrik niceliklerin aynı şey olmadığını anlatmak için çok etkilidir.

### 14. Nokta-küme uzaklığı için temel benchmark'lar

#### Ayrık metrik

- $p\in A$ ise $d(p,A)=0$
- $p\notin A$ ise $d(p,A)=1$
- Rol: nokta-küme uzaklığının tanımını en güvenli ortamda test etmek

#### Reel doğru

- $p=2$, $A=(0,1)$ için $d(p,A)=1$
- $p=1$, $A=(0,1)$ için $d(p,A)=0$ ama $p\notin A$
- Rol: ``uzaklık sıfır'' ifadesinin her zaman ``kümeye ait olma'' anlamına gelmediğini göstermek
- Kitap bağlantısı: Chapter 15; bir sonraki sürümde closure hattı için hazırlık

### 15. Küme-küme uzaklığı sıfır ama kümeler ayrık

- Uzay: $(\mathbb{R},|\cdot|)$
- Kümeler: $A=[0,1)$ ve $B=(1,2]$
- Sonuç: $A\cap B=\varnothing$ olmasına rağmen $d(A,B)=0$
- Rol: kümeler arası uzaklık sezgisini keskinleştirmek
- Kitap bağlantısı: Chapter 15
- Warning line: ``ayrık kümeler arasında pozitif mesafe vardır'' ifadesi yalnız ek varsayımlar altında doğrudur; otomatik değildir.

### 16. Çap ve sınırlılık benchmark'ları

- $\operatorname{diam}([0,1])=1$
- $\operatorname{diam}((0,1))=1$
- $\operatorname{diam}(\mathbb{R})=\infty$
- herhangi bir sonlu altküme sınırlıdır
- sonsuz kümeler de sınırlı olabilir: örn. $(0,1)$
- Rol: ``sonlu \Rightarrow sınırlı'' sonucunun tersinin yanlış olduğunu açık tutmak
- Kitap bağlantısı: Chapter 15

## Öğretim kararı — v1.0.88

Bu dosya artık yalnız klasik ilk metrik örneklerini toplamak için değil, Chapter 15 içindeki yeni metrik nicelikler hattını beslemek için de kullanılmalıdır. Özellikle `distance-to-set`, `distance-between-sets` ve `diameter` örnekleri, bir sonraki closure-karakterizasyon sürümünden önce güvenli hazırlık bandı oluşturur.


## v1.0.92 isometry and stronger equivalence corridor

### 17. Sıkıştırılmış metrik benchmark'ı

- Uzay: herhangi bir metrik uzay $(X,d)$
- Yeni metrik:
  - $d_{\min}(x,y)=\min\{1,d(x,y)\}$
  - $d_{\mathrm{b}}(x,y)=\dfrac{d(x,y)}{1+d(x,y)}$
- Rol: büyük uzaklıkları bastırıp küçük ölçeği koruyan standart dönüşümler
- Kitap bağlantısı: Chapter 15
- Pedagojik not: öğrenciye ``aynı topoloji, farklı sayısal geometri'' fikrini güvenli biçimde verir.

### 18. İzometri benchmark'ları

#### Reel doğru üzerinde öteleme

- Dönüşüm: $f(x)=x+1$
- Uzaylar: $(\mathbb{R},|\cdot|)$ ve yine kendisi
- Sonuç: $|f(x)-f(y)|=|x-y|$
- Rol: izometrinin yalnız soyut bir tanım olmadığını göstermek

#### Birim aralık ile reel doğru

- Uzaylar: $(0,1)$ ve $\mathbb{R}$ standart metrikleriyle
- Sonuç: topolojik olarak homeomorfik, fakat izometrik değil
- Rol: homeomorfizm ile izometrinin ayrımını keskinleştirmek
- Warning line: sınırlılık ve çap gibi nicelikler izometri altında korunur; topolojik eşdeğerlik altında korunmaz.

### 19. Kapanış ve uzaklık için kısa benchmark

- Uzay: $(\mathbb{R},|\cdot|)$
- Küme: $A=(0,1)$
- Gözlem:
  - $d(1,A)=0$ ama $1\notin A$
  - buna karşılık $1\in \overline{A}$
- Rol: ``uzaklık sıfır'' ile ``üyelik'' arasındaki farkı ve closure okumasını görünür yapmak

## Öğretim kararı — v1.0.92

Bu dosya artık yalnız ilk metrik örneklerini değil, eşdeğer metrikler ile izometrilerin pedagojik ayrımını da taşımalıdır. Özellikle `same topology` ile `same metric geometry` ifadelerinin farklı olduğu, bu benchmark ailesi üzerinden sistematik biçimde vurgulanmalıdır.


## v1.0.99 controlled forward-look corridor

Aşağıdaki bant, Chapter 08'in bölüm sonundaki normlu uzay / Hilbert uzayı damarını **ana Chapter 15 gövdesini büyütmeden** ekosisteme eklemek için açılmıştır. Bu yüzden burada amaç yeni bir ana bölüm kurmak değil; metrik uzaylardan fonksiyonel analiz yönüne açılan kapıyı kontrollü biçimde göstermek ve öğrenciyi ana omurgadan koparmamaktır.

### 20. `\mathbb{R}^n` üzerinde normdan gelen metrik ailesi

- Küme: $\mathbb{R}^n$
- Normlar:
  - $\|x\|_1=\sum_{k=1}^n |x_k|$
  - $\|x\|_2=\left(\sum_{k=1}^n |x_k|^2\right)^{1/2}$
  - $\|x\|_\infty=\max_{1\le k\le n}|x_k|$
- Metrik: her norm için $d(x,y)=\|x-y\|$
- Rol: ``aynı taşıyıcı küme, farklı normlar, farklı sayısal geometri'' fikrini düzenli bir çerçevede okumak
- Kitap bağlantısı: Chapter 15 için ileri not; Chapter 23 metrikleşebilirlik sezgisi için kontrollü yan koridor
- Dürüst not: Bu örnek ailesi Volume I ana gövdesine uzun uzun taşınmamalıdır; ana işlevi, metrik ile lineer yapı arasındaki farkı görünür kılmaktır.

### 21. `C[0,1]` üzerinde iki farklı yakınlık dili

#### Sup metriği

- Metrik: $d_\infty(f,g)=\sup\{|f(x)-g(x)|:x\in[0,1]\}$
- Rol: iki fonksiyon arasındaki ``en kötü durum'' farkını okumak
- Pedagojik not: uniform yakınsaklık sezgisini taşır

#### İntegral metriği

- Metrik: $d_1(f,g)=\int_0^1 |f(x)-g(x)|\,dx$
- Rol: iki fonksiyon arasındaki toplam alan farkını okumak
- Pedagojik not: küçük bir bölgede büyük sapma ile geniş bir bölgede küçük sapma arasında fark olduğunu gösterir

- Kitap bağlantısı: Chapter 15 için ileri örnek; Chapter 16 yakınsaklık uyarı çizgisi için destek
- Dürüst not: Bu iki metrik, öğrencinin ``aynı fonksiyon uzayı üzerinde farklı yakınlık kavramları'' fikrini güvenli biçimde görmesini sağlar.

### 22. `x^n` dizisi ile metrik-duyarlılık uyarısı

- Uzay: $C[0,1]$
- Dizi: $f_n(x)=x^n$
- Karşılaştırma:
  - sup metriğinde $d_\infty(f_n,0)=1$ kalır; dolayısıyla sıfıra yakınsaklık yoktur
  - integral metriğinde $d_1(f_n,0)=\int_0^1 x^n\,dx=\frac{1}{n+1}\to 0$
- Rol: tek bir dizi üzerinde, metrik seçiminin yakınsaklık davranışını gerçekten değiştirdiğini göstermek
- Kitap bağlantısı: Chapter 16 ileri uyarı; notebook desteğiyle okunmalıdır
- Warning line: ``aynı noktasal formül'' tek başına yakınsaklık türünü belirlemez; hangi metrikte çalıştığımız belirleyicidir.

### 23. Hilbert uzayı yalnız ileri yön okuması olarak

- Güvenli ilk model: $\mathbb{R}^n$ üzerinde iç çarpım
  \[
  \langle x,y\rangle = \sum_{k=1}^n x_k y_k
  \]
  ve buna bağlı norm $\|x\|_2=\sqrt{\langle x,x\rangle}$
- Rol: ``her Hilbert uzayı bir metrik uzaydır; fakat her metrik uzay Hilbert uzayı değildir'' ayrımını açık tutmak
- Kitap bağlantısı: functional-analysis-facing forward look only
- Dürüst not: Bu satır Volume I ana omurgasının parçası değildir. Buradaki amaç, öğrenciyi yeni bir teoriye taşımak değil; neden burada durduğumuzu ve daha ileri bir kitapta hangi ek yapının devreye gireceğini açıklamaktır.

## Öğretim kararı — v1.0.99

Bu dosyadaki yeni bant, normlu uzay ve Hilbert uzayı dilini Chapter 15 ana metnine yüklemek yerine `examples_bank + notebook + supplement note` üçlüsünde tutmalıdır. Böylece genel topoloji kitabının ekseni korunur; ama öğrenciye fonksiyonel analiz yönüne açılan kapı dürüst biçimde gösterilmiş olur.

## v1.0.273 equivalent metric and isometry headings

Bu bant, Chapter 08 köprü notlarında açılan iki ayrımı örnek bankasında test edilebilir hale getirir: **eşdeğer metrikler** aynı açık kümeleri üretir; **izometriler** ise uzaklık değerlerini aynen korur. Bu nedenle iki başlık birlikte okunmalı, fakat birbirinin yerine kullanılmamalıdır.

### 24. Eşdeğer metrikler için iki yönlü top kontrolü

- Çalışma ilkesi: Aynı taşıyıcı küme üzerindeki `d` ve `rho` metrikleri aynı topolojiyi üretiyorsa, her merkez `x` ve her `d`-topu için içinde kalan bir `rho`-topu; her `rho`-topu için de içinde kalan bir `d`-topu bulunur.
- Güvenli okuma: Eşdeğerlik, uzaklıkların eşitliği değil, açık kümelerin aynı kalmasıdır.
- Test edilebilir sonlu model:
  - Taşıyıcı: `X={a,b,c}`.
  - Yol metriği: `d(a,b)=1`, `d(b,c)=1`, `d(a,c)=2`.
  - Ayrıklaştırılmış karşılaştırma metriği: `rho(x,y)=0` eğer `x=y`, `rho(x,y)=1` eğer `x!=y`.
  - Sonlu metrik uzaylarda her iki metrik de ayrık topolojiyi üretir; dolayısıyla indüklenen topolojiler aynıdır.
  - Buna rağmen özdeşlik dönüşümü izometri değildir; çünkü `d(a,c)=2` iken `rho(a,c)=1`.
- `pytop` test bağlantısı: `FiniteMetricSpace(...)`, `induced_topological_space(...)`.
- Kitap bağlantısı: Chapter 08, Chapter 15.

### 25. Sıkıştırılmış metrikler ve niceliksel uyarı

- Model aileleri:
  - `d_cap(x,y)=min{1,d(x,y)}`,
  - `d_norm(x,y)=d(x,y)/(1+d(x,y))`.
- Rol: Büyük uzaklıkları sınırlarken küçük ölçekteki açık-top davranışını koruyan standart karşılaştırma aileleridir.
- Pedagojik ayrım: Açık kümeler korunabilir; çap, sınırlılık ve Cauchy davranışı gibi metrik-niceliksel bilgiler değişebilir.
- `pytop` bağlantısı: `capped_metric(...)`, `normalized_metric(...)`.
- Dürüst sınır: Sonsuz taşıyıcılarda topolojik eşdeğerlik şu an çekirdekte tam otomatik ispatlanmıyor; bu satır örnek-bank ve manuscript köprüsü olarak kullanılmalıdır.

### 26. İzometri için sonlu yeniden adlandırma benchmark'ı

- Kaynak uzay: `X={a,b,c}` ve metrik değerleri `d(a,b)=1`, `d(b,c)=2`, `d(a,c)=3`.
- Hedef uzay: `Y={0,1,3}` ve standart mutlak değer metriği.
- Dönüşüm: `f(a)=0`, `f(b)=1`, `f(c)=3`.
- Kontrol: Her `x,y` için `|f(x)-f(y)|=d(x,y)`.
- Sonuç: Bu dönüşüm izometridir; dolayısıyla homeomorfizmdir, fakat ondan daha güçlü bir yapı korur.
- `pytop` test bağlantısı: Sonlu taşıyıcı üzerinde tüm nokta çiftleri dolaşılarak uzaklık eşitliği kontrol edilebilir.
- Kitap bağlantısı: Chapter 08, Chapter 15.

### 27. Homeomorfik ama izometrik olmayan güvenli uyarı

- Klasik okuma: `(0,1)` ile `R` standart topolojilerinde homeomorfiktir; ancak standart metriklerle izometrik değildir.
- Neden: `(0,1)` standart metrikte sınırlıdır ve çapı `1`dir; `R` standart metrikte sınırsızdır.
- Rol: Homeomorfizmin açık-küme yapısını, izometrinin ise uzaklık değerlerini koruduğunu aynı örnek üzerinden netleştirir.
- Dürüst sınır: Bu örnek çekirdekte otomatik homeomorfizma/isometri karar vericisi olarak değil, kavramsal benchmark olarak tutulur.

## Öğretim kararı — v1.0.273

`metric_space_examples.md` artık eşdeğer metrik ile izometri ayrımını yalnız sözlü uyarı olarak değil, kontrol edilebilir örnek aileleriyle taşır. Sonlu iki benchmark test katmanına uygundur; sonsuz örnekler ise manuscript ve notebook hattında kavramsal karşılaştırma yüzeyi olarak kalmalıdır.


## Öğretim kararı — v0.1.36

Chapter 15 fiziksel olarak bölünmedi; ancak örneklerin kullanım yeri iki eksene ayrıldı.

- **Metrik sezgi çekirdeği:** reel doğru, açık aralık/açık top, ayrık metrik, sonlu taşıyıcıda metrik aksiyomu kontrolü ve yerel taban örnekleri.
- **İleri metrik yapı:** eşdeğer metrikler, norm karşılaştırmaları, çarpım metrikleri, Cauchy/tamlık uyarısı ve kompakt metrik sonuçlara hazırlık.

Bu karar, örnek bankasının aynı dosya içinde kalmasını ama her örneğin hangi okuma hattına hizmet ettiğinin daha açık görülmesini sağlar.
