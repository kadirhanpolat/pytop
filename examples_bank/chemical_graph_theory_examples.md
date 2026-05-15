# Kimyasal Graf Teorisi ve Planarity -- GTOP-02/GTOP-03

- Surum: `v0.2.500`
- Kapsanan ara rotalar: `GTOP-02`, `GTOP-03`
- Kaynak odagi: Adams & Franzosa Bolum 13.2--13.4
- Paket yuzeyi: `src/pytop/graph_topology.py`

## Planarity engelleri

`k5_nonplanar_profile` ve `k33_nonplanar_profile`, Kuratowski hattindaki iki
temel engel modelini kaydeder. Bu profiller algoritmik planarity karari vermez;
duzlemde kesisimsiz gomulmenin hangi klasik modellerde engellendigini ogretim
dilinde gorunur kilar.

## Kimyasal graf modeli

`benzene_cycle_graph`, atomlari vertex ve kimyasal baglari edge olarak okur.
`isomer_graph_distinction`, ayni atom sayisinin farkli baglanma graflari
uretebilecegini vurgular. Bu, kimyasal izomer ayrimini graf topolojisiyle
konusmak icin kucuk bir kayit yuzeyidir.

## Gecis sayisi ve kalinlik

`k5_crossing_thickness_signal`, planarity engelinden sonra gecis sayisi ve
kalinlik sorularinin neden dogal hale geldigini aciklar.
`molecular_bond_graph_crossing_warning`, kimyasal cizimlerde gorulen gecislerin
her zaman fiziksel bag kesisimi anlamina gelmedigini hatirlatir.

## Kullanim notu

GTOP-02/03 kayitlari, kimyasal graf teorisi ve planarity dilini paketin
denetlenebilir profil modeline tasir. Tam planarity algoritmasi veya molekuler
geometri motoru degildir.
