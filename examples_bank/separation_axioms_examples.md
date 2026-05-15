# Ayırma aksiyomları örnek bankası

Bu dosya, Chapter 10 merkezli ayırma aksiyomları hattı için açılmış test edilebilir örnek iskeletidir. Amaç, `T0`, `T1` ve Hausdorff (`T2`) davranışlarını aynı şeymiş gibi sunmamak; sonlu örnekler, metrik benchmark ve klasik sonsuz warning-line aileleri üzerinden ayrımı görünür tutmaktır.

## v1.0.275 separation axioms examples-bank skeleton

### Kullanım sınırı

Bu iskelet bir genel ayırma aksiyomu karar vericisi değildir. Mevcut doğrulama yüzeyi özellikle şu seviyede tutulur:

- sonlu topolojik uzaylarda `T0`, `T1`, `Hausdorff` için doğrudan açık-küme kontrolü,
- metrik uzaylarda `Hausdorff => T1 => T0` teorem zinciri,
- ayrık, indiscrete, kofinite ve kosayılabilir sonsuz ailelerde aile düzeyi sınıflandırma,
- regular/normal gibi daha ileri aksiyomlar için şimdilik örnek-bankası etiketi ve pedagojik uyarı.

### SA-01 — İki noktalı indiscrete uzay: ayırmanın tamamen başarısız olduğu başlangıç

- Taşıyıcı: `X={0,1}`.
- Topoloji: `{∅, X}`.
- Beklenen profil:
  - `t0`: hayır
  - `t1`: hayır
  - `hausdorff`: hayır
- `pytop` bağlantısı: `FiniteTopologicalSpace(...)`, `is_t0(...)`, `is_t1(...)`, `is_hausdorff(...)`.
- Pedagojik rol: açık kümelerin noktaları ayıramadığı en küçük güvenli uyarı modeli.

### SA-02 — Sierpiński uzayı: `T0` ile `T1` arasındaki fark

- Taşıyıcı: `X={0,1}`.
- Topoloji: `{∅,{1},X}`.
- Beklenen profil:
  - `t0`: evet
  - `t1`: hayır
  - `hausdorff`: hayır
- `pytop` bağlantısı: `FiniteTopologicalSpace(...)`, `is_t0(...)`, `is_t1(...)`.
- Pedagojik rol: tek yönlü ayırmanın `T0` için yeterli, `T1` için yetersiz olduğunu göstermek.

### SA-03 — Sonlu ayrık uzay: tam ayırma benchmark'ı

- Taşıyıcı: sonlu bir küme.
- Topoloji: tüm altkümeler.
- Beklenen profil:
  - `t0`: evet
  - `t1`: evet
  - `hausdorff`: evet
- `pytop` bağlantısı: `FiniteTopologicalSpace(...)`, `is_hausdorff(...)`.
- Pedagojik rol: ayrık topolojide noktaların tekil açık kümelerle ayrıldığı temiz referans modeli.

### SA-04 — Metrik uzaylar: Hausdorff zinciri

- Uzay tipi: herhangi bir metrik uzay `(X,d)`.
- Beklenen profil:
  - `hausdorff`: evet
  - `t1`: evet
  - `t0`: evet
- `pytop` bağlantısı: `MetricLikeSpace(...)`, `is_hausdorff(...)`, `is_t1(...)`, `is_t0(...)`.
- Warning line: metrik olmak güçlü bir ayırma bilgisi verir; fakat bu satır regular/normal kararını otomatik API sözü olarak okumamalıdır.

### SA-05 — Sonsuz kofinite topoloji: `T1` olup Hausdorff olmayan klasik örnek

- Taşıyıcı: sonsuz bir küme.
- Topoloji: boş küme ve sonlu tümleyenli kümeler.
- Beklenen profil:
  - `t0`: evet
  - `t1`: evet
  - `hausdorff`: hayır
- `pytop` bağlantısı: `CofiniteSpace(...)`, `is_t1_infinite(...)`, `is_hausdorff_infinite(...)`.
- Pedagojik rol: `T1` koşulunun Hausdorff koşuluna yetmediğini güvenli bir sonsuz ailede göstermek.

### SA-06 — Kosayılabilir topoloji: güçlü görünen ama Hausdorff olmayan warning-line

- Taşıyıcı: özellikle sayılamaz bir küme.
- Topoloji: boş küme ve sayılabilir tümleyenli kümeler.
- Beklenen profil:
  - `t0`: evet
  - `t1`: evet
  - `hausdorff`: hayır
- `pytop` bağlantısı: `CocountableSpace(carrier="R")`, `is_hausdorff_infinite(...)`.
- Pedagojik rol: büyük açık kümelerin bol olması ile iki noktanın ayrık komşuluklarla ayrılması arasındaki farkı göstermek.

### SA-07 — Regular / normal başlıkları için dürüst sınır

- Hedef kavramlar: regular, normal, tamamen regular, Tychonoff.
- Beklenen kullanım: Chapter 10 içinde isim ve sezgi verilebilir; ancak bu sürümde genel API kararı verilmez.
- `pytop` bağlantısı: şimdilik doğrudan karar verici yok; ileride `chapter_10_separation_api_needs` hattına taşınmalıdır.
- Pedagojik rol: `T0/T1/T2` zinciri ile daha ileri ayırma aksiyomlarının aynı seviyede olmadığı vurgulanır.

### SA-08 — Ayırma aksiyomları ile sayılabilirlik/kompaktlık karıştırılmamalı

- Karşılaştırma fikri:
  - metrik uzaylar Hausdorff'tur; fakat yalnız Hausdorff olmak metrik olmak değildir,
  - kofinite topoloji kompakt ve `T1` olabilir; fakat Hausdorff olmak zorunda değildir,
  - ikinci sayılabilirlik gibi sayılabilirlik koşulları ayırma aksiyomlarının yerine geçmez.
- İlgili yüzeyler: `countability_examples.md`, `compactness_examples.md` gelecek sürüm hattı, `counterexamples.md`.
- Pedagojik rol: Chapter 09, Chapter 10 ve Chapter 11 kavramlarının birbirine karıştırılmasını önlemek.

## Test edilebilir sözleşme

Bu dosyanın v1.0.275 sözleşmesi şudur:

1. `SA-01` ile `SA-08` kodları korunur.
2. `T0`, `T1` ve Hausdorff başlıkları ayrı satırlarda tutulur.
3. Sierpiński uzayı `T0` fakat `T1` olmayan temel sonlu örnek olarak korunur.
4. Kofinite/kosayılabilir aileleri `T1` olup Hausdorff olmayan warning-line olarak etiketlenir.
5. Regular/normal gibi ileri başlıklar bu sürümde API kararı gibi sunulmaz.
6. Sayılabilirlik, kompaktlık ve metrikleşebilirlik sonuçları ayırma aksiyomlarının yerine yazılmaz.

## Öğretim kararı — v1.0.275

Chapter 10 ayırma aksiyomları hattı, "noktalar ayrılabilir" şeklinde tek cümlelik bir sezgiyle yürütülmemelidir. Bu dosya, tek yönlü ayrım (`T0`), iki yönlü tekil ayırma (`T1`) ve ayrık komşuluklarla ayırma (Hausdorff) fikirlerini ayrı ayrı izleyen bir örnek-bankası iskeleti olarak kullanılmalıdır.

## v0.1.42 separation-axiom atlas note

Bu dosya v0.1.42 ile Chapter 11 karşı örnek atlasının birincil örnek kaynağı olarak işaretlenmiştir. Atlas girişleri (CA-1 ... CA-6) buradaki SA-0x kodlarıyla eşleşir:

- CA-1 (indiscrete) ↔ SA-01
- CA-2 (Sierpiński) ↔ SA-04
- CA-3 (kofinite) ↔ SA-03
- CA-4 (ko-sayılabilir) ↔ SA-06
- CA-5 (sonlu T1) ↔ SA-02
- CA-6 (metrik Hausdorff) ↔ SA-05

Bu eşleşme, Chapter 11 ilişki tablosu ve implication zinciri ile doğrudan bağlantılıdır.

## v0.1.55 advanced separation refinements

Bu sürümle `SA-07` satırı artık yalnızca “ileride API gerekecek” uyarısı değildir; Cilt III düzeyinde sınırlı ama test edilebilir bir API yüzeyi vardır:

- `is_regular(space)` açık kümelerle nokta--kapalı küme ayrımını kontrol eder.
- `is_t3(space)` `T1 + regular` olarak okunur.
- `is_completely_regular(space)` fonksiyonla ayırma düzeyini temsil eder; genel sonsuz uzaylar için aşırı iddia üretmez.
- `is_tychonoff(space)` `T1 + completely regular` eşiğini işaretler.
- `is_normal(space)` ayrık kapalı kümeleri ayrık açık kümelerle ayırma koşulunu kontrol eder.
- `is_t4(space)` `T1 + normal` olarak okunur.
- `separation_profile(space)` bu başlıkları tek tabloda verir.

Önemli öğretim kararı: `normal` ile `T4` aynı şey gibi sunulmaz. Örneğin Sierpiński uzayı sonlu kapalı-küme ayrımı bakımından vacuous/pozitif davranış gösterebilir; fakat `T1` olmadığı için `T4` değildir. Bu ayrım, öğrencinin ileri ayırma aksiyomlarında neden “yalnız açık/kapalı ayrımı” ile “T1 ekli aksiyom” arasında dikkatli olması gerektiğini gösterir.
