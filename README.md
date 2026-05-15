# pytop

A mathematical topology library for Python, covering point-set topology, knot theory, graph topology, surface classification, 3-manifolds, and more.

## Installation

```bash
pip install -e .
```

Requires Python 3.11+.

## Quick Start

```python
import pytop

# Spaces and maps
from pytop import TopologicalSpace, continuous_map_profile

# Compactness
from pytop import is_compact, CompactnessProfile

# Knot theory
from pytop import KnotProfile, reidemeister_move_profiles

# Surface classification
from pytop import SurfaceProfile, euler_characteristic_profile

# Degree theory
from pytop import get_retraction_degree_profiles, winding_number_profiles

# Experimental (unstable API)
from pytop.experimental import maturity_registry
```

## Module Overview

| Domain | Key modules |
|--------|-------------|
| Foundations | `sets`, `relations`, `spaces`, `maps`, `predicates` |
| Metric spaces | `metric_spaces`, `metric_completeness`, `metrization_profiles` |
| Compactness | `compactness`, `compactness_variants`, `local_compactness` |
| Connectivity | `connectedness`, `paths`, `covering_spaces` |
| Separation axioms | `separation`, `countability` |
| Degree theory | `degree_theory`, `degree_theory_applications` |
| Knot theory | `knots`, `invariants` |
| Surfaces & manifolds | `surfaces`, `surface_classification`, `manifolds`, `three_manifolds` |
| Graph topology | `graph_topology` |
| Cardinal functions | `cardinal_functions_framework`, `cardinal_numbers` |
| Cosmology | `cosmology_topology` |
| Experimental | `pytop.experimental` |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
