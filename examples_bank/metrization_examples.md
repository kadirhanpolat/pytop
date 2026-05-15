# Metrization examples — v0.1.57

Bu dosya, Cilt III v0.1.57 metrikleşebilirlik koridoru için durable örnek ailesini bir araya getirir. Her örnek `is_metrizable`, `metrization_profile`, `analyze_metrization` API'siyle tutarlı şekilde etiketlenmiştir.

---

## 1. Temel örnekler

### 1.1 Sonlu ayrık uzay
- **Karar:** `is_metrizable` → `true` (exact)
- **Neden:** Ayrık topolojide her tekil küme açıktır; ayrık metrik $d(x,y)=1$ ($x\neq y$) topolojiyi üretir.
- **API davranışı:** Her sonlu ayrık uzay discrete topology kontrolünden geçer.

### 1.2 Sierpiński uzayı `{0,1}`
- **Karar:** `is_metrizable` → `false` (theorem)
- **Neden:** `{0}` açık değil → uzay Hausdorff değil → metrikleşebilir olamaz.
- **API davranışı:** `not_hausdorff` etiketi veya finite non-discrete kontrolü tetiklenir.

### 1.3 Reel doğru `ℝ` (standart topoloji)
- **Etiketler:** `metrizable`, `second_countable`, `t3`
- **Karar:** `true` (theorem) — doğrudan `metrizable` etiketinden veya Urysohn kriterinden.
- **Urysohn kriteri:** `second_countable` + `t3` → metrizable.

### 1.4 Sorgenfrey doğrusu
- **Etiketler:** `not_second_countable` veya `not_metrizable`
- **Karar:** `false` (theorem)
- **Neden:** İkinci sayılabilir değil → Urysohn kriteri uygulanamaz; ve ayrıca normal ama metrizable değil.
- **Pedagojik not:** İyi ayırma (T3½) + Lindelöf, ikinci sayılabilirlik anlamına gelmez.

---

## 2. Gerekli koşullar: eleme tablosu

| Özellik eksikliği | Sonuç |
|---|---|
| Hausdorff değil | `false` — metrik uzaylar Hausdorff'tur |
| Birinci sayılabilir değil | `false` — metrik uzaylar birinci sayılabilirdir |
| İkinci sayılabilir değil | Urysohn kriteri uygulanamaz; tek başına `false` değil |

---

## 3. Urysohn metrizasyon kriteri

**Teorem (Urysohn):** İkinci sayılabilir + T3 (düzenli Hausdorff) → metrikleşebilir.

**Kanıt mimarisi:** Sayılabilir taban, sayılabilir bir sürekli fonksiyon ailesi üretmek için kullanılır; bu aile aracılığıyla uzay $[0,1]^{\mathbb{N}}$ ile gömülür (Hilbert küp). T3 koşulu her adımda ayırıcı fonksiyon sağlar.

**API:** `second_countable` + `t3` etiketleri → `criterion: urysohn_metrization`.

---

## 4. API eşleme tablosu

| Uzay | `is_metrizable` | Mod | Kriter |
|---|---|---|---|
| Sonlu ayrık | `true` | exact | — |
| Sonlu ayrık olmayan | `false` | theorem | finite non-discrete |
| `not_hausdorff` etiketli | `false` | theorem | negative tag |
| `metrizable` etiketli | `true` | theorem | positive tag |
| `second_countable` + `t3` | `true` | theorem | urysohn_metrization |
| Etiket yok | `unknown` | symbolic | — |

---

## 5. Named metrization profiles

Projedeki üç kararlı aile (`get_named_metrization_profiles()`):

| Anahtar | Sunum katmanı | Bölüm hedefleri |
|---|---|---|
| `urysohn_second_countable_regular_route` | main_text | 15, 23 |
| `compact_hausdorff_second_countable_route` | selected_block | 14, 23, 35 |
| `moore_developable_regular_route` | advanced_note | 23, 36 |

---

## 6. Çapraz referanslar

- **Bölüm 23 manuscript:** `23_metrization_directions.tex` — v0.1.57 API köprüsü bölümü
- **Cilt I Bölüm 15:** metrik uzaylar — temel metrik kavramları
- **Bölüm 12:** sayılabilirlik aksiyomları — ikinci sayılabilirlik
- **Bölüm 21:** ileri ayırma — T3, Tychonoff
- **Mevcut örnek bankası:** `examples_bank/separation_compactification_metrization_examples.md`
