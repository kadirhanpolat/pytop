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

from .constructed import (
    Construction,
    ProductSpace,
    QuotientSpace,
    SubspaceSpace,
    SumSpace,
)
from .constructions import (
    binary_product,
    disjoint_sum,
    quotient,
    subspace,
)
from .core import (
    CarrierKind,
    Decidability,
    NotEnumerableError,
    Space,
    Verdict,
)
from .pi_base_bridge import (
    PiBaseSpace,
    analyze_pi_base_space,
    pi_base_space,
)
from .predicates import (
    is_compact,
    is_connected,
    is_first_countable,
    is_hausdorff,
    is_lindelof,
    is_normal,
    is_regular,
    is_second_countable,
    is_separable,
    is_t0,
    is_t1,
    is_t3,
    is_t4,
    is_t5,
    is_t6,
    is_tychonoff,
)
from .reasoning import (
    PRESERVATION,
    Derivation,
    derive,
    explain,
    synthesize,
)
from .representations import (
    CofiniteSpace,
    DiscreteCountableSpace,
    FiniteSpace,
    MetricTopologySpace,
    OpaqueInfiniteSpace,
    OrderTopologySpace,
    SorgenfreyLineSpace,
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
    "is_t0",
    "is_t1",
    "is_t3",
    "is_t4",
    "is_tychonoff",
    "is_t5",
    "is_t6",
    "is_regular",
    "is_normal",
    "is_compact",
    "is_connected",
    "is_lindelof",
    "is_separable",
    "is_second_countable",
    "is_first_countable",
    "subspace",
    "binary_product",
    "disjoint_sum",
    "quotient",
    "Construction",
    "ProductSpace",
    "SumSpace",
    "SubspaceSpace",
    "QuotientSpace",
    "PRESERVATION",
    "Derivation",
    "derive",
    "explain",
    "synthesize",
    "PiBaseSpace",
    "pi_base_space",
    "analyze_pi_base_space",
    "FiniteSpace",
    "CofiniteSpace",
    "OrderTopologySpace",
    "MetricTopologySpace",
    "SorgenfreyLineSpace",
    "DiscreteCountableSpace",
    "OpaqueInfiniteSpace",
    "discrete_finite_space",
    "rational_metric_space",
]
