# Bölüm 1 — pytop'a Hızlı Giriş

pytop kurulumu, temel uzay nesneleri, `Result` tipi ve tag sistemi —
kılavuzun geri kalanını okumadan önce bu bölümü çalıştırın.

---

## 1. Kurulum ve Import

```bash
pip install -e .   # git kökünden
```

Her bölümde ihtiyaç duyulan semboller doğrudan `pytop`'tan import edilir:

```python
import pytop
print("pytop sürümü:", pytop.__version__)
```

---

## 2. Uzay Nesneleri

| Kurucu | Topoloji | Sonuç |
|--------|----------|-------|
| `discrete_topology(*pts)` | Her altküme açık | Ayrık |
| `indiscrete_topology(*pts)` | Yalnız ∅ ve X açık | İndiscrete |
| `sierpinski_space()` | {∅, {1}, {0,1}} | Sierpiński |
| `make_topology(carrier, *open_sets)` | Kullanıcı tanımlı | Özel |

```python
d = discrete_topology(0, 1, 2)
print("carrier:", sorted(d.carrier))
print("topoloji boyutu:", len(d.topology))
print("etiketler:", sorted(d.tags))
```

```text
carrier: [0, 1, 2]
topoloji boyutu: 8
etiketler: ['discrete', 'finite', 'hausdorff', 'metrizable', 'normal', 'regular']
```

---

## 3. Result Tipi

pytop'un çoğu yüklemi bir `Result` nesnesi döner.

```python
s = sierpinski_space()
r = is_t2(s)
print(".status      :", r.status)        # 'true' | 'false' | 'unknown'
print(".value       :", r.value)
print(".mode        :", r.mode)          # 'exact' | 'corridor' | 'assumed'
print(".justification:", r.justification)
```

```text
.status      : false
.value       : hausdorff
.mode        : exact
.justification: ['The explicit finite topology fails hausdorff.']
```

`.status` her zaman `'true'`, `'false'` veya `'unknown'` **dizesidir** — Python
bool'u değil. Karşılaştırmada `r.status == 'true'` kullanın.

---

## 4. Temel Uzaylar Turu

```python
spaces = {
    "Ayrık D(0,1,2)":     discrete_topology(0, 1, 2),
    "İndiscrete I(0,1,2)": indiscrete_topology(0, 1, 2),
    "Sierpinski S":        sierpinski_space(),
}

print(f"{'Uzay':<22} {'kompakt':>8} {'bağlantılı':>11} {'T0':>4} {'T1':>4} {'T2':>4}")
for name, sp in spaces.items():
    print(f"{name:<22} {is_compact(sp).status:>8} {is_connected(sp).status:>11} "
          f"{is_t0(sp).status:>4} {is_t1(sp).status:>4} {is_t2(sp).status:>4}")
```

```text
Uzay                    kompakt  bağlantılı   T0   T1   T2
----------------------------------------------------------
Ayrık D(0,1,2)             true       false true true true
İndiscrete I(0,1,2)        true        true false false false
Sierpinski S               true        true  true false false
```

---

## 5. Özel Topoloji: make_topology

```python
X = [1, 2, 3, 4]
tau = [set(), {1,2}, {3,4}, {1,2,3,4}]
fts = make_topology(X, *tau)
print("topoloji:", sorted([sorted(list(u)) for u in fts.topology],
                          key=lambda x: (len(x), x)))
print("kompakt:", is_compact(fts).status)
print("T2:", is_t2(fts).status)
```

```text
topoloji: [[], [1, 2], [3, 4], [1, 2, 3, 4]]
kompakt: true
T2: false
```

`make_topology` verilen açık kümelerin birleşim ve kesişim kapatmasını otomatik
tamamlar.

---

## 6. Tag Sistemi

```python
print("Ayrık:     ", sorted(discrete_topology(0,1,2).tags))
print("Indiscrete:", sorted(indiscrete_topology(0,1,2).tags))
print("Sierpinski:", sorted(sierpinski_space().tags))
```

```text
Ayrık:      ['discrete', 'finite', 'hausdorff', 'metrizable', 'normal', 'regular']
Indiscrete: ['finite', 'indiscrete']
Sierpinski: ['finite', 'sierpinski']
```

Etiketler yüklem fonksiyonlarının karar mekanizmasını hızlandırır:
`is_t2(d)` açık küme taraması yerine `'hausdorff' in d.tags` kontrolüyle sonuç verir.

---

## 7. n Nokta Üzerindeki Topoloji Sayısı

```python
for n in range(1, 5):
    print(f"n={n}: {count_topologies_on_n_points(n)}")
```

```text
n=1: 1
n=2: 4
n=3: 29
n=4: 355
```

---

## 8. Sıradaki Adım

- **Bölüm 3** — Küme teorisi ve fonksiyon temelleri (matematiksel ön koşullar)
- **Bölüm 4** — Topolojik uzay aksiyomları, baz, alt-baz
- **Bölüm 5** — Açık/kapalı altkümeler, kapanış, iç, sınır
