# %% [markdown]
"""
# Bölüm 2 — Yüklemler ve Altküme Operatörleri

Bu bölümde bir topolojik uzaydaki altkümeler üzerinde tanımlı temel yüklemler
(açık, kapalı, clopen, yoğun, hiçbiryerde-yoğun) ve altküme operatörleri
(kapanış, iç, sınır, türev kümesi) incelenmektedir.
"""

# %% [markdown]
"""
## 1. Konu

### Altküme Yüklemleri

Bir (X, τ) topolojik uzayı ve A ⊆ X alınalım:

- **Açık (open):** A ∈ τ
- **Kapalı (closed):** X ∖ A ∈ τ
- **Clopen:** Hem açık hem kapalı; A ∈ τ ve X ∖ A ∈ τ
- **Yoğun (dense):** Her boş olmayan açık küme A ile kesişir; A⁻ = X
- **Hiçbiryerde-yoğun (nowhere dense):** int(cl(A)) = ∅

### Altküme Operatörleri

| Operatör | Gösterim | Tanım |
|----------|----------|-------|
| Kapanış | A⁻ = cl(A) | En küçük A'yı içeren kapalı küme |
| İç | A° = int(A) | En büyük A'ya dahil açık küme |
| Sınır | ∂A = bd(A) | A⁻ ∖ A° |
| Türev kümesi | A' = d(A) | A'nın birikme noktaları kümesi |

### Komşuluk Sistemi N(x)

x ∈ X için komşuluk sistemi:
    N(x) = {N ⊆ X : ∃U ∈ τ, x ∈ U ⊆ N}

**Komşuluk Aksiyomları (N1–N4):**
- (N1) x ∈ N, her N ∈ N(x) için
- (N2) X ∈ N(x)
- (N3) N1, N2 ∈ N(x) ⇒ N1 ∩ N2 ∈ N(x)
- (N4) N ∈ N(x), N ⊆ M ⇒ M ∈ N(x)
"""

# %% [markdown]
"""
## 2. Teoremler

**Teorem 2.1 (Kuratowski Kapanış Aksiyomları).**
cl: P(X) → P(X) operatörü aşağıdaki dört özelliği sağlar (ve sadece bu dört özelliği
sağlayan her operatör bir topoloji tanımlar):
  (K1) cl(∅) = ∅
  (K2) A ⊆ cl(A)
  (K3) cl(cl(A)) = cl(A)
  (K4) cl(A ∪ B) = cl(A) ∪ cl(B)

**Teorem 2.2 (İç-Kapanış Dualitesi).**
Her A ⊆ X için:
    A° = X ∖ cl(X ∖ A)
    cl(A) = X ∖ int(X ∖ A)

**Teorem 2.3 (Komşuluk Sistemi Round-Trip).**
Bir topolojiden türetilen komşuluk sistemi {N(x)}_{x∈X}, N1–N4'ü sağlar.
Tersine, N1–N4'ü sağlayan her {N(x)}_{x∈X} ailesi birden fazla topoloji
yerine tek bir topolojiyi geri üretir (round-trip teoremi).
"""

# %% [markdown]
"""
## 3. Algoritmalar

### Sonlu Kapanış Hesabı

    Kapaniş(A, X, τ):
        closed_sets ← {X ∖ U : U ∈ τ}
        result ← X               # en büyük küme
        for each C ∈ closed_sets:
            if A ⊆ C and C ⊂ result:
                result ← C
        return result             # A'yı içeren en küçük kapalı küme

Karmaşıklık: O(|τ|·|X|) — her kapalı kümede ⊆ kontrolü.

### Sonlu İç Hesabı

    İç(A, X, τ):
        result ← ∅
        for each U ∈ τ:
            if U ⊆ A and |U| > |result|:
                result ← U
        return result             # A'ya dahil en büyük açık küme

Karmaşıklık: O(|τ|·|X|).

### Türev Kümesi

    TürevKümesi(A, X, τ):
        acc ← ∅
        for each x ∈ X:
            if every open U ∋ x meets A ∖ {x}:
                acc.add(x)
        return acc

Karmaşıklık: O(|X|·|τ|).
"""

# %% [markdown]
"""
## 4. pytop API
"""

# %%
from pytop import (
    sierpinski_space,
    discrete_topology,
    make_topology,
    naturals_cofinite,
    analyze_predicate,
    closure_of_subset,
    interior_of_subset,
    boundary_of_subset,
    derived_set_of_subset,
    is_open_subset,
    is_closed_subset,
    is_dense_subset,
    is_nowhere_dense_subset,
    neighborhood_system,
    character_at_point,
    analyze_neighborhood_system,
)

# %% [markdown]
"""
## 5. Örnekler

### Örnek 5.1 — Kapanış ve İç: Sierpiński Uzayında
"""

# %%
s = sierpinski_space()
carrier = list(s.carrier)
topology = list(s.topology)

print("=== Ornek 5.1: Sierpinski — Kapaniş ve Ic ===")
print("cl({0})  =", closure_of_subset(s, {0}).value)
print("cl({1})  =", closure_of_subset(s, {1}).value)
print("int({0}) =", interior_of_subset(s, {0}).value)
print("int({1}) =", interior_of_subset(s, {1}).value)
print("bd({1})  =", boundary_of_subset(s, {1}).value)
print()
# {0}'in kapanışı {0}'dır çünkü {0} = X ∖ {1} kapalıdır.
# {1}'in kapanışı {0,1}'dir çünkü {1} kapalı değildir; onu içeren en küçük kapalı küme X'tir.
# {0}'in içi boştur — {0}'ı içeren açık küme yok.

# %% [markdown]
"""
### Örnek 5.2 — Türev Kümesi ve Hiçbiryerde-Yoğunluk
"""

# %%
print("=== Ornek 5.2: Turev Kumesi ===")
print("d({0}) in Sierpinski  =", derived_set_of_subset(s, {0}).value)
print("d({1}) in Sierpinski  =", derived_set_of_subset(s, {1}).value)
print("{0} nowhere_dense?    =", is_nowhere_dense_subset(s, {0}).status)
print("{1} nowhere_dense?    =", is_nowhere_dense_subset(s, {1}).status)
print()
# d({0}) = {0}: her açık komşuluk {0} ∋ 0'ı içerse de {0}∖{0}=∅ ile kesişmez → d(∅).
# Gerçekte: 0'ı içeren tek açık küme {0,1}; {0,1} ∩ ({1}∖{1}) = ∅ → 1 ∉ d({1}).
# d({1}) = {0}: 0'ı içeren {0,1}, {1} ∖ {0} = {1} ile kesişir.

# %% [markdown]
"""
### Örnek 5.3 — Yüklemler: Ayrık Topoloji
"""

# %%
d = discrete_topology('a', 'b', 'c')
print("=== Ornek 5.3: Ayrik Topoloji — Yuklemler ===")
print("{'a'} acik?     =", analyze_predicate(d, 'open', {'a'}).status)
print("{'a'} kapali?   =", analyze_predicate(d, 'closed', {'a'}).status)
print("{'a'} clopen?   =", analyze_predicate(d, 'clopen', {'a'}).status)
print("{'a'} yogun?    =", analyze_predicate(d, 'dense', {'a'}).status)
print("{'a','b','c'} yogun? =", analyze_predicate(d, 'dense', {'a','b','c'}).status)
print()
# Ayrık topolojide her tekil küme hem açık hem kapalıdır (clopen).
# {'a'} yoğun değil — cl({'a'}) = {'a'} ≠ X.
# {'a','b','c'} = X trivially yoğundur.

# %% [markdown]
"""
### Örnek 5.4 — Sınır Hesabı
"""

# %%
sp = make_topology({1, 2, 3}, {1}, {2, 3})
print("=== Ornek 5.4: make_topology({1},{2,3}) — Sinirlar ===")
print("bd({1})    =", boundary_of_subset(sp, {1}).value)
print("bd({2,3})  =", boundary_of_subset(sp, {2, 3}).value)
print("bd({1,2})  =", boundary_of_subset(sp, {1, 2}).value)
print()
# bd({1}) = cl({1}) ∖ int({1}) = {1} ∖ {1} = ∅ (açık kümelerin sınırı boş olabilir)
# bd({1,2}): int({1,2}) = ?, cl({1,2}) = ?

# %% [markdown]
"""
### Örnek 5.5 — Komşuluk Sistemi: Sierpiński
"""

# %%
print("=== Ornek 5.5: Komşuluk Sistemi ===")
r_nbhd_0 = neighborhood_system(carrier, topology, 0)
r_nbhd_1 = neighborhood_system(carrier, topology, 1)
print("N(0) =", r_nbhd_0.value)
print("N(1) =", r_nbhd_1.value)
print("chi(0) =", character_at_point(carrier, topology, 0).value)
print("chi(1) =", character_at_point(carrier, topology, 1).value)
print()
# N(0) = {{0,1}} — yalnızca X komşuluk: 0 herhangi bir açık kümede yalnızca X'te.
# N(1) = {{1}, {0,1}} — {1} ve X komşuluk.
# chi(0)=1, chi(1)=2 — karakter sayısı: noktanın yerel baz büyüklüğü.

# %% [markdown]
"""
### Örnek 5.6 — Analiz: Komşuluk Sistemi Aksiyomları
"""

# %%
print("=== Ornek 5.6: analyze_neighborhood_system ===")
r_analyze = analyze_neighborhood_system(carrier, topology, 0)
print("Puan:", r_analyze.value)
print()
# all_axioms=True: N1–N4 tümü geçerli.
# neighborhood_count=1: 0 için yalnızca 1 komşuluk ({0,1}).

# %% [markdown]
"""
## 6. Alıştırmalar

### Kodlama

K1. İndirgenmiş topoloji (iki nokta) üzerinde her iki noktanın komşuluk sistemini
    hesaplayın. N1–N4 aksiyomları geçiyor mu?

K2. X = {1,2,3,4} üzerinde make_topology({1,2,3,4},{1,2},{3,4}) topolojisinde
    bd({1,2,3}) ve cl({1,2,3}) hesaplayın.

K3. finite_chain_space(4) zincirinde {1,2}'nin iç, kapanış ve sınır kümelerini bulun.

### Teori

T1. (X,τ) uzayında A⁰ = X ∖ cl(X ∖ A) eşitliğini Kuratowski aksiyomlarını
    kullanarak kanıtlayın.

T2. Her komşuluk sistemi N1–N4'ü sağlıyorsa, τ = {U : ∀x∈U, U∈N(x)}
    T1–T3'ü sağladığını gösterin.
"""

if __name__ == "__main__":
    print("pytop Kullanim Kilavuzu — Bolum 2: Yuklemler ve Altküme Operatörleri")
    print("=" * 70)
