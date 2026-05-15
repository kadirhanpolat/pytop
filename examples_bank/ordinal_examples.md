# Ordinal examples

Bu dosya, Cilt II Bölüm 27 için sıra sayısı örneklerini toplar.

## Çekirdek örnekler

- sonlu ordinals: düzen tipi fikrinin ilk laboratuvarı
- \(\omega\): ilk sonsuz ordinal
- \(\omega+1\): aynı kardinal büyüklükte ama farklı düzen tipi
- limit ordinals: ardıl olmayan büyüme şeması

## Ana vurgu

Bu dosyanın temel pedagojik işlevi, kardinal sayı ile ordinal sayı arasındaki farkı tek cümlelik soyut tanımla bırakmamaktır. Özellikle `\omega` ve `\omega+1` karşılaştırması, “aynı büyüklük, farklı sıra tipi” mesajını görünür kılmak için merkezdedir.

## v0.6.18 notebook bridge

Bu dosya artık `notebooks/exploration/16_ordinals.ipynb` ile birlikte düşünülmelidir. Özellikle `\omega`, `\omega+1` ve `1+\omega` karşılaştırması notebook tarafında görünür kılınmıştır.


## Worksheet / notebook companions

- worksheet: `manuscript/volume_2/worksheets/03b_ordinals.md`
- quick check: `manuscript/volume_2/quick_checks/03b_ordinals.tex`
- teaching companion: `notebooks/teaching/lesson_10c_ordinals.ipynb`
- exploration companion: `notebooks/exploration/16_ordinals.ipynb`

## v1.0.49 teaching split note

Bu örnek bankası artık yalnız exploration not defteriyle değil, Chapter 27 için açılan dedicated worksheet / quick-check / teaching companion hattıyla birlikte okunmalıdır. Özellikle `\omega`, `\omega+1` ve `1+\omega` örnekleri artık doğrudan sınıf içi yazılı görev bandına da beslenmektedir.

---

## v0.1.66 — pytop API örnek ailesi (OR-01 … OR-06)

Bu bölüm, `ordinal_numbers.py` modülünün durable public API'sini gösteren çekirdek örnek kimliklerini tanımlar.

### OR-01 — Sonlu sıra sayısı: n düzen tipi

**Uzay:** `make_finite(4)` — 4 noktalı uzay  
**Beklenti:** `ordinal_class` → `"finite_ordinal"`, mod `"exact"`, etiket `"4"`, `successor_limit_class` → `"successor"`.  
**Pedagojik kullanım:** Sonlu sıra sayılarında kardinal ve ordinal çakışır; sonsuz durumda bu çakışma bozulur.

### OR-02 — omega: ilk sonsuz sıra sayısı

**Uzay:** `_Tagged(tags=["omega"])`  
**Beklenti:** `ordinal_class` → `"omega"`, `successor_limit_class` → `"limit"`, `cf(omega) = omega`.  
**Pedagojik kullanım:** Dizilerle yakalanan yakınsama fikrinin ordinal altyapısı; `|omega| = |omega+1|` ama `omega ≠ omega+1` olarak sıra tipi.

### OR-03 — omega+1: ardıl sıra sayısı

**Uzay:** `_Tagged(tags=["omega_plus_1"])`  
**Beklenti:** `ordinal_class` → `"infinite_successor"`, `successor_limit_class` → `"successor"`.  
**Pedagojik kullanım:** Aynı kardinal büyüklük (ℵ₀) ama farklı sıra tipi; `cf(omega+1) = 1`.

### OR-04 — Limit sıra sayısı: genel durum

**Uzay:** `_Tagged(tags=["limit_ordinal"])`  
**Beklenti:** `ordinal_class` → `"infinite_limit"`, `successor_limit_class` → `"limit"`.  
**Pedagojik kullanım:** Limit adımının neden transfinit tümevarımda ayrı ele alınması gerektiğini gösterir.

### OR-05 — Sıra uzayı: topolojik kullanım

**Uzay:** `_Tagged(tags=["ordinal_space"])`  
**Beklenti:** `ordinal_class` → `"ordinal_space"`, topolojik köprü: `[0, omega_1)` sayılabilir kompakt ama kompakt değil.  
**Pedagojik kullanım:** Ordinal uzaylar, kompaktlık ve sayılabilir kompaktlık arasındaki farkın klasik karşı-örnek ailesidir.

### OR-06 — Aritmetik değişmezlik tanığı

**Beklenti:** Profil `arithmetic_note` anahtarı; `1 + omega = omega` ama `omega + 1 ≠ omega` ifadesini içermeli.  
**Pedagojik kullanım:** Ordinal aritmetiğin değişmez olmadığını gösteren çekirdek tanık çifti; uzun inşalarda sıra indekslerini doğru kurmak için kritik.
