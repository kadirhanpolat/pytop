# %% [markdown]
"""
# Bölüm 2 — Önerme Mantığı

Matematiksel önerme (proposition), doğru ya da yanlış olabilen bir ifadedir.
Bu bölüm `pytop.logic` modülünün sağladığı araçları —
`Proposition`, bağlaçlar ve sonlu niceleyiciler — tanıtır;
ardından bu araçların topolojik uzay özelliklerini doğrulamakta nasıl
kullanıldığını gösterir.
"""

# %%
from pytop import (
    Proposition,
    negate, conjunction, disjunction, implies, iff,
    for_all, there_exists, unique_exists,
)

# %% [markdown]
"""
## 1. Önerme ve Doğruluk Değeri

`Proposition(name, truth_value)` — isimli bir önerme nesnesi oluşturur.
`bool(p)` ve `p.truth_value` doğruluk değerini verir.
"""

# %%
p = Proposition("p", True)
q = Proposition("q", False)
r = Proposition("r", True)

print(f"p : {p.truth_value}")
print(f"q : {q.truth_value}")
print(f"r : {r.truth_value}")
print(f"bool(p): {bool(p)}")

# %% [markdown]
"""
```text
p : True
q : False
r : True
bool(p): True
```
"""

# %% [markdown]
"""
## 2. Mantıksal Bağlaçlar

| Fonksiyon | Sembol | Anlam |
|-----------|--------|-------|
| `negate(p)` | ¬p | p değil |
| `conjunction(p, q)` | p ∧ q | p ve q |
| `disjunction(p, q)` | p ∨ q | p veya q |
| `implies(p, q)` | p → q | p ise q (p yeter koşul, q gerek koşul) |
| `iff(p, q)` | p ↔ q | p ancak ve ancak q |
"""

# %%
print("neg(p)     :", negate(p).truth_value)          # False
print("p and q    :", conjunction(p, q).truth_value)   # False
print("p or q     :", disjunction(p, q).truth_value)   # True
print("p -> q     :", implies(p, q).truth_value)       # False  (T->F = F)
print("p <-> q    :", iff(p, q).truth_value)           # False
print("p <-> p    :", iff(p, p).truth_value)           # True
print("p and q and r:", conjunction(p, q, r).truth_value)  # False

# %% [markdown]
"""
```text
neg(p)     : False
p and q    : False
p or q     : True
p -> q     : False
p <-> q    : False
p <-> p    : True
p and q and r: False
```

`implies(p, q)` yalnızca `p=True, q=False` durumunda yanlıştır; diğer
üç durumda doğrudur (boş doğruluk / vacuous truth).
"""

# %% [markdown]
"""
## 3. Doğruluk Tablosu

Dört temel bağlaç için tam doğruluk tablosu:
"""

# %%
print(f"{'p':>5}  {'q':>5}  {'neg_p':>5}  {'p&q':>5}  {'p|q':>5}  {'p->q':>6}  {'p<->q':>6}")
print("-" * 52)
for tv_p in (True, False):
    for tv_q in (True, False):
        pp = Proposition("p", tv_p)
        qq = Proposition("q", tv_q)
        row = (
            pp.truth_value,
            qq.truth_value,
            negate(pp).truth_value,
            conjunction(pp, qq).truth_value,
            disjunction(pp, qq).truth_value,
            implies(pp, qq).truth_value,
            iff(pp, qq).truth_value,
        )
        print("  ".join(f"{str(v):>5}" for v in row))

# %% [markdown]
"""
```text
    p      q  neg_p    p&q    p|q   p->q  p<->q
----------------------------------------------------
 True   True  False   True   True   True   True
 True  False  False  False   True  False  False
False   True   True  False   True   True  False
False  False   True  False  False   True   True
```
"""

# %% [markdown]
"""
## 4. Önemli Tautolojiler

Tautoloji: her doğruluk değeri atamasında doğru olan önerme.
"""

# %%
pairs = [(True, True), (True, False), (False, True), (False, False)]

def check_tautology(name, func):
    results = [func(Proposition("p", tv_p), Proposition("q", tv_q))
               for tv_p, tv_q in pairs]
    ok = all(r.truth_value for r in results)
    print(f"{name}: {'tautoloji' if ok else 'DEGIL'}")

# De Morgan yasalari
check_tautology(
    "neg(p&q) <-> neg_p|neg_q",
    lambda p, q: iff(negate(conjunction(p, q)), disjunction(negate(p), negate(q)))
)
check_tautology(
    "neg(p|q) <-> neg_p&neg_q",
    lambda p, q: iff(negate(disjunction(p, q)), conjunction(negate(p), negate(q)))
)

# Karsit (contrapositive)
check_tautology(
    "(p->q) <-> (neg_q->neg_p)",
    lambda p, q: iff(implies(p, q), implies(negate(q), negate(p)))
)

# p -> p (ozdes)
def check_single(name, func):
    results = [func(Proposition("p", tv)) for tv in (True, False)]
    ok = all(r.truth_value for r in results)
    print(f"{name}: {'tautoloji' if ok else 'DEGIL'}")

check_single("p -> p", lambda p: implies(p, p))
check_single("p | neg_p (excluded middle)", lambda p: disjunction(p, negate(p)))

# %% [markdown]
"""
```text
neg(p&q) <-> neg_p|neg_q: tautoloji
neg(p|q) <-> neg_p&neg_q: tautoloji
(p->q) <-> (neg_q->neg_p): tautoloji
p -> p: tautoloji
p | neg_p (excluded middle): tautoloji
```
"""

# %% [markdown]
"""
## 5. Niceleyiciler

`for_all`, `there_exists`, `unique_exists` sonlu taşıyıcı üzerinde ∀, ∃, ∃! niceleyicileri uygular.

```python
for_all(carrier, predicate)       # ∀x ∈ carrier : P(x)
there_exists(carrier, predicate)  # ∃x ∈ carrier : P(x)
unique_exists(carrier, predicate) # ∃!x ∈ carrier : P(x)
```
"""

# %%
X = [1, 2, 3, 4, 5]

print("for_all(X, x>0)       :", for_all(X, lambda x: x > 0))    # True
print("for_all(X, x>2)       :", for_all(X, lambda x: x > 2))    # False
print("there_exists(X, x>4)  :", there_exists(X, lambda x: x > 4))  # True
print("there_exists(X, x>5)  :", there_exists(X, lambda x: x > 5))  # False
print("unique_exists(X, x==3):", unique_exists(X, lambda x: x == 3))  # True
print("unique_exists(X, x>3) :", unique_exists(X, lambda x: x > 3))   # False (>1 eleman)
print("unique_exists(X, x>5) :", unique_exists(X, lambda x: x > 5))   # False (0 eleman)

# %% [markdown]
"""
```text
for_all(X, x>0)       : True
for_all(X, x>2)       : False
there_exists(X, x>4)  : True
there_exists(X, x>5)  : False
unique_exists(X, x==3): True
unique_exists(X, x>3) : False
unique_exists(X, x>5) : False
```

`unique_exists` yalnızca tam bir eleman sayıldığında `True` döner;
sıfır veya birden fazlada `False`.
"""

# %% [markdown]
"""
## 6. Topoloji Uygulaması — Ayrılma Aksiyomları

Ayrılma aksiyomları T0 ve T1 doğal olarak ∀∃ niceleyici ifadeleridir.

**T0 (Kolmogorov):**
∀x ≠ y ∈ X, ∃ açık U : (x ∈ U, y ∉ U) veya (y ∈ U, x ∉ U)

**T1 (Fréchet):**
∀x ≠ y ∈ X, ∃ açık U : x ∈ U, y ∉ U
"""

# %%
from pytop import sierpinski_space, discrete_topology, indiscrete_topology

def is_t0_logic(space):
    pts   = list(space.carrier)
    opens = list(space.topology)
    return for_all(
        [(x, y) for x in pts for y in pts if x != y],
        lambda pair: there_exists(
            opens,
            lambda U: (pair[0] in U) != (pair[1] in U)
        )
    )

def is_t1_logic(space):
    pts   = list(space.carrier)
    opens = list(space.topology)
    return for_all(
        [(x, y) for x in pts for y in pts if x != y],
        lambda pair: there_exists(
            opens,
            lambda U: pair[0] in U and pair[1] not in U
        )
    )

spaces = {
    "Sierpinski": sierpinski_space(),
    "Discrete  ": discrete_topology(0, 1),
    "Indiscrete": indiscrete_topology(0, 1),
}

print(f"{'Uzay':<12}  T0     T1")
print("-" * 26)
for name, sp in spaces.items():
    t0 = is_t0_logic(sp)
    t1 = is_t1_logic(sp)
    print(f"{name}  {str(t0):<5}  {str(t1):<5}")

# %% [markdown]
"""
```text
Uzay          T0     T1
--------------------------
Sierpinski    True   False
Discrete      True   True
Indiscrete    False  False
```

`for_all` ve `there_exists` ile yazılan T0/T1 tanımları, `pytop`'un
`is_t0` ve `is_t1` yüklemlerinin sonuçlarıyla örtüşür.
Bu yaklaşım, aksiyomun tam tanımını kod olarak belgelemek için kullanışlıdır.
"""

# %% [markdown]
"""
## Alıştırmalar

1. Beş önerme değeriyle tam bir doğruluk tablosu oluşturun ve tüm
   olası `(p, q)` çiftleri için `implies` yalnızca kaçında `False` döner?

2. `unique_exists([0,1,2,3,4], predicate)` değerini `True` yapan
   üç farklı koşul (predicate) yazın.

3. T2 (Hausdorff) aksiyomunu `for_all` ve `there_exists` kullanarak
   tanımlayın: ∀x ≠ y, ∃ açık U, V: x ∈ U, y ∈ V, U ∩ V = ∅.
   Bu tanımı sierpinski_space, discrete_topology, indiscrete_topology için test edin.

4. *(Teori)* `implies(p, q)` neden yalnızca `p=True, q=False` durumunda
   yanlıştır? "Boş doğruluk" (vacuous truth) kavramını açıklayın.

5. *(Teori)* De Morgan yasalarını önerme mantığı için ispatlayın:
   ¬(p ∧ q) ↔ ¬p ∨ ¬q.
"""

# %%
if __name__ == "__main__":
    pass
