# Preservation table examples bank — v0.1.48

Bu dosya, Cilt II temel koruma tablosu koridor yüzeyini açar.

## Kapsam

Beş temel topolojik özellik ve beş standart inşaat:

- Özellikler: bağlılık, kompaktlık, Hausdorff, T1, ikinci sayılabilirlik
- İnşaatlar: altuzay, sonlu çarpım, sayılabilir çarpım, bölüm, sürekli görüntü

## Koruma tablosu örnekleri

### PT-01 — Kompaktlık sürekli görüntüde korunur

- **Teorem:** Kompakt uzayın sürekli görüntüsü kompakttır.
- **Örnek:** `[0,1]` kompakttır; `f: [0,1] -> R` sürekli ise `f([0,1])` kompakttır.
- **pytop sözleşmesi:** `preservation_table_lookup("compactness", "continuous_image")` → True.

### PT-02 — Bağlılık sürekli görüntüde korunur

- **Teorem:** Bağlı uzayın sürekli görüntüsü bağlıdır.
- **Örnek:** `R` bağlıdır; `f: R -> R` sürekli ise `f(R)` bir aralıktır.
- **pytop sözleşmesi:** `preservation_table_lookup("connectedness", "continuous_image")` → True.

### PT-03 — Hausdorff bölümde korunmaz

- **Karşı örnek:** `R` Hausdorff'tur; iki ayrı noktayı özdeşleştiren bölüm uzayı Hausdorff olmayabilir.
- **pytop sözleşmesi:** `preservation_table_lookup("hausdorff", "quotient")` → False.

### PT-04 — Kompaktlık altuzayda koşulludur

- **Koşul:** Kompakt uzayın kapalı altuzayı kompakttır; açık altuzay olmayabilir.
- **Örnek:** `(0,1)` açık altuzay olarak kompakt değildir; `[a,b] ⊂ [0,1]` kapalı altuzay olarak kompakttır.
- **pytop sözleşmesi:** `preservation_table_lookup("compactness", "subspace")` → conditional.

### PT-05 — Hausdorff altuzayda korunur

- **Teorem:** Hausdorff uzayın her altuzayı Hausdorff'tur.
- **pytop sözleşmesi:** `preservation_table_lookup("hausdorff", "subspace")` → True.

### PT-06 — İkinci sayılabilirlik bölümde korunmaz

- **Karşı örnek:** Büyük bölüm uzayları ikinci sayılabilirliği yitirebilir.
- **pytop sözleşmesi:** `preservation_table_lookup("second_countability", "quotient")` → False.

## v0.1.48 note

Bu dosya v0.1.48 ile açıldı. Tokenlar: basic preservation table, preservation corridor, preservation_table_lookup, preservation_table_row, preservation_table_column, analyze_preservation_table.

---

## v0.1.64 — Cilt III preservation_table genişletmesi

### PT-09 — 14 özellik için preservation_table

- **API:** `preservation_table(property_name)["rows"]` — 8 satır.
- **Kapsam:** compactness, countable_compactness, sequential_compactness, pseudocompactness, lindelof, paracompactness, local_compactness, metrizability, hausdorff, regularity, normality, second_countability, separability, connectedness.

### PT-10 — Sonsuz çarpım tuzakları

- **Lindelöf:** `preservation_table_lookup("lindelof","finite_product")` → False (Sorgenfrey düzlemi).
- **Normallik:** `preservation_table_lookup("normality","finite_product")` → False.
- **Parakompaktlık:** `preservation_table_lookup("paracompactness","arbitrary_product")` → False.

### PT-11 — Sürekli görüntü sütunu

- **API:** `preservation_table_column("continuous_image")` → 14 özellik için verdict listesi.
- **Korunan:** compactness, countable_compactness, sequential_compactness, pseudocompactness, lindelof, separability, connectedness.
- **Korunmayan:** hausdorff, regularity, normality, metrizability, local_compactness.

### PT-12 — Değişmezlik profili: güç örnekler

- **API:** `invariance_profile(X)["difficult_cases"]` — en az 4 güç örnek.
- **Beklenen:** Sorgenfrey düzlemi, 2^{ω₁}, ℝ^{ω₁} referansları.

### PT-13 — analyze_preservation Result cephesi

- **API:** `analyze_preservation("compactness")` → `status="true"`, `mode="theorem"`, `version="0.1.64"`.

### PT-14 — Eski API uyumluluğu

- `preservation_table_lookup`, `preservation_table_row`, `preservation_table_column`, `analyze_preservation_table` işlevleri v0.1.48 davranışını korur.
