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
| **Python script** | `python/chXX_*.py` | `python docs/user_guide/python/ch01_topological_spaces.py` |
| **Jupyter Notebook** | `notebook/chXX_*.ipynb` | Jupyter Lab veya VS Code ile açın |
| **Markdown** | `markdown/chXX_*.md` | GitHub, VS Code Preview veya herhangi bir Markdown görüntüleyici |
| **LaTeX** | `latex/main.tex` + `latex/chapters/` | `xelatex main.tex` veya `pdflatex main.tex` |

---

## Bölümler

### Ön Koşullar

| # | Bölüm | Konu |
|---|-------|------|
| 0 | Küme Teorisi ve Fonksiyon Temelleri | Kümeler, bağıntılar, denklik, fonksiyon türleri, görüntü/ön-görüntü |
| 0b | pytop'a Hızlı Giriş | Kurulum, uzay nesneleri, Result tipi, tag sistemi |

### Kısım I — Nokta-Küme Topolojisi

| # | Bölüm | Konu |
|---|-------|------|
| 1 | Topolojik Uzaylar | Topoloji aksiyomları, baz, alt-baz, temel uzaylar |
| 2 | Yüklemler ve Altküme Operatörleri | Açık/kapalı/clopen, kapanış, iç, sınır, türev, komşuluk |
| 3 | Ayrılma Aksiyomları | T0–T4, Urysohn, Tietze, Tychonoff |
| 4 | Kompaktlık | Açık örtü, varyantlar, Lindelöf, lokal kompakt, Tychonoff teoremi |
| 5 | Bağlantılılık | Bağlantılı, yol-bağlantılı, ark-bağlantılı, lokal, tam. bağlantısız |
| 6 | Sayılabilirlik Aksiyomları | 1st/2nd countable, ayrılabilir, Lindelöf |
| 10 | Sürekli Fonksiyonlar | Süreklilik tanımı, homeomorfizma, sabit/özdeşlik/bileşke |
| 11 | Alt Uzay ve Çarpım Topolojisi | Alt uzay (τ_A = U∩A), çarpım topolojisi, özellik kalıtımı |
| 12 | Bölüm Topolojisi | Denklik bağıntısı, bölüm kümesi, evrensel özellik |

### Kısım II — Metrik Uzaylar

| # | Bölüm | Konu |
|---|-------|------|
| 7 | Metrik Uzaylar | Metrik aksiyomları, açık/kapalı top, indüklenen topoloji |
| 8 | Metrik Tamlık | Cauchy dizisi, tam metrik, tamamen sınırlılık, kompaktlık |
| 9 | Metrik Fonksiyonlar | İzometri, Lipschitz, benzerlik, homeomorfizma, sınıflandırma |

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
