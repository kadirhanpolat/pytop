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

### Formal Tanım

Bir X kümesi ve tau ⊆ P(X) ailesi verilsin. (X, tau) bir **topolojik uzay**,
tau ise X üzerinde bir **topoloji** olarak adlandırılır, eğer:

  (T1) ∅ ∈ tau  ve  X ∈ tau
  (T2) U, V ∈ tau  ⟹  U ∩ V ∈ tau
  (T3) {U_α}_α ⊆ tau  ⟹  ⋃_α U_α ∈ tau

tau'nun elemanları **açık küme** olarak adlandırılır.

### Baz Koşulları (B1–B2)

  (B1) ⋃B = X
  (B2) B1, B2 ∈ B ve x ∈ B1 ∩ B2 ise ∃ B3 ∈ B: x ∈ B3 ⊆ B1 ∩ B2

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
## 5. Örnekler

### Örnek 5.1 — Sierpiński Uzayı
"""

# %%
s = sierpinski_space()
print("=== Örnek 5.1: Sierpinski Uzayi ===")
print("Tasiyici:", s.carrier)
print("Topoloji:", sorted(str(t) for t in s.topology))
print("Etiketler:", sorted(s.tags))
print()
# Topoloji tam olarak uc acik kume icerir: bos kume, {1}, {0,1}.
# {0} acik degildir — bu T0 fakat T1 olmayan ozelligin kaynagi.

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
## 6. Alıştırmalar

### Kodlama

K1. X = {a, b, c} üzerinde T1 ama T2 (Hausdorff) olmayan bir topoloji inşa edin.
    (İpucu: cofinite_topology veya make_topology kullanın.)

K2. topology_from_subbasis({1,2,3,4}, [{1,2},{3,4},{2,3}]) çağrısının ürettiği
    topolojinin kaç açık küme içerdiğini ve hangi açık kümelerden oluştuğunu bulun.

K3. finite_chain_space(5) oluşturun. Kaç açık küme var? Hangi nokta "en açık"?

### Teori

T1. X = {1, 2, 3} üzerinde kaç farklı topoloji tanımlanabilir? Baz teoremini
    doğrudan saymak yerine neden kullanmak pratiktir?

T2. Ayrık topolojinin her zaman en ince, indirgenmiş topolojinin en kaba olduğunu
    T1–T3 aksiyomlarını kullanarak kanıtlayın.
"""

if __name__ == "__main__":
    print("pytop Kullanim Kilavuzu — Bolum 1: Topolojik Uzaylar")
    print("=" * 60)
    # Tum ornekler yukari koda gerceklestirilir; bu blok sadece dogrudan
    # calistirma icin giris noktasidir.
