# Bölüm 11 — Alt Uzay ve Çarpım Topolojisi

Alt uzay topolojisi bir uzayın alt kümesine "miras kalan" topolojiyi tanımlar.
Çarpım topolojisi ise iki veya daha fazla uzayı birleştirerek yeni bir uzay kurar.

---

## 1. Konu

### Alt Uzay Topolojisi

(X, τ) topolojik uzayı ve A ⊆ X verilsin. **Alt uzay topolojisi:**

    τ_A = {U ∩ A : U ∈ τ}

(A, τ_A) bir topolojik uzaydır; dahil etme i: A → X süreklidir.

### Çarpım Topolojisi

(X, τ_X) ve (Y, τ_Y) verilsin. **Çarpım topolojisi** X × Y üzerinde
{U × V : U ∈ τ_X, V ∈ τ_Y} bazından üretilen topolojidir.

Projeksiyon π_X: X × Y → X ve π_Y: X × Y → Y süreklidir.
τ_{X×Y} her iki projektiyonu sürekli kılan **en kaba** topolojidir.

### Topolojik Özelliklerin Kalıtımı

| Özellik | Alt uzay | Çarpım |
|---------|----------|--------|
| Hausdorff | ✓ (kalıtır) | ✓ |
| Kompaktlık | Yalnız kapalı alt uzay | ✓ (Tychonoff) |
| Bağlantılılık | Genel olarak hayır | ✓ |
| T0/T1/T2 | ✓ | ✓ |

---

## 2. Teoremler

**Teorem 2.1.** Hausdorff uzayın her alt uzayı Hausdorff'tur.

**Teorem 2.2.** Kompakt uzayın kapalı alt uzayı kompakttır.

**Teorem 2.3.** X ve Y bağlantılı ⟹ X × Y bağlantılıdır.

**Teorem 2.4.** X ve Y kompakt ⟹ X × Y kompakt. (Tychonoff, n=2)

**Teorem 2.5.** X ve Y Hausdorff ⟹ X × Y Hausdorff.

**Teorem 2.6 (Evrensel Özellik — Çarpım).**
f: Z → X × Y sürekli ⟺ π_X∘f ve π_Y∘f süreklidir.

---

## 3. Algoritmalar

### finite_subspace — O(|τ| · |A|)

```
Subspace(X, tau, A):
    tau_A <- {}
    for each U in tau:
        tau_A.add(U ∩ A)
    return (A, tau_A)
```

### binary_product — O(|τ_X| · |τ_Y|)

```
Product(X, tau_X, Y, tau_Y):
    basis <- {U x V : U in tau_X, V in tau_Y}
    return topology_from_basis(X x Y, basis)
```

---

## 4. pytop API

```python
from pytop import (
    finite_subspace,
    binary_product,
    sierpinski_space,
    discrete_topology,
    indiscrete_topology,
    make_topology,
    is_compact,
    is_connected,
    is_t2,
)
```

`finite_subspace(space, subset)` → `FiniteTopologicalSpace`

`binary_product(left, right)` → `FiniteTopologicalSpace` (carrier: tuple çiftleri)

---

## 5. Örnekler

### Örnek 5.1 — Alt Uzay: Ayrık Topoloji

```python
d4 = discrete_topology(1, 2, 3, 4)
sub12 = finite_subspace(d4, [1, 2])
print("carrier:", sub12.carrier)
print("topology:", sorted([sorted(list(u)) for u in sub12.topology], key=lambda x: (len(x), x)))
```

```text
carrier: (1, 2)
topology: [[], [1], [2], [1, 2]]
```

Ayrık topolojinin alt uzayı da ayrıktır: U ∩ A her A ⊆ X için açıktır.

### Örnek 5.2 — Alt Uzay: Sierpiński

```python
s = sierpinski_space()
sub0 = finite_subspace(s, [0])
sub1 = finite_subspace(s, [1])
print("carrier {0}:", sub0.carrier, "| topology:", list(sub0.topology))
print("carrier {1}:", sub1.carrier, "| topology:", list(sub1.topology))
```

```text
carrier {0}: (0,)  | topology: [set(), {0}]
carrier {1}: (1,)  | topology: [set(), {1}]
```

### Örnek 5.3 — Alt Uzay: Özel Topoloji

```python
X = [1, 2, 3, 4, 5]
tau_X = [set(), {1,2}, {3,4}, {1,2,3,4}, {1,2,3,4,5}]
fts = make_topology(X, *tau_X)
sub_A = finite_subspace(fts, [2, 3, 4])
print("carrier:", sub_A.carrier)
print("tau_A:", sorted([sorted(list(u)) for u in sub_A.topology], key=lambda x: (len(x),x)))
```

```text
carrier: (2, 3, 4)
tau_A: [[], [2], [3, 4], [2, 3, 4]]
```

τ_A = {∅∩A, {1,2}∩A, {3,4}∩A, {1,2,3,4}∩A, X∩A} = {∅, {2}, {3,4}, {2,3,4}}.

### Örnek 5.4 — Çarpım: D(0,1) × D(0,1)

```python
d2 = discrete_topology(0, 1)
prod_dd = binary_product(d2, d2)
print("carrier:", sorted(prod_dd.carrier))
print("topology size:", len(list(prod_dd.topology)))
print("compact:", is_compact(prod_dd).status)
print("connected:", is_connected(prod_dd).status)
```

```text
carrier: [(0, 0), (0, 1), (1, 0), (1, 1)]
topology size: 16
compact: true
connected: false
```

D(0,1) × D(0,1): 4 nokta, 2⁴ = 16 açık küme. Ayrık → bağlantısız.

### Örnek 5.5 — Çarpım: Sierpiński × Sierpiński

```python
ss = binary_product(s, s)
print("carrier:", sorted(ss.carrier))
print("topology size:", len(list(ss.topology)))
print("compact:", is_compact(ss).status)
print("connected:", is_connected(ss).status)
```

```text
carrier: [(0, 0), (0, 1), (1, 0), (1, 1)]
topology size: 6
compact: true
connected: true
```

Sierpiński bağlantılı → çarpım da bağlantılı.

### Örnek 5.6 — Topolojik Özellik Kalıtımı

```python
d3 = discrete_topology(1, 2, 3)
ind3 = indiscrete_topology(1, 2, 3)
prod_di = binary_product(d3, ind3)
print("topology size:", len(list(prod_di.topology)))
print("compact:", is_compact(prod_di).status)
print("connected:", is_connected(prod_di).status)
print("T2:", is_t2(prod_di).status)
```

```text
topology size: 8
compact: true
connected: false
T2: false
```

İndiscrete bağlantılı ama D ayrık → çarpım bağlantısız. D T2 ama Ind değil → çarpım T2 değil.

---

## 6. Alıştırmalar

### Kodlama

K1. `sierpinski_space()` uzayının {0} ve {1} alt uzaylarını oluşturun.
    Her birinin hangi topolojiyi taşıdığını belirleyin.

K2. `make_topology([1,2,3,4], set(), {1,2}, {3,4}, {1,2,3,4})` ile bir uzay
    tanımlayın ve {2,3} alt uzayını bulun.

K3. `binary_product(sierpinski_space(), discrete_topology(0,1))` için
    `is_compact` ve `is_connected` kontrol edin.

### Teori

T1. Alt uzay topolojisinde i: A → X dahil etme fonksiyonunun sürekli
    olduğunu ispatlayın.

T2. X ve Y bağlantılı ⟹ X × Y bağlantılı olduğunu ispatlayın.
    (İpucu: {x₀} × Y ve X × {y₀} gibi bağlantılı dilimleri kullanın.)
