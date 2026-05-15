# Cofinality and regularity examples

Bu dosya, Cilt II Bölüm 28 için kofinalite ve düzenlilik örneklerini toplar.

## Çekirdek örnekler

- \(\omega\): kofinalitesi sayılabilir olan temel düzenli örnek
- \(\omega_1\): sayılamaz kofinalite fikrinin ilk doğal modeli
- düzenli / tekil şemalar: bir kardinalin daha küçük ailelerle limitlenip limitlenemediği

## Pedagojik amaç

Bu örnekler, Bölüm 29--31 hattında kullanılan kardinal fonksiyon dilinin arkasındaki “hangi büyüklük nasıl yaklaşılıyor” sorusunu görünür kılar. Burada amaç ağır kümeler kuramı açmak değil, kofinalite sezgisini yeterince açık hale getirmektir.

## v0.6.18 notebook bridge

Bu dosya artık `notebooks/exploration/17_cofinality_and_regularity.ipynb` için ana örnek desteğidir. Düzenli/tekil ayrımı ve eşyönlülük sezgisi küçük tablo ve görevlerle notebook tarafına taşınmıştır.


## Worksheet / notebook companions

- worksheet: `manuscript/volume_2/worksheets/03c_cofinality_regularity.md`
- quick check: `manuscript/volume_2/quick_checks/03c_cofinality_regularity.tex`
- teaching companion: `notebooks/teaching/lesson_10d_cofinality_and_regularity.ipynb`
- exploration companion: `notebooks/exploration/17_cofinality_and_regularity.ipynb`

## v1.0.50 teaching split note

Bu örnek bankası artık yalnız exploration not defteriyle değil, Chapter 28 için açılan dedicated worksheet / quick-check / teaching companion hattıyla birlikte okunmalıdır. Özellikle `\omega`, `\omega+1`, düzenli `\kappa` ve tekil `\kappa` örnekleri artık doğrudan sınıf içi yazılı görev bandına da beslenmektedir.

---

## v0.1.67 — pytop API örnek ailesi (CF-01 … CF-06)

Bu bölüm, `cofinality.py` modülünün durable public API'sini gösteren çekirdek örnek kimliklerini tanımlar.

### CF-01 — Sonlu ordinal: cf(n) = 1

**Uzay:** `make_finite(4)` — 4 noktalı uzay  
**Beklenti:** `cofinality_class` → `"finite"`, `regularity_status` → `"trivial"`, label içinde `"1"`.  
**Pedagojik kullanım:** Sonlu yapılarda kofinalite önemsizdir; ilginç davranış sonsuz limit yapılarda başlar.

### CF-02 — omega: cf(ω) = ω (düzenli)

**Uzay:** `_Tagged(tags=["omega"])`  
**Beklenti:** `cofinality_class` → `"omega_regular"`, `regularity_status` → `"regular"`.  
**Pedagojik kullanım:** Dizilerle yakınsama fikrinin kofinalite altyapısı; hiçbir sonlu altküme ω içinde eşyönlü değildir.

### CF-03 — omega_1: cf(ω₁) = ω₁ (sayılamaz düzenli)

**Uzay:** `_Tagged(tags=["omega_1"])`  
**Beklenti:** `cofinality_class` → `"uncountable_regular"`, `regularity_status` → `"regular"`.  
**Pedagojik kullanım:** `[0, ω₁)` sayılabilir kompakttır çünkü `cf(ω₁) = ω₁ > ω`; sayılabilir bir eşyönlü altküme yoktur.

### CF-04 — Tekil kardinal: cf(ω_ω) = ω

**Uzay:** `_Tagged(tags=["omega_omega"])`  
**Beklenti:** `cofinality_class` → `"singular"`, `regularity_status` → `"singular"`.  
**Pedagojik kullanım:** `[0, ω_ω)` sayılabilir kompakt değildir çünkü `cf(ω_ω) = ω`; ω uzunluğunda bir eşyönlü dizi vardır.

### CF-05 — Ardıl kardinal: her zaman düzenli

**Uzay:** `_Tagged(tags=["aleph_1"])`  
**Beklenti:** `cofinality_class` → `"successor_regular"`, `regularity_status` → `"regular"`.  
**Pedagojik kullanım:** Her ardıl kardinalin düzenli olduğunu gösteren kanonik örnek; `cf(κ⁺) = κ⁺`.

### CF-06 — König teoremi tanığı

**Beklenti:** Profil `key_theorems` listesi; König teoremini (`cf(2^κ) > κ`) ve  
`2^{ℵ₀} ≠ ℵ_ω` sonucunu içermeli.  
**Pedagojik kullanım:** Kofinalite kısıtının güç kümesi büyüklüklerini nasıl sınırladığını gösteren temel aritmetik tanık.
