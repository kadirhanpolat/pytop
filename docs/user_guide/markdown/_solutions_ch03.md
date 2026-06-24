# Alıştırma Çözümleri — Bölüm 3

Bu ek, Bölüm 3 (Küme Teorisi) alıştırmalarının tam çözümlerini içerir. Kodlama
çözümlerindeki tüm çıktılar gerçek çalıştırmadan alınmıştır; teori çözümleri tam
argüman verir.

---

## Bölüm 3: Küme Teorisi

### K1 — A∪B, A∩B, A\B

(ch03 K1 alıştırmasına dön)

```python
from pytop import (
    make_set, power_set, set_union, set_intersection, set_difference,
    complement, cartesian_product, equal_sets,
    make_relation, relation_profile, is_equivalence_relation,
    equivalence_class, compose_relations, inverse_relation,
)

A = make_set(1, 2, 3, 4, 5)
B = make_set(3, 4, 5, 6, 7)
print("A u B:", sorted(set_union(A, B)))
print("A n B:", sorted(set_intersection(A, B)))
print("A \\ B:", sorted(set_difference(A, B)))
```

```text
A u B: [1, 2, 3, 4, 5, 6, 7]
A n B: [3, 4, 5]
A \ B: [1, 2]
```

A ∩ B = {3,4,5} ortak elemanlar; A \ B = {1,2} yalnız A'da olanlar.

---

### K2 — {1,2,3,4} güç kümesi

(ch03 K2 alıştırmasına dön)

```python
P = power_set([1, 2, 3, 4])
print("|P({1,2,3,4})| =", len(P))
```

```text
|P({1,2,3,4})| = 16
```

Teorem 2.2 gereği |P(A)| = 2⁴ = 16.

---

### K3 — Tam çarpım bağıntısı denkliktir

(ch03 K3 alıştırmasına dön)

```python
carrier = [0, 1, 2]
R = make_relation(carrier, *[(i, j) for i in carrier for j in carrier])
prof = relation_profile(carrier, R)
print("yansimalı:", prof['is_reflexive'])
print("simetrik :", prof['is_symmetric'])
print("gecisli  :", prof['is_transitive'])
print("denklik  :", is_equivalence_relation(carrier, R))
```

```text
yansimalı: True
simetrik : True
gecisli  : True
denklik  : True
```

Tam çarpım R = A × A her zaman denkliktir: her ikili mevcut olduğundan üç aksiyom
trivially sağlanır. Tek denklik sınıfı tüm taşıyıcıdır.

---

### K5 — Mod-2 denkliği

(ch03 K5 alıştırmasına dön)

```python
c5 = [0, 1, 2, 3, 4]
mod2 = make_relation(c5, *[(i, j) for i in c5 for j in c5 if (i - j) % 2 == 0])
print("[0] =", sorted(equivalence_class(c5, mod2, 0)))
print("[1] =", sorted(equivalence_class(c5, mod2, 1)))
```

```text
[0] = [0, 2, 4]
[1] = [1, 3]
```

İki sınıf: çiftler {0,2,4} ve tekler {1,3}. Bunlar {0,..,4}'ün bir bölüntüsüdür.

---

### K6 — De Morgan (X = {1,…,8})

(ch03 K6 alıştırmasına dön)

```python
X = make_set(1, 2, 3, 4, 5, 6, 7, 8)
A = make_set(1, 2, 3, 4)
B = make_set(3, 4, 5, 6)
dm1_l = complement(set_union(A, B), X)
dm1_r = set_intersection(complement(A, X), complement(B, X))
dm2_l = complement(set_intersection(A, B), X)
dm2_r = set_union(complement(A, X), complement(B, X))
print("(A u B)^c:", sorted(dm1_l), "==", sorted(dm1_r), "->", sorted(dm1_l) == sorted(dm1_r))
print("(A n B)^c:", sorted(dm2_l), "==", sorted(dm2_r), "->", sorted(dm2_l) == sorted(dm2_r))
```

```text
(A u B)^c: [7, 8] == [7, 8] -> True
(A n B)^c: [1, 2, 5, 6, 7, 8] == [1, 2, 5, 6, 7, 8] -> True
```

A ∪ B = {1,…,6} olduğundan tümleyeni {7,8}; A ∩ B = {3,4} olduğundan tümleyeni
{1,2,5,6,7,8}. Her iki De Morgan eşitliği de doğrulanır.

---

### K7 — Kartezyen çarpım değişmeli değildir

(ch03 K7 alıştırmasına dön)

```python
Pp = make_set('x', 'y', 'z')
Qq = make_set(0, 1)
pq = cartesian_product(Pp, Qq)
qp = cartesian_product(Qq, Pp)
print("|PxQ| =", len(pq), "| |QxP| =", len(qp))
print("PxQ == QxP :", equal_sets(pq, qp))
```

```text
|PxQ| = 6 | |QxP| = 6
PxQ == QxP : False
```

Boyutlar eşittir (|P|·|Q| = 3·2 = 6 = |Q|·|P|), ama kümeler farklıdır:
P × Q'nun ikilileri (x,0) biçiminde, Q × P'ninkiler (0,x) biçimindedir.

---

### T1 — A ⊆ B ⟺ A ∩ B = A

(ch03 T1 alıştırmasına dön)

**(⟹)** A ⊆ B varsayalım. A ∩ B ⊆ A her zaman doğrudur. Ters kapsama için
a ∈ A alalım; A ⊆ B olduğundan a ∈ B, dolayısıyla a ∈ A ∩ B. Böylece A ⊆ A ∩ B,
yani A ∩ B = A.

**(⟸)** A ∩ B = A varsayalım. a ∈ A alalım; o halde a ∈ A ∩ B = A, özellikle
a ∈ B. Demek ki A ⊆ B. ∎

---

### T2 — Enjeksiyonların bileşimi enjeksiyondur

(ch03 T2 alıştırmasına dön)

f: A → B ve g: B → C enjeksiyon olsun. (g ∘ f)(a₁) = (g ∘ f)(a₂) varsayalım, yani
g(f(a₁)) = g(f(a₂)). g enjeksiyon olduğundan f(a₁) = f(a₂). f enjeksiyon
olduğundan a₁ = a₂. Dolayısıyla g ∘ f enjeksiyondur. ∎

---

### T3 — (R∘S)⁻¹ = S⁻¹∘R⁻¹ (sonlu doğrulama)

(ch03 T3 alıştırmasına dön)

```python
R = make_relation([1, 2, 3], (1, 2), (2, 3))
S = make_relation([1, 2, 3], (1, 3), (2, 1))
# pytop konvansiyonu: compose_relations(first, second) = second o first
RoS = compose_relations(S, R)          # R o S
lhs = inverse_relation(RoS)            # (R o S)^-1
rhs = compose_relations(inverse_relation(R), inverse_relation(S))  # S^-1 o R^-1
print("(R o S)^-1 :", sorted(lhs))
print("S^-1 o R^-1:", sorted(rhs))
print("esit mi    :", sorted(lhs) == sorted(rhs))
```

```text
(R o S)^-1 : [(2, 2)]
S^-1 o R^-1: [(2, 2)]
esit mi    : True
```

`compose_relations(S, R)` pytop konvansiyonunda R ∘ S'tir (önce S, sonra R). Bu
örnekte R ∘ S = {(2,2)}: S ile 2→1, ardından R ile 1→2. Tersini almak çiftleri
ters çevirir ve sağ taraf S⁻¹ ∘ R⁻¹ ile aynı kümeyi verir — soyut özdeşlik sonlu
örnekte doğrulanır. ∎
