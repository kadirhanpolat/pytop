# %% [markdown]
"""
# Bölüm 4 — Topolojik Uzaylar

Topoloji, bir kümedeki noktaların birbirine "yakın" olup olmadığını, aralarındaki
sürekliliği ve şekilsel özellikleri, mesafe kavramına gerek duymadan inceleyen
matematiksel bir disiplindir. Bunu mümkün kılan temel araç *açık küme* kavramıdır.
"""

# %% [markdown]
"""
## 1. Konu

### Sezgisel Giriş

Sezgisel olarak, bir topolojik uzayda "yakın" kavramı açık kümeler aracılığıyla
kodlanır. Metrik gerektirmeden sürekliliği, yakınsamayı ve şekilsel özellikleri
tanımlayabiliriz.
"""

# %% [markdown]
"""
> **💡 Sezgi:** Bir şehir haritasında "yakınlık"ı sokak mesafesiyle ölçebilirsiniz; ama "hangi mahalleler birbirine komşu?" sorusu mesafe olmadan da anlamlıdır. Topoloji tam bunu yapar: mesafeyi unutur, yalnızca "hangi kümeler bir noktanın çevresini oluşturur?" bilgisini tutar. Matematiksel karşılığı: τ ailesi her noktanın "çevre" kavramını açık kümeler aracılığıyla kodlar; süreklilik ve yakınsama gibi kavramlar yalnız τ'ya başvurularak tanımlanır.
"""

# %% [markdown]
"""
### Formal Tanım

Bir X kümesi ve tau ⊆ P(X) ailesi verilsin. (X, tau) bir **topolojik uzay**,
tau ise X üzerinde bir **topoloji** olarak adlandırılır, eğer:

  (T1) ∅ ∈ tau  ve  X ∈ tau
  (T2) U, V ∈ tau  ⟹  U ∩ V ∈ tau
  (T3) {U_α}_α ⊆ tau  ⟹  ⋃_α U_α ∈ tau

tau'nun elemanları **açık küme** olarak adlandırılır.
"""

# %% [markdown]
"""
Aksiyomların her biri ayrı bir iş görür: **(T1)** uzayın tamamının ve boş kümenin "gözlemlenebilir" olmasını garanti eder; **(T2)** iki gözlemin kesişiminin de gözlem olmasını sağlar — sonlu kesişimle sınırlı kalması bilinçlidir; **(T3)** keyfî birleşime izin verir.

> **🚫 Karşı-örnek:** X={1,2,3} üzerinde σ={∅,{1},{2},X} ailesi bir topoloji *değildir*: {1}∪{2}={1,2}∉σ olduğundan (T3) ihlal edilir.
"""

# %% [markdown]
"""
### Baz Koşulları (B1–B2)

  (B1) ⋃B = X
  (B2) B1, B2 ∈ B ve x ∈ B1 ∩ B2 ise ∃ B3 ∈ B: x ∈ B3 ⊆ B1 ∩ B2
"""

# %% [markdown]
"""
*(Şekil: assets/ch04/fig_ch04_baz_tanimi.png — PDF kılavuzunda Şekil olarak yer alır)*

> **🎯 Neden önemli?** Baz, büyük bir topolojiyi küçük bir çekirdekle temsil etme aracıdır. `topology_from_basis` tam bu ilkeyle çalışır: yalnız baz elemanlarını verirsiniz, kapanışı kütüphane hesaplar.
"""

# %% [markdown]
"""
### Sonlu ve Sonsuz Uzaylar

- FiniteTopologicalSpace: taşıyıcı sonlu; topoloji frozenset koleksiyonu.
- Sonsuz sınıflar: taşıyıcı simgesel ('R', 'N'); topoloji=None, etiket tabanlı çıkarım.
"""

# %% [markdown]
"""
## 2. Teoremler

**Teorem 2.1 (Aksiyomların Yeterliliği):** T1–T3, sonlu kesişimlerin ve keyfi
birleşimlerin tau'da kalmasını garanti eder. Özellikle sonsuz kesişim gerekmez.

**Teorem 2.2 (Baz Teoremi):** B, (B1)–(B2)'yi sağlıyorsa:
    tau_B = {U ⊆ X : ∀x ∈ U, ∃B ∈ B: x ∈ B ⊆ U}
bir topoloji oluşturur ve B bu topolojiye baz olur.

**Teorem 2.3 (Karşılaştırma):** tau1 ⊆ tau2 ise tau1 kaba, tau2 ince topolojidir.
Ayrık topoloji en ince, indirgenmiş topoloji en kabadır.
"""

# %% [markdown]
"""
**Rehberli Kanıt (Baz Teoremi):** (T1) ∅ için koşul boş yere doğru; X için (B1) her x'i bir B içine koyar. (T2) x ∈ U∩V için B_U, B_V seç; (B2)'nin verdiği B₃ ⊆ B_U∩B_V ⊆ U∩V. (T3) x ∈ ⋃U_α ise x'in U_α₀'daki baz elemanı birleşim için de iş görür. `topology_from_basis` çıktısının topoloji olmasının güvencesi budur; koşulları sağlamayan aile `BasisConstructionError` ile reddedilir.

*(Şekil: assets/ch04/fig_ch04_sonsuz_kesisim.png — PDF kılavuzunda Şekil olarak yer alır)*
"""

# %% [markdown]
"""
## 3. Algoritmalar

### Bazdan Topoloji Üretimi (O(|B|·2^|B|) en kötü durum)

    BazdenTopoloji(X, B):
        tau ← {∅, X}
        for each alt_aile S ⊆ B (boş olmayan):
            tau.add(⋃ S)          # keyfi birleşim
        tau ← ClosureUnderIntersection(tau)
        return tau

    ClosureUnderIntersection(tau):
        changed ← true
        while changed:
            changed ← false
            for each U, V ∈ tau:
                if U ∩ V ∉ tau:
                    tau.add(U ∩ V)
                    changed ← true
        return tau

Pratik karmaşıklık (çakışmayan baz): O(|tau|·|B|). Uzay: O(|tau|).
"""

# %% [markdown]
"""
**İz Sürme: Küçük Bir Girdiyle Adım Adım.** X={1,2,3}, B={{1},{2,3}} girdisiyle "Bazdan Topoloji Üretimi":

| Adım | Alt-aile S | Eklenen birleşim | τ (o ana dek) |
|------|-----------|-----------------|---------------|
| 0 | — | — | {∅, X} |
| 1 | {{1}} | {1} | {∅, X, {1}} |
| 2 | {{2,3}} | {2,3} | {∅, X, {1}, {2,3}} |
| 3 | {{1},{2,3}} | {1}∪{2,3}=X | değişmez |
| 4 | kesişim kapanışı | {1}∩{2,3}=∅ | değişmez |

Sonuç: |τ|=4; döngü yeni küme üretmediği anda durur.
"""

# %% [markdown]
"""
## 4. pytop API
"""

# %%
from pytop import (
    TopologicalSpace,
    FiniteTopologicalSpace,
    make_topology,
    discrete_topology,
    indiscrete_topology,
    cofinite_topology,
    sierpinski_space,
    topology_from_basis,
    topology_from_subbasis,
    finite_chain_space,
    naturals_cofinite,
    real_line_metric,
)

# %% [markdown]
"""
**Tag Gerekçeleri:** Etiketler, kurucunun inşa anında *garanti ettiği* gerçeklerdir:

| Kurucu | Etiketler | Gerekçe |
|--------|-----------|---------|
| `sierpinski_space()` | compact, connected, finite, t0 | Sonlu ⇒ kompakt; {1} tek yönlü ayırır ⇒ T0 |
| `discrete_topology(1,2,3)` | discrete, finite, hausdorff, metrizable, normal, regular | Her tekil açık ⇒ tüm ayrılma aksiyomları |
| `indiscrete_topology(1,2,3)` | compact, connected, finite, indiscrete | Açık yalnız ∅ ve X |
| `cofinite_topology('a','b','c')` | cofinite, compact, finite, t1 | Tekiller kapalı ⇒ T1 |
| `make_topology(...)`, `finite_chain_space(n)` | finite | Özellik çıkarımı yapılmaz |

Etiketler *eksiksiz değildir*: `cofinite_topology('a','b','c')` aslında ayrıktır ve Hausdorff'tur, ama `discrete`/`hausdorff` etiketi taşımaz. Kesin sorgu için Bölüm 6'daki `is_*` yüklemlerini kullanın.
"""

# %% [markdown]
"""
## 5. Örnekler

### Örnek 5.1 — Sierpiński Uzayı
"""

# %%
s = sierpinski_space()
print("=== Ornek 5.1: Sierpinski Uzayi ===")
print("Tasiyici:", s.carrier)
print("Topoloji:", sorted(str(t) for t in s.topology))
print("Etiketler:", sorted(s.tags))
print()
# Topoloji tam olarak uc acik kume icerir: bos kume, {1}, {0,1}.
# {0} acik degildir — bu T0 fakat T1 olmayan ozelligin kaynagi.

# %% [markdown]
"""
**Ne oldu?** `Tasiyici` satırı X={0,1}'i verir. `Topoloji` satırındaki üç küme tanımın istediği yapıdır: ∅ ve X (T1), tek ek açık küme {1}. `Etiketler`'de `t0` var ama `t1` yok: 1'i içerip 0'ı dışlayan açık küme vardır ({1}), fakat 0'ı içerip 1'i dışlayan yoktur — T0 sağlanıp T1'in sağlanmamasının kaynağı budur.

*(Şekil: assets/ch04/fig_ch04_sierpinski.png — PDF kılavuzunda Şekil olarak yer alır)*
"""

# %% [markdown]
"""
### Örnek 5.2 — Ayrık Topoloji
"""

# %%
d = discrete_topology(1, 2, 3)
print("=== Örnek 5.2: Ayrik Topoloji {1,2,3} ===")
print("|tau| =", len(d.topology), " (2^3 = 8 olmali)")
print("Etiketler:", sorted(d.tags))
print()
# n=3 icin |tau| = 2^3 = 8. Hausdorff, regular, normal, metrizable etiketleri vardir.

# %% [markdown]
"""
**Ne oldu?** n=3 eleman için |τ|=2³=8: her alt küme açıktır. Her tekil açık → hausdorff, normal, regular etiketleri. `metrizable` 0-1 metriğinden. Listede `compact` yok ama `is_compact` true döner — Tag Gerekçeleri tablosuna bakın.
"""

# %% [markdown]
"""
### Örnek 5.3 — make_topology ile Manuel İnşa
"""

# %%
sp = make_topology({1, 2, 3}, {1}, {2, 3})
print("=== Ornek 5.3: make_topology ===")
print("|tau| =", len(sp.topology))
print("Acik kumeler:", sorted(str(t) for t in sp.topology))
print()
# {1} ve {2,3} acik; bos kume ve X otomatik eklenir.
# {1} U {2,3} = X ve {1} ∩ {2,3} = bos kume zaten tau'da.

# %% [markdown]
"""
**Ne oldu?** `make_topology` verilen {1} ve {2,3} açıklarına yalnızca ∅ ve X'i ekledi; |τ|=4. Bu örnekte şans eseri geçerlidir (iki küme ayrık). `make_topology` kapanışları *hesaplamaz* — aşağıdaki dikkat örneği bu farkı gösterir.
"""

# %%
from pytop import make_topology, topology_from_basis

sessiz = make_topology({1, 2, 3}, {1}, {2})   # denetlemez, kapanis hesaplamaz
print("make_topology:", sorted(sorted(t) for t in sessiz.topology))

try:
    topology_from_basis({1, 2, 3}, [{1}, {2}])  # B1 ihlali: 3 ortulmuyor
except Exception as e:
    print("topology_from_basis:", type(e).__name__)

# %% [markdown]
"""
### Örnek 5.4 — Alexandrov Zincir Uzayı
"""

# %%
c = finite_chain_space(3)
print("=== Ornek 5.4: Alexandrov Zincir (n=3) ===")
print("Tasiyici:", c.carrier)
print("Topoloji:", sorted(str(t) for t in c.topology))
print()
# Topoloji: {bos kume, {1}, {1,2}, {1,2,3}} — her acik kume bir "onek"tir.

# %% [markdown]
"""
**Ne oldu?** Çıktıdaki açıklar tam bir "önek merdiveni"dir: ∅⊂{1}⊂{1,2}⊂{1,2,3}. 1 noktası her boş olmayan açıkta yer alır ("en açık" nokta), 3 ise yalnız X'te görünür.
"""

# %% [markdown]
"""
### Örnek 5.5 — Bazdan Topoloji Üretimi
"""

# %%
b = [{1}, {2, 3}, {4}]
ts = topology_from_basis({1, 2, 3, 4}, b)
print("=== Ornek 5.5: topology_from_basis ===")
print("Baz:", [set(x) for x in b])
print("|tau| =", len(ts.topology))
print("Topoloji:", sorted(str(t) for t in ts.topology))
print()
# Baz {1},{2,3},{4} bir boluntu; kesisimleri bos, B2 trivially saglanir.
# 8 acik kume: tum birlesim kombinasyonlari.

# %% [markdown]
"""
**Ne oldu?** Baz {{1},{2,3},{4}} bir bölüntüdür: elemanları ikişer ikişer ayrıktır. (B2) boş yere sağlanır ve topoloji tüm alt-aile birleşimlerinden oluşur: 2³=8 açık küme.
"""

# %% [markdown]
"""
### Örnek 5.6 — Sonsuz Uzay: Gerçek Doğru
"""

# %%
rl = real_line_metric()
print("=== Ornek 5.6: Gercek Dogru (Metrik Topoloji) ===")
print("Tasiyici:", rl.carrier)
print("Etiketler:", sorted(rl.tags))
print()
# Gercek dogru simbolik temsil edilir; topology=None.
# Ozellikler etiketlerde kodlanmistir: ikinci-sayilabilir, ayrilabilir, Lindelof, tam metrik.

# %% [markdown]
"""
**Ne oldu?** `Tasiyici: R` taşıyıcının simgesel olduğunu söyler: gerçek doğrunun noktaları bellekte tutulmaz, topology=None'dır. Tüm topolojik bilgi etiketlerde kodlanmıştır. Sonlu uzaylardaki "hesapla ve doğrula" yaklaşımının yerini "bilinen teoremleri etiketle" alır.
"""

# %% [markdown]
"""
## 6. Alıştırmalar

### Kodlama

**K1.** `cofinite_topology('a','b','c')` ile üç noktalı kosonlu uzayı kurun; topolojisini ve etiketlerini yazdırın, `is_t1` ve `is_t2` ile test edin. Gözlem: sonlu bir kümede kosonlu topoloji ayrık topolojiyle çakışır. T1 olup Hausdorff olmayan bir örnek için taşıyıcının neden sonsuz olması gerektiğini bir cümleyle açıklayın.
*Ipucu: |τ|=2³ çıkacak; anahtar, Bolum 6'daki "Sonlu T1 ⟺ Ayrik" teoremidir.*
*(Cozum: solutions.py / solutions.ipynb -> Bolum 4 / K1)*

**K2.** `topology_from_subbasis({1,2,3,4}, [{1,2},{3,4},{2,3}])` çağrısının ürettiği topolojinin kaç açık küme içerdiğini ve hangi açık kümelerden oluştuğunu bulun.
*Ipucu: Once alt-baz ciftlerinin kesisimlerini elle listeleyin ({2}, {3}, bos kume); sonra birleşimleri sayın.*
*(Cozum: solutions.py / solutions.ipynb -> Bolum 4 / K2)*

**K3.** `finite_chain_space(5)` oluşturun. Kaç açık küme var? Hangi nokta "en açık"?
*Ipucu: Aciklar onek yapisindadir; "en acik" nokta her bos olmayan acikte bulunanadir.*
*(Cozum: solutions.py / solutions.ipynb -> Bolum 4 / K3)*

### Teori

**T1.** X={1,2,3} üzerinde kaç farklı topoloji tanımlanabilir? Baz teoremini doğrudan saymak yerine neden kullanmak pratiktir?
*Ipucu: Aday aile sayisi 2^(2^3)=256'dir; cevap 29. Baz teoremi adaylari uretkent kucuk ailelere indirger.*
*(Cozum: solutions.py / solutions.ipynb -> Bolum 4 / T1)*

**T2.** Ayrık topolojinin her zaman en ince, indirgenmiş topolojinin en kaba olduğunu kanıtlayın.
*Ipucu: Ayriklik icin aksiyom gerekmez; indirgenmiş icin yalniz (T1) yeter.*
*(Cozum: solutions.py / solutions.ipynb -> Bolum 4 / T2)*
"""

if __name__ == "__main__":
    print("pytop Kullanim Kilavuzu — Bolum 1: Topolojik Uzaylar")
    print("=" * 60)
    # Tum ornekler yukari koda gerceklestirilir; bu blok sadece dogrudan
    # calistirma icin giris noktasidir.
