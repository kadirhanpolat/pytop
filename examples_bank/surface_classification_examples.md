# Euler Karakteristigi ve Yuzey Siniflandirmasi -- MAN-01

- Surum: `v0.2.500`
- Rota: `MAN-01`
- Kaynak odagi: Adams & Franzosa Bolum 14.2
- Paket yuzeyi: `src/pytop/surface_classification.py`

## Orientable aile

`sphere_surface`, `torus_surface` ve `double_torus_surface` profilleri kompakt
orientable yuzey ailesini Euler karakteristigi ile birlikte kaydeder. Kure icin
deger `2`, torus icin `0`, iki kulplu yuzey icin `-2` olarak tutulur.

## Nonorientable aile

`projective_plane_surface` ve `klein_bottle_surface`, nonorientable yuzey
ailesinin ilk iki klasik modelidir. Klein sisesi ile torus ayni Euler
karakteristigine sahip olsa da orientability verisiyle ayrilir.

## Siniflandirma sinyali

MAN-01 profilleri, kompakt yuzey siniflandirmasinda Euler karakteristigi,
orientability ve genus/crosscap sayisinin birlikte okunmasi gerektigini
vurgular. Bu kayitlar bir homeomorfizma motoru degildir; kitap hattindaki
siniflandirma dilini paket API'sine tasir.
