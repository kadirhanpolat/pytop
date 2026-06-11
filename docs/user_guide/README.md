# pytop Kullanım Kılavuzu

Nokta-küme topolojisi ve metrik uzaylar için kapsamlı kullanım kılavuzu.
Her bölüm dört paralel formatta mevcuttur.

---

## Kurulum

```bash
pip install -e .
```

Python 3.11+ gereklidir.

---

## Format Seçimi

| Format | Yol | Kullanım |
|--------|-----|---------|
| **Python script** | `python/chXX_*.py` | `py -3 docs/user_guide/python/chXX_*.py` |
| **Jupyter Notebook** | `notebook/chXX_*.ipynb` | Jupyter Lab veya VS Code ile açın |
| **Markdown** | `markdown/chXX_*.md` | GitHub, VS Code Preview veya herhangi bir Markdown görüntüleyici |
| **LaTeX** | `latex/main.tex` + `latex/chapters/` | `xelatex main.tex` (MiKTeX / TeX Live) |

Çözümler tüm formatlarda mevcuttur: `solutions.py`, `solutions.ipynb`, `solutions.md`,
ve `latex/appendix/solutions.tex`.

---

## Açıklayıcı Pilot — ch04 ve ch06 Zenginleştirmeleri

`feature/user-guide-explanatory-pilot` kapsamında ch04 (Topolojik Uzaylar) ve ch06
(Ayrılma Aksiyomları) tüm dört formatta aşağıdaki pedagojik katmanlarla zenginleştirilmiştir:

- **Yönlendirmeli kanıtlar** — adım adım açıklamalı ispat iskeletleri
- **İz tabloları** — algoritma adımlarını satır satır gösteren tablolar
- **"Ne oldu?" geçişleri** — her önemli adımın sezgisel açıklaması
- **Alıştırma ipuçları ve çözüm bağlantıları** — K1–K3 (kodlama), T1–T2 (teori)
- **TikZ figürleri** — 8 PNG diyagram (aşağıya bakınız)
- **Kutu ortamları** (yalnızca LaTeX) — renk kodlu tcolorbox çerçeveleri

### TikZ Figür Varlıkları

Figürler `assets/` altında önceden oluşturulmuş PNG olarak bulunur; LaTeX ve Markdown
tarafından doğrudan referans alınır. Yeniden oluşturmak için:

```bash
py -3 docs/user_guide/tools/build_figures.py
```

| Dizin | Dosya | İçerik |
|-------|-------|--------|
| `assets/ch04/` | `fig_ch04_baz_tanimi.png` | Baz koşulu — U içindeki x'i saran B |
| `assets/ch04/` | `fig_ch04_kaba_ince.png` | Kaba ve ince topoloji karşılaştırması |
| `assets/ch04/` | `fig_ch04_sierpinski.png` | Sierpiński uzayının açık kümeleri |
| `assets/ch04/` | `fig_ch04_sonsuz_kesisim.png` | Sonsuz kesişim — açık olmama örneği |
| `assets/ch06/` | `fig_ch06_t2_ayirma.png` | Hausdorff: x ve y ayrık açıklarla ayrılır |
| `assets/ch06/` | `fig_ch06_implikasyon.png` | T4→T0 implikasyon zinciri |
| `assets/ch06/` | `fig_ch06_t3_regulerlik.png` | Regülerlik: nokta ile kapalı küme ayrımı |
| `assets/ch06/` | `fig_ch06_urysohn.png` | Urysohn fonksiyonu: C→0, D→1 |

### LaTeX Kutu Ortamları (tcolorbox)

| Ortam | Renk | Kullanım |
|-------|------|---------|
| `sezgi` | Mavi | Sezgisel arka plan ve motivasyon |
| `dikkat` | Turuncu | Yaygın hatalar ve tuzaklar |
| `nedenonemli` | Yeşil | Teoreminin neden önemli olduğu |
| `karsiornek` | Kırmızı | Karşı-örnek ile ifadeyi çürütme |

### Çözümler Eki

10 tam çözüm (ch04: K1–K3, T1–T2; ch06: K1–K3, T1–T2) her formatta mevcuttur:

| Format | Dosya |
|--------|-------|
| LaTeX | `latex/appendix/solutions.tex` (main.tex'e dahil) |
| Markdown | `markdown/solutions.md` |
| Python | `python/solutions.py` |
| Notebook | `notebook/solutions.ipynb` |

---

## Bölümler

### Ön Koşullar

| # | Bölüm | Konu |
|---|-------|------|
| 1 | pytop'a Hızlı Giriş | Kurulum, uzay nesneleri, Result tipi, tag sistemi |
| 2 | Önerme Mantığı | Proposition, bağlaçlar (¬∧∨→↔), tautoloji, ∀/∃/∃! niceleyiciler, T0/T1 uygulaması |
| 3 | Küme Teorisi ve Fonksiyon Temelleri | Kümeler, bağıntılar, denklik, fonksiyon türleri, görüntü/ön-görüntü |

### Kısım I — Nokta-Küme Topolojisi

| # | Bölüm | Konu |
|---|-------|------|
| 4 | Topolojik Uzaylar | Topoloji aksiyomları, baz, alt-baz, temel uzaylar |
| 5 | Yüklemler ve Altküme Operatörleri | Açık/kapalı/clopen, kapanış, iç, sınır, türev, komşuluk |
| 6 | Ayrılma Aksiyomları | T0–T4, Urysohn, Tietze, Tychonoff |
| 7 | Kompaktlık | Açık örtü, varyantlar, Lindelöf, lokal kompakt, Tychonoff teoremi |
| 8 | Bağlantılılık | Bağlantılı, yol-bağlantılı, ark-bağlantılı, lokal, tam. bağlantısız |
| 9 | Sayılabilirlik Aksiyomları | 1st/2nd countable, ayrılabilir, Lindelöf |
| 10 | Sürekli Fonksiyonlar | Süreklilik tanımı, homeomorfizma, sabit/özdeşlik/bileşke |
| 11 | Alt Uzay ve Çarpım Topolojisi | Alt uzay (τ_A = U∩A), çarpım topolojisi, özellik kalıtımı |
| 12 | Bölüm Topolojisi | Denklik bağıntısı, bölüm kümesi, evrensel özellik |
| 13 | Başlangıç ve Son Topoloji | initial_topology_from_maps, altuzay=başlangıç, çarpım=başlangıç, son topoloji, bölüm=son |

### Kısım II — Metrik Uzaylar

| # | Bölüm | Konu |
|---|-------|------|
| 14 | Metrik Uzaylar | Metrik aksiyomları, açık/kapalı top, indüklenen topoloji |
| 15 | Metrik Tamlık | Cauchy dizisi, tam metrik, tamamen sınırlılık, kompaktlık |
| 16 | Metrik Fonksiyonlar | İzometri, Lipschitz, benzerlik, homeomorfizma, sınıflandırma |

---

## Bölüm Yapısı

Her bölüm aynı altı bölümlü şablonu izler:

1. **Konu** — Sezgisel giriş ve formal tanımlar
2. **Teoremler** — Kanıt iskeletleriyle temel teoremler
3. **Algoritmalar** — Sözde kod ve zaman karmaşıklığı
4. **pytop API** — İlgili fonksiyon/sınıf imzaları
5. **Örnekler** — 4–6 çalıştırılabilir örnek
6. **Alıştırmalar** — 3 kodlama + 2 teori sorusu

---

## Mevcut Notebooklar

Aşağıdaki kılavuzdan bağımsız, daha kısa tanıtım notebookları `notebooks/` dizininde mevcuttur:

- `notebooks/spaces_and_predicates.ipynb`
- `notebooks/compactness.ipynb`
- `notebooks/metric_spaces.ipynb`

Bu kılavuz bunların daha kapsamlı ve teorik bir tamamlayıcısıdır.

---

## LaTeX Derleme

```bash
cd docs/user_guide/latex
xelatex main.tex  # veya pdflatex main.tex
```

Türkçe babel desteği için `xelatex` veya `pdflatex` ile `inputenc` kullanılmaktadır.

---

## Lisans

Bu kılavuz `pytop` paketiyle aynı MIT lisansı altındadır.
