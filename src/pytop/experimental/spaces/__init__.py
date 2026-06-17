"""Computable topological spaces (experimental) — the research-grade foundation.

A unified representation protocol (:class:`Space`) for finite *and*
finitely-presented infinite spaces, with witness-carrying, decidability-honest
predicates. This is Milestone S1 of the roadmap toward research-grade set-theoretic
topology (see ``docs/CAPABILITIES_AND_ROADMAP.md``). API is unstable.

```python
from pytop.experimental.spaces import FiniteSpace, is_hausdorff, rational_metric_space

sierpinski = FiniteSpace("Sierpinski", {0, 1}, [set(), {0}, {0, 1}])
is_hausdorff(sierpinski).value          # False  (decided, with counterexample)
is_hausdorff(rational_metric_space()).value   # True  (decided via metric certificate)
```
"""

from __future__ import annotations

from .core import (
    CarrierKind,
    Decidability,
    NotEnumerableError,
    Space,
    Verdict,
)
from .predicates import is_hausdorff
from .representations import (
    CofiniteSpace,
    FiniteSpace,
    MetricTopologySpace,
    OpaqueInfiniteSpace,
    OrderTopologySpace,
    discrete_finite_space,
    rational_metric_space,
)

__all__ = [
    "CarrierKind",
    "Decidability",
    "NotEnumerableError",
    "Space",
    "Verdict",
    "is_hausdorff",
    "FiniteSpace",
    "CofiniteSpace",
    "OrderTopologySpace",
    "MetricTopologySpace",
    "OpaqueInfiniteSpace",
    "discrete_finite_space",
    "rational_metric_space",
]
