# Dugum Teorisi Temel Ornekleri -- KNOT-01

- Surum: `v0.2.300`
- Hat: `KNOT-01`
- Kaynak odagi: Adams & Franzosa Bolum 12.1--12.2
- Dil ilkesi: Bu dosya Turkcedir; Python API adlari paket standardi geregi
  Ingilizce tutulmustur.

## 1. Dugum Teorisi Neyi Modeller?

Dugum teorisinde ana nesne, uc boyutlu uzayda kapali bir egrinin nasil
dolanmis oldugudur. Bir dugum diyagrami bu kapali egrinin duzleme
izdusumudur; kesisimlerde hangi ipin ustten, hangisinin alttan gectigi
ayrica kaydedilir.

KNOT-01 bu kurami hesaplamali bir siniflandirma motoru olarak degil, kitap
kaynakli ogretim profilleri olarak acar. Paket icindeki temel soru sudur:

```text
Bu diyagram hangi ogretim rolunu oynuyor?
```

## 2. Cozuk Dugum, Trefoil ve Sekiz Dugumu

Cozuk dugum kesisimsiz kapali halka modelidir. Trefoil, en kucuk klasik
cozuk-olmayan dugum ornegidir ve uc kesisimli standart diyagramla tanitilir.
Sekiz dugumu ise dort kesisimli kontrast modelidir; trefoil sonrasi
katalogun dogal ikinci adimidir.

Bu uc profil, ogrenciye ayni anda iki ayrimi gosterir:

- kapali egrinin varligi tek basina dolaniklik demek degildir,
- kesisim sayisi diyagram okumasinda onemli ama tek basina tam siniflandirma
  degildir.

## 3. Linke Gecis

Link, birden fazla kapali bilesenden olusur. Iki cozuk halkanin ayrik durmasi
cozuk link profilini verir. Hopf link ise her bilesen tek basina cozuk olsa
bile iki bilesenin birlikte ayrilamaz okunabilecegini gosterir.

Bu gecis, sonraki KNOT-02 hattinda baglanti sayisi ve dugum degismezleri icin
zemin hazirlar.

## 4. Reidemeister Hamleleri

Reidemeister hamleleri, ayni dugum tipini veren diyagramlar arasindaki yerel
donusumleri paketler:

```text
R1: tek bukle ekleme veya kaldirma
R2: iki karsit kesisimi birlikte ekleme veya kaldirma
R3: uc ip parcasi arasinda yerel gecis siralamasi kaydirma
```

Bu hamleler dugum tipini korur. Bu nedenle KNOT-01 profil yuzeyi,
Reidemeister hamlelerini "diyagram degisir, dugum tipi korunur" uyarisiyle
kaydeder.

## 5. Paket Baglantisi

Bu ornek dosyasi su modulle birlikte okunmalidir:

```text
src/pytop/knots.py
```

KNOT-01, `v0.2.300` ile dugum teorisi fazini acar. Sonraki planli adim
`v0.2.301 -- Dugum degismezleri -- baglanti sayisi ve polinomlar / KNOT-02`
olarak tutulur.
