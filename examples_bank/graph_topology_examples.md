# Topolojik Graf Profilleri -- GTOP-01

- Surum: `v0.2.400`
- Rota: `GTOP-01`
- Kaynak odagi: Adams & Franzosa Bolum 13.1
- Paket yuzeyi: `src/pytop/graph_topology.py`

## Vertex ve edge okumasi

`interval_graph_arc` profili, iki vertex ve tek edge iceren en kucuk baglantili
graf modelidir. Bu kayit, graflari 1-boyutlu hucre kompleksleri gibi okumaya
baslamak icin kullanilir.

## Cevrim grafi

`cycle_graph_circle` profili, kapali poligonal cevrimi cemberin graf modeli
olarak sunar. Vertex ve edge sayilari esit oldugundan Euler karakteristigi
`0` olarak kaydedilir.

## Theta grafi

`theta_graph` profili, iki vertex arasinda uc edge yolu tasir. Bu model,
birden fazla cevrim iceren baglantili graflarda Euler karakteristigi sinyalinin
nasil degistigini gostermek icin eklenmistir.

## Gomulme profilleri

`cycle_graph_plane_embedding` ve `theta_graph_plane_embedding`, duzlem
gomulmelerinde yuz sayimi ve V-E+F kontrolunun nasil okunacagini gosterir.
`interval_graph_line_embedding`, her gomulmenin yuz sayimi gerektirmedigini
hatirlatan daha temel bir dogru parcasi modelidir.

## Kullanim notu

Bu dosya planarity veya Kuratowski teoremi icin tam bir algoritma sunmaz.
GTOP-01 yalnizca Bolum 13.1 icin topolojik graf ve gomulme profil yuzeyini acar;
planarity ve kimyasal graf profilleri sonraki GTOP surumlerinin konusudur.
