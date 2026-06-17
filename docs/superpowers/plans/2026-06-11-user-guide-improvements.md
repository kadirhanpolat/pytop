# User Guide İyileştirmeleri — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** pytop user guide'da (markdown + notebook + python) üç iyileştirme: (1) ch10'da ham set/frozenset → make_set/empty_set, (2) ch03'e eksik relation fonksiyon örnekleri, (3) tüm bölümlere maarif tarzı pedagojik Markdown blokları.

**Architecture:** Her bölüm üç formatta paralel tutulur: `docs/user_guide/notebook/*.ipynb`, `docs/user_guide/markdown/*.md`, `docs/user_guide/python/*.py`. Değişiklikler üç formatta senkronize uygulanır. Maarif blokları standart Markdown bloklara (>`...`) dönüştürülür — IPython veya ek bağımlılık gerektirmez.

**Tech Stack:** Python 3.11+, pytop API (`sets.py`, `relations.py`), Jupyter notebook JSON, Markdown

---

## Dosya Haritası

**Değiştirilen dosyalar:**

| Dosya | Aksiyon |
|-------|---------|
| `docs/user_guide/notebook/ch10_continuous_maps.ipynb` | make_set/empty_set import + kullanım + maarif blokları |
| `docs/user_guide/markdown/ch10_continuous_maps.md` | aynı |
| `docs/user_guide/python/ch10_continuous_maps.py` | aynı |
| `docs/user_guide/notebook/ch03_set_theory.ipynb` | yeni örnekler + import + maarif blokları |
| `docs/user_guide/markdown/ch03_set_theory.md` | aynı |
| `docs/user_guide/python/ch03_set_theory.py` | aynı |
| `docs/user_guide/notebook/ch01_quick_start.ipynb` | maarif blokları |
| `docs/user_guide/markdown/ch01_quick_start.md` | maarif blokları |
| `docs/user_guide/python/ch01_quick_start.py` | maarif blokları |
| `docs/user_guide/notebook/ch04_topological_spaces.ipynb` | maarif blokları |
| `docs/user_guide/markdown/ch04_topological_spaces.md` | maarif blokları |
| `docs/user_guide/python/ch04_topological_spaces.py` | maarif blokları |
| `docs/user_guide/notebook/ch07_compactness.ipynb` | maarif blokları |
| `docs/user_guide/markdown/ch07_compactness.md` | maarif blokları |
| `docs/user_guide/python/ch07_compactness.py` | maarif blokları |
| (ch02, ch05, ch06, ch08, ch09, ch11–ch16 de aynı şekilde) | maarif blokları |

---

## Maarif Blok Şablonu (tüm bölümler için)

Her bölüme şu beş blok eklenir:

```markdown
> **Neden bu konu?** [bölüme özgü motivasyon — 1-2 cümle]

> 🔍 **Kendin dene:** [ilk örnek öncesinde talimat]

> ⚠️ **Sık hata:** [yaygın yanlış kullanım]

> ↗️ **Bkz.:** [diğer bölümlerle bağlantı]

> 💭 **Öz-yansıtma:** [kapanış soruları]
```

Notebook'larda her blok ayrı bir `markdown` hücresidir.
Markdown dosyalarında paragraf olarak eklenir.
Python dosyalarında `# %% [markdown]\n"""..."""` bloğu olarak eklenir.

---

## Task 1: ch10 — make_set/empty_set + sadeleme

**Files:**
- Modify: `docs/user_guide/notebook/ch10_continuous_maps.ipynb`
- Modify: `docs/user_guide/markdown/ch10_continuous_maps.md`
- Modify: `docs/user_guide/python/ch10_continuous_maps.py`

### 1a. Python dosyası

- [ ] **Adım 1: Import'a make_set, empty_set ekle**

`ch10_continuous_maps.py` satır 85–94'teki import bloğunu değiştir:

```python
from pytop import (
    sierpinski_space,
    discrete_topology,
    indiscrete_topology,
    make_topology,
    make_set,
    empty_set,
    real_line_metric,
    closed_unit_interval_metric,
    is_continuous_finite_map,
    finite_homeomorphism_result,
)
```

- [ ] **Adım 2: s_topo/d_topo/ind_topo sadeleme**

`[set(u) for u in s.topology]` → `list(s.topology)` (is_continuous_finite_map Iterable[Iterable] kabul eder).

Tüm örneklerde (5.1, 5.2, 5.3, 5.4):
```python
# ÖNCE:
s_topo = [set(u) for u in s.topology]
d_topo = [set(u) for u in d.topology]
ind_topo = [set(u) for u in ind.topology]

# SONRA:
s_topo = list(s.topology)
d_topo = list(d.topology)
ind_topo = list(ind.topology)
```

- [ ] **Adım 3: Örnek 5.6 tau_X → make_set**

```python
# ÖNCE:
tau_X = [set(), {1}, {2, 3}, {1, 2, 3}]

# SONRA:
tau_X = [empty_set(), make_set(1), make_set(2, 3), make_set(1, 2, 3)]
```

### 1b. Markdown dosyası

- [ ] **Adım 4: Kod bloklarını güncelle** (§4 API'ye `make_set, empty_set` ekle, §5.6 kod bloğunu güncelle, `[set(u) for u in ...]` → `list(...)`)

### 1c. Notebook dosyası

- [ ] **Adım 5: Import hücresini güncelle** (make_set, empty_set ekle)
- [ ] **Adım 6: set(u) for u hücrelerini güncelle** → `list(...)`)
- [ ] **Adım 7: tau_X hücresini güncelle** → make_set/empty_set

- [ ] **Adım 8: Commit**
```bash
git add docs/user_guide/notebook/ch10_continuous_maps.ipynb
git add docs/user_guide/markdown/ch10_continuous_maps.md
git add docs/user_guide/python/ch10_continuous_maps.py
git commit -m "docs: ch10 – make_set/empty_set kullanımı ve s_topo sadeleştirme"
```

---

## Task 2: ch03 — Yeni Relation Örnekleri

**Files:**
- Modify: `docs/user_guide/notebook/ch03_set_theory.ipynb`
- Modify: `docs/user_guide/markdown/ch03_set_theory.md`
- Modify: `docs/user_guide/python/ch03_set_theory.py`

### 2a. Import'a eklenecekler

```python
from pytop import (
    make_set, power_set,
    set_union, set_intersection, set_difference,
    is_subset, is_proper_subset, equal_sets,
    make_relation, is_equivalence_relation,
    identity_relation, inverse_relation, compose_relations,
    relation_profile,
    equivalence_class, partition_from_equivalence,
    total_order_from_list,
    normalize_finite_map_data,
    is_injective_finite_map, is_surjective_finite_map, is_bijective_finite_map,
    image_of_subset_finite, preimage_of_subset_finite,
)
```

### 2b. Yeni Örnekler (§5 sonuna ekle: 5.7, 5.8, 5.9)

- [ ] **Adım 1: Örnek 5.7 — Bağıntı Bileşimi**

```python
# Örnek 5.7 — Bağıntı Bileşimi
carrier_c = [1, 2, 3, 4]
R_c = make_relation(carrier_c, (1,2),(2,3),(3,4))
S_c = make_relation(carrier_c, (2,4),(3,1),(4,2))

RS = compose_relations(R_c, S_c)   # S ∘ R: önce R, sonra S
print("R:", sorted(R_c))
print("S:", sorted(S_c))
print("S ∘ R:", sorted(RS))
# Yorum: (1,2)∈R ve (2,4)∈S → (1,4)∈S∘R
```

Beklenen çıktı:
```text
R: [(1, 2), (2, 3), (3, 4)]
S: [(2, 4), (3, 1), (4, 2)]
S ∘ R: [(1, 4), (2, 1), (3, 2)]
```

- [ ] **Adım 2: Örnek 5.8 — Denklik Sınıfları ve Bölüntü**

```python
# Örnek 5.8 — Denklik Sınıfları ve Bölüntü
carrier_e = [0, 1, 2, 3, 4, 5]
# mod-3 denkliği: 0~3, 1~4, 2~5
rel_mod3 = make_relation(carrier_e,
    (0,0),(1,1),(2,2),(3,3),(4,4),(5,5),
    (0,3),(3,0),(1,4),(4,1),(2,5),(5,2))

print("Denklik mi:", is_equivalence_relation(carrier_e, rel_mod3))
print("[0] =", sorted(equivalence_class(carrier_e, rel_mod3, 0)))
print("[1] =", sorted(equivalence_class(carrier_e, rel_mod3, 1)))
print("[2] =", sorted(equivalence_class(carrier_e, rel_mod3, 2)))

boluntu = partition_from_equivalence(carrier_e, rel_mod3)
print("Bölüntü:", sorted([sorted(b) for b in boluntu]))
```

Beklenen çıktı:
```text
Denklik mi: True
[0] = [0, 3]
[1] = [1, 4]
[2] = [2, 5]
Bölüntü: [[0, 3], [1, 4], [2, 5]]
```

- [ ] **Adım 3: Örnek 5.9 — Toplam Sıra**

```python
# Örnek 5.9 — Toplam Sıra (total_order_from_list)
carrier_t = ['a', 'b', 'c', 'd']
total_ord = total_order_from_list(*carrier_t)  # a < b < c < d

from pytop import is_partial_order, is_total_order
print("Toplam sıra çiftleri:", sorted(total_ord))
print("Kısmi sıra mı:", is_partial_order(carrier_t, total_ord))
print("Toplam sıra mı:", is_total_order(carrier_t, total_ord))
```

Beklenen çıktı:
```text
Toplam sıra çiftleri: [('a', 'a'), ('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'b'), ('b', 'c'), ('b', 'd'), ('c', 'c'), ('c', 'd'), ('d', 'd')]
Kısmi sıra mı: True
Toplam sıra mı: True
```

### 2c. Alıştırma ekleri (§6 sonuna)

- [ ] **Adım 4: K4, K5, T3 ekle**

```text
K4. R = {(1,2),(2,3),(3,1)} ve S = {(1,3),(2,1),(3,2)} bağıntıları için
    S∘R ve R∘S'yi hesaplayın; eşit mi?

K5. {0,1,2,3,4} üzerinde mod-2 denkliğini make_relation ile tanımlayın;
    her denklik sınıfını equivalence_class ile yazdırın.

T3. İki bağıntının bileşiminin tersinin, terslerin ters sıraya bileşimi ile
    eşit olduğunu (R∘S)⁻¹ = S⁻¹∘R⁻¹ kanıtlayın.
```

- [ ] **Adım 5: §4 API bölümüne yeni fonksiyonları ekle**

```text
`compose_relations(first, second)` → `set[tuple]` — second ∘ first
`equivalence_class(carrier, relation, point)` → `set` — [point]
`partition_from_equivalence(carrier, relation)` → `set[frozenset]`
`total_order_from_list(*elements)` → `set[tuple]` — yansımalı toplam sıra
```

- [ ] **Adım 6: Commit**
```bash
git add docs/user_guide/notebook/ch03_set_theory.ipynb
git add docs/user_guide/markdown/ch03_set_theory.md
git add docs/user_guide/python/ch03_set_theory.py
git commit -m "docs: ch03 – compose_relations/equivalence_class/partition/total_order örnekleri"
```

---

## Task 3: Maarif Pedagojik Blokları — Tüm Bölümler

Her bölüm için beş standart blok eklenir. Aşağıda bölüm bazlı içerik verilmiştir.

### ch01 — Hızlı Giriş

```
Neden:  pytop'un temel nesnelerini tanımadan diğer bölümler okunamaz.
Keşif:  discrete_topology(0,1,2) oluşturduktan sonra topology listesini
        elle inceleyerek tüm alt kümelerin açık olup olmadığını sayın.
Hata:   r.status == True yerine r.status == 'true' kullanın (dize karşılaştırması).
Bkz.:   Bölüm 4 (uzay aksiyomları), Bölüm 5 (kapalı kümeler/kapanış).
Yansıma: make_topology'nin farkı nedir? Neden Result bir bool değil?
```

### ch02 — Propositional Logic

```
Neden:  pytop'un yüklem sistemi (Result, status) sıfır/bir yerine üçlü
        (true/false/unknown) mantık kullanır; bu bölüm onu açıklar.
Keşif:  status=='unknown' dönen bir yüklem bulup nedenini araştırın.
Hata:   not r.value yerine r.status == 'false' ile karşılaştırın.
Bkz.:   Bölüm 1 (Result tipi), Bölüm 6 (ayırma aksiyomları).
Yansıma: 'unknown' durumu ne zaman ortaya çıkar?
```

### ch03 — Küme Teorisi

```
Neden:  Tüm topoloji API'si küme ve bağıntı soyutlamalarına dayanır;
        bu temeli sağlam kurmadan ilerisi karmaşıklaşır.
Keşif:  make_set(1,2,3) ve frozenset({1,2,3}) arasındaki farkı Python
        print() ile gözlemleyin; tür aynı mı?
Hata:   make_relation(carrier, *pairs)'te carrier verilmezse hata alırsınız;
        her bağıntı tanımında carrier listesini ilk argüman yapın.
Bkz.:   Bölüm 12 (bölüm topolojisi — equivalence_class kullanımı).
Yansıma: Bileşim sırasız mı? compose_relations(R,S) ile compose_relations(S,R)
         her zaman farklı mı?
```

### ch04 — Topolojik Uzaylar

```
Neden:  Topoloji aksiyomları (T1–T3) her şeyin temeli; make_topology bunları
        otomatik tamamlar.
Keşif:  make_topology([1,2,3], {1}) ile make_topology([1,2,3], {1},{2}) arasındaki
        topoloji boyutunu karşılaştırın.
Hata:   make_topology bir alt-baz alıp kapatır; verilen kümeler değil,
        kapatma sonucu topoloji oluşur.
Bkz.:   Bölüm 5 (kapanış/iç), Bölüm 10 (süreklilik).
Yansıma: Kaç açık küme gördünüz? Alt-baz boyutu ile topoloji boyutu
         ne zaman eşit olur?
```

### ch05 — Yüklemler ve Operatörler

```
Neden:  Kapanış, iç ve sınır işlemleri topolojik analizin temel araçları;
        pytop bunları sembolik ve sonlu uzaylarda hesaplar.
Keşif:  cl({0}) ile cl({1})'i Sierpiński uzayında hesaplayın; hangisi
        daha büyük?
Hata:   closure_of_subset bir nokta değil küme alır; cl(0) değil cl({0}).
Bkz.:   Bölüm 4 (topoloji tanımı), Bölüm 6 (T1: nokta kapanışları kapalı).
Yansıma: İç küme her zaman kapalı olur mu? Sınır boş olabilir mi?
```

### ch06 — Ayırma Aksiyomları

```
Neden:  T0–T4 hiyerarşisi Hausdorff gibi güçlü özelliklerin tam
        anlaşılması için gerekli; kümeler arası ayrışma fikrinden doğar.
Keşif:  Sierpiński'nin T0 ama T1 olmadığını is_t0/is_t1 ile doğrulayın.
Hata:   is_t2 True iken is_t1 False olamaz; hiyerarşi sıkı içermedir.
Bkz.:   Bölüm 4 (topoloji), Bölüm 7 (kompakt Hausdorff → normal).
Yansıma: T2 (Hausdorff) neden önemli? Hangi ispatlarda özellikle kullanılır?
```

### ch07 — Kompaktlık

```
Neden:  Kompaktlık sonlu uzaylarda otomatik doğru; sonsuz uzaylarda
        ince bir topik — Heine-Borel ve Tychonoff buradan gelir.
Keşif:  real_line_metric() ve closed_unit_interval_metric() için
        is_compact çıktısını karşılaştırın.
Hata:   Sonlu uzay her zaman kompakttır; finite_chain_space için
        is_compact her zaman True döner.
Bkz.:   Bölüm 6 (kompakt + Hausdorff → normal), Bölüm 10 (kompakt
        görüntü kompakttır).
Yansıma: ℝ kompakt değil ama [0,1] kompakt — fark nerede?
```

### ch08 — Bağlantılılık

```
Neden:  Bağlantılılık ve yol-bağlantılılık aynı kavram değildir;
        pytop ikisini ayrı ayrı test eder.
Keşif:  Sierpiński is_connected mi? Cevabınızı tahmin edin, sonra test edin.
Hata:   Yol-bağlantılı ⟹ Bağlantılı, ama tersi yanlış; is_path_connected
        True iken is_connected False olamaz.
Bkz.:   Bölüm 10 (sürekli görüntü bağlantılıdır).
Yansıma: Ayrık topoloji neden bağlantısızdır?
```

### ch09 — Sayılabilirlik Aksiyomları

```
Neden:  1. ve 2. sayılabilirlik aksiyomları analizin temel araçları;
        metrik uzaylar her ikisini de sağlar.
Keşif:  discrete_topology(0,1,2) için is_first_countable ve is_second_countable
        sonuçlarını karşılaştırın.
Hata:   2. sayılabilirlik ⟹ 1. sayılabilirlik; 1. için True, 2. için False
        mümkündür ama tersi mümkün değil.
Bkz.:   Bölüm 7 (Lindelöf ↔ 2. sayılabilir + T3).
Yansıma: Metrik uzay neden her zaman 1. sayılabilirdir?
```

### ch10 — Sürekli Fonksiyonlar

```
Neden:  Süreklilik topolojinin temel kavramı; homeomorfizma yapı-koruma
        denkliğidir.
Keşif:  Sierpiński → Sierpiński'ye kaç fonksiyon var, kaçı sürekli?
        is_continuous_finite_map ile tek tek test edin.
Hata:   s_topo = list(s.topology) kullanın; [set(u) for u in s.topology]
        gerekmez — is_continuous_finite_map Iterable[Iterable] kabul eder.
Bkz.:   Bölüm 7 (kompakt görüntü kompakt), Bölüm 8 (bağlantılı görüntü
        bağlantılı).
Yansıma: Homeomorfizma ile izomorfizma arasındaki fark ne? Hangi yapıyı korur?
```

### ch11 — Alt-uzay, Çarpım, Bölüm

```
Neden:  Yeni uzay inşa etmenin üç temel yöntemi; çarpım topolojisi
        Tychonoff teoreminin temelidir.
Keşif:  subspace_topology ile product_topology'nin boyutunu karşılaştırın.
Hata:   Çarpım topolojisi ince topolojidir; {U×V} ailesi baz, topoloji değil.
Bkz.:   Bölüm 7 (Tychonoff), Bölüm 12 (bölüm = eşdeğerlikten gelen topoloji).
Yansıma: Alt-uzay topolojisi orijinal topolojiden neden daha az açık küme içerebilir?
```

### ch12 — Bölüm Topolojisi

```
Neden:  Eşdeğerlik bağıntısından yeni uzay üretmek; daire S¹ ve torus
        bu şekilde inşa edilir.
Keşif:  quotient_set ile equivalence_class çıktılarını karşılaştırın:
        hangisi hangi bilgiyi taşır?
Hata:   quotient_set denklik bağıntısı gerektirir; rastgele bağıntı
        RelationError fırlatır.
Bkz.:   Bölüm 3 (partition_from_equivalence), Bölüm 11 (bölüm topolojisi inşası).
Yansıma: S¹ = [0,1] / {0~1} yapısını küçük bir taşıyıcı üzerinde modelleyebilir misiniz?
```

### ch13 — İlk ve Son Topoloji

```
Neden:  İlk topoloji (en kaba), son topoloji (en ince) — süreklilik
        koşulunu minimize eden ve maksimize eden ekstremler.
Keşif:  initial_topology ile final_topology'nin boyutunu karşılaştırın;
        hangisi daha büyük?
Hata:   İlk topoloji çekime göre en küçük, son topoloji itmeye göre en büyük
        topolojidir; karıştırmayın.
Bkz.:   Bölüm 10 (süreklilik), Bölüm 11 (çarpım = fonksiyon ailesine göre ilk).
Yansıma: Çarpım topolojisi neden ilk topolojiye özel bir örnektir?
```

### ch14 — Metrik Uzaylar

```
Neden:  Metrik uzaylar topolojik uzayların en somut alt sınıfı;
        ℝⁿ ve Hilbert uzayları burada yaşar.
Keşif:  real_line_metric() için is_t2 ve is_metrizable sonuçlarını kontrol edin.
Hata:   Her metrik uzay T4 (normal Hausdorff); is_t2 False dönerse metrik
        tanımında hata var demektir.
Bkz.:   Bölüm 9 (metrik ⟹ 2. sayılabilir iff ayrılabilir).
Yansıma: Metrik topoloji ne zaman ayrık topolojiyle çakışır?
```

### ch15 — Metrik Tamlık

```
Neden:  Cauchy dizileri tamlık için gerekli; tam olmayan uzaylarda
        yakınsama "dışarı kaçar".
Keşif:  closed_unit_interval_metric() ve real_line_metric() için
        is_complete sonuçlarını karşılaştırın.
Hata:   Tamlık topolojik özellik değildir; (0,1) ~ ℝ homeomorf ama
        biri tam diğeri değil.
Bkz.:   Bölüm 14 (metrik uzay tanımı), Bölüm 7 (kompakt metrik ⟹ tam).
Yansıma: Baire kategorisi teoremi neden tam metrik uzaylar için geçerli?
```

### ch16 — Metrik Dönüşümler

```
Neden:  Büzülme dönüşümleri (contraction) ve Lipschitz koşulları
        sabit nokta teoremlerinin temelidir.
Keşif:  Banach sabit nokta teoremini küçük tam metrik uzayda verify edin.
Hata:   Uniform süreklilik süreklilikten güçlüdür; uniform True iken
        continuous False olamaz ama tersi mümkün.
Bkz.:   Bölüm 10 (süreklilik), Bölüm 15 (tamlık — Banach için gerekli).
Yansıma: Lipschitz sabiti neden < 1 olmalı Banach için?
```

---

### Uygulama Adımları (Task 3)

- [ ] **ch03 maarif blokları** — 3 formatta ekle (Task 2 ile birleştirilebilir)
- [ ] **ch07 maarif blokları** — 3 formatta ekle
- [ ] **ch10 maarif blokları** — 3 formatta ekle (Task 1 ile birleştirilebilir)
- [ ] **ch01 maarif blokları** — 3 formatta ekle
- [ ] **ch04 maarif blokları** — 3 formatta ekle
- [ ] **ch05 maarif blokları** — 3 formatta ekle
- [ ] **ch06 maarif blokları** — 3 formatta ekle
- [ ] **ch08 maarif blokları** — 3 formatta ekle
- [ ] **ch09 maarif blokları** — 3 formatta ekle
- [ ] **ch11 maarif blokları** — 3 formatta ekle
- [ ] **ch12 maarif blokları** — 3 formatta ekle
- [ ] **ch13 maarif blokları** — 3 formatta ekle
- [ ] **ch14 maarif blokları** — 3 formatta ekle
- [ ] **ch15 maarif blokları** — 3 formatta ekle
- [ ] **ch16 maarif blokları** — 3 formatta ekle
- [ ] **ch02 maarif blokları** — 3 formatta ekle

- [ ] **Tek commit (Task 3 için)**
```bash
git add docs/user_guide/
git commit -m "docs: tüm bölümlere maarif pedagojik blokları (motivasyon/keşif/hata/köprü/yansıma)"
```

---

## Çalıştırma Sırası

1. Task 1 → Task 2 → Task 3 (bağımlılık yok, paralel yapılabilir ancak commit sırası bu şekilde)
2. Her Task sonunda ilgili commit.
3. Task 3 tek commit'te veya bölüm bölüm commit'lenebilir.
