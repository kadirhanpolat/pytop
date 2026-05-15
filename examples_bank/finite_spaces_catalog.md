# Sonlu uzaylar kataloğu

Bu dosya, Cilt I'in özellikle 17. bölümü için seçilmiş temel sonlu topolojik uzay örneklerini toplar.

## 1. Tek noktalı uzay

- Taşıyıcı: `{*}`
- Topoloji: `{\emptyset, \{*\}}`
- Rol: en küçük topolojik uzay, otomatik olarak ayrık, Hausdorff ve kompakt
- `pytop` bağlantısı: `singleton_space()`

## 2. İki noktalı ayrık uzay

- Taşıyıcı: `{a,b}`
- Topoloji: tüm alt kümeler
- Rol: sonlu `T_1` uzayların neden ayrıklaştığına ilk örnek
- `pytop` bağlantısı: `two_point_discrete_space()`

## 3. İki noktalı ayrık olmayan uzay

- Taşıyıcı: `{a,b}`
- Topoloji: `{\emptyset, \{a,b\}}`
- Rol: kompakt ama Hausdorff olmayan küçük örnek ailesine giriş
- `pytop` bağlantısı: `two_point_indiscrete_space()`

## 4. Sierpiński uzayı

- Taşıyıcı: `{0,1}`
- Topoloji: `{\emptyset, \{1\}, \{0,1\}}`
- Rol: `T_0` olup `T_1` olmayan temel örnek
- `pytop` bağlantısı: `sierpinski_space()`

## 5. Sonlu zincir uzayı

- Taşıyıcı: `{0,1,2,\dots,n}` gibi küçük zincirler
- Rol: özelleşme önsırası ve Aleksandrov topolojisi arasındaki köprü
- `pytop` bağlantısı: `finite_chain_space(n)`, `specialization_preorder(...)`

## 6. Özel açık küme ailesiyle verilen küçük uzaylar

- Rol: en küçük açık komşuluk, kapanış ve bağlılık davranışını doğrudan hesaplamak
- `pytop` bağlantısı: `FiniteTopologicalSpace(carrier=..., topology=...)`

## Kullanım notu

Bu dosya özellikle şu başlıklarla birlikte kullanılmalıdır:
- Chapter 03: küçük topoloji örnekleri
- Chapter 11: ayırma aksiyomları
- Chapter 14: kompaktlığın sonlu bağlamı
- Chapter 17: sonlu uzaylar ve özelleşme önsırası

Ayrıca `notebooks/exploration/08_alexandroff_spaces.ipynb` ve `notebooks/teaching/lesson_07_finite_spaces.ipynb` ile birlikte okunmalıdır.


## v1.0.183 stable finite-space catalog codes

Bu sürümde sonlu uzay örnekleri kararlı `FSE-*` kodlarıyla indekslendi. Ayrıntılı ve test edilebilir katalog için `examples_bank/finite_spaces_catalog_v1_0_183.md` ve `src/pytop_publish/finite_space_example_catalog.py` dosyalarına bakılmalıdır.

## v0.1.40 inşaat matrisi capstone notu

Bu katalog v0.1.40 ile Cilt I capstone bölümünün birincil örnek kaynağı olarak işaretlenmiştir. Katalogdaki her uzay, inşaat matrisi köprüsünün en az bir sütunuyla eşleşir:

- Tek noktalı uzay → altuzay ve bölüm uzayı limitlerinin sıfır noktası
- İki noktalı ayrık uzay → ayrık birleşim ve çarpım için temel bileşen
- Sierpiński uzayı → altuzay ve çarpım topolojilerinde T_0 davranışının referans noktası
- Sonlu zincir uzayları → özelleşme önsırası ve operatör tablosunun doğal laboratuvarı

Bu not, , , ,
 ve  ile birlikte okunmalıdır.
