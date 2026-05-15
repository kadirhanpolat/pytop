# Basic cardinal functions examples

Bu dosya, Cilt II Bolum 30 icin ornek ailelerini daha gorunur bicimde toplar.

## Agirlik `w(X)`

- `R`: rasyonel uclu araliklarla sayilabilir taban
- sayilabilir ayrik uzaylar
- indiscrete uzaylar: cok kucuk taban verisi

Mesaj: topolojinin zenginligi ile onu uretmeye yeten en kucuk tabanin buyuklugu farkli seylerdir.

## Yogunluk `d(X)`

- `Q` yogun altkume olarak `R` icinde
- sonsuz ayrik uzaylar: yogunluk tum kardinale esit
- cocountable tarzı ornekler: yogunluk sezgisinin dikkatle okunmasi gerekir

Mesaj: sayilabilir yogun altkume varligi ile kucuk taban verisi iliskili olsa da ozdes degildir.

## Karakter ve sozde karakter

- metrik uzaylar: sayilabilir yerel taban
- sonsuz ayrik uzaylar: her noktada cok kucuk yerel yapi
- acik kumelerin kesisimi ile nokta ayirma sezgisi

Mesaj: yerel kucukluk, global kucuklugu zorunlu kilmaz.

## Lindelof sayisi `L(X)`

- ikinci sayilabilir metrik uzaylar
- standart metrik uzaylar

Mesaj: ortu davranisi, taban davranisi ve yogunluk davranisi ayni motivasyon ailesine ait olsa da ayri niceliklerdir.

## Cellularity, spread, and network weight

- ayrik uzaylar
- ayrik nokta aileleri ile ayrik acik kume aileleri arasindaki karsilastirmalar
- `nw(X) <= w(X)` sezgisi

## Bolum 30 icin kisa kullanim ilkesi

Bu dosya tam karsi-ornek katalogu degildir. Amac, Bolum 30'da tanitilan fonksiyonlarin her biri icin en az bir olumlu model ve en az bir ayrim ureten model gostermektir.

## Notebook gorev eslesmesi

- `lesson_12_basic_cardinal_functions.ipynb`:
  - `w(X)`, `d(X)`, `chi(X)`, `L(X)`, `nw(X)` karsilastirma tablosu
  - kucuk karakter / buyuk agirlik uyarisini aciklayan ornek secimi
- `small_character_large_weight.ipynb`:
  - ayrik uzay ailesi uzerinden yerel-kuresel ayrimi gorunur kilma

## v0.1.75 comparison-route continuation

Chapter 30 now explicitly continues the same five durable comparison identifiers from the Chapter 29 framework corridor:

- `weight_vs_density`
- `character_vs_weight`
- `density_vs_cellularity_spread`
- `metric_second_countable_guard`
- `compactness_vs_small_cardinals`

In this file, these route IDs should be read as the slower example-side continuation of the shared worksheet and the `lesson_12_basic_cardinal_functions.ipynb` teaching notebook.
