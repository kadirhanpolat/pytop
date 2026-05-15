# Cardinal functions framework examples

Bu dosya, Cilt II Bölüm 29 için kardinal fonksiyonların çerçeve örneklerini toplar.

## Ana kullanım soruları

- Hangi nicelik topolojinin hangi yönünü ölçüyor?
- Aynı uzayda farklı nicelikler neden farklı büyüklüklere sahip olabilir?
- Noktasal ölçüler ile global ölçüler neden ayrı ele alınmalıdır?

## Çekirdek örnek aileleri

### Reel doğru
**Mesaj:** birçok olumlu sayılabilirlik davranışının aynı uzayda birleştiği standart model.

### Sonsuz ayrık uzay
**Mesaj:** yerel davranış ile global davranışın farklı büyüklükler doğurabileceği standart karşılaştırma alanı.

### Sonlu uzaylar
**Mesaj:** kardinal fonksiyon sezgisinin hesaplanabilir versiyonu.

### Ağ ağırlığı örnekleri
**Mesaj:** tam taban yerine daha zayıf ağ-benzeri verilerin de anlamlı nicel bilgi taşıyabileceği.

## Bölüm 29 için köprü notu

Bu dosya, Bölüm 24'ün nicel motivasyonu ile Bölüm 30'un tek tek fonksiyonları arasında ara sözlük görevi görür.

## Notebook görev eşleşmesi

- `lesson_11_cardinal_functions_framework.ipynb`:
  - aynı uzayda noktasal / genel veri ayrımı
  - nitel özellik ile nicel eşik tablosunun ilk okunması
- `22_cardinal_functions_framework.ipynb`:
  - aynı tabloda küçük kalan ve büyüyen kardinal verileri karşılaştırma
  - Chapter 29'daki eşik dilini exploration temposunda yeniden okuma
- `lesson_13_properties_and_cardinal_functions.ipynb`:
  - Bölüm 31'e geçerken eşik dili için hazırlık köprüsü

## v0.1.70-fix3 -- Framework comparison examples

### CFF-FIX3-01 — finite discrete space

Task: In an `n`-point discrete space, explain separately what weight, density, character, Lindelof number, and cellularity measure.

Expected reading: the student must not answer only `n`. The answer should mention bases, dense sets, local bases, open-cover reduction, and pairwise disjoint nonempty open families.

### CFF-FIX3-02 — safe metric second-countable example

Task: Use a second-countable metric example to explain why a countable base gives a safe upper bound for weight and supports a countable dense witness.

Expected reading: the student should explicitly state the assumption of second countability; the route must not claim that every metric space is automatically second countable.

### CFF-FIX3-03 — pointwise/global warning

Task: Compare `chi(x,X)` and `chi(X)` in words.

Expected reading: `chi(x,X)` is pointwise local-base data; `chi(X)` is the global reading obtained from pointwise behaviour across the space.

### CFF-FIX3-04 — invariant comparison warning

Task: Explain why a small density value does not by itself determine cellularity or Lindelof number.

Expected reading: the student should name the different topological feature measured by each invariant and should not collapse all invariants to underlying set size.

## v0.1.71 -- Computable/workable cardinal-function example catalog

This version turns the framework examples into reusable records exposed by
`pytop.cardinal_function_examples` and the package-root API.

### CFF-V071-01 -- finite discrete vs finite indiscrete

Task: Compare `finite_discrete_n` and `finite_indiscrete_n` without reducing both to the same carrier size.

Expected reading: the topology, not only the carrier, determines the witness for weight, density, cellularity, spread, and network weight.

### CFF-V071-02 -- countable and uncountable discrete spaces

Task: Use the singleton cover/base to explain why global invariants grow from `aleph_0` to `kappa` while local character remains small.

Expected reading: the student must distinguish local data from global cardinal functions.

### CFF-V071-03 -- second-countable metric safety

Task: Use `second_countable_metric_safe` to record exactly where second-countability enters the computation.

Expected reading: the route must not claim that every metric space is automatically second-countable.

### CFF-V071-04 -- classical warning patterns

Task: Compare `real_line_standard`, `sorgenfrey_line_warning`, and `one_point_compactification_discrete_kappa` as warning records.

Expected reading: the examples should be treated as assumption-sensitive reading patterns; they are not finite-engine calculations.
## v0.1.72 -- Comparison exercises and notebook-route alignment

This version promotes the v0.1.71 example records into five durable comparison routes exposed by `cardinal_function_comparison_exercises()` and `cardinal_function_notebook_route_alignment()`.

### CFF-V072-01 -- `weight_vs_density`

Task: For `finite_discrete_n`, `finite_indiscrete_n`, `real_line_standard`, and `uncountable_discrete_kappa`, state separately the base witness for `w(X)` and the dense-subset witness for `d(X)`.

Expected reading: `d(X) <= w(X)` is a comparison theorem with a proof idea, not a definition and not a rule that both functions always measure the same feature.

### CFF-V072-02 -- `character_vs_weight`

Task: Use the uncountable discrete and one-point compactification patterns to explain why local-base behaviour may stay small while global base complexity grows.

Expected reading: `\chi(x,X)` is pointwise, `\chi(X)` is a global reading of pointwise data, and `w(X)` measures the size of a base for the whole topology.

### CFF-V072-03 -- `density_vs_cellularity_spread`

Task: For each listed example, identify a dense-set witness, a disjoint open-family witness, and a discrete-subspace witness when available.

Expected reading: density, cellularity, and spread use different witness types. Agreement in a familiar example is not a permission to merge definitions.

### CFF-V072-04 -- `metric_second_countable_guard`

Task: In every metric example, underline the exact assumption that gives a countable base.

Expected reading: this route deliberately blocks the invalid shortcut “metric implies second-countable” unless a separate second-countability hypothesis or theorem is supplied.

### CFF-V072-05 -- `compactness_vs_small_cardinals`

Task: Compare the compact metric pattern with the one-point compactification of an uncountable discrete space.

Expected reading: compactness controls open covers; it does not by itself force small weight, density, cellularity, spread, or network weight.

## v0.1.73 -- Assessment/questionbank alignment for comparison routes

This version keeps the v0.1.72 comparison route identifiers and maps them to generated-question-ready assessment records in `src/pytop_questionbank/cilt4_entry_assessment_routes.py`.

### CFF-V073-01 -- `weight_vs_density` assessment route

Assessment route: `CILT4-MS-IV-39-CF-WEIGHT-DENSITY-COMPARISON-ASSESSMENT`

Prompt focus: write the base witness for `w(X)` and the dense-subset witness for `d(X)` separately.

Expected signal: the student treats `d(X) <= w(X)` as a comparison theorem with a witness argument, not as a definition.

### CFF-V073-02 -- `character_vs_weight` assessment route

Assessment route: `CILT4-MS-IV-39-CF-CHARACTER-WEIGHT-COMPARISON-ASSESSMENT`

Prompt focus: distinguish pointwise character data from global base complexity.

Expected signal: the student does not infer small global weight merely from small local-base behavior.

### CFF-V073-03 -- `density_vs_cellularity_spread` assessment route

Assessment route: `CILT4-MS-IV-39-CF-DENSITY-CELLULARITY-SPREAD-ASSESSMENT`

Prompt focus: classify witnesses as dense-set, disjoint-open-family, or discrete-subspace evidence.

Expected signal: the student keeps density, cellularity, and spread definitionally separate even when some values agree.

### CFF-V073-04 -- `metric_second_countable_guard` assessment route

Assessment route: `CILT4-MS-IV-39-CF-METRIC-SECOND-COUNTABLE-GUARD-ASSESSMENT`

Prompt focus: underline the exact hypothesis that gives a countable base in a metric example.

Expected signal: the student rejects the unsupported shortcut “metric implies second-countable.”

### CFF-V073-05 -- `compactness_vs_small_cardinals` assessment route

Assessment route: `CILT4-MS-IV-39-CF-COMPACTNESS-SMALL-CARDINALS-ASSESSMENT`

Prompt focus: write compactness and small-cardinal claims as different statements.

Expected signal: the student separates open-cover compactness from countable-base, density, cellularity, or spread claims.

## v0.1.74 -- Feedback and answer-key/rubric alignment for comparison routes

This version keeps the same v0.1.72 comparison route identifiers and v0.1.73 assessment route IDs, then ties them to durable teacher-feedback surfaces.

### CFF-V074-01 -- `weight_vs_density` feedback route

Assessment route: `CILT4-MS-IV-39-CF-WEIGHT-DENSITY-COMPARISON-ASSESSMENT`

Teacher surfaces: `04_cardinal_functions_thresholds_key.tex`, `06_basic_cardinal_functions_key.tex`, `04_cardinal_functions_thresholds_rubric.md`, `06_basic_cardinal_functions_rubric.md`

Feedback focus: separate base witnesses from dense-set witnesses; do not grade `d(X) <= w(X)` as a definition.

### CFF-V074-02 -- `character_vs_weight` feedback route

Assessment route: `CILT4-MS-IV-39-CF-CHARACTER-WEIGHT-COMPARISON-ASSESSMENT`

Teacher surfaces: `04_cardinal_functions_thresholds_key.tex`, `06_basic_cardinal_functions_key.tex`, `04_cardinal_functions_thresholds_rubric.md`, `06_basic_cardinal_functions_rubric.md`

Feedback focus: require `chi(x,X)`, `chi(X)`, and `w(X)` to stay separated; reject unsupported local-to-global shortcuts.

### CFF-V074-03 -- `density_vs_cellularity_spread` feedback route

Assessment route: `CILT4-MS-IV-39-CF-DENSITY-CELLULARITY-SPREAD-ASSESSMENT`

Teacher surfaces: `04_cardinal_functions_thresholds_key.tex`, `06_basic_cardinal_functions_key.tex`, `04_cardinal_functions_thresholds_rubric.md`, `06_basic_cardinal_functions_rubric.md`

Feedback focus: classify dense-set, disjoint-open-family, and discrete-subspace witnesses before comparing values.

### CFF-V074-04 -- `metric_second_countable_guard` feedback route

Assessment route: `CILT4-MS-IV-39-CF-METRIC-SECOND-COUNTABLE-GUARD-ASSESSMENT`

Teacher surfaces: `04_cardinal_functions_thresholds_key.tex`, `06_basic_cardinal_functions_key.tex`, `04_cardinal_functions_thresholds_rubric.md`, `06_basic_cardinal_functions_rubric.md`

Feedback focus: insist on an explicit countable-base hypothesis or theorem; treat “metric implies second-countable” as a blocked shortcut.

### CFF-V074-05 -- `compactness_vs_small_cardinals` feedback route

Assessment route: `CILT4-MS-IV-39-CF-COMPACTNESS-SMALL-CARDINALS-ASSESSMENT`

Teacher surfaces: `04_cardinal_functions_thresholds_key.tex`, `06_basic_cardinal_functions_key.tex`, `04_cardinal_functions_thresholds_rubric.md`, `06_basic_cardinal_functions_rubric.md`

Feedback focus: keep compactness in open-cover language and require the warning example to explain why large cardinal data can survive compactification.

## v0.1.75 -- Notebook / worksheet route completion

The same five comparison identifiers now survive the full Chapter 29 teaching corridor:

- `weight_vs_density`
- `character_vs_weight`
- `density_vs_cellularity_spread`
- `metric_second_countable_guard`
- `compactness_vs_small_cardinals`

Read them through this durable chain:

`examples_bank/cardinal_functions_framework_examples.md` ->
`22_cardinal_functions_framework.ipynb` ->
`lesson_11_cardinal_functions_framework.ipynb` ->
`04_cardinal_functions_thresholds.md` ->
`24_basic_cardinal_functions.ipynb` ->
`lesson_12_basic_cardinal_functions.ipynb` ->
existing answer-key / rubric surfaces.
