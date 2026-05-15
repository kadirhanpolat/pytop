# Properties and cardinal-functions links examples

Bu dosya, Cilt II Bölüm 31 için nitel özellikler ile kardinal fonksiyon eşikleri arasındaki bağları örneklerle toplar.

## Temel eşik örnekleri

### \(\mathbb{R}\)
- ikinci sayılabilir,
- ayrılabilir,
- birinci sayılabilir,
- Lindelöf.

Dolayısıyla bu uzay, `w(X)`, `d(X)`, `\chi(X)` ve `L(X)` için sayılabilir eşiklerin aynı anda görülebildiği temel modeldir.

### Sonsuz ayrık metrik uzay
- birinci sayılabilir,
- metrik,
- ama çoğu durumda ikinci sayılabilir değildir.

**Mesaj:** küçük karakter, küçük ağırlık anlamına gelmez.

### \(\mathbb{Q}\subseteq \mathbb{R}\)
- sayılabilir yoğun altküme sezgisi
- ayrılabilirlik ile yoğunluk arasındaki bağın en temel laboratuvarı

### Cocountable topoloji örnekleri
- bazı nitel olumlu davranışlarla nicel küçüklüğün ayrışabileceğini hatırlatır.

## Bölüm içi kullanım önerileri

- ikinci sayılabilirlik \(\leftrightarrow\) ağırlık: \(\mathbb{R}\), rasyonel uçlu aralıklar
- ayrılabilirlik \(\leftrightarrow\) yoğunluk: \(\mathbb{Q}\) ve \(\mathbb{R}\)
- birinci sayılabilirlik \(\leftrightarrow\) karakter: metrik uzaylar, ayrık uzaylar
- Lindelöf \(\leftrightarrow\) Lindelöf sayısı: ikinci sayılabilir metrik uzaylar
- küçük karakter / büyük ağırlık ayrımı: sonsuz ayrık metrik uzay ailesi

## Pedagojik not

Bu bölümde amaç, ağır klasik eşitsizlikler kurmak değildir. Asıl amaç, Cilt I'de öğrenilen nitel kavramların kardinal fonksiyon diliyle nasıl yeniden yazıldığını görünür hale getirmektir. Bu nedenle bölüm yazımında örneklerin rolü, tam ispat yükü taşımaktan çok eşik sezgisi vermektir.

## Notebook görev eşleşmesi

- `lesson_13_properties_and_cardinal_functions.ipynb`:
  - sayılabilir eşik tablosunu standart uzaylarla eşleme
  - nitel özellikleri nicel cümlelere dönüştürme etkinliği
- `countable_threshold_failures.ipynb`:
  - `d(X)` küçükken `w(X)` büyük kalabilen örneklerin tartışılması
  - `chi(X)` küçükken küresel niceliklerin büyük kalabildiği uyarıların sınıflanması

## v0.1.41 Cilt II opening note

Bu dosya v0.1.41 ile Cilt II'nin özellik-değişmez köprüsünün örnek kaynağı olarak işaretlenmiştir. Özellik dili (bağlılık, kompaktlık, ayırma) ile cardinal function dili (ağırlık, yoğunluk, karakter) arasındaki bağ, bu dosyadaki örnekler üzerinden temel koruma tablosuyla eşleştirilmelidir.
