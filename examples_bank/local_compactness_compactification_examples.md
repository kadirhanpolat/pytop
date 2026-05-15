# Local compactness and compactification examples — v0.1.56

Bu dosya, Cilt III v0.1.56 yerel kompaktlık ve kompaktlaştırma koridoru için durable örnek ailesini bir araya getirir.  Her örnek `local_compactness_profile` ve `analyze_local_compactness` API'siyle tutarlı olacak şekilde etiketlenmiştir.

---

## 1. Temel örnekler

### 1.1 Sonlu ayrık uzay (`{a, b}`, ayrık topoloji)

- **Yerel kompaktlık:** Her sonlu uzay kompakttır; dolayısıyla her noktanın kompakt zarflaması mevcuttur. `is_locally_compact` → `true` (exact).
- **Hausdorff:** Ayrık topoloji her tekil kümeyi açık yapar; Hausdorff koşulu sağlanır.
- **Alexandroff uygunluğu:** Uzay zaten kompakt olduğundan `alexandroff_point_check` → `false`.
- **Pedagojik not:** `one_point_compactification` yine de çağrılabilir; `∞` noktası eklenerek pedagojik örnekleme yapılabilir.

### 1.2 Reel doğru $\mathbb{R}$ (standart topoloji)

- **Yerel kompaktlık:** Her $x \in \mathbb{R}$ için $[x-1, x+1]$ kompakt bir zarflamadır. `locally_compact` etiketi → `true` (theorem).
- **Hausdorff:** Açık aralıklar iki farklı noktayı ayırır.
- **Kompaktlık:** $\mathbb{R}$ kompakt değildir (sonsuz açık örtüler vardır).
- **Alexandroff uygunluğu:** Yerel kompakt, Hausdorff, kompakt olmayan → `alexandroff_eligible` → `true`.
- **Kompaktlaştırma:** $\mathbb{R} \cup \{\infty\}$ çembere (S¹) özdeşbiçimlidir.

### 1.3 $\mathbb{R}^n$ ($n \geq 1$, standart topoloji)

- **Yerel kompaktlık:** Her noktanın $\varepsilon$-top kapaması kompakttır (Heine-Borel). `locally_compact` etiketi → `true` (theorem).
- **Kompaktlaştırma:** $n = 1$ için S¹, $n = 2$ için S² vb.

### 1.4 Sonsuz ayrık uzay ($X$ sayılabilir, ayrık topoloji)

- **Yerel kompaktlık:** Tekil kümeler hem açık hem kompakttır; her noktanın kompakt açık komşuluğu vardır.
- **Hausdorff:** Ayrık topoloji her iki noktayı ayırır.
- **Kompaktlık:** Sonsuz ayrık uzay kompakt değildir.
- **Alexandroff uygunluğu:** `true`.
- **`∞` komşulukları:** $\{\infty\} \cup (X \setminus K)$ formunda, $K \subseteq X$ sonlu (= kapalı = kompakt).

---

## 2. Yerel kompakt olmayan örnekler

### 2.1 Rasyonel sayılar $\mathbb{Q}$ (alt uzay topolojisi)

- **Yerel kompaktlık:** `not_locally_compact` etiketi → `false` (theorem).
- **Neden?** $\mathbb{Q}$ içinde kompakt olan hiçbir açık aralık yoktur; her kompakt $K \subseteq \mathbb{Q}$ iç noktasızdır.
- **Pedagojik not:** $\mathbb{Q}$ bir tamamlanmamış metrik uzaydır ve yerel kompaktlığın neden Hausdorff + metrik'ten otomatik gelmediğini gösteren temel örnektir.

### 2.2 $\ell^2$ (sonsuz boyutlu Hilbert uzayı)

- **Yerel kompaktlık:** `not_locally_compact` → `false` (theorem).
- **Neden?** Sonsuz boyutlu normlu uzaylarda kapalı birim top kompakt değildir (Riesz lemması).
- **API uyarısı:** `is_locally_compact`, `metric` etiketli bir uzayı `conditional` olarak raporlar; kesin sonuç için `locally_compact` veya `not_locally_compact` etiketi eklenmelidir.

---

## 3. Alexandroff kompaktlaştırması — yapısal notlar

### 3.1 Açık kümeler

Uzay $(X, \tau)$, $\infty$ yeni nokta, $X^* = X \cup \{\infty\}$. $X^*$'ın topolojisi:

1. $U \in \tau$ ise $U \in \tau^*$.
2. $V = \{\infty\} \cup (X \setminus K)$ biçiminde, $K \subseteq X$ kompakt kapalı ise $V \in \tau^*$.

### 3.2 Hausdorff koşulunun rolü

- $X$ yerel kompakt Hausdorff ise $X^*$ kompakt Hausdorff olur.
- $X$ yalnızca yerel kompakt ama Hausdorff değilse $X^*$ Hausdorff olmayabilir.
- Bu ayrım `alexandroff_point_check` içindeki Hausdorff kontrolünün nedenini açıklar.

### 3.3 Sonlu uzay pedagojisi

- Her sonlu uzay kompakttır → `alexandroff_point_check` → `false`.
- Ancak `one_point_compactification` sonlu uzay üzerinde de çalışır; elde edilen uzay pedagojik örnekleme için somut ve test edilebilir bir yapıdır.

---

## 4. API eşleme tablosu

| Uzay                        | `is_locally_compact` | `alexandroff_eligible` | Mod       |
|-----------------------------|----------------------|------------------------|-----------|
| Sonlu ayrık uzay            | `true`               | `false`                | exact     |
| $\mathbb{R}$ (std)          | `true`               | `true`                 | theorem   |
| $\mathbb{R}^n$              | `true`               | `true`                 | theorem   |
| Sonsuz ayrık uzay           | `true`               | `true`                 | theorem   |
| $\mathbb{Q}$ (alt uzay)     | `false`              | `false`                | theorem   |
| Metrik uzay (etiket yok)    | `conditional`        | `unknown`              | theorem   |
| Kompakt Hausdorff uzay      | `true`               | `false`                | theorem   |

---

## 5. Çapraz referanslar

- **Bölüm 22 manuscript:** `22_local_compactness_and_compactifications.tex` — v0.1.56 API köprüsü bölümü
- **Cilt I kompaktlık:** Bölüm 14 — açık örtü kompaktlığı temeli
- **Bölüm 21:** advanced separation — Hausdorff/T3/T4 hattı
- **Cilt IV kardinal fonksiyonlar:** yerel kompaktlık, kompaktlık ile kardinal nicelik bağları
- **Mevcut örnek bankası:** `examples_bank/compactification_examples.md` (genel kompaktlaştırma ailesi)
