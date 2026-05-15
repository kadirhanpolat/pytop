# 3-Manifold Profil Modulu -- MAN-02

- Surum: `v0.2.501`
- Rota: `MAN-02`
- Kaynak odagi: Adams & Franzosa Bolum 14.3
- Paket yuzeyi: `src/pytop/three_manifolds.py`

## Uc kure

`three_sphere_baseline`, 3-manifold katalogunda referans model olarak tutulur.
Kompakt, orientable ve basit baglantili kapali 3-manifold sezgisi icin temel
baslangic kaydidir.

## Lens uzaylari

`lens_space_l_p_q`, S3 uzerindeki sonlu devirsel grup etkisiyle bolum uzayi
olarak okunur. `lens_space_fundamental_group_signal` profili, temel grup
sinyalinin cogunlukla `Z/pZ` olarak gorundugunu ve q parametresinin daha ince
ayrimlar gerektirebilecegini vurgular.

## Seifert lifli uzaylar

`seifert_fibered_space`, cember lifleriyle ayrisan 3-manifold modelidir.
`seifert_fibration_signal`, baz orbifold ve istisnai lif verisinin global yapida
rol oynadigini kaydeder.

## Torus demetleri

`torus_bundle_mapping_torus`, T2 yuzeyinin bir homeomorfizmasindan mapping torus
insasi olarak okunur. `torus_bundle_monodromy_signal`, monodromy matrisinin
topolojik ve geometrik siniflandirma icin ana sinyal oldugunu belirtir.

## Kullanim notu

MAN-02 kayitlari bir 3-manifold tanima algoritmasi degildir. Amac, Bolum 14.3
hattindaki klasik aileleri ve invariant sinyallerini paket API'sinde
denetlenebilir ogretim profilleri olarak sunmaktir.
