# Yakınsama Uzayları (deneysel) -- CONV-01

- Sürüm: `v0.6.0`
- Hat: `CONV-01`
- Kaynak odağı: Dolecki, *A Royal Road to Topology* (2024)
- Dil ilkesi: Bu dosya Türkçedir; Python API adları paket standardı gereği
  İngilizce tutulmuştur.

## 1. Ne Modelliyoruz?

Bir **yakınsama uzayı**, hangi filtrelerin hangi noktalara yakınsadığını belirtir
ve bu yakınsamanın bir topolojiden gelmesini gerektirmez — topolojinin gerçek bir
genellemesidir. Sonlu taşıyıcıda her filtre asaldır, dolayısıyla bir filtre
çekirdeğiyle (üyelerinin kesişimi, boş olmayan bir alt küme) belirlenir. Bu sayede
tüm hiyerarşi hesaplanabilir hale gelir:

```text
yakınsama uzayı  ⊋  pretopoloji = pseudotopoloji (sonlu)  ⊋  topoloji
```

Modül `pytop.experimental` altındadır (API olgunlaşınca çekirdeğe terfi edecek).

## 2. Topoloji ↔ Yakınsama Köprüsü (gidiş-dönüş)

```python
from pytop.experimental.convergence_spaces import (
    convergence_from_topology, topology_from_convergence, is_topological,
)

# Sierpiński uzayı: açıklar {∅, {0}, {0,1}}
space = convergence_from_topology({0, 1}, [set(), {0}, {0, 1}])
print(is_topological(space))                       # True
print(topology_from_convergence(space) == frozenset(
    {frozenset(), frozenset({0}), frozenset({0, 1})}))   # True (geri kazanım)
```

## 3. Hiyerarşinin Katmanları

```python
from pytop.experimental.convergence_spaces import (
    ConvergenceSpace, is_convergence_space, is_pretopology, is_topological,
)

# Pretopoloji olup topoloji OLMAYAN örnek: U_0={0,1} ama 1∈U_0 iken U_1={1,2} ⊄ U_0
from itertools import combinations
def subsets(s):
    s = list(s)
    return [frozenset(c) for k in range(1, len(s)+1) for c in combinations(s, k)]

nbhd = {0: {0, 1}, 1: {1, 2}, 2: {2}}
conv = [(sub, x) for x, U in nbhd.items() for sub in subsets(U)]
space = ConvergenceSpace({0, 1, 2}, conv)
print(is_convergence_space(space), is_pretopology(space), is_topological(space))
# True True False
```

## 4. Süreklilik ve Grill

```python
from pytop.experimental.convergence_spaces import (
    convergence_from_topology, is_continuous_convergence_map, grill_of_filter,
)

s = convergence_from_topology({0, 1}, [set(), {0}, {0, 1}])
print(is_continuous_convergence_map(s, s, {0: 0, 1: 1}))   # True (özdeşlik)
print(is_continuous_convergence_map(s, s, {0: 1, 1: 0}))   # False (takas)

# Asal filtrenin grill'i: çekirdeği kesen kümeler
print(grill_of_filter({0}, {0, 1}))   # {{0}, {0,1}}
```

## 5. Köprü

Bu modül, `filters.py`/`nets.py`'nin *topoloji üzerindeki* yakınsamasını,
yakınsamanın kendisinin birinci sınıf nesne olduğu bir çerçeveye taşır. Sonlu
taşıyıcıda pretopoloji ile pseudotopoloji çakışır (bkz. modül docstring'i).
