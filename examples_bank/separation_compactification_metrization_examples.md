# Separation, compactification, and metrization examples

Bu dosya, Bölüm 21--23 için ortak örnek-bankası merkezidir. Amaç, ayırma aksiyomları, yerel kompaktlık/kompaktlaştırma ve metrikleşebilirlik çizgisinin aynı standart uzay ailesi üzerinde nasıl farklı yapısal sorular sorduğunu göstermektir.

## Çekirdek örnek aileleri

### 1. Reel doğru ve genel metrik uzaylar
- Hausdorff, düzenli, normal ve metrikleşebilir olumlu modeldir.
- Urysohn/Tietze çizgisi ile metrizasyon sezgisini temiz biçimde taşır.

### 2. Sierpiński, indiscrete ve kofinite topolojiler
- Ayırma aksiyomlarının neden birbirine indirgenemediğini gösteren uyarı örnekleridir.
- İyi davranışlı görünen bazı global sezgilerin ayırma aksiyomları olmadan bozulduğunu açıkça hissettirir.

### 3. Yerel kompakt ama kompakt olmayan uzaylar
- Özellikle \(\mathbb{R}\) ve benzeri klasik örnekler, yerel kompaktlık ile global kompaktlık arasındaki farkı görünür kılar.
- Bir-nokta kompaktlaştırmasının neden doğal olduğunu açıklar.

### 4. Metrik olmayan fakat öğretici uzaylar
- Bazı sayılabilirlik veya ayırma koşullarının eksikliği yüzünden metrikleşebilirliğin başarısız olduğu örnekler önemlidir.
- Amaç, olumlu teoremleri yalnız ezberlemek değil, niçin ek varsayım istediklerini görmektir.

## Bölüm bazlı kullanım

| Bölüm | Ana soru | Tercih edilen örnekler | Gösterilen ayrım |
|---|---|---|---|
| 21 | ayırma aksiyomları neden sürekli fonksiyonlarla yeniden okunur? | reel doğru, Sierpiński uzayı, kofinite örnekler | açık kümelerle ayırma ile sürekli fonksiyonla ayırma aynı güçte değildir |
| 22 | yerel kompaktlık neden kompaktlıktan farklı ama ona yakın bir kavramdır? | \(\mathbb{R}\), yerel kompakt Hausdorff uzaylar, bir-nokta kompaktlaştırması | yerel kompaktlık küresel kompaktlık değildir |
| 23 | bir uzay ne zaman metrikten geliyor sayılabilir? | reel doğru, sayılabilir tabanlı metrik uzaylar, metrik olmayan uyarı örnekleri | iyi ayırma + sayılabilirlik her zaman otomatik olarak metrik üretmez; doğru teorem gerekir |

## Notebook ve görev seviyesi eşleşmesi

- `lesson_08_advanced_separation.ipynb`
  - temel: ayırma aksiyomları tablosu
  - orta: fonksiyonla ayırma tartışması
  - ileri: Urysohn/Tietze ispat mimarisi
- `lesson_09_local_compactness_compactifications.ipynb`
  - temel: yerel kompaktlık / kompaktlık karşılaştırması
  - orta: bir-nokta kompaktlaştırması sezgisi
  - ileri: Hausdorff varsayımının rolü
- `lesson_10_metrization_directions.ipynb`
  - temel: olumlu ve olumsuz örnek tablosu
  - orta: ikinci sayılabilirlik ile ayırma koşullarının birlikte rolü
  - ileri: Urysohn metrizasyon çizgisinin yapıcı verisi

## Kullanım ilkesi
- Her büyük olumlu teorem için en az bir olumlu model ve bir uyarı örneği birlikte düşünülmelidir.
- Kompaktlaştırma ve metrizasyon anlatımında örnekler yalnız sonuç doğrulamak için değil, varsayım eksikliğini görünür kılmak için de seçilmelidir.

## v0.6.15 note
Bu dosya, Cilt II'nin orta hattında örnek yerleşimini daha düzenli hale getirmek için eklendi. Böylece ayırma, kompaktlaştırma ve metrikleşebilirlik bölümleri artık aynı standart-uzay havuzu üzerinden birlikte okunabilir.

## v0.6.17 note

Bu dosya artık yalnız örnek havuzu değil, aynı zamanda Bölüm 21--23 için teaching notebook yönlendirme merkezi olarak da kullanılmalıdır. Böylece standart uzay örnekleri, doğrudan ders akışı ve görev seviyesi ile eşlenmiş olur.

## v0.1.42 note

Bu sürümde Bölüm 11 (Separation Axioms) için Cilt II'nin ayrılma-aksiyomları atlası tamamlandı. Bölüm 21–23 ile ortak örnek havuzuna eklenen counterexample ailesi (CA-1 indiscrete, CA-2 Sierpiński, CA-3 cofinite, CA-4 cocountable, CA-5 finite-T1-discrete, CA-6 metric) artık bu dosyanın çekirdek örnek aileleriyle çapraz referanslıdır. Özellikle CA-3 (cofinite) ve CA-4 (cocountable) satırları, yukarıdaki Sierpiński / kofinite topoloji tartışmasının T1-not-Hausdorff koridorunu doğrudan besler. separation-axiom relation table ve counterexample atlas tokenları: is_t0 is_t1 is_hausdorff analyze_separation CA-1 CA-2 CA-3 CA-4 CA-5 CA-6.

## v0.1.55 advanced separation API note

Bölüm 21 için artık örnekler yalnız metinsel karşılaştırma olarak değil, `pytop.separation` üzerinden de kontrol edilebilir:

- sonlu ayrık uzay: `T0`, `T1`, Hausdorff, regular, T3, completely regular, Tychonoff, normal ve T4 için olumlu benchmark;
- Sierpiński uzayı: `T0` fakat `T1` olmayan uyarı modeli; `normal` ve `T4` ayrımını anlatmak için özellikle kullanışlıdır;
- metrik uzay: theorem-backed Tychonoff ve normal/T4 olumlu model;
- kofinite/kosayılabilir sonsuz aileler: `T1` olup Hausdorff olmayan ve bu yüzden T3/T4/Tychonoff hattında başarısız olan warning-line modeller.

Bu not, Bölüm 22 ve 23'e geçerken yerel kompaktlık, kompaktlaştırma ve metrikleşebilirlik varsayımlarının neden ayırma koşullarıyla birlikte okunması gerektiğini vurgular.

---

## v0.1.62 — paracompactness.py API örnekleri

### PC-01 — Sonlu uzay: parakompakt (exact)

- **Model:** $X$ sonlu ayrık.
- **API:** `is_paracompact(X)` → `status="true"`, `mode="exact"`, `criterion="finite"`.

### PC-02 — Metrikleşebilir: Stone teoremi

- **Model:** `tags=["metrizable"]`.
- **API:** `is_paracompact(X).metadata["criterion"]` → `"stone_theorem"`.

### PC-03 — Kompakt: parakompakt

- **Model:** `tags=["compact"]`.
- **API:** `is_paracompact(X).status` → `"true"`, `criterion="compact"`.

### PC-04 — Düzenli + Lindelöf: Michael teoremi

- **Model:** `tags=["t3","lindelof"]`.
- **API:** `is_paracompact(X).metadata["criterion"]` → `"michael_theorem"`.

### PC-05 — Lindelöf yalnız: bilinmiyor

- **Model:** `tags=["lindelof"]` (düzenli yok).
- **API:** `is_paracompact(X).status` → `"unknown"`.

### PC-06 — not_paracompact etiketi: false

- **Model:** `tags=["not_paracompact"]`.
- **API:** `is_paracompact(X).status` → `"false"`.

### PC-07 — Profil: anahtar teoremler ve karşı-örnekler

- **Model:** Herhangi bir uzay.
- **API:** `paracompact_profile(X)["key_theorems"]` — en az 3 teorem.
- **API:** `paracompact_profile(X)["counterexamples"]` — en az 2 karşı-örnek (Sorgenfrey, Moore).

### PC-08 — Birlik bölümleme: metrikleşebilir + Hausdorff

- **Model:** `tags=["metrizable","hausdorff"]`.
- **API:** `paracompact_profile(X)["partition_of_unity"]` — "yes" içeren dize.
