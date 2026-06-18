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

from .cardinal_invariants import (
    CardinalValue,
    cellularity,
    character,
    density,
    weight,
)
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
from .pi1 import (
    Pi1Result,
    pi1_space,
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
    AlexandroffSpace,
    CofiniteSpace,
    DiscreteCountableSpace,
    FiniteSpace,
    InverseLimitSpace,
    MetricTopologySpace,
    OpaqueInfiniteSpace,
    OrderTopologySpace,
    SorgenfreyLineSpace,
    SubbaseSpace,
    discrete_finite_space,
    finite_circle,
    finite_sphere,
    finite_wedge_circles,
    rational_metric_space,
)
from .urysohn import (
    UrysohnWitness,
    urysohn_function,
)

__all__ = [
    # Core protocol
    "CarrierKind",
    "Decidability",
    "NotEnumerableError",
    "Space",
    "Verdict",
    # π₁ computation
    "Pi1Result",
    "pi1_space",
    # Urysohn witnesses
    "UrysohnWitness",
    "urysohn_function",
    # Cardinal invariants
    "CardinalValue",
    "weight",
    "density",
    "character",
    "cellularity",
    # Separation predicates
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
    # Covering and connectedness predicates
    "is_compact",
    "is_connected",
    "is_lindelof",
    "is_separable",
    "is_second_countable",
    "is_first_countable",
    # Construction functions
    "subspace",
    "binary_product",
    "disjoint_sum",
    "quotient",
    # Construction wrappers
    "Construction",
    "ProductSpace",
    "SumSpace",
    "SubspaceSpace",
    "QuotientSpace",
    # Reasoning engine
    "PRESERVATION",
    "Derivation",
    "derive",
    "explain",
    "synthesize",
    # pi-Base bridge
    "PiBaseSpace",
    "pi_base_space",
    "analyze_pi_base_space",
    # Representations
    "AlexandroffSpace",
    "CofiniteSpace",
    "DiscreteCountableSpace",
    "FiniteSpace",
    "InverseLimitSpace",
    "MetricTopologySpace",
    "OpaqueInfiniteSpace",
    "OrderTopologySpace",
    "SorgenfreyLineSpace",
    "SubbaseSpace",
    "discrete_finite_space",
    "finite_circle",
    "finite_sphere",
    "finite_wedge_circles",
    "rational_metric_space",
]
