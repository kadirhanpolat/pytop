# Continuity map taxonomy

This note isolates the Chapter 06 map classes that are easy to blur together during early topology study.
The point is not to maximize abstraction but to keep the distinctions visible with a compact set of reusable examples.

## Core distinction table

| Map behavior | What is checked | Typical warning-line |
| --- | --- | --- |
| continuous | inverse images of open sets are open | says nothing by itself about images of open sets |
| open | images of open sets are open | does not imply continuity |
| closed | images of closed sets are closed | does not imply continuity |
| homeomorphism | bijective, continuous, and inverse continuous | continuous bijection alone is not enough |

## Reusable examples

### 1. Continuous but not open
- Real example: $f:\mathbb{R}\to\mathbb{R}$, $f(x)=x^2$.
- Finite analogue: the identity map from a discrete topology to an indiscrete topology is continuous, but it is not open.

### 2. Open but not continuous
- Finite analogue: the identity map from an indiscrete topology to a discrete topology is open, but it is not continuous.
- Pedagogical use: this is the cleanest way to break the false implication “open map => continuous map”.

### 3. Closed but not open
- Real example: the inclusion $[0,\infty)\hookrightarrow \mathbb{R}$ is closed but not open.
- Classroom use: pair this with the previous line so students stop treating “open” and “closed” as mirror notions for maps.

### 4. Continuous bijection but not homeomorphism
- Canonical finite example: the identity map $\operatorname{id}:(X,\tau_d)\to(X,\tau_i)$ from the discrete topology to the indiscrete topology.
- Why it matters: the inverse map fails to be continuous.

### 5. Sequentially continuous need not mean continuous
- Warning-line example: on cocountable spaces, sequence tests can become too weak.
- Pedagogical rule: whenever the space is not first countable, do not replace the open-set definition by a sequence-only shortcut without an explicit theorem.

## Suggested classroom sequence
1. start with a two-column table: “what is pulled back?” vs “what is pushed forward?”
2. use the two identity maps between discrete and indiscrete topologies before moving to the real-line examples,
3. only after the distinction is stable, introduce the homeomorphism criteria,
4. end with the sequential warning-line so students do not overgeneralize metric intuition.

## v1.0.114 countability-adjacent warning note

Bu dosya doğrudan Chapter 06 map-class ayrımlarını taşısa da, Chapter 12--16 hattı için şu ek uyarı korunmalıdır:

- **Sequential language is not automatically global topology language.**
- ``dizisel süreklilik'' ve ``dizilerle kapanış okuma'' ancak uygun countability güvenliği altında tam öğretici araç olur.

### Cross-corridor reading rule

- **Chapter 06**: inverse-image tanımı birincil dildir.
- **Chapter 12**: birinci sayılabilirlik varsa sequence test güvenli hale gelir.
- **Chapter 16**: sequence-based techniques genişletilir, ama bu genişleme yine Chapter 12 güvenlik notuna geri bağlanmalıdır.

Böylece öğrenci, metric intuition ile general-topology caution arasındaki sınırı daha erken ve daha dürüst görür.

## v1.0.272 ayrım matrisi iskeleti

Bu bölüm, Chapter 07--15 entegrasyon hattının examples bank aşamasında kullanılacak küçük bir ayrım matrisi iskeletidir. Amaç yeni teorem kanıtı vermek değil; süreklilik, açık dönüşüm, kapalı dönüşüm ve özdeşbiçimlilik kavramlarının hangi yönden denetlendiğini görünür tutmaktır.

### Map-class decision matrix

| Sınıf | Birincil denetim | Girdi verisi | Beklenen tanık | Tipik yanlış genelleme | Uygun örnek kaynağı |
| --- | --- | --- | --- | --- | --- |
| Continuous map | Her açık kümenin ters görüntüsü açık mı? | Domain/codomain topolojileri ve fonksiyon | Ters görüntü hesabı veya başarısız açık küme | ``Görüntüler açık olmalı'' sanmak | Discrete-to-indiscrete identity; polynomial maps |
| Open map | Domain'deki her açık kümenin görüntüsü açık mı? | Domain açıkları ve fonksiyon görüntüleri | Açık görüntü hesabı veya karşıörnek | ``Open map continuous olur'' sanmak | Indiscrete-to-discrete finite identity; projections |
| Closed map | Domain'deki her kapalı kümenin görüntüsü kapalı mı? | Kapalı kümeler ve fonksiyon görüntüleri | Kapalı görüntü hesabı veya karşıörnek | ``Closed map open map gibidir'' sanmak | Inclusions; quotient-style warnings |
| Homeomorphism | Sürekli bijeksiyon ve sürekli ters var mı? | İki yönlü fonksiyon davranışı | Fonksiyon + ters fonksiyon sürekliliği | ``Continuous bijection yeterlidir'' sanmak | Discrete/indiscrete finite identity contrast |
| Sequential shortcut | Dizi davranışı topolojiyi yakalıyor mu? | Countability güvenliği | Birinci sayılabilirlik veya karşıuyarı | ``Diziler her uzayda yeterlidir'' sanmak | Cocountable/counterexample bank |

### Üretilecek özgün örnek kartı şablonu

Her örnek kartı aşağıdaki kısa alanlarla tutulmalıdır:

1. **Amaç:** Hangi yanlış çıkarımı engelliyor?
2. **Uzay/veri:** Domain, codomain, topolojiler ve fonksiyon.
3. **Pozitif özellik:** Hangi map-class özelliği sağlanıyor?
4. **Negatif tanık:** Hangi özellik neden sağlanmıyor?
5. **Öğretim notu:** Bu örnek hangi chapter köprüsüne bağlanıyor?
6. **Özgünlük notu:** Dış notlardan doğrudan örnek/metin alınmadı; örnek ya standart kavram ailesinden yeniden formüle edildi ya da finite model olarak yeniden kuruldu.

### Entegrasyon sınırı

- Bu dosya çalışan soru üreticisi değildir.
- Bu dosya API sözleşmesi değildir.
- Bu dosya Chapter 07 problem aileleri için yalnızca examples bank taslağıdır.
- Kod entegrasyonu, ileride questionbank sözleşmeleri tamamlandıktan sonra yapılmalıdır.
