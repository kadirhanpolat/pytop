# Function-space examples bank — v1.0.292

Bu dosya Chapter 15 yönelimli fonksiyon uzayları hattını örnek bankasına açar. Amaç, dış Chapter 15 zipindeki metni, örnekleri veya cümle örgüsünü kopyalamadan; mevcut `pytop` ekosisteminin metrik, çarpım, yakınsaklık ve örnek-bankası yüzeyleriyle uyumlu **küçük, izlenebilir ve test edilebilir** bir sözleşme kurmaktır.

## Kapsam ilkesi

Bu sürüm genel bir function-space API modülü, evrensel compact-open topology inşa motoru, keyfî fonksiyon ailesi için Ascoli karar vericisi veya Banach uzayı altyapısı eklemez. v1.0.292 yalnız şu güvenli yüzeyleri örnek bankasına bağlar:

- fonksiyon kümesinin ürün uzayı sezgisiyle okunması;
- değerlendirme haritalarının nokta seçme işlemi olarak kullanılması;
- noktasal yakınsaklık ile düzgün yakınsaklık ayrımının test edilebilir örneklerle görünür olması;
- sup normun fonksiyonlar arası ortak hata sınırı olarak yorumlanması;
- point-open ve compact-open topoloji fikirlerinin alt-temel sezgi düzeyinde ayrılması;
- equicontinuity koşulunun aile düzeyinde ortak kontrol istediğinin gösterilmesi;
- Ascoli tipi sonuçların bu sürümde yalnız koşul-okuma ve warning-line düzeyinde tutulması.

Aşağıdaki `FS-0*` aileleri theorem-prover değildir. Bunlar ders anlatımı, worksheet üretimi, ilerideki questionbank sözleşmeleri ve otomatik doküman testleri için kullanılan örnek-bankası çekirdekleridir.

## Test edilebilir örnek aileleri

### FS-01 — Fonksiyon kümesini koordinat ailesi olarak okuma

- **Model:** sonlu bir `X={0,1,2}` tanım kümesinden `Y={a,b}` hedef kümesine giden tüm fonksiyonlar.
- **Beklenen davranış:** her fonksiyon, `X` üzerindeki koordinat değerlerinden oluşan bir üçlü gibi okunabilir.
- **pytop sözleşmesi:** bu sürümde genel `F(X,Y)` üreticisi açılmaz; örnek bankası, sonlu listelenebilir model üzerinden koordinat okumasını test eder.
- **Pedagojik vurgu:** Fonksiyon uzayının noktaları artık fonksiyonların kendileridir; tek bir fonksiyon “nokta”, fonksiyonun değeri ise bir koordinat verisi gibi davranır.

### FS-02 — Değerlendirme haritası nokta seçer

- **Model:** `[0,1]` üzerinde tanımlı birkaç basit reel değerli fonksiyon ve seçilen bir `t_0`.
- **Beklenen davranış:** değerlendirme işlemi `ev_{t_0}(f)=f(t_0)` biçiminde tek noktadaki değeri okur.
- **pytop sözleşmesi:** testler bir değerlendirme fonksiyonunun farklı fonksiyonları aynı seçilmiş noktada sayısal değere indirdiğini doğrular.
- **Pedagojik vurgu:** Evaluation map, fonksiyon uzayından hedef uzaya giden doğal haritadır; point-open topoloji sezgisi bu haritaların sürekliliği etrafında okunur.

### FS-03 — Noktasal yakınsaklık düzgün yakınsaklık demek değildir

- **Model:** `f_n(x)=x^n` ailesi, `[0,1]` üzerinde.
- **Beklenen davranış:** her sabit `x<1` için değerler `0`'a yaklaşır; fakat tüm aralık üzerinde tek bir ortak hata sınırıyla yakınsama sağlanmaz.
- **pytop sözleşmesi:** testler, `x_n=1-1/n` seçiminde hata büyüklüğünün sıfıra hızla zorlanmadığını sayısal bir tanık olarak kullanır.
- **Pedagojik vurgu:** Noktasal kontrol her noktayı ayrı ayrı izler; düzgün kontrol bütün tanım kümesini aynı anda denetler.

### FS-04 — Düzgün yakınsaklık sup norm ile okunabilir

- **Model:** `g_n(x)=x/n` ailesi, `[0,1]` üzerinde.
- **Beklenen davranış:** `sup_{x\in[0,1]} |g_n(x)| = 1/n` olduğundan fonksiyonlar sıfır fonksiyonuna düzgün yakınsar.
- **pytop sözleşmesi:** testler sonlu ızgara üzerinde sup hata sınırının `1/n` ile uyumlu olduğunu doğrular.
- **Pedagojik vurgu:** Sup norm, fonksiyonlar arasındaki en büyük ortak hatayı ölçer; düzgün yakınsaklık bu hatanın sıfıra gitmesiyle izlenir.

### FS-05 — Sup norm fonksiyon uzayında metrik sezgisi verir

- **Model:** `C[0,1]` içinde `f(x)=x`, `g(x)=x^2`, `h(x)=0` gibi basit fonksiyonlar.
- **Beklenen davranış:** `d_\infty(f,g)=\sup |f-g|` negatif olmayan, simetrik ve üçgen eşitsizliğiyle uyumlu bir uzaklık fikri verir.
- **pytop sözleşmesi:** bu sürümde analitik maksimum bulucu açılmaz; testler güvenli sonlu ızgara üzerinde metrik sezgisini doğrular.
- **Pedagojik vurgu:** Fonksiyonlar arası uzaklık, grafikleri tek tek karşılaştırmaktan ziyade bütün tanım kümesindeki en büyük sapmaya bakar.

### FS-06 — Point-open koşulu sonlu sayıda nokta değerini denetler

- **Model:** belirli noktalarda değerleri verilen fonksiyonlar ve bu noktalar için seçilen açık aralık hedefleri.
- **Beklenen davranış:** bir fonksiyon, seçili noktalardaki değerleri istenen aralıklara düşüyorsa point-open tipli silindirik koşulu sağlar.
- **pytop sözleşmesi:** testler pointwise membership kontrolünü küçük dictionary tabanlı fonksiyon modelleriyle yapar.
- **Pedagojik vurgu:** Point-open sezgide denetim, tek tek seçilmiş noktalardaki değer koşullarından başlar.

### FS-07 — Compact-open koşulu kompakt parça üzerinde toplu denetim ister

- **Model:** `[0,1]` içinden sonlu ızgara ile temsil edilen kompakt bir tanık küme ve hedef aralık.
- **Beklenen davranış:** fonksiyonun bu tanık kümenin tüm örnek noktalarında hedef aralıkta kalması gerekir.
- **pytop sözleşmesi:** gerçek compact-open topology inşa edilmez; testler kompakt-küme denetimi fikrini sonlu tanıkla ayırır.
- **Pedagojik vurgu:** Compact-open sezgi, yalnız tek nokta değil, kompakt parçalar üzerinde toplu değer kontrolü ister.

### FS-08 — Equicontinuity aile düzeyinde ortak süreklilik kontrolüdür

- **Model:** `0\leq a\leq 1` için `f_a(x)=a x` ailesi ve karşılaştırma için eğimleri büyüyen bir aile.
- **Beklenen davranış:** ilk aile ortak Lipschitz sınırıyla güvenli davranır; ikinci ailede tek bir ortak delta seçimi bozulur.
- **pytop sözleşmesi:** testler bounded-slope ve unbounded-slope ailelerini örnek-bankası warning-line'ı olarak ayırır.
- **Pedagojik vurgu:** Her fonksiyonun tek tek sürekli olması, aile için ortak süreklilik modülü bulunduğu anlamına gelmez; Ascoli tipi sonuçlarda bu ayrım belirleyicidir.

## İleri fazlara bırakılanlar

- genel `src/pytop/function_spaces.py` API katmanı;
- gerçek compact-open topology üreticisi;
- compact convergence ve equicontinuity için sembolik karar vericiler;
- Banach uzayı, normed vector space ve linear-operator yüzeyi;
- Arzela--Ascoli teoremi için ispat motoru.

## Chapter 15 kullanım notu

Bu dosya Chapter 15 zipini doğrudan pakete kopyalamaz; aktif pakete de kopyalamaz. Chapter 15 yalnız dış referans girdisi olarak kullanılmıştır; örnek aileleri özgünleştirilmiş, küçük tutulmuş ve mevcut ekosistemin test edilebilir sınırlarına göre yeniden formüle edilmiştir.

---

## v0.1.58 — `function_spaces.py` API örnekleri

### FS-09 — Sonlu ayrık uzayda üç topoloji çakışır

- **Model:** $X = \{0,1,2\}$ ayrık topoloji, $|X|=3$.
- **API çağrısı:** `analyze_function_space(X)`
- **Beklenen:** `status="true"`, `mode="exact"`, `carrier_size=3`.
- **Açıklama:** Sonlu uzayda $C(X,\mathbb{R}) \cong \mathbb{R}^3$; noktasal = tekdüze = kompakt-açık.

### FS-10 — Kompakt uzayda tekdüze = kompakt-açık

- **Model:** Sembolik uzay, `tags=["compact","hausdorff","second_countable"]`.
- **API çağrısı:** `compact_open_topology_profile(space)["coincides_with_uniform"]`
- **Beklenen:** "yes — when X is compact" içeren dize.
- **API çağrısı:** `uniform_topology_profile(space)["complete"]`
- **Beklenen:** "compact" ve "complete" içeren dize.

### FS-11 — Yerel kompakt uzayda üstel yasa

- **Model:** Sembolik uzay, `tags=["locally_compact","locally_compact_hausdorff"]`.
- **API çağrısı:** `compact_open_topology_profile(space)["exponential_law"]`
- **Beklenen:** "exponential" veya "locally compact" içeren dize.

### FS-12 — İkinci sayılabilir uzayda noktasal topoloji ayrılabilir

- **Model:** Sembolik uzay, `tags=["second_countable"]`.
- **API çağrısı:** `pointwise_topology_profile(space)["second_countable_condition"]`
- **Beklenen:** "second countable" içeren dize.

### FS-13 — Sayılamaz uzayda noktasal topoloji ikinci sayılabilir değil

- **Model:** Sembolik uzay, `tags=["uncountable","non_second_countable"]`.
- **API çağrısı:** `pointwise_topology_profile(space)["second_countable_condition"]`
- **Beklenen:** "not" içeren dize.

### FS-14 — `function_space_profile` dört anahtarla dönüş

- **Model:** Herhangi bir uzay.
- **API çağrısı:** `function_space_profile(space).keys()`
- **Beklenen:** `{"domain_representation","pointwise","uniform","compact_open"}`.

---

## v0.1.59 — compact-open basis elements ve homotopy profile örnekleri

### FS-15 — Sonlu uzayda alt-baz kümeleri S(K,U)

- **Model:** $X = \{0,1,2\}$ ayrık topoloji, $|X|=3$.
- **API çağrısı:** `compact_open_basis_elements(X)["finite_example"]`
- **Beklenen:** "3" ve "product" veya "singleton" içeren dize.

### FS-16 — Alt-baz/baz tanımları her uzayda mevcut

- **Model:** Herhangi bir uzay.
- **API çağrısı:** `compact_open_basis_elements(X).keys()`
- **Beklenen:** `subbasis_description`, `basis_description`, `convergence_characterisation` anahtarları.

### FS-17 — Kompakt-tekdüze yakınsaklık karakterizasyonu

- **Model:** Sembolik uzay.
- **API çağrısı:** `compact_open_basis_elements(X)["convergence_characterisation"]`
- **Beklenen:** "compact" ve "uniform" içeren dize.

### FS-18 — Yerel kompakt uzayda komşuluk tabanı

- **Model:** `tags=["locally_compact","locally_compact_hausdorff"]`.
- **API çağrısı:** `compact_open_basis_elements(X)["neighbourhood_base"]`
- **Beklenen:** "locally compact" içeren dize.

### FS-19 — Döngü uzayı $\Omega(X,x_0)$ tanımı

- **Model:** Herhangi bir uzay.
- **API çağrısı:** `compact_open_homotopy_profile(X)["loop_space"]`
- **Beklenen:** "π₁" ve "[0,1]" içeren dize.

### FS-20 — Yol uzayı fibrasyon

- **Model:** `tags=["compact","hausdorff","second_countable"]`.
- **API çağrısı:** `compact_open_homotopy_profile(X)["path_space"]`
- **Beklenen:** "fibration" içeren dize.

### FS-21 — Yerel kompakt uzayda asılma–döngü adjoint ilişkisi

- **Model:** `tags=["locally_compact","locally_compact_hausdorff"]`.
- **API çağrısı:** `compact_open_homotopy_profile(X)["adjunction_with_suspension"]`
- **Beklenen:** "adjunction" veya "locally compact" içeren dize.

### FS-22 — CW-kompleks k-uzay notu

- **Model:** `tags=["cw_complex","locally_compact_hausdorff"]`.
- **API çağrısı:** `compact_open_homotopy_profile(X)["cw_complex_note"]`
- **Beklenen:** "cw" veya "compactly generated" içeren dize.

---

## v0.1.60 — compare_function_space_topologies örnekleri

### FS-23 — Sonlu uzayda üç topoloji çakışır

- **Model:** $X$ sonlu ayrık.
- **API:** `compare_function_space_topologies(X)["fineness_order"]`
- **Beklenen:** "pt = co = u" içeren dize.

### FS-24 — Kompakt uzayda co = u

- **Model:** `tags=["compact","hausdorff"]`.
- **API:** `compare_function_space_topologies(X)["coincidence_conditions"]["co_eq_u"]`
- **Beklenen:** "yes" ile başlayan dize.

### FS-25 — Yerel kompakt uzayda katı zincir pt < co < u

- **Model:** `tags=["locally_compact","locally_compact_hausdorff"]`.
- **API:** `compare_function_space_topologies(X)["fineness_order"]`
- **Beklenen:** "pt ≤ co ≤ u" içeren dize.

### FS-26 — Karşılaştırma tablosu 3 satır

- **Model:** Herhangi bir uzay.
- **API:** `len(compare_function_space_topologies(X)["comparison_table"])`
- **Beklenen:** `3`.

### FS-27 — Genel uzayda klasik karşı-örnekler

- **Model:** Etiketsiz sembolik uzay.
- **API:** `compare_function_space_topologies(X)["counterexamples"]`
- **Beklenen:** 2+ öğeli liste, "ℝ" içeren dize.

### FS-28 — İnceltme sırası satırları: pt ≤ co, co ≤ u, pt ≤ u

- **Model:** Herhangi bir uzay.
- **API:** `compare_function_space_topologies(X)["comparison_table"]`
- **Beklenen:** Her satırda `"finer"` anahtarı "pt ≤ co", "co ≤ u", "pt ≤ u" değerleri.
