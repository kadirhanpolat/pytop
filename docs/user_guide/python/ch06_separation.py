# %% [markdown]
"""
# Bölüm 6 — Ayrılma Aksiyomları

Ayrılma aksiyomları (T0–T4 ve ötesi), bir topolojik uzaydaki noktaların ve kapalı
kümelerin birbirinden açık kümeler aracılığıyla ne ölçüde "ayrılabildiğini" ölçer.
Her aksiyom bir öncekinden daha güçlüdür.
"""

# %% [markdown]
"""
## 1. Konu

### Ayrılma Aksiyomları Sıralaması

| Aksiyom | İsim | Koşul |
|---------|------|-------|
| T0 | Kolmogorov | ∀ x≠y: ∃ U∈τ, (x∈U, y∉U) veya (y∈U, x∉U) |
| T1 | Fréchet | ∀ x≠y: ∃ U,V∈τ, x∈U∧y∉U, y∈V∧x∉V |
| T2 | Hausdorff | ∀ x≠y: ∃ U,V∈τ, x∈U, y∈V, U∩V=∅ |
| T2.5 | Urysohn | ∀ x≠y: ∃ U,V∈τ, x∈U, y∈V, cl(U)∩cl(V)=∅ |
| T3 | Regüler | T1 + ∀ x, kapalı C ∌ x: ∃ U,V∈τ, x∈U, C⊆V, U∩V=∅ |
| T3.5 | Tychonoff/Tam regüler | T1 + ∀ x, kapalı C ∌ x: ∃f:X→[0,1] sürekli, f(x)=0, f|C=1 |
| T4 | Normal | T1 + ∀ C,D kapalı, C∩D=∅: ∃ U,V∈τ, C⊆U, D⊆V, U∩V=∅ |
| Perfectly normal | — | T4 + kapalı kümeler Gδ |

**Sıralama:** T4 ⟹ T3.5 ⟹ T3 ⟹ T2.5 ⟹ T2 ⟹ T1 ⟹ T0
"""

# %% [markdown]
"""
> **💡 Sezgi:** Ayrılma aksiyomlarını bir mikroskobun çözünürlük kademeleri gibi düşünün: T0'da iki noktayı *en az bir yönden* ayırt edebilirsiniz; T1'de her iki yönden; T2'de noktaları çakışmayan iki ayrı "görüş alanına" koyabilirsiniz; T3 ve T4'te artık nokta–kapalı küme ve kapalı–kapalı çiftleri bile ayrışır.
"""

# %% [markdown]
"""
> **⚠️ Dikkat — sık hata:** T3 = T1 + regüler, T4 = T1 + normal. İki noktalı indirgenmiş uzay regüler *ve* normaldir ama T1 olmadığından T3 de T4 de değildir — aşağıda doğrulanır.

*(Şekil: assets/ch06/fig_ch06_t2_ayirma.png — PDF kılavuzunda Şekil olarak yer alır)*
*(Şekil: assets/ch06/fig_ch06_t3_regulerlik.png — PDF kılavuzunda Şekil olarak yer alır)*

> **🚫 Karşı-örnek:** İki noktalı indirgenmiş uzay T0 bile değildir: açıklar yalnız ∅ ve X olduğundan iki noktayı ayıran hiçbir açık yoktur.
"""

# %% [markdown]
"""
> **Neden bu konu?** T0–T4 hiyerarşisi Hausdorff gibi güçlü özelliklerin tam anlaşılması için gerekli; kümeler arası ayrışma fikrinden doğar.

> 🔍 **Kendin dene:** Sierpiński'nin T0 ama T1 olmadığını `is_t0`/`is_t1` ile doğrulayın.

> ⚠️ **Sık hata:** `is_t2 True` iken `is_t1 False` olamaz; hiyerarşi sıkı içermedir.

> ↗️ **Bkz.:** Bölüm 4 (topoloji), Bölüm 7 (kompakt Hausdorff → normal).

> 💭 **Öz-yansıtma:** T2 (Hausdorff) neden önemli? Hangi ispatlarda özellikle kullanılır?
"""

# %% [markdown]
"""
## 2. Teoremler

**Teorem 2.1 (Ayrılma Zinciri).**
T4 ⟹ T3.5 ⟹ T3 ⟹ T2.5 ⟹ T2 ⟹ T1 ⟹ T0.
Tersi genel olarak doğru değildir.

**Teorem 2.2 (Urysohn Fonksiyon Teoremi).**
X normal (T4) ise ve C, D disjoint kapalı kümeler ise, f: X → [0,1] sürekli bir
fonksiyon vardır: f|C ≡ 0, f|D ≡ 1.

**Teorem 2.3 (Tietze Genişleme Teoremi).**
X normal ise her kapalı A ⊆ X üzerinde tanımlı sürekli f: A → [a,b] fonksiyonu
tüm X'e sürekli olarak genişletilebilir.

**Teorem 2.4 (Tychonoff Karakterizasyonu).**
X, T3.5'tir ⟺ X, [0,1]^I ile homeomorf bir alt uzayı olacak biçimde sürekli
fonksiyonlar X'i ayrıştırır.
"""

# %% [markdown]
"""
**Rehberli Kanıt (T2 ⇒ T1):** x≠y için ayrık U∋x, V∋y al; U∩V=∅ olduğundan y∉U ve x∉V — iki yönlü ayrım hazır. T1 ⇒ T0: iki yönlü ayrım tek yönlüyü içerir. Kalan halkalar Alıştırma T1'de.

*(Şekil: assets/ch06/fig_ch06_implikasyon.png — PDF kılavuzunda Şekil olarak yer alır)*
"""

# %% [markdown]
"""
*(Şekil: assets/ch06/fig_ch06_urysohn.png — PDF kılavuzunda Şekil olarak yer alır)*
"""

# %% [markdown]
"""
**Rehberli Kanıt (Sonlu T1 ⟺ Ayrık):**
1. (⇒) T1 gereği her y≠x için y∈U_y, x∉U_y olan açık U_y vardır; X∖{x}=⋃_{y≠x}U_y açıktır, yani {x} kapalıdır.
2. Herhangi A⊆X, *sonlu* sayıda tekilin birleşimi olarak kapalıdır.
3. Her A kapalı ise X∖A açıktır; topoloji ayrıktır.
4. (⇐) Ayrık topolojide her {x} açıktır; x≠y çifti {x} ve {y} ile iki yönlü ayrılır.

Sonsuzlukta 2. adım çöker: kosonlu ℕ tam bu nedenle T1 olup ayrık değildir.
"""

# %% [markdown]
"""
## 3. Algoritmalar

### Sonlu Ayrılma Karar Prosedürü

T0 (ve analog olarak T1, T2) için sonlu uzayda:

    KontrolT0(X, τ):
        for each pair (x, y) with x ≠ y:
            if not (∃U∈τ: x∈U∧y∉U or y∈U∧x∉U):
                return False
        return True

Karmaşıklık: O(|X|²·|τ|)

T3 için (regülerlik):

    KontrolT3(X, τ):
        closed ← {X ∖ U : U ∈ τ}
        for each x ∈ X, each C ∈ closed with x ∉ C:
            if not ∃ U,V∈τ: x∈U ∧ C⊆V ∧ U∩V=∅:
                return False
        return True

Karmaşıklık: O(|X|·|τ|²)
"""

# %% [markdown]
"""
**İz Sürme: T0 Prosedürü Sierpiński Üzerinde.** X={0,1}, τ={∅,{1},X}:

| Çift (x,y) | Denenen U | x∈U∧y∉U? | y∈U∧x∉U? | Karar |
|------------|-----------|-----------|-----------|-------|
| (0,1) | ∅ | hayır | hayır | devam |
| (0,1) | {1} | hayır | **evet** | çift ayrıldı |
| — | — | — | — | tüm çiftler → **true** |

Genel sınır O(|X|²·|τ|)'dur.
"""

# %% [markdown]
"""
## 4. pytop API
"""

# %%
from pytop import (
    sierpinski_space,
    discrete_topology,
    indiscrete_topology,
    naturals_cofinite,
    real_line_metric,
    is_t0, is_t1, is_t2, is_t2_5, is_t3, is_t4,
    is_hausdorff, is_regular, is_normal,
    is_perfectly_normal,
    separation_chain,
    analyze_separation,
)

# %% [markdown]
"""
> **🎯 Neden önemli?** `is_*` yüklemleri ham `bool` değil, `.status` alanı `true` / `false` / `unknown` olabilen bir `Result` döndürür. `tychonoff: unknown` — sürekli fonksiyon ayırması açık-küme taramasıyla karar verilemez.
"""

# %% [markdown]
"""
## 5. Örnekler

### Örnek 5.1 — Sierpiński: T0 ✓, T1 ✗
"""

# %%
s = sierpinski_space()
print("=== Ornek 5.1: Sierpinski ===")
print("T0:", is_t0(s).status)
print("T1:", is_t1(s).status)
print("T2:", is_t2(s).status)
print()
# Sierpinski: T1 degil cunku {0} acik degildir — 0'i yalnizca X ayirir, sadece 1 degil.

# %% [markdown]
"""
**Ne oldu?** T0: true — (0,1) çifti için {1} açığı 1'i içerir, 0'ı dışlar. T1: false — ters yön yok: {0}∉τ. Sierpiński, zincirin "T0'da takılan" kanonik örneğidir.
"""

# %% [markdown]
"""
### Örnek 5.2 — İndirgenmiş Topoloji: Hiçbir T Aksiyomu Yok
"""

# %%
ind = indiscrete_topology('a', 'b')
print("=== Ornek 5.2: Indiscrete ===")
print("T0:", is_t0(ind).status)
print("T1:", is_t1(ind).status)
print()
# Indiscrete: T0 degil — a ve b'yi ayiran acik kume yok.

# %% [markdown]
"""
### Örnek 5.3 — Kosonlu Doğal Sayılar: T1 ✓, T2 ✗
"""

# %%
nc = naturals_cofinite()
print("=== Ornek 5.3: Naturals Cofinite ===")
print("T0:", is_t0(nc).status)
print("T1:", is_t1(nc).status)
print("T2:", is_t2(nc).status)
print()
# Kosonlu: T1 ama Hausdorff degil — herhangi iki acik kume kesisir.

# %% [markdown]
"""
**Ne oldu?** T1: true — her n için ℕ∖{n} kosonludur (açıktır); iki yönlü ayrım sağlanır. T2: false — boş olmayan iki kosonlu açık daima kesişir (ℕ sonsuz). Bölüm 4 K1'in "neden sonsuz taşıyıcı gerekir" sorusunun cevabı budur.
"""

# %% [markdown]
"""
### Örnek 5.4 — Ayrık Topoloji: Tüm Aksiyomlar ✓
"""

# %%
d = discrete_topology(1, 2, 3)
print("=== Ornek 5.4: Discrete {1,2,3} ===")
chain = separation_chain(d)
for prop, result in chain.items():
    print(f"  {prop:20s}: {result.status}")
print()

# %% [markdown]
"""
**Ne oldu?** Ayrık uzayda her tekil açık → dokuz yüklemin tümü true döner. `tychonoff` bile true: ayrık uzayda her fonksiyon süreklidir. `separation_chain` anahtar sırası zincirin mantıksal sırasıdır — "nerede takıldığını" yukarıdan aşağı okuyun.
"""

# %% [markdown]
"""
### Örnek 5.5 — Regüler Ama T3 Değil: Konvansiyon Testi
"""

# %%
from pytop import two_point_indiscrete_space

tp = two_point_indiscrete_space()
print("regular:", is_regular(tp).status, "| normal:", is_normal(tp).status)
print("t3     :", is_t3(tp).status, "| t4    :", is_t4(tp).status)

# %% [markdown]
"""
**Ne oldu?** Indirgenmiş iki noktalı uzayda ayirma kosullarinin onculu hic gerceklesemez; `regular` ve `normal` true. Ama T1 olmadığından `t3` ve `t4` false kalır.
"""

# %% [markdown]
"""
### Örnek 5.6 — separation_chain Özet
"""

# %%
print("=== Ornek 5.6: separation_chain ozeti ===")
print("Sierpinski chain:")
for prop, result in separation_chain(s).items():
    print(f"  {prop:20s}: {result.status}")
print()

# %% [markdown]
"""
### Örnek 5.7 — analyze_separation
"""

# %%
print("=== Ornek 5.7: analyze_separation ===")
rl = real_line_metric()
# analyze_separation(space) varsayilan olarak 'hausdorff' ozelligini test eder.
print("Real line Hausdorff mi?:", analyze_separation(rl).status)
print("Discrete Hausdorff mi?:", analyze_separation(d).status)
print("Sierpinski Hausdorff mi?:", analyze_separation(s).status)
print("Sierpinski T0 mu?:", analyze_separation(s, 't0').status)
print()
# status='true'  => uzay bu aksiyomu saglar
# status='false' => uzay bu aksiyomu saglamaz

# %% [markdown]
"""
## 6. Alıştırmalar

### Kodlama

**K1.** `make_topology({1,2,3},{1},{2},{1,2})` için `separation_chain` çalıştırın; her sonucu yorumlayın.
*Ipucu: Once aciklari listeleyin. Her cifti ayiran acik arayin; 3'u icerip 1'i dislayan acik var mi?*
*(Cozum: solutions.py / solutions.ipynb -> Bolum 6 / K1)*

**K2.** `finite_chain_space(3)` üzerinde en yüksek sağlanan aksiyomu bulun.
*Ipucu: Ciktida true olan en guclu anahtari arayin; unknown degerleri "Neden onemli?" kutusuna gore yorumlayin.*
*(Cozum: solutions.py / solutions.ipynb -> Bolum 6 / K2)*

**K3.** `two_point_indiscrete_space()` üzerinde T0, T1, T2 test edin.
*Ipucu: Tek bos olmayan acik X iken herhangi bir cift nasil ayrilabilir?*
*(Cozum: solutions.py / solutions.ipynb -> Bolum 6 / K3)*

### Teori

**T1.** T2 ⇒ T1 ⇒ T0 implikasyonlarını kanıtlayın.
*Ipucu: T2=>T1: ayrik U∋x, V∋y; y∉U ve x∉V — iki yonlu ayrim. T1=>T0: iki yonlu tek yonluyu icerir.*
*(Cozum: solutions.py / solutions.ipynb -> Bolum 6 / T1)*

**T2.** Sonlu uzayda T1 ⟺ ayrık topoloji olduğunu gösterin.
*Ipucu: T1 => tekiller kapali => sonlu birlesim => her alt kume kapali => her alt kume acik.*
*(Cozum: solutions.py / solutions.ipynb -> Bolum 6 / T2)*
"""

if __name__ == "__main__":
    print("pytop Kullanim Kilavuzu — Bolum 3: Ayrilma Aksiyomlari")
    print("=" * 60)
