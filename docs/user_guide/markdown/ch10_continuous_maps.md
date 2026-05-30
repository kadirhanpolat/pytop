# Bölüm 10 — Sürekli Fonksiyonlar ve Homeomorfizmalar

Topolojik uzaylar arasındaki fonksiyonlarda süreklilik, açık kümelerin
geri çekiminin (preimage) açık olması koşuluna dayanır. Homeomorfizma ise
topolojik yapıyı tam olarak koruyan bijektif sürekli fonksiyondur.

---

## 1. Konu

### Süreklilik Tanımı

f: (X, τ_X) → (Y, τ_Y) fonksiyonu **sürekli** ise:

    ∀ V ∈ τ_Y: f⁻¹(V) ∈ τ_X

Eşdeğer koşullar:
- Her kapalı F ⊆ Y için f⁻¹(F) kapalıdır.
- Her x ∈ X ve f(x)'in her komşuluğu W için f⁻¹(W), x'in komşuluğudur.

### Süreklilik Hiyerarşisi

| Tür | Koşul |
|-----|-------|
| **Sabit fonksiyon** | f(x) = c; her zaman sürekli |
| **Özdeşlik** | f(x) = x; her zaman sürekli |
| **Bileşke** | f, g sürekli ⟹ g∘f sürekli |
| **Homeomorfizma** | Bijektif, f ve f⁻¹ sürekli |

### Görüntü ve Geri Çekim

- **Görüntü:** f(A) = {f(x) : x ∈ A}
- **Geri çekim:** f⁻¹(B) = {x ∈ X : f(x) ∈ B}

---

## 2. Teoremler

**Teorem 2.1.** Her sabit fonksiyon süreklidir.
*(Kanıt: f⁻¹(V) = X eğer c ∈ V, ∅ eğer c ∉ V; her ikisi de açık.)*

**Teorem 2.2.** f: X → Y ve g: Y → Z sürekli ⟹ g∘f sürekli.

**Teorem 2.3.** f: X → Y sürekli, X kompakt ⟹ f(X) kompakttır.

**Teorem 2.4.** f: X → Y sürekli, X bağlantılı ⟹ f(X) bağlantılıdır.

**Teorem 2.5.** f: X → Y homeomorfizma ⟺ bijektif, f sürekli, f⁻¹ sürekli.

**Teorem 2.6.** Kompakt X'ten Hausdorff Y'ye sürekli bijeksiyon ⟹ homeomorfizma.

---

## 3. Algoritmalar

### is_continuous_finite_map — O(|τ_Y| · |X|)

```
IsContinuous(X, tau_X, Y, tau_Y, f):
    for each V in tau_Y:
        preimage <- {x in X : f(x) in V}
        if preimage not in tau_X: return False
    return True
```

Her açık küme için geri çekim hesaplanır.

---

## 4. pytop API

```python
from pytop import (
    is_continuous_finite_map,
    finite_homeomorphism_result,
    sierpinski_space,
    discrete_topology,
    indiscrete_topology,
)
```

`is_continuous_finite_map(domain, domain_topology, codomain, codomain_topology, mapping)` → `bool`

`finite_homeomorphism_result(left, right)` → `Result` (.status: 'true'/'false')

---

## 5. Örnekler

### Örnek 5.1 — Sabit Fonksiyon: Her Zaman Sürekli

```python
s = sierpinski_space()
s_pts = list(s.carrier)
s_topo = [set(u) for u in s.topology]

f_const = {0: 1, 1: 1}
result = is_continuous_finite_map(s_pts, s_topo, s_pts, s_topo, f_const)
print("continuous:", result)
```

```text
continuous: True
```

### Örnek 5.2 — Ayrık Topoloji: Her Fonksiyon Sürekli

```python
d = discrete_topology(0, 1)
d_pts = list(d.carrier)
d_topo = [set(u) for u in d.topology]

f_id   = {0: 0, 1: 1}
f_swap = {0: 1, 1: 0}
print("ozdeslik continuous:", is_continuous_finite_map(d_pts, d_topo, d_pts, d_topo, f_id))
print("swap     continuous:", is_continuous_finite_map(d_pts, d_topo, d_pts, d_topo, f_swap))
```

```text
ozdeslik continuous: True
swap     continuous: True
```

Ayrık topolojide her fonksiyon süreklidir: geri çekim her zaman açıktır.

### Örnek 5.3 — Sierpiński → Ayrık: Sürekli Değil

```python
print("id: Sierpinski -> Disc:", is_continuous_finite_map(s_pts, s_topo, d_pts, d_topo, f_id))
print("id: Disc -> Sierpinski:", is_continuous_finite_map(d_pts, d_topo, s_pts, s_topo, f_id))
```

```text
id: Sierpinski -> Disc continuous: False
id: Disc -> Sierpinski continuous: True
```

Sierpiński τ = {∅, {0,1}, {1}}: id: S→D'de f⁻¹({0}) = {0} — Sierpiński'de açık değil.

### Örnek 5.4 — İndiscrete'ten Süreklilik

```python
ind = indiscrete_topology(0, 1)
ind_pts = list(ind.carrier)
ind_topo = [set(u) for u in ind.topology]

f_const0 = {0: 0, 1: 0}
print("id (0->0,1->1)    continuous:", is_continuous_finite_map(ind_pts, ind_topo, s_pts, s_topo, f_id))
print("const_0 (tum->0)  continuous:", is_continuous_finite_map(ind_pts, ind_topo, s_pts, s_topo, f_const0))
```

```text
id (0->0, 1->1) continuous: False
const_0 (tum->0) continuous: True
```

İndiscrete'den süreklilik: f⁻¹(V) ∈ {∅, X} olmalı. Sabit fonksiyon sağlar, özdeşlik sağlamaz.

### Örnek 5.5 — Homeomorfizma Kontrolü

```python
d2a = discrete_topology(1, 2)
d2b = discrete_topology('a', 'b')
ind2 = indiscrete_topology(1, 2)

print("D(1,2) ~ D(a,b):", finite_homeomorphism_result(d2a, d2b).status)
print("D(1,2) ~ S(0,1):", finite_homeomorphism_result(d2a, s).status)
print("D(1,2) ~ Ind(1,2):", finite_homeomorphism_result(d2a, ind2).status)
```

```text
D(1,2) ~ D(a,b): true
D(1,2) ~ S(0,1): false
D(1,2) ~ Ind(1,2): false
```

### Örnek 5.6 — Özel Topolojili Süreklilik

```python
X = [1, 2, 3]
tau_X = [set(), {1}, {2, 3}, {1, 2, 3}]
f_23swap = {1: 1, 2: 3, 3: 2}
print("2-3 swap surekli mi:", is_continuous_finite_map(X, tau_X, X, tau_X, f_23swap))
```

```text
2-3 swap surekli mi: True
```

---

## 6. Alıştırmalar

### Kodlama

K1. `make_topology([0,1,2], set(), {0}, {0,1}, {0,1,2})` topolojisinde
    f(0)=0, f(1)=0, f(2)=1 fonksiyonunun sürekli olup olmadığını kontrol edin.

K2. Sierpiński uzayından kendisine giden dört fonksiyonu (sabit 0, sabit 1,
    özdeşlik, swap) test edin: hangileri sürekli?

K3. `finite_homeomorphism_result` ile {1,2,3} ayrık ve {a,b,c} ayrık
    topolojilerinin homeomorf olduğunu doğrulayın.

### Teori

T1. Her sabit fonksiyonun sürekli olduğunu ispatlayın.

T2. f: X → Y ve g: Y → Z sürekli ⟹ g∘f sürekli olduğunu ispatlayın.
