# Derece Teorisi Uygulamaları -- DEG-02

- Sürüm: `v0.2.201`
- Hat: `DEG-02`
- Kaynak odağı: Adams & Franzosa Bölüm 9.3--9.4
- Dil ilkesi: Bu uygulama notu Türkçedir; Python API adları paket standardı
  gereği İngilizce tutulmuştur.

## 1. Cebirin Temel Teoremi: Topolojik Kanıt Fikri

Cebirin temel teoremi, sabit olmayan her karmaşık polinomun en az bir karmaşık
kökü olduğunu söyler. Derece teorisi bu sonucu, kökü doğrudan hesaplamadan,
sınırdaki sarma davranışını izleyerek açıklar.

Monik bir polinom düşünelim:

```text
p(z) = z^n + a_{n-1}z^{n-1} + ... + a_0
```

Yarıçapı yeterince büyük bir çember üzerinde `z^n` terimi baskındır. Bu yüzden
`p(z)` haritasının çember üzerindeki normalize edilmiş görüntüsü, `z^n`
haritasıyla aynı dereceyi taşır: derece `n`.

Eğer `p` hiç kök taşımasaydı, `p(z) / |p(z)|` normalize haritası yalnızca sınırda
değil, diskin tamamında tanımlı olurdu. Sınır haritası diske uzadığı için
derecesi `0` olmak zorunda kalırdı. Ama sınırda derece `n` görülür. `n >= 1`
olduğundan çelişki elde edilir. Bu çelişki, polinomun en az bir kökü olduğunu
gösterir.

Öğretim mesajı şudur: derece, sınırdaki sarma sayısını korur; sarma sayısı
pozitifse içeride sıfır olmadan bu sarım yok edilemez.

## 2. Doğrusal Model: Sarma Sayısını Gözle Görmek

`p(z) = z - a` doğrusal polinomu için büyük bir disk seçelim ve `a` noktası bu
diskin içinde kalsın. Diskin sınırında `p(z)`, orijin etrafında bir kez döner.
Normalize harita derece `1` taşır.

İçeride kök olmasaydı aynı normalize harita diske uzardı ve derecesi `0`
olurdu. Oysa sınırdaki derece `1`dir. Bu en küçük örnek, genel kanıttaki
mantığı görünür hale getirir.

## 3. Kalp Atışı Modeli: Faz Çemberi ve Derece

Periyodik bir biyolojik döngü, özellikle kalp atışı gibi ritmik süreçler, faz
çemberi üzerinde modellenebilir. Çemberin her noktası döngü içindeki bir fazı
temsil eder. Bir atımdan sonraki fazı veren geri dönüş haritası, kabaca
`S^1 -> S^1` türünde bir harita gibi okunur.

Düzenli bir ritimde bu harita çemberi çember etrafında bir kez dolaştırır. Bu
durum derece `1` sinyaliyle anlatılır. Bu, tıbbi tanı anlamına gelmez; topolojik
olarak döngünün kaybolmadığını ve modelin faz yapısını koruduğunu söyleyen
öğretim amaçlı bir özettir.

## 4. Ritim Bozulması İçin Kontrast

Küçük ve sürekli bozulmalar faz haritasının temel sarma sayısını değiştirmez.
Bu, derece değişmezliğinin biyolojik modeldeki sezgisel karşılığıdır. Büyük
bozulmalarda ise modelin varsayımları yeniden denetlenmelidir: faz çemberi hâlâ
uygun mu, geri dönüş haritası sürekliliğini koruyor mu, ölçülen sinyal gerçekten
tek döngüye mi karşılık geliyor?

Bu ayrım, DEG-02'nin ana öğretim katkısıdır: derece sayısal bir ritim ölçümü
değil, döngüsel yapının topolojik korunma işaretidir.

## 5. Paket Bağlantısı

Bu örnek dosyası şu modülle birlikte okunmalıdır:

```text
src/pytop/degree_theory_applications.py
```

DEG-02, DEG-01'deki `src/pytop/degree_theory.py` yüzeyini kullanarak uygulama
katmanını açar. Sonraki planlı adım `v0.2.202 -- EMB-01` hattıdır.
