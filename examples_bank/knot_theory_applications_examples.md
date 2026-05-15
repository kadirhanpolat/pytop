# Dugum Teorisi Uygulamalari -- KNOT-03

- Surum: `v0.2.302`
- Rota: `KNOT-03`
- Kaynak odagi: Adams & Franzosa Bolum 12.4
- Paket yuzeyi: `src/pytop/knots.py`

## DNA topology

DNA supercoiling ornegi, dugum teorisini kapali DNA halkalari ve dolanma
bilgisi uzerinden okur. `dna_supercoiling_topology` profili, biyolojik bir
durumun yalnizca geometrik sekille degil topolojik sinyalle de izlenebilecegini
vurgular.

## Topoizomeraz uyarisi

`topoisomerase_strand_passage` profili, topoizomeraz etkisini Reidemeister
hamleleriyle karistirmamak icin eklenmistir. Reidemeister hamleleri diyagram
tipini koruyan yerel esdegerliklerdir; topoizomeraz ise biyolojik surecte iplik
gecisi yaparak dugum veya link tipini degistirebilir.

## Kimyasal kiralite

`synthetic_chemistry_chiral_knots` profili, sag ve sol elli trefoil benzeri
molekuler dugumleri kiralite anlatimina baglar. Ayna goruntusuyle cakismayan
dugumlu molekuller, kimyasal sentez ve ayirt etme sorularinda topolojik bir dil
saglar.

## Molekuler link tespiti

`molecular_link_detection` profili, KNOT-02 degismezlerini uygulamaya baglar.
Baglanti sayisi ve polinom profilleri, molekuler halkalarin ayrilabilir mi
yoksa linkli mi oldugunu ogretim duzeyinde isaretlemek icin kullanilir.

## Kullanim notu

Bu dosya hesaplama motoru degildir. KNOT-03 amaci, kitap hattindaki DNA ve kimya
uygulamalarini denetlenebilir profil kayitlarina cevirerek sonraki topolojik
cizge fazina temiz bir gecis birakmaktir.
