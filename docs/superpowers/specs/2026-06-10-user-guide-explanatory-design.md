# pytop Kullanım Kılavuzu — Mevcut Bölümleri Daha Açıklayıcı Yapma Tasarımı (Pilot)

**Tarih:** 2026-06-10
**Durum:** Onaylandı (brainstorming oturumu sonucu)
**Tür:** Dokümantasyon zenginleştirme — **yeni bölüm eklenmez**, mevcut bölümler derinleştirilir

---

## 1. Amaç

`docs/user_guide` altındaki 16 bölümlük, 4 paralel formatlı (LaTeX, Markdown,
Python script, Jupyter Notebook) temel seviye kullanım kılavuzunun mevcut
bölümlerini daha açıklayıcı hale getirmek. Bu tasarım **pilot** kapsamını
tanımlar: zenginleştirme şablonu Bölüm 4 (Topolojik Uzaylar) ve Bölüm 6
(Ayrılma Aksiyomları) üzerinde uygulanıp doğrulanır; kalan 14 bölüme
yaygınlaştırma ayrı planlarla yapılır (bkz. §13).

## 2. Mevcut Durumun Tespiti

- 16 bölüm × 4 format; her bölüm altı kısımlık sabit şablon izler:
  Konu → Teoremler → Algoritmalar → pytop API → Örnekler → Alıştırmalar.
- LaTeX kaynaklarında **hiç şekil yok** (0 `tikzpicture`); tüm anlatım metinsel.
- Örnekler "kod + çıktı + 1-2 cümle" kalıbında; çıktının tanımla bağlantısı zayıf.
- Kanıtlar iskelet düzeyinde (ör. Baz Teoremi kanıtı 4 satır).
- Alıştırmaların ipucu/çözümü yok (tek tük ipucu hariç).
- Preamble'da pedagojik kutu ortamı yok; yalnız standart `amsthm` ortamları var.
- Python scriptler `# %% [markdown]` yüzde-hücre formatında yazılmış
  (VS Code/Jupytext uyumlu); notebooklar bunlarla paraleldir.

## 3. Alınan Kararlar

| Soru | Karar |
|------|-------|
| Hedef kitle | **Karma** (öğrenci + kendi kendine öğrenen + pytop kullanıcısı matematikçi); katmanlı anlatım: sezgi + formal + API |
| Zenginleştirme boyutları | **Dördü birden:** TikZ görselleri, pedagojik kutular, derin örnek açıklamaları, kanıt + çözüm derinliği |
| Format kapsamı | **Tam senkron** — 4 format eşdeğer içerik taşır; şekiller Markdown/notebook'ta PNG olarak görünür |
| Bölüm kapsamı | **Pilot önce:** ch04 + ch06; şablon onaylanınca kalan bölümlere yaygınlaştırma |
| Çözüm politikası | **İpucu satır içinde + tam çözüm ek'te** (her formatta karşılığıyla) |
| Yaklaşım | **A — Şablon v2:** preamble altyapısı + elle zenginleştirme; TikZ tek görsel kaynak, betikle PNG üretimi |

## 4. Pilot Kapsamı

- `main.tex` preamble altyapısı (kutular, TikZ, `\ipucu`, çözüm eki iskeleti)
- ch04 ve ch06'nın 4 formatta zenginleştirilmesi
- 8 TikZ şekli (bölüm başına 4) + PNG üretim betiği
- Çözüm dosyaları: yalnız ch04 + ch06 girdileriyle başlar
- `docs/user_guide/README.md` güncellemesi (yeni dosyalar, şekil üretimi, çözüm dosyaları)

## 5. Dosya Düzeni

```
docs/user_guide/
├── latex/
│   ├── main.tex                          ← preamble genişler; appendix \input edilir
│   ├── chapters/
│   │   ├── ch04_topological_spaces.tex   ← pilot zenginleştirme
│   │   └── ch06_separation.tex           ← pilot zenginleştirme
│   ├── figures/                          ← YENİ: fig_chNN_<ad>.tikz (yalnız tikzpicture gövdesi)
│   └── appendix/
│       └── solutions.tex                 ← YENİ: "Ek A — Alıştırma Çözümleri"
├── assets/
│   ├── ch04/*.png                        ← YENİ: üretilen şekiller (git'e commit edilir)
│   └── ch06/*.png
├── tools/
│   └── build_figures.py                  ← YENİ: TikZ → PNG hattı (yalnız stdlib)
├── markdown/
│   ├── ch04_*.md, ch06_*.md              ← senkron zenginleştirme
│   └── solutions.md                      ← YENİ
├── python/
│   ├── ch04_*.py, ch06_*.py              ← senkron zenginleştirme (% hücre düzeni korunur)
│   └── solutions.py                      ← YENİ: çalıştırılabilir çözümler
└── notebook/
    ├── ch04_*.ipynb, ch06_*.ipynb        ← senkron zenginleştirme
    └── solutions.ipynb                   ← YENİ
```

## 6. LaTeX Altyapısı (preamble eklemeleri)

1. **TikZ:** `\usepackage{tikz}` + `\usetikzlibrary{arrows.meta, positioning, calc, patterns, decorations.pathmorphing}`
2. **Kutular:** `\usepackage[most]{tcolorbox}` ile dört ortam; tümü `breakable`,
   başlıklar düz metin (PDF fontu Latin Modern olduğundan **LaTeX'te emoji
   kullanılmaz**; emojiler yalnız Markdown/notebook karşılıklarında):

   | Ortam | Başlık | Zemin / çerçeve | İçerik sözleşmesi |
   |-------|--------|-----------------|-------------------|
   | `sezgi` | Sezgi | `blue!5` / `blue!75!black` | Günlük benzetme **+** benzetmenin matematiksel karşılığını kuran 1 cümle |
   | `dikkat` | Dikkat — sık hata | `orange!8` / `orange!85!black` | Gerçek bir kullanım/akıl yürütme hatası ve düzeltmesi |
   | `nedenonemli` | Neden önemli? | `green!6` / `green!50!black` | Kavramın teorideki ve pytop pratiğindeki rolü |
   | `karsiornek` | Karşı-örnek | `violet!6` / `violet!70!black` | Tanım koşulunu ihlal eden somut örnek; mümkünse çalışan pytop kodu eşliğinde |

3. **İpucu makrosu:**
   `\newcommand{\ipucu}[1]{\par\smallskip\noindent\textit{İpucu: #1}}`
4. **Çözüm eki:** `\mainmatter` sonunda `\appendix` + `\input{appendix/solutions}`;
   `solutions.tex` içinde `\chapter{Alıştırma Çözümleri}` ve bölüm başına bir
   `\section`. Etiket şeması: alıştırma `\label{ex:ch04:K1}`, çözüm
   `\label{sol:ch04:K1}`. Çift yönlü bağlantı: alıştırma maddesi
   `(\hyperref[sol:ch04:K1]{çözüm})` ile biter; çözüm
   `(\hyperref[ex:ch04:K1]{alıştırmaya dön})` bağlantısı içerir.

## 7. Bölüm Zenginleştirme Kontrol Listesi

Altı kısımlık şablon **korunur**; her kısım şu ölçülebilir asgarilerle güçlendirilir.
Pilot bölümlerde şekil sayısı tam 4'tür (§8); yaygınlaştırmada bölüm başına
asgari 2, hedef 3–4 şekildir.

| Kısım | Zorunlu eklemeler |
|-------|-------------------|
| 1. Konu | Sezgisel girişin ardından 1 `sezgi` kutusu • her formal tanım sonrası koşulların rolünü açan kısa çözümleme • en az 1 tanım için `karsiornek` kutusu • en az 1 şekil |
| 2. Teoremler | Kanıt iskeletleri → **rehberli kanıt**: başta tek cümlelik strateji, numaralı adımlar, her adımda kullanılan aksiyom/tanım `\ref` ile anılır • teorem sonrası 1 cümlelik pytop köprüsü ("bu teorem `X` fonksiyonunun doğruluğunu garanti eder") |
| 3. Algoritmalar | Sözde kod altına **iz sürme tablosu**: küçük somut girdiyle adım adım durum |
| 4. pytop API | **Tag gerekçe tablosu**: pilot bölümle ilgili her etiket için "hangi koşul sağlanınca atanır" satırı |
| 5. Örnekler | Her örneğe **"Ne oldu?"** paragrafı: çıktının satır satır yorumu, tanım/teorem çapraz referanslı • bölüm genelinde en az 1 `dikkat` ve 1 `nedenonemli` kutusu |
| 6. Alıştırmalar | Her maddeye `\ipucu{}` • her maddenin ek'te tam çözümü (kodlama: çalıştırılıp doğrulanmış kod + gerçek çıktı; teori: tam argüman) |

**Doğruluk kuralı:** Kutulardaki ve "Ne oldu?" paragraflarındaki API davranışına
dair her iddia, yazım sırasında kod çalıştırılarak doğrulanır; dokümandaki çıktı
blokları gerçek çıktıdan yapıştırılır.

## 8. Pilot Şekil Planı

| Dosya (`latex/figures/`) | İçerik | Yerleşim |
|--------------------------|--------|----------|
| `fig_ch04_baz_tanimi.tikz` | Baz tanımı: $x \in B \subseteq U$ iç içe bölgeler | ch04 §Konu (Baz ve Alt-Baz) |
| `fig_ch04_kaba_ince.tikz` | Aynı küme üzerinde kaba ↔ ince topoloji karşılaştırması | ch04 §Teoremler (Karşılaştırma) |
| `fig_ch04_sierpinski.tikz` | Sierpiński uzayının açık küme diyagramı | ch04 §Örnekler (Örnek 1) |
| `fig_ch04_sonsuz_kesisim.tikz` | $\bigcap_n(-\tfrac1n,\tfrac1n)=\{0\}$ karşı-örneği | ch04 §Teoremler (Aksiyomların Yeterliliği) |
| `fig_ch06_t2_ayirma.tikz` | T2: iki noktanın ayrık komşuluklarla ayrılması | ch06 §Konu |
| `fig_ch06_implikasyon.tikz` | T4→T3→T2→T1→T0 zinciri; "tersi geçmez" karşı-örnek etiketleriyle | ch06 §Teoremler |
| `fig_ch06_t3_regulerlik.tikz` | T3: nokta–kapalı küme ayrımı | ch06 §Konu |
| `fig_ch06_urysohn.tikz` | Urysohn fonksiyonu 0→1 geçiş şeması | ch06 §Teoremler |

Her şeklin alt yazısı 2–6 satırdır ve şekli metinden bağımsız anlaşılır kılar.
PNG adları `.tikz` adıyla birebir aynıdır (`fig_ch04_baz_tanimi.png` →
`assets/ch04/`).

## 9. Dört Format Eşleme Tablosu

| LaTeX öğesi | Markdown | Python script (`# %% [markdown]` hücresi) | Notebook (markdown hücresi) |
|-------------|----------|--------------------------------------------|------------------------------|
| `sezgi` | `> **💡 Sezgi:** …` | aynı blockquote metni | aynı blockquote |
| `dikkat` | `> **⚠️ Dikkat — sık hata:** …` | aynı | aynı |
| `nedenonemli` | `> **🎯 Neden önemli?** …` | aynı | aynı |
| `karsiornek` | `> **🚫 Karşı-örnek:** …` + kod bloğu | blockquote hücresi + *çalışan* kod hücresi | aynı |
| TikZ şekli | `![<alt yazı özeti>](../assets/chNN/fig_*.png)` | hücre içinde şekle metinsel atıf (script'te görüntü gömülmez) | `![](../assets/chNN/fig_*.png)` relatif yol; base64 gömme yapılmaz |
| "Ne oldu?" paragrafı | normal paragraf (`**Ne oldu?**` öncülü) | aynı metin, markdown hücresi | aynı |
| `\ipucu{}` | alıştırma altında `*İpucu: …*` | aynı | aynı |
| Çözüm eki | `markdown/solutions.md` | `python/solutions.py` (çalıştırılabilir, % hücre düzeni) | `notebook/solutions.ipynb` |

Senkron tanımı: dört formatta **aynı bilgi** taşınır; üslup format idiyomuna
uyarlanır (LaTeX `\ref` çapraz referansları diğer formatlarda "bkz. Tanım 4.1"
biçimine düzleşir).

## 10. Şekil Üretim Hattı — `tools/build_figures.py`

- **Girdi:** `latex/figures/*.tikz` — her dosya yalnız `tikzpicture` ortamını
  içerir; LaTeX bölümleri bunları `\input{figures/...}` ile kullanır (tek kaynak).
- **İşlem:** her `.tikz` geçici dizinde `\documentclass[tikz,border=2pt]{standalone}`
  şablonuna sarılır → `xelatex` ile PDF → `pdftoppm` (yoksa Ghostscript:
  `gswin64c`/`gs`) ile **300 dpi, beyaz zeminli PNG** → `assets/chNN/` altına yazılır.
- **Bağımlılık:** yalnız Python stdlib + sistemde kurulu `xelatex` ve
  `pdftoppm`/Ghostscript. Araç eksikse betik hangi aracın bulunamadığını ve
  kurulum önerisini yazarak durur; geçici dizinde çalıştığı için yarım çıktı
  bırakmaz.
- **Kurallar:** PNG'ler git'e commit edilir (okuyucu LaTeX kurmadan görür);
  PNG asla elle düzenlenmez, daima `.tikz`'ten yeniden üretilir; tüm şekiller
  her çağrıda yeniden derlenir (8 şekil için önbellek gereksiz — YAGNI).

## 11. Çözüm Dosyaları

- **LaTeX:** `appendix/solutions.tex` — bölüm başına `\section`, alıştırma
  etiketleriyle (K1–K3, T1–T2) hizalı, çift yönlü `\hyperref` (§6.4).
- **Markdown:** `markdown/solutions.md` — aynı yapı, başlık bağlantılarıyla.
- **Python:** `python/solutions.py` — kodlama çözümleri çalıştırılabilir
  hücreler; teori çözümleri markdown hücreleri.
- **Notebook:** `notebook/solutions.ipynb` — `solutions.py` ile paralel.
- Kodlama çözümlerinde gösterilen çıktılar gerçek çalıştırmadan alınır.

## 12. Doğrulama — Pilot "Bitti" Tanımı

1. `xelatex main.tex` sıfır hatayla derlenir; kutular sayfa sonlarında düzgün
   bölünür (`breakable` görsel kontrolü).
2. `python docs/user_guide/python/ch04_topological_spaces.py`,
   `ch06_separation.py` ve `solutions.py` hatasız çalışır; dokümandaki tüm
   çıktı blokları gerçek çıktıyla eşleşir.
3. `jupyter nbconvert --execute` ile iki pilot notebook ve `solutions.ipynb`
   baştan sona çalışır.
4. `tools/build_figures.py` temiz çalışma ağacında 8 PNG'yi üretir; Markdown
   önizlemede ve notebooklarda görüntü yolları kırık değildir.
5. `docs/user_guide/README.md` yeni dosyaları ve şekil üretim adımını anlatır.

## 13. Süreç, Yaygınlaştırma ve Kapsam Dışı

- **Dal:** `feature/user-guide-explanatory-pilot`; `master`'a doğrudan commit
  yapılmaz (CLAUDE.md kuralı). Bu tasarım dokümanı da bu dalda yaşar.
- **Yaygınlaştırma (bu spec'in kapsamı dışında, ayrı planlar):** kalan 14 bölüm
  aynı kontrol listesiyle (§7) 3–4 bölümlük dalgalar hâlinde zenginleştirilir.
  Elle yazılmış "Dizin" bölümünün gerçek `imakeidx` dizinine dönüştürülmesi
  **son dalganın** işidir.
- **Kapsam dışı:** yeni bölüm eklenmesi; `src/pytop` içinde herhangi bir
  değişiklik; matplotlib veya başka Python paketi bağımlılığı; sürüm numarası
  kararı (birleştirme anında verilecek).
