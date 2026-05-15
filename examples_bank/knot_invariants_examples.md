# Dugum Degismezleri Ornekleri -- KNOT-02

- Surum: `v0.2.301`
- Hat: `KNOT-02`
- Kaynak odagi: Adams & Franzosa Bolum 12.3
- Dil ilkesi: Bu dosya Turkcedir; Python API adlari paket standardi geregi
  Ingilizce tutulmustur.

## 1. Degismez Nedir?

Bir dugum degismezi, Reidemeister hamleleriyle degistirilen diyagramlarda ayni
kalan bilgidir. Diyagramin gorunusu degisebilir; fakat degismez ayni kaldigi
icin dugum veya link tipini karsilastirmada guvenilir bir isaret verir.

KNOT-02 hesaplama motoru kurmaz. Bunun yerine baglanti sayisi, Alexander
polinomu ve Jones polinomu icin sembolik ogretim kayitlari ekler.

## 2. Baglanti Sayisi

Baglanti sayisi iki bilesenli yonlu linklerde kullanilan sayisal bir
degismezdir. Iki cozuk halkanin ayrik durdugu cozuk link icin deger `0`
okunur. Hopf link icin deger yon secimine bagli olarak `+1` veya `-1`
sembolik sinyaliyle kaydedilir.

Bu ayrim, her bilesen tek basina cozuk olsa bile iki bilesenin birlikte
dolanik olabilecegini gosterir.

## 3. Alexander Polinomu

Alexander polinomu, dugum teorisinin klasik cebirsel degismezlerinden biridir.
KNOT-02 yuzeyi cozuk dugum icin `1`, trefoil icin ise ogretim amacli simetrik
normalizasyonla `t^-1 - 1 + t` kaydini tasir.

Bu kayitlar, polinomlarin dogrudan tam siniflandirma yapmadigini ama dugumleri
ayirt etmek icin guclu bir profil sundugunu vurgular.

## 4. Jones Polinomu

Jones polinomu skein iliskileri ve ayna davranisi uzerinden daha ileri bir
cebirsel pencere acar. KNOT-02, cozuk dugum icin `1`, trefoil icin sembolik
`q^-1 + q^-3 - q^-4` kaydini tutar.

Farkli kaynaklarda degisken ve normalizasyon secimleri degisebilir. Bu nedenle
paket degeri hesaplanmis nihai otorite olarak degil, ogretim profili olarak
sunulur.

## 5. Paket Baglantisi

Bu ornek dosyasi su modul yuzeyiyle birlikte okunmalidir:

```text
src/pytop/knots.py
```

KNOT-02, `KnotInvariantProfile` kayitlarini KNOT-01 dugum ve link profilleri
uzerine yerlestirir. Sonraki planli adim `v0.2.302 -- Dugum teorisi
uygulamalari -- DNA ve kimya / KNOT-03` olarak tutulur.
