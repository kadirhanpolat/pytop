# %% [markdown]
"""
# Bölüm 1 — pytop'a Hızlı Giriş

pytop kurulumu, temel uzay nesneleri, `Result` tipi ve tag sistemi —
kılavuzun geri kalanını okumadan önce bu bölümü çalıştırın.
"""

# %% [markdown]
"""
## 1. Kurulum ve Import

```bash
pip install -e .   # git kökünden
```

Her bölümde ihtiyaç duyulan semboller doğrudan `pytop`'tan import edilir.
"""

# %%
import pytop
print("pytop sürümü:", pytop.__version__)

# %% [markdown]
"""
> **Neden bu konu?** pytop'un temel nesnelerini tanımadan diğer bölümler okunamaz.

> 🔍 **Kendin dene:** `discrete_topology(0,1,2)` oluşturduktan sonra `topology` listesini elle inceleyerek tüm alt kümelerin açık olup olmadığını sayın.

> ⚠️ **Sık hata:** `r.status == True` yerine `r.status == 'true'` kullanın (dize karşılaştırması).

> ↗️ **Bkz.:** Bölüm 4 (uzay aksiyomları), Bölüm 5 (kapalı kümeler/kapanış).

> 💭 **Öz-yansıtma:** `make_topology`'nin farkı nedir? Neden `Result` bir `bool` değil?
"""

# %% [markdown]
"""
## 2. Uzay Nesneleri

pytop dört temel kurucuya sahiptir:

| Kurucu | Topoloji | Sonuç |
|--------|----------|-------|
| `discrete_topology(*pts)` | Her altküme açık | Ayrık |
| `indiscrete_topology(*pts)` | Yalnız ∅ ve X açık | İndiscrete |
| `sierpinski_space()` | {∅, {1}, {0,1}} | Sierpiński |
| `make_topology(carrier, *open_sets)` | Kullanıcı tanımlı | Özel |
"""

# %%
from pytop import (
    discrete_topology, indiscrete_topology, sierpinski_space, make_topology,
    is_compact, is_connected, is_t0, is_t1, is_t2, count_topologies_on_n_points,
)

d = discrete_topology(0, 1, 2)
print("Ayrık — carrier:", sorted(d.carrier))
print("Ayrık — topoloji boyutu:", len(d.topology))
print("Ayrık — etiketler:", sorted(d.tags))

# %% [markdown]
"""
```text
Ayrık — carrier: [0, 1, 2]
Ayrık — topoloji boyutu: 8
Ayrık — etiketler: ['discrete', 'finite', 'hausdorff', 'metrizable', 'normal', 'regular']
```

`tags` kümesi uzayın bilinen topolojik özelliklerini depolar; yüklem fonksiyonları
bu etiketten hızlı sonuç üretebilir.
"""

# %% [markdown]
"""
## 3. Result Tipi

pytop'un çoğu yüklemi bir `Result` nesnesi döner.
"""

# %%
from pytop import sierpinski_space, is_t2, is_compact, is_connected

s = sierpinski_space()
r = is_t2(s)

print("Result alanları:")
print("  .status      :", r.status)        # 'true' | 'false' | 'unknown'
print("  .value       :", r.value)         # özelliğin adı
print("  .mode        :", r.mode)          # 'exact' | 'corridor' | 'assumed'
print("  .justification:", r.justification)
print("  .assumptions  :", r.assumptions)
print("  .metadata     :", r.metadata)

# %% [markdown]
"""
```text
Result alanları:
  .status      : false
  .value       : hausdorff
  .mode        : exact
  .justification: ['The explicit finite topology fails hausdorff.']
  .assumptions  : []
  .metadata     : {'representation': 'finite', 'property': 'hausdorff', ...}
```

`.status` her zaman `'true'`, `'false'` veya `'unknown'` dizesidir — Python
bool'u değil. Karşılaştırmada `r.status == 'true'` kullanın.
"""

# %% [markdown]
"""
## 4. Temel Uzaylar Turu
"""

# %%
spaces = {
    "Ayrık D(0,1,2)":     discrete_topology(0, 1, 2),
    "İndiscrete I(0,1,2)": indiscrete_topology(0, 1, 2),
    "Sierpinski S":        sierpinski_space(),
}

print(f"{'Uzay':<22} {'kompakt':>8} {'bağlantılı':>11} {'T0':>4} {'T1':>4} {'T2':>4}")
print("-" * 58)
for name, sp in spaces.items():
    c  = is_compact(sp).status
    co = is_connected(sp).status
    t0 = is_t0(sp).status
    t1 = is_t1(sp).status
    t2 = is_t2(sp).status
    print(f"{name:<22} {c:>8} {co:>11} {t0:>4} {t1:>4} {t2:>4}")

# %% [markdown]
"""
```text
Uzay                   kompakt  bağlantılı   T0   T1   T2
----------------------------------------------------------
Ayrık D(0,1,2)            true       false true true true
İndiscrete I(0,1,2)       true        true false false false
Sierpinski S              true        true  true false false
```
"""

# %% [markdown]
"""
## 5. Özel Topoloji: make_topology
"""

# %%
X = [1, 2, 3, 4]
tau = [set(), {1,2}, {3,4}, {1,2,3,4}]
fts = make_topology(X, *tau)

print("carrier:", sorted(fts.carrier))
print("topoloji:")
for u in sorted([sorted(list(v)) for v in fts.topology], key=lambda x: (len(x), x)):
    print(" ", u if u else "empty")
print("kompakt:", is_compact(fts).status)
print("T0:", is_t0(fts).status)
print("T2:", is_t2(fts).status)

# %% [markdown]
"""
```text
carrier: [1, 2, 3, 4]
topoloji:
  ∅
  [1, 2]
  [3, 4]
  [1, 2, 3, 4]
kompakt: true
T0: false
T2: false
```

`make_topology` verilen açık kümelerin birleşim ve kesişim kapatmasını
otomatik tamamlar. Burada {1,2} ve {3,4} X'in bölümtüsünü oluşturduğundan
ek açık küme gerekmez.
"""

# %% [markdown]
"""
## 6. Tag Sistemi
"""

# %%
d3 = discrete_topology(0, 1, 2)
ind3 = indiscrete_topology(0, 1, 2)
s = sierpinski_space()

print("Ayrık etiketleri:     ", sorted(d3.tags))
print("İndiscrete etiketleri:", sorted(ind3.tags))
print("Sierpinski etiketleri:", sorted(s.tags))

# %% [markdown]
"""
```text
Ayrık etiketleri:      ['discrete', 'finite', 'hausdorff', 'metrizable', 'normal', 'regular']
İndiscrete etiketleri: ['finite', 'indiscrete']
Sierpinski etiketleri: ['finite', 'sierpinski']
```

Etiketler yüklem fonksiyonlarının karar mekanizmasını hızlandırır:
`is_t2(d3)` açık küme taraması yerine `'hausdorff' in d3.tags` kontrolüyle sonuç verir.
"""

# %% [markdown]
"""
## 7. n Nokta Üzerindeki Topoloji Sayısı
"""

# %%
print(f"{'n':>3}  {'topoloji sayısı':>16}")
print("-" * 22)
for n in range(1, 5):
    cnt = count_topologies_on_n_points(n)
    print(f"{n:>3}  {cnt:>16}")

# %% [markdown]
"""
```text
  n  topoloji sayısı
----------------------
  1                 1
  2                 4
  3                29
  4               355
  5              6942
```

Topoloji sayısı hızla büyür; sonlu uzayların tüm topolojileri üzerinde
kaba kuvvet taraması yalnızca küçük n için pratiktir.
"""

# %% [markdown]
"""
## 8. Sıradaki Adım

Bu bölümden sonra kılavuzu sırayla okuyun:

- **Bölüm 4** — Topolojik uzay aksiyomları, baz, alt-baz
- **Bölüm 5** — Açık/kapalı/clopen altkümeler, kapanış, iç, sınır
- **Bölüm 6** — Ayrılma aksiyomları T0–T4

Herhangi bir bölümdeki `from pytop import (...)` satırı
o bölümde kullanılan tüm fonksiyonları listeler.
"""

# %%
if __name__ == "__main__":
    pass
