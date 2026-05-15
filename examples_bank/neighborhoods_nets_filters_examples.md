# Neighborhoods, nets, and filters examples

Bu dosya, Cilt II'nin açılış hattı olan Bölüm 18--20 için ortak örnek ve karşı-örnek merkezidir. Amaç, komşuluk dili, ağ yakınsaklığı ve süzgeç yakınsaklığı arasındaki bağı aynı örnek ailesi üzerinde görünür kılmaktır.

## Çekirdek örnek aileleri

### 1. Reel doğru
- Komşuluk, yerel taban ve sıradan dizi sezgisi için temel olumlu modeldir.
- Ağların ve süzgeçlerin dizileri genişleten araçlar olduğunu göstermek için başlangıç örneğidir.

### 2. Ayrık uzaylar
- Her noktanın tekil açık komşuluğa sahip olduğu uç örnektir.
- Yerel bilginin çok güçlü, yakınsaklığın ise çok katı olduğu durumda komşuluk/ağ/süzgeç ilişkilerini sade biçimde gösterir.

### 3. İndiscrete ve kofinite topolojiler
- Komşuluk bilgisinin çok kaba olabildiğini gösterir.
- Dizi sezgisinin tek başına yeterli görünmediği yerlerde ağ ve süzgeç dilinin neden daha doğal olduğunu sezdirir.

### 4. Sonlu uzaylar
- Komşuluk sistemlerinin ve süzgeç tabanlarının elle listelenebildiği laboratuvar örnekleridir.
- `pytop` ile yapılacak sonraki exploration notebook ailesi için iyi hazırlık sağlar.

## Bölüm bazlı kullanım

| Bölüm | Ana soru | Tercih edilen örnekler | Gösterilen ayrım |
|---|---|---|---|
| 18 | açık küme dili ile komşuluk dili gerçekten eşdeğer mi? | reel doğru, ayrık uzay, indiscrete uzay | açık olmak ile komşuluk olmak aynı değildir |
| 19 | neden dizi yerine ağ gerekir? | reel doğru, kofinite/cocountable örnekler, yönlendirilmiş komşuluk aileleri | dizi sezgisi ile genel topolojik yakınsaklık aynı kapsamda değildir |
| 20 | neden aynı yakınsaklık olgusunu süzgeçlerle de kodlarız? | komşuluk süzgeci, ayrık uzay, kompakt örnekler | indeksli yaklaşma ile kararlı küme aileleri farklı ama eşdeğer okuma sunar |

## Kullanım ilkesi
- İlk örnek, kavramı tanıtmalı.
- İkinci örnek, uç davranışı göstermeli.
- Karşı örnek, dizi sezgisinin veya açıklık varsayımının otomatik olmadığını açıkça vurgulamalıdır.

## v0.6.15 note
Bu dosya, Cilt II'nin açılış hattını örnek-bankası bakımından 24--31 bandına daha yakın olgunluğa taşımak için eklendi. Böylece `18--20` hattı da artık yalnız bölüm içi örneklerle değil, dış destek katmanıyla birlikte okunabilir.

## v0.6.16 notebook bridge note

Bu dosya artık yalnız manuskript dışı örnek havuzu değildir; aşağıdaki exploration notebook ailesiyle doğrudan eşleşir:

- `notebooks/exploration/10_neighborhood_systems.ipynb`
- `notebooks/exploration/11_nets.ipynb`
- `notebooks/exploration/12_filters.ipynb`

Böylece `18--20` hattında örnek seçimi, bölüm metni ile küçük deney not defterleri arasında açık bir köprü kazanmış olur.


## v1.0.60 finite-neighborhood profile

Aşağıdaki sonlu uzay, Chapter 18 için elle çalışılabilecek güvenli benchmark örneği olarak tutulmalıdır:

- taşıyıcı: \(X=\{a,b,c\}\)
- topoloji: \(	au=\{arnothing,\{a\},\{a,b\},X\}\)

Bu uzayda:

- \(a\) için minimal açık komşuluk: \(\{a\}\)
- \(b\) için minimal açık komşuluk: \(\{a,b\}\)
- \(c\) için minimal açık komşuluk: \(X\)

Pedagojik görevler:

1. Her noktanın tüm komşuluklarını listelemek.
2. Bir altkümenin closure'ını yalnız komşuluk karakterizasyonuyla bulmak.
3. Süreklilik için ters görüntü yerine komşuluk koşulunu denemek.

Bu örnek, Chapter 05 operatörleri ile Chapter 18 komşuluk dili arasındaki geçişi görünür kılan en küçük laboratuvarlardan biridir.



## v0.1.37 local checking bridge

Chapter 18 artık komşuluk sistemini yalnız açık komşulukların listesi olarak değil, açık çekirdeklerden üretilen tüm komşuluk ailesi olarak okur. Bu dosyadaki sonlu benchmark örneğinde öğretim sırası şu olmalıdır:

1. Önce \(x\)'i içeren açık kümeleri listele.
2. Sonra bu açık kümelerden en az birini içeren bütün aday kümeleri komşuluk olarak kabul et.
3. Aday kümenin açık olmasının gerekmediğini özellikle göster.
4. Closure ve süreklilik karakterizasyonlarında yerel kontrolün açık çekirdek üzerinden yapıldığını vurgula.

Bu not, `pytop.neighborhood_system_of_point` ve `pytop.is_neighborhood_of_point` davranışıyla uyumludur.


## v0.1.38 nets handoff bridge

Chapter 19 artık üçlü bir öğretim sırasıyla okunmalıdır:

1. İndeks ailesinin gerçekten yönlendirilmiş önsıra olup olmadığını kontrol et.
2. Bir küme için ``sonunda içinde'' ifadesini son-kuyruk tanığıyla test et.
3. Yakınsaklığı, limit adayının her açık komşuluğu için ayrı bir eventual-containment kontrolüne indir.

Bu not `pytop.is_directed_set`, `pytop.is_eventually_in` ve `pytop.net_converges_to` davranışıyla uyumludur. Fonksiyonlar sonlu öğretim modelleri içindir; genel topolojik yakınsaklığı otomatik ispat motoru gibi ele almaz.

## v0.1.39 filters handoff bridge

Chapter 20 artık dörtlü bir öğretim sırasıyla okunmalıdır:

1. Bir ailenin gerçekten süzgeç tabanı olup olmadığını (B1) ve (B2) koşullarıyla kontrol et.
2. Tabanın ürettiği süzgeci üst küme kapatması yoluyla kur.
3. Komşuluk süzgecini, noktayı içeren açık kümelerin ailesinden oluşturulan süzgeç tabanı olarak gör.
4. Süzgeç yakınsaklığını, limit adayının her açık komşuluğunun süzgeçte bulunması koşuluna indir.

Bu not `pytop.is_filter_base`, `pytop.generated_filter`, `pytop.neighborhood_filter_base` ve `pytop.filter_converges_to` davranışıyla uyumludur. Fonksiyonlar sonlu öğretim modelleri içindir; sonsuz süzgeç teorisini otomatik ispat motoru gibi ele almaz.


## v0.1.51 Cilt III komşuluk sistemi koridoru notu

v0.1.51 ile komşuluk sistemleri aksiyomatik (N1–N4) çerçevede ve `pytop` API yüzeyiyle
desteklenmiştir. Yeni API: `neighborhood_system_axioms`, `neighborhood_system`,
`local_base_check`, `character_at_point`, `topology_from_neighborhood_system`,
`analyze_neighborhood_system`.

### Temel örnekler

| Uzay              | χ(x,X)  | N(x) büyüklüğü           |
|-------------------|---------|--------------------------|
| Ayrık {a,b,c}     | 1 (her x) | 2^(n-1) komşuluk       |
| İndiscrete {a,b}  | 1 (her x) | Yalnızca {a,b}          |
| Sierpiński {0,1}  | χ(1)=2, χ(0)=1 | N(1)={1},{0,1} |

### API token check

<!-- neighborhood_system_axioms neighborhood_system local_base_check character_at_point topology_from_neighborhood_system analyze_neighborhood_system cilt_iii_corridor v0_1_51 -->


## v0.1.52 Cilt III nets corridor note

Chapter 19 artık yalnız ``sonunda içinde'' ve yakınsaklık tanığıyla değil, aynı zamanda ``sık sık içinde'' ve küme-noktası tanısıyla da okunmalıdır.

Önerilen öğretim sırası:

1. `is_directed_set` ile indeks ailesinin yönlendirilmiş önsıra olduğunu doğrula.
2. `is_eventually_in` ile belirli bir küme için son-kuyruk tanığı ara.
3. `is_frequently_in` ile her son-kuyruğun aynı kümeye yeniden uğrayıp uğramadığını kontrol et.
4. `net_converges_to` ile her açık komşulukta sonunda kalma koşulunu test et.
5. `net_cluster_points` ile her açık komşuluğa sık sık uğrama koşulundan küme-noktalarını çıkar.
6. `analyze_net` ile aynı veriyi notebook/ödev raporunda tek yapılandırılmış sonuç olarak göster.

Bu not, v0.1.52'nin Cilt III nets koridorudur. Fonksiyonlar sonlu öğretim modelleri içindir; genel sonsuz ağ teorisini otomatik ispat motoru gibi ele almaz.

### API token check

<!-- is_frequently_in net_cluster_points analyze_net cilt_iii_nets_corridor v0_1_52 -->


## v0.1.53 Cilt III filters corridor note

Chapter 20 artık süzgeçleri yalnız taban üretimi ve yakınsaklık testi olarak değil, aynı zamanda incelik karşılaştırması ve yığılma/adherence tanısı olarak da okur.

Önerilen öğretim sırası:

1. `is_filter_base` ile aday tabanın B1--B2 koşullarını doğrula.
2. `generated_filter` ile tabanın ürettiği süzgeci kur.
3. `is_filter` ile F1--F3 aksiyomlarını doğrudan denetle.
4. `neighborhood_filter_base` ve `filter_converges_to` ile komşuluk süzgeci/yakınsaklık bağını göster.
5. `is_finer_filter` ile bir süzgecin diğerinden daha ince olup olmadığını kontrol et.
6. `filter_clusters_at` ve `filter_cluster_points` ile yakınsaklık ile yığılma/adherence farkını görünür kıl.
7. `analyze_filter` ile aynı veriyi notebook/ödev raporunda tek yapılandırılmış sonuç olarak göster.

Bu not, v0.1.53'ün Cilt III filters koridorudur. Fonksiyonlar sonlu öğretim modelleri içindir; genel sonsuz süzgeç teorisini otomatik ispat motoru gibi ele almaz.

### API token check

<!-- is_finer_filter filter_clusters_at filter_cluster_points analyze_filter cilt_iii_filters_corridor v0_1_53 -->


## v0.1.54 Cilt III sequence--net--filter comparison table

The convergence tools can now be introduced as one comparison table rather than as three disconnected APIs.

Suggested reading order:

1. Start with `sequence_converges_to` and `analyze_sequences` to keep the undergraduate intuition visible.
2. Move to `is_eventually_in`, `is_frequently_in`, `net_converges_to`, and `net_cluster_points` to show why directed sets repair the limitations of sequences.
3. Move to `filter_converges_to`, `is_finer_filter`, and `filter_cluster_points` to show how convergence and adherence can be expressed by set families.
4. Use `convergence_comparison_table` or `render_convergence_comparison_table` as the notebook/handout bridge across all three languages.

### API token check

<!-- ConvergenceComparisonRow convergence_comparison_table convergence_comparison_row render_convergence_comparison_table cilt_iii_convergence_comparison v0_1_54 -->

