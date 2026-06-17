# Kullanım Kılavuzu Açıklayıcılık Zenginleştirme — Pilot Uygulama Planı

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** ch04 (Topolojik Uzaylar) ve ch06 (Ayrılma Aksiyomları) bölümlerini dört formatta (LaTeX, Markdown, Python, Notebook) spec'teki kontrol listesine göre zenginleştirmek: 4 pedagojik kutu ortamı, 8 TikZ şekli + PNG hattı, "Ne oldu?" çözümlemeleri, rehberli kanıtlar, iz tabloları, tag gerekçeleri, ipuçları ve ek'te doğrulanmış çözümler.

**Architecture:** LaTeX el yapımı kalır; preamble'a tcolorbox/TikZ altyapısı eklenir. Şekillerin tek kaynağı `latex/figures/*.tikz`; `tools/build_figures.py` bunları standalone+xelatex+pdftoppm ile `assets/chNN/*.png`'ye çevirir, Markdown/Notebook bu PNG'leri gömer. Metinsel öğeler "Ortak İçerik Blokları" (CB-xx) bölümünde bir kez tanımlanır; LaTeX görevleri kendi LaTeX sürümünü, format senkron görevleri CB bloklarını kullanır.

**Tech Stack:** XeLaTeX (MiKTeX), tcolorbox, TikZ, listings; Python 3.14 (stdlib + nbformat 5.10.4); pdftoppm (Poppler); jupyter nbconvert.

**Spec:** `docs/superpowers/specs/2026-06-10-user-guide-explanatory-design.md`

---

## Çalıştırma Ortamı Notları (ÖNEMLİ)

- **Python:** `python` ve `py` varsayılanı pytop'u GÖRMEZ. Her Python komutu **`py -3.14`** ile çalıştırılır (pytop 0.5.33 editable, `E:\PYTHON\pytop\src` — bu oturumda tazelendi).
- **Araçlar (doğrulandı):** `xelatex` OK, `pdftoppm` OK, Ghostscript YOK, `jupytext` YOK, `nbformat` 5.10.4 OK, MiKTeX'te `tcolorbox.sty` + `standalone.cls` OK.
- **Dal:** `feature/user-guide-explanatory-pilot` (mevcut, spec commit'li). master'a commit YASAK.
- **Kod stili:** Yeni Python örneklerinde print metinleri mevcut konvansiyon gibi ASCII (`"Tasiyici:"` stili — Türkçe karakter yok); docstring/markdown hücrelerinde Türkçe serbest (UTF-8).
- **Doğruluk kuralı:** Dokümana giren her çıktı bloğu gerçek çalıştırmadan yapıştırılır. Aşağıdaki "beklenen çıktı"lar bu oturumda doğrulanmıştır; adımda yine de çalıştırıp birebir teyit edin.
- **LaTeX derleme:** `cd docs/user_guide/latex` içinde `xelatex -interaction=nonstopmode main.tex` **iki kez** (yeni `\ref`/`\label`'lar için). Başarı ölçütü: çıktıda `!` ile başlayan hata satırı yok, `main.pdf` güncellenmiş.

## Doğrulanmış API Gerçekleri (içerik bunlara dayanır)

| # | Çağrı | Sonuç |
|---|-------|-------|
| A | `make_topology({1,2,3},{1},{2})` | Sessizce döner: `[[], [1], [1,2,3], [2]]`, tags `['finite']` — **birleşim kapanışı YOK, aksiyom denetimi YOK** ({1,2} eksik → T3 ihlali) |
| B | `cofinite_topology('a','b','c')` | `\|τ\|=8` (= ayrık!), tags `['cofinite','compact','finite','t1']`; `is_t1`→true, `is_t2`→**true** (tag'te hausdorff yok ama yüklem true) |
| C | `topology_from_subbasis({1,2,3,4},[{1,2},{3,4},{2,3}])` | `\|τ\|=9`; açıklar: `[], [2], [3], [1,2], [2,3], [3,4], [1,2,3], [2,3,4], [1,2,3,4]` |
| D | `finite_chain_space(5)` | 6 açık: `[], [1], [1,2], [1,2,3], [1,2,3,4], [1,2,3,4,5]`; tags `['finite']` |
| E | `indiscrete_topology(1,2,3)` tags | `['compact','connected','finite','indiscrete']` |
| F | `sierpinski_space()` tags | `['compact','connected','finite','t0']` |
| G | `separation_chain(make_topology({1,2,3},{1},{2},{1,2}))` | t0=true; t1, hausdorff, urysohn, t3, t4, completely_normal, perfectly_normal=false; **tychonoff=unknown** |
| H | `separation_chain(finite_chain_space(3))` | G ile aynı desen (t0=true, tychonoff=unknown, kalanlar false) |
| I | `two_point_indiscrete_space()` | T0=false, T1=false, T2=false; `is_regular`→true, `is_normal`→true, `is_t3`→**false**, `is_t4`→**false** ⇒ pytop'ta T3=T1+regüler, T4=T1+normal |
| J | `naturals_cofinite()` | T1=true, T2=false |
| K | `separation_chain` anahtarları | `t0, t1, hausdorff, urysohn, t3, tychonoff, t4, completely_normal, perfectly_normal` |
| L | `separation_chain(discrete_topology(1,2,3))` | **9 anahtarın hepsi true** (tychonoff dahil) |
| M | `is_compact(discrete_topology(1,2,3))` | true (tag listesinde 'compact' olmamasına rağmen) |
| N | `topology_from_basis({1,2,3},[{1},{2}])` | **`BasisConstructionError` fırlatır** (B1 ihlali: 3 örtülmüyor) |
| P | ch04 notebook yapısı | 26 hücre (19 md + 7 kod), çıktılar kayıtlı, kernel `python3` |

## Bilinen İçerik Hatası (pilotta düzeltilecek)

Mevcut ch04 alıştırması K1 ("X={a,b,c} üzerinde T1 ama T2 olmayan topoloji inşa edin") **matematiksel olarak imkânsızdır**: sonlu kümede T1 ⇒ ayrık ⇒ Hausdorff (ch06'daki "Sonlu T1 ⟺ Ayrık" teoremi). K1 dört formatta da yeniden yazılır (CB-14'teki metinle).

---

# ORTAK İÇERİK BLOKLARI (CB)

Markdown biçiminde tek kaynak. Görev 8 (Markdown) bunları olduğu gibi kullanır; Görev 9 (Python) `# %% [markdown]` + `"""..."""` hücresine koyar; Görev 10 (Notebook) markdown hücresi yapar. LaTeX sürümleri Görev 5–7 içinde ayrıca verilmiştir (markup farklı, içerik aynı).

### CB-01 — sezgi (ch04, Sezgisel Giriş'in sonuna)

> **💡 Sezgi:** Bir şehir haritasında "yakınlık"ı sokak mesafesiyle ölçebilirsiniz; ama "hangi mahalleler birbirine komşu?" sorusu mesafe olmadan da anlamlıdır. Topoloji tam bunu yapar: mesafeyi unutur, yalnızca "hangi kümeler bir noktanın çevresini oluşturur?" bilgisini tutar. Matematiksel karşılığı: $\tau$ ailesi her noktanın "çevre" kavramını açık kümeler aracılığıyla kodlar; süreklilik ve yakınsama gibi kavramlar yalnız $\tau$'ya başvurularak tanımlanır.

### CB-02 — aksiyom rolleri (ch04, formal tanımın hemen ardına)

Aksiyomların her biri ayrı bir iş görür: **(T1)** uzayın tamamının ve boş kümenin her zaman "gözlemlenebilir" olmasını garanti eder; **(T2)** iki gözlemin kesişiminin de gözlem olmasını sağlar — sonlu kesişimle sınırlı kalması bilinçli bir tercihtir (bkz. Teorem "Aksiyomların Yeterliliği"); **(T3)** keyfî birleşime izin vererek küçük çevrelerden büyük çevre kurma işlemini serbest bırakır.

### CB-03 — karşı-örnek (ch04, CB-02'nin ardına)

> **🚫 Karşı-örnek:** $X=\{1,2,3\}$ üzerinde $\sigma=\{\emptyset,\{1\},\{2\},X\}$ ailesi bir topoloji *değildir*: $\{1\}\cup\{2\}=\{1,2\}\notin\sigma$ olduğundan (T3) ihlal edilir. (T1) ve (T2) sağlansa bile tek bir eksik birleşim aileyi topoloji olmaktan çıkarır. Bu ailenin `make_topology`'ye verilince ne olduğunu Örnekler bölümündeki "Dikkat" kutusunda göreceğiz.

### CB-04 — neden önemli (ch04, Baz ve Alt-Baz alt bölümüne)

> **🎯 Neden önemli?** Baz, büyük bir topolojiyi küçük bir çekirdekle temsil etme aracıdır. Gerçek doğrunun standart topolojisi sayılamaz çoklukta açık küme içerir; ama tümü, sayılabilir $\{(a,b) : a<b,\ a,b\in\mathbb{Q}\}$ bazından üretilir. `pytop` tarafında `topology_from_basis` tam bu ilkeyle çalışır: yalnız baz elemanlarını verirsiniz, kapanışı kütüphane hesaplar.

### CB-05 — Ne oldu? (ch04 Örnek 1, Sierpiński)

**Ne oldu?** Çıktıdaki üç satırı tek tek okuyalım. `Tasiyici` satırı $X=\{0,1\}$'i verir. `Topoloji` satırındaki üç küme tam olarak tanımın istediği yapıdır: $\emptyset$ ve $X$ (T1 aksiyomu), tek ek açık küme $\{1\}$; $\{1\}\cap X=\{1\}$ ve $\{1\}\cup X=X$ zaten listede olduğundan (T2)–(T3) de sağlanır. `Etiketler` satırında `t0` var ama `t1` yok: $1$'i içerip $0$'ı dışlayan açık küme vardır ($\{1\}$), fakat $0$'ı içerip $1$'i dışlayan açık küme yoktur — T0 sağlanıp T1'in sağlanmamasının kaynağı budur (Bölüm 6, Örnek 1'de yüklemlerle test edilir).

### CB-06 — Ne oldu? (ch04 Örnek 2, Ayrık)

**Ne oldu?** $n=3$ eleman için $|\tau|=2^3=8$: her alt küme açıktır. Her tekil küme açık olduğundan herhangi iki nokta kendi tekil komşuluklarıyla ayrılır — `hausdorff`, `normal`, `regular` etiketlerinin kaynağı budur. `metrizable` etiketi 0–1 metriğinden gelir: $d(x,y)=1$ ($x\neq y$) metriği tam olarak ayrık topolojiyi üretir. Listede `compact` etiketi yok; ama bu uzay sonlu olduğu için elbette kompakttır ve `is_compact` yüklemi `true` döner — etiketler ile yüklemler arasındaki bu fark için "Tag Gerekçeleri" tablosuna bakın.

### CB-07 — Ne oldu? (ch04 Örnek 3, make_topology)

**Ne oldu?** `make_topology` verilen $\{1\}$ ve $\{2,3\}$ açıklarına yalnızca $\emptyset$ ve $X$'i ekledi; $|\tau|=4$. Bu örnekte şans eseri sonuç geçerli bir topolojidir, çünkü verilen iki küme ayrıktır: birleşimleri $X$, kesişimleri $\emptyset$ zaten ailededir. `make_topology` bu kapanışları *hesaplamaz* — aşağıdaki "Dikkat" kutusu, kapalı olmayan bir aile verildiğinde ne olduğunu gösterir.

### CB-08 — Ne oldu? (ch04 Örnek 4, Zincir)

**Ne oldu?** Çıktıdaki açıklar tam bir "önek merdiveni"dir: $\emptyset \subset \{1\} \subset \{1,2\} \subset \{1,2,3\}$. Alexandrov zincir uzayında $1$ noktası her boş olmayan açıkta yer alır ("en açık" nokta), $3$ ise yalnız $X$'te görünür. Bu yapı, açıkların kesişim ve birleşimlerinin yine önek olmasından dolayı (T2)–(T3)'ü otomatik sağlar.

### CB-09 — Ne oldu? (ch04 Örnek 5, Bazdan üretim)

**Ne oldu?** Baz $\{\{1\},\{2,3\},\{4\}\}$ bir bölüntüdür: elemanları ikişer ikişer ayrıktır. (B2) koşulu boş yere sağlanır (kesişimler boş olduğundan kontrol edilecek nokta yoktur) ve topoloji tüm alt-aile birleşimlerinden oluşur: $2^3=8$ açık küme. Çıktıdaki 8 küme, üç baz elemanının 8 alt kümesinin birleşimleriyle birebir eşleşir.

### CB-10 — Ne oldu? (ch04 Örnek 6, Gerçek doğru)

**Ne oldu?** `Tasiyici: R` satırı taşıyıcının *simgesel* olduğunu söyler: gerçek doğrunun noktaları bellekte tutulmaz, `topology=None`'dır. Tüm topolojik bilgi etiketlerde kodlanmıştır: `connected`, `hausdorff`, `second_countable` gibi olumlu özellikler yanında `not_compact` gibi olumsuz bilgi de taşınır (Heine–Borel: $\mathbb{R}$ kapalı-sınırlı değildir). Sonlu uzaylardaki "hesapla ve doğrula" yaklaşımının yerini burada "bilinen teoremleri etiketle" yaklaşımı alır; metrik tarafı Bölüm 14'te derinleşir.

### CB-11 — dikkat (ch04, Örnek 3'ün "Ne oldu?"sundan sonra; kod + çıktı dahil)

> **⚠️ Dikkat — sık hata:** `make_topology` verdiğiniz aileye yalnızca $\emptyset$ ve $X$'i ekler; birleşim/kesişim kapanışını **hesaplamaz** ve aksiyomları **denetlemez**. Aşağıdaki çağrıda $\{1\}\cup\{2\}=\{1,2\}$ ailede yoktur; dönen nesne (T3)'ü ihlal eden, geçersiz bir "topoloji"dir. Kapanışın hesaplanmasını ve ailenin denetlenmesini istiyorsanız `topology_from_basis` kullanın — o, baz koşullarını sağlamayan aileyi `BasisConstructionError` ile reddeder.

```python
from pytop import make_topology, topology_from_basis

sessiz = make_topology({1, 2, 3}, {1}, {2})   # denetlemez, kapanis hesaplamaz
print("make_topology:", sorted(sorted(t) for t in sessiz.topology))

try:
    topology_from_basis({1, 2, 3}, [{1}, {2}])  # B1 ihlali: 3 ortulmuyor
except Exception as e:
    print("topology_from_basis:", type(e).__name__)
```

Çıktı:

```text
make_topology: [[], [1], [1, 2, 3], [2]]
topology_from_basis: BasisConstructionError
```

### CB-12 — iz sürme tablosu (ch04, Algoritmalar bölümünün sonuna)

**İz Sürme: Küçük Bir Girdiyle Adım Adım.** $X=\{1,2,3\}$, $\mathcal{B}=\{\{1\},\{2,3\}\}$ girdisiyle "Bazdan Topoloji Üretimi":

| Adım | $\mathcal{S}$ (alt-aile) | Eklenen birleşim | $\tau$ (o ana dek) |
|------|--------------------------|------------------|---------------------|
| 0 | — | — | $\{\emptyset, X\}$ |
| 1 | $\{\{1\}\}$ | $\{1\}$ | $\{\emptyset, X, \{1\}\}$ |
| 2 | $\{\{2,3\}\}$ | $\{2,3\}$ | $\{\emptyset, X, \{1\}, \{2,3\}\}$ |
| 3 | $\{\{1\},\{2,3\}\}$ | $\{1\}\cup\{2,3\}=X$ | değişmez |
| 4 | kesişim kapanışı | $\{1\}\cap\{2,3\}=\emptyset$ | değişmez |

Sonuç: $|\tau|=4$; döngü yeni küme üretmediği anda durur.

### CB-13 — tag gerekçeleri (ch04, pytop API bölümünün sonuna)

**Tag Gerekçeleri.** Etiketler, kurucunun (constructor) inşa anında *garanti ettiği* gerçeklerdir:

| Kurucu | Etiketler | Gerekçe |
|--------|-----------|---------|
| `sierpinski_space()` | compact, connected, finite, t0 | Sonlu ⇒ kompakt; $\{1\}$ tek yönlü ayırır ⇒ T0 (T1 değil); $X$ iki ayrık boş olmayan açığa bölünemez ⇒ bağlantılı |
| `discrete_topology(1,2,3)` | discrete, finite, hausdorff, metrizable, normal, regular | Her tekil açık ⇒ tüm ayrılma aksiyomları; 0–1 metriği ayrık topolojiyi üretir |
| `indiscrete_topology(1,2,3)` | compact, connected, finite, indiscrete | Tek parçalanamaz yapı: açık yalnız $\emptyset$ ve $X$ |
| `cofinite_topology('a','b','c')` | cofinite, compact, finite, t1 | Tekiller kapalı ⇒ T1 |
| `make_topology(...)`, `finite_chain_space(n)` | finite | Özellik çıkarımı yapılmaz; yalnız sonluluk işaretlenir |

Etiketler *eksiksiz değildir*: `cofinite_topology('a','b','c')` aslında ayrıktır ve Hausdorff'tur ($2^3=8$ açık), ama `discrete`/`hausdorff` etiketi taşımaz — `is_t2` yüklemi yine `true` döner. Kesin sorgu için Bölüm 6'daki `is_*` yüklemlerini kullanın; etiket, yüklemin yerine geçmez.

### CB-14 — ch04 alıştırma güncellemeleri (K1 yeniden yazımı + ipuçları)

**K1 (YENİ metin — dört formatta eskisinin yerine):**
`cofinite_topology('a','b','c')` ile üç noktalı kosonlu uzayı kurun; topolojisini ve etiketlerini yazdırın, `is_t1` ve `is_t2` ile test edin. Gözlem: sonlu bir kümede kosonlu topoloji ayrık topolojiyle çakışır. T1 olup Hausdorff olmayan bir örnek için taşıyıcının neden sonsuz olması gerektiğini bir cümleyle açıklayın (krş. Bölüm 6, Örnek 2).

İpuçları (her madde altına):
- K1 — *İpucu: $|\tau|=2^3$ çıkacak; anahtar, Bölüm 6'daki "Sonlu T1 ⟺ Ayrık" teoremidir.*
- K2 — *İpucu: Önce alt-baz çiftlerinin kesişimlerini elle listeleyin ($\{2\}$, $\{3\}$, $\emptyset$); sonra birleşimleri sayın.*
- K3 — *İpucu: Açıklar önek yapısındadır; "en açık" nokta her boş olmayan açıkta bulunandır.*
- T1 — *İpucu: Aday aile sayısı $2^{2^3}=256$'dır; cevap 29. Baz teoremi adayları üretken küçük ailelere indirger.*
- T2 — *İpucu: Ayrıklık için aksiyom gerekmez ($\tau\subseteq\mathcal{P}(X)$ tanım gereğidir); indirgenmişlik için yalnız (T1) yeter.*

Çözüm bağlantısı (her madde sonuna): LaTeX `(\hyperref[sol:ch04:K1]{çözüm})`; Markdown `*(Çözüm: [solutions.md](solutions.md) → Bölüm 4 / K1)*`; Python/Notebook `(Cozum: solutions.py / solutions.ipynb -> Bolum 4 / K1)`.

### CB-15 — sezgi (ch06, giriş paragrafının ardına)

> **💡 Sezgi:** Ayrılma aksiyomlarını bir mikroskobun çözünürlük kademeleri gibi düşünün: T0'da iki noktayı *en az bir yönden* ayırt edebilirsiniz; T1'de her iki yönden; T2'de noktaları çakışmayan iki ayrı "görüş alanına" koyabilirsiniz; T3 ve T4'te artık nokta–kapalı küme ve kapalı–kapalı çiftleri bile ayrışır. Matematiksel karşılığı: her aksiyom, $\tau$'nun "ayırma gücü" üzerine gittikçe güçlenen bir varsayımdır ve zincir boyunca her adım bir öncekini gerektirir.

### CB-16 — dikkat (ch06, aksiyom tablosunun ardına; kod + çıktı dahil)

> **⚠️ Dikkat — sık hata:** T3 ve T4'ün tanımı kaynaktan kaynağa değişir: bazı kitaplar "regüler"i T1 olmadan tanımlar. Bu kılavuzda ve `pytop`'ta tablodaki konvansiyon geçerlidir: **T3 = T1 + regüler, T4 = T1 + normal**. Fark gerçektir: iki noktalı indirgenmiş uzay regüler *ve* normaldir (ayrılacak uygun çift yoktur), ama T1 olmadığından T3 de T4 de değildir.

```python
from pytop import two_point_indiscrete_space, is_regular, is_normal, is_t3, is_t4

tp = two_point_indiscrete_space()
print("regular:", is_regular(tp).status, "| normal:", is_normal(tp).status)
print("t3     :", is_t3(tp).status, "| t4    :", is_t4(tp).status)
```

Çıktı:

```text
regular: true | normal: true
t3     : false | t4    : false
```

### CB-17 — karşı-örnek (ch06, Konu bölümünün sonuna)

> **🚫 Karşı-örnek:** Hiçbir ayrılma aksiyomunu sağlamayan uzay: iki noktalı indirgenmiş uzay. Açıklar yalnız $\emptyset$ ve $X$ olduğundan iki noktayı ayıran *hiçbir* açık yoktur — uzay T0 bile değildir. Örnekler bölümünde `two_point_indiscrete_space()` ile test edilir; zincirin en altının da boş olabileceğini gösterir.

### CB-18 — neden önemli (ch06, pytop API bölümüne, Result tipi)

> **🎯 Neden önemli?** `is_*` yüklemleri ham `bool` değil, `.status` alanı `true` / `false` / `unknown` olabilen bir `Result` döndürür. Üçüncü değer dürüstlüktür: ör. T3.5 (Tychonoff) sürekli fonksiyonlarla tanımlanır ve sonlu açık-küme taramasıyla karar verilemez; `separation_chain` bu durumda `tychonoff: unknown` raporlar. Sembolik uzaylarda (ör. $\mathbb{R}$) da bilinmeyen özellikler `unknown` kalır — kütüphane bilmediğini *bilmediğini söyleyerek* belirtir.

### CB-19 — Ne oldu? (ch06 Örnek 1, Sierpiński)

**Ne oldu?** `T0: true` — $(0,1)$ çifti için $\{1\}$ açığı $1$'i içerir, $0$'ı dışlar; tek çift bu olduğundan T0 tamam. `T1: false` — ters yön yok: $0$'ı içerip $1$'i dışlayan açık küme yoktur ($\{0\}\notin\tau$; bkz. Bölüm 4, Örnek 1). T1 düşünce T2 de düşer: `T2: false`. Sierpiński, zincirin "T0'da takılan" kanonik örneğidir.

### CB-20 — Ne oldu? (ch06 Örnek 2, Kosonlu ℕ)

**Ne oldu?** `T1: true` — her $n\in\mathbb{N}$ için $\mathbb{N}\setminus\{n\}$ kosonludur, dolayısıyla açıktır; bu, her noktayı diğerinden iki yönlü ayırır. `T2: false` — boş olmayan iki kosonlu açık $U,V$ daima kesişir: $\mathbb{N}\setminus(U\cap V)=(\mathbb{N}\setminus U)\cup(\mathbb{N}\setminus V)$ iki sonlu kümenin birleşimi olarak sonludur, $\mathbb{N}$ sonsuz olduğundan $U\cap V\neq\emptyset$. Ayrık komşuluk bulunamaz. Bu örnek, Bölüm 4'teki K1 alıştırmasının "neden sonsuz taşıyıcı gerekir" sorusunun cevabıdır.

### CB-21 — Ne oldu? + tam çıktı (ch06 Örnek 3, Ayrık zincir)

Mevcut "Çıktı (kısa)" bloğu aşağıdaki **tam gerçek çıktıyla değiştirilir**:

```text
  t0                  : true
  t1                  : true
  hausdorff           : true
  urysohn             : true
  t3                  : true
  tychonoff           : true
  t4                  : true
  completely_normal   : true
  perfectly_normal    : true
```

**Ne oldu?** Ayrık uzayda her tekil açık olduğundan her ayırma görevi tekil komşuluklarla çözülür; dokuz yüklemin tümü `true` döner. `tychonoff` bile `true`'dur: ayrık uzayda her fonksiyon süreklidir, istenen ayırıcı fonksiyon doğrudan yazılır. `separation_chain`'in anahtar sırası zincirin mantıksal sırasıdır — bir uzayın "nerede takıldığını" yukarıdan aşağı okuyabilirsiniz (krş. K2 alıştırması).

### CB-22 — iz sürme tablosu (ch06, Algoritmalar bölümünün sonuna)

**İz Sürme: T0 Prosedürü Sierpiński Üzerinde.** $X=\{0,1\}$, $\tau=\{\emptyset,\{1\},X\}$:

| Çift $(x,y)$ | Denenen $U$ | $x\in U \wedge y\notin U$? | $y\in U \wedge x\notin U$? | Karar |
|--------------|-------------|------------------------------|------------------------------|-------|
| $(0,1)$ | $\emptyset$ | hayır | hayır | devam |
| $(0,1)$ | $\{1\}$ | hayır | **evet** | çift ayrıldı |
| — | — | — | — | tüm çiftler bitti → **true** |

Tek çift tek açıkla ayrıldığından prosedür $O(1)$ adımda biter; genel sınır $O(|X|^2\cdot|\tau|)$'dur.

### CB-23 — ch06 ipuçları

- K1 — *İpucu: Önce açıkları listeleyin: $\emptyset,\{1\},\{2\},\{1,2\},X$. Her çifti ayıran açık arayın; 3'ü içerip 1'i dışlayan açık var mı?*
- K2 — *İpucu: Çıktıda `true` olan en güçlü anahtarı arayın; `unknown` değerlerini CB'deki Result kutusuna göre yorumlayın.* *(LaTeX'te: "Neden önemli?" kutusuna göre)*
- K3 — *İpucu: Tek boş olmayan açık $X$ iken herhangi bir çift nasıl ayrılabilir?*
- T1 — *İpucu: T2⇒T1: ayrık $U\ni x$, $V\ni y$ verildiğinde $U$, $y$'yi; $V$, $x$'i dışlar — iki yönlü ayrım hazır. T1⇒T0: iki yönlü ayrım tek yönlüyü içerir.*
- T2 — *İpucu: T1 ⇒ tekiller kapalı ⇒ (sonlu birleşim) her alt küme kapalı ⇒ her alt küme açık.*

Çözüm bağlantıları CB-14'teki formatla (`sol:ch06:K1` vb.).

### CB-24 — şekil gömme satırları (Markdown ve Notebook)

| Şekil | Markdown/Notebook satırı |
|-------|--------------------------|
| baz tanımı | `![Baz koşulu: U içindeki her x, U'da kalan bir B baz elemanıyla sarılır](../assets/ch04/fig_ch04_baz_tanimi.png)` |
| kaba–ince | `![Kaba (indirgenmiş) ve ince (ayrık) topoloji karşılaştırması](../assets/ch04/fig_ch04_kaba_ince.png)` |
| Sierpiński | `![Sierpiński uzayının açık kümeleri; {0} açık değildir](../assets/ch04/fig_ch04_sierpinski.png)` |
| sonsuz kesişim | `![İç içe (-1/n, 1/n) aralıklarının kesişimi {0} açık değildir](../assets/ch04/fig_ch04_sonsuz_kesisim.png)` |
| T2 ayırma | `![Hausdorff: x ve y ayrık U, V açıklarıyla ayrılır](../assets/ch06/fig_ch06_t2_ayirma.png)` |
| implikasyon | `![T4'ten T0'a implikasyon zinciri; terslerin geçmediği karşı-örnekler](../assets/ch06/fig_ch06_implikasyon.png)` |
| T3 regülerlik | `![Regülerlik: nokta ile kapalı küme ayrık açıklarla ayrılır](../assets/ch06/fig_ch06_t3_regulerlik.png)` |
| Urysohn | `![Urysohn fonksiyonu: C üzerinde 0, D üzerinde 1 değerini alan sürekli f](../assets/ch06/fig_ch06_urysohn.png)` |

Python script'lerinde görüntü gömülmez; ilgili markdown hücresine şu satır eklenir: `(Sekil: assets/ch04/fig_ch04_baz_tanimi.png — PDF kilavuzunda Sekil olarak yer alir)` (dosya adı uyarlanır).

### CB-25 — Bölüm 4 çözümleri (solutions.* dosyalarına)

**K1.**

```python
from pytop import cofinite_topology, is_t1, is_t2
c = cofinite_topology('a', 'b', 'c')
print("|tau| =", len(c.topology))
print("Etiketler:", sorted(c.tags))
print("T1:", is_t1(c).status, "| T2:", is_t2(c).status)
```

```text
|tau| = 8
Etiketler: ['cofinite', 'compact', 'finite', 't1']
T1: true | T2: true
```

Üç elemanlı kümede tümleyeni sonlu olan *her* alt küme kosonlu koşulunu sağlar; $|\tau|=2^3=8=|\mathcal{P}(X)|$, yani topoloji ayrıktır. Sonlu kümede T1 ⇒ tekiller kapalı ⇒ her alt küme kapalı (sonlu birleşim) ⇒ her alt küme açık: T1 olan sonlu uzay zorunlu olarak ayrık, dolayısıyla Hausdorff'tur. T1 olup T2 olmayan örnek için taşıyıcı sonsuz olmalıdır: kosonlu $\mathbb{N}$'de boş olmayan iki açık daima kesişir (Bölüm 6, Örnek 2).

**K2.**

```python
from pytop import topology_from_subbasis
s = topology_from_subbasis({1, 2, 3, 4}, [{1, 2}, {3, 4}, {2, 3}])
print("|tau| =", len(s.topology))
print("Acik kumeler:", sorted(sorted(t) for t in s.topology))
```

```text
|tau| = 9
Acik kumeler: [[], [1, 2], [1, 2, 3], [1, 2, 3, 4], [2], [2, 3], [2, 3, 4], [3], [3, 4]]
```

Alt-baz çiftlerinin kesişimleri $\{2\}$, $\{3\}$, $\emptyset$ yeni baz elemanları üretir; birleşimler $\{1,2,3\}$, $\{2,3,4\}$ ve $X$'i ekler. Toplam 9 açık küme.

**K3.**

```python
from pytop import finite_chain_space
c5 = finite_chain_space(5)
print("|tau| =", len(c5.topology))
print("Acik kumeler:", sorted(sorted(t) for t in c5.topology))
```

```text
|tau| = 6
Acik kumeler: [[], [1], [1, 2], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 5]]
```

Açıklar 6 önektir. "En açık" nokta $1$'dir: tek elemanlı $\{1\}$ açığında ve dolayısıyla her boş olmayan açıkta yer alır; $5$ yalnız $X$'tedir.

**T1.** $X=\{1,2,3\}$ üzerinde tam olarak **29** farklı topoloji vardır (homeomorfizma sınıfı olarak 9). Doğrudan yöntem $\mathcal{P}(\mathcal{P}(X))$'in $2^8=256$ elemanlı aday ailesinin her birinde üç aksiyomu denetlemeyi gerektirir. Baz teoremi işi tersine çevirir: (B1)–(B2)'yi sağlayan küçük aileler seçilir, her biri *otomatik olarak geçerli* bir topoloji üretir; yalnız üretilen topolojilerin tekrarları ayıklanır. Aksiyom denetimi aday başına yapılmaz — üretim doğruluğu Baz Teoremi'nce garantilidir.

**T2.** *Ayrık en incedir:* Herhangi bir $\tau$ topolojisi tanım gereği $\tau\subseteq\mathcal{P}(X)=\tau_{\mathrm{disc}}$ sağlar; hiçbir aksiyoma gerek yoktur, "topoloji $X$'in alt kümelerinden oluşur" tanımı yeter. *İndirgenmiş en kabadır:* (T1) aksiyomu her topolojinin $\emptyset$ ve $X$'i içermesini zorunlu kılar; $\tau_{\mathrm{ind}}=\{\emptyset,X\}\subseteq\tau$. Kullanılan tek aksiyom (T1)'dir.

### CB-26 — Bölüm 6 çözümleri (solutions.* dosyalarına)

**K1.**

```python
from pytop import make_topology, separation_chain
k = make_topology({1, 2, 3}, {1}, {2}, {1, 2})
print("Acik kumeler:", sorted(sorted(t) for t in k.topology))
for prop, r in separation_chain(k).items():
    print(f"  {prop:20s}: {r.status}")
```

```text
Acik kumeler: [[], [1], [1, 2], [1, 2, 3], [2]]
  t0                  : true
  t1                  : false
  hausdorff           : false
  urysohn             : false
  t3                  : false
  tychonoff           : unknown
  t4                  : false
  completely_normal   : false
  perfectly_normal    : false
```

T0 sağlanır: $(1,2)$ çiftini $\{1\}$, $(1,3)$ çiftini $\{1\}$, $(2,3)$ çiftini $\{2\}$ ayırır. T1 düşer: $3$'ü içerip $1$'i dışlayan açık yoktur ($3$ yalnız $X$'te). `tychonoff: unknown` — sürekli fonksiyon ayırması açık-küme taramasıyla karara bağlanmaz; kütüphane dürüstçe "bilinmiyor" der.

**K2.**

```python
from pytop import finite_chain_space, separation_chain
for prop, r in separation_chain(finite_chain_space(3)).items():
    print(f"  {prop:20s}: {r.status}")
```

```text
  t0                  : true
  t1                  : false
  hausdorff           : false
  urysohn             : false
  t3                  : false
  tychonoff           : unknown
  t4                  : false
  completely_normal   : false
  perfectly_normal    : false
```

En yüksek sağlanan aksiyom **T0**'dır. Önek yapısı her çifti "daha solda olan" lehine ayırır: $(1,2)$ için $\{1\}$, $(2,3)$ için $\{1,2\}$. T1 imkânsızdır: $2$'yi içerip $1$'i dışlayan önek yoktur.

**K3.**

```python
from pytop import two_point_indiscrete_space, is_t0, is_t1, is_t2
tp = two_point_indiscrete_space()
print("T0:", is_t0(tp).status, "| T1:", is_t1(tp).status, "| T2:", is_t2(tp).status)
```

```text
T0: false | T1: false | T2: false
```

Boş olmayan tek açık $X$'tir ve her iki noktayı da içerir; hiçbir çift hiçbir yönden ayrılamaz. Zincirin tamamı en alt basamakta düşer.

**T1.** *T2 ⇒ T1:* $x\neq y$ verilsin. T2 ile ayrık $U\ni x$, $V\ni y$ açıkları vardır. $U\cap V=\emptyset$ olduğundan $y\notin U$ ve $x\notin V$: hem "$x$'i içerip $y$'yi dışlayan" hem "$y$'yi içerip $x$'i dışlayan" açık bulundu — T1'in iki yönlü koşulu sağlandı. *T1 ⇒ T0:* T0 yalnız *en az bir* yönlü ayrım ister; T1'in verdiği iki yönlü ayrımın herhangi biri yeter. $\square$

**T2.** *(⇒)* $X$ sonlu ve T1 olsun. T1 gereği her $x$ için ve her $y\neq x$ için $y\in U_y$, $x\notin U_y$ olan açık $U_y$ vardır; $X\setminus\{x\}=\bigcup_{y\neq x}U_y$ açıktır, yani $\{x\}$ kapalıdır. Herhangi $A\subseteq X$, sonlu sayıda tekilin birleşimi olarak kapalıdır; o halde tümleyeni $X\setminus A$ açıktır. $A$ keyfî olduğundan *her* alt küme açıktır: topoloji ayrıktır. *(⇐)* Ayrık topolojide her $\{x\}$ açıktır; $x\neq y$ için $\{x\}$ ve $\{y\}$ iki yönlü ayrımı doğrudan verir, T1 (hatta T2) sağlanır. $\square$

---

# GÖREVLER

## Görev 1: LaTeX altyapısı — kutular, TikZ, \ipucu, çözüm eki iskeleti

**Files:**
- Modify: `docs/user_guide/latex/main.tex`
- Create: `docs/user_guide/latex/appendix/solutions.tex`

- [ ] **Adım 1.1: main.tex preamble'ına altyapı bloğunu ekle**

`% ── Hyperlinks` satırından (mevcut 66. satır civarı) HEMEN ÖNCE şu bloğu ekle:

```latex
% ── Figures (TikZ) ─────────────────────────────────────────────────────────────
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, calc, patterns, decorations.pathmorphing}

% ── Pedagogical boxes ──────────────────────────────────────────────────────────
\usepackage[most]{tcolorbox}
\tcbset{pytopbox/.style={breakable, enhanced, boxrule=0.6pt, arc=2pt,
  left=6pt, right=6pt, top=4pt, bottom=4pt, fonttitle=\bfseries}}
\newtcolorbox{sezgi}{pytopbox, colback=blue!5, colframe=blue!75!black,
  title={Sezgi}}
\newtcolorbox{dikkat}{pytopbox, colback=orange!8, colframe=orange!85!black,
  title={Dikkat -- sık hata}}
\newtcolorbox{nedenonemli}{pytopbox, colback=green!6, colframe=green!50!black,
  title={Neden önemli?}}
\newtcolorbox{karsiornek}{pytopbox, colback=violet!6, colframe=violet!70!black,
  title={Karşı-örnek}}

% ── İpucu macro ────────────────────────────────────────────────────────────────
\newcommand{\ipucu}[1]{\par\smallskip\noindent\textit{İpucu: #1}}
```

- [ ] **Adım 1.2: main.tex'e çözüm ekini bağla**

`\backmatter` satırından HEMEN ÖNCE ekle:

```latex
\appendix
\input{appendix/solutions}

```

- [ ] **Adım 1.3: solutions.tex iskeletini oluştur**

`docs/user_guide/latex/appendix/solutions.tex` dosyasını şu içerikle yarat (bölüm içerikleri Görev 7'de eklenecek; bu hâliyle derlenebilir gerçek metindir):

```latex
\chapter{Alıştırma Çözümleri}
\label{app:solutions}

Bu ek, kılavuz alıştırmalarının tam çözümlerini içerir. Kodlama
çözümlerindeki tüm çıktılar gerçek çalıştırmadan alınmıştır; teori
çözümleri tam argüman verir. Pilot kapsamında Bölüm~4 ve Bölüm~6
çözümleri yer alır; diğer bölümler yaygınlaştırma aşamasında eklenecektir.
```

- [ ] **Adım 1.4: Derle ve doğrula**

```powershell
cd E:\PYTHON\pytop\docs\user_guide\latex
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

Beklenen: her iki çalıştırma da `!` hatasız biter; PDF sonunda "Ek A — Alıştırma Çözümleri" bölümü görünür. (MiKTeX eksik paket indirirse normaldir.)

- [ ] **Adım 1.5: Commit**

```powershell
git add docs/user_guide/latex/main.tex docs/user_guide/latex/appendix/solutions.tex
git commit -m "docs(user_guide/latex): add pedagogical box environments, TikZ, ipucu macro, solutions appendix skeleton"
```

## Görev 2: build_figures.py + ilk şekil (uçtan uca hat doğrulaması)

**Files:**
- Create: `docs/user_guide/tools/build_figures.py`
- Create: `docs/user_guide/latex/figures/fig_ch04_baz_tanimi.tikz`
- Output: `docs/user_guide/assets/ch04/fig_ch04_baz_tanimi.png`

- [ ] **Adım 2.1: build_figures.py'yi yaz**

```python
"""TikZ -> PNG uretim hatti (kilavuz sekilleri).

latex/figures/*.tikz dosyalarini standalone sablonuna sarip xelatex ile
derler, pdftoppm (yoksa Ghostscript) ile 300 dpi beyaz zeminli PNG'ye
cevirir ve assets/chNN/ altina yazar. Yalniz stdlib kullanir.

Kullanim:
    py -3.14 docs/user_guide/tools/build_figures.py                  # tum sekiller
    py -3.14 docs/user_guide/tools/build_figures.py fig_ch04_baz_tanimi
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

GUIDE = Path(__file__).resolve().parents[1]
FIGURES = GUIDE / "latex" / "figures"
ASSETS = GUIDE / "assets"
DPI = "300"

TEMPLATE = """\\documentclass[tikz,border=2pt]{standalone}
\\usepackage{fontspec}
\\setmainfont{Latin Modern Roman}
\\usetikzlibrary{arrows.meta, positioning, calc, patterns, decorations.pathmorphing}
\\begin{document}
<<TIKZ>>
\\end{document}
"""


def fail(msg: str) -> None:
    sys.exit(f"HATA: {msg}")


def find_raster() -> tuple[str, str]:
    exe = shutil.which("pdftoppm")
    if exe:
        return ("pdftoppm", exe)
    for name in ("gswin64c", "gs"):
        exe = shutil.which(name)
        if exe:
            return ("gs", exe)
    fail("pdftoppm (Poppler) veya Ghostscript bulunamadi. "
         "MiKTeX'in miktex-poppler-bin paketini ya da Ghostscript'i kurup PATH'e ekleyin.")
    raise AssertionError  # fail() cikar; tip denetleyici icin


def run(cmd: list[str], cwd: Path) -> None:
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        fail(f"{cmd[0]} basarisiz oldu:\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")


def build(tikz: Path, xelatex: str, raster: tuple[str, str]) -> Path:
    m = re.match(r"fig_(ch\d+)_", tikz.stem)
    if not m:
        fail(f"{tikz.name}: ad 'fig_chNN_<ad>.tikz' kalibina uymali")
    out_dir = ASSETS / m.group(1)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_png = out_dir / (tikz.stem + ".png")
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        body = tikz.read_text(encoding="utf-8")
        (tmp / "fig.tex").write_text(TEMPLATE.replace("<<TIKZ>>", body), encoding="utf-8")
        run([xelatex, "-interaction=nonstopmode", "-halt-on-error", "fig.tex"], tmp)
        pdf = tmp / "fig.pdf"
        if not pdf.exists():
            fail(f"{tikz.name}: PDF uretilemedi")
        kind, exe = raster
        if kind == "pdftoppm":
            run([exe, "-png", "-r", DPI, "-singlefile", str(pdf), str(tmp / "out")], tmp)
        else:
            run([exe, "-dSAFER", "-dBATCH", "-dNOPAUSE", "-sDEVICE=png16m",
                 f"-r{DPI}", f"-sOutputFile={tmp / 'out.png'}", str(pdf)], tmp)
        shutil.copyfile(tmp / "out.png", out_png)
    return out_png


def main() -> None:
    xelatex = shutil.which("xelatex")
    if not xelatex:
        fail("xelatex bulunamadi (MiKTeX veya TeX Live kurun)")
    raster = find_raster()
    istenen = set(sys.argv[1:])
    tikzler = sorted(FIGURES.glob("*.tikz"))
    if istenen:
        tikzler = [t for t in tikzler if t.stem in istenen]
        if not tikzler:
            fail("eslesen .tikz dosyasi yok: " + ", ".join(sorted(istenen)))
    if not tikzler:
        fail(f"{FIGURES} altinda .tikz dosyasi yok")
    for t in tikzler:
        png = build(t, xelatex, raster)
        print(f"  {t.name} -> {png.relative_to(GUIDE)}")
    print(f"Tamam: {len(tikzler)} sekil.")


if __name__ == "__main__":
    main()
```

Not: `.tikz` dosyalarında `%` yorum satırı kullanmayın (şablon yerleştirme sade kalsın diye kural; gerekirse açıklamayı bu planda tutun).

- [ ] **Adım 2.2: İlk şekli yaz — fig_ch04_baz_tanimi.tikz**

`docs/user_guide/latex/figures/fig_ch04_baz_tanimi.tikz`:

```latex
\begin{tikzpicture}[scale=1.0, font=\small]
  \draw[blue!70!black, thick, fill=blue!8]
    plot[smooth cycle, tension=0.8] coordinates
    {(0,0) (2.2,-0.4) (4.2,0.2) (4.6,2.0) (2.6,3.0) (0.3,2.4)};
  \node[blue!70!black] at (4.35,2.65) {$U$};
  \draw[violet!80!black, thick, fill=violet!12]
    (2.2,1.3) ellipse [x radius=1.15, y radius=0.7];
  \node[violet!80!black] at (3.05,1.95) {$B$};
  \fill (2.2,1.25) circle (1.8pt) node[below right=0.5pt] {$x$};
  \node[align=left, anchor=west] at (5.2,1.5)
    {Her $x\in U$ için\\ $x\in B\subseteq U$ olan\\ bir $B\in\mathcal{B}$ vardır.};
\end{tikzpicture}
```

- [ ] **Adım 2.3: Hattı çalıştır, PNG'yi doğrula**

```powershell
py -3.14 docs/user_guide/tools/build_figures.py
```

Beklenen çıktı:

```text
  fig_ch04_baz_tanimi.tikz -> assets\ch04\fig_ch04_baz_tanimi.png
Tamam: 1 sekil.
```

PNG'yi Read aracıyla görüntüleyip kontrol et: $U$ blob'u içinde $B$ elipsi, içinde $x$ noktası, sağda açıklama metni okunaklı. Gerekirse koordinatlarda küçük ayar yapıp yeniden üret (estetik ayar serbest, içerik sabit).

- [ ] **Adım 2.4: Commit**

```powershell
git add docs/user_guide/tools/build_figures.py docs/user_guide/latex/figures/fig_ch04_baz_tanimi.tikz docs/user_guide/assets/ch04/fig_ch04_baz_tanimi.png
git commit -m "docs(user_guide): add TikZ->PNG figure pipeline and first figure (basis definition)"
```

## Görev 3: Kalan ch04 şekilleri (3 adet)

**Files:**
- Create: `docs/user_guide/latex/figures/fig_ch04_kaba_ince.tikz`
- Create: `docs/user_guide/latex/figures/fig_ch04_sierpinski.tikz`
- Create: `docs/user_guide/latex/figures/fig_ch04_sonsuz_kesisim.tikz`
- Output: `docs/user_guide/assets/ch04/*.png` (3 yeni)

- [ ] **Adım 3.1: fig_ch04_kaba_ince.tikz**

```latex
\begin{tikzpicture}[font=\small,
    kutu/.style={draw, rounded corners, align=center, inner sep=8pt}]
  \node[kutu, fill=orange!6] (kaba) at (0,0)
    {$\tau_{\mathrm{ind}}$ (kaba)\\[3pt] $\emptyset,\quad \{a,b\}$};
  \node[kutu, fill=blue!6] (ince) at (6.4,0)
    {$\tau_{\mathrm{disc}}$ (ince)\\[3pt] $\emptyset,\ \{a\},\ \{b\},\ \{a,b\}$};
  \draw[-{Stealth[length=3mm]}, thick]
    (kaba) -- node[above] {$\subseteq$} node[below] {açık küme eklenir} (ince);
\end{tikzpicture}
```

- [ ] **Adım 3.2: fig_ch04_sierpinski.tikz**

```latex
\begin{tikzpicture}[font=\small]
  \fill (0,0) circle (2pt) node[below=3pt] {$0$};
  \fill (2,0) circle (2pt) node[below=3pt] {$1$};
  \draw[blue!70!black, thick] (1,0.05) ellipse [x radius=2.1, y radius=1.0];
  \node[blue!70!black] at (1,1.3) {$X=\{0,1\}$};
  \draw[violet!80!black, thick] (2,0.05) ellipse [x radius=0.62, y radius=0.5];
  \node[violet!80!black] at (2.05,0.82) {$\{1\}$};
  \draw[red!70!black, dashed] (0,0.05) ellipse [x radius=0.62, y radius=0.5];
  \node[red!70!black] at (-0.15,-1.05) {$\{0\}\notin\tau$ (açık değil)};
\end{tikzpicture}
```

- [ ] **Adım 3.3: fig_ch04_sonsuz_kesisim.tikz**

```latex
\begin{tikzpicture}[font=\small, xscale=2.8]
  \draw[-{Stealth}] (-1.35,0) -- (1.5,0) node[right] {$\mathbb{R}$};
  \draw (-1,0.05) -- (-1,-0.05) node[below, font=\scriptsize] {$-1$};
  \draw (0,0.05) -- (0,-0.05);
  \draw (1,0.05) -- (1,-0.05) node[below, font=\scriptsize] {$1$};
  \draw[blue!75, very thick] (-1,0.85) -- (1,0.85);
  \node[blue!75, font=\scriptsize, right] at (1.04,0.85) {$(-1,1)$};
  \draw[blue!55, very thick] (-0.5,0.62) -- (0.5,0.62);
  \node[blue!55, font=\scriptsize, right] at (1.04,0.62) {$(-\tfrac12,\tfrac12)$};
  \draw[blue!40, very thick] (-0.25,0.39) -- (0.25,0.39);
  \node[blue!40, font=\scriptsize, right] at (1.04,0.39) {$(-\tfrac14,\tfrac14)$};
  \node at (0,0.22) {$\vdots$};
  \fill[red!70!black] (0,0) circle (1.2pt);
  \node[red!70!black, below=7pt, font=\scriptsize] at (0,-0.02)
    {$\bigcap_n \bigl(-\tfrac1n,\tfrac1n\bigr)=\{0\}$ --- açık değil};
\end{tikzpicture}
```

- [ ] **Adım 3.4: Üret, görsel kontrol, commit**

```powershell
py -3.14 docs/user_guide/tools/build_figures.py fig_ch04_kaba_ince fig_ch04_sierpinski fig_ch04_sonsuz_kesisim
```

Beklenen: 3 satır `... -> assets\ch04\....png` + `Tamam: 3 sekil.` Üç PNG'yi Read ile görüntüle; etiket çakışması varsa koordinat ayarla, yeniden üret.

```powershell
git add docs/user_guide/latex/figures docs/user_guide/assets/ch04
git commit -m "docs(user_guide): add remaining ch04 figures (coarse/fine, Sierpinski, infinite intersection)"
```

## Görev 4: ch06 şekilleri (4 adet)

**Files:**
- Create: `docs/user_guide/latex/figures/fig_ch06_t2_ayirma.tikz`
- Create: `docs/user_guide/latex/figures/fig_ch06_implikasyon.tikz`
- Create: `docs/user_guide/latex/figures/fig_ch06_t3_regulerlik.tikz`
- Create: `docs/user_guide/latex/figures/fig_ch06_urysohn.tikz`
- Output: `docs/user_guide/assets/ch06/*.png` (4 yeni)

- [ ] **Adım 4.1: fig_ch06_t2_ayirma.tikz**

```latex
\begin{tikzpicture}[font=\small]
  \draw[blue!70!black, thick, fill=blue!8] (0,0) ellipse [x radius=1.25, y radius=0.85];
  \draw[violet!80!black, thick, fill=violet!10] (3.4,0) ellipse [x radius=1.25, y radius=0.85];
  \fill (0,0) circle (1.8pt) node[below=2pt] {$x$};
  \fill (3.4,0) circle (1.8pt) node[below=2pt] {$y$};
  \node[blue!70!black] at (0,1.15) {$U$};
  \node[violet!80!black] at (3.4,1.15) {$V$};
  \node at (1.7,-1.3) {$U \cap V = \emptyset$};
\end{tikzpicture}
```

- [ ] **Adım 4.2: fig_ch06_implikasyon.tikz**

```latex
\begin{tikzpicture}[font=\small, node distance=9mm,
    aks/.style={draw, rounded corners, fill=blue!6, inner sep=5pt}]
  \node[aks] (t4) {T4};
  \node[aks, right=of t4] (t35) {T3.5};
  \node[aks, right=of t35] (t3) {T3};
  \node[aks, right=of t3] (t25) {T2.5};
  \node[aks, right=of t25] (t2) {T2};
  \node[aks, right=of t2] (t1) {T1};
  \node[aks, right=of t1] (t0) {T0};
  \foreach \a/\b in {t4/t35, t35/t3, t3/t25, t25/t2, t2/t1, t1/t0}
    \draw[-{Stealth[length=2.6mm]}, thick] (\a) -- (\b);
  \draw[red!70!black, -{Stealth[length=2.2mm]}, dashed]
    (t1.south) to[bend right=40] node[below, font=\scriptsize, align=center]
    {geçmez: kosonlu $\mathbb{N}$\\ (T1, T2 değil)} (t2.south);
  \draw[red!70!black, -{Stealth[length=2.2mm]}, dashed]
    (t0.south) to[bend right=40] node[below, font=\scriptsize, align=center]
    {geçmez: Sierpiński\\ (T0, T1 değil)} (t1.south);
\end{tikzpicture}
```

- [ ] **Adım 4.3: fig_ch06_t3_regulerlik.tikz**

```latex
\begin{tikzpicture}[font=\small]
  \fill (0,0) circle (1.8pt) node[below=3pt] {$x$};
  \draw[blue!70!black, thick] (0,0.05) ellipse [x radius=1.0, y radius=0.72];
  \node[blue!70!black] at (0,1.05) {$U$};
  \draw[red!70!black, thick, fill=red!6, pattern=north east lines, pattern color=red!40]
    plot[smooth cycle, tension=0.9] coordinates
    {(3.3,-0.3) (4.4,-0.5) (5.0,0.4) (4.0,0.9) (3.2,0.5)};
  \node[red!70!black] at (4.15,-1.0) {$F$ (kapalı)};
  \draw[violet!80!black, thick] (4.1,0.15) ellipse [x radius=1.55, y radius=1.2];
  \node[violet!80!black] at (4.1,1.6) {$V$};
  \node at (2.05,-1.75) {$x\notin F,\qquad x\in U,\quad F\subseteq V,\quad U\cap V=\emptyset$};
\end{tikzpicture}
```

- [ ] **Adım 4.4: fig_ch06_urysohn.tikz**

```latex
\begin{tikzpicture}[font=\small]
  \draw[rounded corners=8pt, thick] (-0.4,-1.15) rectangle (6.4,1.45);
  \node at (5.95,1.2) {$X$};
  \draw[blue!70!black, thick, fill=blue!10] (0.8,0.15) ellipse [x radius=0.85, y radius=0.6];
  \node[blue!70!black] at (0.8,0.15) {$C$};
  \draw[red!70!black, thick, fill=red!10] (5.2,0.15) ellipse [x radius=0.85, y radius=0.6];
  \node[red!70!black] at (5.2,0.15) {$D$};
  \draw[-{Stealth}] (7.7,-0.9) -- (7.7,1.3);
  \draw (7.6,-0.6) -- (7.8,-0.6) node[right] {$0$};
  \draw (7.6,1.0) -- (7.8,1.0) node[right] {$1$};
  \draw[blue!70!black, -{Stealth}, dashed]
    (1.7,0.0) to[bend right=14] node[below, font=\scriptsize, pos=0.45] {$f$} (7.58,-0.6);
  \draw[red!70!black, -{Stealth}, dashed] (6.1,0.3) to[bend left=10] (7.58,1.0);
  \node[font=\scriptsize, align=center] at (3.0,-1.65)
    {$f$ sürekli; $f|_C\equiv 0$, $f|_D\equiv 1$; ara bölgede $0$ ile $1$ arası değerler};
\end{tikzpicture}
```

- [ ] **Adım 4.5: Üret, görsel kontrol, commit**

```powershell
py -3.14 docs/user_guide/tools/build_figures.py fig_ch06_t2_ayirma fig_ch06_implikasyon fig_ch06_t3_regulerlik fig_ch06_urysohn
```

Beklenen: 4 satır + `Tamam: 4 sekil.` Dört PNG'yi Read ile kontrol et (özellikle implikasyon zincirindeki alt etiketlerin çakışmaması). Sonra:

```powershell
git add docs/user_guide/latex/figures docs/user_guide/assets/ch06
git commit -m "docs(user_guide): add ch06 separation figures (T2, implication chain, regularity, Urysohn)"
```

## Görev 5: ch04 LaTeX zenginleştirme

**Files:**
- Modify: `docs/user_guide/latex/chapters/ch04_topological_spaces.tex`

Tüm eklemeler aşağıda tam LaTeX olarak verilmiştir; çapa (anchor) mevcut dosyadaki konumu tarif eder. Sıra önemli değildir ama yukarıdan aşağı uygulamak satır kaymasını önler.

- [ ] **Adım 5.1: Sezgi kutusu** — "Sezgisel Giriş" alt bölümünün son paragrafından (`...tanımlamak mümkündür.`) sonra:

```latex
\begin{sezgi}
Bir şehir haritasında ``yakınlık''ı sokak mesafesiyle ölçebilirsiniz; ama
``hangi mahalleler birbirine komşu?'' sorusu mesafe olmadan da anlamlıdır.
Topoloji tam bunu yapar: mesafeyi unutur, yalnızca ``hangi kümeler bir
noktanın çevresini oluşturur?'' bilgisini tutar. Matematiksel karşılığı:
$\tau$ ailesi her noktanın ``çevre'' kavramını açık kümeler aracılığıyla
kodlar; süreklilik ve yakınsama gibi kavramlar yalnız $\tau$'ya
başvurularak tanımlanır.
\end{sezgi}
```

- [ ] **Adım 5.2: Aksiyom rolleri + karşı-örnek** — Tanım `def:topological_space`'in `\end{definition}` satırından sonra:

```latex
Aksiyomların her biri ayrı bir iş görür: (T1) uzayın tamamının ve boş
kümenin her zaman ``gözlemlenebilir'' olmasını garanti eder; (T2) iki
gözlemin kesişiminin de gözlem olmasını sağlar --- sonlu kesişimle sınırlı
kalması bilinçli bir tercihtir (bkz.\ Teorem~\ref{thm:axiom_sufficiency});
(T3) keyfî birleşime izin vererek küçük çevrelerden büyük çevre kurma
işlemini serbest bırakır.

\begin{karsiornek}
$X=\{1,2,3\}$ üzerinde $\sigma=\{\emptyset,\{1\},\{2\},X\}$ ailesi bir
topoloji \emph{değildir}: $\{1\}\cup\{2\}=\{1,2\}\notin\sigma$
olduğundan (T3) ihlal edilir. (T1) ve (T2) sağlansa bile tek bir eksik
birleşim aileyi topoloji olmaktan çıkarır. Bu ailenin
\texttt{make\_topology}'ye verilince ne olduğunu Örnekler bölümündeki
``Dikkat'' kutusunda göreceğiz.
\end{karsiornek}
```

- [ ] **Adım 5.3: Baz şekli + neden önemli** — Tanım `def:basis`'in `\end{definition}` satırından sonra:

```latex
Şekil~\ref{fig:ch04:baz} koşulu resmeder: açık kümenin her noktası,
tamamen o kümenin içinde kalan bir baz elemanıyla sarılır.

\begin{figure}[ht]
  \centering
  \input{figures/fig_ch04_baz_tanimi.tikz}
  \caption{Baz koşulunun geometrisi: $U$ açık kümesinin her $x$ noktası
    için $x\in B\subseteq U$ sağlayan bir $B\in\mathcal{B}$ vardır.
    Topolojinin tüm açıkları bu tür ``yapı taşları''nın birleşimleridir.}
  \label{fig:ch04:baz}
\end{figure}

\begin{nedenonemli}
Baz, büyük bir topolojiyi küçük bir çekirdekle temsil etme aracıdır.
Gerçek doğrunun standart topolojisi sayılamaz çoklukta açık küme içerir;
ama tümü, sayılabilir $\{(a,b): a<b,\ a,b\in\mathbb{Q}\}$ bazından
üretilir. \texttt{pytop} tarafında \texttt{topology\_from\_basis} tam bu
ilkeyle çalışır: yalnız baz elemanlarını verirsiniz, kapanışı kütüphane
hesaplar (Algoritma~\ref{alg:basis_to_topology}).
\end{nedenonemli}
```

- [ ] **Adım 5.4: Yeterlilik teoremi — rehberli kanıt + şekil** — `thm:axiom_sufficiency`'nin `\end{theorem}` satırından sonra (teoremin içindeki *Not* cümlesi teoremde kalır):

```latex
\begin{proof}[Rehberli Kanıt]
\textbf{Strateji:} $n$ üzerinde tümevarım; tek araç (T2).
\begin{enumerate}
  \item $n=1$: $U_1\in\tau$ zaten verili.
  \item $n=k$ için doğru varsayalım: $V=\bigcap_{i=1}^{k}U_i\in\tau$.
  \item $n=k+1$: $\bigcap_{i=1}^{k+1}U_i = V\cap U_{k+1}$ olup (T2)
        gereği $\tau$'dadır.
\end{enumerate}
Sonsuz kesişimde 3.~adım çalışmaz: tümevarım yalnız sonlu $n$'lere
ulaşır. Şekil~\ref{fig:ch04:kesisim} bunun gerçek bir başarısızlık
olduğunu gösterir: her sonlu kesişim açıkken limit $\{0\}$ açık değildir.
\end{proof}

\begin{figure}[ht]
  \centering
  \input{figures/fig_ch04_sonsuz_kesisim.tikz}
  \caption{(T2)'nin sonlu kesişimle sınırlı olmasının nedeni: iç içe
    $(-\tfrac1n,\tfrac1n)$ açık aralıklarının sonsuz kesişimi tek
    noktaya çöker ve $\{0\}$ standart topolojide açık değildir.}
  \label{fig:ch04:kesisim}
\end{figure}
```

- [ ] **Adım 5.5: Baz Teoremi — iskeleti rehberli kanıtla DEĞİŞTİR + API köprüsü**

Mevcut `\begin{proof}[Kanıt İskeleti] ... \end{proof}` bloğunu (thm:basis'in altındaki) şununla değiştir:

```latex
\begin{proof}[Rehberli Kanıt]
\textbf{Strateji:} $\tau_{\mathcal{B}}$'nin üç aksiyomu sağladığını, her
adımda yalnız (B1)--(B2)'yi kullanarak doğrularız.
\begin{enumerate}
  \item \textbf{(T1):} $\emptyset\in\tau_{\mathcal B}$, çünkü ``her
        $x\in\emptyset$ için\ldots'' koşulu boş yere doğrudur.
        $X\in\tau_{\mathcal B}$: $x\in X$ verilsin; (B1) gereği
        $x\in\bigcup\mathcal B$, yani $x\in B\subseteq X$ olan bir
        $B\in\mathcal B$ vardır.
  \item \textbf{(T2):} $U,V\in\tau_{\mathcal B}$ ve $x\in U\cap V$
        olsun. Tanım gereği $x\in B_U\subseteq U$ ve
        $x\in B_V\subseteq V$ bulunur. (B2), $x\in B_3\subseteq
        B_U\cap B_V\subseteq U\cap V$ veren bir $B_3$ sağlar; $x$
        keyfî olduğundan $U\cap V\in\tau_{\mathcal B}$.
  \item \textbf{(T3):} $x\in\bigcup_\alpha U_\alpha$ ise
        $x\in U_{\alpha_0}$ olan bir indis vardır; $U_{\alpha_0}$'ın
        tanımından gelen $B$, $x\in B\subseteq
        U_{\alpha_0}\subseteq\bigcup_\alpha U_\alpha$ koşulunu da sağlar.
  \item $\mathcal B$'nin $\tau_{\mathcal B}$'ye baz olması,
        $\tau_{\mathcal B}$'nin tanımının Tanım~\ref{def:basis}'teki
        koşulu birebir içermesindendir.
\end{enumerate}
\end{proof}

\noindent Bu teorem, \texttt{topology\_from\_basis}'in döndürdüğü
ailenin gerçekten topoloji olduğunun matematiksel güvencesidir;
fonksiyon ayrıca (B1)--(B2)'yi sağlamayan girdiyi
\texttt{BasisConstructionError} ile reddeder.
```

- [ ] **Adım 5.6: Karşılaştırma teoremi — mini kanıt + şekil + köprü** — `thm:comparison`'ın `\end{theorem}` satırından sonra:

```latex
\begin{proof}[Rehberli Kanıt]
Herhangi bir $\tau$ için $\tau\subseteq\mathcal{P}(X)=\tau_{\mathrm{disc}}$
topoloji tanımının kendisinden gelir (aksiyom gerekmez); (T1) aksiyomu da
$\{\emptyset,X\}=\tau_{\mathrm{ind}}\subseteq\tau$ verir.
\end{proof}

\begin{figure}[ht]
  \centering
  \input{figures/fig_ch04_kaba_ince.tikz}
  \caption{Aynı $X=\{a,b\}$ üzerinde iki uç: indirgenmiş topoloji (kaba)
    ile ayrık topoloji (ince). Açık küme eklemek topolojiyi inceltir;
    tüm topolojiler bu iki uç arasında yaşar.}
  \label{fig:ch04:kabaince}
\end{figure}

\noindent\texttt{pytop} bu uçları \texttt{tags} ile işaretler:
\texttt{indiscrete\_topology} nesnesi \texttt{indiscrete},
\texttt{discrete\_topology} nesnesi \texttt{discrete} etiketi taşır.
```

- [ ] **Adım 5.7: İz sürme tablosu** — Algoritmalar bölümünde "Alt-Bazdan Topoloji Üretimi" alt bölümünden ÖNCE:

```latex
\subsection{İz Sürme: Küçük Bir Girdiyle Adım Adım}

$X=\{1,2,3\}$, $\mathcal{B}=\{\{1\},\{2,3\}\}$ girdisiyle
Algoritma~\ref{alg:basis_to_topology}:

\begin{table}[ht]
\centering
\begin{tabular}{clll}
\toprule
\textbf{Adım} & $\mathcal{S}$ (alt-aile) & \textbf{Eklenen birleşim} & $\tau$ \textbf{(o ana dek)} \\
\midrule
0 & --- & --- & $\{\emptyset, X\}$ \\
1 & $\{\{1\}\}$ & $\{1\}$ & $\{\emptyset, X, \{1\}\}$ \\
2 & $\{\{2,3\}\}$ & $\{2,3\}$ & $\{\emptyset, X, \{1\}, \{2,3\}\}$ \\
3 & $\{\{1\},\{2,3\}\}$ & $\{1\}\cup\{2,3\}=X$ & değişmez \\
4 & kesişim kapanışı & $\{1\}\cap\{2,3\}=\emptyset$ & değişmez \\
\bottomrule
\end{tabular}
\caption{İz sürme: $|\tau|=4$; döngü yeni küme üretmeyince durur.}
\end{table}
```

- [ ] **Adım 5.8: Tag gerekçeleri** — "Tag Sistemi" alt bölümünün sonuna (Örnekler bölümünden önce):

```latex
\subsection{Tag Gerekçeleri}

Etiketler, kurucunun inşa anında \emph{garanti ettiği} gerçeklerdir:

\begin{table}[ht]
\centering
\begin{tabular}{lp{4.2cm}p{5.6cm}}
\toprule
\textbf{Kurucu} & \textbf{Etiketler} & \textbf{Gerekçe} \\
\midrule
\texttt{sierpinski\_space()} & compact, connected, finite, t0 &
  Sonlu $\Rightarrow$ kompakt; $\{1\}$ tek yönlü ayırır $\Rightarrow$ T0
  (T1 değil); ayrık parçalanış yok $\Rightarrow$ bağlantılı \\
\texttt{discrete\_topology(1,2,3)} & discrete, finite, hausdorff,
  metrizable, normal, regular &
  Her tekil açık $\Rightarrow$ tüm ayrılma aksiyomları; 0--1 metriği
  ayrık topolojiyi üretir \\
\texttt{indiscrete\_topology(1,2,3)} & compact, connected, finite,
  indiscrete & Açık yalnız $\emptyset$ ve $X$: parçalanamaz \\
\texttt{cofinite\_topology('a','b','c')} & cofinite, compact, finite,
  t1 & Tekiller kapalı $\Rightarrow$ T1 \\
\texttt{make\_topology(\ldots)},
  \texttt{finite\_chain\_space(n)} & finite &
  Özellik çıkarımı yapılmaz; yalnız sonluluk işaretlenir \\
\bottomrule
\end{tabular}
\caption{Pilot bölümdeki kurucuların etiket gerekçeleri}
\end{table}

\noindent Etiketler \emph{eksiksiz değildir}:
\texttt{cofinite\_topology('a','b','c')} aslında ayrıktır ve
Hausdorff'tur ($2^3=8$ açık), ama \texttt{discrete}/\texttt{hausdorff}
etiketi taşımaz --- \texttt{is\_t2} yüklemi yine \texttt{true} döner.
Kesin sorgu için Bölüm~\ref{ch:separation}'daki \texttt{is\_*}
yüklemlerini kullanın; etiket, yüklemin yerine geçmez.
```

- [ ] **Adım 5.9: Örnek 1 sonrası — "Ne oldu?" + şekil**

Örnek 1'in mevcut kapanış cümlesini ("Topoloji tam olarak üç açık küme içerir... kaynağıdır.") şununla DEĞİŞTİR:

```latex
\paragraph{Ne oldu?}
Çıktıdaki üç satırı tek tek okuyalım. \texttt{Tasiyici} satırı
$X=\{0,1\}$'i verir. \texttt{Topoloji} satırındaki üç küme tam olarak
Tanım~\ref{def:topological_space}'in istediği yapıdır: $\emptyset$ ve
$X$ (T1), tek ek açık küme $\{1\}$; $\{1\}\cap X=\{1\}$ ve
$\{1\}\cup X=X$ zaten listede olduğundan (T2)--(T3) de sağlanır.
\texttt{Etiketler} satırında \texttt{t0} var ama \texttt{t1} yok:
$1$'i içerip $0$'ı dışlayan açık küme vardır ($\{1\}$), fakat $0$'ı
içerip $1$'i dışlayan açık küme yoktur --- T0 sağlanıp T1'in
sağlanmamasının kaynağı budur (Bölüm~\ref{ch:separation}, Örnek~1'de
yüklemlerle test edilir). Şekil~\ref{fig:ch04:sierpinski} açık küme
yapısını gösterir.

\begin{figure}[ht]
  \centering
  \input{figures/fig_ch04_sierpinski.tikz}
  \caption{Sierpiński uzayının açıkları: $\emptyset$, $\{1\}$ ve $X$.
    Kesikli bölge $\{0\}$'ın açık \emph{olmadığını} vurgular; bu
    asimetri uzayı T0 yapar ama T1 yapmaz.}
  \label{fig:ch04:sierpinski}
\end{figure}
```

- [ ] **Adım 5.10: Örnek 2–6 sonrası "Ne oldu?" paragrafları**

Her örneğin mevcut kapanış cümlesini aşağıdaki paragrafla DEĞİŞTİR (kapanış cümlesinin bilgisi paragraflara taşınmıştır):

Örnek 2 (mevcut: "$n=3$ için ... metriklenebilirdir."):

```latex
\paragraph{Ne oldu?}
$n=3$ eleman için $|\tau|=2^3=8$: her alt küme açıktır. Her tekil küme
açık olduğundan herhangi iki nokta kendi tekil komşuluklarıyla ayrılır
--- \texttt{hausdorff}, \texttt{normal}, \texttt{regular} etiketlerinin
kaynağı budur. \texttt{metrizable}, 0--1 metriğinden gelir:
$d(x,y)=1$ $(x\neq y)$ metriği tam olarak ayrık topolojiyi üretir.
Listede \texttt{compact} yok; oysa uzay sonlu olduğu için kompakttır ve
\texttt{is\_compact} yüklemi \texttt{true} döner --- fark için Tag
Gerekçeleri tablosuna bakın.
```

Örnek 3 (mevcut: "$\{1\}$ ve $\{2,3\}$ açık verilince ... otomatik eklenir."):

```latex
\paragraph{Ne oldu?}
\texttt{make\_topology} verilen $\{1\}$ ve $\{2,3\}$ açıklarına yalnızca
$\emptyset$ ve $X$'i ekledi; $|\tau|=4$. Bu örnekte sonuç geçerli bir
topolojidir, çünkü verilen iki küme ayrıktır: birleşimleri $X$,
kesişimleri $\emptyset$ zaten ailededir. \texttt{make\_topology} bu
kapanışları \emph{hesaplamaz} --- aşağıdaki kutu, kapalı olmayan bir
aile verildiğinde ne olduğunu gösterir.
```

ve hemen ardından dikkat kutusu + kontrast kodu:

```latex
\begin{dikkat}
\texttt{make\_topology} verdiğiniz aileye yalnızca $\emptyset$ ve $X$'i
ekler; birleşim/kesişim kapanışını \textbf{hesaplamaz} ve aksiyomları
\textbf{denetlemez}. Aşağıdaki çağrıda $\{1\}\cup\{2\}=\{1,2\}$ ailede
yoktur; dönen nesne (T3)'ü ihlal eden, geçersiz bir ``topoloji''dir.
Kapanışın hesaplanmasını ve ailenin denetlenmesini istiyorsanız
\texttt{topology\_from\_basis} kullanın --- o, baz koşullarını
sağlamayan aileyi \texttt{BasisConstructionError} ile reddeder.
\end{dikkat}

\begin{lstlisting}[language=Python, caption={Kapanış hesaplanmaz --- sorumluluk kullanıcıda}]
from pytop import make_topology, topology_from_basis

sessiz = make_topology({1, 2, 3}, {1}, {2})   # denetlemez!
print("make_topology:", sorted(sorted(t) for t in sessiz.topology))

try:
    topology_from_basis({1, 2, 3}, [{1}, {2}])  # B1 ihlali
except Exception as e:
    print("topology_from_basis:", type(e).__name__)
\end{lstlisting}

\begin{lstlisting}[style=output, caption={Çıktı}]
make_topology: [[], [1], [1, 2, 3], [2]]
topology_from_basis: BasisConstructionError
\end{lstlisting}
```

Örnek 4 (mevcut: "Her açık küme bir ``önek''tir. ..."):

```latex
\paragraph{Ne oldu?}
Çıktıdaki açıklar tam bir ``önek merdiveni''dir:
$\emptyset\subset\{1\}\subset\{1,2\}\subset\{1,2,3\}$. Alexandrov zincir
uzayında $1$ her boş olmayan açıkta yer alır (``en açık'' nokta), $3$
yalnız $X$'te görünür. Öneklerin kesişimi ve birleşimi yine önek
olduğundan (T2)--(T3) otomatik sağlanır.
```

Örnek 5 (mevcut: "Baz ... kombinasyonlarından elde edilir."):

```latex
\paragraph{Ne oldu?}
Baz $\{\{1\},\{2,3\},\{4\}\}$ bir bölüntüdür: elemanları ikişer ikişer
ayrıktır. (B2) koşulu boş yere sağlanır (kesişimler boş olduğundan
kontrol edilecek nokta yoktur) ve topoloji tüm alt-aile
birleşimlerinden oluşur: $2^3=8$ açık küme. Çıktıdaki 8 küme, üç baz
elemanının $2^3$ alt kümesinin birleşimleriyle birebir eşleşir.
```

Örnek 6 (mevcut: "Gerçek doğru simgesel temsil edilir; ... kodlanmıştır."):

```latex
\paragraph{Ne oldu?}
\texttt{Tasiyici: R} satırı taşıyıcının \emph{simgesel} olduğunu söyler:
gerçek doğrunun noktaları bellekte tutulmaz, \texttt{topology=None}'dır.
Tüm topolojik bilgi etiketlerde kodlanmıştır: \texttt{connected},
\texttt{hausdorff}, \texttt{second\_countable} gibi olumlu özellikler
yanında \texttt{not\_compact} gibi olumsuz bilgi de taşınır
(Heine--Borel: $\mathbb{R}$ sınırlı değildir). Sonlu uzaylardaki
``hesapla ve doğrula'' yaklaşımının yerini burada ``bilinen teoremleri
etiketle'' yaklaşımı alır; metrik tarafı Bölüm~14'te derinleşir.
```

- [ ] **Adım 5.11: Alıştırmalar — K1 yeniden yazımı, etiketler, ipuçları, çözüm bağlantıları**

Kodlama listesinin tamamını şununla DEĞİŞTİR:

```latex
\begin{enumerate}[label=\textbf{K\arabic*.}]
  \item \label{ex:ch04:K1} \texttt{cofinite\_topology('a','b','c')} ile üç
        noktalı kosonlu uzayı kurun; topolojisini ve etiketlerini
        yazdırın, \texttt{is\_t1} ve \texttt{is\_t2} ile test edin.
        Gözlem: sonlu bir kümede kosonlu topoloji ayrık topolojiyle
        çakışır. T1 olup Hausdorff olmayan bir örnek için taşıyıcının
        neden sonsuz olması gerektiğini bir cümleyle açıklayın
        (krş.\ Bölüm~\ref{ch:separation}, Örnek~2).
        \ipucu{$|\tau|=2^3$ çıkacak; anahtar, Bölüm~\ref{ch:separation}'daki
        ``Sonlu T1 $\iff$ Ayrık'' teoremidir.}
        (\hyperref[sol:ch04:K1]{çözüm})

  \item \label{ex:ch04:K2} \texttt{topology\_from\_subbasis(\{1,2,3,4\},
        [\{1,2\},\{3,4\},\{2,3\}])} çağrısının ürettiği topolojinin kaç
        açık küme içerdiğini bulun ve açık kümeleri listeleyin.
        \ipucu{Önce alt-baz çiftlerinin kesişimlerini elle listeleyin
        ($\{2\}$, $\{3\}$, $\emptyset$); sonra birleşimleri sayın.}
        (\hyperref[sol:ch04:K2]{çözüm})

  \item \label{ex:ch04:K3} \texttt{finite\_chain\_space(5)} ile bir
        Alexandrov-5 zinciri oluşturun; topolojinin kaç açık küme
        içerdiğini ve hangi elemanın ``en açık'' nokta olduğunu bulun.
        \ipucu{Açıklar önek yapısındadır; ``en açık'' nokta her boş
        olmayan açıkta bulunandır.}
        (\hyperref[sol:ch04:K3]{çözüm})
\end{enumerate}
```

Teori listesinin tamamını şununla DEĞİŞTİR:

```latex
\begin{enumerate}[label=\textbf{T\arabic*.}]
  \item \label{ex:ch04:T1} $X=\{1,2,3\}$ üzerinde kaç farklı topoloji
        tanımlanabilir? Bu sayıyı T1--T3 aksiyomlarını doğrudan kontrol
        ederek hesaplamak yerine neden baz teoremini kullanmak daha
        pratiktir?
        \ipucu{Aday aile sayısı $2^{2^3}=256$'dır; cevap 29. Baz teoremi
        adayları üretken küçük ailelere indirger.}
        (\hyperref[sol:ch04:T1]{çözüm})

  \item \label{ex:ch04:T2} Ayrık topolojinin her zaman diğer
        topolojilerden daha ince, indirgenmiş topolojinin ise daha kaba
        olduğunu kanıtlayın. Kanıt için T1--T3 aksiyomlarından hangisi
        gereklidir?
        \ipucu{Ayrıklık için aksiyom gerekmez
        ($\tau\subseteq\mathcal{P}(X)$ tanım gereğidir); indirgenmişlik
        için yalnız (T1) yeter.}
        (\hyperref[sol:ch04:T2]{çözüm})
\end{enumerate}
```

- [ ] **Adım 5.12: Derle, görsel kontrol, commit**

```powershell
cd E:\PYTHON\pytop\docs\user_guide\latex
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

Beklenen: hatasız; Bölüm 4'te 4 şekil, 4 kutu, 6 "Ne oldu?", iz tablosu, tag tablosu görünür. (Çözüm hyperref'leri Görev 7'ye dek `??` görünür — normaldir; Görev 7 derlemesi düzeltir.)

```powershell
git add docs/user_guide/latex/chapters/ch04_topological_spaces.tex
git commit -m "docs(user_guide/latex): enrich ch04 with figures, boxes, walkthroughs, guided proofs, hints"
```

## Görev 6: ch06 LaTeX zenginleştirme

**Files:**
- Modify: `docs/user_guide/latex/chapters/ch06_separation.tex`

- [ ] **Adım 6.1: Sezgi kutusu** — giriş paragrafından (`...ne ölçüde ``ayrılabildiğini'' ölçer.`) sonra:

```latex
\begin{sezgi}
Ayrılma aksiyomlarını bir mikroskobun çözünürlük kademeleri gibi
düşünün: T0'da iki noktayı \emph{en az bir yönden} ayırt edebilirsiniz;
T1'de her iki yönden; T2'de noktaları çakışmayan iki ayrı ``görüş
alanına'' koyabilirsiniz; T3 ve T4'te artık nokta--kapalı küme ve
kapalı--kapalı çiftleri bile ayrışır. Matematiksel karşılığı: her
aksiyom, $\tau$'nun ``ayırma gücü'' üzerine gittikçe güçlenen bir
varsayımdır ve zincir boyunca her adım bir öncekini gerektirir.
\end{sezgi}
```

- [ ] **Adım 6.2: Konvansiyon uyarısı + T2/T3 şekilleri + karşı-örnek** — aksiyom tablosunun ve "Sıralama" satırının ardına:

```latex
\begin{dikkat}
T3 ve T4'ün tanımı kaynaktan kaynağa değişir: bazı kitaplar
``regüler''i T1 olmadan tanımlar. Bu kılavuzda ve \texttt{pytop}'ta
tablodaki konvansiyon geçerlidir: \textbf{T3 = T1 + regüler,
T4 = T1 + normal}. Fark gerçektir: iki noktalı indirgenmiş uzay
regüler \emph{ve} normaldir (ayrılacak uygun çift yoktur), ama T1
olmadığından T3 de T4 de değildir; Örnekler bölümünde
\texttt{is\_regular}/\texttt{is\_t3} ile doğrulanır.
\end{dikkat}

Şekil~\ref{fig:ch06:t2} Hausdorff koşulunu, Şekil~\ref{fig:ch06:t3}
regülerlik koşulunu resmeder.

\begin{figure}[ht]
  \centering
  \input{figures/fig_ch06_t2_ayirma.tikz}
  \caption{T2 (Hausdorff): farklı $x,y$ noktaları, kesişmeyen $U\ni x$
    ve $V\ni y$ açıklarıyla ayrılır.}
  \label{fig:ch06:t2}
\end{figure}

\begin{figure}[ht]
  \centering
  \input{figures/fig_ch06_t3_regulerlik.tikz}
  \caption{Regülerlik: $x$ noktası ile onu içermeyen kapalı $F$ kümesi,
    ayrık $U$ ve $V$ açıklarına konabilir. T3 bunun üstüne T1 ister.}
  \label{fig:ch06:t3}
\end{figure}

\begin{karsiornek}
Hiçbir ayrılma aksiyomunu sağlamayan uzay: iki noktalı indirgenmiş
uzay. Açıklar yalnız $\emptyset$ ve $X$ olduğundan iki noktayı ayıran
\emph{hiçbir} açık yoktur --- uzay T0 bile değildir. Örnekler
bölümünde \texttt{two\_point\_indiscrete\_space()} ile test edilir;
zincirin en altının da boş kalabileceğini gösterir.
\end{karsiornek}
```

- [ ] **Adım 6.3: Ayrılma Zinciri — rehberli kanıt (model halka) + implikasyon şekli** — "Ayrılma Zinciri" teoreminin `\end{theorem}` satırından sonra:

```latex
\begin{proof}[Rehberli Kanıt --- model halka: T2 $\Rightarrow$ T1]
$x\neq y$ verilsin. T2 ile ayrık $U\ni x$, $V\ni y$ açıkları vardır.
$U\cap V=\emptyset$ olduğundan $y\notin U$ ve $x\notin V$: hem
``$x$'i içerip $y$'yi dışlayan'' hem ``$y$'yi içerip $x$'i dışlayan''
açık bulundu --- T1'in iki yönlü koşulu sağlandı. Kalan halkalar
(T1 $\Rightarrow$ T0 dahil) aynı şablonla Alıştırma~T1'de
kanıtlanır.
\end{proof}

\begin{figure}[ht]
  \centering
  \input{figures/fig_ch06_implikasyon.tikz}
  \caption{Ayrılma zinciri: düz oklar implikasyonları gösterir.
    Kesikli kırmızı oklar terslerin \emph{geçmediği} iki kanonik
    karşı-örneği işaretler; her ikisi de bu kılavuzun örnekleridir
    (Örnek~1 ve Örnek~2).}
  \label{fig:ch06:zincir}
\end{figure}
```

- [ ] **Adım 6.4: Urysohn şekli + neden önemli** — Urysohn teoreminin `\end{theorem}` satırından sonra:

```latex
\begin{figure}[ht]
  \centering
  \input{figures/fig_ch06_urysohn.tikz}
  \caption{Urysohn fonksiyonu: normal uzayda ayrık kapalı $C$ ve $D$
    için $f|_C\equiv 0$, $f|_D\equiv 1$ olan sürekli $f:X\to[0,1]$
    vardır; uzay, iki kapalı küme arasında ``sürekli geçiş'' yapacak
    kadar zengindir.}
  \label{fig:ch06:urysohn}
\end{figure}

\begin{nedenonemli}
Urysohn teoremi, küme dilindeki bir ayırma özelliğini (normallik)
\emph{sürekli fonksiyon üretimine} çevirir. Tietze Genişleme bunun
doğrudan sonucudur ve metrikleştirme teoremlerinin (Bölüm~9 sonrası
ufuk) temel aracıdır: fonksiyon üretebilen uzay, metrik benzeri
yapılar kurabilen uzaydır.
\end{nedenonemli}
```

- [ ] **Adım 6.5: "Sonlu T1 ⟺ Ayrık" — iskeleti tam rehberli kanıtla DEĞİŞTİR**

Mevcut `\begin{proof}[İskelet] ... \end{proof}` bloğunu şununla değiştir:

```latex
\begin{proof}[Rehberli Kanıt]
\textbf{Strateji:} T1'den tekillerin kapalılığına, oradan sonlu
birleşimle her alt kümenin kapalılığına yürünür.
\begin{enumerate}
  \item ($\Rightarrow$) T1 gereği her $y\neq x$ için $y\in U_y$,
        $x\notin U_y$ olan açık $U_y$ vardır;
        $X\setminus\{x\}=\bigcup_{y\neq x}U_y$ açıktır, yani $\{x\}$
        kapalıdır.
  \item Herhangi $A\subseteq X$, \emph{sonlu} sayıda tekilin birleşimi
        olarak kapalıdır (kapalıların sonlu birleşimi kapalıdır).
  \item Her $A$ kapalı ise her $X\setminus A$ açıktır; $A$ keyfî
        olduğundan her alt küme açıktır: topoloji ayrıktır.
  \item ($\Leftarrow$) Ayrık topolojide her $\{x\}$ açıktır; $x\neq y$
        çifti $\{x\}$ ve $\{y\}$ ile iki yönlü ayrılır: T1 (hatta T2).
\end{enumerate}
Sonsuzlukta 2.~adım çöker: sonsuz birleşim kapalılığı korumaz ---
kosonlu $\mathbb{N}$ tam bu nedenle T1 olup ayrık değildir.
\end{proof}

\noindent Bu teorem, Bölüm~\ref{ch:topological_spaces} K1
alıştırmasındaki gözlemin --- üç noktalı kosonlu uzayın ayrık çıkması
--- genel açıklamasıdır.
```

- [ ] **Adım 6.6: İz sürme tablosu** — Algoritmalar bölümünde karmaşıklık satırından sonra:

```latex
\subsection{İz Sürme: T0 Prosedürü Sierpiński Üzerinde}

$X=\{0,1\}$, $\tau=\{\emptyset,\{1\},X\}$:

\begin{table}[ht]
\centering
\begin{tabular}{llccl}
\toprule
\textbf{Çift} $(x,y)$ & \textbf{Denenen} $U$ &
$x\in U \wedge y\notin U$ & $y\in U \wedge x\notin U$ & \textbf{Karar} \\
\midrule
$(0,1)$ & $\emptyset$ & hayır & hayır & devam \\
$(0,1)$ & $\{1\}$ & hayır & \textbf{evet} & çift ayrıldı \\
--- & --- & --- & --- & tüm çiftler bitti $\to$ \textbf{true} \\
\bottomrule
\end{tabular}
\caption{Tek çift tek açıkla ayrılır; genel sınır
  $O(|X|^2\cdot|\tau|)$'dur.}
\end{table}
```

- [ ] **Adım 6.7: Result tipi kutusu** — pytop API bölümünde fonksiyon tablosunun ardına:

```latex
\begin{nedenonemli}
\texttt{is\_*} yüklemleri ham \texttt{bool} değil, \texttt{.status}
alanı \texttt{true} / \texttt{false} / \texttt{unknown} olabilen bir
\texttt{Result} döndürür. Üçüncü değer dürüstlüktür: örneğin T3.5
(Tychonoff) sürekli fonksiyonlarla tanımlanır ve sonlu açık-küme
taramasıyla karar verilemez; \texttt{separation\_chain} bu durumda
\texttt{tychonoff: unknown} raporlar. Sembolik uzaylarda da
bilinmeyen özellikler \texttt{unknown} kalır --- kütüphane bilmediğini
\emph{bilmediğini söyleyerek} belirtir.
\end{nedenonemli}
```

- [ ] **Adım 6.8: Örnek 1–3 "Ne oldu?" + Örnek 3 tam çıktı**

Örnek 1'in çıktı bloğundan sonra ekle:

```latex
\paragraph{Ne oldu?}
\texttt{T0: true} --- $(0,1)$ çifti için $\{1\}$ açığı $1$'i içerir,
$0$'ı dışlar; tek çift bu olduğundan T0 tamam. \texttt{T1: false} ---
ters yön yok: $0$'ı içerip $1$'i dışlayan açık küme yoktur
($\{0\}\notin\tau$; bkz.\ Bölüm~\ref{ch:topological_spaces},
Örnek~1). T1 düşünce T2 de düşer. Sierpiński, zincirin ``T0'da
takılan'' kanonik örneğidir (Şekil~\ref{fig:ch06:zincir}).
```

Örnek 2'nin çıktı bloğundan sonra ekle:

```latex
\paragraph{Ne oldu?}
\texttt{T1: true} --- her $n$ için $\mathbb{N}\setminus\{n\}$
kosonludur, dolayısıyla açıktır; bu, her noktayı diğerinden iki yönlü
ayırır. \texttt{T2: false} --- boş olmayan iki kosonlu açık $U,V$
daima kesişir: $\mathbb{N}\setminus(U\cap V)=
(\mathbb{N}\setminus U)\cup(\mathbb{N}\setminus V)$ iki sonlu kümenin
birleşimi olarak sonludur; $\mathbb{N}$ sonsuz olduğundan
$U\cap V\neq\emptyset$. Bu örnek,
Bölüm~\ref{ch:topological_spaces}~K1'in ``neden sonsuz taşıyıcı
gerekir'' sorusunun cevabıdır.
```

Örnek 3'te `caption={Çıktı (kısa)}` bloğunu şu TAM çıktıyla değiştir (caption `{Çıktı}` olur):

```latex
\begin{lstlisting}[style=output, caption={Çıktı}]
  t0                  : true
  t1                  : true
  hausdorff           : true
  urysohn             : true
  t3                  : true
  tychonoff           : true
  t4                  : true
  completely_normal   : true
  perfectly_normal    : true
\end{lstlisting}

\paragraph{Ne oldu?}
Ayrık uzayda her tekil açık olduğundan her ayırma görevi tekil
komşuluklarla çözülür; dokuz yüklemin tümü \texttt{true} döner.
\texttt{tychonoff} bile \texttt{true}'dur: ayrık uzayda her fonksiyon
süreklidir, ayırıcı fonksiyon doğrudan yazılır.
\texttt{separation\_chain}'in anahtar sırası zincirin mantıksal
sırasıdır --- bir uzayın ``nerede takıldığını'' yukarıdan aşağı
okuyabilirsiniz (krş.\ Alıştırma~K2).
```

Hemen ardından konvansiyon doğrulama örneği olarak ekle (CB-16 kodu):

```latex
\subsection{Örnek 4: Regüler Ama T3 Değil --- Konvansiyon Testi}

\begin{lstlisting}[language=Python]
from pytop import two_point_indiscrete_space, is_regular, is_normal, is_t3, is_t4

tp = two_point_indiscrete_space()
print("regular:", is_regular(tp).status, "| normal:", is_normal(tp).status)
print("t3     :", is_t3(tp).status, "| t4    :", is_t4(tp).status)
\end{lstlisting}

\begin{lstlisting}[style=output, caption={Çıktı}]
regular: true | normal: true
t3     : false | t4    : false
\end{lstlisting}

\paragraph{Ne oldu?}
İndirgenmiş iki noktalı uzayda kapalı kümeler yalnız $\emptyset$ ve
$X$'tir; ``nokta--kapalı'' ve ``kapalı--kapalı'' ayırma koşullarının
öncülü hiç gerçekleşmez, koşullar boş yere sağlanır:
\texttt{regular} ve \texttt{normal} \texttt{true}. Ama uzay T1
olmadığından (tekiller kapalı değil) \texttt{t3} ve \texttt{t4}
\texttt{false} kalır --- ``Dikkat'' kutusundaki konvansiyonun
davranışsal kanıtı.
```

- [ ] **Adım 6.9: Alıştırmalar — etiketler, ipuçları, çözüm bağlantıları**

Kodlama listesini şununla DEĞİŞTİR:

```latex
\begin{enumerate}[label=\textbf{K\arabic*.}]
  \item \label{ex:ch06:K1} \texttt{make\_topology(\{1,2,3\},\{1\},\{2\},\{1,2\})}
        için \texttt{separation\_chain} çalıştırın; her sonucu yorumlayın.
        \ipucu{Önce açıkları listeleyin:
        $\emptyset,\{1\},\{2\},\{1,2\},X$. Her çifti ayıran açık
        arayın; $3$'ü içerip $1$'i dışlayan açık var mı?}
        (\hyperref[sol:ch06:K1]{çözüm})

  \item \label{ex:ch06:K2} \texttt{finite\_chain\_space(3)} üzerinde en
        yüksek sağlanan aksiyomu bulun.
        \ipucu{Çıktıda \texttt{true} olan en güçlü anahtarı arayın;
        \texttt{unknown} değerlerini ``Neden önemli?'' kutusuna göre
        yorumlayın.}
        (\hyperref[sol:ch06:K2]{çözüm})

  \item \label{ex:ch06:K3} \texttt{two\_point\_indiscrete\_space()}
        üzerinde T0, T1, T2 test edin.
        \ipucu{Tek boş olmayan açık $X$ iken herhangi bir çift nasıl
        ayrılabilir?}
        (\hyperref[sol:ch06:K3]{çözüm})
\end{enumerate}
```

Teori listesini şununla DEĞİŞTİR:

```latex
\begin{enumerate}[label=\textbf{T\arabic*.}]
  \item \label{ex:ch06:T1} T2 $\Rightarrow$ T1 $\Rightarrow$ T0
        implikasyonlarını kanıtlayın.
        \ipucu{T2 $\Rightarrow$ T1: ayrık $U\ni x$, $V\ni y$
        verildiğinde $U$, $y$'yi; $V$, $x$'i dışlar --- iki yönlü ayrım
        hazır. T1 $\Rightarrow$ T0: iki yönlü ayrım tek yönlüyü içerir.}
        (\hyperref[sol:ch06:T1]{çözüm})

  \item \label{ex:ch06:T2} Sonlu uzayda T1 $\iff$ ayrık topoloji
        olduğunu gösterin.
        \ipucu{T1 $\Rightarrow$ tekiller kapalı $\Rightarrow$ (sonlu
        birleşim) her alt küme kapalı $\Rightarrow$ her alt küme açık.}
        (\hyperref[sol:ch06:T2]{çözüm})
\end{enumerate}
```

- [ ] **Adım 6.10: Yeni Örnek 4'ü doğrula, derle, commit**

Önce yeni örneğin çıktısını birebir doğrula:

```powershell
py -3.14 -c "from pytop import two_point_indiscrete_space, is_regular, is_normal, is_t3, is_t4; tp = two_point_indiscrete_space(); print('regular:', is_regular(tp).status, '| normal:', is_normal(tp).status); print('t3     :', is_t3(tp).status, '| t4    :', is_t4(tp).status)"
```

Beklenen: `regular: true | normal: true` ve `t3     : false | t4    : false`.

```powershell
cd E:\PYTHON\pytop\docs\user_guide\latex
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
git add chapters/ch06_separation.tex
git commit -m "docs(user_guide/latex): enrich ch06 with figures, convention warning, Result box, walkthroughs, full proofs"
```

## Görev 7: Çözüm eki (LaTeX)

**Files:**
- Modify: `docs/user_guide/latex/appendix/solutions.tex`

- [ ] **Adım 7.1: Çözüm kodlarını çalıştırıp çıktıları teyit et**

CB-25 ve CB-26'daki beş kod bloğunu sırayla `py -3.14 -` ile çalıştır; çıktının CB'dekiyle BİREBİR aynı olduğunu doğrula. Fark varsa CB'yi değil gerçeği esas al ve bu planda not düş.

- [ ] **Adım 7.2: solutions.tex'e Bölüm 4 ve Bölüm 6 kısımlarını ekle**

Görev 1'deki giriş paragrafının altına, CB-25/CB-26 içeriğinin LaTeX'i. Şablon (her çözüm için aynı desen; tamamı yazılır):

```latex
\section{Bölüm 4 --- Topolojik Uzaylar}

\subsection*{K1}\label{sol:ch04:K1}

\begin{lstlisting}[language=Python]
from pytop import cofinite_topology, is_t1, is_t2
c = cofinite_topology('a', 'b', 'c')
print("|tau| =", len(c.topology))
print("Etiketler:", sorted(c.tags))
print("T1:", is_t1(c).status, "| T2:", is_t2(c).status)
\end{lstlisting}

\begin{lstlisting}[style=output, caption={Çıktı}]
|tau| = 8
Etiketler: ['cofinite', 'compact', 'finite', 't1']
T1: true | T2: true
\end{lstlisting}

Üç elemanlı kümede tümleyeni sonlu olan \emph{her} alt küme kosonlu
koşulunu sağlar; $|\tau|=2^3=8=|\mathcal{P}(X)|$: topoloji ayrıktır.
Sonlu kümede T1 $\Rightarrow$ tekiller kapalı $\Rightarrow$ her alt
küme kapalı $\Rightarrow$ her alt küme açık; T1 olan sonlu uzay
zorunlu olarak ayrık, dolayısıyla Hausdorff'tur. T1 olup T2 olmayan
örnek için taşıyıcı sonsuz olmalıdır: kosonlu $\mathbb{N}$'de boş
olmayan iki açık daima kesişir (Bölüm~\ref{ch:separation}, Örnek~2).
\hfill(\hyperref[ex:ch04:K1]{alıştırmaya dön})
```

Aynı desenle sırasıyla: **K2** (CB-25 K2 kodu+çıktısı+açıklaması, `\label{sol:ch04:K2}`), **K3** (`sol:ch04:K3`), **T1** (`sol:ch04:T1`, yalnız metin: CB-25 T1 paragrafı), **T2** (`sol:ch04:T2`, CB-25 T2 paragrafı; $\square$ ile bitir). Ardından:

```latex
\section{Bölüm 6 --- Ayrılma Aksiyomları}
```

altında **K1** (`sol:ch06:K1`, CB-26 K1 kodu + 9 satırlık tam çıktı + açıklama), **K2** (`sol:ch06:K2`), **K3** (`sol:ch06:K3`), **T1** (`sol:ch06:T1`, CB-26 T1 metni), **T2** (`sol:ch06:T2`, CB-26 T2 metni). Her çözüm `\hfill(\hyperref[ex:...]{alıştırmaya dön})` ile biter; matematik gösterimi CB'lerdeki gibi ($\LaTeX$'e çevrilmiş: `**...**` → `\textbf`, backtick → `\texttt`).

- [ ] **Adım 7.3: Derle (2×), çapraz bağlantıları doğrula, commit**

```powershell
cd E:\PYTHON\pytop\docs\user_guide\latex
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

Beklenen: hatasız; `main.log` içinde "undefined references" UYARISI YOK (`Get-Content main.log | Select-String 'undefined'` boş döner). PDF'te Bölüm 4 alıştırmasındaki "(çözüm)" tıklaması Ek A'ya gider.

```powershell
git add appendix/solutions.tex
git commit -m "docs(user_guide/latex): add verified solutions for ch04 and ch06 exercises"
```

## Görev 8: Markdown senkronu (ch04 + ch06)

**Files:**
- Modify: `docs/user_guide/markdown/ch04_topological_spaces.md`
- Modify: `docs/user_guide/markdown/ch06_separation.md`

Kurallar: CB blokları OLDUĞU GİBİ kullanılır (markdown zaten kaynak biçim). LaTeX `\ref`'leri düz metne çevrilmiştir (CB'lerde hazır). Şekiller CB-24 satırlarıyla gömülür. Bölüm yapısı (başlık numaraları `### 1.1` stili) korunur.

- [ ] **Adım 8.1: ch04.md eklemeleri** (yukarıdan aşağı):

| Çapa (mevcut metin) | Eklenecek/Değiştirilecek |
|---------------------|--------------------------|
| §1.1 son paragraf (`...mümkündür.`) sonrası | CB-01 |
| §1.2 aksiyom tablosu sonrası | CB-02 + CB-03 |
| §1.4 Baz tanımı sonrası | CB-24 "baz tanımı" satırı + CB-04 |
| §2 Baz Teoremi "Kanıt İskeleti" paragrafı (satır ~81) | ŞUNUNLA DEĞİŞTİR: `**Rehberli Kanıt:** (T1) ∅ için koşul boş yere doğru; X için (B1) her x'i bir B içine koyar. (T2) x ∈ U∩V için B_U, B_V seç; (B2)'nin verdiği B₃ ⊆ B_U∩B_V ⊆ U∩V. (T3) x ∈ ⋃U_α ise x'in U_α₀'daki baz elemanı birleşim için de iş görür. Bu teorem, topology_from_basis çıktısının topoloji olmasının güvencesidir; koşulları sağlamayan aile BasisConstructionError ile reddedilir.` |
| §2 Karşılaştırma teoremi sonrası | CB-24 "kaba–ince" satırı |
| §3 Algoritmalar sonu | CB-12 |
| §4 (pytop API) sonu | CB-13 |
| §5 Örnek 1 mevcut kapanış cümlesi | CB-05 ile DEĞİŞTİR + ardından CB-24 "Sierpiński" satırı |
| §5 Örnek 2 kapanış cümlesi | CB-06 ile DEĞİŞTİR |
| §5 Örnek 3 kapanış cümlesi | CB-07 ile DEĞİŞTİR + CB-11 |
| §5 Örnek 4 kapanış cümlesi | CB-08 ile DEĞİŞTİR |
| §5 Örnek 5 kapanış cümlesi | CB-09 ile DEĞİŞTİR |
| §5 Örnek 6 kapanış cümlesi | CB-10 ile DEĞİŞTİR |
| §2 Yeterlilik teoremi sonrası | CB-24 "sonsuz kesişim" satırı |
| §6 K1 maddesi | CB-14'teki yeni K1 metniyle DEĞİŞTİR |
| §6 her madde altı | CB-14 ipucu satırları + `*(Çözüm: [solutions.md](solutions.md) → Bölüm 4 / K1)*` biçimli bağlantılar |

- [ ] **Adım 8.2: ch06.md eklemeleri:**

| Çapa | Ekleme |
|------|--------|
| Giriş paragrafı sonrası | CB-15 |
| Aksiyom tablosu + sıralama satırı sonrası | CB-16 (kod ve çıktı bloklarıyla) + CB-24 "T2 ayırma" ve "T3 regülerlik" satırları + CB-17 |
| Ayrılma Zinciri teoremi sonrası | `**Rehberli Kanıt (model halka, T2 ⇒ T1):** x≠y için ayrık U∋x, V∋y al; U∩V=∅ olduğundan y∉U ve x∉V — iki yönlü ayrım hazır. Kalan halkalar Alıştırma T1'de.` + CB-24 "implikasyon" satırı |
| Urysohn teoremi sonrası | CB-24 "Urysohn" satırı |
| "Sonlu T1 ⟺ Ayrık" iskelet kanıtı | Görev 6 Adım 6.5'teki 4 adımın markdown'a düzleştirilmiş hâliyle DEĞİŞTİR (numaralı liste, aynı cümleler, `\(...\)` yerine `$...$`) |
| Algoritma karmaşıklık satırı sonrası | CB-22 |
| API tablosu sonrası | CB-18 |
| Örnek 1 çıktısı sonrası | CB-19 |
| Örnek 2 çıktısı sonrası | CB-20 |
| Örnek 3 "Çıktı (kısa)" bloğu | CB-21 (tam çıktı + Ne oldu) ile DEĞİŞTİR |
| Örnek 3 sonrası | Yeni "Örnek 4" alt bölümü: CB-16'daki kod + çıktı + Görev 6 Adım 6.8'deki "Ne oldu?" metninin düz markdown'ı |
| §Alıştırmalar | CB-23 ipuçları + çözüm bağlantıları (`solutions.md → Bölüm 6 / K1`) |

- [ ] **Adım 8.3: Önizleme doğrulaması ve commit**

İki dosyada tüm `![...](...)` yollarının `../assets/...` ile başladığını doğrula:

```powershell
Select-String -Path docs\user_guide\markdown\ch04_topological_spaces.md, docs\user_guide\markdown\ch06_separation.md -Pattern '!\[' | ForEach-Object Line
```

Beklenen: 8 satır, hepsi `](../assets/ch0X/fig_...png)` içerir. Sonra:

```powershell
git add docs/user_guide/markdown/ch04_topological_spaces.md docs/user_guide/markdown/ch06_separation.md
git commit -m "docs(user_guide/markdown): sync ch04+ch06 enrichment (boxes, figures, walkthroughs, hints)"
```

## Görev 9: Python script senkronu (ch04 + ch06)

**Files:**
- Modify: `docs/user_guide/python/ch04_topological_spaces.py`
- Modify: `docs/user_guide/python/ch06_separation.py`

Kurallar: Her metinsel CB, mevcut dosya stilinde bir hücre olur:

```python
# %% [markdown]
"""
<CB içeriği aynen; emoji ve blockquote işareti korunur>
"""
```

Görüntü gömülmez; CB-24'ün script notu (`(Sekil: assets/...)`) ilgili markdown hücresinin sonuna eklenir. KOD içeren CB'lerde (CB-11, CB-16 ve ch06 yeni Örnek 4) kod ayrı `# %%` hücresi olur ve **çalışır durumda** eklenir (print'ler ASCII). Ekleme konumları Görev 8'deki çapa tablolarının py karşılıklarıdır (aynı bölüm başlıkları dosyada `## N.` hücreleri olarak mevcuttur). Alıştırma hücresinde K1 metni CB-14'le değiştirilir; ipuçları `Ipucu:` satırları olarak eklenir (ASCII).

- [ ] **Adım 9.1: ch04.py'ye ekle** — Görev 8.1 tablosundaki sırayla; CB-11 kodu şu hücre olarak:

```python
# %%
from pytop import make_topology, topology_from_basis

sessiz = make_topology({1, 2, 3}, {1}, {2})   # denetlemez, kapanis hesaplamaz
print("make_topology:", sorted(sorted(t) for t in sessiz.topology))

try:
    topology_from_basis({1, 2, 3}, [{1}, {2}])  # B1 ihlali: 3 ortulmuyor
except Exception as e:
    print("topology_from_basis:", type(e).__name__)
```

- [ ] **Adım 9.2: ch06.py'ye ekle** — Görev 8.2 tablosundaki sırayla; CB-16 kodu + yeni Örnek 4 şu hücre olarak:

```python
# %%
from pytop import two_point_indiscrete_space, is_regular, is_normal, is_t3, is_t4

tp = two_point_indiscrete_space()
print("regular:", is_regular(tp).status, "| normal:", is_normal(tp).status)
print("t3     :", is_t3(tp).status, "| t4    :", is_t4(tp).status)
```

- [ ] **Adım 9.3: Script'leri uçtan uca çalıştır**

```powershell
py -3.14 docs/user_guide/python/ch04_topological_spaces.py
py -3.14 docs/user_guide/python/ch06_separation.py
```

Beklenen: ikisi de hatasız biter; yeni hücrelerin çıktıları CB-11/CB-16'daki çıktı bloklarıyla birebir aynıdır.

- [ ] **Adım 9.4: Commit**

```powershell
git add docs/user_guide/python/ch04_topological_spaces.py docs/user_guide/python/ch06_separation.py
git commit -m "docs(user_guide/python): sync ch04+ch06 enrichment cells (boxes, walkthroughs, pitfall demos, hints)"
```

## Görev 10: Notebook senkronu (ch04 + ch06)

**Files:**
- Modify: `docs/user_guide/notebook/ch04_topological_spaces.ipynb`
- Modify: `docs/user_guide/notebook/ch06_separation.ipynb`

- [ ] **Adım 10.1: Hücreleri ekle (NotebookEdit ile)**

Her notebook'u Read ile aç (hücre kimliklerini gör); Görev 9'da py dosyalarına eklenen HER hücrenin birebir karşılığını aynı sıra konumuna ekle: metinsel CB'ler markdown hücresi, kod CB'leri kod hücresi. Şekiller: CB-24 markdown satırları (`![...](../assets/...)`) kendi markdown hücreleri olarak, Görev 8'deki çapa konumlarına. Alıştırma hücresinde K1 + ipuçları güncellenir.

- [ ] **Adım 10.2: Çalıştırarak doğrula**

```powershell
py -3.14 -m jupyter nbconvert --to notebook --execute --inplace docs/user_guide/notebook/ch04_topological_spaces.ipynb
py -3.14 -m jupyter nbconvert --to notebook --execute --inplace docs/user_guide/notebook/ch06_separation.ipynb
```

Beklenen: ikisi de hatasız. `ModuleNotFoundError: pytop` çıkarsa kernel uyuşmazlığı vardır; şu iki komutla pytop'lu çekirdeği kaydet ve nbconvert'i `--ExecutePreprocessor.kernel_name=pytop314` ekiyle tekrarla:

```powershell
py -3.14 -m pip install ipykernel
py -3.14 -m ipykernel install --user --name pytop314 --display-name "Python 3.14 (pytop)"
```

- [ ] **Adım 10.3: Commit**

```powershell
git add docs/user_guide/notebook/ch04_topological_spaces.ipynb docs/user_guide/notebook/ch06_separation.ipynb
git commit -m "docs(user_guide/notebook): sync ch04+ch06 enrichment cells and refresh outputs"
```

## Görev 11: Çözüm dosyaları (md + py + ipynb) ve dönüştürücü

**Files:**
- Create: `docs/user_guide/markdown/solutions.md`
- Create: `docs/user_guide/python/solutions.py`
- Create: `docs/user_guide/tools/percent_to_ipynb.py`
- Create: `docs/user_guide/notebook/solutions.ipynb`

- [ ] **Adım 11.1: solutions.md** — yapı:

```markdown
# Alıştırma Çözümleri

Kodlama çözümlerindeki tüm çıktılar gerçek çalıştırmadan alınmıştır.
Pilot kapsamında Bölüm 4 ve Bölüm 6 çözümleri yer alır.

## Bölüm 4 — Topolojik Uzaylar

### K1
<CB-25 K1: kod + çıktı + açıklama>
### K2 ... ### K3 ... ### T1 ... ### T2 ...

## Bölüm 6 — Ayrılma Aksiyomları

### K1 ... ### K2 ... ### K3 ... ### T1 ... ### T2 ...
```

İçerik birebir CB-25 ve CB-26'dan alınır (zaten markdown).

- [ ] **Adım 11.2: solutions.py** — `# %% [markdown]` hücre düzeniyle: başlık hücresi, sonra her çözüm için bir markdown hücresi (soru başlığı + açıklama metni) ve kodlama çözümlerinde bir `# %%` kod hücresi (CB-25/CB-26 kodları aynen; teori çözümleri yalnız markdown hücresi). Dosya sonuna `if __name__` bloğu KONMAZ. Çalıştır:

```powershell
py -3.14 docs/user_guide/python/solutions.py
```

Beklenen: hatasız; 6 kod hücresinin çıktıları CB'lerdekiyle birebir aynı.

- [ ] **Adım 11.3: percent_to_ipynb.py dönüştürücüsünü yaz**

```python
"""Yuzde-hucre (.py) dosyasini .ipynb'ye cevirir.

Yalniz bu depodaki hucre stilini taniyor:
  '# %% [markdown]' + hemen ardindan uclu-tirnak blogu -> markdown hucresi
  '# %%'                                               -> kod hucresi

Kullanim:
    py -3.14 docs/user_guide/tools/percent_to_ipynb.py <girdi.py> <cikti.ipynb>
"""
from __future__ import annotations

import re
import sys

import nbformat as nbf

CELL_RE = re.compile(r"^# %%( \[markdown\])?[ \t]*$", re.M)
MD_BODY_RE = re.compile(r'^\s*(?:r?)"""\n?(.*?)\n?"""\s*$', re.S)


def parse_cells(text: str):
    cells = []
    parts = CELL_RE.split(text)
    # parts: [on-soz, marker1, govde1, marker2, govde2, ...]
    it = iter(parts[1:])
    for marker, body in zip(it, it):
        body = body.strip("\n")
        if marker:  # markdown hucresi
            m = MD_BODY_RE.match(body)
            cells.append(nbf.v4.new_markdown_cell(m.group(1) if m else body))
        elif body.strip():
            cells.append(nbf.v4.new_code_cell(body))
    return cells


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit("Kullanim: percent_to_ipynb.py <girdi.py> <cikti.ipynb>")
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, encoding="utf-8") as f:
        text = f.read()
    nb = nbf.v4.new_notebook()
    nb.cells = parse_cells(text)
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3", "language": "python", "name": "python3",
    }
    nbf.write(nb, dst)
    print(f"{dst}: {len(nb.cells)} hucre")


if __name__ == "__main__":
    main()
```

- [ ] **Adım 11.4: solutions.ipynb'yi üret ve çalıştır**

```powershell
py -3.14 docs/user_guide/tools/percent_to_ipynb.py docs/user_guide/python/solutions.py docs/user_guide/notebook/solutions.ipynb
py -3.14 -m jupyter nbconvert --to notebook --execute --inplace docs/user_guide/notebook/solutions.ipynb
```

Beklenen: ilk komut `solutions.ipynb: N hucre` yazar (N ≈ 22: 1 başlık + 10 çözüm md + 6 kod + ara başlıklar); ikincisi hatasız biter (kernel sorununda Görev 10.2'deki çare).

- [ ] **Adım 11.5: Commit**

```powershell
git add docs/user_guide/markdown/solutions.md docs/user_guide/python/solutions.py docs/user_guide/tools/percent_to_ipynb.py docs/user_guide/notebook/solutions.ipynb
git commit -m "docs(user_guide): add cross-format exercise solutions and percent-to-ipynb converter"
```

## Görev 12: README güncellemesi + uçtan uca doğrulama

**Files:**
- Modify: `docs/user_guide/README.md`

- [ ] **Adım 12.1: README'ye yeni bölümler ekle**

"Bölüm Yapısı" başlığından sonra şu yeni bölümü ekle:

```markdown
---

## Zenginleştirilmiş Öğeler (pilot: Bölüm 4 ve 6)

- **Pedagojik kutular:** Sezgi 💡, Dikkat ⚠️, Neden önemli? 🎯, Karşı-örnek 🚫
  (LaTeX'te renkli tcolorbox; Markdown/Notebook'ta blockquote).
- **Şekiller:** Kaynak `latex/figures/*.tikz`; PNG türevleri `assets/chNN/`
  altındadır ve Markdown/Notebook'a gömülüdür. Yeniden üretmek için:

  ```bash
  python docs/user_guide/tools/build_figures.py   # xelatex + pdftoppm gerektirir
  ```

  PNG'ler elle düzenlenmez; tek kaynak `.tikz` dosyalarıdır.
- **"Ne oldu?" çözümlemeleri:** Her örneğin çıktısı satır satır açıklanır.
- **İpuçları ve çözümler:** Alıştırmaların ipuçları bölüm içinde; tam
  çözümler `latex/appendix/solutions.tex` (PDF'te Ek A), `markdown/solutions.md`,
  `python/solutions.py` ve `notebook/solutions.ipynb` dosyalarındadır.
```

"LaTeX Derleme" bölümündeki açıklamayı şununla DEĞİŞTİR (xelatex iki kez + şekil notu):

```markdown
## LaTeX Derleme

```bash
cd docs/user_guide/latex
xelatex main.tex
xelatex main.tex   # çapraz referanslar için ikinci geçiş
```

Şekiller bölüm dosyalarına `\input{figures/*.tikz}` ile gömülüdür; ayrıca
derleme gerekmez. Türkçe için XeLaTeX + polyglossia kullanılmaktadır.
```

- [ ] **Adım 12.2: Uçtan uca doğrulama (spec §12 Definition of Done)**

```powershell
cd E:\PYTHON\pytop\docs\user_guide\latex
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
Get-Content main.log | Select-String 'undefined|^!'
cd E:\PYTHON\pytop
py -3.14 docs/user_guide/python/ch04_topological_spaces.py
py -3.14 docs/user_guide/python/ch06_separation.py
py -3.14 docs/user_guide/python/solutions.py
py -3.14 docs/user_guide/tools/build_figures.py
Select-String -Path docs\user_guide\markdown\*.md -Pattern '\]\(\.\./assets/' | Measure-Object | ForEach-Object Count
```

Beklenen: log taraması boş; üç script hatasız; build_figures `Tamam: 8 sekil.`; son sayım ≥ 8. PDF'i Read ile aç (sayfa örnekleri): kutular renkli ve sayfa kırılımlarında düzgün, şekiller yerinde, Ek A bağlantıları çalışıyor.

- [ ] **Adım 12.3: Commit**

```powershell
git add docs/user_guide/README.md docs/user_guide/latex/main.pdf
git commit -m "docs(user_guide): document enriched elements and figure pipeline in README; final pilot build"
```

Not: `main.pdf` depoda izlendiği için güncel derlemeyi bu commit'e dahil et (`main.aux/log/out/toc` zaten izleniyorsa onlar da `git add -u docs/user_guide/latex` ile eklenebilir).

- [ ] **Adım 12.4: Pilot bitti — gözden geçirme**

`superpowers:requesting-code-review` akışına geçmeden önce dal özetini çıkar:

```powershell
git log --oneline master..HEAD
git diff --stat master..HEAD
```

Beklenen: ~12 commit; değişiklikler yalnız `docs/` altında (src/pytop'a dokunulmamış — spec kapsam dışı kuralı).

---

## Plan Öz-Değerlendirme Kontrolü (spec ↔ plan eşlemesi)

| Spec gereği | Görev |
|-------------|-------|
| §6 preamble (4 kutu, tikz, \ipucu, appendix) | 1 |
| §10 build_figures.py + kurallar | 2 |
| §8 sekiz şekil | 2, 3, 4 |
| §7 kontrol listesi: sezgi/karşı-örnek/dikkat/nedenonemli | 5.1–5.3, 5.10 (ch04); 6.1, 6.2, 6.4, 6.7 (ch06) |
| §7 rehberli kanıtlar + API köprüleri | 5.4–5.6, 6.3, 6.5 |
| §7 iz sürme tabloları | 5.7, 6.6 |
| §7 tag gerekçe tablosu | 5.8 (ch04); **bilinçli sapma:** ch06'nın API bölümü kurucular değil `is_*` yüklemleri üzerinedir; tag tablosunun karşılığı olarak Result tipi davranış kutusu (6.7) konur — spec'in "API davranış gerekçesi" amacı bu şekilde karşılanır |
| §7 "Ne oldu?" her örneğe | 5.9–5.10, 6.8 |
| §7 ipucu + çözüm | 5.11, 6.9, 7 |
| §9 format eşleme | 8, 9, 10, 11 |
| §11 çözüm dosyaları (4 format) | 7, 11 |
| §12 doğrulama | her görevin son adımları + 12.2 |
| §13 dal/kapsam | Ortam notları + 12.4 |
| Spec doğruluk kuralı (çıktılar gerçek) | "Doğrulanmış API Gerçekleri" tablosu + 7.1, 9.3, 10.2, 11.2 |
