# Hereditary and local cardinal functions examples

Bu dosya, Cilt III Bölüm 33 için örnek-bankası merkezidir. Amaç, aynı niceliğin global, hereditary ve local okuma biçimlerinin hangi örneklerde ayrıştığını görünür hale getirmektir.

## Bölüm odağı

- Bölüm 33: hereditary ve local kardinal fonksiyonlar
- geri referanslar: Cilt I altuzay / yerel taban hattı, Cilt II Bölüm 30--31, Cilt III Bölüm 32
- sonraki kullanım: Bölüm 34 ve Bölüm 35

## Ana example familyaları

### 1. Second-countable güvenli bölge
Amaç:
- hereditary smallness ile local smallness'ın birlikte düzenli göründüğü sınıfı sabitlemek.
Kullanım:
- ilk okuma için güvenli örnek yüzeyi kurmak.
Standart adaylar:
- `\mathbb{R}`
- sayılabilir çarpım olmayan klasik ikinci sayılabilir metrik uzaylar
Not:
- her altuzay yine ikinci sayılabilir olduğu için `hd(X)` ve `hL(X)` sayılabilir kalır.

### 2. Discrete extreme behavior
Amaç:
- hereditary niceliklerin gerçekten en kötü altuzayı kaydettiğini göstermek.
Kullanım:
- `hd(X)` ve `hL(X)` için kaba ama öğretici uç örnek vermek.
Standart adaylar:
- sonsuz ayrık uzaylar
Not:
- her altuzay yine ayrık olduğu için yoğunluk ve Lindelöf davranışı doğrudan kardinaliteye eşitlenir.

### 3. Local good / global large topological sums
Amaç:
- local smallness'ın küresel nicelikleri otomatik sınırlamadığını göstermek.
Kullanım:
- Bölüm 33'ün warning-line örneği ve Bölüm 34 öncesi quantifier uyarısı.
Standart adaylar:
- `\bigsqcup_{i\in I}\mathbb{R}`
- çok bileşenli yerel olarak metrik toplam uzaylar
Not:
- her nokta first countable olabilir; buna rağmen yoğunluk ve hereditary density büyük kalabilir.

### 4. Altuzayda bozulan davranış fişleri
Amaç:
- global küçük görünen niceliklerin seçilmiş altuzaylarda neden büyüyebildiğini kısa fişler halinde tutmak.
Kullanım:
- Bölüm 35 compactness hattına geçişte hangi nicelemenin kritik olduğunu ayırmak için.
İçerik önerisi:
- ayrık altuzay çıkarımı
- yoğunluk tanığı / Lindelöf tanığı ayrımı
- subspace warning-line listesi

## Karşılaştırma tablosu için notlar

Bu dosya özellikle şu karşılaştırmaları taşımalıdır:

- global `d(X)` ile hereditary `hd(X)` aynı veri değildir,
- global `L(X)` ile hereditary `hL(X)` aynı soru değildir,
- `\chi(x,X)` gibi local nicelikler pointwise smallness söyler, hereditary smallness söylemez,
- Bölüm 32'deki `t(x,X)` ve `nw\chi(x,X)` dili, Bölüm 33'te quantifier-level warning olarak yeniden kullanılmalıdır.

## Cilt II geri referans notu

Bu dosya şu farkları açık tutmalıdır:

- Cilt II'deki temel kardinal fonksiyon sözlüğü burada yeni sembollerle değil, yeni nicelemelerle derinleşir.
- Bölüm 31'de nitel özelliklerden nicel eşiklere geçiş yapılmıştı; burada aynı niceliklerin altuzay ve nokta bazlı okuması eklenir.
- Bölüm 30'daki `\chi(X)`, `d(X)` ve `L(X)` çizgisi, Bölüm 33'te `hd(X)`, `hL(X)` ve local-smallness warning'leri ile ayrışır.


## v0.1.78 Chapter 32 entry-lane bridge

Bu sürümde örnek bankası yalnız örnek adı tutmaz; Chapter 33 profillerini Chapter 32'nin entry-lane anahtarlarına bağlayan kısa bir okuma haritası da taşır.

| Chapter 33 profili | Lane | Chapter 32 entry köprüsü | Kullanım uyarısı |
|---|---|---|---|
| `second_countable_safe_region` | entry | `character_controls_tightness`, `network_vs_weight_control` | ilk okuma için güvenli benchmark |
| `global_vs_hereditary_density` | bridge | `discrete_extreme_behavior` | global yoğunluk iddiasını altuzay tanığıyla test et |
| `global_vs_hereditary_lindelof` | bridge | `network_vs_weight_control` | bütün uzay örtü kontrolü ile en kötü altuzay örtü kontrolünü ayır |
| `local_good_global_large_sum` | warning | `character_controls_tightness`, `discrete_extreme_behavior` | local iyi davranışın global/hereditary küçüklük üretmediğini vurgula |

Chapter 34'e geçmeden önce bu dört profil, klasik eşitsizliklerin hangi niceleme düzeyinde kullanılacağını belirleyen ön filtre olarak okunmalıdır.

## Sonraki açılışlar

İlerleyen sürümlerde bu dosyaya:

- hereditary/local inequality warning fişleri,
- compactness altında hereditary smallness davranışı,
- Chapter 34 ve 35 için kısa bridge tabloları

eklenebilir.

## v0.6.27 note

Bu aşamada dosya artık yalnız başlık listesi değildir. Bölüm 33 gerçek metne dönüştürüldüğü için hereditary/local example bank da güvenli bölge, ayrık uç, local-good/global-large toplam uzay ve subspace-warning fişleriyle aktif kullanım katmanına geçirilmiştir.
